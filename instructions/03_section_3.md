# instructions/03_section_3.md: Session 3 instructions for Claude Code

Build all of Section 3 of `PLAN.md` (steps 3.1 to 3.4), with the amendments below. Step 3.0 comes first. Precedence (rule 13): this file beats `PLAN.md`, which beats the kickoff.

---

## A. Approval of Section 2

Section 2 is approved, and SHB is restored. The SHB stop was correct under the rule as written. The rule was the reviewer's error.

What the reviewer checked independently:

- **Random entries.** In the earlier review, 25 random entries were all found on their cited pages.
- **Seam 2.** The reviewer read the seam 2 rows for every bank. Report profit_owners and EBA profit_owners at 2025-06-30 agree within 0.25% for 21 of 26 banks.
- **The exceptions.** Each is explained by the bank's own documents, not by entry errors:
  - **KBC (17%):** the report, as printed, gives an H1 2025 result after tax of 1,564m, and total operating income of 5,955m against EBA's 4,256m. The prudential scope treats KBC's insurance subsidiaries differently from the accounting scope.
  - **SHB (7.6%) and DNB (4.4%):** both pass scope checks on their own LR1, and both show the same kind of scope effect in fees and income.
- **The LR1 gate cannot work for every bank.** Banks fill LR1 row 1 differently:
  - SHB prints the prudential total in row 1 and adds the scope item in row 2.
  - DANSKE prints the prudential total in row 1 with a 0 adjustment, while its balance sheet total is 16.8% higher.

  So no single formula on LR1 or on profit tells a wrong entity apart from a real difference in scope for every bank.

### A.1 Decisions on the Section 2 questions

1. **The scope gate is informational.** Check `8b_scope_gate` keeps its rows, with threshold blank and passed blank. No bank is blocked by it.
   - SHB's report and p3 rows are restored, and its KPIs at 2025-12-31 and 2026-06-30 are computed.
   - The entity check is the combination already in place:
     - provenance on every report figure;
     - seam 1 (p3 against EBA, 72 of 72 within 0.1%);
     - the published seam 2 table.
   - The README states the scope difference for bank insurers as a caveat. Those banks are NDA, DANSKE, SWED, SEB, SHB, KBC, BNP, GLE and CAG, plus any with a total_assets seam above 5%.
2. **Pillar 3 not obtainable (DNB, SHB and UCG at 2026-06-30; CBK at every date).** Take the KM1 figures from the capital adequacy note of the same date's interim or annual report:
   - cet1, tier1, rwa, cet1_ratio_reported and leverage_exposure;
   - lcr and nsfr where printed.

   These rows are family `p3`, with status `p3_from_report`. CR1 fields stay blank where no Pillar 3 exists.
3. **Bankinter's 2026 workbook.** Use its KM1 prior period columns for 2Q25 and 4Q25. They are figures published in a hashed document, so they get status `from_comparative` (B.9 of the 02b decisions).
4. **`mixed_family` blanks** for BKT at 2026-06-30 and UNI nim at 2025-12-31 are accepted as blanks.
5. **KPI statuses** carrying input statuses (deviation 16) are accepted.
6. **`xlrd`** is accepted. Confirm it is in `requirements-lock.txt`.
7. **UNI total_equity at 2025-06-30** stays out.

Step 3.0 writes Section A and A.1 to `decisions/section_2_review.md`. It also appends A.1 items 1 and 2 to CLAUDE.md Amendments, noting that amendment 13's CAG gate and the 02b gate rule are superseded. Rule 14 is lifted for that step.

---

## B. Section 3 decisions

### B.1 Fields added in this section

Append these to `fields.yaml` and `source_map.yaml`, all family `report`:

| field | kind | period | meaning | source |
|---|---|---|---|---|
| minority_interests | amount | bs | non controlling interests in equity, as printed on the balance sheet | balance sheet |
| at1_coupons | amount | pl | distributions on AT1 instruments in the period, year to date, entered positive | statement of changes in equity, or the note on equity instruments |
| shares_out | count | bs | ordinary shares in issue net of treasury shares at the reference date | the share capital note or the EPS note; the EPS note's period end number is not the weighted average |
| fte | count | bs | full time equivalent employees at the reference date | key figures or the notes |
| customers | count | bs | customers at the reference date | key figures; entered only where printed |
| rote_reported | ratio | pl | the bank's own published RoTE (or RoTE equivalent named as such) | key figures; FY2025 and H1 2026 only; used only for the comparison in step 3.4 |

Count fields have `unit_scale` 1 times the printed scale (for example, shares printed in millions get 1e6), and `ccy` blank.

### B.2 Dates

| bank group | fields | dates |
|---|---|---|
| EU banks | B.1 fields (except rote_reported) | every 31 Dec from 2020-12-31 to 2025-12-31, and every 30 Jun from 2021-06-30 to 2026-06-30 |
| UK banks | every field in `fields.yaml` | the same dates |

That is 12 dates in each case. For EU banks at EBA dates, these report rows combine with `eba` rows under the mixed currency rule (amendment 9).

### B.3 Documents

Per bank, in `report_urls.csv`:

- **annual:** FY2020 to FY2025.
- **half_year:** H1 2021 to H1 2026.
- **pillar3 (UK banks only):** every date. UK KM1, CC1 and CR1 use the same row numbers as the EU templates; the B.2 template table of instruction 02 applies.

A figure is entered from the document where it is the current period. If that document cannot be obtained, use the next document's comparative column, with status `from_comparative`.

**Rules for UK banks:**

