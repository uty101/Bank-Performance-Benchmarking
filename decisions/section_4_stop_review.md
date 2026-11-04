# Section 4 stop review decisions

Written in step 4.0b from `instructions/04b_section_4_continue.md` Sections A and B, verbatim.

---

## A. Review

The stop was correct. The reviewer's `min_cluster_size` of 6 does not fit a universe of 31.

The measurement in E4.1i shows the structure in the data:

- The same 5 banks (BARC, BNP, DBK, GLE and HSBA) form their own cluster in every year at every k. These are the trading heavy global banks.
- The other 26 split only weakly: silhouette 0.19 to 0.31.

That is a real finding. It shows that business mix separates the investment bank heavy groups from everyone else, and not much more. The README will say so.

Section 3 is closed. Step 3.8 and amendments 28 to 32 are accepted.

## B. Decisions

1. **OPEN-36: (a), plus one change.** Reviewer changes to `config.toml`:
   - `min_cluster_size` = 5;
   - `min_peers` = 4.

   Without the second change, every bank in the 5 bank cluster would have 4 peers, fall below `min_peers` and get no cluster benchmark at all. With 4 peers the Harrell Davis target and its interval are noisy. The intervals will show it, and wide intervals mean more gaps fall inside the noise and go unsized, which is the honest outcome. The change also lets the UK and Italy market groups (4 others each) produce benchmarks. Record both changes in `decisions/section_4_stop_review.md`.

2. **OPEN-37: the 4 feature readings.**
   1. **Years present: (b) with a floor.** A feature is the mean of the values present at the 3 year ends, if at least 2 are present; otherwise it is missing. Status `two_of_three` where only 2 are present. DNB in 2023 therefore uses 2022 and 2023.
   2. **fee_share basis: (a) reported.** Features describe business mix, not performance.
   3. **Status column: (a).** Add a trailing `status` column to PEERS. This is a reviewer schema change; record it in CLAUDE.md Amendments.
   4. **Standardisation: (a).** Standardise again within each stability draw. The draw then repeats the whole method, standardisation included.

   If any year still has no qualifying k under these readings, stop again and print the sizes.

3. **OPEN-38: (a), O = other_income.** other_income is the residual and already holds dividends, so adding dividend_income counted them twice. That was the reviewer's error in kickoff 5.6. I = NII + F + O now holds by construction.

   The reading of "drivers that are not sized keep the bank's own value" is confirmed, in levels:
   - If the fee gap is not sized, F′ = F.
   - If the cost to income gap is not sized, C′ = C, so costs do not rise because income rose.
   - If the cost of risk gap is not sized, LLP′ = LLP.
   - If the NIM gap is not sized, NII′ = NII.

   With these, `test_joint_single` holds on real data.

4. **Deviation 2 is accepted.** The comparative rule is general, and applying it to dates OPEN-35 did not list is correct.

5. **Deviation 3.** For each of the 5 rows, keep it only if it meets one of these:
   - the no non controlling interests rule of 03c decision 2: no balance sheet line and no column in the statement of changes in equity;
   - the dash rule: a printed row whose cell is a dash or blank.

   Remove any other row and list it in the review.

6. **Housekeeping.** The owner will delete the `C:\bpbs*` folders by hand.
