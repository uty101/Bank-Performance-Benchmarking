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
