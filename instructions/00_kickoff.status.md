# Status: instructions/00_kickoff.md (session 0)

## Outcome

Completed.

## Last step reached

Step 0.0, plan and scaffolding (7e06f94). Review file `review/section_0.md` committed as 295b725. No data was pulled and no analysis code was written.

## Stop reason

None.

## Questions and blockers for the reviewer

Sixteen items are open in `decisions/OPEN.md`, each with 2 options; none was decided. Section 1 is blocked on some of them:

- OPEN-01 and OPEN-02 block step 1.1.
- OPEN-06 and OPEN-07 affect step 1.6.
- OPEN-03 to OPEN-05 shape `config/source_map.yaml`.

The full list:

1. OPEN-01: where the 2021 to 2023 EBA URLs are recorded before the download runs.
2. OPEN-02: step 1.1 filters by LEI before step 1.2 fills any LEI; no staging path is fixed for the unfiltered originals.
3. OPEN-03: EU report rows at 2024-12-31 and 2025-06-30 as opening balances and rolling components, against "seam test only".
4. OPEN-04: the `p3` or `report` family for the remaining EU bridge capital and liquidity fields, and for UK capital fields.
5. OPEN-05: lcr and nsfr for EU banks before 2025-06-30.
6. OPEN-06: the income identity components for EBA rows.
7. OPEN-07: no field for the reported CET1 ratio (check 4).
8. OPEN-08: `peers.features` lacks rates.
9. OPEN-09: `benchmark` lacks the market grouping.
10. OPEN-10: `valuation.uplift` inputs.
11. OPEN-11: GLEIF lookup under rule 8.
12. OPEN-12: evaluating the formulas in `hand_check.xlsx`.
13. OPEN-13: unfixed output paths.
14. OPEN-14: the trace and README tests against rule 7.
15. OPEN-15: unfixed test inputs.
16. OPEN-16: the column position of `lei` in `universe.csv`.

Other notes for the reviewer:

- `pytest -p socket --disable-socket` emits a `PytestAssertRewriteWarning`, because pytest-socket is already autoloaded. The tests pass and sockets are disabled. The command was left as fixed by rule 7.
- Session 0 used 3 commits:
  1. `step 0.0`
  2. `section 0: review`, pushed
  3. this status commit, pushed second

  This follows rule 11 and WORKFLOW Part 2 step 5, so the log below reflects the pushed section.
- CI has not been observed running yet; it triggers on these pushes.

## git log origin/main --oneline -3

```
295b725 section 0: review
7e06f94 step 0.0: plan and scaffolding
cf54b6a Add workflow, final project outline and session 0 kickoff
```
