# Status: instructions/04_section_4.md

## Outcome

**Stopped** under rule 4 at step 4.1. No k qualifies for the 2024 clusters, which kickoff 5.4 makes a stop (OPEN-36). Step 3.8 is complete, so Section 3 is closed. Steps 4.2, 4.3 and 4.4 are not built.

The fresh clone at ab3f25f passes 29 of 29 tests, and ruff is clean. The review is `review/section_4.md`.

## Last step reached

Step 4.1, code and tests only. Commits this session:

- **3.8:** da5d6e6
- **4.1:** 606dcb0
- **Open questions OPEN-36 to OPEN-38:** ab3f25f

## Results

- **Step 3.8:** 31 entries added, all value 0. BMPS at1_coupons at 12 dates and NDA at 2026-06-30 (status no_at1_coupon); 8 BKT minority_interests rows; 10 comparative rows for SANUK, DANSKE and ABN.
- **Provenance:** 10,967 of 10,967 report entries pass.
- **rote:** filled at 245 of 310 bank-dates (218 before), on both bases.
- **Amendments 28 to 32** are in CLAUDE.md; rule 14 was lifted for this step.
- **Step 4.1:** `bpb/peers.py` is built and its 3 tests pass. `outputs/tables/peers.csv` is not written.

## Stop reason

At year 2024, 29 banks have all 6 features. BARC, BNP, DBK, GLE and HSBA stay together as a cluster of 5 at every k, below min_cluster_size 6. The sizes are [24, 5], [15, 9, 5], [9, 8, 7, 5] and [9, 8, 5, 4, 3]. The result is the same on the underlying basis and with either missing value reading. 2023 and 2025 qualify only at k = 2. Changing min_cluster_size is a config change that rule 6 does not allow.

## Questions and blockers for the reviewer

1. **OPEN-36 (blocking):** set min_cluster_size to 5, or keep 6 and carry the previous year's clusters? Option (a) is measured in E4.1i.
2. **OPEN-37:** 4 unstated readings in the peer features. Under the mean of values present, 2025 also has no qualifying k.
3. **OPEN-38:** kickoff 5.6's O counts dividends twice, because other_income is a residual that already holds them. dividend_income also has no report row for 16 banks at 2025-12-31, including LLOY and SWED, so the joint hand check could not run as written. Please decide before step 4.3, and confirm the reading of "drivers that are not sized keep the bank's own value".
4. **Review Deviation 2:** the comparative rule was applied to dates OPEN-35 did not list: SANUK 2022-06-30 and 2022-12-31, DANSKE 2022-06-30, 2022-12-31 and 2023-12-31.
5. **Review Deviation 3:** 5 comparative rows have no printed amount, only no column or a blank cell. Do they fit A.1?

## Housekeeping

The safety check blocked removing C:\bpbs3, C:\bpbs3b and C:\bpbs3c, so they were left, as Section A allows. C:\bpbs4 from this session is also left. All 4 can be deleted by hand.

## git log origin/main --oneline -3

```
dfcc0ef section 4: review (stopped at step 4.1: no k qualifies for 2024, OPEN-36)
ab3f25f section 4: open questions OPEN-36 to OPEN-38
606dcb0 step 4.1: peer features, clusters and stability (stopped: no k qualifies for 2024, OPEN-36)
```
