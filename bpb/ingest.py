"""FACTS from raw sources (kickoff Section 6.1). Section 1 builds the EBA path; reports and Pillar 3 come in Section 2."""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path

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


def build_facts(cfg) -> pd.DataFrame:
    """Loads every source, applies the source map and writes data/processed/facts.parquet (EBA rows in Section 1)."""
    kept, _ = eba_facts(cfg)
    kept = kept.sort_values(["bank_id", "ref_date", "field", "family"]).reset_index(drop=True)
    out = cfg.root / "data" / "processed" / "facts.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    kept.to_parquet(out, index=False)
    return kept
