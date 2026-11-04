"""Driver decomposition (kickoff Section 5.7, instruction 05 B.1).

The tree's ratios come from `compute_kpis` with their own KPI specs, so they follow the KPI family rule at every date.
"""

from __future__ import annotations

from collections.abc import Callable
from itertools import product
from math import factorial

import numpy as np
import pandas as pd

from bpb import fx
from bpb.benchmark import target
from bpb.gaps import PCT, _ccy, average_te
from bpb.ingest import read_source_map, read_universe
from bpb.kpi import compute_kpis
from bpb.peers import cluster_year

DRIVERS_COLUMNS = ["date", "bank_id", "basis", "reference", "driver", "bank_value", "ref_value", "shapley_pts",
                   "other_below_line_pts", "minorities_and_at1_pts", "status"]
OTH = "OTH/A"
DRIVERS = ["NII/A", "F/A", "O/A", "C/A", "LLP/A", "t", "A/TE"]  # the 7 Shapley drivers, B.1
HIGHER = {"NII/A", "F/A", "O/A", "A/TE"}  # B.1; every other driver, OTH/A included (PLAN 5.1), lowers RoTE
# B.1: the Harrell Davis level of each run, for drivers that raise RoTE and drivers that lower it
RUNS = {"median": (0.5, 0.5), "target": (0.75, 0.25)}
# the amounts of the tree, each over average total_assets
TREE = {"nii": "nii", "fees": "net_fees", "other": "other_income", "cost": "opex", "llp": "impairments_fin",
        "income": "total_operating_income", "pbt": "pbt", "tax": "tax"}
TREE_SPEC = {"kpis": [{"kpi": k, "numerator": f, "denominator": "total_assets", "average": True, "unit": "",
                       "direction": "context"} for k, f in TREE.items()]}


def rote_tree(drivers: dict) -> float:
    """B.1: the bracket is pbt / A, so this is pat / T-bar, before minorities and AT1 coupons."""
    d = drivers
    return (d["NII/A"] + d["F/A"] + d["O/A"] - d["C/A"] - d["LLP/A"] - d[OTH]) * (1 - d["t"]) * d["A/TE"]


def shapley(f: Callable[[dict], float], bank: dict, ref: dict) -> dict:
    """Exact Shapley values over the keys of `bank` (kickoff Section 5.7): f sees the keys in S at the bank's values
    and the rest at the reference."""
    names = list(bank)
    n = len(names)
    value = {s: f({k: bank[k] if on else ref[k] for k, on in zip(names, s, strict=True)})
             for s in product((False, True), repeat=n)}
    out = dict.fromkeys(names, 0.0)
    for s, v in value.items():
        size = sum(s)
        for i, k in enumerate(names):
            if not s[i]:
                with_i = s[:i] + (True,) + s[i + 1:]
                out[k] += factorial(size) * factorial(n - size - 1) / factorial(n) * (value[with_i] - v)
    return out


def merger_breaks(facts: pd.DataFrame, rates: pd.DataFrame, cfg) -> dict[str, list[str]]:
    """{bank: completion dates} of the material mergers (Convention 4.10), as in scripts/merger_materiality.py: the
    target against the acquirer's total_assets at its last reference date strictly before completion, eba rows for an
    EU bank and report rows for a UK bank, both in EUR at that date's rate."""
    uk = set(read_source_map(cfg.root)["bank_groups"]["uk"])
    ta = facts[(facts["field"] == "total_assets") & facts["value"].notna()]
    out: dict[str, list[str]] = {}
    for r in pd.read_csv(cfg.root / "data" / "manual" / "mergers.csv", dtype={"target_ccy": str}).itertuples(index=False):
        fam = "report" if r.acquirer_id in uk else "eba"
        a = ta[(ta["bank_id"] == r.acquirer_id) & (ta["family"] == fam) & (ta["ref_date"] < r.completion_date)]
        if a.empty or pd.isna(r.target_total_assets):
            continue
        last = a.sort_values("ref_date").iloc[-1]
        acquirer = fx.to_eur(float(last["value"]), last["ccy"], last["ref_date"], "bs", rates, None)
        size = fx.to_eur(float(r.target_total_assets), r.target_ccy, last["ref_date"], "bs", rates, None)
        if size / acquirer > cfg.merger.merger_materiality:
            out.setdefault(r.acquirer_id, []).append(r.completion_date)
    return out


def _in_period(d: str, completions: list[str]) -> bool:
    """The 12 months ending at d hold a completion: the fiscal year at 31 Dec, the rolling period at 30 Jun."""
    start = fx.period_start(d, rolling=d[5:] == "06-30").strftime("%Y-%m-%d")
    return any(start <= c <= d for c in completions)


