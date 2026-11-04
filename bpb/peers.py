"""Peer groups (kickoff Section 5.4, instruction 04 B.1): 6 features per bank, Ward clusters, bootstrap stability.

Features are levels, so a 3 year mean may mix families (B.1). Banks missing a feature in a year are left out of that
year's clustering and assigned to the nearest centroid on the features they have, status `assigned_nearest`.
"""

from __future__ import annotations

from itertools import pairwise

import numpy as np
import pandas as pd
import yaml
from scipy.cluster.hierarchy import fcluster, linkage
from sklearn.metrics import adjusted_rand_score, silhouette_score

from bpb import fx
from bpb.ingest import read_source_map

FEATURES = ["ln_assets", "loans_assets", "fee_share", "household_share", "trading_assets", "loan_deposit"]
PEERS_COLUMNS = ["year", "bank_id", "cluster", "k", "silhouette", "stability", "borderline", "override_reason",
                 "status"]
FEATURE_BASIS = "reported"  # instruction 04b B.2: features describe business mix, not performance
FIRST_CLUSTER_DATE = "2023-12-31"  # B.1: every date before this uses the 2023 clusters
LAST_YEARS = 3  # B.1: the 3 fiscal year ends up to and including the year
MIN_YEARS = 2  # instruction 04b B.2: a feature needs at least 2 of the 3 year ends


class StopSection(RuntimeError):
    """A rule 4 stop: no k qualifies (kickoff Section 5.4)."""


def cluster_year(date: str) -> int:
    """B.1: 31 Dec of y uses the year y clusters, 30 Jun of y the year y - 1 clusters; dates before 2023-12-31 use
    the 2023 clusters."""
    if date < FIRST_CLUSTER_DATE:
        return int(FIRST_CLUSTER_DATE[:4])
    return int(date[:4]) if date[5:] == "12-31" else int(date[:4]) - 1


def _year_end_values(facts: pd.DataFrame, d: str, cfg) -> pd.DataFrame:
    """bank_id x field at date d, one family per value, under the KPI rule: a UK bank is report family at every date,
    an EU bank is eba up to the last EBA date and p3 or report after it (kickoff 3.3, OPEN-03)."""
    uk = set(read_source_map(cfg.root)["bank_groups"]["uk"])
    x = facts[(facts["ref_date"] == d) & facts["value"].notna()]
    is_eba = x["family"] == "eba"
    keep = (~is_eba) if d > cfg.sources.eba_last else (is_eba ^ x["bank_id"].isin(uk))
    x = x[keep].sort_values("family").drop_duplicates(["bank_id", "field"])  # p3 before report
    return x.pivot(index="bank_id", columns="field", values="value").join(
        x[x["field"] == "total_assets"].set_index("bank_id")["ccy"].rename("_ta_ccy"))


def _features_at(kpi: pd.DataFrame, facts: pd.DataFrame, d: str, rates: pd.DataFrame, cfg) -> pd.DataFrame:
    banks = sorted(facts["bank_id"].unique())
    v = _year_end_values(facts, d, cfg).reindex(banks)

    def col(f):
        return v[f] if f in v else pd.Series(np.nan, index=v.index)

    ta_eur = pd.Series([fx.to_eur(a, c, d, "bs", rates, None) if pd.notna(a) else np.nan
                        for a, c in zip(col("total_assets"), v["_ta_ccy"], strict=True)], index=v.index)
    k = kpi[(kpi["date"] == d) & (kpi["basis"] == FEATURE_BASIS)]
    level = {name: k[k["kpi"] == name].set_index("bank_id")["value"].reindex(banks) for name in
             ("fee_share", "loan_deposit")}
    net = col("loans_customers_gross") - col("loans_customers_allowance")
    return pd.DataFrame({
        "ln_assets": np.log(ta_eur), "loans_assets": net / col("total_assets"), "fee_share": level["fee_share"],
        "household_share": col("loans_households_gross") / col("loans_customers_gross"),
        "trading_assets": col("trading_assets") / col("total_assets"), "loan_deposit": level["loan_deposit"]})


