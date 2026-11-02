"""Checks (kickoff Section 5.3). Section 1 builds checks 2, 3, 4, 5, 6 and 9; step 2.4 adds checks 1, 7 and 8.

Every check writes CHECKS rows; a failed row keeps its data with passed = False. Check 9 only flags.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from bpb import fx
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
            if fam == "report":  # kickoff 5.3 item 3: only the components the bank's income statement shows
                missing = [k for k in missing if k in ("interest_income", "interest_expense")]
                parts = {k: (0.0 if pd.isna(v) else v) for k, v in parts.items()}
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


# --- check 1: provenance (kickoff 5.3 item 1, instruction 02 B.4) -------------------------------------------------

SPACES = "    "  # space, no-break space, thin space, narrow no-break space
DIGITS = "0123456789"  # ASCII only: str.isdigit() also accepts superscripts such as a footnote mark


def _page_numbers(text: str, decimal_mark: str) -> list[tuple[float, int]]:
    """Every number the page can be read as: (absolute value, decimals shown). Thousands separators are the ones
    that are not the declared decimal mark (`,` or `.`, and spaces) between digit groups of 3. Because a table row
    can print columns separated by single spaces, every grouping is offered from every run of digits: `1 234 5 678`
    gives 1, 1234, 234, 5, 5678 and 678. Brackets, signs and currency symbols are ignored (the comparison is on
    absolute values)."""
    seps = ("," if decimal_mark == "." else ".") + SPACES
    out = []
    n = len(text)
    starts = [i for i in range(n) if text[i] in DIGITS and (i == 0 or text[i - 1] not in DIGITS)]
    for i in starts:
        j = i
        while j < n and text[j] in DIGITS:
            j += 1
        head = text[i:j]
        cands = [(head, j)]
        if len(head) <= 3:  # a first group can carry thousands groups after it
            k, acc = j, head
            while k + 3 < n + 1 and k < n and text[k] in seps and all(c in DIGITS for c in text[k + 1:k + 4]) \
                    and (k + 4 >= n or text[k + 4] not in DIGITS):
                acc += text[k + 1:k + 4]
                k += 4
                cands.append((acc, k))
        for digits, end in cands:
            out.append((float(digits), 0))
            if end < n - 1 and text[end] == decimal_mark and text[end + 1] in DIGITS:
                e = end + 1
                while e < n and text[e] in DIGITS:
                    e += 1
                out.append((float(f"{digits}.{text[end + 1:e]}"), e - end - 1))
    return out


def _on_page(target: float, numbers: list[tuple[float, int]]) -> bool:
    t = abs(target)  # equal at the decimals shown: within half a unit of the last decimal, less float noise
    return any(abs(t - v) < 0.5 * 10.0 ** -d * (1 - 1e-9) or abs(round(t, d) - v) < 1e-6 * 10.0 ** -d
               for v, d in numbers)


def _read_cache(text_root: Path, sha: str) -> dict[int, str]:
    path = Path(text_root) / f"{sha}.jsonl.gz"
    if not path.exists():
        return {}
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return {(r := json.loads(line))["page"]: r["text"] for line in f}


def provenance(entries: pd.DataFrame, text_root: Path) -> pd.DataFrame:
    """Check 1 on every entry: the snippet contains value_as_printed verbatim, and |value| / unit_scale appears as a
    number on the cited page of the cached page text, at the decimals the page shows. A failing row is excluded from
    every KPI (by the caller). The decimal mark is the entry's `decimal_mark` column, `.` when absent. The note
    starts `entry <i>`, the entry's position in `entries`."""
    from bpb.ingest import entry_values

    rows = []
    if entries.empty:
        return pd.DataFrame(rows, columns=CHECKS_COLUMNS)
    e = entries.reset_index(drop=True)
    values = entry_values(e)
    marks = e["decimal_mark"] if "decimal_mark" in e else pd.Series(".", index=e.index)
    cache: dict[str, dict[int, str]] = {}
    for i, r in e.iterrows():
        sha, page = r["report_sha256"], int(r["page"])
        if sha not in cache:
            cache[sha] = _read_cache(text_root, sha)
        text = cache[sha].get(page)
        target = values[i] / float(r["unit_scale"]) if pd.notna(values[i]) else np.nan
        why = []
        if str(r["value_as_printed"]) not in str(r["snippet"]):
            why.append("value_as_printed not in snippet")
        if text is None:
            why.append("page not in cache")
        elif pd.isna(target):
            why.append("value disagrees with value_as_printed x unit_scale")
        elif not _on_page(target, _page_numbers(text, marks[i] or ".")):
            why.append("value not on page")
        note = f"entry {i}; {sha[:12]}@{page}" + (f"; {', '.join(why)}" if why else "")
        rows.append(_row("1_provenance", r["bank_id"], r["ref_date"], r["field"], target, np.nan, np.nan,
                         not why, note, diff_rel=np.nan))
    return pd.DataFrame(rows, columns=CHECKS_COLUMNS)


MERGER_SCALES = (1.0, 1e3, 1e6)  # mergers.csv records no unit: the figure may be printed in units, thousands or millions


