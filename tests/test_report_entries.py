"""Step 2.1 tests (instruction 02 Section C): load_p3 and load_report_entries on synthetic entries."""

import pandas as pd

from bpb.ingest import ENTRY_COLUMNS, ROOT, load_p3, load_report_entries, read_universe

SHA = "a" * 64


def _entry(field: str, printed: str, value: str = "", doc_type: str = "pillar3", unit_scale: str = "1000000",
           snippet: str | None = None, ref_date: str = "2025-12-31", page: str = "5") -> dict:
    return {"bank_id": "ISP", "ref_date": ref_date, "field": field, "value_as_printed": printed,
            "unit_scale": unit_scale, "value": value, "ccy": "EUR", "period_months": "", "doc_type": doc_type,
            "report_sha256": SHA, "page": page, "snippet": snippet if snippet is not None else f"line {printed}",
            "entered_utc": "2026-11-02T00:00:00Z"}


def _write(tmp_path, rows: list[dict]):
    manual, raw = tmp_path / "manual", tmp_path / "raw"
    manual.mkdir()
    raw.mkdir()
    path = manual / "report_entries.csv"
    pd.DataFrame(rows, columns=ENTRY_COLUMNS).to_csv(path, index=False)
    manifest = pd.DataFrame([{"bank_id": "ISP", "doc_type": "pillar3", "period": "2025-12-31", "url": "u",
                              "sha256": SHA, "bytes": "1", "pages": "9", "downloaded_utc": "t"}])
    manifest.to_csv(raw / "report_manifest.csv", index=False)
    return path, raw, manifest.astype(str)


def test_family_from_source_map(tmp_path):
    path, raw, manifest = _write(tmp_path, [_entry("cet1", "48,123"), _entry("intangibles_deduction", "(9,876)")])
    universe = read_universe(ROOT)
    p3 = load_p3(raw, universe)
    rep = load_report_entries(path, manifest)
    assert list(p3["field"]) == ["cet1"] and set(p3["family"]) == {"p3"}
    assert list(rep["field"]) == ["intangibles_deduction"] and set(rep["family"]) == {"report"}
    assert rep["value"].iloc[0] == 9_876_000_000  # a deduction is stored positive (Convention 4.2)


def test_component_sum(tmp_path):
    comps = [_entry("loans_customers_gross", p, snippet=f"component {k}/4 row {r}: {p}")
             for k, (r, p) in enumerate([("030", "1,000"), ("050", "200"), ("060", "30"), ("080", "4")], start=1)]
    path, _, manifest = _write(tmp_path, comps)
    rep = load_report_entries(path, manifest)
    assert len(rep) == 1 and rep["value"].iloc[0] == 1_234_000_000
    assert rep["status"].iloc[0] == "ok"

    (tmp_path / "missing_one").mkdir()
    path2, _, manifest2 = _write(tmp_path / "missing_one", comps[:3])
    rep2 = load_report_entries(path2, manifest2)
    assert rep2[rep2["field"] == "loans_customers_gross"].empty


def test_scale_and_sign(tmp_path):
    rows = [_entry("admin_expenses", "(1,234.5)", doc_type="annual"),
            _entry("depreciation", "(1,234.5)", value="1234500000", doc_type="annual")]
    path, _, manifest = _write(tmp_path, rows)
    rep = load_report_entries(path, manifest).set_index("field")
    assert rep.loc["admin_expenses", "value"] == 1_234_500_000
    assert rep.loc["depreciation", "value"] == 1_234_500_000
    assert rep.loc["admin_expenses", "unit_scale"] == 1e6
