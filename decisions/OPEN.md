# Open decisions

Items are appended as found. Each names where it arises and gives 2 concrete options. None is decided by Claude Code; the reviewer decides in the next instruction file.

---

## OPEN-01: where the EBA download URLs are recorded before step 1.1 downloads them

**DECIDED (see decisions/section_0_review.md):** option (a).

Raised in session 0 (step 1.1). Section 3.2 fixes the 2024 and 2025 URLs and says the 2021 to 2023 URLs "are read from each year's release page ... and recorded in the manifest". The manifest is written by the download, so the script needs the URLs from somewhere before it runs, and no path is fixed.

- (a) A committed `data/manual/eba_urls.csv` (release, file, url, release_page_url) written in session 1 from the release pages; `scripts/pull_data.py --stage eba` reads it.
- (b) A literal URL table inside `scripts/pull_data.py`, one entry per release and file, each with a comment citing its release page.

## OPEN-02: step 1.1 filters EBA CSVs to universe banks before step 1.2 has filled any LEI

**DECIDED (see decisions/section_0_review.md):** option (b), with a change.

Raised in session 0 (steps 1.1, 1.2). Correction 8 filters oversized CSVs to universe-bank rows, which needs LEIs; step 1.2 fills the LEIs afterwards from the 2025 release. The unfiltered originals also need a place to sit between the 2 steps, and no gitignored path for them is fixed.

- (a) Step 1.1 downloads the originals into a gitignored `data/eba_download/` (added to `.gitignore`) and hashes them; step 1.2 fills LEIs; the filter and the committed `data/raw/eba/` files are written after 1.2, still within Section 1, committed as part of step 1.1's work in a second commit `step 1.1: filter EBA files to universe LEIs`.
- (b) Step 1.1 filters on the country code column instead, keeping every bank from the universe countries, and step 1.2 matches LEIs within that filtered set. The 50 MB limit is then checked on the country-filtered files.

## OPEN-03: report-family values for EU banks at 2024-12-31 and 2025-06-30

**DECIDED (see decisions/section_0_review.md):** option (a).

Raised in session 0 (steps 2.3, 2.5; `config/source_map.yaml`). Section 3.3 allows `report` for EU banks only at 2025-06-30 ("seam test only"), 2025-12-31 and 2026-06-30. But Convention 4.4 needs both ends of an average from one family, so FY2025 averages need a `report` balance at 2024-12-31, which step 2.3 enters as comparatives. Convention 4.3 needs H1 2025 from `report` for the rolling 12 months at 2026-06-30, which makes the 2025-06-30 report rows more than seam inputs.

- (a) The source map adds a third role, `bridge_input`: `report` rows for EU banks at 2024-12-31 and 2025-06-30 may be used as opening balances and rolling components for report-family KPIs at 2025-12-31 and 2026-06-30. The KPI value at 2025-06-30 itself still comes from `eba`.
- (b) Strict reading: these rows are seam-only. EU KPIs at 2025-12-31 with an averaged denominator, and every EU P&L KPI at 2026-06-30, are blank with status `missing_input`.

## OPEN-04: which family fills capital and liquidity fields in the bridge and for UK banks

**DECIDED (see decisions/section_0_review.md):** option (b).

Raised in session 0 (`config/source_map.yaml`, steps 2.1, 2.3, 3.1). Correction 1 puts bridge capital in `p3`, and check 7 compares cet1, rwa and leverage_exposure, so those (and tier1) are written as `p3` for EU bridge dates. Still undecided: (i) at1_instruments, intangibles_deduction, lcr and nsfr for EU bridge dates; (ii) every capital field for UK banks, where Section 3.3 says "bank reports for UK banks for every date" but Convention 4.5 defines a bank's Pillar 3 report as `p3`.

- (a) All of cet1, tier1, rwa, leverage_exposure, at1_instruments, intangibles_deduction, lcr and nsfr are `p3` for EU bridge dates and for UK banks at every date. Every other UK field is `report`.
- (b) For EU bridge dates, only cet1, tier1, rwa and leverage_exposure are `p3`; at1_instruments, intangibles_deduction, lcr and nsfr are `report`. Every UK field is `report`, with a Pillar 3 PDF treated as a report document (doc_type `pillar3`).

