"""Builds tests/fixtures/hand_check.xlsx (instruction 04 B.4, instruction 04b step 4.3): 1 sheet per hand check bank at
2025-12-31, cluster group, underlying basis. Inputs are typed values with their lineage IDs in the next cell; every sized
value is a spreadsheet formula. A bank with no sized gap at that cell uses its universe group, noted on the sheet.
usage: python scripts/build_hand_check.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import yaml
from openpyxl import Workbook

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bpb.benchmark import benchmark
from bpb.config import load_config
from bpb.fx import ecb_rates, period_start, rate
from bpb.gaps import TaxRates, average_te, bank_inputs, joint_table, size_gaps
from bpb.ingest import build_facts, read_universe
from bpb.kpi import _join, compute_kpis
from bpb.lineage import lineage_id
from bpb.peers import cluster_year, peer_groups

DATE = "2025-12-31"  # B.4
GROUP = "cluster"
FALLBACK_GROUP = "universe"
BASIS = "underlying"
FIXTURE = Path("tests") / "fixtures" / "hand_check.xlsx"


def tables(cfg) -> dict:
    """Every table the hand check needs, from raw and manual files, benchmarked at DATE only: each bootstrap has its
    own generator, so the rows equal those of the full run."""
    root = cfg.root
    facts = build_facts(cfg)
    rates = ecb_rates(root / "data" / "raw")
    with open(root / "config" / "kpis.yaml", encoding="utf-8") as f:
        kpis = yaml.safe_load(f)
    one_offs = pd.read_csv(root / "data" / "manual" / "one_offs.csv", dtype={"page": str})
    kpi = compute_kpis(facts, kpis, one_offs, rates)
    peers = peer_groups(kpi, facts, cfg)
    universe = read_universe(root)
    bench = benchmark(kpi[kpi["date"] == DATE], peers, universe, cfg)
    gaps = size_gaps(bench, kpi, facts, rates, cfg)
    return {"facts": facts, "rates": rates, "kpi": kpi, "peers": peers, "universe": universe, "bench": bench,
            "gaps": gaps, "joint": joint_table(gaps, bench, kpi, facts, rates, cfg)}


def scope_group(gaps: pd.DataFrame, bank: str) -> str:
    cell = gaps[(gaps["bank_id"] == bank) & (gaps["group"] == GROUP) & (gaps["basis"] == BASIS)]
    return GROUP if cell["delta_pi_lc"].notna().any() else FALLBACK_GROUP


def _target_lineage(t: dict, bank: str, name: str, group: str) -> str:
    k = t["kpi"]
    k = k[(k["date"] == DATE) & (k["kpi"] == name) & (k["basis"] == BASIS) & k["value"].notna() & (k["bank_id"] != bank)]
    if group == GROUP:
        p = t["peers"]
        p = p[p["year"] == cluster_year(DATE)].set_index("bank_id")["cluster"]
        k = k[k["bank_id"].map(p) == p[bank]]
    return _join(k["inputs_lineage"])


def write_sheet(wb: Workbook, bank: str, t: dict, cfg) -> None:
    ws = wb.create_sheet(bank)
    group = scope_group(t["gaps"], bank)
    b = bank_inputs(t["kpi"], t["universe"], average_te(t["facts"], t["rates"]))[(DATE, bank, BASIS)]
    bench = t["bench"]
    rows = bench[(bench["bank_id"] == bank) & (bench["group"] == group) & (bench["basis"] == BASIS)].set_index("kpi")
    cell = t["gaps"][(t["gaps"]["bank_id"] == bank) & (t["gaps"]["group"] == group) & (t["gaps"]["basis"] == BASIS)]
    sized = cell[cell["delta_pi_lc"].notna()]["gap"].tolist()
    tax_rate, _, tax_lineage = TaxRates(t["facts"], t["rates"], cfg).get(bank, DATE, BASIS)
    ccy = b["ccy"]["cost_income"]
    note = "" if group == GROUP else "no sized gap in the cluster group: the universe group is used (B.4)"
    ws.append(["bank", bank])
    ws.append(["date", DATE])
    ws.append(["group", group, note])
    ws.append(["basis", BASIS])
    ws.append(["currency", ccy])
    ws.append([])
    ws.append(["input", "value", "lineage"])
    at: dict[str, str] = {}

    def add(label, value, third=""):
        ws.append([label, value, third])
        at[label] = f"B{ws.max_row}"

    lin = b["lineage"]
    add("I", float(b["I"]), lin["cost_income"])
    add("F", float(b["F"]), lin["fee_share"])
    add("O", float(b["O"]), _join([lin["cost_income"], lin["fee_share"], lin["nim"]]))
    add("C", float(b["C"]), lin["cost_income"])
    add("LLP", float(b["LLP"]), lin["risk_adj_nim"])
    add("IEA", float(b["IEA"]), lin["risk_adj_nim"])
    add("TE", float(b["TE"]), lin["te"])
    add("t", float(tax_rate), tax_lineage)
    for name in cfg.gaps.sized:
        add(f"target_{name}", float(rows.loc[name, "target"]), _target_lineage(t, bank, name, group))
    if ccy != "EUR":
        add("fx_period_mean", rate(ccy, DATE, "pl", t["rates"], period_start(DATE, rolling=False)),
            lineage_id(ccy, DATE, "fx_period_mean", "ecb", f"data/raw/fx/{ccy}.csv"))
    ws.append([])
    ws.append(["formula", "result", "gap sized"])
    a = at
    add("NII", f"={a['I']}-{a['F']}-{a['O']}")
    add("cost_income", f"={a['C']}/{a['I']}")
    add("risk_adj_nim", f"=({a['NII']}-{a['LLP']})/{a['IEA']}")
    pi = {"cost_income": "=({v}-{s})*{I}".format(v=a["cost_income"], s=a["target_cost_income"], I=a["I"]),
          "risk_adj_nim": "=({s}-{v})*{E}".format(v=a["risk_adj_nim"], s=a["target_risk_adj_nim"], E=a["IEA"])}
    fx_div = f"/{a['fx_period_mean']}" if ccy != "EUR" else ""
    for name in cfg.gaps.sized:
        if name in sized:
            add(f"delta_pi_lc|{name}", pi[name], "sized")
            add(f"delta_pi_eur|{name}", f"={a[f'delta_pi_lc|{name}']}{fx_div}", "sized")
            add(f"delta_rote_pts|{name}", f"={a[f'delta_pi_lc|{name}']}*(1-{a['t']})/{a['TE']}*100", "sized")
    # kickoff Section 5.6 with O = other_income, the level rule of instruction 04b B.3 for drivers not sized, and F' = F
    # always (instruction 05 A.1 item 1); the margin gap closes through NII, with LLP' = LLP (instruction 06c B.1 item 5)
    d = f"{a['target_risk_adj_nim']}*{a['IEA']}-({a['NII']}-{a['LLP']})"
    add("NII_prime", f"={a['NII']}+{d}" if "risk_adj_nim" in sized else f"={a['NII']}")
    add("I_prime", f"={a['NII_prime']}+{a['F']}+{a['O']}")
    add("C_prime", f"={a['target_cost_income']}*{a['I_prime']}" if "cost_income" in sized else f"={a['C']}")
    add("LLP_prime", f"={a['LLP']}")
    add("joint_delta_pi_lc", f"=({a['I_prime']}-{a['C_prime']}-{a['LLP_prime']})-({a['I']}-{a['C']}-{a['LLP']})")
    add("joint_delta_pi_eur", f"={a['joint_delta_pi_lc']}{fx_div}")
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 22


def main() -> int:
    cfg = load_config(Path(__file__).resolve().parents[1] / "config.toml")
    t = tables(cfg)
    wb = Workbook()
    wb.remove(wb.active)
    for bank in cfg.gaps.hand_check_banks:
        write_sheet(wb, bank, t, cfg)
        print(bank, scope_group(t["gaps"], bank))
    wb.save(cfg.root / FIXTURE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
