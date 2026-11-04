"""Regenerates every output built so far from committed raw and manual files (no network).

Section 3: data/processed/facts.parquet (eba, report and p3 rows), outputs/tables/kpi.csv (every bank, 2021-12-31 to
2026-06-30, reported and underlying) and outputs/tables/checks.csv (checks 1 to 9; check 9 on EBA rows; check 1 also
on one_offs.csv rows, whose failures are left out of the underlying basis). Section 4: outputs/tables/peers.csv,
bench.csv, gaps.csv, gaps_joint.csv, gaps_range.csv, and the profiles of the hand check banks. Section 5:
outputs/tables/drivers.csv, yoy.csv, valuation_fits.csv, valuation_stability.csv, valuation.csv, the valuation figures,
and spec_log.csv, rewritten with 1 row per fit.
usage: python scripts/run_all.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bpb.benchmark import benchmark
from bpb.checks import one_off_provenance, run_checks
from bpb.config import load_config
from bpb.drivers import decompose, year_on_year
from bpb.fx import ecb_rates
from bpb.gaps import gaps_range, joint_table, size_gaps
from bpb.ingest import build_facts, read_manifest, read_universe, report_p3_facts
from bpb.kpi import compute_kpis
from bpb.market import load_prices
from bpb.peers import peer_groups
from bpb.report import build_profile, render_png
from bpb.tables import write_csv
from bpb.valuation import (
    FITS_COLUMNS,
    STABILITY_COLUMNS,
    YEARS,
    figure,
    fit_frame,
    fit_pooled,
    fit_stability,
    fit_year,
    ptbv,
    spec_log,
    spec_row,
    uplift,
)

KPI_LAST = "2026-06-30"  # instruction 02 step 2.5: kpi.csv now runs to 2026-06-30


def main() -> int:
    cfg = load_config(Path(__file__).resolve().parents[1] / "config.toml")
    root = cfg.root
    facts = build_facts(cfg)
    rates = ecb_rates(root / "data" / "raw")
    with open(root / "config" / "kpis.yaml", encoding="utf-8") as f:
        kpis = yaml.safe_load(f)
    one_offs = pd.read_csv(root / "data" / "manual" / "one_offs.csv", dtype={"page": str})
    urls = pd.read_csv(root / "data" / "manual" / "report_urls.csv", dtype=str, keep_default_na=False)
    man = read_manifest(root / "data" / "raw").merge(urls, how="left", on=["bank_id", "doc_type", "period"])
    marks = dict(zip(man["sha256"], man["decimal_mark"].fillna(""), strict=True))
    oprov = one_off_provenance(one_offs, root / "data" / "raw" / "report_text", marks)
    failed = set(oprov.loc[~oprov["passed"].astype(bool), "note"].str.extract(r"one_off (\d+)")[0].astype(int))
    kpi = compute_kpis(facts, kpis, one_offs.drop(index=sorted(failed)), rates)
    kpi = kpi[kpi["date"] <= KPI_LAST]
    write_csv(kpi, root / "outputs" / "tables" / "kpi.csv")
    _, prov = report_p3_facts(cfg)
    checks = run_checks(facts, cfg, pd.concat([prov, oprov], ignore_index=True))
    write_csv(checks, root / "outputs" / "tables" / "checks.csv")
    print(f"facts {len(facts)} rows, kpi {len(kpi)} rows, checks {len(checks)} rows")
    peers = peer_groups(kpi, facts, cfg)
    write_csv(peers, root / "outputs" / "tables" / "peers.csv")
    bench = benchmark(kpi, peers, read_universe(root), cfg)
    write_csv(bench, root / "outputs" / "tables" / "bench.csv")
    print(f"peers {len(peers)} rows, bench {len(bench)} rows")
    gaps = size_gaps(bench, kpi, facts, rates, cfg)
    write_csv(gaps, root / "outputs" / "tables" / "gaps.csv")
    write_csv(joint_table(gaps, bench, kpi, facts, rates, cfg), root / "outputs" / "tables" / "gaps_joint.csv")
    write_csv(gaps_range(gaps), root / "outputs" / "tables" / "gaps_range.csv")
    print(f"gaps {len(gaps)} rows")
    drivers = decompose(kpi, facts, peers, cfg)
    write_csv(drivers, root / "outputs" / "tables" / "drivers.csv")
    yoy = year_on_year(kpi, facts, cfg)
    write_csv(yoy, root / "outputs" / "tables" / "yoy.csv")
    print(f"drivers {len(drivers)} rows, yoy {len(yoy)} rows")
    universe = read_universe(root)
    prices = ptbv(facts, load_prices(root / "data" / "raw"), rates, universe)
    frame = fit_frame(prices, kpi, universe, cfg)
    params = {"dependent": "ptbv", "regressors": ["rote", "spread"], "growth": cfg.valuation.growth}
    fits, specs = [], []
    for year in YEARS:
        fit = fit_year(frame[frame["year"] == year])
        fits.append(fit)
        specs.append(spec_row(f"fit_year_{year}", "yearly OLS, HC3", {**params, "year": year}, fit))
        (root / "outputs" / "figures" / f"valuation_{year}.png").write_bytes(figure(frame[frame["year"] == year], fit))
    pooled = fit_pooled(frame)
    specs.append(spec_row("fit_pooled", "pooled OLS, year dummies, clustered by bank", params, pooled))
    stable = fit_stability(frame)
    specs.append(spec_row("fit_stability", "pooled OLS, year dummies, rote x year, clustered by bank, Wald F", params, stable))
    write_csv(pd.DataFrame([stable])[STABILITY_COLUMNS], root / "outputs" / "tables" / "valuation_stability.csv")
    write_csv(spec_log(specs), root / "outputs" / "tables" / "spec_log.csv")
    fits_table = pd.DataFrame(fits)[FITS_COLUMNS]
    write_csv(fits_table, root / "outputs" / "tables" / "valuation_fits.csv")
    joint = pd.read_csv(root / "outputs" / "tables" / "gaps_joint.csv")
    write_csv(uplift(joint, fits_table, pooled, prices), root / "outputs" / "tables" / "valuation.csv")
    print(f"valuation {len(frame)} rows")
    for bank in cfg.gaps.hand_check_banks:  # instruction 04 step 4.4: the first profiles
        pdf = build_profile(bank, KPI_LAST, root, root / "outputs" / "reports")
        render_png(pdf, root / "outputs" / "figures" / f"{pdf.stem}.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