def merger_provenance(mergers: pd.DataFrame, text_root: Path, decimal_marks: dict[str, str]) -> pd.DataFrame:
    """Check 1 on every mergers.csv row sized from a hashed PDF (instruction 02 A item 1): target_total_assets
    divided by one of MERGER_SCALES appears as a number on source_page of source_sha256. decimal_marks maps a
    document's sha256 to its declared decimal mark."""
    rows = []
    for r in mergers.itertuples(index=False):
        sha = str(r.source_sha256) if pd.notna(r.source_sha256) else ""
        if not sha:
            continue
        page = int(r.source_page)
        text = _read_cache(text_root, sha).get(page)
        nums = _page_numbers(text, decimal_marks.get(sha, ".") or ".") if text is not None else []
        hit = [s for s in MERGER_SCALES if _on_page(float(r.target_total_assets) / s, nums)]
        note = f"{r.target_name}; {sha[:12]}@{page}" + (f"; printed at scale {hit[0]:g}" if hit else
                                                         ("; page not in cache" if text is None else
                                                          "; value not on page"))
        rows.append(_row("1_provenance_merger", r.acquirer_id, r.completion_date, "target_total_assets",
                         float(r.target_total_assets), np.nan, np.nan, bool(hit), note, diff_rel=np.nan))
    return pd.DataFrame(rows, columns=CHECKS_COLUMNS)


# --- checks 7 and 8: seams at 2025-06-30 (instruction 02 B.6) ------------------------------------------------------

SEAM_DATE = "2025-06-30"
SEAM_CAPITAL_FIELDS = ["cet1", "rwa", "leverage_exposure"]
CAG_TOTAL_ASSETS_TOL = 0.02  # instruction 02 B.3: CAG total_assets from report and eba agree within 2%


def _to_eur_row(value: float, ccy: str, field: str, rates: pd.DataFrame) -> float:
    if not ccy or ccy == "EUR":
        return value
    if field_meta()[field]["period"] == "pl":
        return fx.to_eur(value, ccy, SEAM_DATE, "pl", rates, fx.period_start(SEAM_DATE, rolling=False))
    return fx.to_eur(value, ccy, SEAM_DATE, "bs", rates, None)


def seam_capital(facts: pd.DataFrame, cfg) -> pd.DataFrame:
    """Check 7: cet1, rwa and leverage_exposure at 2025-06-30, eba (value_a, EUR) against p3 (value_b, converted to
    EUR at the 2025-06-30 ECB rate), within seam_capital_tol. diff_rel = |p3 - eba| / |eba|. Flagged, not dropped."""
    rates = fx.ecb_rates(cfg.root / "data" / "raw")
    tol = cfg.checks.seam_capital_tol
    f = facts[(facts["ref_date"] == SEAM_DATE) & facts["field"].isin(SEAM_CAPITAL_FIELDS)]
    rows = []
    for (bank, field), g in f.groupby(["bank_id", "field"]):
        eba, p3 = g[g["family"] == "eba"], g[g["family"] == "p3"]
        if eba.empty or p3.empty:
            continue
        a = float(eba["value"].iloc[0])
        b = _to_eur_row(float(p3["value"].iloc[0]), p3["ccy"].iloc[0], field, rates)
        rel = abs(b - a) / abs(a) if a else np.inf
        rows.append(_row("7_seam_capital", bank, SEAM_DATE, field, a, b, tol, rel <= tol,
                         f"p3 {p3['ccy'].iloc[0]} {float(p3['value'].iloc[0]):.10g}", diff_rel=rel))
    return pd.DataFrame(rows, columns=CHECKS_COLUMNS)


def seam_pl(facts: pd.DataFrame) -> pd.DataFrame:
    """Check 8: every field present in eba and report at 2025-06-30: eba (value_a, EUR) against report (value_b,
    converted to EUR: balance sheet at the 2025-06-30 rate, P&L at the H1 2025 mean), absolute and relative
    difference. No threshold, except CAG total_assets within 2% (instruction 02 B.3)."""
    from bpb.ingest import ROOT

    rates = fx.ecb_rates(ROOT / "data" / "raw")
    f = facts[facts["ref_date"] == SEAM_DATE]
    rows = []
    for (bank, field), g in f.groupby(["bank_id", "field"]):
        eba, rep = g[g["family"] == "eba"], g[g["family"] == "report"]
        if eba.empty or rep.empty or eba["value"].isna().all() or rep["value"].isna().all():
            continue
        a = float(eba["value"].iloc[0])
        b = _to_eur_row(float(rep["value"].iloc[0]), rep["ccy"].iloc[0], field, rates)
        rel = abs(b - a) / abs(a) if a else np.nan
        if bank == "CAG" and field == "total_assets":
            rows.append(_row("8_seam_pl", bank, SEAM_DATE, field, a, b, CAG_TOTAL_ASSETS_TOL,
                             rel <= CAG_TOTAL_ASSETS_TOL, f"report {rep['ccy'].iloc[0]}", diff_rel=rel))
        else:
            rows.append(_row("8_seam_pl", bank, SEAM_DATE, field, a, b, np.nan, True,
                             f"no threshold; report {rep['ccy'].iloc[0]}", diff_rel=rel))
    return pd.DataFrame(rows, columns=CHECKS_COLUMNS)


def run_checks(facts: pd.DataFrame, cfg, provenance_rows: pd.DataFrame | None = None) -> pd.DataFrame:
    """CHECKS rows for every check built so far, failed rows kept and flagged. Checks 2 to 6 run on every family,
    check 9 on eba rows; provenance rows (check 1) are computed with the entries and passed in."""
    parts = [identities(facts, cfg), outliers(facts, cfg), seam_capital(facts, cfg), seam_pl(facts)]
    if provenance_rows is not None and len(provenance_rows):
        parts.append(provenance_rows)
    out = pd.concat([p for p in parts if len(p)], ignore_index=True)
    return out.sort_values(["check", "bank_id", "ref_date", "field"], kind="stable").reset_index(drop=True)
