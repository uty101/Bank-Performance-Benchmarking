# instructions/06_section_6.md: Session 6 instructions for Claude Code

Apply the Section 5 review decisions as step 6.0, then build all of Section 6 of `PLAN.md` (steps 6.1 to 6.5) with the amendments below. This is the last section. Precedence (rule 13): this file beats `PLAN.md`, which beats the kickoff.

---

## A. Approval of Section 5

Section 5 is approved once step 6.0 is done.

The reviewer read `valuation_fits.csv` in full. The yearly fits tell a clear story:

| year | β | R² | implied CoE |
|---|---|---|---|
| 2022 | 4.5 | 0.48 | 24% |
| 2024 | 6.6 | 0.55 | 17% |
| 2025 | 10.4 | 0.74 | 11.6% |

The market has been paying more for each point of RoTE every year. That is a finding for the README. It also means a pooled fit with 1 slope is the wrong model for anything but the significance gate.

### A.1 Decisions

1. **Prices must not be split adjusted.** yfinance's `Close` is adjusted for splits and consolidations even with `auto_adjust=False`. shares_out comes from the reports as printed, so the 2 do not match across a split. NWG (share consolidation, 2022) and BMPS (reverse split, 2022) are the likely cases. BMPS is also named in Cook's distance in 2022 to 2024.

   Fix:
   - Pull `Ticker(t).history(..., actions=True)` and store the `Stock Splits` column in `data/raw/market/splits.csv` (ticker, date, ratio).
   - The unadjusted price at date t = Close(t) × the product of every split ratio dated after t. A consolidation has a ratio below 1.
   - **Test `tests/test_market.py::test_unsplit`:** a synthetic series with a 1:10 consolidation dated mid series gives the pre consolidation unadjusted prices at 10 times the adjusted ones.
   - **Review evidence:** every split row found, and the P/TBV before and after the fix for every bank and year it touches.

2. **Year fits that are not significant.** When the 90% interval of a year's β contains 0, that year's `coe_implied` is blank, with status `beta_ns_year`. That applies to 2021: β 1.04 with se 1.54 gives a "CoE" of 98%, which is meaningless.

3. **Slope stability.**
   - **Test:** add a pooled fit with year dummies and rote × year interactions, standard errors clustered by bank, and an F test (Wald) that the year slopes are equal.
   - **Output:** write the F statistic, its degrees of freedom and its p value to `outputs/tables/valuation_stability.csv`.
   - **Uplift:** the uplift stays on the year's own fit, which is the market's pricing at that date. Add a trailing column `uplift_pooled_ptbv` to VALUATION (a reviewer schema change): the uplift on the pooled β, so the README can show both.
   - **Pooled β:** it still sets the significance gate.

4. **Bank insurers' OTH/A.** In the review, print the income statement lines between total operating income and pbt, as entered, for ISP and KBC at 2025-12-31 and 2026-06-30, with each line's page. If a line was entered in the wrong field, fix the entry. If the lines are right, the size of `other_below_line` is the insurance effect. The README will say so.

5. **Profile waterfall date.** The profile waterfall uses the latest date at which the bank has a decomposition, printed in the panel title. If there is none at any date, the panel states why.

6. **F/A stays a Shapley driver.** Decomposition explains where a RoTE gap comes from. Business mix is a legitimate part of that explanation. Sizing (Section 4) is where mix must not count as opportunity. The README states this split in 1 sentence.

7. **NII year on year coverage** of 10 of 62 rows at 2025-12-31 is accepted. That is amendment 17 working as intended.

8. **OPEN-39: (a).**

9. **OPEN-40: (a).**

10. **OPEN-41.** `spec_log.csv` is rewritten on every build, not appended. It holds 1 row per fit specification run in that build. Its `run_utc` holds the committer date of `HEAD` (`git log -1 --format=%cI`), so a build of a given commit is byte identical. The 18 accumulated rows are replaced. Rule 9 then holds, with no exemption.

### Step 6.0 (commit `step 6.0: section 5 review decisions`)

1. Write Sections A and A.1 to `decisions/section_5_review.md`.
2. Apply A.1.
3. Re-pull market data with splits.
4. Recompute valuation, the fits, the profiles and DRIVERS (OPEN-39 and OPEN-40).
5. Append A.1 items 1, 2, 3, 5, 8, 9 and 10 to CLAUDE.md Amendments. Rule 14 is lifted for this step.

---

## B. Section 6 decisions

### B.1 Profiles and league tables (step 6.1)

- **Profiles:** 1 PDF and 1 PNG for every bank at 2026-06-30, per amendment 5. If a bank has no KPIs at that date, use its latest date and say so in the header.
- **League CSVs:** `outputs/tables/league_{kpi}_{group}_{date}.csv` for every ranked KPI, every group and the 2 latest dates (2025-12-31 and 2026-06-30) only.
  - Columns: rank, bank_id, name, value, verdict, inside_noise, status.
  - Sort by value, best first.
- **League HTML:** `outputs/tables/league_{kpi}.html` for every ranked KPI. It shows the cluster group and universe group tables at both dates, as static HTML with no JavaScript.

### B.2 Dashboard and trace (step 6.2)

**Streamlit app (`bpb/dashboard.py`).** It reads only `outputs/`. The user picks a bank, a group, a basis and a date, and sees:
- the KPI table;
- a 5 year trend chart for each ranked KPI;
- the sized gaps with ranges;
- the Shapley waterfall;
- the valuation panel.

Every number has an expander showing its `bpb trace` output.

