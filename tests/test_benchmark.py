"""Step 4.2 tests (instruction 04 B.6): leave one out, Harrell Davis, verdicts and independence from row order."""

import numpy as np
import pandas as pd
from scipy.stats.mstats import hdquantiles

from bpb.benchmark import benchmark, target, target_interval, verdict
from bpb.config import load_config
from bpb.ingest import ROOT

CFG = load_config(ROOT / "config.toml")
DATE = "2025-12-31"


def _frames(values: dict):
    banks = list(values)
    kpi = pd.DataFrame({"bank_id": banks, "date": DATE, "kpi": "nim", "basis": "reported", "value": list(values.values()),
                        "family": "report", "status": "ok"})
    peers = pd.DataFrame({"year": 2025, "bank_id": banks, "cluster": 1})
    universe = pd.DataFrame({"bank_id": banks, "market": "M"})
    return kpi, peers, universe


def test_leave_one_out():
    values = {f"P{i}": float(i) for i in range(1, 7)} | {"BANK": 100.0}
    b = benchmark(*_frames(values), CFG)
    row = b[(b["bank_id"] == "BANK") & (b["group"] == "cluster")].iloc[0]
    assert row["n_peers"] == 6
    assert row["target"] == target(np.arange(1.0, 7.0), 0.75)
    assert row["target"] < 7


def test_hd_matches_scipy():
    v = np.array([0.11, 0.07, 0.15, 0.09, 0.12, 0.10, 0.13])
    assert abs(target(v, 0.75) - float(hdquantiles(v, prob=[0.75])[0])) < 1e-12


def test_interval_uses_the_same_estimator():
    v = np.array([0.11, 0.07, 0.15, 0.09, 0.12, 0.10, 0.13])
    reps = 50
    rng = np.random.default_rng(7)
    idx = rng.integers(0, len(v), (reps, len(v)))
    slow = np.percentile([target(v[i], 0.75) for i in idx], [5, 95])
    fast = target_interval(v, 0.75, reps, np.random.default_rng(7))
    assert np.abs(slow - np.array(fast)).max() < 1e-12


def test_verdicts():
    assert verdict(0.10, 0.08, 0.10, True, "higher") == "in_line"
    assert verdict(0.12, 0.08, 0.10, False, "higher") == "leading"
    assert verdict(0.07, 0.08, 0.10, False, "higher") == "lagging"
    assert verdict(0.09, 0.08, 0.10, False, "higher") == "in_line"


def test_seed_independent_of_order():
    values = {f"P{i}": float(i) * 1.7 % 5 for i in range(1, 12)}
    kpi, peers, universe = _frames(values)
    a = benchmark(kpi, peers, universe, CFG)
    b = benchmark(kpi.sample(frac=1, random_state=3), peers.sample(frac=1, random_state=4),
                  universe.sample(frac=1, random_state=5), CFG)
    pd.testing.assert_frame_equal(a, b)
