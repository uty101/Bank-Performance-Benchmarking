"""Step 1.2: fills `lei` for EU banks and writes config/eba_map_{year}.csv (instruction 01 Section C).

No network: reads the committed SDD.xlsx and TR_Metadata.xlsx of each release under data/raw/eba/.

usage: python scripts/build_eba_maps.py   (prints the review evidence to stdout)

Name matching (instruction 01, step 1.2): casefold, strip accents and punctuation (punctuation becomes a
space, so "A/S" reads "a s"), remove the listed legal suffixes as whole words, then an exact match to
exactly 1 normalised 2025 name, else containment in exactly 1 (as a run of whole words).

Map matching: each field names its template and its label as printed in the 2025 SDD.xlsx. In every
release the label is matched exactly, after casefolding and collapsing whitespace, within that template.
A dimension filter is matched on the dimension value labels of that release's TR_Metadata.xlsx. A field
whose label has no exact match in an earlier release is mapped through the 2025 SDD crosswalk column
Item_TR_{year} and both labels are printed side by side. More than 1 fit is never guessed.
"""

from __future__ import annotations

import csv
import io
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EBA = ROOT / "data" / "raw" / "eba"
RELEASES = [2021, 2022, 2023, 2024, 2025]
EU_COUNTRIES = {"FI", "NO", "DK", "SE", "NL", "BE", "FR", "DE", "ES", "IT"}

SUFFIXES = ["ag", "sa", "s a", "spa", "s p a", "plc", "ab", "publ", "nv", "n v", "asa", "oyj", "a s", "u a",
            "se", "group", "groep", "gruppo", "banca", "banco", "bank"]
ALIASES = {"BBVA": "Banco Bilbao Vizcaya Argentaria",
           "DBK": "Deutsche Bank Aktiengesellschaft"}  # OPEN-17 (a), instruction 01b

