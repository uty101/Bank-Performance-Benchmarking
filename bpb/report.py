"""Bank profiles, first version (kickoff Section 5.9, instruction 04 B.5): 1 A4 page per bank, reportlab with Helvetica.

Reads only outputs/tables. Charts are drawn in memory (amendment 5). `invariant=1` and a PNG with no metadata keep the PDF
byte identical from run to run (rule 9).
"""

from __future__ import annotations

import io
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

from bpb.peers import cluster_year

GROUP, BASIS = "cluster", "underlying"  # B.5
MARGIN = 36.0
FONT, BOLD = "Helvetica", "Helvetica-Bold"
PLACEHOLDER = "Section 5"  # B.5
PNG_DPI = 110  # B.5
TOP_GAPS = 3  # B.5
GRID = colors.Color(0.8, 0.8, 0.8)
LABELS = {"rote": "RoTE", "roa": "RoA", "ppp_assets": "PPP / assets", "nim": "NIM", "fee_share": "Fee share",
          "cost_income": "Cost to income", "cost_assets": "Cost / assets", "cost_of_risk": "Cost of risk",
          "npl_ratio": "NPL ratio", "npl_coverage": "NPL coverage", "cet1_ratio": "CET1 ratio",
          "leverage_ratio": "Leverage ratio", "lcr": "LCR", "nsfr": "NSFR", "income_fte": "Income / FTE",
          "cost_fte": "Cost / FTE", "cost_customer": "Cost / customer"}


def _fmt(value: float, unit: str) -> str:
    """Convention 4.7: % to 2 decimals, bps to 1 decimal."""
    if pd.isna(value):
        return ""
    if unit == "pct":
        return f"{value * 100:.2f}%"
    if unit == "bps":
        return f"{value * 1e4:.1f} bps"
    if unit == "eur_k":
        return f"{value / 1e3:,.1f}k"
    return f"{value:,.0f}"


def _load(root: Path) -> dict:
    tables = root / "outputs" / "tables"
    with open(root / "config" / "kpis.yaml", encoding="utf-8") as f:
        kpis = [k for k in yaml.safe_load(f)["kpis"] if k["direction"] != "context"]
    return {"kpis": kpis, "bench": pd.read_csv(tables / "bench.csv"), "kpi": pd.read_csv(tables / "kpi.csv"),
            "peers": pd.read_csv(tables / "peers.csv"), "gaps": pd.read_csv(tables / "gaps.csv"),
            "range": pd.read_csv(tables / "gaps_range.csv"),
            "universe": pd.read_csv(root / "data" / "manual" / "universe.csv", dtype=str, keep_default_na=False)}


def _quartile_position(x: np.ndarray, peers: np.ndarray, sign: float) -> np.ndarray:
    """Peer min, quartiles and max mapped to 0, 0.25, 0.5, 0.75 and 1, with better to the right."""
    q = np.unique(np.quantile(sign * peers, [0, 0.25, 0.5, 0.75, 1]))
    return np.interp(sign * x, q, np.linspace(0, 1, len(q)))


