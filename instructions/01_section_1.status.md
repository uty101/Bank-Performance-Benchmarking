# Status: instructions/01_section_1.md (session 1)

## Outcome

Stopped.

## Last step reached

Step 1.2, EU LEIs and EBA field maps (e028dab). Steps 1.0 (117db5a) and 1.1 (5eeb4e2) are complete. Step 1.3 was started but not committed. Steps 1.4 to 1.7 were not started. The review is `review/section_1.md` (0c5a655).

## Stop reason

Rules 4 and 5, at step 1.3. `test_load_eba_synthetic` must check "value scaling per the release's unit (read the unit from `SDD.xlsx` ...)". No `SDD.xlsx` from 2021 to 2025 states a unit, and neither does any `TR_Metadata.xlsx`. Every cell and comment was searched.

The unit is printed only in each release's `Mapped_templates.xlsx` headings and in the bank PDFs, as `(mln EUR)` or `(mln EUR, %)`. The data confirm that EBA amounts are EUR millions for every bank, including DNB, Danske, SEB, SHB and Swedbank, which report in NOK, DKK and SEK. That conflicts with Convention 4.1 (units of the reporting currency). Choosing another unit source, or converting those banks out of EUR, is a design choice. The evidence and 2 options are OPEN-25 in `decisions/OPEN.md`, and the raw rows are under "Stop evidence: OPEN-25" in the review.

## Questions and blockers for the reviewer

Each item has 2 options in `decisions/OPEN.md`.

1. **OPEN-25 (blocks steps 1.3 to 1.7):** the source of the EBA unit, and whether `eba` rows stay in EUR for SEK, NOK and DKK banks or are converted to `report_ccy`.
2. **OPEN-17:** DBK has no unique name match. 5 2025 names contain "deutsche", and `DEUTSCHE BANK AKTIENGESELLSCHAFT` is 7LTWFZYICNSX8D621K86. DBK's `lei` is blank.
3. **OPEN-18:** `cet1`, transitional (2520102) or fully loaded (2520143). This blocks cet1_ratio and check 4.
4. **OPEN-19:** `cet1_ratio_reported`, transitional (2520140) or fully loaded (2520146). 2025 adds a pre-floor ratio (2520155).
5. **OPEN-20:** `leverage_exposure`, transitional (2520903) or fully phased-in (2520904). This blocks leverage_ratio.
6. **OPEN-21:** `debt_securities` has no all-portfolio carrying amount line. This blocks iea and nim.
7. **OPEN-22:** `loans_customers_gross` and `loans_customers_allowance` need a sum over Exposure (and Perf_Status) rows, and the map format has 1 row per field. This blocks cost_of_risk and loan_deposit.
8. **OPEN-23:** `deposits_customers` needs a sum over 4 counterparty sectors. This blocks loan_deposit.
9. **OPEN-24:** `minority_interests` has no EBA line. This blocks tangible_equity in Section 3.

Other notes:

- **Instruction path that returned 404.** The 2021 release page path in instruction 01 (`.../2021-eu-wide-transparency-exercise`) returns 404. The EBA hub links the release as `.../eu-wide-transparency-exercise/2021-eu-wide-transparency`, and that page was used. The 2025 files are linked from the hub page itself, so the hub is recorded as the 2025 release page.
- **Data coverage.** DNB's first EBA date is 2022-06-30. BPER is not in the 2021 release. Rabobank reports only at 30 Jun and 31 Dec in the 2021 to 2023 releases.
- **Uncommitted draft.** Drafts of `bpb/config.py` and `bpb/lineage.py` (step 1.3) were written, then taken out of the repo when the session stopped. Nothing from step 1.3 is committed.
- **Pushes.** There were 3 pushes: the step commits (so that the fresh-clone check clones the pushed repo, rule 12), the review, then this file.
- **Fresh-clone check.** A clone from GitHub at e028dab passed: ruff clean, `3 passed`.

## git log origin/main --oneline -3

```
0c5a655 section 1: review (stopped at step 1.3, OPEN-25)
e028dab step 1.2: EU LEIs from the 2025 release and EBA field maps
5eeb4e2 step 1.1: EBA download, country filter and manifest
```
