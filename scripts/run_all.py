"""Regenerates every output built so far from committed raw and manual files (no network).

Section 3: data/processed/facts.parquet (eba, report and p3 rows), outputs/tables/kpi.csv (every bank, 2021-12-31 to
2026-06-30, reported and underlying) and outputs/tables/checks.csv (checks 1 to 9; check 9 on EBA rows; check 1 also
on one_offs.csv rows, whose failures are left out of the underlying basis).
usage: python scripts/run_all.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bpb.checks import one_off_provenance, run_checks
from bpb.config import load_config
from bpb.fx import ecb_rates
from bpb.ingest import build_facts, read_manifest, report_p3_facts
from bpb.kpi import compute_kpis
from bpb.tables import write_csv

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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
