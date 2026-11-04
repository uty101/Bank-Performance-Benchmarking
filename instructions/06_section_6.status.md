# Status: instructions/06_section_6.md

## Outcome

**Stopped** under rules 4 and 5 at step 6.0. The test specified in A.1 item 1 contradicts the formula it tests (OPEN-42). No code, data or output changed. Section 5 stays unapproved until step 6.0 is done.

The fresh clone at a485b37 passes 52 of 52 tests, and ruff is clean. The review is `review/section_6.md`.

## Last step reached

Step 6.0, started and not committed. Steps 6.1 to 6.5 were not run. Commits this session:

- **Review and OPEN-42 to OPEN-44:** 1e375c0

## Stop reason

A.1 item 1 sets the unadjusted price to Close(t) × the product of later split ratios, with a consolidation's ratio below 1. A 1:10 consolidation has ratio 0.1, so pre consolidation prices come out at 1/10 of the adjusted ones. `test_unsplit` is specified to assert 10 times the adjusted ones. Rule 5 says to stop when a test in the instruction is wrong, and not to rewrite it.

The data support the formula. NWG.L closes at 270.20p on 2022-08-26 and 249.00p on 2022-08-30. The formula gives 250.90p before the consolidation, and the test's direction gives 290.98p.

## Questions and blockers for the reviewer

1. **OPEN-42 (blocking):** keep the formula and assert 1/10 in the test, or keep the test and divide by the ratio? The evidence favours the first.
2. **OPEN-43 (before step 6.3):** `spec_log.csv` is committed, so `run_utc` as `HEAD`'s committer date changes with every later commit, and `git status` cannot be empty after `bpb build`. Use the last commit touching the build's inputs, or exempt the file?
3. **OPEN-44 (before step 6.2):** 4,783 of 10,967 snippets start with a `component n/m:` note that is not on the page, so `test_trace_sample` fails on them as written. All 4,783 match once the note is dropped. Drop the note in the test, or check `value_as_printed` instead?

For information, the split fix is small:

- yfinance shows 2 splits: NWG on 2022-08-30 (ratio 13/14) and BMPS on 2022-09-26 (ratio 0.01).
- Only 1 P/TBV changes: NWG at 2021-12-31, from 0.8668 to 0.8049.
- BMPS at 2021-12-31 has no tbvps, so it stays blank. BMPS's Cook's distance namings in 2022 to 2024 all fall after its split, so the fix cannot explain them.
- BMPS's 2021 price may also carry a rights issue adjustment that `Stock Splits` does not undo. This is not verified, and it affects no P/TBV.

## Housekeeping

The safety check blocked removing C:\bpbs6 from this session, so it joins the other `C:\bpbs*` folders for the owner to delete.

## git log origin/main --oneline -3

```
1e375c0 section 6: review (stopped at step 6.0: test_unsplit contradicts its formula, OPEN-42)
a485b37 Add instructions for section 6
5a524ea section 5: status of instruction 05 (completed)
```
