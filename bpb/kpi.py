"""Derived quantities, rolling 12 months, averages and KPIs (kickoff Sections 5.1, 5.2; Conventions 4.3, 4.4, 4.8).

Code holds decimals (Convention 4.7): a KPI value is numerator / denominator, and `unit` says how it is shown.
A blank value always carries a status: `missing_input:<field>`, `mixed_family` or `zero_denominator`.
"""

from __future__ import annotations

import re
from functools import cache

import numpy as np
import pandas as pd
import yaml

from bpb import fx
from bpb.config import load_config
from bpb.ingest import ROOT, field_meta, read_source_map, read_universe
from bpb.lineage import lineage_id

KPI_COLUMNS = ["bank_id", "date", "kpi", "basis", "value", "numerator", "denominator", "unit", "family",
               "inputs_lineage", "status"]
FIRST_KPI_DATE = "2021-12-31"  # kickoff Section 3.3 and Correction 3: the first KPI year is FY2021
# instruction 03 B.4: one offs sit in a cost line (their amount is added back) or in an income component (a gain,
# entered negative, is removed); the pre tax effect also reaches the profit lines, with tax not adjusted
# (Convention 4.8), and an income component's effect reaches total operating income
ONE_OFF_COSTS = {"interest_expense", "admin_expenses", "resolution_dgs_contrib", "depreciation", "impairments_fin",
                 "provisions", "impairments_nonfin"}
ONE_OFF_PROFIT = ["pbt", "pat", "profit_owners"]
# instruction 03 step 3.4: rote for EU banks at EBA dates combines eba rows with report rows (at1_coupons,
# minority_interests) under the mixed currency rule (amendment 9), so its 2 derived inputs may be eba+report there
EBA_MIXED = {"profit_to_ordinary", "tangible_equity"}
FAMILY_ORDER = ["eba", "p3", "report"]  # a KPI at 2025-06-30 stays eba (OPEN-03); one family per value
OK = "ok"
# statuses that describe how a value was built but leave it usable (instruction 01b B.2; instruction 02 B.2)
# instruction 02b: dep_in_admin (B.5), toi_summed (B.8), from_comparative (B.9); instruction 03 A.1 item 2:
# p3_from_report. A status of several of these is joined with ";".
# instruction 03b: at1_liability (B.2), at1_net_of_tax (B.3), headcount (B.4), no_nci_line (B.5); instruction 03c:
# coupon_in_pl (B.1), class_from_annual (B.4); instruction 04 A.1: no_at1_coupon
USABLE = (OK, "fx_combined", "levies_in_admin", "dep_in_admin", "toi_summed", "from_comparative", "p3_from_report",
          "at1_liability", "at1_net_of_tax", "headcount", "no_nci_line", "coupon_in_pl", "class_from_annual",
          "no_at1_coupon")
# instruction 03c B.1: (flag field, flag value, field set to 0, status); where the bond sits and where its coupon is
# charged are separate questions
AT1_RULES = [("at1_in_equity", 0.0, "at1_instruments", "at1_liability"),
             ("at1_coupon_in_pl", 1.0, "at1_coupons", "coupon_in_pl")]
# fields a report income statement may fold into administrative expenses: opex takes them as 0 with a status
IN_ADMIN = {"resolution_dgs_contrib": "levies_in_admin", "depreciation": "dep_in_admin"}


def usable(status) -> bool:
    return pd.isna(status) or all(s in USABLE for s in str(status).split(";"))


@cache
def derived_formulas() -> dict[str, list[tuple[float, str]]]:
    """fields.yaml `derived` as {name: [(sign, input), ...]}, in file order."""
    with open(ROOT / "config" / "fields.yaml", encoding="utf-8") as f:
        raw = yaml.safe_load(f)["derived"]
    out = {}
    for name, expr in raw.items():
        terms = re.findall(r"([+-]?)\s*(\w+)", expr)
        out[name] = [(-1.0 if s == "-" else 1.0, fld) for s, fld in terms]
    return out


@cache
def quantity_period() -> dict[str, str]:
    """pl or bs for every base field and derived quantity (a derived quantity is pl if any input is pl)."""
    period = {f: m["period"] for f, m in field_meta().items()}
    for name, terms in derived_formulas().items():
        period[name] = "pl" if any(period[f] == "pl" for _, f in terms) else "bs"
    return period


