# Section 2 stop review decisions

Copied verbatim from `instructions/02b_section_2_continue.md` Sections A and B in step 2.0b.

## A. Review of the stopped session

The stop was correct, and the gate that failed was the reviewer's error.

The B.3 gate compared total assets on 2 different scopes of consolidation:
- the EBA figure is on the prudential scope, which excludes insurance subsidiaries;
- the annual report figure is on the accounting scope, which includes them.

CAG's own LR1 bridges the 2 to the unit (2,614,011 − 426,262 = 2,187,749). That proves the entries are Group figures, which is what the gate was meant to show.

What the reviewer checked independently:
- 25 random entries from `report_entries.csv`, read against the committed page text cache with the reviewer's own matching code. All 25 values appear on their cited pages.
- Small values such as Nordea `loans_all` 3,614m are the non performing component of a summed field, which is correct.

### The scope finding matters beyond CAG

For bank insurers (NDA, DANSKE, SWED, SEB, KBC, BNP, GLE and CAG), total assets differ by about 10% to 20% between the 2 sources.

Cross section at the latest dates: every bank's KPIs at 2025-12-31 and 2026-06-30 come from the `report` and `p3` families. All banks are therefore on the accounting scope at those dates, so the cross section stays consistent.

Time series across the switch from `eba` to `report`: a change, trend or year on year split would mix the 2 scopes. B.2 below fixes this.

---

## B. Decisions

1. **The CAG gate becomes a scope adjusted gate.** Enter 2 new fields from EU LR1 at 2025-06-30 for every EU bank (both `report` family, used by checks only):
   - `lr1_total_assets` (row 1)
   - `lr1_scope_adjustment` (row 2, the adjustment for entities consolidated for accounting purposes but outside the regulatory scope), entered with the sign as printed.

   The gate: |(lr1_total_assets + lr1_scope_adjustment) − eba total_assets| / eba total_assets ≤ 0.02 for every EU bank where LR1 is entered. Use the sign convention so that a printed negative reduces assets. This replaces the CAG only gate. A failure is a rule 4 stop for that bank only: leave its bridge entries out of the KPIs, finish every other bank, and report it. Seam 2 adds a column with the scope adjusted report total assets.

2. **No time comparison crosses the family switch.** From this section on, every year on year change, every 3 year trend and every driver decomposition that compares 2 dates uses values from 1 family.
   - FY2024 P&L is entered from the FY2025 annual report's comparative column (role `bridge_input`, all P&L fields and `income_components_other`). FY2024 against FY2025 is then report against report.
   - Where a comparison must span the switch and no same family pair exists, the result is blank with status `family_switch`.

   Record this rule in `decisions/` and CLAUDE.md Amendments. Sections 4 and 5 will apply it.

3. **OPEN-26: (b).** A Pillar 3 workbook (.xlsx) is a valid source.
   - Download and hash it like a PDF.
   - `page` holds `sheet!cell` (for example `KM1!D12`).
   - The text cache stores, per cited sheet, one JSON line `{"page": "<sheet>", "text": ...}` holding the sheet's cell values row by row, tab separated.
   - Provenance checks the value against that text.
   - A report on the Data Hub only: use it if the hub offers a per bank file download (PDF, xlsx or csv) at a URL you can fetch with a script. Treat it as a hashed document with doc_type `pillar3`. Otherwise leave it blank and list it.

4. **Blank and dash cells in a printed template row are 0.**
   - When a template row is printed and a cell in it is `-`, `–` or empty, the component is entered with value 0, and `value_as_printed` holds the dash or `blank`.
   - For these rows, provenance checks that the row label appears on the cited page.
   - A row that is not printed at all stays missing, and B.1 of `decisions/section_1_review.md` still applies.
   - Go back over the committed banks and add the zero components this unlocks (debt_securities, customer loans and allowances).

5. **Depreciation inside administrative expenses.** When the income statement prints no depreciation line, the bank's administrative expenses line is taken to include it. admin_expenses is entered as printed (DBK: compensation and benefits + general and administrative expenses). depreciation is not entered, and opex treats it as 0 with status `dep_in_admin`, exactly like the levies rule.

6. **Insurance lines.** admin_expenses is staff and other administrative expenses as printed on the income statement. Insurance service expenses and technical charges are never added in. Where a bank nets them into revenue under IFRS 17, take the lines as printed. The seam table shows the effect, and the README caveat covers it.

7. **profit_owners is net profit minus non controlling interests,** matching FINREP and the EBA history. For RABO this includes the amounts attributed to Rabobank Certificates and Capital Securities holders: enter them as components summed into profit_owners. AT1 coupons are deducted later, through at1_coupons.

8. **No printed total.**
   - total_operating_income: if the income statement prints no total, it is derived as the sum of the printed income lines, with status `toi_summed`. Enter each line as a component. Applies to CBK and any similar bank.
   - total_liabilities: if no total is printed, it is not entered, and check 2 writes a row with status `no_liabilities_line` and no pass or fail. Applies to CBK and UCG.

9. **Documents you cannot get.**
   - Bankinter returns 403 to scripts. Do not circumvent it. When a current period document cannot be obtained, take the figures from the comparative column of the next document that has them (for H1 2025 P&L, the H1 2026 report), with status `from_comparative`. This applies to any bank. The Pillar 3 dates stay blank unless decision 3 finds a Data Hub file.
   - Commerzbank publishes its Pillar 3 as the "Disclosure Report" (Offenlegungsbericht) on its investor relations site under Reports. Search for those titles before listing it as missing.

10. **Mergers.** Use the first published of these, in order, as the size: total assets, else loans, else the consideration paid. Record which in `size_basis`.
    - Size the UBI branch unit and AXA IM this way.
    - Add RON to `[fx] currencies` (a reviewer change to `config.toml`), re-run the fx stage, and compute Alpha Bank Romania's ratio.
    - BPER and Carige (0.164) is accepted as a material break.

11. **Uncommitted work from the stopped session.**
    - Commit `tests/test_checks.py` and `scripts/run_all.py` under step 2.4 if they still match this file.
    - The scratchpad entries for DBK to UCG and the partial UNI to BMPS entries may be used only if every row passes provenance against a freshly downloaded and hashed document. Otherwise redo them.

