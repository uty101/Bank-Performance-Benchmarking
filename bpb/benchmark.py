"""Benchmarks (kickoff Section 5.5, instruction 04 B.2): leave one out targets, position, trend and verdict.

Every bootstrap has its own generator keyed on date, bank, KPI, basis and group, so results do not depend on loop order.
"""

from __future__ import annotations

import zlib
from functools import cache

import numpy as np
import pandas as pd
import yaml
from scipy.stats import beta, median_abs_deviation
from scipy.stats.mstats import hdquantiles

from bpb.peers import cluster_year

BENCH_COLUMNS = ["date", "bank_id", "kpi", "basis", "group", "n_peers", "value", "median", "target", "target_lo",
                 "target_hi", "pct_rank", "robust_z", "trend_kpi", "trend_gap", "inside_noise", "verdict", "status"]
GROUPS = ["cluster", "market", "universe"]
P_TARGET = {"higher": 0.75, "lower": 0.25}  # kickoff Section 5.5
P_MEDIAN = 0.5
INTERVAL = [5, 95]  # kickoff Section 5.5: the 5th and 95th percentiles of the draws
MAD_SCALE = 1.4826  # kickoff Section 5.5
TREND_YEARS = 3  # kickoff Section 5.5: the latest 3 fiscal year ends


def target(values: np.ndarray, p: float) -> float:
    """Harrell Davis quantile of `values` at p."""
    return float(hdquantiles(np.asarray(values, dtype=float), prob=[p])[0])


@cache
def _hd_weights(n: int, p: float) -> np.ndarray:
    """The weights `hdquantiles` puts on the sorted values, so a whole bootstrap is 1 matrix product."""
    return np.diff(beta.cdf(np.arange(n + 1) / n, (n + 1) * p, (n + 1) * (1 - p)))


def target_interval(values: np.ndarray, p: float, reps: int, rng) -> tuple[float, float]:
    """The 5th and 95th percentiles of `reps` Harrell Davis estimates on draws of the peers with replacement."""
    v = np.asarray(values, dtype=float)
    draws = np.sort(v[rng.integers(0, len(v), (reps, len(v)))], axis=1) @ _hd_weights(len(v), p)
    lo, hi = np.percentile(draws, INTERVAL)
    return float(lo), float(hi)


def bench_rng(cfg, date: str, bank: str, kpi: str, basis: str, group: str):
    key = f"{date}|{bank}|{kpi}|{basis}|{group}"
    return np.random.default_rng(np.random.SeedSequence([cfg.bench.bench_seed, zlib.crc32(key.encode())]))


def better(a: float, b: float, direction: str) -> bool:
    return a > b if direction == "higher" else a < b


def verdict(value: float, median: float, tgt: float, inside_noise: bool, direction: str) -> str:
    """B.2: inside noise is in_line; otherwise leading if better than the target, lagging if worse than the median,
    otherwise in_line."""
    if inside_noise:
        return "in_line"
    if better(value, tgt, direction):
        return "leading"
    return "lagging" if better(median, value, direction) else "in_line"


def _position(value: float, peers: np.ndarray, median: float, direction: str) -> tuple[float, float]:
    """Percentile rank (share of peers beaten, ties half) and robust z, signed so positive is better."""
    sign = 1.0 if direction == "higher" else -1.0
    rank = (np.sum(sign * value > sign * peers) + 0.5 * np.sum(value == peers)) / len(peers)
    mad = median_abs_deviation(peers)
    return float(rank), (sign * (value - median) / (MAD_SCALE * mad) if mad > 0 else np.nan)


def _slope(y: list[float]) -> float:
    """OLS slope per year over 3 equally spaced year ends."""
    x = np.arange(len(y), dtype=float)
    return float(np.polyfit(x, np.asarray(y, dtype=float), 1)[0])


def _fiscal_ends(date: str) -> list[str]:
    last = int(date[:4]) if date[5:] == "12-31" else int(date[:4]) - 1
    return [f"{y}-12-31" for y in range(last - TREND_YEARS + 1, last + 1)]


def _group_members(peers: pd.DataFrame, universe: pd.DataFrame, banks: list[str], date: str) -> dict:
    """{group: {bank: label}} at a date; a bank with no label is in no group of that kind."""
    year = cluster_year(date)
    p = peers[(peers["year"] == year) & peers["cluster"].notna()]
    market = dict(zip(universe["bank_id"], universe["market"], strict=True))
    return {"cluster": dict(zip(p["bank_id"], p["cluster"], strict=True)),
            "market": {b: market[b] for b in banks if b in market}, "universe": dict.fromkeys(banks, "all")}


