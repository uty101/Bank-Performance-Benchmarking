# instructions/01_section_1.md: Session 1 instructions for Claude Code

Build all of Section 1 of `PLAN.md` (steps 1.1 to 1.7), with the amendments below, in one session. Step 1.0 comes first. Precedence (rule 13): this file beats `PLAN.md`, which beats the kickoff.

---

## A. Approval of session 0

Session 0 is approved. The reviewer checked it independently:

- **Clean install.** A fresh clone on Linux, Python 3.12, installed from `requirements-lock.txt` then `pip install -e . --no-deps`. `ruff check .` passes, `pytest -p socket --disable-socket -q` gives 1 passed, and `bpb` prints its usage and returns 0.
- **Config.** `config.toml` is byte identical to kickoff Section 7.
- **Universe.** `data/manual/universe.csv` holds 31 banks in kickoff order.
- **Ignore and attribute files.** `.gitignore` and `.gitattributes` match kickoff Section 9.

The `PytestAssertRewriteWarning` is harmless and the command stays as it is.

---

## B. Decisions on OPEN-01 to OPEN-16

Each decision states the reason. Step 1.0 copies this section into `decisions/section_0_review.md`, marks each item `DECIDED (see decisions/section_0_review.md)` in `decisions/OPEN.md`, and appends the amendments to `CLAUDE.md` and `PLAN.md`. Rule 14 is lifted for step 1.0 only.

1. **OPEN-01: (a).** Step 1.1 writes `data/manual/eba_urls.csv` (release, file, url, release_page_url), reading the file links from each release page. The pages are:
   - 2021: `.../eu-wide-transparency-exercise/2021-eu-wide-transparency-exercise`
   - 2022: `.../2022-eu-wide-transparency-exercise`
   - 2023: `.../2023-eu-wide-transparency-exercise`
   - 2024 and 2025: the URLs in kickoff Section 3.2

   All 2021 to 2023 pages sit under `https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis`. Then `scripts/pull_data.py --stage eba` reads that file. Reason: URLs are data, and a data file can be reviewed row by row. If a release splits its CSVs under different file names than `tr_oth.csv` and `tr_cre.csv`, record every CSV it publishes under its real name and list the difference in the review file.

2. **OPEN-02: (b), with a change.** Step 1.1 filters on the country column, keeping banks from FI, NO, DK, SE, NL, BE, FR, DE, ES and IT. It writes `data/raw/eba/{release}/{file}.csv.gz`, and the 50 MB limit applies to the gzipped file. If a gzipped, country filtered file still exceeds 50 MB, stop under rule 4. Unfiltered downloads go to the gitignored `data/eba_download/`, which you add to `.gitignore` in step 1.1, and their sha256 is recorded in the manifest. Reason: this removes the order problem with step 1.2, and the 10 country set is small.

3. **OPEN-03: (a).** The source map gets a role `bridge_input`: `report` rows for EU banks at 2024-12-31 and 2025-06-30 may be opening balances and rolling components for report family KPIs at 2025-12-31 and 2026-06-30. The KPI value at 2025-06-30 itself stays `eba`. Reason: (b) blanks every EU P&L KPI at the latest date, which defeats the project.

4. **OPEN-04: (b).**
   - **EU banks at bridge dates:** cet1, tier1, rwa and leverage_exposure are `p3`; at1_instruments, intangibles_deduction, lcr and nsfr are `report`.
   - **UK banks:** every field is `report`. A Pillar 3 PDF is entered as a document with doc_type `pillar3` and family `report`.
   - Convention 4.5 is amended to say so.

   Reason: tangible equity then takes all its parts from one family, and every UK average and rolling figure stays inside one family.

5. **OPEN-05: (a).** lcr and nsfr are blank (`missing_input`) for EU banks to 2025-06-30. They are ranked only at dates where they exist. Reason: liquidity ratios are not central to the profit gap, and backfilling 4 years from Pillar 3 PDFs is about 300 entries for little gain.

6. **OPEN-06: (a).** Step 1.2 maps every EBA P&L line between net fees and TOTAL OPERATING INCOME, NET as extra fields, listed in `fields.yaml` under `income_components_other`. They are used by check 3 only. other_income stays the residual for KPIs. Reason: a check that passes by construction checks nothing.

7. **OPEN-07: (a).** Add the field `cet1_ratio_reported` (kind ratio). It is mapped from the EBA capital template, and later from KM1 and reports. Reason: check 4 needs it.

8. **OPEN-08: (a).** The signature is `features(kpi, facts, year, rates)`.

9. **OPEN-09: (a).** The signature is `benchmark(kpi, peers, universe, cfg)`.

10. **OPEN-10: (b).** The signature is `uplift(gaps_joint, fits, pooled, ptbv)`.

