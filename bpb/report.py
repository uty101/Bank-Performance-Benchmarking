"""Bank profiles (kickoff Section 5.9, instructions 04 B.5 and 05 B.3): 1 A4 page per bank, reportlab with Helvetica;
league tables (instruction 06 B.1).

`root` holds outputs/tables, the only results read; the universe and KPI specs come from the repo. Charts are drawn in memory (amendment 5). `invariant=1` and a PNG with no metadata keep the PDF
byte identical from run to run (rule 9).
"""

from __future__ import annotations

import html
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

from bpb.drivers import DRIVERS, rote_tree
from bpb.ingest import ROOT
from bpb.peers import cluster_year
from bpb.tables import write_csv
from bpb.valuation import UPLIFT_YEAR

GROUP, BASIS = "cluster", "underlying"  # B.5
MARGIN = 36.0
FONT, BOLD = "Helvetica", "Helvetica-Bold"
PNG_DPI = 110  # B.5
TOP_GAPS = 3  # B.5
GRID = colors.Color(0.8, 0.8, 0.8)
BOX_H = 196.0
REFERENCE = "median"  # instruction 05 B.3
RISE, FALL, TOTAL = "#2f6f9f", "#b3261e", "#6f6f6f"
DRIVER_LABELS = {"NII/A": "NII / assets", "F/A": "Fees / assets", "O/A": "Other income / assets", "C/A": "Costs / assets",
                 "LLP/A": "Credit losses / assets", "t": "Tax rate", "A/TE": "Assets / tangible equity"}
BLANK_WORDS = {"missing_input": "a driver input is missing at this date, so no decomposition is shown.",
               "merger_break": "the period holds a material merger, so no decomposition is shown.",
               "too_few_peers": "too few cluster peers have this driver, so no decomposition is shown.",
               "mixed_family": "assets and tangible equity are in different currencies, so no decomposition is shown.",
               "rote_blank": "the bank's RoTE is blank at this date, so the bridge cannot close.",
               "beta_not_significant": "the 90% interval of the pooled beta contains 0, so no uplift is shown.",
               "no_joint_gap": "this bank has no joint RoTE gap at this date, so there is no uplift to show."}
LABELS = {"rote": "RoTE", "roa": "RoA", "ppp_assets": "PPP / assets", "nim": "NIM", "fee_share": "Fee share",
          "cost_income": "Cost to income", "cost_assets": "Cost / assets", "cost_of_risk": "Cost of risk",
          "risk_adj_nim": "Risk adjusted NIM",
          "npl_ratio": "NPL ratio", "npl_coverage": "NPL coverage", "cet1_ratio": "CET1 ratio",
          "leverage_ratio": "Leverage ratio", "lcr": "LCR", "nsfr": "NSFR", "income_fte": "Income / FTE",
          "cost_fte": "Cost / FTE", "cost_customer": "Cost / customer"}
LEAGUE_COLUMNS = ["rank", "bank_id", "name", "value", "verdict", "inside_noise", "status"]
LEAGUE_DATES = 2  # instruction 06 B.1: the 2 latest dates
LEAGUE_GROUPS = ["cluster", "market", "universe"]
LEAGUE_PAGE_GROUPS = ["cluster", "universe"]  # instruction 06 B.1
PAGE_STYLE = ("body{font-family:Helvetica,Arial,sans-serif;margin:24px;color:#222}table{border-collapse:collapse;"
              "margin:0 0 24px}th,td{padding:3px 10px;border-bottom:1px solid #ccc;text-align:left;font-size:14px}"
              "td.n{text-align:right}h2{font-size:17px;margin-bottom:6px}")


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


def ranked_kpis() -> list[dict]:
    with open(ROOT / "config" / "kpis.yaml", encoding="utf-8") as f:
        return [k for k in yaml.safe_load(f)["kpis"] if k["direction"] != "context"]


