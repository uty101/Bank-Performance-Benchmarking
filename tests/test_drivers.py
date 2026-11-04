"""Step 5.1 tests (instruction 05 Section C)."""

import numpy as np
import pandas as pd
import pytest
import yaml

from bpb.config import load_config
from bpb.drivers import DRIVERS, OTH, decompose, rote_tree, shapley
from bpb.fx import ecb_rates
from bpb.ingest import ROOT, build_facts
from bpb.kpi import compute_kpis
from bpb.peers import peer_groups

CFG = load_config(ROOT / "config.toml")


@pytest.fixture(scope="module")
def table():
    facts = build_facts(CFG)
    with open(ROOT / "config" / "kpis.yaml", encoding="utf-8") as f:
        kpis = yaml.safe_load(f)
    one_offs = pd.read_csv(ROOT / "data" / "manual" / "one_offs.csv", dtype={"page": str})
    kpi = compute_kpis(facts, kpis, one_offs, ecb_rates(ROOT / "data" / "raw"))
    return decompose(kpi, facts, peer_groups(kpi, facts, CFG), CFG)


def test_shapley_sums(table):
    done = table[table["shapley_pts"].notna() | (table["driver"] == OTH) & table["bank_value"].notna()]
    assert len(done) > 0
    for _, g in done.groupby(["date", "bank_id", "basis", "reference"]):
        by = g.set_index("driver")
        bank = by["bank_value"].to_dict()
        ref = {**by["ref_value"].to_dict(), OTH: bank[OTH]}
        gap = (rote_tree(bank) - rote_tree(ref)) * 100
        assert abs(by["shapley_pts"].sum() - gap) <= CFG.drivers.tol_pts


def test_shapley_additive():
    rng = np.random.default_rng(1)
    names = [f"x{i}" for i in range(7)]
    w, x, r = (dict(zip(names, rng.normal(size=7), strict=True)) for _ in range(3))
    phi = shapley(lambda d: sum(w[k] * d[k] for k in names), x, r)
    for k in names:
        assert abs(phi[k] - w[k] * (x[k] - r[k])) <= 1e-12


def test_tree_exact():
    nii, fees, other, cost, llp, oth, tax, assets, te = 600.0, 250.0, 150.0, 520.0, 40.0, 30.0, 95.0, 41000.0, 2600.0
    pbt = nii + fees + other - cost - llp - oth
    d = {"NII/A": nii / assets, "F/A": fees / assets, "O/A": other / assets, "C/A": cost / assets, "LLP/A": llp / assets,
         OTH: oth / assets, "t": tax / pbt, "A/TE": assets / te}
    bracket = d["NII/A"] + d["F/A"] + d["O/A"] - d["C/A"] - d["LLP/A"] - d[OTH]
    assert abs(bracket - pbt / assets) <= 1e-12
    assert abs(rote_tree(d) - (pbt - tax) / te) <= 1e-12
    assert set(DRIVERS) | {OTH} == set(d)