def _missing(field: str) -> str:
    return f"missing_input:{field}"


def _join(ids) -> str:
    out = set()
    for s in ids:
        if isinstance(s, str) and s:
            out.update(s.split(";"))
    return ";".join(sorted(out))


def at1_rules(facts: pd.DataFrame) -> pd.DataFrame:
    """Instruction 03c B.1: where at1_in_equity is 0 at a bank and date, AT1 is not in total_equity, so the
    at1_instruments term of tangible_equity is 0 there, status at1_liability; where at1_coupon_in_pl is 1, the coupons
    are inside interest expense, so profit_owners is already net of them and at1_coupons is 0, status coupon_in_pl.
    Every family's row of the field at that bank and date is set to 0; a field with no row gets a report row. Where a
    flag has the other value, or is not entered, nothing changes."""
    out = facts.copy()
    new = []
    ccy_of = dict(zip(*(read_universe(ROOT)[c] for c in ("bank_id", "report_ccy")), strict=True))
    for flag_field, flag_value, field, status in AT1_RULES:
        for r in facts[(facts["field"] == flag_field) & (facts["value"] == flag_value)].itertuples(index=False):
            hit = (out["bank_id"] == r.bank_id) & (out["ref_date"] == r.ref_date) & (out["field"] == field)
            if hit.any():
                out.loc[hit, ["value", "status"]] = [0.0, status]
                out.loc[hit, "lineage_id"] = [_join([x, r.lineage_id]) for x in out.loc[hit, "lineage_id"]]
            else:
                new.append({**r._asdict(), "field": field, "value": 0.0, "status": status,
                            "ccy": ccy_of.get(r.bank_id, ""), "family": "report",
                            "period_months": 12 if field == "at1_coupons" and r.ref_date[5:] == "12-31" else
                            (6 if field == "at1_coupons" else pd.NA)})
    if new:
        add = pd.DataFrame(new)[out.columns]
        out = pd.concat([out, add], ignore_index=True)
    return out


def derived(facts: pd.DataFrame, rates: pd.DataFrame) -> pd.DataFrame:
    """The derived quantities of Section 5.1 at every bank, date and family where any input exists.

    Returns FACTS-like rows (bank_id, ref_date, field, value, ccy, period_months, family, lineage_id, status), where
    lineage_id lists the inputs' lineage IDs. Inputs come from one family where one family holds them all.
    Otherwise inputs are taken across families in the order eba, p3, report, any non-EUR value is converted to EUR
    at the Convention 4.6 rate (instruction 01b B.2) and the status gains `fx_combined`. A missing input gives a
    blank value with `missing_input:<field>`, naming the base field that is missing.
    """
    base = facts[["bank_id", "ref_date", "field", "value", "ccy", "period_months", "family", "lineage_id",
                  "status"]].copy()
    table = base.copy()
    rows_out = []
    for name, terms in derived_formulas().items():
        inputs = [f for _, f in terms]
        sub = table[table["field"].isin(inputs)]
        new = []
        for (bank, ref_date), g in sub.groupby(["bank_id", "ref_date"], sort=True):
            by_fam = {fam: gg.set_index("field") for fam, gg in g.groupby("family")}
            done = False
            for fam in sorted(by_fam, key=lambda x: FAMILY_ORDER.index(x) if x in FAMILY_ORDER else 99):
                gg = by_fam[fam]
                if all(f in gg.index for f in inputs):
                    new.append(_combine(name, bank, ref_date, terms, [gg.loc[f] for f in inputs], fam, rates))
                    done = True
                elif fam == "report" and (miss := [f for f in inputs if f not in gg.index])                         and all(f in IN_ADMIN for f in miss) and len(miss) < len(inputs):
                    # instruction 02 B.2 and 02b B.5: no levy line, or no depreciation line, in the income
                    # statement means it sits in administrative expenses; opex takes it as 0 with status
                    # levies_in_admin or dep_in_admin, never a missing input
                    ref = gg.loc[next(f for f in inputs if f not in miss)]
                    picks = [pd.Series({"value": 0.0, "ccy": ref["ccy"], "period_months": ref["period_months"],
                                        "family": fam, "lineage_id": "", "status": OK}, name=f)
                             if f in miss else gg.loc[f] for f in inputs]
                    row = _combine(name, bank, ref_date, terms, picks, fam, rates)
                    if usable(row["status"]):
                        row["status"] = ";".join(dict.fromkeys(
                            [s for s in str(row["status"]).split(";") if s != OK] + [IN_ADMIN[f] for f in miss]))
                    new.append(row)
                    done = True
            # instruction 03 step 3.4: rote's inputs at an EBA date are eba first, with report rows where eba has none,
            # even when the report family alone holds every input (the eba+report row is the one rote uses there)
            mixed = name in EBA_MIXED and "eba" in by_fam and not all(f in by_fam["eba"].index for f in inputs)
            if done and not mixed:
                continue
            picks = []
            for f in inputs:
                cands = [by_fam[fam].loc[f] for fam in FAMILY_ORDER if fam in by_fam and f in by_fam[fam].index]
                picks.append(cands[0] if cands else None)
            if any(p is None for p in picks):
                miss = inputs[[p is None for p in picks].index(True)]
                new.append({"bank_id": bank, "ref_date": ref_date, "field": name, "value": np.nan, "ccy": "",
                            "period_months": pd.NA, "family": "+".join(sorted(by_fam)),
                            "lineage_id": _join(p["lineage_id"] for p in picks if p is not None),
                            "status": _missing(miss)})
            else:
                fam = "+".join(sorted({p["family"] for p in picks}))
                new.append(_combine(name, bank, ref_date, terms, picks, fam, rates))
        new_df = pd.DataFrame(new, columns=base.columns)
        rows_out.append(new_df)
        table = pd.concat([table, new_df], ignore_index=True)
    out = pd.concat(rows_out, ignore_index=True)
    return out.sort_values(["bank_id", "ref_date", "field", "family"]).reset_index(drop=True)


