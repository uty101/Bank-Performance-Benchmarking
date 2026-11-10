# Status: instructions/06e_readme_lead.md

## Outcome

**Stopped** under rules 4 and 5 at step 6.9. Instruction 06e B is applied and committed, but README.md is 15,332 bytes, so `test_tables_match` fails on its 15,000 byte check. 06e says that test passes unchanged, and rule 5 forbids changing it (OPEN-48). Everything else passes: 64 passed, 1 failed, on CI, locally and on the fresh clone. ruff is clean.

`main` was already red before this step. Commit f28cfae's badges took the README from 14,844 to 15,020 bytes, and CI run 42833253149 failed on the same check.

## Last step reached

Step 6.9, up to the stop. Then the fresh clone check, the review and this file. Commits this session:

- **6.9:** 849b84c
- **Review:** 888aeb9

Not done: the second `bpb build` check (C.3) and a passing CI (C.4). Both wait for OPEN-48.

## Results

- **The lead** now opens: "**At 30 June 2026, ING Groep has the largest gap to the best quartile of its peers: 10.20 RoTE points, or EUR 6,926m of annual pre tax profit.**" The valuation sentence follows: 0.104x at the end of 2025 against 0.045x at the end of 2022, "about 2.3 times as much", then the scope sentence.
- **The opening sentence** sits below the headline markers, and the data line follows the outputs pointer.
- **answers.csv:** the headline row uses the same wording.
- **README size:** 15,332 bytes. Q5 already lists only the fields at least 15 banks report (06c B.2 item 5), so the rule on record has nothing left to cut.

## Questions for the reviewer

1. **OPEN-48 (blocking):** how should the README get back under 15 KB?
   - (a) Raise `Q5_MIN_BANKS` from 15 to 24. Q5 then lists 21 fields, the README is 14,978 bytes and there are 22 bytes of headroom.
   - (b) Keep Q5 and raise `LIMIT` in `tests/test_readme.py`, for example to 16,000.

   The measured sizes at other thresholds are in E6.9b of `review/section_6.md`.

## Notes

- **The valuation multiples** keep 3 decimals (0.104x, 0.045x), as before. At 2 they would read 0.10x and 0.05x, and the stated ratio, 2.3, would not follow from them.
- **The step 6.9 commit** includes `decisions/OPEN.md` with OPEN-48, as the 06c stop at step 6.6 did.
- **Housekeeping:** `C:\bpbs6f` joins the other `C:\bpbs*` folders for the owner to delete.

## git log origin/main --oneline -5

```
888aeb9 section 6: review of step 6.9 (stopped, OPEN-48)
849b84c step 6.9: readme lead (stopped: README over 15 KB, OPEN-48)
18df1dd instruction 06e: README lead
f28cfae repo polish: badges to match the other repos, generated HTML out of the language bar
f83c81a decisions: section 6 final review, OPEN-47 (b)
```
