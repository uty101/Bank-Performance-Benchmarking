"""Step 1.7: merger materiality (Convention 4.10). No network; prints the table for the review file.

ratio = target_total_assets in EUR / the acquirer's EBA total_assets at the last EBA reference date strictly
before completion. A non-EUR target is converted with bpb/fx.py at the balance sheet rate of that reference date.
break = ratio > [merger] merger_materiality. A blank ratio carries a note saying why.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bpb.config import load_config
from bpb.fx import ecb_rates, to_eur
from bpb.ingest import eba_facts, read_source_map


def materiality(cfg) -> pd.DataFrame:
    root = cfg.root
    m = pd.read_csv(root / "data" / "manual" / "mergers.csv", dtype={"target_ccy": str})
    facts, _ = eba_facts(cfg)
    ta = facts[facts["field"] == "total_assets"]
    rates = ecb_rates(root / "data" / "raw")
    uk = set(read_source_map(root)["bank_groups"]["uk"])
    rows = []
    for r in m.itertuples(index=False):
        out = {"acquirer_id": r.acquirer_id, "target_name": r.target_name, "completion_date": r.completion_date,
               "target_total_assets": r.target_total_assets, "target_ccy": r.target_ccy, "ref_date": "",
               "acquirer_total_assets_eur": float("nan"), "target_total_assets_eur": float("nan"),
               "ratio": float("nan"), "break": "", "note": ""}
        if r.acquirer_id in uk:
            out["note"] = "UK acquirer: total assets from reports, entered in Section 3"
            rows.append(out)
            continue
        a = ta[(ta["bank_id"] == r.acquirer_id) & (ta["ref_date"] < r.completion_date)]
        if a.empty:
            out["note"] = "no EBA reference date before completion"
            rows.append(out)
            continue
        last = a.sort_values("ref_date").iloc[-1]
        out["ref_date"], out["acquirer_total_assets_eur"] = last["ref_date"], last["value"]
        if pd.isna(r.target_total_assets):
            out["note"] = "target total assets not found on an acquirer or target page"
        elif r.target_ccy != "EUR" and r.target_ccy not in cfg.fx.currencies:
            out["note"] = f"{r.target_ccy} is not in [fx] currencies"
        else:
            t_eur = to_eur(float(r.target_total_assets), r.target_ccy, last["ref_date"], "bs", rates, None)
            out["target_total_assets_eur"] = t_eur
            out["ratio"] = t_eur / last["value"]
            out["break"] = str(out["ratio"] > cfg.merger.merger_materiality)
        rows.append(out)
    return pd.DataFrame(rows)


def main() -> int:
    pd.set_option("display.width", 300)
    pd.set_option("display.max_colwidth", 60)
    cfg = load_config(Path(__file__).resolve().parents[1] / "config.toml")
    print(materiality(cfg).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