def _year_frames(kpi, facts, year, rates, cfg) -> list[pd.DataFrame]:
    return [_features_at(kpi, facts, f"{y}-12-31", rates, cfg) for y in range(year - LAST_YEARS + 1, year + 1)]


def _config(cfg):
    if cfg is not None:
        return cfg
    from bpb.config import load_config
    from bpb.ingest import ROOT
    return load_config(ROOT / "config.toml")


def features(kpi: pd.DataFrame, facts: pd.DataFrame, year: int, rates: pd.DataFrame, cfg=None) -> pd.DataFrame:
    """The 6 features at 31 Dec of `year`, index bank_id. Each is the mean of the values present at the 3 fiscal year
    ends up to and including that year, if at least 2 are present; otherwise it is missing (instruction 04b B.2)."""
    frames = _year_frames(kpi, facts, year, rates, _config(cfg))
    present = sum(f.notna().astype(int) for f in frames)
    mean = sum(f.fillna(0.0) for f in frames) / present.where(present > 0)
    return mean.where(present >= MIN_YEARS)[FEATURES]


def two_of_three(kpi: pd.DataFrame, facts: pd.DataFrame, year: int, rates: pd.DataFrame, cfg=None) -> pd.Series:
    """True for a bank with a feature built from only 2 of its 3 year ends (status `two_of_three`)."""
    frames = _year_frames(kpi, facts, year, rates, _config(cfg))
    return (sum(f.notna().astype(int) for f in frames) == MIN_YEARS).any(axis=1)


def _standardise(x: pd.DataFrame) -> pd.DataFrame:
    return (x - x.mean()) / x.std(ddof=0)  # kickoff Section 5.4: standard deviation with ddof 0


def _cut(z: np.ndarray, k: int) -> np.ndarray:
    return fcluster(linkage(z, method="ward"), t=k, criterion="maxclust")


def candidates(features: pd.DataFrame, cfg) -> pd.DataFrame:
    """Every k of `k_range`: k, cluster sizes, silhouette, and whether every cluster has `min_cluster_size` banks."""
    z = _standardise(features).to_numpy()
    rows = []
    for k in cfg.peers.k_range:
        labels = _cut(z, k)
        sizes = np.bincount(labels)[1:]
        rows.append({"k": k, "sizes": sorted(sizes.tolist(), reverse=True), "silhouette":
                     silhouette_score(z, labels) if len(sizes) > 1 else np.nan,
                     "qualifies": bool(len(sizes) == k and sizes.min() >= cfg.peers.min_cluster_size)})
    return pd.DataFrame(rows)


def cluster(features: pd.DataFrame, cfg) -> tuple[pd.Series, int, float]:
    """(labels, k, silhouette) on complete rows. The highest silhouette among qualifying k, ties to the smaller k;
    clusters are numbered 1 to k in descending mean ln_assets (B.1). No qualifying k is a rule 4 stop."""
    c = candidates(features, cfg)
    ok = c[c["qualifies"]]
    if ok.empty:
        raise StopSection(f"no k qualifies:\n{c.to_string()}")
    best = ok.sort_values(["silhouette", "k"], ascending=[False, True], kind="stable").iloc[0]
    k = int(best["k"])
    raw = pd.Series(_cut(_standardise(features).to_numpy(), k), index=features.index)
    order = features["ln_assets"].groupby(raw).mean().sort_values(ascending=False, kind="stable").index
    labels = raw.map({old: new for new, old in enumerate(order, start=1)}).rename("cluster")
    return labels, k, float(best["silhouette"])


def stability(features: pd.DataFrame, k: int, cfg) -> pd.Series:
    """Kickoff Section 5.4 and B.1: one generator per call, `stability_reps` draws in order, the drawn rows being the
    unique indices of rng.integers(0, n, n). The drawn set is reclustered with the same k; each original cluster,
    restricted to the drawn banks, takes its Jaccard with its best matching bootstrap cluster. A bank's stability is
    the mean over the draws that hold any bank of its cluster."""
    rng = np.random.default_rng(cfg.peers.peer_seed)
    labels = _cut(_standardise(features).to_numpy(), k)
    n = len(features)
    total, count = np.zeros(k + 1), np.zeros(k + 1)
    for _ in range(cfg.peers.stability_reps):
        idx = np.unique(rng.integers(0, n, n))
        sub = _standardise(features.iloc[idx]).fillna(0.0).to_numpy()  # a feature constant in the draw adds nothing
        boot = _cut(sub, min(k, len(idx)))
        orig = labels[idx]
        for c in np.unique(orig):
            a = orig == c
            best = max((a & (boot == b)).sum() / (a | (boot == b)).sum() for b in np.unique(boot))
            total[c] += best
            count[c] += 1
    return pd.Series((total / np.where(count == 0, 1, count))[labels], index=features.index, name="stability")