## OPEN-05: lcr and nsfr for EU banks at EBA-period dates

**DECIDED (see decisions/section_0_review.md):** option (a).

Raised in session 0 (`config/source_map.yaml`, steps 1.5, 2.3). Section 5.1 says lcr and nsfr come from the `p3` and `report` families only, but no step enters them for EU banks before 2025-06-30.

- (a) The lcr and nsfr KPIs stay blank for EU banks at every date up to 2025-06-30, with status `missing_input`.
- (b) Step 3.2's report entry scope is widened to include lcr and nsfr for EU banks at every 31 Dec from 2021-12-31 and every 30 Jun from 2022-06-30, from Pillar 3 reports.

## OPEN-06: components of the income identity (check 3) for EBA rows

**DECIDED (see decisions/section_0_review.md):** option (a).

Raised in session 0 (`config/fields.yaml`, step 1.6). Check 3 sums nii, dividend_income, net_fees and "other components listed in fields.yaml", but Section 5.1 lists no component between net fees and total operating income. Since `other_income` is defined as the residual, using it would make the check pass by construction.

- (a) Step 1.2 maps the remaining EBA P&L lines between net fees and TOTAL OPERATING INCOME, NET (gains or losses on financial assets and liabilities, trading, hedge accounting, exchange differences, other operating income and expenses, as labelled in `TR_Metadata.xlsx`) as extra fields. They are listed in `fields.yaml` under `income_components_other` and used by check 3 only.
- (b) Check 3 is run on report rows only, using the components each bank's income statement shows. For EBA rows it writes no row, until a later instruction says otherwise.

## OPEN-07: check 4 needs a reported CET1 ratio, which is not a field

**DECIDED (see decisions/section_0_review.md):** option (a).

Raised in session 0 (step 1.6). Check 4 compares a reported CET1 ratio with cet1 / rwa "where a reported ratio exists". Section 5.1 has no field for the reported ratio.

- (a) Add a field `cet1_ratio_reported` (kind ratio), mapped from the EBA capital template in step 1.2 and entered from KM1 or reports in Sections 2 and 3. Check 4 runs wherever it exists.
- (b) No field is added and check 4 writes no rows until a later instruction adds one.

## OPEN-08: `peers.features` has no FX rates argument

**DECIDED (see decisions/section_0_review.md):** option (a).

Raised in session 0 (step 4.1). The first feature is ln(total_assets in EUR), but `features(kpi, facts, year)` receives no rates.

- (a) The signature becomes `features(kpi, facts, year, rates)`, and `peer_groups(kpi, facts, cfg)` reads the rates itself with `fx.ecb_rates(Path("data/raw"))`.
- (b) The signature is unchanged; `build_facts` adds a `value_eur` column for total_assets (31 Dec ECB rate) that `features` reads. This changes the FACTS schema.

## OPEN-09: `benchmark` needs each bank's market, which PEERS does not carry

**DECIDED (see decisions/section_0_review.md):** option (a).

Raised in session 0 (step 4.2). The `market` peer group comes from `universe.csv`, but `benchmark(kpi, peers, cfg)` receives no universe and the PEERS schema has no market column.

- (a) The signature becomes `benchmark(kpi, peers, universe, cfg)`.
- (b) `benchmark` reads `data/manual/universe.csv` through a path in `cfg` (a new key `[paths] universe`).

## OPEN-10: `valuation.uplift` needs the joint RoTE gap and the pooled fit

**DECIDED (see decisions/section_0_review.md):** option (b).

Raised in session 0 (step 5.3). The uplift uses the joint RoTE gap (GAPS_JOINT `joint_rote_pts`), and its blanking depends on the pooled β interval (`fit_pooled`). `uplift(gaps, fits, ptbv)` names neither.

- (a) `gaps` is the GAPS_JOINT frame, and `fits` is VALUATION_FITS with the pooled fit as a row whose `year` is blank and whose `status` holds `beta_not_significant` where it applies.
- (b) The signature becomes `uplift(gaps_joint, fits, pooled, ptbv)`, with `pooled` the dict returned by `fit_pooled`.