Run it with `streamlit run bpb/dashboard.py`.

**`bpb trace <lineage_id>`.** For a derived row, it prints the chain down to every FACTS input. For each input it shows:
- the EBA release year and item code; or
- the report URL, its sha256, the page, and the snippet.

**Test `tests/test_trace.py::test_trace_sample`** (OPEN-14 (a)):
1. Build into `tmp_path`.
2. Draw 20 KPI rows used in the profiles with `numpy.random.default_rng(seed)`.
3. Assert that each traces to FACTS rows that all have a non-empty locator. Every report locator must resolve to a cached page whose text contains the snippet.

### B.3 Build (step 6.3)

`bpb build` runs the whole pipeline from `data/raw/` and `data/manual/`: facts, checks, KPIs, peers, bench, gaps, drivers, yoy, valuation, profiles and league tables.

**Test** `tests/test_build.py::test_build_twice_identical`: build twice into 2 `tmp_path` folders, and every output file is byte identical between the 2. This includes `spec_log.csv` under A.1 item 10 and the PDFs.

Then run `bpb build` in the repo: `git status --porcelain` must be empty.

### B.4 Write up (step 6.4)

**`README.md`**, under 15 KB, in this order:

1. **Title, CI badge, the test count, and 2 sentences:** what the project does and the headline result. Under them, a line pointing to `outputs/reports/` (31 profiles), `outputs/tables/` and the dashboard command.
2. **What it does:** 1 short paragraph.
3. **How to run it:** install from the lock, `bpb build`, `streamlit run bpb/dashboard.py` and `bpb trace`.
4. **Results.** Answers to kickoff Section 1, questions 1 to 5, 1 subsection each. Each subsection has 1 table or figure, with its callout in the prose before it:
   - **Q1:** RoTE and cost_income league at 2026-06-30, cluster group, underlying basis: rank, bank, value and verdict.
   - **Q2:** sized gaps outside noise at 2026-06-30: bank, gap, headline EUR, min, max and joint. The 10 largest by joint.
   - **Q3:** the Shapley table for the 5 banks with the largest RoTE gaps to the median.
   - **Q4:** β, R², n and implied CoE by year, the slope stability test, and the 2025 figure.
   - **Q5:** the seam 2 summary: median and 90th percentile absolute relative difference by field. Then the bank insurer scope note.
5. **Peer groups:** the 5 bank global cluster against everyone else, and what that says. Silhouette and stability in 1 sentence.
6. **Caveats.** 1 line each:
   - accounting scope for bank insurers;
   - the FX move inside averages for the 5 non EUR banks;
   - the 2 seams;
   - one offs only as each bank discloses them;
   - the broad cluster 2;
   - small peer groups and wide intervals;
   - valuation slope instability;
   - headcount used for FTE at 9 banks;
   - coverage: the count of blank KPI cells at the latest date and why.
7. **What it does not do:** kickoff Section 9 of the outline.
8. **Repository map:** 1 line per folder. `instructions/`, `review/`, `decisions/` and `PLAN.md` are the build record.

**Generated content.** Every number in the README comes from a CSV. Tables are generated from the CSVs by `scripts/write_readme_tables.py` between marker comments.

**Test** `tests/test_readme.py::test_tables_match`: build into `tmp_path`, regenerate the tables, and compare with the README text between the markers.

**`answers.csv`.** `outputs/tables/answers.csv` has 1 row or more per question, with columns question, claim and source (table and row filter). Each row's claim is generated from the source table.

**`docs/METHODS.md`.** Kickoff Sections 4 and 5, rewritten to the state after every amendment, as 1 coherent text. Not a diff.

**Writing rules** for the README, the docs, the profiles, the dashboard text and the HTML:
- plain English, conversational but technical;
- numerals, not words, for numbers;
- no em or en dashes anywhere; ranges read "2021 to 2026";
- hyphens only inside compound words;
- none of the words robust, resilient, rigorous, leveraging or grounded;
- no filler.

**Test** `tests/test_readme.py::test_no_dashes`: no U+2013 or U+2014 character in `README.md`, `docs/*.md` or `outputs/tables/*.html`.

### B.5 Tidy and completion (step 6.5)

1. **MIT licence.** `LICENSE`, MIT, copyright 2026 Utkarsh Malhotra.
2. **CI.** `.github/workflows/ci.yml` must pass on GitHub for the final commit. Check the run with `gh run list` and `gh run view`, or the Actions page. Print its conclusion and the test summary line in the review. If CI fails on Linux only (a lock or wheel issue), fix the lock under rule 15 and say what changed.
3. **Folder rename.** `Project Outline/` is renamed to `project_outline/`, and every reference is updated.
4. **Leave as the build record:** `instructions/`, `review/`, `decisions/`, `PLAN.md`, and their old dashes.

---

## C. Review evidence

1. **Step 6.0:** A.1 items 1 to 4 evidence.
2. **Profiles:** the 31 profile PNGs, embedded at reduced width, or a contact sheet image `review/figures/section_6_contact.png` with all 31.
3. **Data:** 1 league HTML, and the trace output for 3 of the 20 sampled rows.
4. **Build:** `test_build_twice_identical` output and `git status --porcelain` after `bpb build`.
5. **README:** the final README, rendered as text, and its size in bytes.
6. **CI:** the run conclusion.

---

## D. End

1. Run the fresh clone check.
2. Write `review/section_6.md`.
3. Push.
4. Write `instructions/06_section_6.status.md`, commit it, push it and stop.

The partial rule applies.
