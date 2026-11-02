# Section 1 completion review decisions

Copied verbatim from `instructions/02_section_2.md` Sections A and B in step 2.0.

## A. Approval of Section 1

Section 1 is approved.

### What the reviewer verified independently

- **Fresh clone.** On Linux, Python 3.12, from the lock: ruff clean, 17 passed.
- **KPI recompute.** 4 KPIs were recomputed with the reviewer's own code, straight from `tr_oth.csv` and `tr_cre.csv` of the 2024 and 2025 releases, not through `bpb`. They are cost_income, cet1_ratio, nim and cost_of_risk, for Intesa Sanpaolo and Swedbank at 2024-12-31. All 8 match `outputs/tables/kpi.csv` to 1e-9 relative:

  | bank | cost_income | cet1_ratio | nim | cost_of_risk |
  |---|---|---|---|---|
  | ISP | 0.52237549 | 0.13262930 | 0.02361549 | 0.00272178 |
  | SWED | 0.42486145 | 0.19798101 | 0.02097644 | 0.00022796 |

- **Mergers.** The 4 material breaks are accepted as found:
  - CaixaBank and Bankia: 0.545
  - Unicaja and Liberbank: 0.723
  - BPER and Banca Popolare di Sondrio: 0.392
  - Monte dei Paschi and Mediobanca: 0.796
- **Housekeeping.** The `period` key in `fields.yaml` and `bank_groups` in `source_map.yaml` are accepted.

### Decisions on the 6 merger questions

Step 2.0 writes these to `decisions/section_1_completion_review.md`.

1. **BPER and Carige.** Carige is not in any EBA release. Step 2.0 fetches Banca Carige's FY2021 annual report through `fetch_reports.py`, takes total assets at 2021-12-31 from its balance sheet, and records the page.
   - `mergers.csv` gains 2 columns at the end: `source_sha256` and `source_page`. They are filled wherever the size comes from a hashed PDF; otherwise they stay blank, with the source_url as the reference.
   - Carige's PDF page text goes into the cache under the provenance rules in B.4, and the provenance check covers it.
2. **Non bank targets stay in the file.** These are AXA IM, LeasePlan and Numis. Add Banco BPM and Anima, sized from Anima Holding's last annual report before completion.

   Size every target with blank total assets from the target's last annual report before completion, the same way as Carige. Fetch the report, record the page, and keep the hash in `source_sha256`. Do this for:
   - BPER's UBI branch unit;
   - LeasePlan;
   - Numis;
   - AXA IM;
   - Alpha Bank Romania.
3. **Business transfers.** For a business transfer where the only published size is lending, that lending figure is the size. This is Nordea and Danske Norway, at EUR 9bn. Note it in a `size_basis` column, added at the end: `total_assets` or `loans`.
4. **UK targets.** Tesco Bank, Sainsbury's Bank and every UK acquirer's ratio are done in Section 3.
5. **CHF.** Add CHF to `[fx] currencies`. This is a reviewer change to `config.toml`, allowed in step 2.0. Re-run the fx stage so REYL's ratio is computed.
6. **Merger research method.** It is accepted, but the 4 material deals must be checked again in this session. Fetch each source page, print the line that gives the total assets in the review file, and confirm the figure.

---

## B. Decisions for Section 2

### B.1 Bridge capital comes from bank Pillar 3 reports, not the Data Hub

The Pillar 3 Data Hub has no documented public bulk download. Its user guides describe only visual tools. Scraping it would be fragile, and that fragility is what this project avoids.

Each EU bank's own Pillar 3 report publishes the same templates, so those are used.

- **`load_p3(raw_root, universe)`** reads the `report_entries.csv` rows whose doc_type is `pillar3` and whose field the source map assigns to `p3`.
- **Family comes from the source map.** A row's family is decided by the source map, by bank group, field and date, never by doc_type. doc_type only says which document the figure came from.
- **The Data Hub** is out of scope. Record this in `decisions/data_sources.md`.

### B.2 Which template gives which field

Templates are the EU Pillar 3 templates (CRR3 versions where the 2025 and 2026 reports use them). Row numbers are as printed in the bank's own table, and the row label must match.

| field | template | row | column |
|---|---|---|---|
| cet1 | EU KM1 | 1 | the reference date's column |
| tier1 | EU KM1 | 2 | the reference date's column |
| rwa | EU KM1 | 4 (total risk exposure amount; never the pre floor row 4a) | the reference date's column |
| cet1_ratio_reported | EU KM1 | 5 | the reference date's column |
| leverage_exposure | EU KM1 | 13 | the reference date's column |
| lcr | EU KM1 | 17 | the reference date's column |
| nsfr | EU KM1 | 20 | the reference date's column |
| at1_instruments | EU CC1 | 30 (Additional Tier 1 capital: instruments, capital instruments and the related share premium) | amount |
| intangibles_deduction | EU CC1 | 8 (Intangible assets, net of related tax liability), entered positive | amount |
| loans_all | EU CR1 | 010 Loans and advances | gross carrying amount, performing + non performing |
| loans_customers_gross | EU CR1 | 030 + 050 + 060 + 080 | gross, performing + non performing, summed |
| loans_customers_allowance | EU CR1 | 030 + 050 + 060 + 080 | accumulated impairment, performing + non performing |
| loans_households_gross | EU CR1 | 080 Households | gross, performing + non performing |
| npl_gross | EU CR1 | 010 | gross, non performing |
| npl_allowance | EU CR1 | 010 | accumulated impairment, non performing |
| debt_securities | EU CR1 | 090 Debt securities | gross, performing + non performing |

