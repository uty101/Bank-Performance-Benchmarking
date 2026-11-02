# Conventions resolved

Section 4 of `instructions/00_kickoff.md`, items 1 to 13, numbered as there.

1. **Units.** All monetary values stored in units of the reporting currency (not thousands or millions). The scale stated on the source page is applied on entry and recorded in `unit_scale`.
2. **Signs.** Expenses, impairments and tax are stored as positive numbers. A reversal (a net release) is stored negative. The internal formulas in Section 5.2 then add and subtract as written.
3. **Year to date.** EBA and report P&L values are year to date. FY = the 31 Dec value. H1 = the 30 Jun value. Rolling 12 months at 30 Jun of year y: R(y) = H1(y) + FY(y − 1) − H1(y − 1), all 3 from one source family.
4. **Averages.** Average balance for a fiscal year = (closing balance at 31 Dec of y − 1 + closing balance at 31 Dec of y) / 2. Average for a rolling 12 months at 30 Jun of y = (balance at 30 Jun of y − 1 + balance at 30 Jun of y) / 2. Both ends from one source family; a report's comparative column counts as the same source family as its current column.
5. **Source family.** `eba`, `p3` (Pillar 3 data, Data Hub or bank Pillar 3 report), `report` (annual or half year report). Section 5.1 says which family fills which field.
6. **Local currency first.** Every KPI is computed in reporting currency. Conversion to EUR is applied only to sized values (Section 5.6) and only after the KPI is computed: 31 Dec or 30 Jun ECB rate for balance sheet values, the mean of daily ECB rates over the period for P&L values.
7. **Basis points and percent.** Code holds decimals. Tables show % to 2 decimals and bps to 1 decimal.
8. **Underlying figures.** Underlying = reported adjusted for the one offs in `data/manual/one_offs.csv` only, each added back or removed before tax at the amount the bank discloses. Tax on one offs is not adjusted. KPIs are computed on both bases with a `basis` column.
9. **Failed or missing values** keep their rows with a `status` column and a blank value, never a fallback number.
10. **Merger breaks.** A bank with a row in `data/manual/mergers.csv` whose target total assets exceed `merger_materiality` of the acquirer's total assets at the last reference date before completion gets a break at the completion date. Year on year changes that span a break, and the driver decomposition for the fiscal year containing it, are blank with status `merger_break`.
11. **Tax rate for sizing.** t̄ = (sum of tax over the 3 fiscal years ending at the KPI date) / (sum of profit before tax over the same years). If the sum of profit before tax is ≤ 0, or t̄ falls outside [0, 0.6], use the country rate in `[tax_fallback]` and set status `tax_fallback`.
12. **Prices.** Close on the last trading day on or before the KPI date, in price currency, divided by 100 when yfinance reports the currency as `GBp`.
13. **Lineage ID.** `lineage_id` = first 12 hex characters of sha256 of `bank_id|ref_date|field|source_family|locator`, where `locator` is the EBA item code and release year, or the report sha256 and page number. Every derived row stores the lineage IDs of its inputs, `;` separated.
