# Status: instructions/04b_section_4_continue.md

## Outcome

**Completed.** Steps 4.0b and 4.1 to 4.4 are done, so Section 4 is complete. The review is `review/section_4.md`.

- 41 of 41 tests pass locally and in the fresh clone at d90f7eb, and ruff is clean.
- Running `scripts/run_all.py` again left every committed output byte identical, and the 3 PDFs rebuild to the same hash.

## Last step reached

Step 4.4. Commits this session:

- **4.0b:** f94e098
- **4.1:** 19dd997
- **4.2:** 5b1c2ab
- **4.3:** 09a87e0
- **4.4:** d90f7eb

## Results

- **Decision 5:** all 5 rows of Deviation 3 meet a rule, so none is removed (E4.0b).
- **Peers:** k = 3 in 2023 (silhouette 0.2469), and k = 2 in 2024 (0.3085) and 2025 (0.2932). BARC, BNP, DBK, GLE and HSBA are cluster 1 in every year. ARI is 0.366 for 2023 to 2024 and 1.0 for 2024 to 2025. 5 banks are borderline in 2025 and none earlier. LLOY and SANUK are `assigned_nearest` in every year.
- **BENCH:** 31,620 rows. Status counts by group are in E4.2b, and the cost of the small groups is in E4.2c and E4.2d.
- **GAPS:** 7,440 rows, of which 4,061 are `not_sized`.
- **Hand check:** LLOY, ISP and SWED all use the cluster group. Every formula matches `size_gaps` within tolerance (E4.3g).
- **Profiles:** LLOY, ISP and SWED at 2026-06-30, embedded in the review.

## Stop reason

None.

## Questions and blockers for the reviewer

No blockers. To confirm or correct (review, Open questions):

1. **Negative overlap:** where NIM and fee gaps are both sized, F′ rises with NII′, so the joint gap can exceed the sum of the standalones (CABK, KBC, SWED at 2026-06-30). This follows the formula. Is it intended?
2. **Broad cluster 2:** with 26 banks, retail heavy banks show large fee gaps (LLOY EUR 7.4bn). This may need a README caveat.
3. **Joint gap blank** where a sized fee gap meets a blank NIM, since O needs NII: BKT, DNB, SHB and UCG at 2026-06-30, cluster group, underlying basis.
4. **8 readings the instructions leave open,** listed in the review. The main ones: t̄ at 30 Jun uses 3 rolling periods; t̄ with fewer than 3 years is blank, not the fallback; T̄E comes from the rote row, so ΔRoTE is blank where rote's numerator alone is missing.
5. **`target_interval`** applies the Harrell Davis weights directly instead of calling `hdquantiles` per draw, for speed. A test shows they agree to 1e-12 (Deviation 7).

## Housekeeping

- pycel moved networkx from 3.7 to 2.6.3 in the lock, because it requires networkx below 2.7.
- `tests/test_gaps.py` takes about 7 minutes, and the full suite 8 to 11.
- C:\bpbs4b from this session joins the other `C:\bpbs*` folders for the owner to delete.

## git log origin/main --oneline -3

```
9db9a38 section 4: review rewritten for the whole section
d90f7eb step 4.4: first profiles for LLOY, ISP and SWED
09a87e0 step 4.3: gap sizing and the hand check
```
