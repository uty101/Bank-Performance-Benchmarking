"""Step 1.3 tests (instruction 01 Section C, amended by instruction 01b Section C)."""

import hashlib
import math
from pathlib import Path

import pandas as pd
import pytest
import yaml

from bpb.ingest import (
    FACTS_COLUMNS,
    apply_source_map,
    load_eba,
    read_eba_map,
    read_universe,
)
from bpb.lineage import lineage_id

ROOT = Path(__file__).resolve().parents[1]
TR_OTH_2025 = ["LEI_Code", "NSA", "Period", "Item", "Label", "ASSETS_FV", "ASSETS_Stages", "Exposure",
               "Financial_instruments", "Amount", "Fin_end_year", "n_quarters", "Row", "Column", "Sheet"]
TR_CRE_2025 = ["LEI_Code", "NSA", "Period", "Item", "Label", "Portfolio", "Country", "Country_rank", "Exposure",
               "Status", "Perf_Status", "NACE_codes", "Amount", "Row", "Column", "Sheet"]
LEI_A, LEI_B = "TESTLEI000000000000A", "TESTLEI000000000000B"
ISP = "2W8N8UU78PMDQKZENC08"


def _write(df: pd.DataFrame, raw_root: Path, year: int, name: str) -> None:
    path = raw_root / "eba" / str(year) / f"{name}.csv.gz"
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, compression={"method": "gzip", "mtime": 0}, encoding="latin-1")


def _universe() -> pd.DataFrame:
    return pd.DataFrame({"bank_id": ["TA", "TB"], "lei": [LEI_A, LEI_B], "country": ["IT", "SE"]})


def _map(rows: list[tuple[str, str, str]]) -> pd.DataFrame:
    return pd.DataFrame([{"field": f, "item": i, "template": "T", "label": lab, "dim_filter": "{}"}
                         for f, i, lab in rows])


def test_load_eba_synthetic(tmp_path):
    amounts = {"I1": 1.5, "I2": 2.0, "I3": 3.0, "I4": 0.1375}
    rows = []
    for lei in (LEI_A, LEI_B):
        for period, nq in (("202312", "4"), ("202406", "2")):
            for item, amt in amounts.items():
                rows.append({"LEI_Code": lei, "NSA": "IT", "Period": period, "Item": item, "Label": f"label {item}",
                             "ASSETS_FV": "0", "ASSETS_Stages": "0", "Exposure": "0", "Financial_instruments": "0",
                             "Amount": str(amt), "Fin_end_year": "0", "n_quarters": nq, "Row": "1", "Column": "1",
                             "Sheet": "S"})
    frame = pd.DataFrame(rows, columns=TR_OTH_2025)
    assert len(frame) == 16  # instruction 01's 12 rows plus I4 at 2 banks x 2 dates (instruction 01b)
    _write(frame, tmp_path, 2025, "tr_oth")
    emap = _map([("total_assets", "I1", "Total Assets"), ("interest_income", "I2", "Interest income"),
                 ("cet1_ratio_reported", "I4", "COMMON EQUITY TIER 1 CAPITAL RATIO (transitional period)")])
    facts = load_eba(2025, tmp_path, emap, _universe())

    assert list(facts.columns) == FACTS_COLUMNS
    assert len(facts) == 12  # 3 mapped items x 2 banks x 2 dates
    assert "I3" not in set(facts["locator"].str.split("@").str[0])
    ta = facts[facts["field"] == "total_assets"]
    assert (ta["value"] == 1_500_000).all() and (ta["ccy"] == "EUR").all() and (ta["unit_scale"] == 1e6).all()
    ii = facts[facts["field"] == "interest_income"].set_index(["bank_id", "ref_date"])
    assert (ii["value"] == 2_000_000).all()
    assert ii.loc[("TA", "2023-12-31"), "period_months"] == 12 and ii.loc[("TA", "2024-06-30"), "period_months"] == 6
    cr = facts[facts["field"] == "cet1_ratio_reported"]
    assert (cr["value"] == 0.1375).all() and (cr["unit_scale"] == 1).all() and (cr["ccy"] == "").all()
    assert set(facts["ref_date"]) == {"2023-12-31", "2024-06-30"}
    assert set(facts["family"]) == {"eba"} and set(facts["status"]) == {"ok"}
    for r in facts.itertuples():
        assert r.lineage_id == lineage_id(r.bank_id, r.ref_date, r.field, r.family, r.locator)


