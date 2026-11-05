"""Gap sizing (kickoff Section 5.6, instruction 04 B.3, instruction 04b B.3).

Values are computed in the currency of their KPI rows: EUR for eba rows (amendment 7), the reporting currency otherwise.
P&L effects convert at the mean ECB rate of the period and excess capital at the date's rate.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from bpb import fx
from bpb.benchmark import _directions, better
from bpb.ingest import read_source_map, read_universe
from bpb.kpi import _join, compute_kpis, rolling_12m, underlying_facts

GAPS_COLUMNS = ["date", "bank_id", "group", "basis", "gap", "delta_pi_lc", "delta_pi_eur", "delta_rote_pts", "tax_rate",
                "tax_status", "status"]
JOINT_COLUMNS = ["date", "bank_id", "group", "basis", "sum_standalone_eur", "joint_eur", "overlap_eur",
                 "joint_rote_pts", "excess_capital_eur"]
RANGE_COLUMNS = ["date", "bank_id", "gap", "min_eur", "max_eur", "headline_eur", "n_sized"]
TAX_BOUNDS = (0.0, 0.6)  # Convention 4.11
TAX_YEARS = 3  # Convention 4.11
PCT = 100.0  # B.3: delta_rote_pts is in points
HEADLINE = ("cluster", "underlying")  # kickoff Section 5.6
# instruction 05 A.1 item 4: T-bar is the averaged tangible_equity itself, under the KPI family rule. Its numerator is
# the closing balance, so it does not depend on rote's numerator, and no one off touches it, so 1 basis serves both.
TE_SPEC = {"kpis": [{"kpi": "te", "numerator": "tangible_equity", "denominator": "tangible_equity", "average": True,
                     "unit": "", "direction": "context"}]}


def _rolling(d: str) -> bool:
    return d[5:] == "06-30"


def _ccy(family: str, report_ccy: str) -> str:
    return "EUR" if str(family).startswith("eba") else report_ccy  # amendment 7


def pl_to_eur(value: float, ccy: str, d: str, rates: pd.DataFrame) -> float:
    """B.3: the mean ECB rate over 1 Jan to 31 Dec at 31 Dec, and over 1 Jul of y - 1 to 30 Jun of y at 30 Jun."""
    return fx.to_eur(value, ccy, d, "pl", rates, fx.period_start(d, rolling=_rolling(d)))


def average_te(facts: pd.DataFrame, rates: pd.DataFrame) -> pd.DataFrame:
    """T-bar at every bank and date: bank_id, date, denominator, family, inputs_lineage, status."""
    te = compute_kpis(facts, TE_SPEC, None, rates)
    return te[te["basis"] == "reported"][["bank_id", "date", "denominator", "family", "inputs_lineage", "status"]]


def bank_inputs(kpi: pd.DataFrame, universe: pd.DataFrame, te: pd.DataFrame) -> dict:
    """{(date, bank, basis): inputs}: I, F, O, C, LLP, L, IEA, NII from the KPI rows, O = I - NII - F (instruction 04b
    B.3), TE from `average_te`, and the currency and lineage of each input used. Where risk_adj_nim has a numerator,
    LLP is read as NII less it, so the margin and its parts agree (instruction 06c B.1)."""
    report_ccy = dict(zip(universe["bank_id"], universe["report_ccy"], strict=True))
    want = kpi[kpi["kpi"].isin(["cost_income", "fee_share", "cost_of_risk", "nim", "risk_adj_nim", "cet1_ratio"])]
    te_of = {(r.date, r.bank_id): r for r in te.itertuples(index=False)}
    out: dict = {}
    for r in want.itertuples(index=False):
        d = out.setdefault((r.date, r.bank_id, r.basis), {"lineage": {}, "ccy": {}})
        d["lineage"][r.kpi] = r.inputs_lineage
        if pd.notna(r.denominator) and isinstance(r.family, str):
            d["ccy"][r.kpi] = _ccy(r.family, report_ccy[r.bank_id])
        if r.kpi == "cost_income":
            d["C"], d["I"] = r.numerator, r.denominator
        elif r.kpi == "fee_share":
            d["F"], d["I_fee"] = r.numerator, r.denominator
        elif r.kpi == "cost_of_risk":
            d["LLP"], d["L"] = r.numerator, r.denominator
        elif r.kpi == "nim":
            d["NII"], d["IEA"] = r.numerator, r.denominator
        elif r.kpi == "risk_adj_nim":
            d["NII_LLP"] = r.numerator
        elif r.kpi == "cet1_ratio":
            d["RWA"] = r.denominator
    for (date, bank, _), d in out.items():
        t = te_of[(date, bank)]
        d["TE"], d["TE_status"], d["lineage"]["te"] = t.denominator, t.status, t.inputs_lineage
        if pd.notna(t.denominator):
            d["ccy"]["te"] = _ccy(t.family, report_ccy[bank])
        i = d.get("I", np.nan)
        d["I"] = d.get("I_fee", np.nan) if pd.isna(i) else i
        d["O"] = d["I"] - d.get("NII", np.nan) - d.get("F", np.nan)
        if pd.notna(d.get("NII_LLP", np.nan)):
            d["LLP"] = d.get("NII", np.nan) - d["NII_LLP"]
    return out


def _standalone(gap: str, value: float, tgt: float, b: dict) -> float:
    """Kickoff Section 5.6."""
    if gap == "cost_income":
        return (value - tgt) * b.get("I", np.nan)
    if gap == "cost_of_risk":
        return (value - tgt) * b.get("L", np.nan)
    if gap in ("nim", "risk_adj_nim"):  # instruction 06c B.1 item 4
        return (tgt - value) * b.get("IEA", np.nan)
    if gap == "fee_share":
        i, f = b.get("I", np.nan), b.get("F", np.nan)
        return tgt * (i - f) / (1 - tgt) - f
    raise ValueError(gap)


def joint_gap(bank: dict, targets: dict) -> float:
    """Delta pi joint, kickoff Section 5.6 with O = other_income and the level rule of instruction 04b B.3.

    `targets` holds only the sized gaps. A driver not sized keeps the bank's own level (NII' = NII, F' = F, C' = C,
    LLP' = LLP), so it adds nothing to the difference and needs no input. I' = NII' + F' + O is written as I plus the
    income changes, which is the same thing because I = NII + F + O.

    `risk_adj_nim` (instruction 06c B.1 item 5) closes the margin gap through NII at the bank's current credit cost:
    d = target x IEA - (NII - LLP), NII' = NII + d, LLP' = LLP. The pipeline sizes it in place of `nim` and
    `cost_of_risk`, whose branches stay for `[gaps] sized` values that name them."""
    d_nii = d_fee = d_cost = d_llp = 0.0
    nii = bank.get("NII", np.nan)
    if "nim" in targets:
        d_nii = targets["nim"] * bank["IEA"] - nii
        nii = nii + d_nii
    if "risk_adj_nim" in targets:
        d_nii = targets["risk_adj_nim"] * bank["IEA"] - (nii - bank["LLP"])
        nii = nii + d_nii
    if "fee_share" in targets:
        s = targets["fee_share"]
        d_fee = s * (nii + bank["O"]) / (1 - s) - bank["F"]
    if "cost_income" in targets:
        d_cost = bank["C"] - targets["cost_income"] * (bank["I"] + d_nii + d_fee)
    if "cost_of_risk" in targets:
        d_llp = bank["LLP"] - targets["cost_of_risk"] * bank["L"]
    return d_nii + d_fee + d_cost + d_llp


class TaxRates:
    """t-bar of Convention 4.11 at a bank, date and basis: tax over profit before tax, summed over the 3 fiscal years
    ending at the date. At 30 Jun the years are the 3 rolling 12 month periods ending at 30 Jun (B.3). It is a level,
    so the years may mix families; values in different currencies are converted to EUR first (amendment 9)."""

    def __init__(self, facts: pd.DataFrame, rates: pd.DataFrame, cfg):
        self.cfg, self.rates = cfg, rates
        self.uk = set(read_source_map(cfg.root)["bank_groups"]["uk"])
        universe = read_universe(cfg.root)
        self.country = dict(zip(universe["bank_id"], universe["country"], strict=True))
        self.report_ccy = dict(zip(universe["bank_id"], universe["report_ccy"], strict=True))
        one_offs = pd.read_csv(cfg.root / "data" / "manual" / "one_offs.csv", dtype={"page": str})
        pl = facts[facts["field"].isin(["pbt", "pat"]) & facts["value"].notna()]
        self.index = {"reported": self._index(pl),
                      "underlying": self._index(underlying_facts(pl, one_offs, rates))}
        self.memo: dict = {}

    @staticmethod
    def _index(pl: pd.DataFrame) -> dict:
        out = {(r.bank_id, r.field, r.ref_date, r.family): (r.value, r.lineage_id) for r in pl.itertuples(index=False)
               if r.ref_date[5:] == "12-31"}
        for r in rolling_12m(pl).dropna(subset=["value"]).itertuples(index=False):
            out[(r.bank_id, r.field, r.date, r.family)] = (r.value, r.inputs_lineage)
        return out

    def _year(self, bank: str, d: str, basis: str):
        """(pbt, tax, ccy, lineage) of the 12 months ending at d, under the KPI family rule."""
        fam = "report" if bank in self.uk or d > self.cfg.sources.eba_last else "eba"
        pbt = self.index[basis].get((bank, "pbt", d, fam))
        pat = self.index[basis].get((bank, "pat", d, fam))
        if pbt is None or pat is None:
            return None
        return pbt[0], pbt[0] - pat[0], _ccy(fam, self.report_ccy[bank]), _join([pbt[1], pat[1]])

    def get(self, bank: str, d: str, basis: str) -> tuple[float, str, str]:
        """(rate, status, lineage). Fewer than 3 years gives the country rate, status `tax_fallback` (instruction 05
        A.1 item 3)."""
        key = (bank, d, basis)
        if key not in self.memo:
            self.memo[key] = self._compute(bank, d, basis)
        return self.memo[key]

    def _compute(self, bank: str, d: str, basis: str) -> tuple[float, str, str]:
        ends = [f"{int(d[:4]) - i}{d[4:]}" for i in range(TAX_YEARS)]
        years = [self._year(bank, e, basis) for e in ends]
        if any(y is None for y in years):
            return getattr(self.cfg.tax_fallback, self.country[bank]), "tax_fallback", _join(y[3] for y in years if y)
        mixed = len({y[2] for y in years}) > 1
        conv = (lambda v, c, e: pl_to_eur(v, c, e, self.rates)) if mixed else (lambda v, c, e: v)
        pbt = sum(conv(y[0], y[2], e) for y, e in zip(years, ends, strict=True))
        tax = sum(conv(y[1], y[2], e) for y, e in zip(years, ends, strict=True))
        lineage = _join(y[3] for y in years)
        lo, hi = TAX_BOUNDS
        if pbt <= 0 or not lo <= tax / pbt <= hi:
            return getattr(self.cfg.tax_fallback, self.country[bank]), "tax_fallback", lineage
        return tax / pbt, "ok", lineage


def is_sized(r, direction: str) -> bool:
    """B.3: verdict lagging, or in_line with the bank worse than its target, and not inside noise."""
    if pd.isna(r.target) or pd.isna(r.value) or str(r.inside_noise) != "False":
        return False
    return r.verdict == "lagging" or (r.verdict == "in_line" and better(r.target, r.value, direction))


def size_gaps(bench: pd.DataFrame, kpi: pd.DataFrame, facts: pd.DataFrame, rates: pd.DataFrame, cfg) -> pd.DataFrame:
    """GAPS: a row per date, bank, group, basis and gap of `[gaps] sized`; status `not_sized` and blank values for a
    gap that is not sized (B.3)."""
    universe = read_universe(cfg.root)
    inputs = bank_inputs(kpi, universe, average_te(facts, rates))
    tax = TaxRates(facts, rates, cfg)
    directions = _directions(cfg)
    rows = []
    for r in bench[bench["kpi"].isin(cfg.gaps.sized)].itertuples(index=False):
        row = {"date": r.date, "bank_id": r.bank_id, "group": r.group, "basis": r.basis, "gap": r.kpi,
               "delta_pi_lc": np.nan, "delta_pi_eur": np.nan, "delta_rote_pts": np.nan, "tax_rate": np.nan,
               "tax_status": "", "status": "not_sized"}
        if is_sized(r, directions[r.kpi]):
            row.update(_sized(r, inputs[(r.date, r.bank_id, r.basis)], tax, rates))
        rows.append(row)
    out = pd.DataFrame(rows, columns=GAPS_COLUMNS)
    return out.sort_values(["date", "bank_id", "group", "basis", "gap"]).reset_index(drop=True)


def _sized(r, b: dict, tax: TaxRates, rates: pd.DataFrame) -> dict:
    lc = _standalone(r.kpi, r.value, r.target, b)
    ccy = b["ccy"][r.kpi]
    t, tax_status, _ = tax.get(r.bank_id, r.date, r.basis)
    te = b.get("TE", np.nan)
    status = "ok"
    pts = np.nan
    if pd.isna(te):
        status = b["TE_status"]
    elif b["ccy"]["te"] != ccy:
        status = "mixed_family"
    else:
        pts = lc * (1 - t) / te * PCT
    return {"delta_pi_lc": lc, "delta_pi_eur": pl_to_eur(lc, ccy, r.date, rates), "delta_rote_pts": pts, "tax_rate": t,
            "tax_status": tax_status, "status": status}


def joint_table(gaps: pd.DataFrame, bench: pd.DataFrame, kpi: pd.DataFrame, facts: pd.DataFrame, rates: pd.DataFrame,
                cfg) -> pd.DataFrame:
    """GAPS_JOINT: a row per date, bank, group and basis. Joint values are blank where no gap is sized; excess capital
    is max(0, cet1_ratio - peer median) x rwa, reported separately at the date's rate."""
    universe = read_universe(cfg.root)
    inputs = bank_inputs(kpi, universe, average_te(facts, rates))
    keys = ["date", "bank_id", "group", "basis"]
    target_of = {(r.date, r.bank_id, r.group, r.basis, r.kpi): r.target for r in
                 bench[bench["kpi"].isin(cfg.gaps.sized)].itertuples(index=False)}
    cet1 = {(r.date, r.bank_id, r.group, r.basis): (r.value, r.median) for r in
            bench[bench["kpi"] == "cet1_ratio"].itertuples(index=False)}
    rows = []
    for key, g in gaps.groupby(keys, sort=True):
        date, bank, group, basis = key
        b = inputs[(date, bank, basis)]
        row = dict(zip(keys, key, strict=True))
        sized = g[g["delta_pi_lc"].notna()]
        row.update(sum_standalone_eur=np.nan, joint_eur=np.nan, overlap_eur=np.nan, joint_rote_pts=np.nan)
        if not sized.empty:
            targets = {k: target_of[(date, bank, group, basis, k)] for k in sized["gap"]}
            ccy = b["ccy"][sized["gap"].iloc[0]]
            joint_lc = joint_gap(b, targets)
            row["sum_standalone_eur"] = sized["delta_pi_eur"].sum()
            row["joint_eur"] = pl_to_eur(joint_lc, ccy, date, rates)
            row["overlap_eur"] = row["sum_standalone_eur"] - row["joint_eur"]
            t = sized["tax_rate"].iloc[0]
            if b["ccy"].get("te") == ccy:
                row["joint_rote_pts"] = joint_lc * (1 - t) / b["TE"] * PCT
        value, median = cet1.get(key[:4], (np.nan, np.nan))
        row["excess_capital_eur"] = np.nan
        if pd.notna(value) and pd.notna(median) and "cet1_ratio" in b["ccy"]:
            row["excess_capital_eur"] = fx.to_eur(max(0.0, value - median) * b["RWA"], b["ccy"]["cet1_ratio"], date,
                                                  "bs", rates, None)
        rows.append(row)
    return pd.DataFrame(rows, columns=JOINT_COLUMNS)


def gaps_range(gaps: pd.DataFrame) -> pd.DataFrame:
    """outputs/tables/gaps_range.csv (B.3): min and max over the sized cells of 3 groups x 2 bases, the headline being
    the cluster group on the underlying basis, blank if that cell is not sized."""
    rows = []
    for (date, bank, gap), g in gaps.groupby(["date", "bank_id", "gap"], sort=True):
        v = g["delta_pi_eur"].dropna()
        head = g[(g["group"] == HEADLINE[0]) & (g["basis"] == HEADLINE[1])]["delta_pi_eur"]
        rows.append({"date": date, "bank_id": bank, "gap": gap, "min_eur": v.min() if len(v) else np.nan,
                     "max_eur": v.max() if len(v) else np.nan, "headline_eur": head.iloc[0] if len(head) else np.nan,
                     "n_sized": len(v)})
    return pd.DataFrame(rows, columns=RANGE_COLUMNS)
