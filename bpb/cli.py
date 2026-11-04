"""Command line entry point (kickoff Section 5.9, instruction 06 B.2 and B.3): `bpb build`, `bpb trace`, `bpb bank`."""

from __future__ import annotations

import argparse
from pathlib import Path

from bpb.ingest import ROOT


def build(root: Path = ROOT) -> None:
    """The whole pipeline from data/raw and data/manual (instruction 06 B.3): facts, checks, KPIs, peers, bench, gaps,
    drivers, yoy, valuation, lineage, profiles and league tables. Everything is written under `root`."""
    import pandas as pd
    import yaml

    from bpb import valuation as val
    from bpb.answers import answers
    from bpb.benchmark import benchmark
    from bpb.checks import one_off_provenance, run_checks
    from bpb.config import load_config
    from bpb.drivers import TREE_SPEC, decompose, year_on_year
    from bpb.fx import ecb_rates
    from bpb.gaps import gaps_range, joint_table, size_gaps
    from bpb.ingest import (
        build_facts,
        entries_with_marks,
        read_manifest,
        read_universe,
        report_p3_facts,
    )
    from bpb.kpi import compute_kpis
    from bpb.lineage import derived_table, source_table
    from bpb.market import load_prices
    from bpb.peers import peer_groups
    from bpb.report import publish
    from bpb.tables import write_csv

    root = Path(root)
    cfg = load_config(ROOT / "config.toml")
    tables = root / "outputs" / "tables"
    figures = root / "outputs" / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    latest = cfg.sources.latest
    raw = ROOT / "data" / "raw"

    facts = build_facts(cfg, root)
    rates = ecb_rates(raw)
    with open(ROOT / "config" / "kpis.yaml", encoding="utf-8") as f:
        kpis = yaml.safe_load(f)
    one_offs = pd.read_csv(ROOT / "data" / "manual" / "one_offs.csv", dtype={"page": str})
    urls = pd.read_csv(ROOT / "data" / "manual" / "report_urls.csv", dtype=str, keep_default_na=False)
    manifest = read_manifest(raw)
    man = manifest.merge(urls, how="left", on=["bank_id", "doc_type", "period"])
    marks = dict(zip(man["sha256"], man["decimal_mark"].fillna(""), strict=True))
    oprov = one_off_provenance(one_offs, raw / "report_text", marks)
    failed = set(oprov.loc[~oprov["passed"].astype(bool), "note"].str.extract(r"one_off (\d+)")[0].astype(int))
    kept_offs = one_offs.drop(index=sorted(failed))
    kpi = compute_kpis(facts, kpis, kept_offs, rates)
    kpi = kpi[kpi["date"] <= latest]
    write_csv(kpi, tables / "kpi.csv")
    _, prov = report_p3_facts(cfg)
    checks = run_checks(facts, cfg, pd.concat([prov, oprov], ignore_index=True))
    write_csv(checks, tables / "checks.csv")
    print(f"facts {len(facts)} rows, kpi {len(kpi)} rows, checks {len(checks)} rows", flush=True)

    universe = read_universe(ROOT)
    peers = peer_groups(kpi, facts, cfg)
    write_csv(peers, tables / "peers.csv")
    bench = benchmark(kpi, peers, universe, cfg)
    write_csv(bench, tables / "bench.csv")
    print(f"peers {len(peers)} rows, bench {len(bench)} rows", flush=True)

    gaps = size_gaps(bench, kpi, facts, rates, cfg)
    write_csv(gaps, tables / "gaps.csv")
    write_csv(joint_table(gaps, bench, kpi, facts, rates, cfg), tables / "gaps_joint.csv")
    write_csv(gaps_range(gaps), tables / "gaps_range.csv")
    print(f"gaps {len(gaps)} rows", flush=True)

    drivers = decompose(kpi, facts, peers, cfg)
    write_csv(drivers, tables / "drivers.csv")
    yoy = year_on_year(kpi, facts, cfg)
    write_csv(yoy, tables / "yoy.csv")
    print(f"drivers {len(drivers)} rows, yoy {len(yoy)} rows", flush=True)

    prices = val.ptbv(facts, load_prices(raw), rates, universe)
    frame = val.fit_frame(prices, kpi, universe, cfg)
    params = {"dependent": "ptbv", "regressors": ["rote", "spread"], "growth": cfg.valuation.growth}
    fits, specs = [], []
    for year in val.YEARS:
        fit = val.fit_year(frame[frame["year"] == year])
        fits.append(fit)
        specs.append(val.spec_row(f"fit_year_{year}", "yearly OLS, HC3", {**params, "year": year}, fit))
        (figures / f"valuation_{year}.png").write_bytes(val.figure(frame[frame["year"] == year], fit))
    pooled = val.fit_pooled(frame)
    specs.append(val.spec_row("fit_pooled", "pooled OLS, year dummies, clustered by bank", params, pooled))
    stable = val.fit_stability(frame)
    specs.append(val.spec_row("fit_stability", "pooled OLS, year dummies, rote x year, clustered by bank, Wald F", params,
                              stable))
    write_csv(pd.DataFrame([stable])[val.STABILITY_COLUMNS], tables / "valuation_stability.csv")
    write_csv(val.spec_log(specs), tables / "spec_log.csv")
    fits_table = pd.DataFrame(fits)[val.FITS_COLUMNS]
    write_csv(fits_table, tables / "valuation_fits.csv")
    joint = pd.read_csv(tables / "gaps_joint.csv")
    valuation = val.uplift(joint, fits_table, pooled, prices)
    write_csv(valuation, tables / "valuation.csv")
    print(f"valuation {len(frame)} rows", flush=True)

    tree = compute_kpis(facts, {"kpis": TREE_SPEC["kpis"] + val.TE_CLOSE["kpis"]}, kept_offs, rates)
    write_csv(source_table(facts, kept_offs, entries_with_marks(ROOT), manifest, valuation, universe),
              tables / "lineage.csv")
    write_csv(derived_table(kpi, tree, gaps, drivers, valuation, facts, universe), tables / "lineage_derived.csv")
    publish(root, latest)
    write_csv(answers(root), tables / "answers.csv")
    print("profiles, league tables and answers written", flush=True)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="bpb", description="Bank Performance Benchmarking")
    commands = ap.add_subparsers(dest="command", required=True)
    b = commands.add_parser("build", help="rebuild every output from raw files")
    b.add_argument("--root", type=Path, default=ROOT, help="folder to write outputs/ and data/processed/ under")
    t = commands.add_parser("trace", help="print the chain behind a figure")
    t.add_argument("lineage_id")
    t.add_argument("--root", type=Path, default=ROOT, help="folder holding outputs/")
    k = commands.add_parser("bank", help="build one bank profile")
    k.add_argument("bank_id")
    k.add_argument("--root", type=Path, default=ROOT, help="folder holding outputs/")
    args = ap.parse_args(argv)
    if args.command == "build":
        build(args.root)
    elif args.command == "trace":
        from bpb.lineage import trace, trace_text

        frame = trace(args.lineage_id, args.root)
        print(trace_text(frame))
        return 0 if not frame.empty else 1
    else:
        from bpb.config import load_config
        from bpb.report import build_profile, render_png

        pdf = build_profile(args.bank_id, load_config(ROOT / "config.toml").sources.latest, args.root,
                            args.root / "outputs" / "reports")
        render_png(pdf, args.root / "outputs" / "figures" / f"{pdf.stem}.png")
        print(pdf)
    return 0