11. **OPEN-11: (a).** `scripts/pull_data.py --stage gleif` queries `https://api.gleif.org/api/v1/lei-records?filter[entity.legalName]=<name>` and writes `data/raw/gleif/{bank_id}.json`. Used in Section 3.

12. **OPEN-12: (b), using `pycel`.** The test evaluates the committed workbook's formulas with pycel. Reason: the owner's machine has no LibreOffice. Add `pycel` to the dev extra in Section 4, not now.

13. **OPEN-13: (a).** The paths are:
    - PDF profiles: `outputs/reports/{bank_id}_{date}.pdf`
    - page renders: `outputs/figures/{bank_id}_{date}.png`
    - league table pages: `outputs/tables/league_{kpi}.html`
    - charts are drawn in memory and not saved separately.

14. **OPEN-14: (a).** Both tests run `bpb build` into `tmp_path` from committed raw and manual files.

15. **OPEN-15: (a).** The reviewer fixes test inputs in each section's instruction file. Section 1's are in Section C below.

16. **OPEN-16: (b).** `lei` moves to the second column of `universe.csv`, after `bank_id`.

### B.1 A correction to the kickoff found in review

**Crédit Agricole.** The EBA exercise reports each group at its highest level of consolidation, which for Crédit Agricole is Crédit Agricole Group, not the listed Crédit Agricole SA. Benchmarking the Group while pricing the SA would compare 2 different balance sheets.

Step 1.0 changes the universe row to: bank_id `CAG`, name `Crédit Agricole Group`, listed 0, ticker blank, price_ccy blank, report_ccy EUR. CAG is benchmarked and left out of valuation. Its bridge figures come from the Group figures published in Crédit Agricole SA's universal registration document and half year report.

Apply the same test to every EU bank in step 1.2. If the 2025 release names an entity at a different level from the universe row, list it in the review file and in `decisions/OPEN.md` with 2 options. Do not change the universe yourself.

---

## C. Amendments to Section 1 steps

### Step 1.0: decisions and amendments (commit `step 1.0: apply section 0 review decisions`)

1. Write `decisions/section_0_review.md` with Section B and B.1 of this file, verbatim.
2. Mark OPEN-01 to OPEN-16 decided in `decisions/OPEN.md`.
3. Append to `CLAUDE.md` under `## Amendments`:
   - every changed signature (OPEN-08, 09, 10);
   - the Convention 4.5 change (OPEN-04);
   - the new field (OPEN-07);
   - the `bridge_input` role (OPEN-03);
   - the output paths (OPEN-13);
   - the CAG change.
4. Update `PLAN.md` steps the decisions touch. Change nothing else in them.
5. Update the config files and the universe:
   - `config/source_map.yaml`: OPEN-03, 04 and 05.
   - `config/fields.yaml`: add `cet1_ratio_reported` and an empty `income_components_other` list, filled in step 1.2.
   - `universe.csv`: move `lei` to the second column and apply B.1.

### Step 1.1: EBA download

- Steps 1 and 2 in Section B govern the URLs and the filter.
- **Test** `tests/test_eba_raw.py::test_manifest_hashes` recomputes the sha256 of every committed file in `data/raw/eba/` and compares it with `MANIFEST.json`.
- **Test** `tests/test_eba_raw.py::test_reference_dates`:
  - each release holds exactly 4 reference dates;
  - the 20 dates taken together are the quarter ends from 2020-09-30 to 2025-06-30 with no gap and no duplicate.

### Step 1.2: LEIs and EBA maps

**Name matching.** Name matching against the 2025 release:

1. Casefold, strip accents and punctuation, and remove these legal suffixes as whole words: ag, sa, s a, spa, s p a, plc, ab, publ, nv, n v, asa, oyj, a s, u a, se, group, groep, gruppo, banca, banco, bank.
2. A bank matches when its normalised name equals exactly 1 normalised EBA name, or failing that is contained in exactly 1.
3. One alias applies before matching: BBVA is matched as `Banco Bilbao Vizcaya Argentaria`.
4. Anything else goes to OPEN with the candidate names and LEIs.

Print the universe with LEI, the matched EBA name and the match type (`exact` or `contained`).

**The map file.** `config/eba_map_{year}.csv` has these columns:
- field
- item
- template
- label
- dim_filter: a JSON object of the extra dimension columns and values the row needs, for example `{"Portfolio": "...", "Exposure": "..."}`, or `{}`

Labels match exactly after casefolding and collapsing whitespace. A field that needs a dimension filter is matched on label plus the dimension value labels in `TR_Metadata.xlsx` or `SDD.xlsx`. If more than 1 item or dimension combination fits, it goes to OPEN with every candidate, never a guess.