def _tree_inputs(facts: pd.DataFrame, rates: pd.DataFrame, cfg) -> dict:
    """{(date, bank, basis): drivers}: the 7 drivers and OTH/A where every input exists, with t blank in a loss year,
    or {} where an input is missing; "status" says which of the 2 it is."""
    one_offs = pd.read_csv(cfg.root / "data" / "manual" / "one_offs.csv", dtype={"page": str})
    report_ccy = dict(zip(*(read_universe(cfg.root)[c] for c in ("bank_id", "report_ccy")), strict=True))
    te = {(r.date, r.bank_id): r for r in average_te(facts, rates).itertuples(index=False)}
    raw: dict = {}
    for r in compute_kpis(facts, TREE_SPEC, one_offs, rates).itertuples(index=False):
        raw.setdefault((r.date, r.bank_id, r.basis), {})[r.kpi] = r
    out = {}
    for (date, bank, basis), rows in raw.items():
        v = {k: r.value for k, r in rows.items()}
        t = te[(date, bank)]
        assets = rows["pbt"].denominator
        if any(pd.isna(x) for x in v.values()) or pd.isna(assets) or pd.isna(t.denominator):
            out[(date, bank, basis)] = {"status": "missing_input"}
            continue
        if _ccy(rows["pbt"].family, report_ccy[bank]) != _ccy(t.family, report_ccy[bank]):
            out[(date, bank, basis)] = {"status": "mixed_family"}
            continue
        loss = v["pbt"] <= 0
        out[(date, bank, basis)] = {
            "NII/A": v["nii"], "F/A": v["fees"], "O/A": v["other"], "C/A": v["cost"], "LLP/A": v["llp"],
            OTH: v["income"] - v["cost"] - v["llp"] - v["pbt"], "t": np.nan if loss else v["tax"] / v["pbt"],
            "A/TE": assets / t.denominator, "status": "loss_year" if loss else "ok"}
    return out


def _reference(tree: dict, members: list[str], date: str, basis: str, run: str, min_peers: int) -> dict | None:
    """Each driver and OTH/A at its run's level over the peers holding it; None if a driver has too few peers."""
    hi, lo = RUNS[run]
    ref = {}
    for name in [*DRIVERS, OTH]:
        values = [tree[(date, m, basis)][name] for m in members if name in tree.get((date, m, basis), {})]
        values = [x for x in values if pd.notna(x)]
        if len(values) < min_peers:
            return None
        ref[name] = target(np.array(values), hi if name in HIGHER else lo)
    return ref


def _rows(key: tuple, run: str, status: str) -> list[dict]:
    date, bank, basis = key
    return [{"date": date, "bank_id": bank, "basis": basis, "reference": run, "driver": name, "bank_value": np.nan,
             "ref_value": np.nan, "shapley_pts": np.nan, "other_below_line_pts": np.nan,
             "minorities_and_at1_pts": np.nan, "status": status} for name in [*DRIVERS, OTH]]


def _decomposed(key: tuple, run: str, b: dict, ref: dict, rote: float) -> list[dict]:
    """The Shapley values of a bank against a reference. In a loss year the tax driver sits at the reference (B.1)."""
    bank_d = {k: b[k] for k in DRIVERS}
    if pd.isna(bank_d["t"]):
        bank_d["t"] = ref["t"]
    oth = b[OTH]

    def f(d: dict) -> float:
        return rote_tree({**d, OTH: oth})

    phi = shapley(f, bank_d, {k: ref[k] for k in DRIVERS})
    at_ref = {k: ref[k] for k in DRIVERS}
    below = (rote_tree({**at_ref, OTH: ref[OTH]}) - f(at_ref)) * PCT
    minorities = (rote - f(bank_d)) * PCT
    # B.1 reports the difference from the KPI, so a blank KPI leaves it blank; the Shapley values stand
    status = b["status"] if pd.notna(rote) else "rote_blank" if b["status"] == "ok" else f"{b['status']};rote_blank"
    rows = _rows(key, run, status)
    for row in rows:
        name = row["driver"]
        row.update(bank_value=oth if name == OTH else bank_d[name], ref_value=ref[name],
                   shapley_pts=np.nan if name == OTH else phi[name] * PCT, other_below_line_pts=below,
                   minorities_and_at1_pts=minorities)
    return rows


def decompose(kpi: pd.DataFrame, facts: pd.DataFrame, peers: pd.DataFrame, cfg) -> pd.DataFrame:
    """DRIVERS: 8 rows (7 drivers and OTH/A, whose shapley_pts is blank) per date, bank, basis and run, against the
    bank's cluster peers (B.1). The bank and reference values are those the Shapley values used."""
    rates = fx.ecb_rates(cfg.root / "data" / "raw")
    tree = _tree_inputs(facts, rates, cfg)
    breaks = merger_breaks(facts, rates, cfg)
    rote = {(r.date, r.bank_id, r.basis): r.value for r in kpi[kpi["kpi"] == "rote"].itertuples(index=False)}
    rows = []
    for date, bank, basis in sorted(tree):
        key = (date, bank, basis)
        clusters = peers[peers["year"] == cluster_year(date)].set_index("bank_id")["cluster"].dropna()
        members = [] if bank not in clusters else [m for m in clusters.index[clusters == clusters[bank]] if m != bank]
        for run in RUNS:
            b = tree[key]
            ref = _reference(tree, members, date, basis, run, cfg.bench.min_peers)
            if _in_period(date, breaks.get(bank, [])):
                rows += _rows(key, run, "merger_break")
            elif b["status"] in ("missing_input", "mixed_family"):
                rows += _rows(key, run, b["status"])
            elif ref is None:
                rows += _rows(key, run, "too_few_peers")
            else:
                rows += _decomposed(key, run, b, ref, rote.get(key, np.nan))
    return pd.DataFrame(rows, columns=DRIVERS_COLUMNS)
