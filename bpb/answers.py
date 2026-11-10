"""The results behind the README and outputs/tables/answers.csv (instruction 06 B.4). Everything is read from the tables
of a build, so each claim and README table is generated, never typed.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from bpb.ingest import ROOT, read_universe
from bpb.report import BASIS, GROUP, REFERENCE, waterfall_steps

ANSWERS_COLUMNS = ["question", "claim", "source"]
TOP_JOINT = 10  # instruction 06 B.4: the 10 largest by joint
TOP_DRIVERS = 5  # instruction 06 B.4: the 5 banks with the largest RoTE gaps to the median
P90 = 0.9  # instruction 06 B.4
SCOPE_LIMIT = 0.05  # amendment 26: any bank with a total_assets seam above 5%
INSURERS = ["NDA", "DANSKE", "SWED", "SEB", "SHB", "KBC", "BNP", "GLE", "CAG"]  # amendment 26
TOTAL_ASSETS, SEAM = "total_assets", "8_seam_pl"
LOWER_BETTER = {"cost_income"}  # direction of the 2 KPIs ranked in Q1


def load(root: Path) -> dict:
    out = Path(root) / "outputs" / "tables"
    names = ("bench", "kpi", "gaps_joint", "gaps_range", "drivers", "peers", "checks", "valuation", "valuation_fits",
             "valuation_stability")
    t = {name: pd.read_csv(out / f"{name}.csv") for name in names}
    t["latest"] = t["kpi"]["date"].max()
    t["league"] = {k: pd.read_csv(out / f"league_{k}_{GROUP}_{t['latest']}.csv") for k in ("rote", "cost_income")}
    return t


def overall(t: dict, kpi: str) -> pd.DataFrame:
    """Instruction 06c B.3 item 3: every bank of a cluster league file with a value, ranked over all banks, best first."""
    lg = t["league"][kpi]
    lg = lg[lg["value"].notna()]
    return lg.sort_values(["value", "bank_id"], ascending=[kpi in LOWER_BETTER, True]).reset_index(drop=True)


def headline_gap(t: dict) -> pd.Series:
    """Instruction 06c B.2 item 1: the largest joint RoTE gap in points among banks outside the scope list."""
    j = t["gaps_joint"]
    j = j[(j["date"] == t["latest"]) & (j["group"] == GROUP) & (j["basis"] == BASIS) & j["joint_rote_pts"].notna()
          & ~j["bank_id"].isin(scope_banks(t))]
    return j.sort_values(["joint_rote_pts", "bank_id"], ascending=[False, True]).iloc[0]


def prose_date(d: str) -> str:
    """Instruction 06e B.1: a date in the headline reads "30 June 2026"; tables keep ISO dates."""
    ts = pd.Timestamp(d)
    return f"{ts.day} {ts:%B %Y}"


def headline_claim(t: dict) -> str:
    """Instruction 06e B.1: the README's bold result, named by the universe's `name` column, never the ticker."""
    h = headline_gap(t)
    name = read_universe(ROOT).set_index("bank_id").loc[h["bank_id"], "name"]
    return (f"At {prose_date(t['latest'])}, {name} has the largest gap to the best quartile of its peers: "
            f"{h['joint_rote_pts']:.2f} RoTE points, or EUR {h['joint_eur'] / 1e6:,.0f}m of annual pre tax profit.")


def largest_gaps(t: dict) -> pd.DataFrame:
    """Every gap outside noise of the banks with the 10 largest joint gaps: a gap is sized only outside noise."""
    j = t["gaps_joint"]
    j = j[(j["date"] == t["latest"]) & (j["group"] == GROUP) & (j["basis"] == BASIS) & j["joint_eur"].notna()]
    top = j.sort_values(["joint_eur", "bank_id"], ascending=[False, True]).head(TOP_JOINT)
    g = t["gaps_range"]
    g = g[(g["date"] == t["latest"]) & g["headline_eur"].notna() & g["bank_id"].isin(top["bank_id"])]
    out = g.merge(top[["bank_id", "joint_eur", "joint_rote_pts"]], on="bank_id")
    return out.sort_values(["joint_eur", "bank_id", "headline_eur"], ascending=[False, True, False]).reset_index(drop=True)


def driver_table(t: dict) -> pd.DataFrame:
    """The Shapley steps of the banks with a decomposition at the latest date and the largest gaps to the median in
    either direction: 1 row per bank, in points of RoTE."""
    b = t["bench"]
    b = b[(b["date"] == t["latest"]) & (b["group"] == GROUP) & (b["basis"] == BASIS) & (b["kpi"] == "rote")]
    b = b.assign(gap=(b["value"] - b["median"]) * 100).dropna(subset=["gap"])
    rows = []
    for r in b.assign(size=b["gap"].abs()).sort_values(["size", "bank_id"], ascending=[False, True]).itertuples():
        steps, start, end, _ = waterfall_steps(t, r.bank_id, t["latest"])
        if steps:
            rows.append({"bank_id": r.bank_id, "gap": r.gap, "reference": start, **dict(steps), "bank": end})
        if len(rows) == TOP_DRIVERS:
            break
    return pd.DataFrame(rows)


def seam_summary(t: dict) -> pd.DataFrame:
    c = t["checks"]
    c = c[c["check"] == SEAM].assign(size=lambda x: x["diff_rel"].abs())
    g = c.groupby("field")["size"]
    return pd.DataFrame({"banks": g.count(), "median": g.median(), "p90": g.quantile(P90)}).reset_index()


def scope_banks(t: dict) -> list[str]:
    """Amendment 26: the named bank insurers, and any bank whose total_assets seam is above 5%."""
    c = t["checks"]
    c = c[(c["check"] == SEAM) & (c["field"] == TOTAL_ASSETS)]
    wide = c.loc[c["diff_rel"].abs() > SCOPE_LIMIT, "bank_id"]
    return INSURERS + sorted(set(wide) - set(INSURERS))


def below_line(t: dict, bank: str) -> float:
    """The other below the line step of a bank's waterfall at the latest date, in points of RoTE."""
    d = t["drivers"]
    d = d[(d["date"] == t["latest"]) & (d["bank_id"] == bank) & (d["basis"] == BASIS) & (d["reference"] == REFERENCE)]
    return -float(d["other_below_line_pts"].iloc[0])


