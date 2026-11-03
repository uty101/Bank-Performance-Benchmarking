# Status: instructions/02b_section_2_continue.md

## Outcome

Section 2 is complete, with one bank stopped under rule 4: **SHB, which failed the scope adjusted gate (B.1)**. Every other bank is finished. The review is `review/section_2.md` (d279eaa).

## Last step reached

End of section. Fresh-clone check passed at f8adbcb, review written and pushed. Commits this session:

- **2.0b:** 419f762
- **2.3**, in universe order:
  - NDA 62c7620, DNB 9a76d43, DANSKE f5c2d3f, SEB 7995fe1, SHB 6272787, SWED 5944351, INGA a49491f, ABN 56814ec, KBC b6d8b82, RABO 32f3e82, BNP 9496cc8, GLE 9a332ca, CAG dfc1c22;
  - DBK 14a2815, CBK 1109095, SAN 66af9b6, BBVA f437e86, CABK a47aa1d, SAB 012561d, BKT bbddac1, UNI 714657f, UCG 0a87383, ISP b056d49, BAMI a8bbf85, BPE df24aa1, BMPS 9c8b55f.
- **2.4:** fdf60a2
- **2.5:** f8adbcb
- **Review:** d279eaa

## Results

- **Entries and provenance:** `report_entries.csv` holds 5,589 entries for 26 banks, and all 5,589 pass provenance. All 11 hashed merger sizes pass merger provenance.
- **Seams and checks 2 to 5:** seam 1 passes 72 of 72. Seam 2 has 738 rows and no threshold. Checks 2 to 5 have no failures. Check 2 writes 24 `no_liabilities_line` rows, for BAMI, BMPS, BPE, CBK, ISP and UCG (B.8).
- **Scope gate:** passes for 23 banks; SHB fails at 8.54%. CBK and BKT have no LR1.
- **KPIs:** `kpi.csv` runs to 2026-06-30. The ISP hand check at 2025-12-31 (nim 0.026664, cost_income 0.431708) agrees with it.
- **Mergers:** Alpha Bank Romania's ratio is 0.0059. UBI unit and AXA IM are sized by consideration.
- **Tests and fresh clone:** 21 tests pass and ruff is clean. The fresh clone rebuilds `kpi.csv` and `checks.csv` byte-identical.

## Stop reason (SHB only)

SHB's EU LR1 at 2025-06-30 prints:
- row 1 at 3,372,742m SEK, which is the prudential total (EBA total assets match it);
- row 2 at +288,024m;
- row 1 + row 2 = 3,660,767m, the balance sheet total.

The B.1 formula therefore gives 8.54% > 2%. SHB's report and p3 rows stay in FACTS and in the checks with status `scope_gate_failed`, and its KPIs after 2025-06-30 are blank.

## Questions and blockers for the reviewer

1. **SHB gate.**
   - (a) Keep SHB out of the report-family KPIs.
   - (b) Gate SHB on LR1 row 1 alone.
   - (c) Gate every bank on report total_assets + row 2. On that basis SHB is 17.1% and DANSKE 16.8% off. DANSKE passes B.1 only because its own row 1 is already prudential and its row 2 is 0.
2. **Documents not obtained.** These pairs stay blank:
   - DNB, SHB and UCG Pillar 3 at 2026-06-30. They exist only on the Data Hub, which serves them through Power BI with no per-bank file URL.
   - Commerzbank's Disclosure Report at all 4 dates. The links are built client-side.
   - Bankinter's H1 2025 report and its Pillar 3 reports for 2024-12-31, 2025-06-30 and 2025-12-31. These returned 403 and were not circumvented. Bankinter's 2026 workbook also prints KM1 columns for 2Q25 and 4Q25; these were not used. Should they be?
3. **`mixed_family` blanks** (B.2 forbids crossing families):
   - BKT at 2026-06-30 has 5 average-based KPIs with no 2025-06-30 report balance sheet;
   - UNI nim at 2025-12-31 has no 2024-12-31 loans_all or debt_securities.
4. **KPI statuses.** `kpi.py` now carries usable input statuses into each KPI, for example `dep_in_admin`, `toi_summed` and `from_comparative`. Before this it reported plain `ok`. Deviation 16 in the review.
5. **New dependency.** `xlrd` was added to the dev extras for Danske's `.xls` workbooks (B.3).
6. **Left out:** UNI total_equity at 2025-06-30, because text extraction splits the printed number.

## git log origin/main --oneline -3

```
d279eaa section 2: review (complete; SHB stopped at the scope adjusted gate)
f8adbcb step 2.5: KPIs at 2025-12-31 and 2026-06-30 for EU banks
fdf60a2 step 2.4: provenance and seams
```