# field -> (template, label as printed in the 2025 SDD, {dimension: dimension value label}), or a list of such
# rows when the field is a sum (instruction 01b B.1 item 2). Every dimension column of the source CSV that a
# row does not name is 0, "Total / No breakdown" (instruction 01b B.1 item 1).
SPEC: dict[str, tuple[str, str, dict[str, str]] | list[tuple[str, str, dict[str, str]]]] = {
    "interest_income": ("P&L", "Interest income", {}),
    "interest_expense": ("P&L", "Interest expenses", {}),
    "dividend_income": ("P&L", "Dividend income", {}),
    "net_fees": ("P&L", "Net Fee and commission income", {}),
    "total_operating_income": ("P&L", "TOTAL OPERATING INCOME_ NET", {}),
    "admin_expenses": ("P&L", "(Administrative expenses)", {}),
    "resolution_dgs_contrib": ("P&L", "(Cash contributions to resolution funds and deposit guarantee schemes)", {}),
    "depreciation": ("P&L", "(Depreciation)", {}),
    "impairments_fin": ("P&L", ("(Impairment or (-) reversal of impairment on financial assets not measured at "
                               "fair value through profit or loss)"), {}),
    "provisions": ("P&L", "(Provisions or (-) reversal of provisions)", {}),
    "impairments_nonfin": ("P&L", ("(Impairment or (-) reversal of impairment of investments in subsidaries_ joint "
                                  "ventures and associates and on non-financial assets)"), {}),
    "pbt": ("P&L", "PROFIT OR (-) LOSS BEFORE TAX FROM CONTINUING OPERATIONS", {}),
    "pat": ("P&L", "PROFIT OR (-) LOSS AFTER TAX FROM CONTINUING OPERATIONS", {}),
    "profit_owners": ("P&L", "PROFIT OR (-) LOSS FOR THE YEAR - Of which attributable to owners of the parent", {}),
    "total_assets": ("Assets", "Total Assets", {}),
    "total_liabilities": ("Liabilities", "TOTAL LIABILITIES", {}),
    "total_equity": ("Liabilities", "TOTAL EQUITY", {}),
    "cash_cb": ("Assets", "Cash, cash balances at central banks and other demand deposits", {}),
    "loans_all": ("NPE", "Gross carrying amount on Loans and advances (including at amortised cost  and fair value)",
                  {}),
    "loans_households_gross": ("NPE", ("Gross carrying amount on Loans and advances (including at amortised cost  and "
                                      "fair value) - by exposure"), {"Exposure": "Households"}),
    "npl_gross": ("NPE", "Gross carrying amount on Loans and advances (including at amortised cost  and fair value)",
                  {"Perf_Status": "Non Performing"}),
    "npl_allowance": ("NPE", ("Accumulated impairment, accumulated changes in fair value due to credit risk and "
                             "provisions on Loans and advances (including at amortised cost  and fair value)"),
                      {"Perf_Status": "Non Performing"}),
    "trading_assets": ("Assets", "Financial assets held for trading", {}),
    "tier1": ("Capital", "TIER 1 CAPITAL (net of deductions and after transitional adjustments)", {}),
    "rwa": ("RWA OV1", "Total Risk exposure amount", {}),
    "at1_instruments": ("Capital", "Additional Tier 1 Capital instruments", {}),
    "intangibles_deduction": ("Capital", "(-) Intangible assets (including Goodwill)", {}),
    # OPEN-06 (a): every P&L line between net fees and TOTAL OPERATING INCOME, NET
    "gains_derecognition_not_fvtpl": ("P&L", ("Gains or (-) losses on derecognition of financial assets and "
                                             "liabilities not measured at fair value through profit or loss_ and of "
                                             "non financial assets_ net"), {}),
    "gains_held_for_trading": ("P&L", "Gains or (-) losses on financial assets and liabilities held for trading_ net",
                               {}),
    "gains_designated_fvtpl": ("P&L", ("Gains or (-) losses on financial assets and liabilities designated at fair "
                                      "value through profit or loss_ net"), {}),
    "gains_hedge_accounting": ("P&L", "Gains or (-) losses from hedge accounting_ net", {}),
    "exchange_differences": ("P&L", "Exchange differences [gain or (-) loss]_ net", {}),
    "other_operating_net": ("P&L", "Net other operating income /(expenses)", {}),
}
INCOME_COMPONENTS_OTHER = ["gains_derecognition_not_fvtpl", "gains_held_for_trading", "gains_designated_fvtpl",
                           "gains_hedge_accounting", "exchange_differences", "other_operating_net"]

# Decided in instruction 01b Section B (OPEN-18 to OPEN-23).
# Exposure sub-codes 311 (NFC - SME), 312 (NFC - collateralised by commercial immovable property),
# 431 (households - residential immovable property) and 432 (households - credit for consumption) sit inside
# 301 and 401 and are never summed (instruction 01b B item 6).
CUSTOMER_SECTORS = ("General governments", "Financial corporations other than credit institutions",
                    "Non-financial corporations", "Households")
SPEC |= {
    "cet1": ("Capital", ("COMMON EQUITY TIER 1 CAPITAL (net of deductions and after applying transitional "
                         "adjustments)"), {}),
    "cet1_ratio_reported": ("Capital", "COMMON EQUITY TIER 1 CAPITAL RATIO (transitional period)", {}),
    "leverage_exposure": ("Leverage", ("Total leverage ratio exposures - using a transitional definition of Tier 1 "
                                       "capital"), {}),
    "debt_securities": ("NPE", "Gross carrying amount on Debt securities (including at amortised cost  and fair value)",
                        {}),
    "loans_customers_gross": [("NPE", ("Gross carrying amount on Loans and advances (including at amortised cost  and "
                                       "fair value) - by exposure"), {"Exposure": e})
                              for e in CUSTOMER_SECTORS],
    "loans_customers_allowance": [("NPE", ("Accumulated impairment, accumulated changes in fair value due to credit "
                                           "risk and provisions on Loans and advances (including at amortised cost  "
                                           "and fair value) - by exposure"), {"Exposure": e, "Perf_Status": p})
                                  for e in CUSTOMER_SECTORS for p in ("Performing", "Non Performing")],
    "deposits_customers": [("Liabilities", "Financial liabilities -  by instrument and by counterparty sector",
                            {"Financial_instruments": "Deposits", "Exposure": e})
                           for e in CUSTOMER_SECTORS],
}
NOT_EBA = {"minority_interests": "OPEN-24 (a): report family at every EU date (Section 3)",
           "lcr": "OPEN-05 (a): no family for EU banks to 2025-06-30",
           "nsfr": "OPEN-05 (a): no family for EU banks to 2025-06-30",
           "fte": "report family only", "customers": "report family only",
           "at1_coupons": "report family only", "shares_out": "report family only"}