**Summed fields.** A field summed over rows or columns is entered as 1 row per printed number, with the same field name and a `component` note in the snippet. `load_report_entries` sums them, and B.1 of `decisions/section_1_review.md` applies: if any component is missing, the field is missing.

**Signs.** Accumulated impairment is printed negative in CR1. Enter `value_as_printed` as printed and `value` positive (Convention 4.2).

**Row numbers that differ.** If a bank's CR1 numbers its rows differently, match on the row label and write the bank's row number in the snippet.

**Everything else comes from the annual and half year reports.** That covers every P&L field, total_assets, total_liabilities, total_equity, cash_cb, trading_assets and deposits_customers, from the consolidated statements and their notes:

- **total_operating_income:** the income statement's total operating income, or net revenue as the bank names it.
- **income_components_other:** each line between net fees and total operating income as printed, so check 3 can run.
- **admin_expenses:** staff expenses + other administrative expenses.
- **depreciation:** depreciation, amortisation and impairment of property, equipment and intangibles, as printed in operating expenses.
- **resolution_dgs_contrib:** entered only where the income statement shows it as its own line. Where it does not, the field is not entered. The derived opex then treats it as 0, with status `levies_in_admin`, so it is never a missing input.
- **impairments_fin:** credit impairment losses, or net impairment on financial assets, as printed.
- **deposits_customers:** deposits from customers as printed on the balance sheet. If the balance sheet splits customer deposits from deposits by banks, use the customer line only.
- **trading_assets:** financial assets held for trading. If not shown separately, the field is not entered.

### B.3 Documents and dates for EU banks

Per EU bank, in `report_urls.csv`:

- **annual:** FY2025 annual report or universal registration document. Its 2025-12-31 column, and its 2024-12-31 comparative column, supply both dates.
- **half_year:** H1 2025 report, for 2025-06-30, and H1 2026 report, for 2026-06-30.
- **pillar3:** 2024-12-31, 2025-06-30, 2025-12-31 and 2026-06-30.

**Comparative columns.** A figure is entered from the document where it is the current period, except 2024-12-31 balance sheet values, which come from the FY2025 comparative column. Restated comparatives are not used for any other date.

**Crédit Agricole Group (CAG).** Use the Group columns of Crédit Agricole SA's universal registration document and half year report, and the Group Pillar 3 report, never the CASA columns. Seam 2 shows whether this was done right: CAG total_assets at 2025-06-30 from report and from eba must agree within 2%. If not, stop under rule 4.

### B.4 Page text cache and provenance

- **Cache.** `data/raw/report_text/{sha256}.jsonl.gz` holds only the pages cited by at least 1 entry, to keep the repo small. Each line is `{"page": n, "text": ...}`, where page is the 1 based physical page index of the PDF, not the printed folio. `scripts/fetch_reports.py --cache-pages` rebuilds it from the entries and the PDFs.
- **Snippet.** Each entry's `snippet` must contain `value_as_printed` verbatim.
- **Provenance rule.** Kickoff 5.3 item 1 applies. A failed row is excluded and listed.

### B.5 Working bank by bank

Step 2.3 is large: about 26 banks × 4 dates × 30 fields.

**Commits.** Commit after each bank with message `step 2.3: <bank_id> entries`. The rule 2 one-commit-per-step limit is lifted for step 2.3 only. Work in universe order.

**If the session cannot finish every bank:**
1. Finish the bank in progress.
2. Run steps 2.4 and 2.5 on the banks done.
3. Write the review and status with outcome `partial`, listing the banks done and the banks left.
4. Push.

Running out of time or context is not a rule 4 stop. The next instruction file continues from the first bank left.

### B.6 Seam tests

- **Seam 1.** At 2025-06-30, cet1, rwa and leverage_exposure from eba and p3 are compared within `seam_capital_tol` (0.1%). Failures are flagged, not stopped, except as below. Print every row.
  - If more than 5 banks fail on cet1 or rwa, stop under rule 4.
  - The 2025 EBA amounts are EUR millions, and KM1 is in reporting currency. For the 5 non EUR banks, convert KM1 to EUR at the 2025-06-30 ECB rate before comparing (decision B.2 of `decisions/section_1_review.md`).
- **Seam 2.** At 2025-06-30, for every field present in both eba and report: report value converted to EUR as above, the absolute difference and the relative difference. No threshold except CAG's total_assets (B.3). The full table goes in the review, sorted by absolute relative difference, largest first.

