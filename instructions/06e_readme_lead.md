# instructions/06e_readme_lead.md: README lead

This is 1 step, 6.9. It changes how the README's top paragraph is written and nothing else. Precedence (rule 13): this file beats every earlier instruction file on the points below.

## A. Why

The reviewer compared this repo's GitHub page with the owner's other finished repos. The reviewer has already pushed 2 fixes in commit f28cfae:
- badges matching the other repos;
- `.gitattributes` rules that take the generated HTML out of the language bar.

The README's opening lines still read worse than the other repos'. The headline uses the ticker `INGA's` and the ISO date `2026-06-30`, and it wraps the result in a qualifying clause. The other repos open with the result in bold, in plain words.

## B. Decisions

1. **Headline text.** `_headline` in `scripts/write_readme_tables.py` writes 2 sentences.

   The first sentence is bold and in this form:

   > **At 30 June 2026, {bank name} has the largest gap to the best quartile of its peers: {pts} RoTE points, or EUR {eur}m of annual pre tax profit.**

   The second sentence is in this form:

   > Each RoTE point was worth {last}x of price to tangible book at the end of {last year}, against {first}x at the end of {first year}, so the market now pays about {ratio} times as much for the same gap. Banks whose accounting scope differs between the 2 sources, mainly bank insurers, are left out of the headline (see Caveats).

   - **Bank name** is the `name` column of the universe, never the ticker.
   - **Dates in prose** read "30 June 2026", not "2026-06-30". This applies to this sentence only. Tables keep ISO dates.
   - **The ratio** is last ÷ first to 1 decimal. Say "about".
   - **Everything else** is as now: the same bank rule (instruction 06c B.2) and the same 2 decimals.

2. **Opening paragraph.** The sentence above the headline markers ("This project benchmarks 31 European banks...") moves below them. The README then opens with the bold result, as the other repos do.

3. **Data line.** Add 1 line after the outputs pointer: "Data: EBA EU wide transparency exercise, the banks' own annual, half year and Pillar 3 reports, ECB exchange rates and Yahoo Finance prices."

4. **answers.csv.** The headline claim follows the same wording.

## C. Step 6.9 (commit `step 6.9: readme lead`)

1. Apply B.
2. Run `bpb build` and regenerate the README tables. The edit to `scripts/` moves `spec_log.csv`'s `run_utc`, so the outputs commit with this step.
3. Check that `git status --porcelain` is empty after a second `bpb build`.
4. Push, and confirm that CI passes.

**Tests.** `test_tables_match` and `test_no_dashes` pass unchanged. All other tests pass.

## D. End

1. Run the fresh clone check.
2. Append step 6.9 to `review/section_6.md`, with the README's first 15 lines rendered as text and its size in bytes.
3. Push.
4. Write `instructions/06e_readme_lead.status.md`, commit it, push it and stop.
