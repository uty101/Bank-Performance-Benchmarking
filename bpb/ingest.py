"""FACTS from raw sources (kickoff Section 6.1). Section 1 builds the EBA path; reports and Pillar 3 come in Section 2."""

from __future__ import annotations

import json
import re
from functools import cache
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from bpb.lineage import lineage_id

ROOT = Path(__file__).resolve().parents[1]
FACTS_COLUMNS = ["bank_id", "lei", "ref_date", "field", "value", "ccy", "unit_scale", "period_months", "family",
                 "locator", "lineage_id", "status"]
# instruction 01b B.1 item 1: the dimension columns of each EBA CSV
EBA_DIMS = {
    "tr_oth": ["ASSETS_FV", "ASSETS_Stages", "Exposure", "Financial_instruments"],
    "tr_cre": ["Portfolio", "Country", "Exposure", "Status", "Perf_Status", "NACE_codes"],
}
EBA_AMOUNT_SCALE = 1e6  # instruction 01b B item 9: every eba amount is EUR millions
QUARTER_END_DAY = {"03": "31", "06": "30", "09": "30", "12": "31"}


@cache
def field_meta() -> dict[str, dict]:
    """config/fields.yaml as {field: {kind, period, meaning}}."""
    with open(ROOT / "config" / "fields.yaml", encoding="utf-8") as f:
        return {r["field"]: r for r in yaml.safe_load(f)["fields"]}


def _quarter_end(period: str) -> str:
    return f"{period[:4]}-{period[4:6]}-{QUARTER_END_DAY[period[4:6]]}"


def load_eba(release_year: int, raw_root: Path, eba_map: pd.DataFrame, universe: pd.DataFrame) -> pd.DataFrame:
    """One EBA release as FACTS rows for the universe banks that have a LEI.

    The release's CSVs are read with `encoding="latin-1"`: they are not valid UTF-8 (byte 0x96 appears in labels,
    instruction 01b Section A). A map row matches a CSV row on Item, on every dimension named in its `dim_filter`,
    and on 0 in every other dimension column of that CSV (instruction 01b B.1 item 1). A field with several map
    rows is their sum, and is absent for a bank and date where any of its rows is absent (B.1 item 2).

    Units (instruction 01b B item 9): amounts are EUR millions, stored in EUR (`unit_scale` 1e6, `ccy` EUR) for
    every bank; fields of `kind: ratio` are decimals stored as reported (`unit_scale` 1, `ccy` blank). A line
    labelled `(-) ...` is a deduction the EBA reports negative; it is stored positive (Section 5.1,
    intangibles_deduction). P&L period_months = 3 × n_quarters (B.1 item 3).
    """
    meta = field_meta()
    banks = universe.loc[universe["lei"].fillna("") != "", ["bank_id", "lei"]]
    emap = eba_map.reset_index(drop=True).copy()
    emap["item"] = emap["item"].astype(str)
    emap["sign"] = [-1.0 if str(lab).startswith("(-)") else 1.0 for lab in emap["label"]]
    parts = []
    for name, dims in EBA_DIMS.items():
        path = Path(raw_root) / "eba" / str(release_year) / f"{name}.csv.gz"
        if not path.exists():
            continue
        d = pd.read_csv(path, dtype=str, encoding="latin-1", keep_default_na=False)
        d = d[d["LEI_Code"].isin(banks["lei"]) & d["Item"].isin(emap["item"]) & (d["Amount"] != "")]
        if "n_quarters" not in d:
            d = d.assign(n_quarters="")
        for i, row in emap.iterrows():
            flt = json.loads(row["dim_filter"])
            mask = d["Item"] == row["item"]
            for dim in dims:
                mask &= d[dim] == str(flt.get(dim, "0"))
            hit = d.loc[mask, ["LEI_Code", "Period", "Item", "Amount", "n_quarters"]]
            if not hit.empty:
                parts.append(hit.assign(map_row=i))
    if not parts:
        return pd.DataFrame(columns=FACTS_COLUMNS)
    sel = pd.concat(parts, ignore_index=True)
    dup = sel.duplicated(["LEI_Code", "Period", "map_row"], keep=False)
    if dup.any():
        raise ValueError(f"release {release_year}: map rows match more than 1 CSV row:\n{sel[dup].to_string()}")
    sel = sel.merge(emap[["field", "sign"]], left_on="map_row", right_index=True)
    sel["amount"] = sel["Amount"].astype(float) * sel["sign"]
    n_rows = emap.groupby("field").size()
    g = sel.groupby(["LEI_Code", "Period", "field"], sort=False).agg(
        amount=("amount", "sum"), n=("map_row", "nunique"),
        items=("Item", lambda s: "+".join(sorted(set(s)))),
        n_quarters=("n_quarters", lambda s: ",".join(sorted(set(s)))),
    ).reset_index()
    g = g[g["n"] == g["field"].map(n_rows)]  # never a partial sum

    kind = g["field"].map(lambda f: meta[f]["kind"])
    is_ratio = kind == "ratio"
    out = pd.DataFrame({
        "bank_id": g["LEI_Code"].map(dict(zip(banks["lei"], banks["bank_id"], strict=True))),
        "lei": g["LEI_Code"],
        "ref_date": g["Period"].map(_quarter_end),
        "field": g["field"],
        "value": g["amount"].where(is_ratio, g["amount"] * EBA_AMOUNT_SCALE),
        "ccy": ["" if r else "EUR" for r in is_ratio],
        "unit_scale": [1.0 if r else EBA_AMOUNT_SCALE for r in is_ratio],
        "period_months": pd.array(
            [3 * int(q) if meta[f]["period"] == "pl" else None for f, q in zip(g["field"], g["n_quarters"],
                                                                                 strict=True)],
            dtype="Int64"),
        "family": "eba",
        "locator": g["items"] + f"@{release_year}",
    })
    out["lineage_id"] = [lineage_id(b, r, f, "eba", loc) for b, r, f, loc in
                         zip(out["bank_id"], out["ref_date"], out["field"], out["locator"], strict=True)]
    out["status"] = "ok"
    return out.sort_values(["bank_id", "ref_date", "field"]).reset_index(drop=True)[FACTS_COLUMNS]


