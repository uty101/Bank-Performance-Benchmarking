"""Step 4.3 tests (instruction 04 B.4, instruction 04b B.3): the hand check workbook against size_gaps, and the joint gap."""

import numpy as np
import openpyxl
import pandas as pd
import pytest
from pycel import ExcelCompiler

from bpb.config import load_config
from bpb.gaps import joint_gap
from bpb.ingest import ROOT
from scripts.build_hand_check import BASIS, DATE, FIXTURE, tables

CFG = load_config(ROOT / "config.toml")
WORKBOOK = ROOT / FIXTURE
BANK = {"I": 1000.0, "F": 250.0, "O": 150.0, "NII": 600.0, "C": 600.0, "LLP": 40.0, "L": 8000.0, "IEA": 20000.0}
SINGLE = {"cost_income": (0.5, (0.6 - 0.5) * 1000.0), "cost_of_risk": (0.003, (0.005 - 0.003) * 8000.0),
          "nim": (0.035, (0.035 - 0.03) * 20000.0), "fee_share": (0.3, 0.3 * 750.0 / 0.7 - 250.0)}


@pytest.fixture(scope="module")
def t():
    return tables(CFG)


def _cells(sheet) -> dict[str, str]:
    return {r[0].value: f"{sheet.title}!B{r[0].row}" for r in sheet.iter_rows(min_col=1, max_col=1) if r[0].value}


def test_hand_check(t):
    book = openpyxl.load_workbook(WORKBOOK)
    excel = ExcelCompiler(filename=str(WORKBOOK))
    gaps, joint = t["gaps"], t["joint"]
    tol = CFG.gaps.hand_check_tol_eur
    for bank in CFG.gaps.hand_check_banks:
        sheet = book[bank]
        cells = _cells(sheet)
        group = sheet["B3"].value
        print(bank, group, sheet["C3"].value or "")
        cell = gaps[(gaps["bank_id"] == bank) & (gaps["group"] == group) & (gaps["basis"] == BASIS)]
        sized = cell[cell["delta_pi_lc"].notna()].set_index("gap")
        assert len(sized) > 0
        assert {k.split("|")[1] for k in cells if k.startswith("delta_pi_lc|")} == set(sized.index)
        for gap, row in sized.iterrows():
            assert abs(excel.evaluate(cells[f"delta_pi_eur|{gap}"]) - row["delta_pi_eur"]) <= tol
            assert abs(excel.evaluate(cells[f"delta_rote_pts|{gap}"]) - row["delta_rote_pts"]) <= 1e-6
        j = joint[(joint["bank_id"] == bank) & (joint["group"] == group) & (joint["basis"] == BASIS)].iloc[0]
        assert abs(excel.evaluate(cells["joint_delta_pi_eur"]) - j["joint_eur"]) <= tol


@pytest.mark.parametrize("gap", list(SINGLE))
def test_joint_single_synthetic(gap):
    target, standalone = SINGLE[gap]
    assert abs(joint_gap(BANK, {gap: target}) / standalone - 1) < 1e-9



def test_ram_joint():
    """Instruction 06c step 6.7: the margin gap closes through NII at the bank's own credit cost."""
    ram, ci = 0.035, 0.5
    d = ram * BANK["IEA"] - (BANK["NII"] - BANK["LLP"])
    assert abs(joint_gap(BANK, {"risk_adj_nim": ram}) - d) < 1e-9
    both = d + BANK["C"] - ci * (BANK["I"] + d)
    assert abs(joint_gap(BANK, {"risk_adj_nim": ram, "cost_income": ci}) - both) < 1e-9

def test_joint_single(t):
    """Instruction 04b B.3: with the level rule the identity holds on real data."""
    gaps, joint = t["gaps"], t["joint"]
    keys = ["date", "bank_id", "group", "basis"]
    n = gaps.groupby(keys)["delta_pi_lc"].count().rename("n").reset_index()
    one = joint.merge(n[n["n"] == 1], on=keys)
    assert len(one) > 0
    assert np.abs(one["joint_eur"] / one["sum_standalone_eur"] - 1).max() < 1e-9


def test_sized_rows_have_values(t):
    g = t["gaps"]
    assert (g.loc[g["status"] == "not_sized", ["delta_pi_lc", "delta_pi_eur", "delta_rote_pts"]].isna().all(axis=None))
    assert isinstance(g, pd.DataFrame) and g["delta_pi_lc"].notna().any()
    assert (g["date"] == DATE).all()
