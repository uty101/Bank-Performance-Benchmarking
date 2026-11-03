# Status: instructions/03c_section_3_finish.md

## Outcome

**Stopped** under rule 4 at step 3.7. BMPS holds no AT1 at all, and NDA at 2026-06-30 charges no AT1 coupon to equity after its 2025 redemption. Under decision B.1, at1_coupons there has neither a printed amount nor a flag of 1, so it is missing, and so is rote: BMPS at every date, NDA at 2026-06-30. Entering 0 would be a design choice (OPEN-34).

Every other part of step 3.7 is done:
- decisions 1 to 4 are applied to all 31 banks;
- rote is recomputed;
- `tests/test_yields.py::test_coverage` passes unchanged;
- 26 of 26 tests pass, and ruff is clean;
- the fresh clone at 56292fe gives the same result.

The review is `review/section_3.md` (6eb4ce6).

## Last step reached

Step 3.7. Commits this session:

- **3.7:** 5dabeef
- **Open questions OPEN-34 and OPEN-35:** 56292fe
- **Review:** 6eb4ce6

## Results

- **at1_coupon_in_pl:** 345 entries, all at the same dates as at1_in_equity.
  - 173 annual citations and 172 half year copies (status class_from_annual).
  - Value 1 for SEB, SHB, SWED and INGA at every date, and for DANSKE from 2023. The reviewer's check of the flag-0 banks:
    - SEB, SHB, SWED and INGA: confirmed in interest expense.
    - DANSKE: 0 to 2022 (coupons charged to equity), 1 from 2023.
    - NDA: 0 throughout, because the 2025 coupon went to equity.
    - BMPS: no AT1 at all.
  - Value 0 everywhere else, including SAN, BBVA, CABK, SAB and BKT (coupons charged to reserves).
  - BMPS is not entered.
- **at1_coupons, Spanish banks:** every existing entry was checked against the definition in B.1.
  - SAB 2020-12-31 was re-entered as 73,227 thousand from the EPS note.
  - SAN's H1 2021 and H1 2022 reports print no coupon, so SAN's rote at 2022-06-30 and 2023-06-30 is now blank.
- **minority_interests, no_nci_line:** 26 entries:
  - SEB at all 12 dates;
  - DANSKE and NDA from 2024-06-30;
  - SANUK at 2024-06-30, 2025-06-30, 2025-12-31 and 2026-06-30.
- **at1_in_equity:** 178 half year rows now cite the annual report of the same year (2026-06-30: the 2025 report), status class_from_annual. BKT's 2021-06-30 to 2024-06-30 are newly filled. No value changed.
- **NO yields:** every month is the mean of `B.10Y.GBON` business days, status monthly_from_daily.
  - 2025-12: 4.153157895 (19 days).
  - 2025-11 and 2026-06 match the monthly series to 3 decimals.
- **Provenance:** 10,936 of 10,936 report entries pass.
- **rote:** filled at 218 of 310 bank-dates (213 before this step).
  - 17 bank-dates newly filled: SEB at 10 dates, DANSKE at 3, NDA at 2, SANUK at 2.
  - 12 newly blank: BMPS at all 10 KPI dates and SAN at 2.
- **Hand checks match kpi.csv:**
  - LLOY 2025-12-31: 0.120589;
  - BBVA 2024-12-31: 0.185516, now net of coupons of 388m;
  - SEB 2025-12-31: 0.138456.
- **BAMI and BMPS (decision 5):** no entry error. The gaps come from the banks' definitions:
  - BAMI uses closing equity, gross profit and accounting AT1, and excludes the year's profit from equity.
  - BMPS excludes Mediobanca, which was consolidated only at year end.

## Stop reason

BMPS: each annual report says "the Group held no equity instruments", and Tier 1 equals CET1 from 2020 to 2024. The EUR 95m of AT1 capital in 2025 is Mediobanca's minorities (CC1 row 34; row 30 is a dash). No coupon is printed anywhere.

NDA H1 2026: its equity AT1 was redeemed in 2025, and the cash flow line "Paid interest on Additional Tier 1 capital" is a dash for H1 2026.

Under 03c B.1, at1_coupons is the amount charged to equity or reserves, and is 0 only where at1_coupon_in_pl is 1. Neither case has an amount or a flag of 1.

## Questions and blockers for the reviewer

1. **OPEN-34:** at1_coupons where no AT1 coupon is charged to equity and none is printed (BMPS every date, NDA 2026-06-30). Should it be 0 with a status, or stay missing as now?
2. **OPEN-35:** the strict reading of "any amount" in B.2 left these missing:
   - SANUK at 2023-06-30, 2023-12-31 and 2024-12-31, DANSKE at 2023-06-30 and ABN at 2020-12-31: only comparative-period amounts;
   - BKT at every date: a balance sheet NCI line of dashes.

   Should comparative blocks and dash-only lines count? The BKT and ABN entries are already built.
3. **2026-06-30 flags** were taken from the 2025 annual report, because 2026 has no annual report of the same year (review Deviation 22).
4. **Value-1 citations:** SEB, SHB, SWED, INGA and DANSKE cite the interest expense line for subordinated liabilities, which also holds Tier 2 interest. None prints a policy line that names the AT1 coupon (Deviation 23).

## Housekeeping

The fresh clone folders C:\bpbs3, C:\bpbs3b and C:\bpbs3c can be deleted by hand. This session's safety check blocked their removal.

## git log origin/main --oneline -3

```
6eb4ce6 section 3: review updated for instruction 03c (stopped at step 3.7: BMPS and NDA 2026-06-30 at1_coupons, OPEN-34)
56292fe section 3: open questions OPEN-34 and OPEN-35
5dabeef step 3.7: coupon location, nci and NO yields
```
