"""Pulls raw data. The only module besides fetch_reports.py that touches the network (CLAUDE.md rule 8).

usage: python scripts/pull_data.py --stage eba [--stage fx ...]

Every pull writes an entry per file to data/raw/MANIFEST.json (kickoff Section 3.2).
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import shutil
import sys
import time
import tomllib
from datetime import UTC, datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
MANIFEST = RAW / "MANIFEST.json"
DOWNLOAD = ROOT / "data" / "eba_download"  # gitignored, unfiltered originals (OPEN-02)
HEADERS = {"User-Agent": "Mozilla/5.0 (bank-performance-benchmarking data pull)"}
CHUNK = 1 << 20
BOM = b"\xef\xbb\xbf"


def load_cfg() -> dict:
    with open(ROOT / "config.toml", "rb") as f:
        return tomllib.load(f)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def download(url: str, dest: Path, attempts: int = 3) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    for i in range(attempts):
        try:
            with requests.get(url, headers=HEADERS, stream=True, timeout=120) as r:
                r.raise_for_status()
                with open(tmp, "wb") as f:
                    f.writelines(r.iter_content(CHUNK))
            tmp.replace(dest)
            return
        except requests.RequestException as e:
            print(f"  attempt {i + 1} failed: {e}", file=sys.stderr)
            time.sleep(5)
    raise SystemExit(f"data pull failed: {url}")


def read_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {"files": []}


def write_manifest(entries: list[dict]) -> None:
    m = read_manifest()
    by_path = {e["path"]: e for e in m["files"]}
    for e in entries:
        by_path[e["path"]] = e
    m["files"] = [by_path[k] for k in sorted(by_path)]
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_bytes((json.dumps(m, indent=2, sort_keys=True) + "\n").encode("utf-8"))


# --- stage eba -------------------------------------------------------------

def period_to_date(p: str) -> str:
    """EBA Period yyyymm (a quarter-end month) to the ISO quarter-end date."""
    y, m = int(p[:4]), int(p[4:6])
    day = {3: 31, 6: 30, 9: 30, 12: 31}[m]
    return f"{y:04d}-{m:02d}-{day:02d}"


def filter_csv(src: Path, dest: Path, countries: set[str]) -> tuple[int, int, list[str]]:
    """Keeps the header and every row whose NSA (the bank's home country) is in `countries`.

    Rows are copied byte for byte. Returns (rows in, rows out, sorted distinct Period values out).
    """
    rows_in = rows_out = 0
    periods: set[str] = set()
    dest.parent.mkdir(parents=True, exist_ok=True)
    # mtime=0 and no file name keep the gzip bytes identical across runs (rule 9)
    with (
        open(src, "rb") as fin,
        open(dest, "wb") as raw_out,
        gzip.GzipFile(filename="", mode="wb", fileobj=raw_out, mtime=0) as fout,
    ):
        header = fin.readline()
        cols = next(csv.reader([header.removeprefix(BOM).decode("latin-1")]))
        i_nsa, i_per = cols.index("NSA"), cols.index("Period")
        fout.write(header)
        for line in fin:
            if not line.strip():
                continue
            rec = next(csv.reader([line.decode("latin-1")]))  # NSA and Period are ASCII
            if len(rec) != len(cols):
                raise SystemExit(f"{src}: row {rows_in + 2} has {len(rec)} fields, header has {len(cols)}")
            rows_in += 1
            if rec[i_nsa] in countries:
                fout.write(line)
                rows_out += 1
                periods.add(rec[i_per])
    return rows_in, rows_out, sorted(periods)


def csv_periods(path: Path) -> tuple[int, list[str]]:
    with open(path, "rb") as f:
        if f.read(len(BOM)) != BOM:
            f.seek(0)
        text = io.TextIOWrapper(f, encoding="latin-1", newline="")
        r = csv.reader(text)
        i_per = next(r).index("Period")
        n, periods = 0, set()
        for rec in r:
            if rec:
                n += 1
                periods.add(rec[i_per])
    return n, sorted(periods)


def text_encoding(path: Path) -> str:
    """utf-8 if the whole file decodes as UTF-8, else cp1252 (recorded in the manifest for readers)."""
    try:
        with open(path, encoding="utf-8") as f:
            for _ in iter(lambda: f.read(CHUNK), ""):
                pass
        return "utf-8"
    except UnicodeDecodeError:
        return "cp1252"


def stage_eba(cfg: dict) -> None:
    eba = cfg["eba"]
    max_bytes = eba["max_commit_mb"] * 1024 * 1024
    with open(ROOT / "data" / "manual" / "universe.csv", encoding="utf-8") as f:
        countries = {r["country"] for r in csv.DictReader(f) if r["country"] != "GB"}
    # instruction 01 Section B item 2 fixes this set
    assert countries == {"FI", "NO", "DK", "SE", "NL", "BE", "FR", "DE", "ES", "IT"}, countries
    with open(ROOT / "data" / "manual" / "eba_urls.csv", encoding="utf-8") as f:
        urls = list(csv.DictReader(f))

    entries = []
    for release in eba["releases"]:
        for name in eba["files"]:
            hits = [u for u in urls if int(u["release"]) == release and u["file"] == name]
            if len(hits) != 1:
                raise SystemExit(f"eba_urls.csv: {len(hits)} rows for {release} {name}")
            url = hits[0]["url"]
            print(f"eba {release} {name}")
            orig = DOWNLOAD / str(release) / name
            pulled = now_utc()
            download(url, orig)
            o_sha, o_bytes = sha256_file(orig), orig.stat().st_size
            if name.endswith(".csv"):
                dest = RAW / "eba" / str(release) / (name + ".gz")
                rows_in, rows_out, periods = filter_csv(orig, dest, countries)
                _, all_periods = csv_periods(orig)
                enc = text_encoding(orig)
                entries.append({
                    "path": rel(orig), "committed": False, "url": url, "pulled_utc": pulled,
                    "sha256": o_sha, "bytes": o_bytes, "rows": rows_in,
                    "first_date": period_to_date(all_periods[0]), "last_date": period_to_date(all_periods[-1]),
                    "encoding": enc,
                })
                f_bytes = dest.stat().st_size
                entries.append({
                    "path": rel(dest), "committed": True, "url": url, "pulled_utc": pulled,
                    "sha256": sha256_file(dest), "bytes": f_bytes, "rows": rows_out,
                    "first_date": period_to_date(periods[0]), "last_date": period_to_date(periods[-1]),
                    "filtered_from": rel(orig), "filter": "NSA in " + ",".join(sorted(countries)), "encoding": enc,
                })
                if f_bytes > max_bytes:
                    write_manifest(entries)
                    raise SystemExit(f"{rel(dest)} is {f_bytes} bytes gzipped, over max_commit_mb (rule 4)")
            else:
                dest = RAW / "eba" / str(release) / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(orig, dest)
                entries.append({
                    "path": rel(dest), "committed": True, "url": url, "pulled_utc": pulled,
                    "sha256": o_sha, "bytes": o_bytes, "rows": None, "first_date": None, "last_date": None,
                })
    write_manifest(entries)


# --- stage fx --------------------------------------------------------------

ECB_URL = "https://data-api.ecb.europa.eu/service/data/EXR/D.{ccy}.EUR.SP00.A?format=csvdata"  # kickoff 3.2
FX_START, FX_END = "2020-01-01", "2026-07-31"  # instruction 01 step 1.4


def stage_fx(cfg: dict) -> None:
    entries = []
    for ccy in cfg["fx"]["currencies"]:
        url = f"{ECB_URL.format(ccy=ccy)}&startPeriod={FX_START}&endPeriod={FX_END}"
        print(f"fx {ccy}")
        dest = RAW / "fx" / f"{ccy}.csv"
        pulled = now_utc()
        download(url, dest)
        with open(dest, encoding="utf-8", newline="") as f:
            recs = list(csv.DictReader(f))
        dates = sorted(r["TIME_PERIOD"] for r in recs)
        if not dates:
            raise SystemExit(f"data pull failed: no rows for {ccy}")
        entries.append({
            "path": rel(dest), "committed": True, "url": url, "pulled_utc": pulled,
            "sha256": sha256_file(dest), "bytes": dest.stat().st_size, "rows": len(recs),
            "first_date": dates[0], "last_date": dates[-1], "encoding": "utf-8",
        })
    write_manifest(entries)


STAGES = {"eba": stage_eba, "fx": stage_fx}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stage", action="append", required=True, choices=sorted(STAGES))
    args = ap.parse_args(argv)
    cfg = load_cfg()
    for s in args.stage:
        STAGES[s](cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