def assign_nearest(row: pd.Series, clustered: pd.DataFrame, labels: pd.Series) -> int:
    """B.1: the cluster whose centroid is nearest in standardised space, on the features the bank has, standardised
    with the means and standard deviations of the clustered banks."""
    have = row.dropna().index
    mean, sd = clustered.mean(), clustered.std(ddof=0)
    centroids = ((clustered - mean) / sd).groupby(labels).mean()
    point = (row[have] - mean[have]) / sd[have]
    return int(((centroids[have] - point) ** 2).sum(axis=1).idxmin())


def _overrides(cfg) -> list[dict]:
    with open(cfg.root / "data" / "manual" / "peer_overrides.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def year_groups(feats: pd.DataFrame, year: int, cfg, partial: pd.Series | None = None) -> pd.DataFrame:
    """PEERS rows of one year from its feature table; `partial` marks the banks with status `two_of_three`."""
    full = feats.dropna()
    labels, k, sil = cluster(full, cfg)
    stab = stability(full, k, cfg)
    rows = []
    for bank, r in feats.iterrows():
        row = {"year": year, "bank_id": bank, "cluster": pd.NA, "k": k, "silhouette": sil, "stability": np.nan,
               "borderline": False, "override_reason": "", "status": "ok"}
        if bank in labels.index:
            row.update(cluster=int(labels[bank]), stability=float(stab[bank]),
                       borderline=bool(stab[bank] < cfg.peers.stability_flag))
        elif r.notna().any():
            row.update(cluster=assign_nearest(r, full, labels), status="assigned_nearest")
        else:
            row["status"] = "no_features"
        if partial is not None and partial.get(bank, False):
            row["status"] = "two_of_three" if row["status"] == "ok" else f"{row['status']};two_of_three"
        rows.append(row)
    return pd.DataFrame(rows, columns=PEERS_COLUMNS)


def peer_groups(kpi: pd.DataFrame, facts: pd.DataFrame, cfg) -> pd.DataFrame:
    """PEERS for every year from `first_year` to the last fiscal year end in `kpi`; peer_overrides.yaml applies after
    clustering (kickoff Section 5.4)."""
    rates = fx.ecb_rates(cfg.root / "data" / "raw")
    last = max(int(d[:4]) for d in kpi["date"].unique() if d[5:] == "12-31")
    out = pd.concat([year_groups(features(kpi, facts, y, rates, cfg), y, cfg, two_of_three(kpi, facts, y, rates, cfg))
                     for y in range(cfg.peers.first_year, last + 1)], ignore_index=True)
    for o in _overrides(cfg):
        hit = (out["year"] == o["year"]) & (out["bank_id"] == o["bank_id"])
        out.loc[hit, ["cluster", "override_reason"]] = [o["cluster"], o["reason"]]
    out["cluster"] = out["cluster"].astype("Int64")
    return out.sort_values(["year", "bank_id"]).reset_index(drop=True)


def ari_between_years(peers: pd.DataFrame) -> pd.DataFrame:
    """Adjusted Rand index between consecutive years' labels, over banks present in both (kickoff Section 5.4)."""
    rows = []
    years = sorted(peers["year"].unique())
    for a, b in pairwise(years):
        x = peers[peers["year"] == a].dropna(subset=["cluster"]).set_index("bank_id")["cluster"]
        y = peers[peers["year"] == b].dropna(subset=["cluster"]).set_index("bank_id")["cluster"]
        both = x.index.intersection(y.index)
        rows.append({"from": a, "to": b, "n": len(both), "ari": adjusted_rand_score(x[both], y[both])})
    return pd.DataFrame(rows)
