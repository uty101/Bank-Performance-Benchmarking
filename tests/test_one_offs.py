"""Step 3.3 test (instruction 03 Section C)."""

import pandas as pd

from bpb.ingest import FACTS_COLUMNS
from bpb.kpi import underlying_facts

RATES = pd.DataFrame(columns=["date", "ccy", "per_eur"])


def _facts(rows):
    base = {"lei": "L", "ccy": "EUR", "unit_scale": 1.0, "period_months": 12, "family": "report", "locator": "x@1",
            "status": "ok"}
    return pd.DataFrame([{**base, "bank_id": "NDA", "ref_date": "2025-12-31", "field": f, "value": v,
                          "lineage_id": f} for f, v in rows])[FACTS_COLUMNS]


def _one_off(field, amount):
    return pd.DataFrame([{"bank_id": "NDA", "ref_date": "2025-12-31", "period_months": 12, "field": field,
                          "amount": amount, "description": "synthetic", "report_sha256": "s", "page": 1}])


def test_underlying():
    facts = _facts([("admin_expenses", 100.0), ("net_fees", 50.0)])
    und = underlying_facts(facts, _one_off("admin_expenses", 10.0), RATES).set_index("field")["value"]
    assert und["admin_expenses"] == 90.0
    assert facts.set_index("field").loc["admin_expenses", "value"] == 100.0  # reported basis unchanged
    gain = underlying_facts(facts, _one_off("net_fees", -5.0), RATES).set_index("field")["value"]
    assert gain["net_fees"] == 45.0
