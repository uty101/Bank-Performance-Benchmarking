"""Lineage IDs (Convention 4.13) and `trace` (instruction 06 B.2).

The build writes 2 tables, so that a trace reads only outputs/tables: lineage.csv holds every source row (a FACTS row, a
one off or a price; 1 row per printed number, so a summed field has several rows under 1 ID), and lineage_derived.csv
holds every derived row with the IDs it was computed from. A sized gap or driver stops at its own bank's inputs: its
target or reference comes from peers, and those are named by the BENCH and DRIVERS rows, not traced.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

SOURCE_COLUMNS = ["lineage_id", "kind", "bank_id", "ref_date", "field", "value", "ccy", "family", "status", "locator",
                  "release_year", "item_code", "url", "sha256", "page", "value_as_printed", "unit_scale", "entry_value",
                  "decimal_mark", "snippet"]
DERIVED_COLUMNS = ["lineage_id", "table", "bank_id", "date", "item", "basis", "detail", "value", "inputs_lineage"]
TRACE_COLUMNS = ["depth", "kind", "lineage_id", "bank_id", "date", "item", "basis", "detail", "value", "family",
                 "locator", "release_year", "item_code", "url", "sha256", "page", "snippet"]
GAP_INPUTS = ["pbt", "tax"]  # the tree rows behind the tax rate of a sized gap
# the tree rows behind each driver, by the amounts in bpb/drivers.py TREE
DRIVER_INPUTS = {"NII/A": ["nii"], "F/A": ["fees"], "O/A": ["other"], "C/A": ["cost"], "LLP/A": ["llp"],
                 "t": ["tax", "pbt"], "A/TE": ["pbt"], "OTH/A": ["income", "cost", "llp", "pbt"]}
PRICE_SOURCE = "yfinance Ticker(t).history, Close, with data/raw/market/splits.csv undone"


def lineage_id(bank_id: str, ref_date: str, field: str, family: str, locator: str) -> str:
    """First 12 hex characters of sha256 of `bank_id|ref_date|field|source_family|locator`."""
    key = f"{bank_id}|{ref_date}|{field}|{family}|{locator}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]


def row_id(table: str, bank_id: str, date: str, item: str, basis: str = "", detail: str = "") -> str:
    """The ID of a derived row: Convention 4.13 with the table as the family and basis and detail as the locator."""
    return lineage_id(bank_id, date, item, f"derived:{table}", f"{basis}|{detail}")


def price_id(bank_id: str, date: str, ticker: str) -> str:
    return lineage_id(bank_id, date, "price", "market", f"{ticker}@{date}")


def _report_rows(fact, entries: pd.DataFrame, urls: dict) -> list[dict]:
    parts = set(fact.locator.split("+"))
    hits = entries[[f"{s}@{p}" in parts for s, p in zip(entries["report_sha256"], entries["page"], strict=True)]]
    return [{"sha256": e.report_sha256, "page": e.page, "url": urls.get(e.report_sha256, ""), "snippet": e.snippet,
             "value_as_printed": e.value_as_printed, "unit_scale": e.unit_scale, "entry_value": e.value,
             "decimal_mark": e.decimal_mark} for e in hits.itertuples(index=False)]


def source_table(facts: pd.DataFrame, one_offs: pd.DataFrame, entries: pd.DataFrame, manifest: pd.DataFrame,
                 valuation: pd.DataFrame, universe: pd.DataFrame) -> pd.DataFrame:
    """outputs/tables/lineage.csv. `entries` is `bpb.ingest.entries_with_marks` output."""
    urls = dict(zip(manifest["sha256"], manifest["url"], strict=True))
    by_key = {k: g for k, g in entries.groupby(["bank_id", "ref_date", "field"], sort=False)}
    rows = []
    for f in facts.itertuples(index=False):
        base = {"lineage_id": f.lineage_id, "kind": "facts", "bank_id": f.bank_id, "ref_date": f.ref_date,
                "field": f.field, "value": f.value, "ccy": f.ccy, "family": f.family, "status": f.status,
                "locator": f.locator}
        if f.family == "eba":
            item, release = f.locator.rsplit("@", 1)
            rows.append({**base, "release_year": release, "item_code": item})
        else:
            rows += [{**base, **r} for r in _report_rows(f, by_key[(f.bank_id, f.ref_date, f.field)], urls)]
    for o in one_offs.itertuples(index=False):
        locator = f"{o.report_sha256}@{o.page}"
        rows.append({"lineage_id": lineage_id(o.bank_id, o.ref_date, o.field, "one_off", locator), "kind": "one_off",
                     "bank_id": o.bank_id, "ref_date": o.ref_date, "field": o.field, "value": o.amount,
                     "family": "one_off", "status": "ok", "locator": locator, "url": urls.get(o.report_sha256, ""),
                     "sha256": o.report_sha256, "page": o.page, "value_as_printed": o.value_as_printed,
                     "unit_scale": o.unit_scale, "entry_value": o.amount, "snippet": o.snippet})
    ticker = dict(zip(universe["bank_id"], universe["ticker"], strict=True))
    for v in valuation.itertuples(index=False):
        rows.append({"lineage_id": price_id(v.bank_id, v.date, ticker[v.bank_id]), "kind": "market", "bank_id": v.bank_id,
                     "ref_date": v.date, "field": "price", "value": v.price, "ccy": v.price_ccy, "family": "market",
                     "status": "ok" if pd.notna(v.price) else "missing_input", "locator": f"{ticker[v.bank_id]}@{v.date}",
                     "url": PRICE_SOURCE})
    return pd.DataFrame(rows, columns=SOURCE_COLUMNS)


def derived_table(kpi: pd.DataFrame, tree: pd.DataFrame, gaps: pd.DataFrame, drivers: pd.DataFrame,
                  valuation: pd.DataFrame, facts: pd.DataFrame, universe: pd.DataFrame) -> pd.DataFrame:
    """outputs/tables/lineage_derived.csv. `tree` is `compute_kpis` output of the tree amounts and closing `te`."""
    def row(table, bank, date, item, basis, detail, value, inputs) -> dict:
        return {"lineage_id": row_id(table, bank, date, item, basis, detail), "table": table, "bank_id": bank,
                "date": date, "item": item, "basis": basis, "detail": detail, "value": value,
                "inputs_lineage": ";".join(dict.fromkeys(i for i in inputs if i))}

    def own(field) -> list[str]:
        return [] if pd.isna(field) else str(field).split(";")

    rows = [row("kpi", r.bank_id, r.date, r.kpi, r.basis, "", r.value, own(r.inputs_lineage))
            for r in kpi.itertuples(index=False)]
    rows += [row("tree", r.bank_id, r.date, r.kpi, r.basis, "", r.value, own(r.inputs_lineage))
             for r in tree.itertuples(index=False)]
    for r in gaps.itertuples(index=False):
        inputs = [row_id("kpi", r.bank_id, r.date, name, r.basis) for name in (r.gap, "rote")]
        inputs += [row_id("tree", r.bank_id, r.date, name, r.basis) for name in GAP_INPUTS]
        rows.append(row("gaps", r.bank_id, r.date, r.gap, r.basis, r.group, r.delta_pi_eur, inputs))
    for r in drivers.itertuples(index=False):
        inputs = [row_id("tree", r.bank_id, r.date, name, r.basis) for name in DRIVER_INPUTS[r.driver]]
        rows.append(row("drivers", r.bank_id, r.date, r.driver, r.basis, r.reference, r.shapley_pts, inputs))
    shares = facts[facts["field"] == "shares_out"]
    shares = dict(zip(zip(shares["bank_id"], shares["ref_date"], strict=True), shares["lineage_id"], strict=True))
    ticker = dict(zip(universe["bank_id"], universe["ticker"], strict=True))
    for r in valuation.itertuples(index=False):
        inputs = [price_id(r.bank_id, r.date, ticker[r.bank_id]), row_id("tree", r.bank_id, r.date, "te", "reported"),
                  shares.get((r.bank_id, r.date), "")]
        rows.append(row("valuation", r.bank_id, r.date, "ptbv", "", "", r.ptbv, inputs))
    return pd.DataFrame(rows, columns=DERIVED_COLUMNS)


@dataclass(frozen=True)
class Lineage:
    """The 2 tables, and their rows by ID, so that tracing many rows reads and indexes them once."""
    sources: pd.DataFrame
    derived: pd.DataFrame
    source_rows: dict
    derived_rows: dict


def read_lineage(root: Path) -> Lineage:
    tables = Path(root) / "outputs" / "tables"
    text = {"page": str, "release_year": str, "item_code": str, "value_as_printed": str, "entry_value": str}
    sources = pd.read_csv(tables / "lineage.csv", dtype=text, keep_default_na=False, na_values=[""])
    derived = pd.read_csv(tables / "lineage_derived.csv", dtype={"inputs_lineage": str})
    by_source: dict = {}
    for s in sources.itertuples(index=False):
        by_source.setdefault(s.lineage_id, []).append(s)
    return Lineage(sources, derived, by_source, {d.lineage_id: d for d in derived.itertuples(index=False)})


def trace(lineage_id: str, root: Path, tables: Lineage | None = None) -> pd.DataFrame:
    """The chain behind a figure, depth first: each derived row, then every source row beneath it, with the EBA release
    year and item code, or the report URL, sha256, page and snippet. `tables` is `read_lineage` output, for a caller
    tracing many rows. An unknown ID gives an empty frame."""
    tables = read_lineage(root) if tables is None else tables
    rows: list[dict] = []
    seen: set[str] = set()

    def walk(node: str, depth: int) -> None:
        if node in seen:
            return
        seen.add(node)
        d = tables.derived_rows.get(node)
        if d is not None:
            rows.append({"depth": depth, "kind": d.table, "lineage_id": node, "bank_id": d.bank_id, "date": d.date,
                         "item": d.item, "basis": d.basis, "detail": d.detail, "value": d.value})
            for child in [] if pd.isna(d.inputs_lineage) else d.inputs_lineage.split(";"):
                walk(child, depth + 1)
        for s in tables.source_rows.get(node, []):
            rows.append({"depth": depth, "kind": s.kind, "lineage_id": node, "bank_id": s.bank_id, "date": s.ref_date,
                         "item": s.field, "value": s.value, "family": s.family, "locator": s.locator,
                         "release_year": s.release_year,
                         "item_code": s.item_code, "url": s.url, "sha256": s.sha256, "page": s.page,
                         "snippet": s.snippet})

    walk(lineage_id, 0)
    return pd.DataFrame(rows, columns=TRACE_COLUMNS)


def trace_text(frame: pd.DataFrame) -> str:
    """A trace as printed by `bpb trace`: 1 block per row, blank fields left out."""
    if frame.empty:
        return "no row has this lineage ID"
    lines = []
    for r in frame.itertuples(index=False):
        head = f"{'  ' * r.depth}{r.kind} {r.lineage_id}  {r.bank_id} {r.date} {r.item}"
        extra = " ".join(str(x) for x in (r.basis, r.detail) if pd.notna(x) and x != "")
        lines.append(f"{head} {extra}  value {r.value}".replace("  value nan", "  value blank"))
        pad = "  " * (r.depth + 1)
        if pd.notna(r.item_code):
            lines.append(f"{pad}EBA release {r.release_year}, item {r.item_code}")
        if pd.notna(r.sha256):
            lines.append(f"{pad}{r.url}")
            lines.append(f"{pad}sha256 {r.sha256}, page {r.page}")
            lines.append(f"{pad}snippet: {r.snippet}")
        elif pd.notna(r.url):
            lines.append(f"{pad}{r.url}")
    return "\n".join(lines)