def _directions(cfg) -> dict[str, str]:
    with open(cfg.root / "config" / "kpis.yaml", encoding="utf-8") as f:
        return {k["kpi"]: k["direction"] for k in yaml.safe_load(f)["kpis"] if k["direction"] in P_TARGET}


def benchmark(kpi: pd.DataFrame, peers: pd.DataFrame, universe: pd.DataFrame, cfg) -> pd.DataFrame:
    """BENCH: every KPI date, ranked KPI, basis and group (B.2). Peers exclude the bank and blank values; fewer than
    `min_peers` gives `too_few_peers`. A bank with a blank value keeps its row, with its KPI's status."""
    directions = _directions(cfg)
    k = kpi[kpi["kpi"].isin(directions)].sort_values(["date", "kpi", "basis", "bank_id"], kind="stable")
    rows = []
    for (date, name, basis), sub in k.groupby(["date", "kpi", "basis"], sort=True):
        direction = directions[name]
        banks = sub["bank_id"].tolist()
        vals = dict(zip(sub["bank_id"], sub["value"], strict=True))
        stats = dict(zip(sub["bank_id"], sub["status"], strict=True))
        members = _group_members(peers, universe, banks, date)
        for bank in banks:
            for group in GROUPS:
                rows.append(_one_row(date, bank, name, basis, group, vals, stats, members[group], direction, cfg))
    out = pd.DataFrame(rows, columns=BENCH_COLUMNS)
    return _add_trends(out, k).sort_values(["date", "bank_id", "kpi", "basis", "group"]).reset_index(drop=True)


def _one_row(date, bank, name, basis, group, vals, stats, member, direction, cfg) -> dict:
    row = dict.fromkeys(BENCH_COLUMNS, np.nan)
    row.update(date=date, bank_id=bank, kpi=name, basis=basis, group=group, value=vals[bank], verdict="", status="ok",
               inside_noise=pd.NA)
    if bank not in member:
        row["status"], row["n_peers"] = "no_cluster", 0
        return row
    peer_values = np.array([vals[b] for b in sorted(member) if b != bank and member[b] == member[bank]
                            and b in vals and pd.notna(vals[b])], dtype=float)
    row["n_peers"] = len(peer_values)
    if len(peer_values) < cfg.bench.min_peers:
        row["status"] = "too_few_peers"
        return row
    p = P_TARGET[direction]
    row["median"], row["target"] = target(peer_values, P_MEDIAN), target(peer_values, p)
    lo, hi = target_interval(peer_values, p, cfg.bench.bench_reps, bench_rng(cfg, date, bank, name, basis, group))
    row["target_lo"], row["target_hi"] = lo, hi
    value = vals[bank]
    if pd.isna(value):
        row["status"] = stats[bank]
        return row
    row["pct_rank"], row["robust_z"] = _position(value, peer_values, row["median"], direction)
    inside = bool(lo <= value <= hi)
    row["inside_noise"] = inside
    row["verdict"] = verdict(value, row["median"], row["target"], inside, direction)
    return row


def _add_trends(bench: pd.DataFrame, k: pd.DataFrame) -> pd.DataFrame:
    """trend_kpi and trend_gap over the latest 3 fiscal year ends up to each date, all 3 of 1 family (B.2)."""
    value = {(r.bank_id, r.kpi, r.basis, r.date): (r.value, r.family) for r in k.itertuples(index=False)}
    tgt = {(r.bank_id, r.kpi, r.basis, r.group, r.date): r.target for r in bench.itertuples(index=False)}
    trend_k, trend_g, status = [], [], []
    for r in bench.itertuples(index=False):
        ends = _fiscal_ends(r.date)
        got = [value.get((r.bank_id, r.kpi, r.basis, d), (np.nan, "")) for d in ends]
        tk = tg = np.nan
        st = r.status
        if any(pd.isna(v) for v, _ in got):
            note = "short_history"
        elif len({f for _, f in got}) != 1:
            note = "family_switch"
        else:
            note = ""
            tk = _slope([v for v, _ in got])
            ts = [tgt.get((r.bank_id, r.kpi, r.basis, r.group, d), np.nan) for d in ends]
            if any(pd.isna(t) for t in ts):
                note = "short_history"
            else:
                tg = _slope([t - v for t, (v, _) in zip(ts, got, strict=True)])
        if note:
            st = note if st == "ok" else f"{st};{note}"
        trend_k.append(tk)
        trend_g.append(tg)
        status.append(st)
    return bench.assign(trend_kpi=trend_k, trend_gap=trend_g, status=status)
