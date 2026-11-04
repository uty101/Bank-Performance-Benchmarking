"""Step 5.3 tests (instruction 05 Section C)."""

import numpy as np
import pandas as pd

from bpb.ingest import ROOT, read_universe
from bpb.market import in_price_ccy
from bpb.valuation import fit_stability, fit_year, ptbv


def test_ols_matches_lstsq():
    rng = np.random.default_rng(3)
    n = 30
    rote = rng.uniform(0.05, 0.20, n)
    spread = rng.normal(0, 0.01, n)
    y = 0.2 + 9.0 * rote - 4.0 * spread + rng.normal(0, 0.1, n)
    df = pd.DataFrame({"bank_id": [f"B{i:02d}" for i in range(n)], "year": 2025, "ptbv": y, "rote": rote,
                       "spread": spread})
    fit = fit_year(df)
    s = df.sort_values("bank_id")
    x = np.column_stack([np.ones(n), s["rote"], s["spread"]])
    coef = np.linalg.lstsq(x, s["ptbv"], rcond=None)[0]
    assert np.abs(np.array([fit["alpha"], fit["beta"], fit["gamma"]]) - coef).max() <= 1e-10


def test_coe_recovery():
    rng = np.random.default_rng(4)
    n = 30
    rote = rng.uniform(0.05, 0.20, n)
    spread = rng.normal(0, 0.01, n)
    df = pd.DataFrame({"bank_id": [f"B{i:02d}" for i in range(n)], "year": 2025, "ptbv": (rote - 0.02) / (0.10 - 0.02),
                       "rote": rote, "spread": spread})
    fit = fit_year(df)
    assert abs(fit["coe_implied"] - 0.10) <= 1e-9
    assert abs(fit["gamma"]) <= 1e-9


def test_gbp_pence_in_ptbv():
    date = "2025-12-31"
    amounts = {"total_equity": 400.0, "minority_interests": 0.0, "at1_instruments": 0.0, "intangibles_deduction": 0.0,
               "shares_out": 100.0}
    facts = pd.DataFrame([{"bank_id": "LLOY", "lei": "", "ref_date": date, "field": k, "value": v,
                           "ccy": "" if k == "shares_out" else "GBP", "unit_scale": 1.0, "period_months": pd.NA,
                           "family": "report", "locator": "", "lineage_id": k, "status": "ok"}
                          for k, v in amounts.items()])
    prices = in_price_ccy(pd.DataFrame({"date": [date], "ticker": ["LLOY.L"], "close": [500.0]}),
                          pd.DataFrame({"ticker": ["LLOY.L"], "currency": ["GBp"]}))
    rates = pd.DataFrame({"date": pd.to_datetime([date]), "ccy": ["GBP"], "per_eur": [0.85]})
    out = ptbv(facts, prices, rates, read_universe(ROOT))
    row = out[out["date"] == date].iloc[0]
    assert (row["price"], row["price_ccy"], row["tbvps"]) == (5.0, "GBP", 4.0)
    assert abs(row["ptbv"] - 1.25) <= 1e-12


def _frame(slopes: dict, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    frames = []
    for year, slope in slopes.items():
        rote = rng.uniform(0.05, 0.20, 30)
        spread = rng.normal(0, 0.01, 30)
        frames.append(pd.DataFrame({"bank_id": [f"B{i:02d}" for i in range(30)], "year": year, "rote": rote,
                                    "spread": spread, "ptbv": 0.2 + slope * rote + rng.normal(0, 0.05, 30)}))
    return pd.concat(frames, ignore_index=True)


def test_year_not_significant():
    df = _frame({2021: 0.0}, 5)
    fit = fit_year(df)
    assert fit["beta"] - 1.645 * fit["beta_se"] <= 0 <= fit["beta"] + 1.645 * fit["beta_se"]
    assert fit["status"] == "beta_ns_year" and np.isnan(fit["coe_implied"])


def test_stability_separates_slopes():
    equal = fit_stability(_frame({2021: 5.0, 2022: 5.0, 2023: 5.0}, 6))
    apart = fit_stability(_frame({2021: 2.0, 2022: 6.0, 2023: 12.0}, 6))
    assert equal["df_num"] == 2 and equal["n_banks"] == 30
    assert apart["p_value"] < 0.001 < equal["p_value"]