def _combine(name, bank, ref_date, terms, rows, family, rates) -> dict:
    lineage = _join(r["lineage_id"] for r in rows)
    bad = [r for r in rows if not usable(r["status"])]
    pm = next((r["period_months"] for r in rows if pd.notna(r["period_months"])), pd.NA)
    if bad:
        return {"bank_id": bank, "ref_date": ref_date, "field": name, "value": np.nan, "ccy": "",
                "period_months": pm, "family": family, "lineage_id": lineage, "status": bad[0]["status"]}
    ccys = {r["ccy"] for r in rows}
    status, ccy = OK, next(iter(ccys))
    carried = [s for r in rows for s in str(r["status"]).split(";") if s not in (OK, "fx_combined", "nan")]
    if carried:
        status = ";".join(dict.fromkeys(carried))
    values = [float(r["value"]) for r in rows]
    if len(ccys) > 1:  # instruction 01b B.2: convert the non-EUR values to EUR first
        status, ccy = "fx_combined", "EUR"
        for i, r in enumerate(rows):
            if r["ccy"] != "EUR":
                if quantity_period()[r.name] == "pl":
                    start = fx.period_start(ref_date, rolling=False)
                    values[i] = fx.to_eur(values[i], r["ccy"], ref_date, "pl", rates, start)
                else:
                    values[i] = fx.to_eur(values[i], r["ccy"], ref_date, "bs", rates, None)
    value = sum(s * v for (s, _), v in zip(terms, values, strict=True))
    return {"bank_id": bank, "ref_date": ref_date, "field": name, "value": value, "ccy": ccy, "period_months": pm,
            "family": family, "lineage_id": lineage, "status": status}


def _pieces(df: pd.DataFrame) -> dict:
    """{(bank, field, ref_date): {family: row}} from a FACTS-like frame."""
    out: dict = {}
    for r in df.itertuples(index=False):
        out.setdefault((r.bank_id, r.field, r.ref_date), {})[r.family] = r
    return out


def _piece_status(r) -> str:
    st = getattr(r, "status", OK)
    return OK if usable(st) else st


def _span(index, bank: str, field: str, dates: list[str]):
    """Rows for the given dates from one family: (family, rows) or the status explaining the blank."""
    got = [index.get((bank, field, d), {}) for d in dates]
    for i, g in enumerate(got):
        if not g:
            return None, _missing(field)
        bad = [_piece_status(r) for r in g.values() if _piece_status(r) != OK]
        if len(bad) == len(g):
            return None, bad[0]
    common = set.intersection(*(set(g) for g in got))
    common = [f for f in FAMILY_ORDER if f in common] + sorted(f for f in common if f not in FAMILY_ORDER)
    for fam in common:
        rows = [g[fam] for g in got]
        if all(_piece_status(r) == OK for r in rows):
            return fam, rows
    return None, "mixed_family"


