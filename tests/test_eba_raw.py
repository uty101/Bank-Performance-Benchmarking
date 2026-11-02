"""Step 1.1 tests on the committed EBA raw files (instruction 01 Section C)."""

import csv
import gzip
import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
EBA = RAW / "eba"


def _manifest() -> dict:
    m = json.loads((RAW / "MANIFEST.json").read_text(encoding="utf-8"))
    return {e["path"]: e for e in m["files"]}


def test_manifest_hashes():
    manifest = _manifest()
    files = sorted(p for p in EBA.rglob("*") if p.is_file())
    assert files, "no committed EBA files"
    for p in files:
        key = p.relative_to(ROOT).as_posix()
        assert key in manifest, key
        assert manifest[key]["committed"] is True, key
        assert hashlib.sha256(p.read_bytes()).hexdigest() == manifest[key]["sha256"], key
        assert p.stat().st_size == manifest[key]["bytes"], key
    committed = {k for k, e in manifest.items() if e["committed"] and k.startswith("data/raw/eba/")}
    assert committed == {p.relative_to(ROOT).as_posix() for p in files}


def _periods(path: Path) -> set[str]:
    with gzip.open(path, "rt", encoding="latin-1", newline="") as f:  # Period is ASCII in every release
        r = csv.reader(f)
        i = next(r).index("Period")
        return {rec[i] for rec in r if rec}


def test_reference_dates():
    releases = sorted(int(p.name) for p in EBA.iterdir() if p.is_dir())
    assert releases == [2021, 2022, 2023, 2024, 2025]
    all_dates: list[pd.Timestamp] = []
    for y in releases:
        sets = [_periods(f) for f in sorted((EBA / str(y)).glob("*.csv.gz"))]
        assert len(sets) == 2
        dates = set().union(*sets)
        assert len(dates) == 4, (y, sorted(dates))
        all_dates += [pd.Period(f"{d[:4]}-{d[4:]}", "M").to_timestamp(how="end").normalize() for d in dates]
    expected = list(pd.date_range("2020-09-30", "2025-06-30", freq="QE"))
    assert len(expected) == 20
    assert sorted(all_dates) == expected
    assert len(set(all_dates)) == len(all_dates)
