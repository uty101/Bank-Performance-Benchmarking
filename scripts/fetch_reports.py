"""Downloads and hashes bank reports. The only module besides pull_data.py that touches the network (rule 8).

usage:
  python scripts/fetch_reports.py [--bank ID ...] [--force]   download every row of data/manual/report_urls.csv
  python scripts/fetch_reports.py --cache-pages               rebuild data/raw/report_text/ (no network)

Download (PLAN step 2.2): each PDF goes to data/reports/ (gitignored) as {bank_id}_{doc_type}_{period}.pdf, and
data/raw/report_manifest.csv gets bank_id, doc_type, period, url, sha256, bytes, pages, downloaded_utc. A row already
in the manifest with the same url is skipped unless --force. A document that cannot be downloaded, or is not a PDF,
is printed and left out of the manifest (instruction 02 step 2.2: listed, not a stop). The full page text of each
PDF is also written to data/reports/text/{sha256}.jsonl.gz (gitignored) for locating figures.

Page cache (instruction 02 B.4): data/raw/report_text/{sha256}.jsonl.gz holds only the pages cited by at least 1
row of data/manual/report_entries.csv or data/manual/mergers.csv. Each line is {"page": n, "text": ...}, with n the
1 based physical page index and the text extracted by pdfplumber. Cache files no longer cited are removed.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
URLS = ROOT / "data" / "manual" / "report_urls.csv"
ENTRIES = ROOT / "data" / "manual" / "report_entries.csv"
MERGERS = ROOT / "data" / "manual" / "mergers.csv"
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


def pdf_path(bank_id: str, doc_type: str, period: str) -> Path:
    return REPORTS / f"{bank_id}_{doc_type}_{period}.pdf"


def download(url: str, dest: Path, attempts: int = 3) -> str | None:
    """Downloads url to dest. Returns None on success, else the reason."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".part")
    reason = ""
    for i in range(attempts):
        # some hosts refuse a browser user agent but serve the library default: the last attempt sends no headers
        headers = HEADERS if i < attempts - 1 else None
        try:
            with requests.get(url, headers=headers, stream=True, timeout=180) as r:
                r.raise_for_status()
                with open(tmp, "wb") as f:
                    f.writelines(r.iter_content(CHUNK))
            with open(tmp, "rb") as f:
                head = f.read(1024)
            if b"%PDF" not in head:
                tmp.unlink()
                return f"not a PDF (starts {head[:40]!r})"
            tmp.replace(dest)
            return None
        except requests.RequestException as e:
            reason = str(e)
            print(f"  attempt {i + 1} failed: {e}", file=sys.stderr)
            time.sleep(3)
    return reason


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
    """Every page's text (PyMuPDF, fast) to data/reports/text/ for locating figures; returns the page count."""
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
        dest = pdf_path(*key)
        print(f"{' '.join(key)}: {u['url']}")
        when = now_utc()
        reason = download(u["url"], dest)
        if reason:
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


def cache_pages() -> int:
    """Rebuilds data/raw/report_text/ from the cited pages, extracting text with pdfplumber."""
    import pdfplumber

    cited: dict[str, set[int]] = {}
    for r in read_csv(ENTRIES):
        cited.setdefault(r["report_sha256"], set()).add(int(r["page"]))
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
        need = sorted(p for p in pages if p not in old)
        if need:
            with pdfplumber.open(pdf) as doc:
                for p in need:
                    old[p] = {"page": p, "text": doc.pages[p - 1].extract_text() or ""}
        write_gz_jsonl(dest, [old[p] for p in sorted(pages)])
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
