"""P/TBV against RoTE (kickoff Section 5.8, instruction 05 B.2).

RoTE and the spread are decimals, so beta is the change in P/TBV per unit of RoTE. Fits read a frame with bank_id, year,
ptbv, rote and spread; a bank with any of them missing is dropped and is not in `n`.
"""

from __future__ import annotations

import io
import json
from datetime import UTC, datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

from bpb import fx
from bpb.config import load_config
from bpb.gaps import _ccy
from bpb.ingest import ROOT
from bpb.kpi import compute_kpis

FITS_COLUMNS = ["year", "n", "alpha", "beta", "beta_se", "gamma", "gamma_se", "r2", "coe_implied", "huber_beta",
                "cooks_named", "status"]
VALUATION_COLUMNS = ["date", "bank_id", "price", "price_ccy", "tbvps", "ptbv", "rote_gap_pts", "uplift_ptbv",
                     "uplift_lo", "uplift_hi", "status"]
SPEC_COLUMNS = ["run_utc", "spec_id", "description", "params_json", "result_json"]
YEARS = range(2021, 2026)  # B.2: each 31 Dec from 2021 to 2025
UPLIFT_YEAR = 2025  # B.2: the uplift is computed at 2025-12-31 only
Z_90 = 1.645  # B.2: lo and hi from beta -/+ 1.645 x beta_se
PCT = 100.0  # B.2: spreads are in percent, and uplift_ptbv = beta x joint_rote_pts / 100
GROUP, BASIS = "cluster", "underlying"  # B.2
REGRESSORS = ["rote", "spread"]
# B.2: TBV per share uses the closing balance, under the KPI family rule
TE_CLOSE = {"kpis": [{"kpi": "te", "numerator": "tangible_equity", "denominator": "tangible_equity", "average": False,
                      "unit": "", "direction": "context"}]}
FIGURE_DPI = 150
LABEL_OFFSETS = [(5, 3), (5, -8), (-5, 3), (-5, -8), (0, 7), (0, -12), (11, -2), (-11, -2)]  # points from the marker
LABEL_SIZE = 7
LABEL_BOX = (24, 9)  # a label's width and height in points, for placing labels apart


def ptbv(facts: pd.DataFrame, prices: pd.DataFrame, rates: pd.DataFrame, universe: pd.DataFrame) -> pd.DataFrame:
    """date, bank_id, price, price_ccy, tbvps, ptbv, status for each listed bank in `facts` at each 31 Dec of YEARS.

    `prices` is `bpb.market.in_price_ccy` output, so the GBp rule (Convention 4.12) is already applied. TBV per share is
    in the family's currency (EUR for an eba row, amendment 7) and is converted at the date's ECB cross rate."""
    te = compute_kpis(facts, TE_CLOSE, None, rates)
    te = {(r.date, r.bank_id): r for r in te[te["basis"] == "reported"].itertuples(index=False)}
    shares = facts[(facts["field"] == "shares_out") & facts["value"].notna()]
    shares = {(r.ref_date, r.bank_id): float(r.value) for r in shares.itertuples(index=False)}
    listed = universe[(universe["listed"].astype(str) == "1") & universe["bank_id"].isin(facts["bank_id"])]
    rows = []
    for u in listed.itertuples(index=False):
        quotes = prices[prices["ticker"] == u.ticker].sort_values("date")
        for year in YEARS:
            d = f"{year}-12-31"
            row = {"date": d, "bank_id": u.bank_id, "price": np.nan, "price_ccy": u.price_ccy, "tbvps": np.nan,
                   "ptbv": np.nan, "status": "ok"}
            on = quotes[quotes["date"] <= d]
            if not on.empty:
                row["price"], row["price_ccy"] = on["price"].iloc[-1], on["price_ccy"].iloc[-1]
            t = te.get((d, u.bank_id))
            if t is None or pd.isna(t.numerator) or (d, u.bank_id) not in shares:
                row["status"] = "missing_input"
            else:
                per_share = t.numerator / shares[(d, u.bank_id)]
                ccy = _ccy(t.family, u.report_ccy)
                cross = 1.0 if ccy == row["price_ccy"] else (fx.rate(row["price_ccy"], d, "bs", rates, None)
                                                             / fx.rate(ccy, d, "bs", rates, None))
                row["tbvps"] = per_share * cross
            if pd.isna(row["price"]):
                row["status"] = "missing_input"
            elif pd.notna(row["tbvps"]):
                row["ptbv"] = row["price"] / row["tbvps"]
            rows.append(row)
    return pd.DataFrame(rows, columns=["date", "bank_id", "price", "price_ccy", "tbvps", "ptbv", "status"])