**Reconcile the maps.** The same field must map to the same label in every release. Where a release's label differs, print both labels side by side in the review file.

**New fields.** The OPEN-06 components and `cet1_ratio_reported` are mapped here too.

### Step 1.3: ingest

**Test** `tests/test_ingest.py::test_load_eba_synthetic`, on this synthetic frame:
- 2 banks: LEIs `TESTLEI000000000000A` and `TESTLEI000000000000B`
- 2 reference dates: 202312 and 202406
- 3 items: `I1` mapped to total_assets, `I2` to interest_income, `I3` unmapped
- 12 rows in total

Built in the test with the column names of the real 2025 `tr_oth.csv`. The test asserts:
- 8 FACTS rows in the FACTS column order;
- `I3` absent;
- value scaling per the release's unit (read the unit from `SDD.xlsx`, and print the unit rule in the review file);
- `lineage_id` equals `lineage_id(...)` recomputed from the row.

**Test** `test_source_map_rejects`: a `report` family row for an EU bank at 2023-12-31 lands in `rejected`.

**Test** `test_lineage_stable`: 2 calls with the same inputs return the same 12 hex characters, and changing any 1 of the 5 inputs changes the result.

### Step 1.4: FX

- `scripts/pull_data.py --stage fx` pulls the ECB series from 2020-01-01 to 2026-07-31.
- The rate on a date is the last published rate on or before it.
- The P&L rate is the mean of published daily rates for dates d with period_start ≤ d ≤ date:
  - period_start = 1 Jan of the date's year for a year to date figure;
  - period_start = 1 Jul of y − 1 for a rolling 12 months at 30 Jun of y.
- **Test** `tests/test_fx.py::test_roundtrip`: for every currency and each of 2021-12-31, 2023-06-30 and 2025-12-31, from_eur(to_eur(1234567.89)) returns the input within `fx_roundtrip`, for both kinds.
- **Test** `test_pl_rate_is_mean`: on a synthetic 5 day rate frame, the P&L rate equals the arithmetic mean.

### Step 1.5: KPIs

- **Test** `tests/test_kpi.py::test_rolling_hand`: H1 2023 = 60, FY2022 = 100, H1 2022 = 40 gives R(2023) = 120. A missing H1 2022 gives a blank with `missing_input`.
- **Test** `test_averages_one_family`: an average whose 2 ends come from different families is blank with status `mixed_family`.
- **Test** `test_recompute`: every row of the KPI table built from the committed EBA files has |value − numerator/denominator| ≤ `ratio_recompute` × max(1, |value|), using the stored numerator and denominator.
- **Test** `test_missing_input`: a KPI whose input is missing is blank with `missing_input` naming the field.
- rote, income_fte, cost_fte and cost_customer are blank in Section 1 with status `pending_section_3`. lcr and nsfr are blank with `missing_input`.
- **Outputs:**
  - `data/processed/facts.parquet` (gitignored);
  - `outputs/tables/kpi.csv`, committed, with EU banks only and dates 2021-12-31 to 2025-06-30.

### Step 1.6: checks

- Run checks 2, 3, 4, 5, 6 and 9 on EBA rows, written to `outputs/tables/checks.csv`.
- Check 3 uses `income_components_other`.
- **Test** `tests/test_checks.py::test_bs_identity`: on a synthetic balance sheet, a row with assets 100, liabilities 90 and equity 9.6 passes, and 9.4 fails.
- **Test** `test_cet1`: a reported ratio 5.1 bps away from cet1/rwa fails, and 4.9 bps passes.

**Review evidence:**
- the full KPI table for ISP, SWED and BBVA at every date;
- every failed check row;
- KPI row counts by bank and status;
- check row counts by check and passed.

### Step 1.7: mergers

List every acquisition by a universe bank completed between 2020-09-30 and 2026-06-30, each with a source URL from the acquirer's own announcement or report. At minimum, check and include or explain the exclusion of each of these:
- CaixaBank and Bankia
- Unicaja and Liberbank
- BPER and Carige
- BPER and Banca Popolare di Sondrio
- Monte dei Paschi and Mediobanca
- Santander UK and TSB
- ABN AMRO and NIBC
- KBC and 365.bank
- Intesa Sanpaolo and UBI, completed before the window

target_total_assets is taken from the acquirer's announcement or the target's last report before completion, with the page cited. Compute the materiality ratio against the acquirer's EBA total_assets at the last reference date before completion; for Santander UK, use its reports, entered in Section 3.

Print the full table with the ratio and the break flag.

---

## D. End of section

- Run the fresh-clone check (rule 12).
- Write `review/section_1.md` with the TEMPLATE headings. Add an Evidence subsection for each of the items listed in Section C.
- Push, then write `instructions/01_section_1.status.md` (rule 11), commit it, push it and stop.
