"""Step 3.6 test (instruction 03b Section C)."""

from pathlib import Path

import pandas as pd

from bpb.config import load_config

ROOT = Path(__file__).resolve().parents[1]


def test_coverage():
    """Every [sovereign] country has a yield for every December from 2020 to 2025 and for 2026-06."""
    cfg = load_config(ROOT / "config.toml")
    need = [f"{y}-12" for y in range(2020, 2026)] + ["2026-06"]
    for cc in cfg.sovereign.countries:
        y = pd.read_csv(ROOT / "data" / "raw" / "yields" / f"{cc}.csv", dtype={"period": str})
        have = set(y.loc[y["yield_pct"].notna(), "period"])
        assert set(need) <= have, (cc, sorted(set(need) - have))