def _rule_allows(rule: dict, group: str, family: str, ref_date: str) -> bool:
    if rule["banks"] != group or rule["family"] != family:
        return False
    if "dates" in rule:
        return ref_date in rule["dates"]
    return rule["from"] <= ref_date <= rule["to"]


def apply_source_map(facts: pd.DataFrame, source_map: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Keeps each row only where `config/source_map.yaml` allows its family for that field, bank and date.

    A bank is `uk` if listed under `bank_groups: uk`, else `eu`. Returns (kept, rejected); rejected carries a
    `reason` column.
    """
    uk = set(source_map["bank_groups"]["uk"])
    rules = source_map["fields"]
    group = facts["bank_id"].map(lambda b: "uk" if b in uk else "eu")
    keys = pd.DataFrame({"field": facts["field"], "group": group, "family": facts["family"],
                         "ref_date": facts["ref_date"]})
    allowed = {}
    for k in keys.drop_duplicates().itertuples(index=False):
        allowed[tuple(k)] = any(_rule_allows(r, k.group, k.family, k.ref_date) for r in rules.get(k.field, []))
    ok = pd.Series([allowed[tuple(k)] for k in keys.itertuples(index=False)], index=facts.index, dtype=bool)
    kept = facts[ok].reset_index(drop=True)
    rejected = facts[~ok].assign(reason="family not allowed by source map for this field, bank and date")
    return kept, rejected.reset_index(drop=True)


# --- report and Pillar 3 entries (instruction 02 B.1, B.2, B.4) --------------------------------------------------

ENTRY_COLUMNS = ["bank_id", "ref_date", "field", "value_as_printed", "unit_scale", "value", "ccy", "period_months",
                 "doc_type", "report_sha256", "page", "snippet", "entered_utc"]
COMPONENT = re.compile(r"component (\d+)/(\d+)")  # the `component` note of a summed field's snippet (B.2)
# instruction 03b B.2 to B.5: a status the reviewer fixed for an entry (at1_net_of_tax, headcount, no_nci_line),
# held in an optional trailing column of report_entries.csv; blank for every other entry. Instruction 03c B.2:
# no_nci_line also marks minority_interests 0; B.4: class_from_annual marks a half year flag read from the annual report.
# Instruction 04 A.1: no_at1_coupon marks at1_coupons 0; from_comparative marks a comparative column cited on purpose,
# including the FY2025 column for 2024-12-31, which the automatic rule below does not mark
DECISION_COLUMN = "decision_status"
DECISION_STATUSES = ("at1_net_of_tax", "headcount", "no_nci_line", "class_from_annual", "no_at1_coupon",
                     "from_comparative")
VALUE_REL_TOL = 1e-9  # |value| against |value_as_printed| x unit_scale: equal up to float rounding
# instruction 02b B.4: a dash or empty cell in a printed template row is a component of value 0
ZERO_PRINTED = {"-", "–", "—", "blank"}  # hyphen, en dash, em dash, or an empty cell


def parse_printed(text: str, decimal_mark: str = ".") -> float:
    """A number as printed: brackets or a leading minus mean negative; thousands separators (`,` `.` space or thin
    space, whichever is not the declared decimal mark), currency signs and `%` are dropped."""
    s = str(text).strip()
    neg = s.startswith("(") and s.endswith(")") or s[:1] in "-−–"
    digits = "".join(ch for ch in s if ch.isdigit() or ch == decimal_mark)
    digits = digits.replace(decimal_mark, ".")
    if not any(ch.isdigit() for ch in digits) or digits.count(".") > 1:
        raise ValueError(f"not a number: {text!r}")
    v = float(digits)
    return -v if neg else v


def read_entries(path: Path) -> pd.DataFrame:
    e = pd.read_csv(path, dtype=str, keep_default_na=False)
    if list(e.columns[:len(ENTRY_COLUMNS)]) != ENTRY_COLUMNS:
        raise ValueError(f"{path}: columns {list(e.columns)} != {ENTRY_COLUMNS}")
    if DECISION_COLUMN not in e:
        e[DECISION_COLUMN] = ""
    bad = sorted(set(e[DECISION_COLUMN]) - {"", *DECISION_STATUSES})
    if bad:
        raise ValueError(f"{path}: unknown {DECISION_COLUMN} {bad}")
    return e


def entry_values(e: pd.DataFrame) -> pd.Series:
    """Each entry's value in reporting-currency units (Convention 4.1). The magnitude is |value_as_printed| x
    unit_scale. The sign is the entered `value`'s (Convention 4.2 is applied on entry); a blank `value` gives a
    positive amount for a field stored positive (expenses, impairments, allowances, deductions) and the printed sign
    otherwise. An entered value whose magnitude differs gives NaN."""
    marks = e["decimal_mark"] if "decimal_mark" in e else pd.Series(".", index=e.index)
    meta = field_meta()
    out = []
    for printed, scale, value, field, mark in zip(e["value_as_printed"], e["unit_scale"], e["value"], e["field"],
                                                 marks, strict=True):
        if meta.get(field, {}).get("kind") == "flag":  # instruction 03b B.2: the entered 1 or 0, printed is a phrase
            out.append(float(value) if str(value).strip() in ("0", "1") else np.nan)
            continue
        if str(printed).strip() in ZERO_PRINTED:
            out.append(0.0 if str(value).strip() in ("", "0") else np.nan)
            continue
        mag = abs(parse_printed(printed, mark or ".")) * float(scale)
        if str(value).strip() == "":
            sign = 1.0 if field in POSITIVE_FIELDS else (-1.0 if parse_printed(printed, mark or ".") < 0 else 1.0)
            out.append(sign * mag)
            continue
        v = float(value)
        out.append(v if abs(abs(v) - mag) <= VALUE_REL_TOL * max(mag, 1.0) else np.nan)
    return pd.Series(out, index=e.index, dtype=float)


# Convention 4.2: fields stored as positive amounts whatever sign the statement prints
POSITIVE_FIELDS = {"interest_expense", "admin_expenses", "resolution_dgs_contrib", "depreciation", "impairments_fin",
                   "provisions", "impairments_nonfin", "loans_customers_allowance", "npl_allowance",
                   "intangibles_deduction"}


# instruction 03 A.1 item 2: where no Pillar 3 report can be obtained, an EU bank's KM1 figures come from the capital
# adequacy note of the same date's interim or annual report, as family p3 with status p3_from_report
KM1_FIELDS = {"cet1", "tier1", "rwa", "cet1_ratio_reported", "leverage_exposure", "lcr", "nsfr"}
P3_FROM_REPORT = "p3_from_report"


def _family(source_map: dict, bank: str, field: str, ref_date: str, doc_type: str) -> str:
    """p3 for a pillar3 entry whose field the source map assigns to p3 at that bank group and date, else report
    (instruction 02 B.1: the family comes from the source map, doc_type only names the document). A KM1 field
    entered from an EU bank's interim or annual report is p3 on the same rule (instruction 03 A.1 item 2)."""
    group = "uk" if bank in set(source_map["bank_groups"]["uk"]) else "eu"
    if doc_type != "pillar3" and not (group == "eu" and field in KM1_FIELDS):
        return "report"
    rules = source_map["fields"].get(field, [])
    return "p3" if any(_rule_allows(r, group, "p3", ref_date) for r in rules) else "report"


def _p3_from_report(source_map: dict, bank: str, field: str, doc_type: str) -> bool:
    uk = set(source_map["bank_groups"]["uk"])
    return doc_type != "pillar3" and field in KM1_FIELDS and bank not in uk


def entries_facts(entries: pd.DataFrame, manifest: pd.DataFrame) -> pd.DataFrame:
    """Every entry as FACTS rows, family from the source map, summed fields summed (B.2).

    A summed field is entered as 1 row per printed number, each snippet carrying `component k/n`; the field is the
    sum when all n components are present and absent otherwise (decision B.1 of decisions/section_1_review.md).
    locator = report sha256 and page (`sha256@page`, `+` joined for a sum). An entry whose document is not in the
    manifest raises. Status: ok, or `value_mismatch` when an entered value disagrees with its printed number, or the
    status a caller already set in an `entry_status` column (provenance, step 2.4).
    """
    if entries.empty:
        return pd.DataFrame(columns=FACTS_COLUMNS)
    unknown = sorted(set(entries["report_sha256"]) - set(manifest["sha256"]))
    if unknown:
        raise ValueError(f"entries cite documents not in report_manifest.csv: {unknown}")
    smap = read_source_map(ROOT)
    universe = read_universe(ROOT)
    lei = dict(zip(universe["bank_id"], universe["lei"], strict=True))
    e = entries.copy()
    e["_value"] = entry_values(e)
    e["_status"] = e.get("entry_status", "ok")
    e.loc[e["_value"].isna() & (e["_status"] == "ok"), "_status"] = "value_mismatch"
    # instruction 02b B.9: a figure taken from a later document's comparative column. The FY2025 annual report's
    # 2024-12-31 column is the prescribed source for that date (instruction 02 B.3, 02b B.2), not a fallback.
    period = dict(zip(manifest["sha256"], manifest["period"], strict=True))
    dtype = dict(zip(manifest["sha256"], manifest["doc_type"], strict=True))
    comparative = [(period[s] != d) and not (dtype[s] == "annual" and period[s] == "2025-12-31" and d == "2024-12-31")
                   for s, d in zip(e["report_sha256"], e["ref_date"], strict=True)]
    e.loc[pd.Series(comparative, index=e.index) & (e["_status"] == "ok"), "_status"] = "from_comparative"
    from_report = [_p3_from_report(smap, b, f, t) for b, f, t in zip(e["bank_id"], e["field"], e["doc_type"],
                                                                     strict=True)]
    e.loc[pd.Series(from_report, index=e.index) & (e["_status"] == "ok"), "_status"] = P3_FROM_REPORT
    if DECISION_COLUMN in e:
        dec = e[DECISION_COLUMN].fillna("")
        e.loc[(dec != "") & e["_status"].isin(["ok", "from_comparative"]), "_status"] = dec
    e["_family"] = [_family(smap, b, f, d, t) for b, f, d, t in
                    zip(e["bank_id"], e["field"], e["ref_date"], e["doc_type"], strict=True)]
    rows = []
    for (bank, ref_date, field, fam), g in e.groupby(["bank_id", "ref_date", "field", "_family"], sort=True):
        comps = [COMPONENT.search(s) for s in g["snippet"]]
        if len(g) > 1 or any(comps):
            if not all(comps):
                raise ValueError(f"{bank} {ref_date} {field}: several entries, not all marked as components")
            n = {int(m.group(2)) for m in comps}
            ks = [int(m.group(1)) for m in comps]
            if len(n) != 1 or len(set(ks)) != len(ks):
                raise ValueError(f"{bank} {ref_date} {field}: inconsistent component notes {ks} / {n}")
            if set(ks) != set(range(1, n.pop() + 1)):
                continue  # a missing component makes the field missing, never a partial sum
        locator = "+".join(dict.fromkeys(f"{s}@{p}" for s, p in zip(g["report_sha256"], g["page"], strict=True)))
        built_all = ("from_comparative", P3_FROM_REPORT, *DECISION_STATUSES)
        bad = [s for s in g["_status"] if s not in ("ok", *built_all)]
        built = [s for s in built_all if s in set(g["_status"])]
        status = bad[0] if bad else (built[0] if built else "ok")
        if not bad and field == "total_operating_income" and len(g) > 1:
            status = "toi_summed"  # instruction 02b B.8: no printed total, the printed income lines summed
        scales = sorted(set(g["unit_scale"].astype(float)))
        pm = g["period_months"].iloc[0]
        rows.append({
            "bank_id": bank, "lei": lei.get(bank, ""), "ref_date": ref_date, "field": field,
            "value": np.nan if bad else float(g["_value"].sum()), "ccy": g["ccy"].iloc[0],
            "unit_scale": scales[0] if len(scales) == 1 else np.nan,
            "period_months": int(pm) if str(pm).strip() else None, "family": fam, "locator": locator,
            "lineage_id": lineage_id(bank, ref_date, field, fam, locator), "status": status,
        })
    out = pd.DataFrame(rows, columns=FACTS_COLUMNS)
    out["period_months"] = out["period_months"].astype("Int64")
    return out.reset_index(drop=True)


def read_manifest(raw_root: Path) -> pd.DataFrame:
    return pd.read_csv(Path(raw_root) / "report_manifest.csv", dtype=str, keep_default_na=False)


def load_report_entries(path: Path, manifest: pd.DataFrame) -> pd.DataFrame:
    """FACTS rows with family `report` from data/manual/report_entries.csv: every entry the source map does not
    assign to p3 (instruction 02 B.1). Rows that the source map does not allow are rejected later by
    apply_source_map."""
    f = entries_facts(read_entries(path), manifest)
    return f[f["family"] == "report"].reset_index(drop=True)


def load_p3(raw_root: Path, universe: pd.DataFrame) -> pd.DataFrame:
    """FACTS rows with family `p3`: the report_entries.csv rows whose doc_type is pillar3 and whose field the source
    map assigns to p3 for that bank group and date (instruction 02 B.1). raw_root is data/raw; the entries are read
    from data/manual next to it and the documents from data/raw/report_manifest.csv."""
    raw_root = Path(raw_root)
    e = read_entries(raw_root.parent / "manual" / "report_entries.csv")
    e = e[e["bank_id"].isin(universe["bank_id"])]
    f = entries_facts(e, read_manifest(raw_root))
    return f[f["family"] == "p3"].reset_index(drop=True)


def read_universe(root: Path) -> pd.DataFrame:
    return pd.read_csv(Path(root) / "data" / "manual" / "universe.csv", dtype=str, keep_default_na=False)


def read_source_map(root: Path) -> dict:
    with open(Path(root) / "config" / "source_map.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_eba_map(root: Path, year: int) -> pd.DataFrame:
    return pd.read_csv(Path(root) / "config" / f"eba_map_{year}.csv", dtype=str, keep_default_na=False)


def eba_facts(cfg) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Every EBA release through the source map: (kept, rejected)."""
    root = cfg.root
    universe = read_universe(root)
    frames = [load_eba(y, root / "data" / "raw", read_eba_map(root, y), universe) for y in cfg.eba.releases]
    facts = pd.concat(frames, ignore_index=True)
    return apply_source_map(facts, read_source_map(root))


def entries_with_marks(root: Path) -> pd.DataFrame:
    """report_entries.csv with each entry's declared decimal mark, from its document's row in report_urls.csv
    (blank = `.`)."""
    e = read_entries(Path(root) / "data" / "manual" / "report_entries.csv")
    urls = pd.read_csv(Path(root) / "data" / "manual" / "report_urls.csv", dtype=str, keep_default_na=False)
    man = read_manifest(Path(root) / "data" / "raw")
    if "decimal_mark" not in urls:
        urls["decimal_mark"] = ""
    marks = man.merge(urls[["bank_id", "doc_type", "period", "decimal_mark"]], how="left",
                      on=["bank_id", "doc_type", "period"])
    by_sha = dict(zip(marks["sha256"], marks["decimal_mark"].fillna(""), strict=True))
    e["decimal_mark"] = [by_sha.get(s, "") or "." for s in e["report_sha256"]]
    return e


def report_p3_facts(cfg) -> tuple[pd.DataFrame, pd.DataFrame]:
    """report and p3 rows with provenance applied (check 1): (facts, provenance CHECKS rows). A failed entry keeps
    its row with a blank value and status `provenance_failed` (Convention 4.9), so it is excluded from every KPI."""
    from bpb.checks import provenance  # checks imports this module

    root = cfg.root
    e = entries_with_marks(root)
    man = read_manifest(root / "data" / "raw")
    if e.empty:
        return pd.DataFrame(columns=FACTS_COLUMNS), provenance(e, root / "data" / "raw" / "report_text")
    prov = provenance(e, root / "data" / "raw" / "report_text")
    failed = set(prov.loc[~prov["passed"], "note"].str.extract(r"entry (\d+)")[0].astype(int))
    e["entry_status"] = ["provenance_failed" if i in failed else "ok" for i in range(len(e))]
    return entries_facts(e, man), prov


def build_facts(cfg) -> pd.DataFrame:
    """Loads every source, applies the source map and writes data/processed/facts.parquet: eba rows, and the report
    and p3 rows of data/manual/report_entries.csv after provenance (Section 2). The scope adjusted gate is
    informational (instruction 03 A.1 item 1) and blocks no bank."""
    kept, _ = eba_facts(cfg)
    rp, _ = report_p3_facts(cfg)
    rp_kept, _ = apply_source_map(rp, read_source_map(cfg.root))
    kept = pd.concat([kept, rp_kept], ignore_index=True) if len(rp_kept) else kept
    kept = kept.sort_values(["bank_id", "ref_date", "field", "family"]).reset_index(drop=True)
    out = cfg.root / "data" / "processed" / "facts.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    kept.to_parquet(out, index=False)
    return kept
