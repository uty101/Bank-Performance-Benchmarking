"""Step 1.4 tests (instruction 01 Section C)."""

from pathlib import Path

import pandas as pd

from bpb.config import load_config
from bpb.fx import ecb_rates, from_eur, period_start, rate, to_eur

ROOT = Path(__file__).resolve().parents[1]
DATES = ["2021-12-31", "2023-06-30", "2025-12-31"]
VALUE = 1234567.89


def test_roundtrip():
    cfg = load_config(ROOT / "config.toml")
    rates = ecb_rates(ROOT / "data" / "raw")
    assert set(rates["ccy"]) == set(cfg.fx.currencies)
    for ccy in cfg.fx.currencies:
        for d in DATES:
            for kind in ("bs", "pl"):
                start = period_start(d, rolling=False) if kind == "pl" else None
                back = from_eur(to_eur(VALUE, ccy, d, kind, rates, start), ccy, d, kind, rates, start)
                assert abs(back - VALUE) <= cfg.tolerances.fx_roundtrip, (ccy, d, kind, back - VALUE)


def test_pl_rate_is_mean():
    days = pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-08"])
    per_eur = [11.0, 11.2, 10.9, 11.4, 11.1]
    rates = pd.DataFrame({"date": days, "ccy": "SEK", "per_eur": per_eur})
    assert rate("SEK", "2024-01-08", "pl", rates, "2024-01-01") == sum(per_eur) / 5
    assert to_eur(111.0, "SEK", "2024-01-08", "pl", rates, "2024-01-01") == 111.0 / (sum(per_eur) / 5)
    assert rate("SEK", "2024-01-07", "bs", rates, None) == 11.4  # last published on or before