def norm_label(s: str) -> str:
    return re.sub(r"\s+", " ", str(s)).strip().casefold()


def norm_name(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s).casefold())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^\w\s]|_", " ", s)
    words = s.split()
    for suf in sorted(SUFFIXES, key=lambda x: -len(x.split())):
        sw = suf.split()
        out, i = [], 0
        while i < len(words):
            if words[i:i + len(sw)] == sw:
                i += len(sw)
            else:
                out.append(words[i])
                i += 1
        words = out
    return " ".join(words)


def contains_words(hay: str, needle: str) -> bool:
    return re.search(rf"(?:^| ){re.escape(needle)}(?: |$)", hay) is not None


def read_sdd(year: int) -> pd.DataFrame:
    path = EBA / str(year) / "SDD.xlsx"
    raw = pd.read_excel(path, header=None)
    hdr = next(i for i in range(5) if "Item" in raw.iloc[i].astype(str).tolist())
    s = pd.read_excel(path, header=hdr, dtype=str)
    s = s.rename(columns={"DERIVED_TEMPLATE": "Template"})
    s["Item"] = s["Item"].str.replace(r"\.0$", "", regex=True)
    return s


def read_dims(year: int) -> dict[str, pd.DataFrame]:
    """Dimension sheets of TR_Metadata.xlsx as {dimension column name: frame(code, label)}."""
    sheets = pd.read_excel(EBA / str(year) / "TR_Metadata.xlsx", sheet_name=None, header=None, dtype=str)
    out = {}
    for name in ("Exposure", "Perf_status", "Financial_instruments", "Portfolio", "Status", "ASSETS_FV",
                 "ASSETS_Stages"):
        df = sheets[name].dropna(how="all", axis=1).dropna(how="all")
        df = df.iloc[:, -2:]
        df.columns = ["code", "label"]
        df = df[df["code"].str.fullmatch(r"\d+", na=False)]
        col = "Perf_Status" if name == "Perf_status" else name
        out[col] = df.reset_index(drop=True)
    return out


def institutions(year: int) -> pd.DataFrame:
    sheets = pd.read_excel(EBA / str(year) / "TR_Metadata.xlsx", sheet_name=None, header=None, dtype=str)
    name = "List of Institutions" if "List of Institutions" in sheets else "Banks list"
    raw = sheets[name]
    hdr = next(i for i in range(6) if "LEI_Code" in raw.iloc[i].astype(str).tolist())
    df = raw.iloc[hdr + 1:].copy()
    df.columns = raw.iloc[hdr].tolist()
    return df.dropna(subset=["LEI_Code"])


# --- LEIs ------------------------------------------------------------------

def match_leis(universe: pd.DataFrame) -> pd.DataFrame:
    inst = institutions(2025)
    inst = inst[inst["Country"].isin(EU_COUNTRIES)].copy()
    inst["norm"] = inst["Name"].map(norm_name)
    rows = []
    for _, b in universe[universe["country"] != "GB"].iterrows():
        target = norm_name(ALIASES.get(b["bank_id"], b["name"]))
        exact = inst[inst["norm"] == target]
        cont = inst[inst["norm"].map(lambda h, t=target: contains_words(h, t))]
        if len(exact) == 1:
            hit, kind = exact.iloc[0], "exact"
        elif len(exact) == 0 and len(cont) == 1:
            hit, kind = cont.iloc[0], "contained"
        else:
            cands = exact if len(exact) else cont
            rows.append({"bank_id": b["bank_id"], "name": b["name"], "normalised": target, "lei": "",
                         "eba_name": "", "match": "OPEN",
                         "candidates": "; ".join(f"{r.Name} ({r.LEI_Code})" for r in cands.itertuples())})
            continue
        rows.append({"bank_id": b["bank_id"], "name": b["name"], "normalised": target, "lei": hit["LEI_Code"],
                     "eba_name": hit["Name"], "match": kind, "candidates": ""})
    return pd.DataFrame(rows)