def blank_cells(t: dict) -> tuple[int, int, pd.Series]:
    """Blank KPI cells at the latest date on the headline basis: (blank, all, count by reason)."""
    k = t["kpi"]
    k = k[(k["date"] == t["latest"]) & (k["basis"] == BASIS)]
    blank = k[k["value"].isna()]
    reason = blank["status"].str.split(";").str[0].str.replace("missing_input:", "", regex=False)
    return len(blank), len(k), reason.value_counts()


def answers(root: Path) -> pd.DataFrame:
    """outputs/tables/answers.csv: each claim is generated from the source named beside it."""
    t = load(root)
    d = t["latest"]
    rote, ci = overall(t, "rote").iloc[0], overall(t, "cost_income").iloc[0]
    gaps = largest_gaps(t)
    top = gaps.iloc[0]
    drivers = driver_table(t)
    first = drivers.iloc[0]
    steps = first.drop(["bank_id", "gap", "reference", "bank"]).astype(float)
    fits = t["valuation_fits"].set_index("year")
    last = fits.index.max()
    stable = t["valuation_stability"].iloc[0]
    seam = seam_summary(t).set_index("field")
    rows = [
        (1, f"{rote['name']} has the highest RoTE at {d}, {rote['value'] * 100:.2f}%, with verdict {rote['verdict']}.",
         f"league_rote_{GROUP}_{d}.csv, largest value"),
        (1, f"{ci['name']} has the lowest cost to income at {d}, {ci['value'] * 100:.2f}%, with verdict {ci['verdict']}.",
         f"league_cost_income_{GROUP}_{d}.csv, lowest value"),
        (2, f"{top['bank_id']} has the largest joint gap at {d}, EUR {top['joint_eur'] / 1e6:,.0f}m.",
         f"gaps_joint.csv, date == {d}, group == {GROUP}, basis == {BASIS}, largest joint_eur"),
        (2, f"{headline_claim(t)} Banks whose accounting scope differs between the 2 sources are left out.",
         (f"gaps_joint.csv, date == {d}, group == {GROUP}, basis == {BASIS}, bank_id not in the scope list, "
          "largest joint_rote_pts")),
        (3, (f"{first['bank_id']} has the largest RoTE gap to the median among banks with a decomposition at {d}, "
            f"{first['gap']:+.2f} points; its largest step is {steps.abs().idxmax()}, "
            f"{steps[steps.abs().idxmax()]:+.2f} points."),
         f"drivers.csv, date == {d}, basis == {BASIS}, reference == {REFERENCE}, bank_id == {first['bank_id']}"),
        (4, (f"A point of RoTE added {fits.loc[last, 'beta'] / 100:.3f}x of P/TBV at the end of {last}, implying a cost of "
            f"equity of {fits.loc[last, 'coe_implied'] * 100:.2f}%."), f"valuation_fits.csv, year == {last}"),
        (4, f"The year slopes differ: F {stable['f_stat']:.2f}, p {stable['p_value']:.5f}.", "valuation_stability.csv"),
        (5, (f"Total assets differ between EBA and bank reports by a median of {seam.loc[TOTAL_ASSETS, 'median'] * 100:.2f}% "
            f"and pbt by {seam.loc['pbt', 'median'] * 100:.2f}%."), f"checks.csv, check == {SEAM}, field in (total_assets, pbt)"),
    ]
    return pd.DataFrame(rows, columns=ANSWERS_COLUMNS)
