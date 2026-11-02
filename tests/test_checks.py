"""Step 1.6 tests (instruction 01 Section C)."""

from pathlib import Path

import pandas as pd

from bpb.checks import identities
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