# --- maps ------------------------------------------------------------------

def resolve(year: int, sdd: pd.DataFrame, dims: dict, field: str, spec, sdd25: pd.DataFrame):
    """Returns (rows, note): map rows for one field in one release, or [] and the reason."""
    template, label, dimlabels = spec
    in_t = sdd[sdd["Template"] == template]
    hits = in_t[in_t["Label"].map(norm_label) == norm_label(label)]
    note = ""
    if len(hits) == 0 and year != 2025:
        base = sdd25[(sdd25["Template"] == template) & (sdd25["Label"].map(norm_label) == norm_label(label))]
        col = f"Item_TR_{year}"
        if len(base) == 1 and col in base and pd.notna(base.iloc[0][col]):
            item = str(base.iloc[0][col]).replace(".0", "")
            hits = in_t[in_t["Item"] == item]
            note = "crosswalk"
    hits = hits.drop_duplicates("Item")
    if len(hits) != 1:
        return [], f"{len(hits)} items with this label in template {template}"
    dim_codes = {}
    for dim, lab in dimlabels.items():
        d = dims[dim]
        m = d[d["label"].map(norm_label) == norm_label(lab)]
        if len(m) != 1:
            return [], f"{len(m)} codes for {dim} = {lab!r}"
        dim_codes[dim] = m.iloc[0]["code"]
    h = hits.iloc[0]
    return [{"field": field, "item": h["Item"], "template": template, "label": h["Label"],
             "dim_filter": json.dumps(dim_codes, sort_keys=True)}], note


def build_maps() -> tuple[dict[int, pd.DataFrame], pd.DataFrame]:
    sdd25 = read_sdd(2025)
    maps, notes = {}, []
    for y in RELEASES:
        sdd, dims = read_sdd(y), read_dims(y)
        rows = []
        for field, specs in SPEC.items():
            field_rows = []
            for spec in specs if isinstance(specs, list) else [specs]:
                r, note = resolve(y, sdd, dims, field, spec, sdd25)
                if not r:
                    notes.append({"release": y, "field": field, "issue": note})
                    field_rows = []
                    break
                if note == "crosswalk":
                    notes.append({"release": y, "field": field,
                                  "issue": f"label differs: 2025 {spec[1]!r} | {y} {r[0]['label']!r}"})
                field_rows += r
            rows += field_rows
        maps[y] = pd.DataFrame(rows, columns=["field", "item", "template", "label", "dim_filter"])
    return maps, pd.DataFrame(notes)


def write_csv(df: pd.DataFrame, path: Path) -> None:
    buf = io.StringIO()
    df.to_csv(buf, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    path.write_bytes(buf.getvalue().encode("utf-8"))


def main() -> int:
    pd.set_option("display.width", 250)
    pd.set_option("display.max_colwidth", 120)
    upath = ROOT / "data" / "manual" / "universe.csv"
    universe = pd.read_csv(upath, dtype=str, keep_default_na=False)
    m = match_leis(universe)
    print("## LEI matches against the 2025 release\n")
    print(m.to_string(index=False))
    lei = dict(zip(m["bank_id"], m["lei"], strict=True))
    universe["lei"] = [lei.get(b, v) for b, v in zip(universe["bank_id"], universe["lei"], strict=True)]
    write_csv(universe, upath)

    maps, notes = build_maps()
    for y, df in maps.items():
        write_csv(df, ROOT / "config" / f"eba_map_{y}.csv")
        print(f"\n## config/eba_map_{y}.csv ({len(df)} rows)\n")
        print(df.to_string(index=False))
    print("\n## Map notes (label differences and unmapped fields)\n")
    print(notes.to_string(index=False) if len(notes) else "(none)")
    print("\n## Fields of [5.1] not taken from EBA\n")
    print(pd.Series(NOT_EBA).to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