def fit_frame(table: pd.DataFrame, kpi: pd.DataFrame, universe: pd.DataFrame, cfg) -> pd.DataFrame:
    """`ptbv` rows with year, underlying rote at the date and the December spread of the home 10 year over DE."""
    out = table.assign(year=table["date"].str[:4].astype(int))
    rote = kpi[(kpi["kpi"] == "rote") & (kpi["basis"] == BASIS)][["bank_id", "date", "value"]]
    out = out.merge(rote.rename(columns={"value": "rote"}), on=["bank_id", "date"], how="left")
    raw = cfg.root / "data" / "raw" / "yields"

    def december(country: str) -> dict[int, float]:
        y = pd.read_csv(raw / f"{country}.csv", dtype={"period": str})
        y = y[y["period"].str[5:] == "12"]
        return dict(zip(y["period"].str[:4].astype(int), y["yield_pct"], strict=True))

    base = december(cfg.sovereign.benchmark)
    home = {c: december(c) for c in cfg.sovereign.countries}
    country = dict(zip(universe["bank_id"], universe["country"], strict=True))
    out["spread"] = [(home[country[b]][y] - base[y]) / PCT for b, y in zip(out["bank_id"], out["year"], strict=True)]
    return out


def _sample(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(subset=["ptbv", *REGRESSORS]).sort_values("bank_id").reset_index(drop=True)


def fit_year(df: pd.DataFrame) -> dict:
    """The VALUATION_FITS row of 1 year's banks, plus `cooks`, each bank's Cook's distance."""
    cfg = load_config(ROOT / "config.toml").valuation
    s = _sample(df)
    x = sm.add_constant(s[REGRESSORS])
    res = sm.OLS(s["ptbv"], x).fit(cov_type="HC3")
    n = len(s)
    cooks = dict(zip(s["bank_id"], res.get_influence().cooks_distance[0], strict=True))
    beta = float(res.params["rote"])
    return {"year": int(s["year"].iloc[0]) if "year" in s else np.nan, "n": n, "alpha": float(res.params["const"]),
            "beta": beta, "beta_se": float(res.bse["rote"]), "gamma": float(res.params["spread"]),
            "gamma_se": float(res.bse["spread"]), "r2": float(res.rsquared),
            "coe_implied": cfg.growth + 1 / beta if beta > 0 else np.nan,
            "huber_beta": float(sm.RLM(s["ptbv"], x, M=sm.robust.norms.HuberT()).fit().params["rote"]),
            "cooks_named": ";".join(b for b, c in cooks.items() if c > cfg.cooks_factor / n),
            "status": "ok" if beta > 0 else "beta_not_positive", "cooks": cooks}


def fit_pooled(df: pd.DataFrame) -> dict:
    """OLS over all years with year dummies, standard errors clustered by bank; `contains_zero` is the B.2 test on the
    `[valuation] ci` interval of beta."""
    cfg = load_config(ROOT / "config.toml").valuation
    s = _sample(df)
    dummies = pd.get_dummies(s["year"], prefix="y", drop_first=True, dtype=float)
    x = sm.add_constant(pd.concat([s[REGRESSORS], dummies], axis=1))
    groups = s["bank_id"].astype("category").cat.codes.to_numpy()
    res = sm.OLS(s["ptbv"], x).fit(cov_type="cluster", cov_kwds={"groups": groups})
    lo, hi = (float(v) for v in res.conf_int(alpha=1 - cfg.ci).loc["rote"])
    return {"n": len(s), "n_banks": int(s["bank_id"].nunique()), "beta": float(res.params["rote"]),
            "beta_se": float(res.bse["rote"]), "gamma": float(res.params["spread"]),
            "gamma_se": float(res.bse["spread"]), "r2": float(res.rsquared), "ci_lo": lo, "ci_hi": hi,
            "contains_zero": bool(lo <= 0 <= hi)}


def uplift(gaps_joint: pd.DataFrame, fits: pd.DataFrame, pooled: dict, ptbv: pd.DataFrame) -> pd.DataFrame:
    """VALUATION: every `ptbv` row; the uplift columns are filled at 2025-12-31 only, from that year's fit and the joint
    RoTE gap of the cluster group on the underlying basis (B.2)."""
    date = f"{UPLIFT_YEAR}-12-31"
    fit = fits[fits["year"] == UPLIFT_YEAR].iloc[0]
    j = gaps_joint[(gaps_joint["date"] == date) & (gaps_joint["group"] == GROUP) & (gaps_joint["basis"] == BASIS)]
    gap = dict(zip(j["bank_id"], j["joint_rote_pts"], strict=True))
    rows = []
    for r in ptbv.itertuples(index=False):
        row = {"date": r.date, "bank_id": r.bank_id, "price": r.price, "price_ccy": r.price_ccy, "tbvps": r.tbvps,
               "ptbv": r.ptbv, "rote_gap_pts": np.nan, "uplift_ptbv": np.nan, "uplift_lo": np.nan, "uplift_hi": np.nan,
               "status": "uplift_2025_only"}
        if r.date == date:
            pts = gap.get(r.bank_id, np.nan)
            row["rote_gap_pts"] = pts
            if pooled["contains_zero"]:
                row["status"] = "beta_not_significant"
            elif pd.isna(pts):
                row["status"] = "no_joint_gap"
            else:
                row.update(uplift_ptbv=fit["beta"] * pts / PCT,
                           uplift_lo=(fit["beta"] - Z_90 * fit["beta_se"]) * pts / PCT,
                           uplift_hi=(fit["beta"] + Z_90 * fit["beta_se"]) * pts / PCT, status="ok")
        rows.append(row)
    return pd.DataFrame(rows, columns=VALUATION_COLUMNS)


def append_spec_log(path: Path, spec_id: str, description: str, params: dict, result: dict) -> None:
    """B.2: 1 row per fit, added to outputs/tables/spec_log.csv."""
    row = pd.DataFrame([{"run_utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"), "spec_id": spec_id,
                         "description": description, "params_json": json.dumps(params, sort_keys=True),
                         "result_json": json.dumps(result, sort_keys=True, default=float)}], columns=SPEC_COLUMNS)
    text = row.to_csv(index=False, header=not Path(path).exists(), lineterminator="\n")
    with open(path, "ab") as f:
        f.write(text.encode("utf-8"))


