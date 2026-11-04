"""Steps 5.1 and 5.2 tests (instruction 05 Section C)."""

import numpy as np
import pandas as pd
import pytest
import yaml

from bpb.config import load_config
from bpb.drivers import (
    DRIVERS,
    OTH,
    ci_change,
    decompose,
    nii_change,
    rote_tree,
    shapley,
)
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


@pytest.mark.parametrize("c0,i0,c1,i1", [(600.0, 1000.0, 650.0, 1100.0), (480.0, 900.0, 450.0, 780.0),
                                         (1.2e9, 2.1e9, 1.3e9, 1.9e9)])
def test_ci_change_exact(c0, i0, c1, i1):
    r = ci_change(c0, i0, c1, i1)
    assert abs(r["cost_effect_pts"] + r["income_effect_pts"] - (c1 / i1 - c0 / i0) * 100) <= 1e-12


@pytest.mark.parametrize("nim0,iea0,nim1,iea1", [(0.02, 5.0e10, 0.023, 5.4e10), (0.031, 2.0e9, 0.027, 1.8e9)])
def test_nii_change_exact(nim0, iea0, nim1, iea1):
    r = nii_change(nim0, iea0, nim1, iea1)
    change = nim1 * iea1 - nim0 * iea0
    assert abs((r["volume"] + r["rate"] + r["cross"]) / change - 1) <= 1e-9
