# instructions/06b_section_6_continue.md: continue Section 6

Resume at step 6.0 and build steps 6.0 to 6.5 as written in `instructions/06_section_6.md`, with the decisions below. Precedence (rule 13): this file beats instruction 06.

## A. Review

The stop was correct. The reviewer's test had the direction wrong.

In a 1:10 consolidation, 10 old shares become 1 new share. The pre consolidation price is therefore one tenth of the adjusted series. The formula in A.1 item 1 is right, and the test was wrong.

The NWG evidence confirms it: 270.20p adjusted × 13/14 = 250.90p, against 249.00p on the day after.

The split fix turns out small:
- 2 splits are found;
- 1 P/TBV changes (NWG at 2021-12-31, from 0.8668 to 0.8049);
- BMPS's Cook's distance namings are not explained by it.

That settles the question honestly.

## B. Decisions

1. **OPEN-42: keep the formula and correct the test.** `test_unsplit` asserts that pre consolidation unadjusted prices equal the adjusted prices × 0.1 for a 1:10 consolidation (ratio 0.1). Add a second case: a 2:1 split (ratio 2) gives pre split prices at 2 times the adjusted ones. This is a reviewer correction to a reviewer written test, allowed here.

   **BMPS rights issue.** Note in the README caveats that BMPS's earlier prices may carry a rights issue adjustment that `Stock Splits` does not undo. It touches no P/TBV, since BMPS's 2021 tbvps is blank.

2. **OPEN-43.** `run_utc` in `spec_log.csv` is the committer date of the last commit that touched any build input. It is read with:

   ```
   git log -1 --format=%cI -- data/raw data/manual config config.toml bpb scripts
   ```

   A commit of outputs alone does not change it, so `bpb build` followed by `git status --porcelain` is empty. If git is not available (a tarball), the field is blank with status `no_git`. There is no exemption from rule 9.

3. **OPEN-44.** The trace test checks 2 things against the cited page text:
   - the snippet, with any leading note matching `^component \d+/\d+: ` removed;
   - `value_as_printed`, under the provenance normalisation of kickoff 5.3 item 1.

   Both must be found. Do not rewrite the snippets in `report_entries.csv`.

4. **Housekeeping.** `C:\bpbs6` joins the other folders the owner will delete.

## C. Steps

### Step 6.0

As in instruction 06, with B.1.

**Review evidence:**
- both split rows;
- the NWG and BMPS prices either side of each split, adjusted and unadjusted;
- every P/TBV that changes.

### Steps 6.1 to 6.5

As in instruction 06, with B.2 in step 6.3 and B.3 in step 6.2.

The partial rule applies.

## D. End

1. Run the fresh clone check.
2. Rewrite `review/section_6.md` for the whole section.
3. Push.
4. Write `instructions/06b_section_6_continue.status.md`, commit it, push it and stop.
