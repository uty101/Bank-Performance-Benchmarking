# Status: instructions/06b_section_6_continue.md

## Outcome

**Completed.** Steps 6.0 to 6.5 are done, so Section 6, the last section, is complete. The review is `review/section_6.md`.

- **Fresh clone at 77c368f:** 62 of 62 tests pass with sockets disabled, and ruff is clean. The first suite run in that clone failed with `out of memory` under load, and the rerun passed. Both are in the review.
- **CI on 77c368f:** `success`, 62 passed, on Linux.
- **`bpb build` in the fresh clone:** `git status --porcelain` is empty, so every output is byte identical to the committed files.

## Last step reached

Step 6.5. Commits this session:

- **6.0:** 37f943f
- **6.1:** 735090e
- **6.2:** d4dcf83
- **6.3:** 80f09f1
- **6.4:** 43c346c
- **6.5:** 0dcaffd, 77c368f

## Results

- **Splits:** 2 found. 1 P/TBV changes: NWG at 2021-12-31, from 0.8668 to 0.8049.
- **2021 fit:** status `beta_ns_year`, with the implied CoE blank.
- **Slope stability:** F(4, 26) = 10.00, p = 0.00005, so the year slopes differ.
- **LLOY uplift at 2025-12-31:** +0.94x on the year's β, +0.31x on the pooled β.
- **ISP and KBC:** every line is in the right field, and the lines with no field reconcile to other_below_line, so no entry changed. It is the insurance effect: −7.85 and −10.11 RoTE points at 2026-06-30.
- **Waterfalls:** 29 of 31 banks have one. CAG and BPE have none at any date, and their panels say why.
- **Outputs:** 31 profiles, 102 league CSVs, 17 HTML pages, `answers.csv`, `lineage.csv` and `lineage_derived.csv`.
- **README:** 14,388 bytes.

## Stop reason

None.

## Questions and blockers for the reviewer

No blockers. To confirm or correct:

1. **The README's headline gap is CAG's** (EUR 19.9bn), a bank insurer with a scope caveat and a blank joint RoTE gap. Is it the right lead?
2. **`spec_log.csv` gained a trailing `status` column,** because 06b B.2 asks for status `no_git` and the schema has none (Deviation 3).
3. **League tables:** underlying basis, and a cluster file ranks all 31 banks together, with each verdict against the bank's own cluster (Deviation 4).
4. **README readings:** Q2 is the 10 banks with the largest joint gap, and Q3 is the largest gaps in either direction (Deviation 5).

Things to know:

- **The dashboard has no test.** The test I added needs a socket, which rule 7 forbids, so I removed it. It passed a smoke run outside pytest, and it was never opened in a real browser.
- **A trace of a gap or driver stops at the bank's own inputs,** and does not list the peers behind a target.
- **I committed step 6.3 before reading its test result,** which had failed with `OSError: [Errno 22]`. It was not pushed. Memory pressure is the likely cause, but this error was not reproduced.
- **Peak memory of a build was not measured,** and a build can fail on a machine short of memory.

## Housekeeping

C:\bpbs6, C:\bpbs6b and C:\bpbs6c join the other `C:\bpbs*` folders for the owner to delete.

## git log origin/main --oneline -3

```
7d84701 section 6: review with both fresh clone runs
31f34ae section 6: status of instruction 06b (completed)
a61681d section 6: review of the whole section
```