def _carried(rows) -> str:
    """The usable statuses of the input rows, joined with ";" in USABLE order (OK when there are none)."""
    st = {s for r in rows if r is not None for s in str(getattr(r, "status", OK)).split(";") if s not in (OK, "nan")}
    return ";".join(sorted(st, key=USABLE.index)) or OK


def _flat(fam_rows, op) -> dict:
    fam, rows = fam_rows
    if fam is None:
        return {"value": np.nan, "family": "", "lineage": "", "status": rows}
    return {"value": op([float(r.value) for r in rows]), "family": fam,
            "lineage": _join(r.lineage_id for r in rows), "status": _carried(rows)}


def rolling_12m(pl: pd.DataFrame) -> pd.DataFrame:
    """R(y) = H1(y) + FY(y - 1) - H1(y - 1) at 30 Jun of every year y with any of its 3 pieces, all 3 from one
    family (Convention 4.3). Columns: bank_id, date, field, value, family, inputs_lineage, status."""
    index = _pieces(pl)
    keys = {(b, f, int(d[:4]) + (0 if d[5:] == "06-30" else 1)) for b, f, d in index if d[5:] in ("06-30", "12-31")}
    rows = []
    for bank, field, y in sorted(keys):
        dates = [f"{y}-06-30", f"{y - 1}-12-31", f"{y - 1}-06-30"]
        r = _flat(_span(index, bank, field, dates), lambda v: v[0] + v[1] - v[2])
        rows.append({"bank_id": bank, "date": dates[0], "field": field, "value": r["value"], "family": r["family"],
                     "inputs_lineage": r["lineage"], "status": r["status"]})
    return pd.DataFrame(rows, columns=["bank_id", "date", "field", "value", "family", "inputs_lineage", "status"])


def averages(bs: pd.DataFrame) -> pd.DataFrame:
    """(balance at d one year earlier + balance at d) / 2 at every 31 Dec and 30 Jun d with any end present, both
    ends from one family (Convention 4.4). Columns as rolling_12m."""
    index = _pieces(bs)
    keys = set()
    for b, f, d in index:
        if d[5:] in ("06-30", "12-31"):
            keys.add((b, f, d))
            keys.add((b, f, f"{int(d[:4]) + 1}{d[4:]}"))
    rows = []
    for bank, field, d in sorted(keys):
        dates = [f"{int(d[:4]) - 1}{d[4:]}", d]
        r = _flat(_span(index, bank, field, dates), lambda v: (v[0] + v[1]) / 2)
        rows.append({"bank_id": bank, "date": d, "field": field, "value": r["value"], "family": r["family"],
                     "inputs_lineage": r["lineage"], "status": r["status"]})
    return pd.DataFrame(rows, columns=["bank_id", "date", "field", "value", "family", "inputs_lineage", "status"])


def kpi_dates(facts: pd.DataFrame) -> list[str]:
    last = facts["ref_date"].max()
    return [d.strftime("%Y-%m-%d") for d in pd.date_range(FIRST_KPI_DATE, last, freq="QE")
            if d.month in (6, 12)]


