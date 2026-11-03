"""Downloads and hashes bank reports. The only module besides pull_data.py that touches the network (rule 8).

usage:
  python scripts/fetch_reports.py [--bank ID ...] [--force]   download every row of data/manual/report_urls.csv
  python scripts/fetch_reports.py --cache-pages               rebuild data/raw/report_text/ (no network)

Download (PLAN step 2.2): each document goes to data/reports/ (gitignored) as {bank_id}_{doc_type}_{period}.pdf, or
.xlsx / .xls for a Pillar 3 workbook, or the PDF inside a ZIP served by the EBA Data Hub (instruction 02b B.3), and
data/raw/report_manifest.csv gets bank_id, doc_type, period, url, sha256, bytes, pages, downloaded_utc. A row already
in the manifest with the same url is skipped unless --force. A document that cannot be downloaded, or is not a PDF,
is printed and left out of the manifest (instruction 02 step 2.2: listed, not a stop). The full page text of each
PDF is also written to data/reports/text/{sha256}.jsonl.gz (gitignored) for locating figures.

Page cache (instruction 02 B.4): data/raw/report_text/{sha256}.jsonl.gz holds only the pages cited by at least 1
row of data/manual/report_entries.csv, data/manual/mergers.csv or
data/manual/one_offs.csv. Each line is {"page": n, "text": ...}, with n the
1 based physical page index and the text extracted by pdfplumber. Cache files no longer cited are removed.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import subprocess
import sys
import time
import zipfile
from datetime import UTC, datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
URLS = ROOT / "data" / "manual" / "report_urls.csv"
ENTRIES = ROOT / "data" / "manual" / "report_entries.csv"
MERGERS = ROOT / "data" / "manual" / "mergers.csv"
ONE_OFFS = ROOT / "data" / "manual" / "one_offs.csv"
MANIFEST = ROOT / "data" / "raw" / "report_manifest.csv"
CACHE = ROOT / "data" / "raw" / "report_text"
REPORTS = ROOT / "data" / "reports"
SEARCH_TEXT = REPORTS / "text"
MANIFEST_COLUMNS = ["bank_id", "doc_type", "period", "url", "sha256", "bytes", "pages", "downloaded_utc"]
HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/126.0 Safari/537.36"),
    "Accept": "application/pdf,application/octet-stream;q=0.9,*/*;q=0.8",
}
CHUNK = 1 << 20


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_manifest(rows: list[dict]) -> None:
    rows = sorted(rows, key=lambda r: (r["bank_id"], r["doc_type"], r["period"]))
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=MANIFEST_COLUMNS, lineterminator="\n")
    w.writeheader()
    w.writerows({k: r[k] for k in MANIFEST_COLUMNS} for r in rows)
    MANIFEST.write_bytes(buf.getvalue().encode("utf-8"))


DOC_EXTS = ("pdf", "xlsx", "xls")  # instruction 02b B.3: a Pillar 3 workbook is a valid source


def pdf_path(bank_id: str, doc_type: str, period: str, ext: str | None = None) -> Path:
    """The downloaded document: {bank_id}_{doc_type}_{period}.{pdf|xlsx|xls}; without ext, the one on disk."""
    stem = REPORTS / f"{bank_id}_{doc_type}_{period}"
    if ext:
        return stem.with_name(stem.name + "." + ext)
    for e in DOC_EXTS:
        if stem.with_name(stem.name + "." + e).exists():
            return stem.with_name(stem.name + "." + e)
    return stem.with_name(stem.name + ".pdf")


def kind_of(path: Path) -> str | None:
    """pdf, xlsx, xls, zip_pdf (a ZIP holding a PDF, as the EBA Pillar 3 Data Hub serves), or None."""
    with open(path, "rb") as f:
        head = f.read(1024)
    if b"%PDF" in head:
        return "pdf"
    if head.startswith(bytes.fromhex("d0cf11e0")):  # OLE2: an .xls workbook
        return "xls"
    if head.startswith(b"PK"):
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
        if "[Content_Types].xml" in names and any(n.startswith("xl/") for n in names):
            return "xlsx"
        if any(n.lower().endswith(".pdf") for n in names):
            return "zip_pdf"
    return None


def _cell(v) -> str:
    """A cell value as text: numbers in shortest form at 15 significant digits, strings with tabs and newlines as
    spaces, empty cells blank."""
    if v is None:
        return ""
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, int | float):
        s = format(v, ".15g")
        if "e" in s:  # never an exponent: provenance reads plain decimal numbers
            s = format(v, ".15f").rstrip("0").rstrip(".")
        return s
    return " ".join(str(v).split())


def sheet_texts(path: Path) -> dict[str, str]:
    """Every sheet of a workbook as text: one line per row, cell values tab separated, trailing blanks dropped
    (instruction 02b B.3)."""
    out = {}
    if path.suffix == ".xls":
        import xlrd

        book = xlrd.open_workbook(path)
        for sh in book.sheets():
            rows = [[_cell(sh.cell_value(r, c)) if sh.cell_type(r, c) not in (0, 6) else ""
                     for c in range(sh.ncols)] for r in range(sh.nrows)]
            out[sh.name] = "\n".join("\t".join(r).rstrip("\t") for r in rows)
    else:
        import openpyxl

        book = openpyxl.load_workbook(path, read_only=True, data_only=True)
        for sh in book.worksheets:
            lines = ["\t".join(_cell(v) for v in row).rstrip("\t") for row in sh.iter_rows(values_only=True)]
            out[sh.title] = "\n".join(lines)
        book.close()
    return out


def _accept(tmp: Path, stem: Path) -> tuple[Path | None, str]:
    """Moves a finished download into place by kind; a ZIP holding a PDF keeps the PDF. (path, "") or (None, why)."""
    kind = kind_of(tmp)
    if kind is None:
        with open(tmp, "rb") as f:
            head = f.read(40)
        tmp.unlink()
        return None, f"not a PDF or workbook (starts {head!r})"
    if kind == "zip_pdf":
        with zipfile.ZipFile(tmp) as z:
            pdfs = sorted(n for n in z.namelist() if n.lower().endswith(".pdf"))
            dest = stem.with_name(stem.name + ".pdf")
            dest.write_bytes(z.read(pdfs[0]))
        tmp.unlink()
        return dest, ""
    dest = stem.with_name(stem.name + "." + kind)
    tmp.replace(dest)
    return dest, ""


def download(url: str, stem: Path, attempts: int = 3) -> tuple[Path | None, str]:
    """Downloads url to stem.{pdf|xlsx|xls}. Returns (path, "") on success, else (None, the reason)."""
    stem.parent.mkdir(parents=True, exist_ok=True)
    tmp = stem.with_name(stem.name + ".part")
    reason = ""
    for i in range(attempts):
        # some hosts refuse a browser user agent but serve the library default: the last attempt sends no headers
        headers = HEADERS if i < attempts - 1 else None
        try:
            with requests.get(url, headers=headers, stream=True, timeout=180) as r:
                r.raise_for_status()
                with open(tmp, "wb") as f:
                    f.writelines(r.iter_content(CHUNK))
            return _accept(tmp, stem)
        except requests.exceptions.SSLError as e:
            # certifi lacks the chain some hosts serve; curl verifies against the operating system's store instead
            reason = str(e)
            r = subprocess.run(["curl", "-sSfL", "-A", HEADERS["User-Agent"], "-o", str(tmp), url],
                               capture_output=True, text=True, check=False)
            if r.returncode == 0:
                return _accept(tmp, stem)
            reason += f"; curl: {r.stderr.strip()}"
            break
        except requests.RequestException as e:
            reason = str(e)
            print(f"  attempt {i + 1} failed: {e}", file=sys.stderr)
            time.sleep(3)
    return None, reason


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def write_gz_jsonl(path: Path, records: list[dict]) -> None:
    """Deterministic gzip (mtime 0, no file name) of one JSON object per line (rule 9)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    data = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records).encode("utf-8")
    with open(path, "wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
        gz.write(data)


def search_text(pdf: Path, sha: str) -> int:
    """Every page's text (PyMuPDF, fast), or every sheet's text for a workbook, to data/reports/text/ for locating
    figures; returns the page (or sheet) count."""
    if pdf.suffix in (".xlsx", ".xls"):
        recs = [{"page": name, "text": text} for name, text in sheet_texts(pdf).items()]
        write_gz_jsonl(SEARCH_TEXT / f"{sha}.jsonl.gz", recs)
        return len(recs)
    import fitz  # pymupdf

    with fitz.open(pdf) as doc:
        recs = [{"page": i + 1, "text": p.get_text()} for i, p in enumerate(doc)]
    write_gz_jsonl(SEARCH_TEXT / f"{sha}.jsonl.gz", recs)
    return len(recs)


def fetch(banks: set[str] | None, force: bool) -> int:
    urls = read_csv(URLS)
    manifest = {(r["bank_id"], r["doc_type"], r["period"]): r for r in read_csv(MANIFEST)}
    failed = []
    for u in urls:
        key = (u["bank_id"], u["doc_type"], u["period"])
        if banks and u["bank_id"] not in banks:
            continue
        have = manifest.get(key)
        if have and have["url"] == u["url"] and not force and pdf_path(*key).exists():
            continue
        stem = REPORTS / f"{key[0]}_{key[1]}_{key[2]}"
        print(f"{' '.join(key)}: {u['url']}")
        when = now_utc()
        dest, reason = download(u["url"], stem)
        if dest is None:
            failed.append((*key, u["url"], reason))
            continue
        sha = sha256_file(dest)
        pages = search_text(dest, sha)
        manifest[key] = {"bank_id": key[0], "doc_type": key[1], "period": key[2], "url": u["url"], "sha256": sha,
                         "bytes": dest.stat().st_size, "pages": pages, "downloaded_utc": when}
        write_manifest(list(manifest.values()))
    if failed:
        print("\nnot downloaded:")
        for f in failed:
            print("  " + " | ".join(str(x) for x in f))
    return 0


def page_key(page: str) -> int | str:
    """An entry's page: the 1 based physical page of a PDF, or for a workbook `sheet!cell`, cached by sheet."""
    page = str(page)
    return page.rsplit("!", 1)[0] if "!" in page else int(page)


def cache_pages() -> int:
    """Rebuilds data/raw/report_text/ from the cited pages: PDF page text by pdfplumber, workbook sheets as tab
    separated rows (instruction 02b B.3)."""
    import pdfplumber

    cited: dict[str, set] = {}
    for r in read_csv(ENTRIES):
        cited.setdefault(r["report_sha256"], set()).add(page_key(r["page"]))
    for r in read_csv(ONE_OFFS):  # instruction 03 B.4: provenance applies to every one off row
        cited.setdefault(r["report_sha256"], set()).add(page_key(r["page"]))
    for r in read_csv(MERGERS):
        if r.get("source_sha256"):
            cited.setdefault(r["source_sha256"], set()).add(int(r["source_page"]))
    by_sha = {r["sha256"]: r for r in read_csv(MANIFEST)}
    missing = sorted(s for s in cited if s not in by_sha)
    if missing:
        raise SystemExit(f"cited documents not in report_manifest.csv: {missing}")
    for sha, pages in sorted(cited.items()):
        m = by_sha[sha]
        pdf = pdf_path(m["bank_id"], m["doc_type"], m["period"])
        if sha256_file(pdf) != sha:
            raise SystemExit(f"{pdf} does not match its manifest sha256 {sha}")
        dest = CACHE / f"{sha}.jsonl.gz"
        old = {}
        if dest.exists():
            with gzip.open(dest, "rt", encoding="utf-8") as f:
                old = {json.loads(line)["page"]: json.loads(line) for line in f}
        need = sorted((p for p in pages if p not in old), key=str)
        if need and pdf.suffix in (".xlsx", ".xls"):
            sheets = sheet_texts(pdf)
            for p in need:
                old[p] = {"page": p, "text": sheets[p]}
        elif need:
            with pdfplumber.open(pdf) as doc:
                for p in need:
                    old[p] = {"page": p, "text": doc.pages[p - 1].extract_text() or ""}
        write_gz_jsonl(dest, [old[p] for p in sorted(pages, key=lambda x: (isinstance(x, str), str(x).zfill(6)))])
        print(f"{sha[:12]} {m['bank_id']} {m['doc_type']} {m['period']}: {len(pages)} pages ({len(need)} new)")
    for f in CACHE.glob("*.jsonl.gz"):
        if f.name.removesuffix(".jsonl.gz") not in cited:
            f.unlink()
            print(f"removed {f.name}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bank", action="append", help="only this bank_id (repeatable)")
    ap.add_argument("--force", action="store_true", help="download again even if in the manifest")
    ap.add_argument("--cache-pages", action="store_true", help="rebuild data/raw/report_text/ from the entries")
    args = ap.parse_args(argv)
    if args.cache_pages:
        return cache_pages()
    return fetch(set(args.bank) if args.bank else None, args.force)


if __name__ == "__main__":
    raise SystemExit(main())