def strip_chart(t: dict, bank: str, d: str, width_pt: float, height_pt: float) -> bytes:
    """Each ranked KPI on its own row, the bank marked among its cluster peers; PNG bytes, nothing saved."""
    p = t["peers"]
    p = p[(p["year"] == cluster_year(d)) & p["cluster"].notna()].set_index("bank_id")["cluster"]
    k = t["kpi"]
    k = k[(k["date"] == d) & (k["basis"] == BASIS)]
    same = p[p == p[bank]].index
    fig, ax = plt.subplots(figsize=(width_pt / 72, height_pt / 72), dpi=200)
    n = len(t["kpis"])
    for i, spec in enumerate(t["kpis"]):
        row = k[k["kpi"] == spec["kpi"]].set_index("bank_id")["value"]
        peers = row[row.index.isin(same) & (row.index != bank)].dropna().to_numpy()
        y = n - 1 - i
        ax.axhline(y, color="#dddddd", lw=0.5, zorder=1)
        if len(peers) < 2:
            continue
        sign = 1.0 if spec["direction"] == "higher" else -1.0
        ax.scatter(_quartile_position(peers, peers, sign), np.full(len(peers), y), s=5, color="#8a8a8a", zorder=2,
                   linewidths=0)
        if pd.notna(row.get(bank, np.nan)):
            ax.scatter(_quartile_position(np.array([row[bank]]), peers, sign), [y], s=26, marker="D", color="#b3261e",
                       zorder=3, linewidths=0)
    for x in (0.25, 0.5, 0.75):
        ax.axvline(x, color="#555555" if x == 0.5 else "#aaaaaa", lw=0.6, zorder=1)
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.6, n - 0.4)
    ax.set_yticks([])
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1], ["worst", "Q1", "median", "Q3", "best"], fontsize=6)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.subplots_adjust(left=0.01, right=0.99, top=1.0, bottom=0.07)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def _table(data, widths, row_height, font_size, align_from=1) -> Table:
    tbl = Table(data, colWidths=widths, rowHeights=row_height)
    tbl.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), FONT, font_size), ("FONT", (0, 0), (-1, 0), BOLD, font_size),
                             ("ALIGN", (align_from, 0), (-1, -1), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                             ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
                             ("LINEBELOW", (0, 1), (-1, -1), 0.25, GRID),
                             ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                             ("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (-1, -1), 2)]))
    return tbl


def _statuses(t: dict, rows: pd.DataFrame, bank: str, d: str, peer_row: pd.Series) -> list[str]:
    g = t["gaps"]
    g = g[(g["bank_id"] == bank) & (g["date"] == d) & (g["group"] == GROUP) & (g["basis"] == BASIS)]
    found = set()
    for s in list(rows["status"].dropna()) + list(g["tax_status"].dropna()) + [peer_row["status"]]:
        found.update(x.split(":")[0] for x in str(s).split(";"))
    return sorted(found - {"ok", "", "not_sized"})


def build_profile(bank_id: str, date, root: Path, out: Path) -> Path:
    """1 A4 page for a bank at a date (B.5), written to `out`/{bank_id}_{date}.pdf (amendment 5)."""
    d = str(date)
    root = Path(root)
    t = _load(root)
    u = t["universe"].set_index("bank_id").loc[bank_id]
    peer_row = t["peers"][(t["peers"]["year"] == cluster_year(d)) & (t["peers"]["bank_id"] == bank_id)].iloc[0]
    b = t["bench"]
    rows = b[(b["bank_id"] == bank_id) & (b["date"] == d) & (b["group"] == GROUP) & (b["basis"] == BASIS)]
    rows = rows.set_index("kpi")
    path = Path(out) / f"{bank_id}_{d}.pdf"
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=A4, invariant=1, pageCompression=1)
    c.setTitle(f"{u['name']} profile {d}")
    w, h = A4
    y = h - MARGIN - 14
    c.setFont(BOLD, 16)
    c.drawString(MARGIN, y, u["name"])
    y -= 14
    c.setFont(FONT, 9)
    stab = "stability not computed" if pd.isna(peer_row["stability"]) else f"stability {peer_row['stability']:.2f}"
    c.drawString(MARGIN, y, f"Market {u['market']}  |  cluster {int(peer_row['cluster'])} of {int(peer_row['k'])}  |  "
                            f"{stab}  |  as at {d}  |  cluster group, underlying basis")
    y -= 10
    table_w = 312.0
    data = [["KPI", "Value", "Peer median", "Target", "Pctl", "Verdict"]]
    for spec in t["kpis"]:
        r = rows.loc[spec["kpi"]]
        pct = "" if pd.isna(r["pct_rank"]) else f"{r['pct_rank'] * 100:.0f}"
        data.append([LABELS[spec["kpi"]], _fmt(r["value"], spec["unit"]), _fmt(r["median"], spec["unit"]),
                     _fmt(r["target"], spec["unit"]), pct, "" if pd.isna(r["verdict"]) else r["verdict"]])
    row_h = 14.0
    tbl = _table(data, [84, 58, 58, 58, 22, 32 + 0], row_h, 7.5)
    _, th = tbl.wrapOn(c, table_w, 400)
    y -= th
    tbl.drawOn(c, MARGIN, y)
    chart_w = w - 2 * MARGIN - table_w - 10
    png = strip_chart(t, bank_id, d, chart_w, th - row_h + 12)
    c.drawImage(ImageReader(io.BytesIO(png)), MARGIN + table_w + 10, y - 12, chart_w, th - row_h + 12)
    c.setFont(BOLD, 7.5)
    c.drawString(MARGIN + table_w + 10, y + th - 9, "Position among cluster peers (bank in red)")
    y -= 26
    c.setFont(BOLD, 10)
    c.drawString(MARGIN, y, "Top sized gaps (EUR m, annual profit)")
    y -= 6
    g = t["range"]
    g = g[(g["bank_id"] == bank_id) & (g["date"] == d) & g["headline_eur"].notna()]
    g = g.sort_values(["headline_eur", "gap"], ascending=[False, True]).head(TOP_GAPS)
    if g.empty:
        y -= 12
        c.setFont(FONT, 8)
        c.drawString(MARGIN, y, "No gap is sized in the cluster group on the underlying basis.")
    else:
        data = [["Gap", "Headline", "Min", "Max", "Cells sized"]]
        data += [[LABELS[r.gap], f"{r.headline_eur / 1e6:,.0f}", f"{r.min_eur / 1e6:,.0f}", f"{r.max_eur / 1e6:,.0f}",
                  str(r.n_sized)] for r in g.itertuples(index=False)]
        tbl = _table(data, [150, 70, 70, 70, 60], 14.0, 8)
        _, gh = tbl.wrapOn(c, w, 200)
        y -= gh
        tbl.drawOn(c, MARGIN, y)
    y -= 22
    box_w = (w - 2 * MARGIN - 10) / 2
    box_h = 92.0
    for i, title in enumerate(("Profitability waterfall", "Valuation uplift")):
        x = MARGIN + i * (box_w + 10)
        c.setStrokeColor(GRID)
        c.rect(x, y - box_h, box_w, box_h)
        c.setFont(BOLD, 9)
        c.drawString(x + 6, y - 14, title)
        c.setFont(FONT, 9)
        c.drawCentredString(x + box_w / 2, y - box_h / 2 - 4, PLACEHOLDER)
    y -= box_h + 16
    notes = _statuses(t, rows, bank_id, d, peer_row)
    text = "Statuses that apply: " + (", ".join(notes) if notes else "none") + "."
    c.setFont(FONT, 7)
    for line in simpleSplit(text, FONT, 7, w - 2 * MARGIN):
        c.drawString(MARGIN, y, line)
        y -= 9
    c.showPage()
    c.save()
    return path


def render_png(pdf: Path, png: Path) -> Path:
    """B.5: the page rendered with pymupdf at 110 dpi."""
    import pymupdf

    png.parent.mkdir(parents=True, exist_ok=True)
    with pymupdf.open(pdf) as doc:
        doc[0].get_pixmap(dpi=PNG_DPI).save(png)
    return png
