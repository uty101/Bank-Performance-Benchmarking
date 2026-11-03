# Status: instructions/03b_section_3_completion.md

## Outcome

**Stopped** under rule 4 at step 3.6. `tests/test_yields.py::test_coverage` fails for NO at 2025-12: Norges Bank's monthly 10 year series has no December 2025 value, and filling it would be a design choice (OPEN-31).

Step 3.5 is complete. Step 3.6 is complete for the other 10 countries. The review is `review/section_3.md` (42145f7), rewritten for the whole section.

## Last step reached

Step 3.6. Commits this session:

- **3.5:**
  - at1_in_equity UK: deb80cb
  - at1_in_equity EU: e89d51c
  - decisions 3 to 6 and rote recomputed: e7bef6e
- **3.6:** 10aa994
- **Open questions OPEN-32 and OPEN-33:** 9e19da4
- **Review:** 42145f7

## Results

- **at1_in_equity:** 354 entries.
  - 0 (AT1 as a liability, or none in equity):
    - SEB, SHB, SWED, INGA, SAN, BBVA, CABK, SAB, BKT and BMPS at every entered date;
    - DANSKE from 2022-06-30;
    - NDA from 2025-06-30.
  - 1 everywhere else.
  - Left out: GLE before 2023-12-31, CAG before 2024-12-31 and BKT's H1 2021 to H1 2024.
- **Decisions 3 to 5:** 133 entries.
  - 19 net-of-tax coupons;
  - 104 headcount entries in fte;
  - 2 SANUK profit_owners with no_nci_line;
  - 8 true FTEs, for BAMI at each 31 Dec and KBC at 2024 and 2025.
- **One offs:** 40 removed under decision 6, leaving 576. Every row passes provenance.
- **Provenance:** 10,561 of 10,561 report entries pass.
- **rote:** filled at 213 of 310 bank-dates (reported basis), up from 165. The hand checks match `kpi.csv`:
  - LLOY at 2025-12-31: 0.120589;
  - BBVA at 2024-12-31: 0.192974 under the at1_liability rule.
- **Yields:** 11 countries from ECB, BoE (IUMAMNPY) and Norges Bank (GOVT_GENERIC_RATES M.10Y.GBON), 2020-01 to 2026-07. NO is missing 2025-12.
- **Tests:** 25 pass and 1 fails (test_coverage), and ruff is clean. The fresh clone at 9e19da4 gives the same result.

## Stop reason

Norges Bank `https://data.norges-bank.no/api/data/GOVT_GENERIC_RATES/M.10Y.GBON.?format=csv&startPeriod=2020-01&endPeriod=2026-07&locale=en` returns 2025-11 (4.074) and 2026-01 (4.174), but no 2025-12 row. The business-day series `B.10Y.GBON` has every December 2025 business day. Averaging it into a monthly value would be a design choice, so it is OPEN-31. The test was not changed, skipped or marked.

## Questions and blockers for the reviewer

1. **OPEN-31:** NO 2025-12. Use the mean of Norges Bank's business-day series, or name another monthly source.
2. **OPEN-32:** SAN, BBVA, CABK, SAB and BKT book AT1 as a liability but charge the coupons to reserves. Their EPS notes deduct them, so their profit_owners is not net of the coupons. Applied as written, the B.2 rule overstates their rote. Should the rule apply to the tangible_equity term only for these 5 banks?
3. **OPEN-33:** these banks print no non-controlling interests line, so minority_interests is missing and rote is blank at those dates. Should it be 0 with a status?
   - SEB, DANSKE and BKT;
   - NDA from 2022-06-30;
   - SWED at the 30 June dates from 2024;
   - SANUK from 2022-06-30.
4. **rote far from rote_reported** at 2025-12-31: BAMI is -5.4 pts and BMPS -6.0 pts (review E3b.5).
5. **Weak at1_in_equity citations:** these are half year reports that never name the AT1 classification. They are listed in Open question 5 of the review.

## git log origin/main --oneline -3

```
42145f7 section 3: review rewritten for the whole section (stopped at step 3.6: NO 2025-12 yield missing)
9e19da4 section 3: open questions OPEN-32 and OPEN-33
10aa994 step 3.6: yields from ECB, BoE and Norges Bank; NO 2025-12 missing (rule 4 stop)
```
