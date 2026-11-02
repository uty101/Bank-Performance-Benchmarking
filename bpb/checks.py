"""Checks (kickoff Section 5.3). Section 1 builds checks 2, 3, 4, 5, 6 and 9; checks 1, 7 and 8 come in step 2.4.

Every check writes CHECKS rows; a failed row keeps its data with passed = False. Check 9 only flags.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import yaml

from bpb.ingest import field_meta

CHECKS_COLUMNS = ["check", "bank_id", "ref_date", "field", "value_a", "value_b", "diff_abs", "diff_rel",
                  "threshold", "passed", "note"]


def _row(check, bank, ref_date, field, a, b, threshold, passed, note="", diff_rel=None) -> dict:
    diff = abs(a - b) if pd.notna(a) and pd.notna(b) else np.nan
    if diff_rel is None:
        diff_rel = diff / abs(a) if pd.notna(diff) and a != 0 else np.nan
    return {"check": check, "bank_id": bank, "ref_date": ref_date, "field": field, "value_a": a, "value_b": b,
            "diff_abs": diff, "diff_rel": diff_rel, "threshold": threshold, "passed": bool(passed), "note": note}


def _wide(facts: pd.DataFrame) -> pd.DataFrame:
    return facts.pivot_table(index=["bank_id", "ref_date", "family"], columns="field", values="value",
                             aggfunc="first")


def _income_components(root) -> list[str]:
    with open(root / "config" / "fields.yaml", encoding="utf-8") as f:
        y = yaml.safe_load(f)
    return [c for c in y["income_components"] if c != "nii"] + list(y["income_components_other"])


def identities(facts: pd.DataFrame, cfg) -> pd.DataFrame:
    """Checks 2 (balance sheet), 3 (income), 4 (CET1), 5 (period length) and 6 (currency)."""
    c = cfg.checks
    rows = []
    w = _wide(facts)
    comps = _income_components(cfg.root)
    for (bank, d, fam), r in w.iterrows():
        get = r.get
        # 2: |total_assets - total_liabilities - total_equity| / total_assets <= bs_tol
        ta, tl, te = get("total_assets"), get("total_liabilities"), get("total_equity")
        if pd.notna(ta) and pd.notna(tl) and pd.notna(te):
            diff_rel = abs(ta - tl - te) / abs(ta)
            rows.append(_row("2_balance_sheet", bank, d, "total_assets", ta, tl + te, c.bs_tol,
                             diff_rel <= c.bs_tol, fam, diff_rel))
        # 3: total_operating_income against nii + dividend_income + net_fees + income_components_other
        toi = get("total_operating_income")
        if pd.notna(toi):
            parts = {"interest_income": get("interest_income"), "interest_expense": get("interest_expense")}
            parts |= {k: get(k) for k in comps}
            missing = [k for k, v in parts.items() if pd.isna(v)]
            if missing:
                rows.append(_row("3_income", bank, d, "total_operating_income", toi, np.nan, c.income_tol, False,
                                 f"{fam}; missing: {','.join(missing)}"))
            else:
                total = parts["interest_income"] - parts["interest_expense"] + sum(parts[k] for k in comps)
                diff_rel = abs(toi - total) / abs(toi) if toi != 0 else np.inf
                rows.append(_row("3_income", bank, d, "total_operating_income", toi, total, c.income_tol,
                                 diff_rel <= c.income_tol, fam, diff_rel))
        # 4: |reported CET1 ratio - cet1 / rwa| <= cet1_tol_bps / 10000 (formula in kickoff Section 5.3)
        rep, cet1, rwa = get("cet1_ratio_reported"), get("cet1"), get("rwa")
        if pd.notna(rep) and pd.notna(cet1) and pd.notna(rwa) and rwa != 0:
            tol = c.cet1_tol_bps / 10000
            rows.append(_row("4_cet1", bank, d, "cet1_ratio_reported", rep, cet1 / rwa, tol,
                             abs(rep - cet1 / rwa) <= tol, fam))
    # 5: a P&L value at 30 Jun is 6 months year to date, at 31 Dec 12 months (instruction 01b B.1 item 3)
    meta = field_meta()
    pl = facts[facts["field"].map(lambda f: meta.get(f, {}).get("period")) == "pl"]
    for r in pl.itertuples(index=False):
        md = r.ref_date[5:]
        if md not in ("06-30", "12-31"):
            continue
        expected = 6 if md == "06-30" else 12
        got = r.period_months
        rows.append(_row("5_period_length", r.bank_id, r.ref_date, r.field,
                         float(got) if pd.notna(got) else np.nan, float(expected), np.nan,
                         pd.notna(got) and int(got) == expected, r.family, diff_rel=np.nan))
    rows += _currency(facts, cfg)
    return pd.DataFrame(rows, columns=CHECKS_COLUMNS)


def _currency(facts: pd.DataFrame, cfg) -> list[dict]:
    """Check 6: within a bank and family the currency never changes, unless data/manual/fx_events.csv says so."""
    events = pd.read_csv(cfg.root / "data" / "manual" / "fx_events.csv", dtype=str)
    rows = []
    amounts = facts[facts["ccy"].fillna("") != ""]
    for (bank, fam), g in amounts.groupby(["bank_id", "family"]):
        ccys = sorted(g["ccy"].unique())
        allowed = 1 + int((events["bank_id"] == bank).sum())
        rows.append(_row("6_currency", bank, g["ref_date"].max(), "ccy", float(len(ccys)), float(allowed), np.nan,
                         len(ccys) <= allowed, f"{fam}: {','.join(ccys)}", diff_rel=np.nan))
    return rows


def outliers(facts: pd.DataFrame, cfg) -> pd.DataFrame:
    """Check 9: a quarter on quarter change more than outlier_z standard deviations (ddof 1) from the bank's own
    mean change of that field over the history is flagged (passed = False); nothing is dropped. Changes are taken
    between consecutive quarter ends only."""
    z_max = cfg.checks.outlier_z
    rows = []
    eba = facts[facts["family"] == "eba"].copy()
    eba["q"] = pd.PeriodIndex(eba["ref_date"], freq="Q").astype("int64")
    for (bank, field), g in eba.sort_values("ref_date").groupby(["bank_id", "field"]):
        g = g.reset_index(drop=True)
        consecutive = g["q"].diff() == 1
        chg = g["value"].diff()[consecutive]
        if len(chg) < 2:
            continue
        mean, sd = chg.mean(), chg.std(ddof=1)
        for i, v in chg.items():
            if sd > 0:
                z = abs(v - mean) / sd
                rows.append(_row("9_outlier", bank, g.loc[i, "ref_date"], field, v, mean, z_max, z <= z_max,
                                 "flag only", diff_rel=z))
            else:
                rows.append(_row("9_outlier", bank, g.loc[i, "ref_date"], field, v, mean, z_max, True,
                                 "flag only; standard deviation 0", diff_rel=np.nan))
    return pd.DataFrame(rows, columns=CHECKS_COLUMNS)


def run_checks(facts: pd.DataFrame, cfg) -> pd.DataFrame:
    """CHECKS rows for every check built so far, failed rows kept and flagged."""
    out = pd.concat([identities(facts, cfg), outliers(facts, cfg)], ignore_index=True)
    return out.sort_values(["check", "bank_id", "ref_date", "field"], kind="stable").reset_index(drop=True)