def _load(root: Path) -> dict:
    tables = root / "outputs" / "tables"
    return {"kpis": ranked_kpis(), "bench": pd.read_csv(tables / "bench.csv"), "kpi": pd.read_csv(tables / "kpi.csv"),
            "peers": pd.read_csv(tables / "peers.csv"), "gaps": pd.read_csv(tables / "gaps.csv"),
            "range": pd.read_csv(tables / "gaps_range.csv"), "drivers": pd.read_csv(tables / "drivers.csv"),
            "fits": pd.read_csv(tables / "valuation_fits.csv"), "valuation": pd.read_csv(tables / "valuation.csv"),
            "universe": pd.read_csv(ROOT / "data" / "manual" / "universe.csv", dtype=str, keep_default_na=False)}


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


def waterfall_steps(t: dict, bank: str, d: str, basis: str = BASIS) -> tuple[list[tuple[str, float]], float, float, str]:
    """(steps, reference RoTE, bank RoTE, status) in points, from the median run (B.3). The reference is every driver and
    OTH/A at the peer median. The steps close on the KPI rote: the Shapley values reach the tree with the bank's OTH/A,
    other_below_line is the move from the reference's OTH/A to the bank's, and minorities_and_at1 takes the tree to the
    KPI."""
    x = t["drivers"]
    x = x[(x["date"] == d) & (x["bank_id"] == bank) & (x["basis"] == basis) & (x["reference"] == REFERENCE)]
    x = x.set_index("driver")
    status = str(x["status"].iloc[0])
    if x["shapley_pts"].isna().all() or "rote_blank" in status:
        return [], np.nan, np.nan, status
    steps = [(DRIVER_LABELS[k], float(x.loc[k, "shapley_pts"])) for k in DRIVERS]
    steps.append(("Other below the line", -float(x["other_below_line_pts"].iloc[0])))
    steps.append(("Minorities and AT1", float(x["minorities_and_at1_pts"].iloc[0])))
    start = rote_tree(x["ref_value"].to_dict()) * 100
    return steps, start, start + sum(v for _, v in steps), status


def waterfall_date(t: dict, bank: str, d: str, basis: str = BASIS) -> str | None:
    """Instruction 06 A.1 item 5: the latest date, up to d, at which the bank has a decomposition."""
    x = t["drivers"]
    x = x[(x["bank_id"] == bank) & (x["basis"] == basis) & (x["reference"] == REFERENCE) & (x["date"] <= d)]
    return next((on for on in sorted(x["date"].unique(), reverse=True) if waterfall_steps(t, bank, on, basis)[0]), None)


def waterfall_chart(steps: list[tuple[str, float]], start: float, end: float, width_pt: float, height_pt: float) -> bytes:
    """Horizontal waterfall from the reference RoTE to the bank's; PNG bytes, nothing saved (amendment 5)."""
    labels = ["Reference RoTE", *[s[0] for s in steps], "Bank RoTE"]
    fig, ax = plt.subplots(figsize=(width_pt / 72, height_pt / 72), dpi=200)
    y = list(range(len(labels)))[::-1]
    level = start
    spans = [(0.0, start, TOTAL)]
    for _, v in steps:
        spans.append((level, level + v, RISE if v >= 0 else FALL))
        level += v
    spans.append((0.0, end, TOTAL))
    far = max(max(a, b) for a, b, _ in spans)
    near = min(0.0, *[min(a, b) for a, b, _ in spans])
    pad = (far - near) * 0.02
    for row, (a, b, colour), label in zip(y, spans, labels, strict=True):
        ax.barh(row, b - a, left=a, height=0.62, color=colour, linewidth=0)
        total = label in (labels[0], labels[-1])
        ax.text(max(a, b) + pad, row, f"{b:.1f}%" if total else f"{b - a:+.1f}", va="center", fontsize=5.5,
                color="#222222", fontweight="bold" if total else "normal")
    ax.set_yticks(y, labels, fontsize=5.5)
    ax.set_xlim(near, far + (far - near) * 0.2)
    ax.set_xticks([])
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.subplots_adjust(left=0.36, right=0.995, top=0.995, bottom=0.005)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def blank_words(status: str) -> str:
    return next((BLANK_WORDS[s] for s in BLANK_WORDS if s in status), f"blank, status {status}.")


