# Section 5 review decisions

Written in step 6.0 from `instructions/06_section_6.md` Sections A and A.1, verbatim, with OPEN-42 settled by `instructions/06b_section_6_continue.md` B.1.

---

## A. Approval of Section 5

Section 5 is approved once step 6.0 is done.

The reviewer read `valuation_fits.csv` in full. The yearly fits tell a clear story:

| year | β | R² | implied CoE |
|---|---|---|---|
| 2022 | 4.5 | 0.48 | 24% |
| 2024 | 6.6 | 0.55 | 17% |
| 2025 | 10.4 | 0.74 | 11.6% |

The market has been paying more for each point of RoTE every year. That is a finding for the README. It also means a pooled fit with 1 slope is the wrong model for anything but the significance gate.

### A.1 Decisions

1. **Prices must not be split adjusted.** yfinance's `Close` is adjusted for splits and consolidations even with `auto_adjust=False`. shares_out comes from the reports as printed, so the 2 do not match across a split. NWG (share consolidation, 2022) and BMPS (reverse split, 2022) are the likely cases. BMPS is also named in Cook's distance in 2022 to 2024.

   Fix:
   - Pull `Ticker(t).history(..., actions=True)` and store the `Stock Splits` column in `data/raw/market/splits.csv` (ticker, date, ratio).
   - The unadjusted price at date t = Close(t) × the product of every split ratio dated after t. A consolidation has a ratio below 1.
   - **Test `tests/test_market.py::test_unsplit`:** a synthetic series with a 1:10 consolidation dated mid series gives the pre consolidation unadjusted prices at 10 times the adjusted ones.
   - **Review evidence:** every split row found, and the P/TBV before and after the fix for every bank and year it touches.

2. **Year fits that are not significant.** When the 90% interval of a year's β contains 0, that year's `coe_implied` is blank, with status `beta_ns_year`. That applies to 2021: β 1.04 with se 1.54 gives a "CoE" of 98%, which is meaningless.

3. **Slope stability.**
   - **Test:** add a pooled fit with year dummies and rote × year interactions, standard errors clustered by bank, and an F test (Wald) that the year slopes are equal.
   - **Output:** write the F statistic, its degrees of freedom and its p value to `outputs/tables/valuation_stability.csv`.
   - **Uplift:** the uplift stays on the year's own fit, which is the market's pricing at that date. Add a trailing column `uplift_pooled_ptbv` to VALUATION (a reviewer schema change): the uplift on the pooled β, so the README can show both.
   - **Pooled β:** it still sets the significance gate.

4. **Bank insurers' OTH/A.** In the review, print the income statement lines between total operating income and pbt, as entered, for ISP and KBC at 2025-12-31 and 2026-06-30, with each line's page. If a line was entered in the wrong field, fix the entry. If the lines are right, the size of `other_below_line` is the insurance effect. The README will say so.

5. **Profile waterfall date.** The profile waterfall uses the latest date at which the bank has a decomposition, printed in the panel title. If there is none at any date, the panel states why.

6. **F/A stays a Shapley driver.** Decomposition explains where a RoTE gap comes from. Business mix is a legitimate part of that explanation. Sizing (Section 4) is where mix must not count as opportunity. The README states this split in 1 sentence.

7. **NII year on year coverage** of 10 of 62 rows at 2025-12-31 is accepted. That is amendment 17 working as intended.

8. **OPEN-39: (a).**

9. **OPEN-40: (a).**

10. **OPEN-41.** `spec_log.csv` is rewritten on every build, not appended. It holds 1 row per fit specification run in that build. Its `run_utc` holds the committer date of `HEAD` (`git log -1 --format=%cI`), so a build of a given commit is byte identical. The 18 accumulated rows are replaced. Rule 9 then holds, with no exemption.