- **HSBC** reports in USD at HSBC Holdings level: `ccy` USD.
- **Santander UK Group Holdings** reports in GBP.
- **The UK bank levy**, where it is a separate income statement line, is `resolution_dgs_contrib`.
- Every other mapping rule from instruction 02 B.2 and from 02b B.4 to B.8 applies unchanged.

### B.4 One offs (`data/manual/one_offs.csv`)

**Source.** Only items that the bank itself lists as excluded from its own adjusted or underlying measure, in its alternative performance measure reconciliation, for the same period, in an annual or half year report. Nothing is judged by you.

**Columns.** As in kickoff 6.2, plus 3 more at the end: `value_as_printed`, `unit_scale` and `snippet`. Provenance applies to every row.

**Field.** `field` is the P&L field the item sits in: admin_expenses, depreciation, impairments_fin, provisions, impairments_nonfin, or an income component.

**Amount.** `amount` is the pre tax effect on profit:
- positive when the item reduced profit (a cost, which is added back for underlying);
- negative when it increased profit (a gain, which is removed).

**Coverage.** Every bank with such a reconciliation, every date in B.2.

**Underlying KPIs.** The reported field minus the item's effect on that field. Fields not touched by one offs are the same on both bases. Tax is not adjusted (Convention 4.8).

### B.5 Market and sovereign data

- **Prices:** `scripts/pull_data.py --stage market` pulls yfinance daily `Close` with `auto_adjust=False`, from 2020-12-01 to 2026-07-31, for every listed ticker. It also stores the `currency` field of `Ticker(t).fast_info` or `.info` per ticker in `data/raw/market/currency.csv`, so the GBp rule (Convention 4.12) is applied from data, not assumed. yfinance's `end` is exclusive, so pass 2026-08-01.
- **Sovereign yields:** `--stage fred` pulls the series in kickoff 3.2.

### B.6 Working method

- Same as Section 2: 1 commit per bank, message `step 3.1: <bank_id> entries` for UK banks and `step 3.2: <bank_id> entries` for the B.1 fields.
- The partial rule holds: finish the bank in progress, run step 3.4 on the banks done, and write the review and status with outcome `partial`.
- Running out of time or context is not a rule 4 stop.
- Universe order: UK banks first in step 3.1, then all 31 banks in step 3.2.

---

## C. Steps

### Step 3.0: decisions (commit `step 3.0: apply section 2 review decisions`)

1. Write the decisions file per Section A.
2. Update the fields and source map per B.1.
3. Add the 3 new `one_offs.csv` columns.
4. Restore SHB's report and p3 rows.
5. Enter the A.1 item 2 and 3 figures (`p3_from_report` and Bankinter's comparative KM1 columns).
6. Re-run the KPIs to 2026-06-30.

Review evidence:
- SHB's KPIs at 2025-12-31 and 2026-06-30;
- every `p3_from_report` row.

### Step 3.1: UK banks

1. Fill `lei` for the 5 UK banks via `scripts/pull_data.py --stage gleif` (OPEN-11 (a)), using exactly 1 active record per bank. Print the name and LEI.
2. Add `report_urls.csv` rows, fetch the documents, and make the entries (B.2, B.3).
3. Compute UK merger ratios:
   - SANUK–TSB, HSBA–SVB UK, BARC–Tesco Bank and NWG–Sainsbury's Bank;
   - size Tesco Bank and Sainsbury's Bank by the B.10 order of the 02b decisions.

Review evidence:
- per UK bank, a field × date count table;
- every missing field with its reason;
- the merger rows.

### Step 3.2: B.1 fields for all 31 banks

Review evidence:
- per bank, a date × field table of the B.1 values in their own units;
- every missing value with its reason.

### Step 3.3: one offs

**Test** `tests/test_one_offs.py::test_underlying`:
- A synthetic bank with admin_expenses 100 and a one off of +10 on admin_expenses has an underlying admin_expenses of 90, and a reported admin_expenses of 100.
- A gain of −5 on an income component lowers that component by 5 on the underlying basis.

Review evidence:
- the full `one_offs.csv` row count by bank;
- the 10 largest items by absolute amount relative to total operating income.

### Step 3.4: rote, market and sovereign data

1. Compute rote for every bank at every date where inputs exist (kickoff 5.2, Convention 4.3 and 4.4; the mixed currency rule for EU banks at EBA dates).
2. Run `--stage market` and `--stage fred`.

**Tests:**
- `tests/test_kpi.py::test_rote_hand`: on a synthetic bank with profit_owners 120, at1_coupons 20, and tangible equity inputs at 2 dates giving an average tangible equity of 1,000, rote is 0.10.
- `tests/test_market.py::test_gbp_pence`: a synthetic price series with currency `GBp` is divided by 100; `GBP` is not.

**Review evidence:**

1. **rote table.** rote for every bank at every date, in pct, both bases.
2. **rote comparison.** A table of `rote` against `rote_reported` at 2025-12-31 for every bank that prints one, with the difference. No threshold: differences in definition are expected. Print it so the reviewer can judge.
3. **Hand checks.** Shown line by line from the entries:
   - LLOY rote at 2025-12-31;
   - BBVA rote at 2024-12-31. This one uses `eba` and `report` rows under the mixed currency rule; BBVA is EUR, so there is no FX.
4. **Market coverage.** Per ticker: first date, last date, row count, and currency.
5. **FRED coverage.** Per series: first date, last date, row count.

---

## D. End of section

- Run the fresh clone check (rule 12).
- Write `review/section_3.md` with the TEMPLATE headings.
- Push, then write `instructions/03_section_3.status.md` (rule 11), commit it, push it and stop.
