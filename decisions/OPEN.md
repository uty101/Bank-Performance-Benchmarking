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

---

## OPEN-17: Deutsche Bank has no unique name match in the 2025 release

**DECIDED (see decisions/section_1_review.md):** option (a).

Raised in session 1 (step 1.2). "Deutsche Bank" normalises to `deutsche` ("bank" is a listed suffix). No 2025 EU name normalises to exactly `deutsche`, and `deutsche` is contained, as whole words, in 5:

| EBA name (2025 TR_Metadata) | LEI |
|---|---|
| DEUTSCHE APOTHEKER- UND ÄRZTEBANK EG | 5299007S3UH5RKUYDA52 |
| DEUTSCHE BANK AKTIENGESELLSCHAFT | 7LTWFZYICNSX8D621K86 |
| DZ BANK AG Deutsche Zentral-Genossenschaftsbank, Frankfurt am Main | 529900HNOAA1KXQJUQ27 |
| DekaBank Deutsche Girozentrale | 0W2PZJM8XOY22M4GG883 |
| Deutsche Pfandbriefbank AG | DZZ47B9A52ZJ6LT6VV95 |

DBK's `lei` is left blank, so DBK has no EBA rows until this is decided.

- (a) Add a second alias before matching, DBK matched as `Deutsche Bank Aktiengesellschaft`, which matches `DEUTSCHE BANK AKTIENGESELLSCHAFT` (7LTWFZYICNSX8D621K86) exactly.
- (b) The reviewer fixes DBK's LEI in the next instruction file as 7LTWFZYICNSX8D621K86, entered by hand into `universe.csv`.

## OPEN-18: `cet1` has 2 candidate lines in the EBA Capital template

**DECIDED (see decisions/section_1_review.md):** option (a).

Raised in session 1 (step 1.2). Both exist in every release (2025 item codes; earlier releases use the same last 5 digits):

- 2520102 `COMMON EQUITY TIER 1 CAPITAL (net of deductions and after applying transitional adjustments)`
- 2520143 `COMMON EQUITY TIER 1 CAPITAL (fully loaded)`

`cet1` is not mapped, so the cet1_ratio KPI and check 4 are blank until this is decided. `tier1` (2520133, the only Tier 1 line in the Capital template) is transitional.

- (a) Transitional, 2520102 (consistent with tier1 2520133 and rwa).
- (b) Fully loaded, 2520143.

## OPEN-19: `cet1_ratio_reported` has 2 candidate lines (3 in 2025)

**DECIDED (see decisions/section_1_review.md):** option (a).

Raised in session 1 (step 1.2), for check 4. Capital template:

- 2520140 `COMMON EQUITY TIER 1 CAPITAL RATIO (transitional period)` (every release)
- 2520146 `COMMON EQUITY TIER 1 CAPITAL RATIO (fully loaded)` (every release)
- 2520155 `COMMON EQUITY TIER 1 CAPITAL RATIO (transitional period - pre floor)` (2025 only)

Check 4 compares it with cet1 / rwa, so the choice should follow OPEN-18.

- (a) Transitional, 2520140 in every release.
- (b) Fully loaded, 2520146 in every release.

## OPEN-20: `leverage_exposure` has 2 candidate lines in the EBA Leverage template

**DECIDED (see decisions/section_1_review.md):** option (a).

Raised in session 1 (step 1.2). Both exist in every release:

- 2520903 `Total leverage ratio exposures - using a transitional definition of Tier 1 capital`
- 2520904 `Total leverage ratio exposures - using a fully phased-in definition of Tier 1 capital`

The leverage_ratio KPI (tier1 / leverage_exposure) is blank until this is decided.

- (a) Transitional, 2520903 (consistent with tier1 2520133, which is transitional).
- (b) Fully phased-in, 2520904.

## OPEN-21: `debt_securities` has no single carrying-amount line for all accounting portfolios

**DECIDED (see decisions/section_1_review.md):** option (a).

Raised in session 1 (step 1.2). Section 5.1 defines debt_securities as "all accounting portfolios, carrying amount". No EBA line carries that. The nearest lines are:

- NPE 2520602 `Gross carrying amount on Debt securities (including at amortised cost  and fair value)` (gross, all portfolios other than held for trading);
- Assets 2521016 and 2521018, gross carrying amount of FVOCI and amortised-cost debt securities, each split by stage (ASSETS_Stages 1, 2, 3).

iea = cash_cb + debt_securities + loans_all, so nim is blank until this is decided.

- (a) NPE 2520602 with every dimension 0 (gross, all portfolios other than held for trading).
- (b) The sum of Assets 2521016 and 2521018 over ASSETS_Stages 1, 2 and 3. The map then needs several rows per field, summed (see OPEN-22).

## OPEN-22: `loans_customers_gross` and `loans_customers_allowance` need a sum over dimension rows

**DECIDED (see decisions/section_1_review.md):** option (a).

Raised in session 1 (step 1.2). No Exposure code means "other than central banks and credit institutions". In the NPE template:

- gross: 2520605 `... - by exposure` has 1 row per Exposure (101 central banks, 102 general governments, 201 credit institutions, 202 other financial corporations, 301 non-financial corporations, 401 households), with no Exposure 0 total;
- allowance: 2520615 has rows only for Perf_Status 1 (performing) and 2 (non performing), with no Perf_Status 0 total.

The map format (field, item, template, label, dim_filter) holds one row per field. loans_customers_net (loan_deposit), cost_of_risk and, in Section 4, the peer features need these.

