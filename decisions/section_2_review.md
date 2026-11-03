# Section 2 review decisions

Written in step 3.0 from `instructions/03_section_3.md` Sections A and A.1, verbatim.

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