def _income_fields() -> set[str]:
    with open(ROOT / "config" / "fields.yaml", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return {"interest_income", "dividend_income", "net_fees"} | set(raw["income_components_other"])


def underlying_facts(facts: pd.DataFrame, one_offs: pd.DataFrame, rates: pd.DataFrame) -> pd.DataFrame:
    """FACTS on the underlying basis (Convention 4.8, instruction 03 B.4): each one off's pre tax `amount` (positive
    when it reduced profit) taken out of the field it sits in, in every family's row of that bank, date and field.

    A cost field's underlying value is reported - amount; an income component's is reported + amount (a gain is
    entered negative), and total operating income moves with it. pbt, pat and profit_owners move by + amount: the
    item is added back or removed before tax and tax is not adjusted. The amount is in the bank's reporting currency;
    a row in another currency (an eba row, EUR) gets it converted at the P&L rate of the year to date (Convention
    4.6) and status fx_combined. Each adjusted row's lineage gains the one off's lineage ID. Fields not touched are
    unchanged."""
    out = facts.copy()
    if one_offs is None or one_offs.empty:
        return out
    ccy_of = dict(zip(*(read_universe(ROOT)[c] for c in ("bank_id", "report_ccy")), strict=True))
    income = _income_fields()
    for o in one_offs.itertuples(index=False):
        amount = float(o.amount)
        lin = lineage_id(o.bank_id, o.ref_date, o.field, "one_off", f"{o.report_sha256}@{o.page}")
        effects = {o.field: -amount if o.field in ONE_OFF_COSTS else amount}
        if o.field in income:
            effects["total_operating_income"] = amount
        effects.update({f: amount for f in ONE_OFF_PROFIT})
        for field, eff in effects.items():
            hit = (out["bank_id"] == o.bank_id) & (out["ref_date"] == o.ref_date) & (out["field"] == field)
            for i in out.index[hit & out["value"].notna()]:
                row_ccy, e = out.at[i, "ccy"], eff
                if row_ccy and row_ccy != ccy_of[o.bank_id]:
                    e = fx.to_eur(eff, ccy_of[o.bank_id], o.ref_date, "pl", rates,
                                  fx.period_start(o.ref_date, rolling=False))
                    st = [s for s in str(out.at[i, "status"]).split(";") if s not in (OK, "nan")]
                    out.at[i, "status"] = ";".join(dict.fromkeys(st + ["fx_combined"]))
                out.at[i, "value"] = float(out.at[i, "value"]) + e
                out.at[i, "lineage_id"] = _join([out.at[i, "lineage_id"], lin])
    return out


def compute_kpis(facts: pd.DataFrame, kpis: dict, one_offs: pd.DataFrame, rates: pd.DataFrame) -> pd.DataFrame:
    """Every KPI of config/kpis.yaml for every bank in `facts` at every KPI date, on both bases (Section 5.2).

    P&L quantities are the FY value at 31 Dec and the rolling 12 months at 30 Jun (Convention 4.3); averaged
    denominators follow Convention 4.4. Numerator and denominator come from one family, eba first. The underlying
    basis is the same computation on `underlying_facts` (Convention 4.8, step 3.3).
    """
    rep = _kpis_one_basis(facts, kpis, rates).assign(basis="reported")
    und = _kpis_one_basis(underlying_facts(facts, one_offs, rates), kpis, rates).assign(basis="underlying")
    out = pd.concat([rep, und], ignore_index=True)
    order = {k["kpi"]: i for i, k in enumerate(kpis["kpis"])}
    out["_k"] = out["kpi"].map(order)
    out = out.sort_values(["bank_id", "date", "_k", "basis"], kind="stable").drop(columns="_k")
    return out.reset_index(drop=True)


def _kpis_one_basis(facts: pd.DataFrame, kpis: dict, rates: pd.DataFrame) -> pd.DataFrame:
    facts = at1_rules(facts)
    period = quantity_period()
    dq = derived(facts, rates)
    q = pd.concat([facts[["bank_id", "ref_date", "field", "value", "family", "lineage_id", "status"]],
                   dq[["bank_id", "ref_date", "field", "value", "family", "lineage_id", "status"]]],
                  ignore_index=True)
    # currency of each (bank, field, family): a P&L numerator converted to EUR (Section 5.2) needs it
    ccys = pd.concat([facts[["bank_id", "field", "family", "ccy"]], dq[["bank_id", "field", "family", "ccy"]]])
    ccys = ccys[ccys["ccy"].fillna("") != ""].drop_duplicates(["bank_id", "field", "family"])
    ccy_of = {(b, f, fam): c for b, f, fam, c in ccys.itertuples(index=False)}
    pl = q[q["field"].map(period) == "pl"]
    bs = q[q["field"].map(period) == "bs"]
    roll = rolling_12m(pl).rename(columns={"inputs_lineage": "lineage_id"})
    avg = averages(bs).rename(columns={"inputs_lineage": "lineage_id"})
    point = _pieces(q)
    roll_i = _pieces(roll.rename(columns={"date": "ref_date"}))
    avg_i = _pieces(avg.rename(columns={"date": "ref_date"}))

    eba_last = load_config(ROOT / "config.toml").sources.eba_last
    uk = set(read_source_map(ROOT)["bank_groups"]["uk"])

    def quantity(bank, field, d, average):
        # a KPI of an EU bank at an EBA date stays eba (OPEN-03: report rows there are seam checks and bridge inputs
        # only); after the last EBA date it comes from the report and p3 families. A UK bank is report family at
        # every date (kickoff 3.3).
        if bank in uk:
            keep = lambda f: f != "eba"
        else:
            keep = ((lambda f: f == "eba" or (field in EBA_MIXED and f.startswith("eba+"))) if d <= eba_last
                    else (lambda f: f != "eba"))
        if field == "1":
            fams = [f for f in FAMILY_ORDER if keep(f)]
            return {fam: None for fam in fams}, None
        if period.get(field) == "pl":
            src = point if d[5:] == "12-31" else roll_i
        else:
            src = avg_i if average else point
        got = src.get((bank, field, d), {})
        return {f: r for f, r in got.items() if keep(f)}, field

    eur = set(kpis.get("eur_converted", []))

    def to_eur(bank, field, fam, d, value):
        # Section 5.2: income_fte, cost_fte and cost_customer convert their P&L numerator to EUR at the mean rate of
        # its period (Convention 4.6): the fiscal year at 31 Dec, the rolling 12 months at 30 Jun
        c = ccy_of.get((bank, field, fam), "EUR")
        if c == "EUR":
            return value
        return fx.to_eur(value, c, d, "pl", rates, fx.period_start(d, rolling=d[5:] == "06-30"))

    rows = []
    banks = sorted(facts["bank_id"].unique())
    for bank in banks:
        for d in kpi_dates(facts):
            for k in kpis["kpis"]:
                rows.append(_one_kpi(bank, d, k, quantity, to_eur if k["kpi"] in eur else None))
    return pd.DataFrame(rows, columns=KPI_COLUMNS)


def _one_kpi(bank, d, k, quantity, to_eur=None) -> dict:
    row = {"bank_id": bank, "date": d, "kpi": k["kpi"], "basis": "reported", "value": np.nan, "numerator": np.nan,
           "denominator": np.nan, "unit": k["unit"], "family": "", "inputs_lineage": "", "status": ""}
    num, nf = quantity(bank, k["numerator"], d, False)
    den, df_ = quantity(bank, str(k["denominator"]), d, bool(k["average"]))
    if not num:
        row["status"] = _missing(nf)
        return row
    if df_ is not None and not den:
        row["status"] = _missing(df_)
        return row
    for part in (num, den if df_ is not None else {}):  # only blank pieces: their status explains the blank
        if part and all(_piece_status(p) != OK for p in part.values()):
            row["status"] = _piece_status(next(iter(part.values())))
            return row
    # a family common to numerator and denominator: eba, p3, report first, then a combined one such as eba+report
    common = [f for f in num if df_ is None or f in den]
    fams = sorted(common, key=lambda f: FAMILY_ORDER.index(f) if f in FAMILY_ORDER else len(FAMILY_ORDER))
    if fams:
        fam = fams[0]
        n = num[fam]
        dn = den[fam] if df_ is not None else None
    elif df_ is not None and set(num) | set(den) <= {"p3", "report"}:
        # after the last EBA date a ratio may pair a p3 amount with a report amount (e.g. rwa / total_assets): both
        # are the bank's own disclosures at the same date; averages and rolling sums stay within one family
        fn, fd = next(f for f in ("p3", "report") if f in num), next(f for f in ("p3", "report") if f in den)
        n, dn, fam = num[fn], den[fd], f"{fn}+{fd}"
    else:
        row["status"] = "mixed_family"
        return row
    for part in (n, dn):
        if part is not None and _piece_status(part) != OK:
            row["status"] = _piece_status(part)
            return row
    nv = float(n.value)
    if to_eur is not None:
        nv = to_eur(bank, k["numerator"], fam.split("+")[0], d, nv)
    dv = 1.0 if dn is None else float(dn.value)
    row.update(numerator=nv, denominator=dv, family=fam,
               inputs_lineage=_join([n.lineage_id] + ([dn.lineage_id] if dn is not None else [])))
    if dv == 0:
        row["status"] = "zero_denominator"
        return row
    row.update(value=nv / dv, status=_carried([n, dn]))
    return row