def _write_lines(c, lines: list[str], x: float, y: float, width: float, size: float = 8.0) -> None:
    c.setFont(FONT, size)
    for text in lines:
        for line in simpleSplit(text, FONT, size, width):
            c.drawString(x, y, line)
            y -= size + 3


def _waterfall_panel(c, t: dict, bank: str, d: str, on: str | None, x: float, top: float, w: float, h: float) -> None:
    if on is not None:
        steps, start, end, _ = waterfall_steps(t, bank, on)
        png = waterfall_chart(steps, start, end, w - 12, h - 34)
        c.drawImage(ImageReader(io.BytesIO(png)), x + 6, top - h + 6, w - 12, h - 34)
        c.setFont(FONT, 6.5)
        c.drawString(x + 6, top - 25, f"Points of RoTE against the peer median at {on}, Shapley values")
    else:
        status = waterfall_steps(t, bank, d)[3]
        _write_lines(c, [f"Not available at any date. At {d}: {blank_words(status)}"], x + 6, top - 30, w - 12)


def _valuation_panel(c, t: dict, bank: str, x: float, top: float, w: float) -> None:
    fit = t["fits"][t["fits"]["year"] == UPLIFT_YEAR].iloc[0]
    v = t["valuation"]
    r = v[(v["bank_id"] == bank) & (v["date"] == f"{UPLIFT_YEAR}-12-31")]
    lines = [f"Fit at 31 Dec {UPLIFT_YEAR}: beta {fit['beta']:.2f}, n {int(fit['n'])}, R\u00b2 {fit['r2']:.2f}."]
    if r.empty:
        lines.append("Not available: the bank is not listed, so it has no valuation.")
    elif r.iloc[0]["status"] == "ok":
        r = r.iloc[0]
        lines.append(f"Uplift in P/TBV at 31 Dec {UPLIFT_YEAR}: {r['uplift_ptbv']:+.2f}x on a joint RoTE gap of "
                     f"{r['rote_gap_pts']:.2f} points.")
        lines.append(f"90% interval: {r['uplift_lo']:+.2f}x to {r['uplift_hi']:+.2f}x.")
    else:
        lines.append(f"Not available: {blank_words(r.iloc[0]['status'])}")
    _write_lines(c, lines, x + 6, top - 30, w - 12)


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


def profile_date(t: dict, bank: str, d: str) -> str:
    """Instruction 06 B.1: d, or the bank's latest date with a ranked KPI value if it has none at d."""
    k = t["kpi"]
    names = [s["kpi"] for s in t["kpis"]]
    held = k[(k["bank_id"] == bank) & k["kpi"].isin(names) & k["value"].notna() & (k["date"] <= d)]["date"]
    return d if held.empty or held.max() == d else held.max()


def build_profile(bank_id: str, date, root: Path, out: Path) -> Path:
    """1 A4 page for a bank at a date (B.5), written to `out`/{bank_id}_{date}.pdf (amendment 5)."""
    wanted = str(date)
    root = Path(root)
    t = _load(root)
    d = profile_date(t, bank_id, wanted)
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
    if d != wanted:
        y -= 11
        c.drawString(MARGIN, y, f"No KPIs at {wanted}, so this page uses the bank's latest date, {d}.")
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
    box_h = BOX_H
    on = waterfall_date(t, bank_id, d)
    waterfall_title = "Profitability waterfall" if on is None else f"Profitability waterfall at {on}"
    for i, title in enumerate((waterfall_title, "Valuation uplift")):
        x = MARGIN + i * (box_w + 10)
        c.setStrokeColor(GRID)
        c.rect(x, y - box_h, box_w, box_h)
        c.setFont(BOLD, 9)
        c.drawString(x + 6, y - 14, title)
    _waterfall_panel(c, t, bank_id, d, on, MARGIN, y, box_w, box_h)
    _valuation_panel(c, t, bank_id, MARGIN + box_w + 10, y, box_w)
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


