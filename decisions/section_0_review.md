# Section 0 review decisions

Copied verbatim from `instructions/01_section_1.md` Sections B and B.1 in step 1.0.

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
