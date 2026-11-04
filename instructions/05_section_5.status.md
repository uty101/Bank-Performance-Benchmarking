# Status: instructions/05_section_5.md

## Outcome

**Completed.** Step 4.5 and steps 5.1 to 5.3 are done, so Section 5 is complete. The review is `review/section_5.md`.

- 52 of 52 tests pass locally and in the fresh clone at 34e49f1, and ruff is clean.
- Running `scripts/run_all.py` twice left 23 output files and `facts.parquet` byte identical. `spec_log.csv` is the exception (OPEN-41).

## Last step reached

Step 5.3. Commits this session:

- **4.5:** 2412466
- **5.1:** f92173b
- **5.2:** 4349b91
- **5.3:** 34e49f1
- **Review:** b180337

## Results

- **Step 4.5:** fee_share is no longer sized. LLOY's joint gap at 2026-06-30 falls from EUR 9.0bn to EUR 4.7bn, and from 16.4 to 8.5 RoTE points. GAPS has 5,580 rows, and `short_history` is gone. The hand check passes without the fee lines.
- **DRIVERS:** 9,920 rows. Per basis and run: 206 `ok`, 13 `rote_blank`, 2 `loss_year`, 47 `missing_input`, 32 `too_few_peers`, 10 `merger_break`.
- **yoy.csv:** 992 rows, with 140 `family_switch` and 10 `merger_break`.
- **Fits:** β rises from 1.04 in 2021 to 10.43 in 2025 (n 25, R² 0.74, implied CoE 11.6%). The pooled β is 3.45, with a 90% interval of 1.75 to 5.15, so the uplifts are not blanked.
- **LLOY uplift at 2025-12-31:** +0.94x, interval +0.72x to +1.16x.
- **Profiles:** both panels are filled for LLOY and ISP. SWED's valuation panel is filled and its waterfall panel states the blank.

## Stop reason

None.

## Questions and blockers for the reviewer

No blockers. To confirm or correct (review, Open questions):

1. **The uplift rests on the highest β of the 5 years,** about 3 times the pooled β. LLOY would be about +0.31x on the pooled β.
2. **Bank insurers distort OTH/A.** ISP's and KBC's other_below_line bars are −7.9 and −10.1 points at 2026-06-30, and the same treatment flatters ISP's cost_income. This is the insurance treatment of amendment 21. The line by line cause was not traced.
3. **SWED has no waterfall** because minority_interests has no row at 30 Jun since 2024. 11 of 31 banks have no decomposition at 2026-06-30: 8 from missing inputs and 3 from merger breaks.
4. **F/A stays a Shapley driver,** and is LLOY's largest bar at −7.0 points, though A.1 item 1 calls that gap business mix.
5. **`nii` year on year rows** are filled for only 10 of 62 at 2025-12-31, under amendment 17.
6. **OPEN-39** (too few peers in a driver reference), **OPEN-40** (`basis` in DRIVERS) and **OPEN-41** (`spec_log.csv` against rule 9) need a decision. The code applies the first option of OPEN-39 and OPEN-40 for now. OPEN-41 must be settled before step 6.3.

Not verified: split adjustment of prices (NWG at 2021-12-31 is the likely case), and the cause of the largest minorities_and_at1_pts values.

## Housekeeping

- A.1 item 2 (the README sentence on cluster 2) waits for step 6.4.
- `spec_log.csv` holds 18 rows from this session's 3 full runs.
- C:\bpbs5 from this session joins the other `C:\bpbs*` folders for the owner to delete.

## git log origin/main --oneline -3

```
b180337 section 5: review
34e49f1 step 5.3: valuation and the 2 profile panels
4349b91 step 5.2: year on year changes
```
