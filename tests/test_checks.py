"""Step 1.6 tests (instruction 01 Section C) and step 2.4 test (instruction 02 Section C)."""

import gzip
import json
from pathlib import Path

import pandas as pd

from bpb.checks import identities, provenance
from bpb.config import load_config
from bpb.ingest import FACTS_COLUMNS

ROOT = Path(__file__).resolve().parents[1]
CFG = load_config(ROOT / "config.toml")


def _facts(bank_values: dict[str, dict[str, float]]) -> pd.DataFrame:
    rows = []
    for bank, fields in bank_values.items():
        for field, v in fields.items():
            rows.append({"bank_id": bank, "lei": "L", "ref_date": "2024-12-31", "field": field, "value": v,
                         "ccy": "EUR", "unit_scale": 1e6, "period_months": pd.NA, "family": "eba",
                         "locator": "x@2025", "lineage_id": "x", "status": "ok"})
    return pd.DataFrame(rows)[FACTS_COLUMNS]


def _result(checks: pd.DataFrame, check: str) -> dict[str, bool]:
    c = checks[checks["check"] == check]
    return dict(zip(c["bank_id"], c["passed"], strict=True))


def test_bs_identity():
    facts = _facts({"PASS": {"total_assets": 100, "total_liabilities": 90, "total_equity": 9.6},
                    "FAIL": {"total_assets": 100, "total_liabilities": 90, "total_equity": 9.4}})
    assert _result(identities(facts, CFG), "2_balance_sheet") == {"PASS": True, "FAIL": False}


def test_cet1():
    cet1, rwa = 0.13, 1.0
    facts = _facts({"FAIL": {"cet1": cet1, "rwa": rwa, "cet1_ratio_reported": cet1 / rwa + 0.00051},
                    "PASS": {"cet1": cet1, "rwa": rwa, "cet1_ratio_reported": cet1 / rwa + 0.00049}})
    assert _result(identities(facts, CFG), "4_cet1") == {"FAIL": False, "PASS": True}


def test_provenance_styles(tmp_path):
    """Pages printing 1,234.5 / 1 234,5 / 1.234,5 (the last 2 with a declared decimal comma) all pass; a value absent
    from the page fails."""
    pages = {"p1": ("Net fees and commissions (1,234.5) 1,100.0 EUR", "(1,234.5)", "."),
             "p2": ("Provisions -1 234,5 SEK 987,1", "1 234,5", ","),
             "p3": ("Total € 1.234,5 2.000,0", "1.234,5", ",")}
    rows = []
    for sha, (text, printed, mark) in pages.items():
        sha64 = sha * 32
        with gzip.open(tmp_path / f"{sha64}.jsonl.gz", "wt", encoding="utf-8") as f:
            f.write(json.dumps({"page": 3, "text": text}) + "\n")
        rows.append({"bank_id": "ISP", "ref_date": "2025-12-31", "field": "provisions", "value_as_printed": printed,
                     "unit_scale": "1000000", "value": "1234500000", "report_sha256": sha64, "page": "3",
                     "snippet": text, "decimal_mark": mark})
    absent = dict(rows[0], value_as_printed="4,321.0", value="4321000000", snippet="4,321.0 is elsewhere")
    res = provenance(pd.DataFrame(rows + [absent]), tmp_path)
    assert list(res["passed"]) == [True, True, True, False]
    assert res["note"].iloc[3].endswith("value not on page")