- (a) Allow several map rows per field, summed by `load_eba`: gross = 2520605 over Exposure 102, 202, 301 and 401; allowance = 2520615 over the same 4 Exposures × Perf_Status 1 and 2.
- (b) Gross = 2520603 (all loans, every dimension 0) minus 2520605 at Exposure 101 and 201. Allowance = 2520613 at Perf_Status 1 plus 2, minus 2520615 at Exposure 101 and 201 × Perf_Status 1 and 2. This needs a sign column in the map.

## OPEN-23: `deposits_customers` needs a sum over 4 counterparty sectors

**DECIDED (see decisions/section_1_review.md):** option (a).

Raised in session 1 (step 1.2). Liabilities 2521215 `Financial liabilities -  by instrument and by counterparty sector`, Financial_instruments 30 (Deposits), has 1 row per Exposure: 101, 102, 201, 202, 301 and 401. Section 5.1 wants 102 + 202 + 301 + 401. loan_deposit is blank until this is decided.

- (a) As OPEN-22 (a): several map rows summed, 2521215 at Financial_instruments 30 × Exposure 102, 202, 301 and 401.
- (b) Total deposits (Financial_instruments 30 summed over every Exposure present) minus Exposure 101 and 201.

## OPEN-24: `minority_interests` has no EBA line

**DECIDED (see decisions/section_1_review.md):** option (a).

Raised in session 1 (step 1.2). No Liabilities, Assets or Capital line in any release is non-controlling interests in equity. `Minority interest given recognition in CET1 capital` (Capital 2520108) is a regulatory amount, not the accounting one. tangible_equity, and so rote (Section 3), need it.

- (a) minority_interests comes from the `report` family at every EU date (annual and half year reports, entered in Section 3 alongside at1_coupons and shares_out). The source map changes accordingly.
- (b) Use Capital 2520108 `Minority interest given recognition in CET1 capital` as a stand-in, stated as a caveat.

## OPEN-25: the EBA unit is not in SDD.xlsx, and EBA amounts are in EUR for every bank

**DECIDED (see decisions/section_1_review.md):** option (a), without downloading the mapped templates.

Raised in session 1 (step 1.3). This is the stop reason for session 1. Instruction 01 step 1.3 says to "read the unit from `SDD.xlsx`" for `test_load_eba_synthetic`. No `SDD.xlsx` (2021 to 2025) and no `TR_Metadata.xlsx` states a unit. Every cell, cell comment and sheet was searched, and the 2024 CSV guide PDF does not state one either.

The unit is printed in 2 other EBA files of each release:

- the template headings of `{year}_EU-wide_Transparency_exercise_Mapped_templates.xlsx`: `(mln EUR)` on P&L, Assets, Liabilities, NPE and the rest, and `(mln EUR,  %)` on Capital, Leverage, RWA OV1 and the credit risk sheets;
- each bank's PDF, for example `SE_M312WZV08Y7LYUC71685_TR_2025.pdf` (Swedbank): `(mln EUR, %)`.

The data agree. Total assets (item 2521010) at 2024-12-31 are 226,125.3 for Swedbank, 276,393.4 for DNB and 425,547.2 for Danske Bank, which are EUR millions, not SEK, NOK or DKK. Ratio items are decimals, for example Intesa Sanpaolo's CET1 ratio of 0.138004 at 2022-12-31.

So the unit cannot be read where the test says. EBA amounts are also in EUR for DNB, Danske, SEB, SHB and Swedbank, which conflicts with Convention 4.1 ("units of the reporting currency") and with the FACTS `ccy` column.

- (a) Read the unit from the release's `Mapped_templates.xlsx` heading. That file is added to `[eba] files` and pulled in step 1.1; the 2021 file is linked from the 2021 page under a `document_library` path. Amounts get `unit_scale` 1e6, ratios are stored as reported, and `ccy` is `EUR` for every EBA row. Convention 4.1 is amended: the `eba` family is in EUR for every bank. KPIs are pure ratios and are unaffected, except that an average of 2 EUR balances carries the EUR/SEK, NOK or DKK move between its 2 ends.
- (b) The same unit rule, with `load_eba` converting EBA amounts for SEK, NOK and DKK banks back to `report_ccy`: balance sheet values at the reference-date ECB rate, P&L values at the period mean (Convention 4.6 in reverse). This keeps Convention 4.1 but needs `bpb/fx.py` (step 1.4) before step 1.3, and the rate EBA itself used is not published.

## OPEN-26: Pillar 3 templates published only as Excel, or only on the EBA Pillar 3 Data Hub

Raised in session 2 (step 2.2). Instruction 02 B.3 lists a Pillar 3 report per EU bank at 2024-12-31, 2025-06-30, 2025-12-31 and 2026-06-30, and B.4 fixes provenance on a page of a hashed PDF. For several bank and date pairs the EU KM1, CC1 and CR1 templates exist only as an Excel workbook on the bank's site (the PDF, where there is one, is narrative only). For a few, from 2026, they exist only on the EBA Pillar 3 Data Hub, which B.1 puts out of scope. The full list is in `review/section_2.md` (step 2.2). Each pair is not fetched by `scripts/fetch_reports.py` (not a PDF), so the dates it would fill are blank.

- (a) Leave these pairs blank, as now. cet1, tier1, rwa, leverage_exposure, cet1_ratio_reported, lcr, nsfr, the CC1 fields and the CR1 fields are missing for those banks and dates, and the KPIs built on them (cet1_ratio, leverage_ratio, rwa_density, lcr, nsfr, npl_ratio, npl_coverage, cost_of_risk, loan_deposit, nim) are blank with `missing_input`.
- (b) Accept a hashed Excel workbook as a source document. `fetch_reports.py` also downloads `.xlsx` and `.xls` files and hashes them; an entry's `page` holds the sheet name and cell (for example `EU KM1!D12`); the cache stores the cited cells' values; provenance compares the value with the cell. Data Hub only pairs stay blank under B.1.
