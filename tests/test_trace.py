"""Step 6.2 tests (instruction 06 B.2, with 06b B.3)."""

import re

import numpy as np
import pandas as pd

from bpb.checks import _read_cache, provenance
from bpb.cli import main
from bpb.config import load_config
from bpb.ingest import ROOT
from bpb.lineage import read_lineage, row_id, trace
from bpb.report import ranked_kpis

SAMPLE = 20  # instruction 06 B.2
NOTE = re.compile(r"^component \d+/\d+: ")  # instruction 06b B.3


def _page(cache: dict, sha: str, page: str) -> str:
    if sha not in cache:
        cache[sha] = _read_cache(ROOT / "data" / "raw" / "report_text", sha)
    return cache[sha][page.rsplit("!", 1)[0] if "!" in page else int(page)]


def test_trace_sample(built):
    cfg = load_config(ROOT / "config.toml")
    kpi = pd.read_csv(built / "outputs" / "tables" / "kpi.csv")
    names = [s["kpi"] for s in ranked_kpis()]
    used = kpi[(kpi["date"] == cfg.sources.latest) & (kpi["basis"] == "underlying") & kpi["kpi"].isin(names)
               & kpi["value"].notna()].sort_values(["bank_id", "kpi"]).reset_index(drop=True)
    picks = used.iloc[np.random.default_rng(cfg.run.seed).choice(len(used), SAMPLE, replace=False)]
    tables = read_lineage(built)
    sources = tables.sources
    pages: dict = {}
    for r in picks.itertuples(index=False):
        frame = trace(row_id("kpi", r.bank_id, r.date, r.kpi, r.basis), built, tables)
        inputs = frame[frame["kind"].isin(["facts", "one_off"])]
        assert not inputs.empty and frame["kind"].iloc[0] == "kpi"
        assert inputs["locator"].notna().all() and (inputs["locator"] != "").all()
        eba = inputs[inputs["family"] == "eba"]
        assert eba["release_year"].notna().all() and eba["item_code"].notna().all()
        report = sources[sources["lineage_id"].isin(inputs.loc[inputs["family"] != "eba", "lineage_id"])]
        for s in report.itertuples(index=False):
            assert NOTE.sub("", s.snippet) in _page(pages, s.sha256, s.page), (s.lineage_id, s.snippet)
        if len(report):
            e = report.rename(columns={"sha256": "report_sha256", "value": "fact_value", "entry_value": "value"})
            e = e.assign(decimal_mark=e["decimal_mark"].fillna("."))
            checked = provenance(e, ROOT / "data" / "raw" / "report_text")
            assert checked["passed"].all(), checked.loc[~checked["passed"], "note"].tolist()


def test_trace_command(built, capsys):
    kpi = pd.read_csv(built / "outputs" / "tables" / "kpi.csv")
    r = kpi[(kpi["bank_id"] == "LLOY") & (kpi["kpi"] == "rote") & (kpi["basis"] == "underlying")].iloc[-1]
    assert main(["trace", row_id("kpi", "LLOY", r["date"], "rote", "underlying"), "--root", str(built)]) == 0
    text = capsys.readouterr().out
    assert "sha256" in text and "snippet" in text
    assert main(["trace", "000000000000", "--root", str(built)]) == 1