def _place_labels(ax, xy: np.ndarray, names: list[str]) -> None:
    """Each label takes the first offset, nearest first, that clears the markers and the labels already placed."""
    fig = ax.figure
    fig.canvas.draw()
    scale = fig.dpi / 72
    pts = ax.transData.transform(xy)
    w, h = LABEL_BOX[0] * scale, LABEL_BOX[1] * scale
    taken: list[tuple[float, float]] = []

    def clash(c: tuple[float, float]) -> float:
        boxes = sum(abs(c[0] - t[0]) < w and abs(c[1] - t[1]) < h for t in taken)
        return boxes + sum(abs(c[0] - p[0]) < w / 2 and abs(c[1] - p[1]) < h / 2 for p in pts) / 2

    for p, xy_i, name in sorted(zip(pts.tolist(), xy.tolist(), names, strict=True), key=lambda z: z[0]):
        options = []
        for dx, dy in LABEL_OFFSETS:
            sx = 1 if dx >= 0 else -1
            c = (p[0] + (dx * scale + sx * w / 2), p[1] + dy * scale + h / 2)
            options.append((clash(c), c, (dx, dy)))
        _, c, off = min(options, key=lambda o: o[0])
        taken.append(c)
        ax.annotate(name, xy_i, xytext=off, textcoords="offset points", fontsize=LABEL_SIZE, color="#333333",
                    ha="left" if off[0] >= 0 else "right")


def figure(year_df: pd.DataFrame, fit: dict) -> bytes:
    """Review figure (B.2): P/TBV against underlying RoTE, 1 labelled point per bank, the OLS line at the mean spread."""
    s = _sample(year_df)
    fig, ax = plt.subplots(figsize=(8.5, 5.6), dpi=FIGURE_DPI)
    x = s["rote"].to_numpy() * PCT
    ax.scatter(x, s["ptbv"], s=30, color="#2f5d8a", linewidths=0, zorder=3)
    line = np.array([s["rote"].min(), s["rote"].max()])
    ax.plot(line * PCT, fit["alpha"] + fit["beta"] * line + fit["gamma"] * s["spread"].mean(), color="#8a8a8a", lw=1.4,
            zorder=2)
    ax.margins(0.09)
    ax.set_xlabel("Underlying RoTE (%)", fontsize=9)
    ax.set_ylabel("P/TBV (x)", fontsize=9)
    ax.set_title(f"P/TBV against underlying RoTE, 31 Dec {fit['year']}: beta {fit['beta']:.2f}, "
                 f"n {fit['n']}, R² {fit['r2']:.2f}", fontsize=10, loc="left")
    ax.tick_params(labelsize=8, length=0)
    ax.grid(color="#e6e6e6", lw=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    _place_labels(ax, np.column_stack([x, s["ptbv"]]), s["bank_id"].tolist())
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()