## OPEN-11: how UK LEIs are fetched from GLEIF

**DECIDED (see decisions/section_0_review.md):** option (a).

Raised in session 0 (step 3.1). Rule 8 allows network access only in `scripts/pull_data.py` and `scripts/fetch_reports.py`, and no GLEIF stage or stored file is fixed.

- (a) A stage `scripts/pull_data.py --stage gleif` queries the GLEIF API by name for each UK bank, writes `data/raw/gleif/{bank_id}.json` and its manifest row, and fills `lei` from those files.
- (b) The LEIs are entered by hand into `universe.csv` from the GLEIF website, with each record's URL printed in the review file.

## OPEN-12: how `tests/fixtures/hand_check.xlsx` formula results are evaluated

**DECIDED (see decisions/section_0_review.md):** option (b), using `pycel`.

Raised in session 0 (step 4.3). The workbook must hold spreadsheet formulas, not pasted values. openpyxl writes formulas without cached results, so a test reading it with `data_only=True` sees blanks.

- (a) The workbook is written with openpyxl formulas, then recalculated once with LibreOffice headless (`soffice --convert-to xlsx`) so cached values are stored. The committed file holds both, and the test reads the cached values.
- (b) Add the dev dependency `formulas` (or `pycel`). The test evaluates the formulas itself from the committed workbook.

## OPEN-13: output file paths not fixed

**DECIDED (see decisions/section_0_review.md):** option (a).

Raised in session 0 (steps 4.4, 6.1). Section 5.9 fixes league table CSV paths but not:

- the PDF profile name (`outputs/reports/` exists);
- the PNG renders used as review evidence;
- the per-KPI HTML pages;
- the strip chart and waterfall images.

- (a) `outputs/reports/{bank_id}_{date}.pdf`, `outputs/figures/{bank_id}_{date}.png` (page render), `outputs/tables/league_{kpi}.html` (all groups and dates on one page), charts drawn in memory and not saved separately.
- (b) `outputs/reports/profile_{bank_id}.pdf` (latest date only), `review/figures/section_N/{bank_id}.png`, `outputs/html/league_{kpi}.html`, charts saved under `outputs/figures/{chart}_{bank_id}_{date}.png`.

## OPEN-14: tests on outputs versus rule 7

**DECIDED (see decisions/section_0_review.md):** option (a).

Raised in session 0 (steps 6.2, 6.4). The trace test samples numbers "from the PDFs' source tables" and the README test compares README tables with "the CSVs". Rule 7 says no test may depend on `outputs/` already existing.

- (a) Both tests run `bpb build` into a pytest `tmp_path` from committed raw and manual files, then test against what that build wrote.
- (b) An explicit exception to rule 7 for these 2 tests only: they read the committed `outputs/tables/` CSVs, and step 6.3's clean `git status` check ensures those match a fresh build.

## OPEN-15: test inputs the kickoff leaves unfixed

**DECIDED (see decisions/section_0_review.md):** option (a).

Raised in session 0 (PLAN.md, several steps). Unfixed inputs include:

- the 3 dates of the FX round trip test (1.4);
- the hand example for the rolling 12 months test (1.5);
- the synthetic EBA frame (1.3);
- the date, peer groups and bases covered by the hand check (4.3);
- the synthetic values for the verdict rules (4.2);
- the known CoE and dataset size for the valuation test (5.3).

- (a) The reviewer fixes each in the instruction file of the section that uses it.
- (b) The session picks them, writes them at the top of the test file as named constants, and prints them in the review file for approval. Changing them later counts as a test change under rule 5.

## OPEN-16: column position of `lei` in `universe.csv`

**DECIDED (see decisions/section_0_review.md):** option (b).

Raised in session 0 (step 0.0). Section 3.1 gives the column order without `lei` and says the file is written "with `lei` blank". Session 0 wrote `lei` as the last column.

- (a) Keep `lei` as the last column.
- (b) Move `lei` to the second column, after `bank_id`, matching FACTS (bank_id, lei, ...).
