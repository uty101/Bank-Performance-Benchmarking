"""Step 1.5 tests (instruction 01 Section C)."""

from pathlib import Path

import pandas as pd
import yaml

from bpb.config import load_config
from bpb.fx import ecb_rates
from bpb.ingest import FACTS_COLUMNS, eba_facts
from bpb.kpi import averages, compute_kpis, rolling_12m

ROOT = Path(__file__).resolve().parents[1]


def _rows(rows):
    return pd.DataFrame([{"bank_id": "B", "field": f, "ref_date": d, "value": v, "family": fam,
                          "lineage_id": f"{f}{d}", "status": "ok"} for f, d, v, fam in rows])


def test_rolling_hand():
    pl = _rows([("net_fees", "2023-06-30", 60.0, "eba"), ("net_fees", "2022-12-31", 100.0, "eba"),
                ("net_fees", "2022-06-30", 40.0, "eba")])
    r = rolling_12m(pl).set_index("date")
    assert r.loc["2023-06-30", "value"] == 120.0 and r.loc["2023-06-30", "status"] == "ok"
    r2 = rolling_12m(pl[pl["ref_date"] != "2022-06-30"]).set_index("date")
    assert pd.isna(r2.loc["2023-06-30", "value"])
    assert r2.loc["2023-06-30", "status"] == "missing_input:net_fees"


def test_averages_one_family():
    bs = _rows([("total_assets", "2022-12-31", 100.0, "eba"), ("total_assets", "2023-12-31", 110.0, "report")])
    a = averages(bs).set_index("date")
    assert pd.isna(a.loc["2023-12-31", "value"]) and a.loc["2023-12-31", "status"] == "mixed_family"
    same = _rows([("total_assets", "2022-12-31", 100.0, "eba"), ("total_assets", "2023-12-31", 110.0, "eba")])
    assert averages(same).set_index("date").loc["2023-12-31", "value"] == 105.0


def _kpis():
    with open(ROOT / "config" / "kpis.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_recompute():
    cfg = load_config(ROOT / "config.toml")
    facts, _ = eba_facts(cfg)
    kpi = compute_kpis(facts, _kpis(), pd.DataFrame(), ecb_rates(ROOT / "data" / "raw"))
    v = kpi[kpi["value"].notna()]
    assert len(v) > 0
    diff = (v["value"] - v["numerator"] / v["denominator"]).abs()
    assert (diff <= cfg.tolerances.ratio_recompute * v["value"].abs().clip(lower=1)).all()
    assert set(kpi.loc[kpi["value"].isna(), "status"]) and not (kpi.loc[kpi["value"].isna(), "status"] == "ok").any()


def test_missing_input():
    base = {"lei": "L", "ccy": "EUR", "unit_scale": 1e6, "family": "eba", "locator": "x@2025", "status": "ok"}
    rows = []
    for d in ("2022-12-31", "2023-12-31"):
        rows.append({**base, "bank_id": "B", "ref_date": d, "field": "total_assets", "value": 100.0,
                     "period_months": pd.NA, "lineage_id": f"ta{d}"})
    facts = pd.DataFrame(rows)[FACTS_COLUMNS]
    kpi = compute_kpis(facts, _kpis(), pd.DataFrame(), pd.DataFrame(columns=["date", "ccy", "per_eur"]))
    roa = kpi[(kpi["kpi"] == "roa") & (kpi["date"] == "2023-12-31")]
    assert len(roa) == 2  # reported and underlying
    assert roa["value"].isna().all() and (roa["status"] == "missing_input:profit_owners").all()


def test_rote_hand():
    """Instruction 03 step 3.4: profit_owners 120, at1_coupons 20, average tangible equity 1,000 gives rote 0.10."""
    base = {"lei": "L", "ccy": "GBP", "unit_scale": 1.0, "family": "report", "locator": "x@1", "status": "ok"}
    rows = [("2025-12-31", "profit_owners", 120.0, 12), ("2025-12-31", "at1_coupons", 20.0, 12)]
    for d, te in (("2024-12-31", 900.0), ("2025-12-31", 1100.0)):
        rows += [(d, "total_equity", te + 150.0, None), (d, "minority_interests", 10.0, None),
                 (d, "at1_instruments", 100.0, None), (d, "intangibles_deduction", 40.0, None)]
    facts = pd.DataFrame([{**base, "bank_id": "LLOY", "ref_date": d, "field": f, "value": v, "period_months": pm,
                           "lineage_id": f"{f}{d}"} for d, f, v, pm in rows])[FACTS_COLUMNS]
    kpi = compute_kpis(facts, _kpis(), pd.DataFrame(), pd.DataFrame(columns=["date", "ccy", "per_eur"]))
    rote = kpi[(kpi["kpi"] == "rote") & (kpi["date"] == "2025-12-31") & (kpi["basis"] == "reported")].iloc[0]
    assert abs(rote["value"] - 0.10) < 1e-12 and rote["denominator"] == 1000.0 and rote["status"] == "ok"


def test_at1_liability():
    """Instruction 03c step 3.7: where the AT1 bond sits (at1_in_equity) and where its coupon is charged
    (at1_coupon_in_pl) are separate questions: (a) AT1 in equity, coupon to equity; (b) AT1 a liability, coupon in
    interest expense; (c) AT1 a liability, coupon to reserves (the Spanish case)."""
    base = {"lei": "L", "ccy": "GBP", "unit_scale": 1.0, "family": "report", "locator": "x@1", "status": "ok"}
    rates = pd.DataFrame(columns=["date", "ccy", "per_eur"])

    def run(in_equity, in_pl, at1_instruments):
        rows = [("2025-12-31", "profit_owners", 100.0, 12), ("2025-12-31", "at1_coupons", 20.0, 12)]
        for d in ("2024-12-31", "2025-12-31"):
            rows += [(d, "at1_in_equity", in_equity, None), (d, "at1_coupon_in_pl", in_pl, None),
                     (d, "total_equity", 1050.0, None), (d, "intangibles_deduction", 0.0, None),
                     (d, "minority_interests", 0.0, None)]
            if at1_instruments is not None:
                rows.append((d, "at1_instruments", at1_instruments, None))
        flags = ("at1_in_equity", "at1_coupon_in_pl")
        facts = pd.DataFrame([{**base, "bank_id": "LLOY", "ref_date": d, "field": f, "value": v, "period_months": pm,
                               "lineage_id": f"{f}{d}", "ccy": "" if f in flags else "GBP"}
                              for d, f, v, pm in rows])[FACTS_COLUMNS]
        kpi = compute_kpis(facts, _kpis(), pd.DataFrame(), rates)
        return kpi[(kpi["kpi"] == "rote") & (kpi["date"] == "2025-12-31") & (kpi["basis"] == "reported")].iloc[0]

    a = run(1.0, 0.0, 50.0)
    assert a["denominator"] == 1000.0 and abs(a["value"] - 80.0 / 1000.0) < 1e-12
    b = run(0.0, 1.0, None)
    assert b["denominator"] == 1050.0 and abs(b["value"] - 100.0 / 1050.0) < 1e-12
    assert "at1_liability" in b["status"] and "coupon_in_pl" in b["status"]
    c = run(0.0, 0.0, None)
    assert c["denominator"] == 1050.0 and abs(c["value"] - 80.0 / 1050.0) < 1e-12
    assert "at1_liability" in c["status"]