def test_source_map_rejects():
    with open(ROOT / "config" / "source_map.yaml", encoding="utf-8") as f:
        smap = yaml.safe_load(f)
    base = {"lei": "X", "field": "total_assets", "value": 1.0, "ccy": "EUR", "unit_scale": 1.0, "period_months": pd.NA,
                "locator": "loc", "lineage_id": "x", "status": "ok"}
    facts = pd.DataFrame([
        {**base, "bank_id": "ISP", "ref_date": "2023-12-31", "family": "report"},
        {**base, "bank_id": "ISP", "ref_date": "2023-12-31", "family": "eba"},
    ])[FACTS_COLUMNS]
    kept, rejected = apply_source_map(facts, smap)
    assert list(rejected["family"]) == ["report"] and list(rejected["bank_id"]) == ["ISP"]
    assert list(kept["family"]) == ["eba"]


def test_lineage_stable():
    args = ["ISP", "2024-12-31", "total_assets", "eba", "2521010@2025"]
    a, b = lineage_id(*args), lineage_id(*args)
    assert a == b and len(a) == 12 and all(c in "0123456789abcdef" for c in a)
    assert a == hashlib.sha256("|".join(args).encode()).hexdigest()[:12]
    for i in range(5):
        changed = list(args)
        changed[i] = changed[i] + "x"
        assert lineage_id(*changed) != a


def test_unnamed_dims_zero(tmp_path):
    rows = [{"LEI_Code": LEI_A, "NSA": "IT", "Period": "202412", "Item": "X1", "Label": "loans",
             "Portfolio": "0", "Country": "0", "Country_rank": "0", "Exposure": "0", "Status": "0",
             "Perf_Status": ps, "NACE_codes": "0", "Amount": amt, "Row": "1", "Column": "1", "Sheet": "NPE"}
            for ps, amt in (("0", "10"), ("1", "4"), ("2", "6"))]
    _write(pd.DataFrame(rows, columns=TR_CRE_2025), tmp_path, 2025, "tr_cre")
    facts = load_eba(2025, tmp_path, _map([("loans_all", "X1", "loans")]), _universe())
    assert len(facts) == 1 and facts["value"].iloc[0] == 10_000_000


def test_summed_field_real():
    facts = load_eba(2025, ROOT / "data" / "raw", read_eba_map(ROOT, 2025), read_universe(ROOT))
    got = facts[(facts["lei"] == ISP) & (facts["ref_date"] == "2024-12-31")].set_index("field")["value"]
    expected = {  # instruction 01b step 1.3, computed by the reviewer from the raw rows
        "loans_customers_gross": 425_626_292_361.999,
        "loans_customers_allowance": 6_960_860_569,
        "debt_securities": 143_153_074_398,
        "deposits_customers": 445_313_449_876,
    }
    for field, value in expected.items():
        assert math.isclose(got[field], value, rel_tol=1e-9), (field, got[field], value)


def test_summed_field_partial_missing(tmp_path):
    cre = pd.read_csv(ROOT / "data" / "raw" / "eba" / "2025" / "tr_cre.csv.gz", dtype=str, encoding="latin-1",
                      keep_default_na=False)
    cre = cre[cre["LEI_Code"] == ISP]
    drop = ((cre["Item"] == "2520605") & (cre["Period"] == "202412") & (cre["Exposure"] == "301")
            & (cre["Perf_Status"] == "0") & (cre["Status"] == "0"))
    assert drop.sum() == 1
    _write(cre[~drop], tmp_path, 2025, "tr_cre")
    facts = load_eba(2025, tmp_path, read_eba_map(ROOT, 2025), read_universe(ROOT))
    lcg = facts[facts["field"] == "loans_customers_gross"]
    assert "2024-12-31" not in set(lcg["ref_date"])
    assert {"2024-09-30", "2025-03-31", "2025-06-30"} <= set(lcg["ref_date"])


if __name__ == "__main__":
    pytest.main([__file__])
