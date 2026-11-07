"""Streamlit dashboard (instruction 06 B.2): `streamlit run bpb/dashboard.py`. It reads only outputs/.

It reads outputs/ under the folder in BPB_ROOT, or under the current directory if that is not set (instruction 06c
B.4), which is how the test runs it on a build in tmp_path.
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st

from bpb.lineage import Lineage, read_lineage, row_id, trace, trace_text
from bpb.report import (
    BASIS,
    DRIVER_LABELS,
    GROUP,
    LABELS,
    REFERENCE,
    _fmt,
    blank_words,
    waterfall_chart,
    waterfall_date,
    waterfall_steps,
)

ROOT = Path(os.environ.get("BPB_ROOT", "."))
GROUPS = [GROUP, "market", "universe"]
BASES = [BASIS, "reported"]
TREND_YEARS = 5  # instruction 06 B.2
CHART_SIZE = (640.0, 300.0)  # points


@st.cache_resource
def tables() -> dict:
    """Every table from outputs/tables. The bank names come from a league table and the units from kpi.csv."""
    out = ROOT / "outputs" / "tables"
    t = {name: pd.read_csv(out / f"{name}.csv") for name in ("bench", "kpi", "gaps", "drivers", "valuation")}
    t["range"] = pd.read_csv(out / "gaps_range.csv")
    latest = t["bench"]["date"].max()
    t["names"] = pd.read_csv(out / f"league_rote_universe_{latest}.csv").sort_values("bank_id")
    units = t["kpi"].drop_duplicates("kpi").set_index("kpi")["unit"]
    t["kpis"] = [{"kpi": k, "unit": units[k]} for k in LABELS]
    return t


@st.cache_resource
def lineage() -> Lineage:
    return read_lineage(ROOT)


def show_trace(label: str, node: str) -> None:
    with st.expander(f"Trace: {label}"):
        st.code(f"bpb trace {node}\n\n{trace_text(trace(node, ROOT, lineage()))}", language=None)


def kpi_section(t: dict, bank: str, group: str, basis: str, d: str) -> None:
    st.subheader("KPIs")
    b = t["bench"]
    rows = b[(b["bank_id"] == bank) & (b["date"] == d) & (b["group"] == group) & (b["basis"] == basis)].set_index("kpi")
    shown = []
    for s in t["kpis"]:
        r = rows.loc[s["kpi"]]
        shown.append({"KPI": LABELS[s["kpi"]], "Value": _fmt(r["value"], s["unit"]),
                      "Peer median": _fmt(r["median"], s["unit"]), "Target": _fmt(r["target"], s["unit"]),
                      "Percentile": "" if pd.isna(r["pct_rank"]) else f"{r['pct_rank'] * 100:.0f}",
                      "Verdict": "" if pd.isna(r["verdict"]) else r["verdict"]})
    st.dataframe(pd.DataFrame(shown), hide_index=True, width="stretch")
    for s in t["kpis"]:
        show_trace(LABELS[s["kpi"]], row_id("kpi", bank, d, s["kpi"], basis))


def trend_section(t: dict, bank: str, basis: str, d: str) -> None:
    st.subheader(f"{TREND_YEARS} year trends")
    k = t["kpi"]
    first = f"{int(d[:4]) - TREND_YEARS}{d[4:]}"
    k = k[(k["bank_id"] == bank) & (k["basis"] == basis) & (k["date"] > first) & (k["date"] <= d)]
    columns = st.columns(2)
    for i, s in enumerate(t["kpis"]):
        with columns[i % 2]:
            series = k[k["kpi"] == s["kpi"]].set_index("date")["value"].sort_index()
            st.caption(LABELS[s["kpi"]])
            if series.notna().any():
                st.line_chart(series, height=180)
            else:
                st.write("No values in this window.")
            with st.expander(f"Trace: {LABELS[s['kpi']]} by date"):
                on = st.selectbox("Date", list(series.index[::-1]), key=f"trend_{s['kpi']}")
                node = row_id("kpi", bank, on, s["kpi"], basis)
                st.code(f"bpb trace {node}\n\n{trace_text(trace(node, ROOT, lineage()))}", language=None)


def gaps_section(t: dict, bank: str, group: str, basis: str, d: str) -> None:
    st.subheader("Sized gaps (EUR m, annual profit)")
    g = t["gaps"]
    g = g[(g["bank_id"] == bank) & (g["date"] == d) & (g["group"] == group) & (g["basis"] == basis)
          & g["delta_pi_eur"].notna()]
    if g.empty:
        st.write("No gap is sized for this bank, group and basis.")
        return
    r = t["range"]
    r = r[(r["bank_id"] == bank) & (r["date"] == d)].set_index("gap")
    st.dataframe(pd.DataFrame([{"Gap": LABELS[x.gap], "Value": f"{x.delta_pi_eur / 1e6:,.0f}",
                                "Min": f"{r.loc[x.gap, 'min_eur'] / 1e6:,.0f}", "Max": f"{r.loc[x.gap, 'max_eur'] / 1e6:,.0f}",
                                "RoTE points": f"{x.delta_rote_pts:.2f}"} for x in g.itertuples(index=False)]),
                 hide_index=True, width="stretch")
    for x in g.itertuples(index=False):
        show_trace(LABELS[x.gap], row_id("gaps", bank, d, x.gap, basis, group))


def waterfall_section(t: dict, bank: str, basis: str, d: str) -> None:
    on = waterfall_date(t, bank, d, basis)
    st.subheader("Shapley waterfall" if on is None else f"Shapley waterfall at {on}")
    st.caption("Always against the cluster peers.")
    if on is None:
        st.write(f"Not available at any date. At {d}: {blank_words(waterfall_steps(t, bank, d, basis)[3])}")
        return
    steps, start, end, _ = waterfall_steps(t, bank, on, basis)
    st.image(waterfall_chart(steps, start, end, *CHART_SIZE))
    for key, label in DRIVER_LABELS.items():
        show_trace(label, row_id("drivers", bank, on, key, basis, REFERENCE))


def valuation_section(t: dict, bank: str) -> None:
    st.subheader("Valuation")
    v = t["valuation"]
    v = v[v["bank_id"] == bank]
    if v.empty:
        st.write("The bank is not listed, so it has no valuation.")
        return
    shown = v.rename(columns={"date": "Date", "price": "Price", "price_ccy": "Currency", "tbvps": "TBV per share",
                              "ptbv": "P/TBV", "uplift_ptbv": "Uplift (year fit)", "uplift_lo": "Low", "uplift_hi": "High",
                              "uplift_pooled_ptbv": "Uplift (pooled)"})
    st.dataframe(shown[["Date", "Price", "Currency", "TBV per share", "P/TBV", "Uplift (year fit)", "Low", "High",
                        "Uplift (pooled)"]], hide_index=True, width="stretch")
    for on in v["date"]:
        show_trace(f"P/TBV at {on}", row_id("valuation", bank, on, "ptbv"))


def main() -> None:
    st.set_page_config(page_title="Bank benchmarking", layout="wide")
    st.title("Bank Performance Benchmarking")
    t = tables()
    names = dict(zip(t["names"]["bank_id"], t["names"]["name"], strict=True))
    left, group_box, basis_box, date_box = st.columns(4)
    bank = left.selectbox("Bank", list(names), format_func=names.get)
    group = group_box.selectbox("Group", GROUPS)
    basis = basis_box.selectbox("Basis", BASES)
    d = date_box.selectbox("Date", sorted(t["bench"]["date"].unique(), reverse=True))
    kpi_section(t, bank, group, basis, d)
    trend_section(t, bank, basis, d)
    gaps_section(t, bank, group, basis, d)
    waterfall_section(t, bank, basis, d)
    valuation_section(t, bank)


main()