def league_table(bench: pd.DataFrame, universe: pd.DataFrame, spec: dict, group: str, d: str) -> pd.DataFrame:
    """Every bank on 1 ranked KPI at a date, best first, with each verdict against the bank's own peers in the group.
    A blank value keeps its row (Convention 4.9), after the ranked banks and with no rank."""
    b = bench[(bench["kpi"] == spec["kpi"]) & (bench["group"] == group) & (bench["date"] == d)
              & (bench["basis"] == BASIS)]
    b = b.merge(universe[["bank_id", "name"]], on="bank_id", how="left", validate="one_to_one")
    b = b.sort_values(["value", "bank_id"], ascending=[spec["direction"] != "higher", True], na_position="last")
    held = int(b["value"].notna().sum())
    b = b.assign(rank=pd.array(list(range(1, held + 1)) + [pd.NA] * (len(b) - held), dtype="Int64"))
    return b[LEAGUE_COLUMNS].reset_index(drop=True)


def _league_html(spec: dict, tables: list[tuple[str, str, pd.DataFrame]]) -> str:
    label = html.escape(LABELS[spec["kpi"]])
    head = (f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>{label} league table</title>"
            f"<style>{PAGE_STYLE}</style></head><body><h1>{label} league table</h1>"
            "<p>Underlying basis, best first. Each verdict is against the bank's own peers in the group, so a cluster "
            "table holds banks from every cluster.</p>")
    parts = [head]
    for group, d, table in tables:
        parts.append(f"<h2>{group.capitalize()} group at {d}</h2><table><tr><th>Rank</th><th>Bank</th><th>Value</th>"
                     "<th>Verdict</th><th>Inside noise</th><th>Status</th></tr>")
        for r in table.itertuples(index=False):
            cells = ["" if pd.isna(r.rank) else str(r.rank), html.escape(r.name), _fmt(r.value, spec["unit"]),
                     "" if pd.isna(r.verdict) else r.verdict, "" if pd.isna(r.inside_noise) else str(r.inside_noise),
                     "" if pd.isna(r.status) else html.escape(str(r.status))]
            parts.append(f"<tr><td class=\"n\">{cells[0]}</td><td>{cells[1]}</td><td class=\"n\">{cells[2]}</td>"
                         + "".join(f"<td>{c}</td>" for c in cells[3:]) + "</tr>")
        parts.append("</table>")
    parts.append("</body></html>\n")
    return "".join(parts)


def league_tables(root: Path) -> None:
    """Instruction 06 B.1: the CSVs of every ranked KPI, group and latest date, and 1 static HTML page per KPI."""
    t = _load(Path(root))
    out = Path(root) / "outputs" / "tables"
    dates = sorted(t["bench"]["date"].unique())[-LEAGUE_DATES:]
    for spec in t["kpis"]:
        pages = []
        for group in LEAGUE_GROUPS:
            for d in dates:
                table = league_table(t["bench"], t["universe"], spec, group, d)
                write_csv(table, out / f"league_{spec['kpi']}_{group}_{d}.csv")
                if group in LEAGUE_PAGE_GROUPS:
                    pages.append((group, d, table))
        (out / f"league_{spec['kpi']}.html").write_bytes(_league_html(spec, pages).encode("utf-8"))


def publish(root: Path, latest: str) -> None:
    """Instruction 06 B.1: a PDF and a PNG for every bank, then the league tables."""
    root = Path(root)
    for bank in pd.read_csv(ROOT / "data" / "manual" / "universe.csv", dtype=str)["bank_id"]:
        pdf = build_profile(bank, latest, root, root / "outputs" / "reports")
        render_png(pdf, root / "outputs" / "figures" / f"{pdf.stem}.png")
    league_tables(root)


def render_png(pdf: Path, png: Path) -> Path:
    """B.5: the page rendered with pymupdf at 110 dpi."""
    import pymupdf

    png.parent.mkdir(parents=True, exist_ok=True)
    with pymupdf.open(pdf) as doc:
        doc[0].get_pixmap(dpi=PNG_DPI).save(png)
    return png
