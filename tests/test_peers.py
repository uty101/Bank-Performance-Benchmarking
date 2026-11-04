"""Step 4.1 tests (instruction 04 B.6): clusters, stability and nearest assignment on synthetic data."""

from dataclasses import replace

import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score

from bpb.config import load_config
from bpb.ingest import ROOT
from bpb.peers import FEATURES, assign_nearest, cluster, stability


def _data():
    rng = np.random.default_rng(1)
    means = np.array([0.0, 10.0, 20.0])
    truth = np.repeat([0, 1, 2], 10)
    x = means[truth][:, None] + rng.standard_normal((30, 6))
    return pd.DataFrame(x, columns=FEATURES, index=[f"B{i:02d}" for i in range(30)]), truth


def _cfg():
    cfg = load_config(ROOT / "config.toml")
    return replace(cfg, peers=replace(cfg.peers, peer_seed=1))


def test_three_clusters():
    x, truth = _data()
    labels, k, _ = cluster(x, _cfg())
    assert k == 3
    assert adjusted_rand_score(truth, labels) == 1.0


def test_stability_perfect():
    x, _ = _data()
    assert np.abs(stability(x, 3, _cfg()) - 1.0).max() < 1e-12


def test_assigned_nearest():
    x, truth = _data()
    cfg = _cfg()
    bank, rest = x.iloc[25].copy(), x.drop(index=x.index[25])
    labels, _, _ = cluster(rest, cfg)
    bank["trading_assets"] = np.nan  # feature 5
    own = labels[x.index[truth == truth[25]].drop(x.index[25])].unique()
    assert len(own) == 1 and assign_nearest(bank, rest, labels) == own[0]
