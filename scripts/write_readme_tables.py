"""Writes the generated blocks of README.md from the tables of a build (instruction 06 B.4). A block sits between the
marker comments `<!-- table:NAME start -->` and `<!-- table:NAME end -->`, and holds every result number of the README.

usage: python scripts/write_readme_tables.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bpb import answers as a
from bpb.report import BASIS, LABELS

README = ROOT / "README.md"
BLOCK = re.compile(r"(<!-- table:(\w+) start -->\n)(.*?)(<!-- table:\2 end -->)", re.DOTALL)
BIG = 1e6  # EUR m
Q5_MIN_BANKS = 15  # instruction 06c B.2 item 5: the README went over 15 KB, so Q5 lists only fields this many banks report


def _table(header: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    return "\n".join(lines + ["| " + " | ".join(r) + " |" for r in rows])


def _eur(x: float) -> str:
    return f"{x / BIG:,.0f}"


def _text(x) -> str:
    return "" if pd.isna(x) else str(x)


def _significant(t: dict) -> pd.DataFrame:
    """The fit years with a significant beta: the implied cost of equity is blank where the 90% interval holds 0."""
    f = t["valuation_fits"]
    return f[f["coe_implied"].notna()].reset_index(drop=True)


def _headline(t: dict) -> str:
    """Instruction 06e B.1: the result in bold, then what a RoTE point is worth to the market."""
    sig = _significant(t)
    first, last = sig.iloc[0], sig.iloc[-1]
    return (f"**{a.headline_claim(t)}** Each RoTE point was worth {last['beta'] / 100:.3f}x of price to tangible book at "
            f"the end of {int(last['year'])}, against {first['beta'] / 100:.3f}x at the end of {int(first['year'])}, so "
            f"the market now pays about {last['beta'] / first['beta']:.1f} times as much for the same gap. Banks whose "
            "accounting scope differs between the 2 sources, mainly bank insurers, are left out of the headline (see "
            "Caveats).")


def _q1(t: dict) -> str:
    rote, ci = a.overall(t, "rote"), a.overall(t, "cost_income")
    verdicts = rote["verdict"].value_counts()
    text = (f"{rote.iloc[0]['name']} leads on RoTE at {rote.iloc[0]['value'] * 100:.2f}% and {ci.iloc[0]['name']} on cost to "
            f"income at {ci.iloc[0]['value'] * 100:.2f}%. On RoTE, {verdicts.get('leading', 0)} banks are leading their "
            f"peers and {verdicts.get('lagging', 0)} are lagging. The table below ranks {len(rote)} banks on RoTE and "
            f"{len(ci)} on cost to income, the rest being blank at this date. Each verdict is against the bank's own "
            "cluster, named beside it, so the ranks and verdicts need not agree.")
    rows = []
    for i in range(max(len(rote), len(ci))):
        r = rote.iloc[i] if i < len(rote) else None
        c = ci.iloc[i] if i < len(ci) else None
        rows.append([str(i + 1),
                     *([""] * 4 if r is None else [r["name"], str(r["cluster"]), f"{r['value'] * 100:.2f}%",
                                                   _text(r["verdict"])]),
                     *([""] * 4 if c is None else [c["name"], str(c["cluster"]), f"{c['value'] * 100:.2f}%",
                                                   _text(c["verdict"])])])
    return text + "\n\n" + _table(["Rank", "RoTE: bank", "Cluster", "RoTE", "Verdict", "Cost to income: bank", "Cluster",
                                   "Cost to income", "Verdict"], rows)


def _q2(t: dict) -> str:
    g = a.largest_gaps(t)
    top = g.iloc[0]
    text = (f"{g['bank_id'].nunique()} banks have the largest joint gaps, led by {top['bank_id']} at EUR "
            f"{_eur(top['joint_eur'])}m. Min and max run over the 3 peer groups and 2 bases, and the joint figure closes "
            "every sized gap at once, so it can be less than the sum of the bank's rows. Amounts are EUR m of annual pre "
            "tax profit. NIM and cost of risk are sized together as a risk adjusted margin, because a high cost of risk "
            "is the price of a high margin.")
    scope = set(a.scope_banks(t))
    return text + "\n\n" + _table(["Bank", "Gap", "Headline", "Min", "Max", "Joint", "Joint RoTE pts", "Scope"], [
        [r.bank_id, LABELS[r.gap], _eur(r.headline_eur), _eur(r.min_eur), _eur(r.max_eur), _eur(r.joint_eur),
         "" if pd.isna(r.joint_rote_pts) else f"{r.joint_rote_pts:.2f}", "yes" if r.bank_id in scope else ""]
        for r in g.itertuples(index=False)])


def _q3(t: dict) -> str:
    d = a.driver_table(t)
    steps = [c for c in d.columns if c not in ("bank_id", "gap", "reference", "bank")]
    first = d.iloc[0]
    big = first[steps].astype(float).abs().idxmax()
    text = (f"Of the banks with a decomposition at {t['latest']}, {first['bank_id']} sits furthest from its peer median, "
            f"{first['gap']:+.2f} points, and its largest step is {big.lower()} at {first[big]:+.2f} points. Each row runs "
            "from the reference RoTE, every driver at the peer median, to the bank's RoTE, in points.")
    header = ["Bank", "Gap to median", "Reference", *steps, "Bank RoTE"]
    rows = [[r["bank_id"], f"{r['gap']:+.2f}", f"{r['reference']:.2f}", *[f"{r[s]:+.2f}" for s in steps], f"{r['bank']:.2f}"]
            for _, r in d.iterrows()]
    return text + "\n\n" + _table(header, rows)


def _q4(t: dict) -> str:
    f = t["valuation_fits"]
    s = t["valuation_stability"].iloc[0]
    v = t["valuation"]
    v = v[v["uplift_ptbv"].notna()]
    lloy = v[v["bank_id"] == "LLOY"].iloc[0]
    last = f.iloc[-1]
    sig = _significant(t)
    s0, s1 = sig.iloc[0], sig.iloc[-1]
    blank = f[f["coe_implied"].isna()]["year"].tolist()
    text = (f"β rose from {s0['beta']:.2f} in {int(s0['year'])} to {s1['beta']:.2f} in {int(s1['year'])}, the first and "
            f"last years with a significant β, and the implied cost of equity went from {s0['coe_implied'] * 100:.2f}% to "
            f"{s1['coe_implied'] * 100:.2f}%. "
            f"The cost of equity is blank in {', '.join(str(y) for y in blank)}, where the 90% interval of β contains 0. "
            f"The test that the year slopes are equal is rejected: F({int(s['df_num'])}, {int(s['df_denom'])}) = "
            f"{s['f_stat']:.2f}, p = {s['p_value']:.5f}, over {int(s['n'])} bank years. So 1 pooled slope is the wrong model "
            f"for anything but the significance gate, and the choice of slope matters: LLOY's uplift at the end of "
            f"{int(last['year'])} is {lloy['uplift_ptbv']:+.2f}x on that year's β and {lloy['uplift_pooled_ptbv']:+.2f}x on "
            f"the pooled β. The figure below shows {int(last['year'])}, the tightest fit.")
    rows = [[str(int(r.year)), f"{r.beta:.2f}", f"{r.r2:.2f}", str(int(r.n)),
             "blank" if pd.isna(r.coe_implied) else f"{r.coe_implied * 100:.2f}%"] for r in f.itertuples(index=False)]
    figure = f"![P/TBV against RoTE](outputs/figures/valuation_{int(last['year'])}.png)"
    return text + "\n\n" + _table(["Year", "β", "R²", "n", "Implied CoE"], rows) + "\n\n" + figure


def _q5(t: dict) -> str:
    s = a.seam_summary(t)
    x = s.set_index("field")
    shown = s[s["banks"] >= Q5_MIN_BANKS]
    text = (f"Fields the 2 sources define alike agree closely: the median absolute difference is "
            f"{x.loc['loans_all', 'median'] * 100:.2f}% for loans and {x.loc['pat', 'median'] * 100:.2f}% for profit after "
            f"tax. Total assets differ by a median of {x.loc[a.TOTAL_ASSETS, 'median'] * 100:.2f}%, because the supervisory "
            "scope leaves out entities such as insurers. Small residual lines differ the most, since each source draws "
            "them differently. The table covers 2025-06-30, the date both sources report, and lists the "
            f"{len(shown)} fields that at least {Q5_MIN_BANKS} banks report, leaving out {len(s) - len(shown)}.")
    table = _table(["Field", "Banks", "Median", "90th percentile"], [
        [r.field, str(r.banks), f"{r.median * 100:.2f}%", f"{r.p90 * 100:.2f}%"] for r in shown.itertuples(index=False)])
    note = (f"**Bank insurer scope.** {', '.join(a.scope_banks(t))} carry a scope difference between the 2 sources, as bank "
            f"insurers or with a total assets seam above {a.SCOPE_LIMIT * 100:.0f}%. For ISP and KBC, the income statement "
            "lines were read line by line and every one sits in the right field, so the size of other below the line is the "
            f"insurance effect: {a.below_line(t, 'ISP'):+.2f} points of RoTE for ISP and {a.below_line(t, 'KBC'):+.2f} for KBC "
            f"at {t['latest']}. The same treatment flatters their cost to income.")
    return text + "\n\n" + table + "\n\n" + note


def _peers(t: dict) -> str:
    p = t["peers"]
    p = p[p["year"] == p["year"].max()]
    sizes = p.groupby("cluster")["bank_id"].apply(sorted)
    small, broad = sizes[sizes.map(len).idxmin()], sizes[sizes.map(len).idxmax()]
    stab = p.groupby("cluster")["stability"].mean()
    return (f"The clustering splits the {len(p)} banks into {len(small)} and {len(broad)}. The {len(small)} are "
            f"{', '.join(small)}: global banks, far larger than the rest, with a much higher share of trading assets and a "
            "lower share of loans. Everyone else, from Lloyds to Unicaja, is 1 broad group of retail and commercial banks, "
            "so the cluster says more about what the global banks are than about how the others differ. That is why every "
            f"sized gap is shown with its range across the 3 groups. The silhouette is {p['silhouette'].iloc[0]:.2f}, and "
            f"mean stability is {stab[sizes.map(len).idxmin()]:.2f} for the {len(small)} bank cluster and "
            f"{stab[sizes.map(len).idxmax()]:.2f} for the other.")


def _coverage(t: dict) -> str:
    blank, cells, why = a.blank_cells(t)
    named = ", ".join(f"{name} ({n})" for name, n in why.head(3).items())
    return (f"- **Coverage.** {blank} of {cells} KPI cells are blank at {t['latest']} on the {BASIS} basis, because an input "
            f"is not published or not comparable. The largest causes are {named}.")


def _headcount(t: dict, root: Path) -> str:
    source = pd.read_csv(Path(root) / "outputs" / "tables" / "lineage.csv", usecols=["bank_id", "field", "status", "ref_date"])
    hit = source[(source["field"] == "fte") & (source["ref_date"] == t["latest"])
                 & source["status"].astype(str).str.contains("headcount")]
    return f"- **Headcount.** {hit['bank_id'].nunique()} banks publish only headcount, which stands in for FTE."


def blocks(root: Path) -> dict[str, str]:
    t = a.load(root)
    return {"headline": _headline(t), "q1": _q1(t), "q2": _q2(t), "q3": _q3(t), "q4": _q4(t), "q5": _q5(t),
            "peers": _peers(t), "coverage": _coverage(t), "headcount": _headcount(t, root)}


def read_blocks(text: str) -> dict[str, str]:
    return {m.group(2): m.group(3).strip() for m in BLOCK.finditer(text)}


def fill(text: str, new: dict[str, str]) -> str:
    return BLOCK.sub(lambda m: f"{m.group(1)}{new[m.group(2)]}\n{m.group(4)}", text)


def main() -> int:
    README.write_bytes(fill(README.read_bytes().decode("utf-8"), blocks(ROOT)).encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
