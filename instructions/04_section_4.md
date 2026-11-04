# instructions/04_section_4.md: Session 4 instructions for Claude Code

Close Section 3 with step 3.8, then build all of Section 4 of `PLAN.md` (steps 4.1 to 4.4) with the amendments below. Precedence (rule 13): this file beats `PLAN.md`, which beats the kickoff.

---

## A. Approval of Section 3

Section 3 is approved once step 3.8 is done.

What the reviewer checked:
- rote at reported basis across banks and dates. It is plausible where filled: NWG 19.2% and HSBA 14.5%, against their published figures.
- The 3 hand checks (LLOY, BBVA, SEB) match `kpi.csv`.
- The BAMI and BMPS gaps to their published RoTE trace to the banks' own definitions, not to entry errors, and are accepted.
- Deviations 22 and 23 are accepted.

You may delete the fresh clone folders on the owner's machine (`C:\bpbs3`, `C:\bpbs3b`, `C:\bpbs3c`) if your safety check allows it. If it does not, leave them.

### A.1 Decisions on OPEN-34 and OPEN-35

1. **OPEN-34.** at1_coupons is 0 with status `no_at1_coupon` when the bank had no AT1 in equity during the period, or when the period's coupon line is printed as a dash or as nil. Cite the page that says so:
   - BMPS: the "no equity instruments" statement, with CC1 row 30 a dash;
   - NDA H1 2026: the cash flow line.

   That gap was the reviewer's, left open in the 03c rule.
2. **OPEN-35.**
   - **Comparative columns.** A comparative column in a later document counts as a printed amount for its date, with status `from_comparative`. This applies to SANUK, DANSKE and ABN.
   - **Dash-only lines.** A balance sheet non controlling interests line printed only as dashes is 0 with status `no_nci_line`, the same as no line. This applies to BKT.

### Step 3.8 (commit `step 3.8: section 3 review decisions`)

1. Write Sections A and A.1 to `decisions/section_3_review.md`.
2. Apply A.1 and recompute rote.
3. Append A.1 to CLAUDE.md Amendments, together with the 03b and 03c rules for at1_in_equity, at1_coupon_in_pl and at1_coupons. Rule 14 is lifted for this step.

Review evidence: the rote table for BMPS, NDA, SANUK, DANSKE, ABN and BKT at every date.

---

## B. Section 4 decisions

### B.1 Peer features (`bpb/peers.py`)

**Years.** Features are computed at 31 Dec of 2023, 2024 and 2025. Each feature is the mean of the bank's values at the 3 fiscal year ends up to and including that year. Features are levels, not comparisons, so amendment 17 does not apply to them: a 3 year mean may mix families.

**The 6 features:**
1. ln(total_assets in EUR), at the 31 Dec ECB rate.
2. loans_customers_net / total_assets.
3. fee_share.
4. loans_households_gross / loans_customers_gross.
5. trading_assets / total_assets. A bank that prints no trading assets line has this feature missing.
6. loan_deposit.

**Missing features.** A bank missing a feature in a year is left out of the clustering for that year. It is then assigned to the cluster whose centroid is nearest in standardised space, using only the features it has, with status `assigned_nearest`. The standardisation uses the means and standard deviations of the clustered banks.

**Cluster numbering.** Clusters are numbered 1 to k in descending order of their mean ln(total_assets), so the labels are stable from run to run.

**Which clusters a KPI date uses:**
- 31 Dec of year y: the year y clusters.
- 30 Jun of year y: the year y − 1 clusters.
- Every date before 2023-12-31 uses the 2023 clusters.

**Stability.** Kickoff 5.4, with `numpy.random.default_rng(peer_seed)` created once per year and drawn in bootstrap order. For each draw, the drawn rows are the unique indices of `rng.integers(0, n, n)`.

### B.2 Benchmarks (`bpb/benchmark.py`)

**Scope.**
- Every KPI date, every ranked KPI (direction higher or lower), both bases.
- 3 groups: cluster, market and universe.
- Peers exclude the bank itself and banks with a blank value.
- Fewer than `min_peers` peers gives status `too_few_peers`. That will be most market groups, and it is expected.

**Random draws.** Every bootstrap uses its own generator: `numpy.random.default_rng(numpy.random.SeedSequence([bench_seed, zlib.crc32(key.encode())]))`, where key is `date|bank_id|kpi|basis|group`. Results then do not depend on loop order.

**Estimator and interval.** Kickoff 5.5: Harrell Davis via `scipy.stats.mstats.hdquantiles`, and the 5th and 95th percentiles of `bench_reps` draws.

**Trend.** OLS slope per year over the bank's values at the latest 3 fiscal year ends up to the date. All 3 values must have the same `family`. If they do not, the trend is blank with status `family_switch`. Fewer than 3 gives status `short_history`.

**Verdict.** As in kickoff 5.5:
- inside noise is `in_line`;
- otherwise `leading` if better than the target;
- otherwise `lagging` if worse than the median;
- otherwise `in_line`.

### B.3 Gaps (`bpb/gaps.py`)

**Formulas.** Kickoff 5.6 exactly.

| variable | at 31 Dec | at 30 Jun |
|---|---|---|
| I, F, O, C, LLP | FY values | rolling 12 month values (Convention 4.3) |
| L̄, ĪEA, T̄E | Convention 4.4 averages | Convention 4.4 averages |

`delta_rote_pts` = Δπ × (1 − t̄) / T̄E × 100. The tax rate t̄ is a level, so the 3 years may mix families.

**EUR conversion.** P&L effects use the mean ECB rate over the period:
- 31 Dec: from 1 Jan to 31 Dec;
- 30 Jun: from 1 Jul of y − 1 to 30 Jun of y.

Excess capital uses the date's rate.

**Which gaps are sized.** For each bank, date, group and basis:
- a gap is sized only when the bench row has verdict `lagging` or `in_line` with the bank worse than its target, and `inside_noise` is false;
- otherwise the gap row has status `not_sized` and blank values.

**Joint gap.** Kickoff 5.6 rules. Drivers that are not sized keep the bank's own value.

**Ranges.** A new output table, `outputs/tables/gaps_range.csv`, with columns:
- date, bank_id, gap
- min_eur and max_eur, over the up to 6 cells of 3 groups × 2 bases that are sized
- headline_eur: the cluster group on the underlying basis, blank if that cell is not sized
- n_sized

### B.4 Hand check (`tests/fixtures/hand_check.xlsx`)

**Scope.** LLOY, ISP and SWED at 2025-12-31, cluster group, underlying basis.

**Layout.**
- 1 sheet per bank.
- The inputs (I, F, O, C, LLP, L̄, ĪEA, T̄E, t̄, the 4 targets, and the period mean FX rate for SWED and LLOY) are typed values, each with its lineage ID in the next cell.
- Every sized value is a spreadsheet formula: each standalone Δπ, Δπ in EUR, ΔRoTE, and the joint Δπ.

**Tests.**
- **`tests/test_gaps.py::test_hand_check`:** evaluates the workbook with `pycel` (add it to the dev extra and rebuild the lock under rule 15). It asserts that every formula result matches `size_gaps` within `hand_check_tol_eur`, and within 1e-6 points for ΔRoTE. If a bank has no sized gap at that cell, print it and use the same bank's universe group instead, noted on the sheet.
- **`test_joint_single`:** when only 1 gap is sized, the joint gap equals that standalone gap to 1e-9 relative.

### B.5 Profiles (`bpb/report.py`), first version

**Contents.** 1 A4 page per bank at the latest KPI date, 2026-06-30:
- a header with the name, market, cluster number and stability;
- a KPI table of value, peer median, target, percentile and verdict, cluster group, underlying basis;
- a quartile strip chart (matplotlib, drawn in memory), with each ranked KPI on its own row and the bank marked among its peers;
- the top 3 sized gaps by headline EUR, with min to max;
- a footnote line for the statuses that apply.

The waterfall and valuation panels are text placeholders reading "Section 5".

**Paths.** Amendment 5. Render the PNG with `pymupdf` at 110 dpi.

**Determinism.** Building twice must give byte identical PDFs.

### B.6 Tests (from kickoff Section 8 plus the above)

**`tests/test_peers.py`:**
- **`test_three_clusters`:** 30 synthetic points in 3 clusters of 10, means 10 standard deviations apart on all 6 features, seed 1. It returns k = 3 and ARI 1.
- **`test_stability_perfect`:** on the same data, every bank's stability is 1.0 to 1e-12.
- **`test_assigned_nearest`:** a bank missing feature 5 is assigned to the cluster it was generated from.

**`tests/test_benchmark.py`:**
- **`test_leave_one_out`:** with peers [1, 2, 3, 4, 5, 6] plus the bank at 100, the target excludes 100.
- **`test_hd_matches_scipy`:** on the values [0.11, 0.07, 0.15, 0.09, 0.12, 0.10, 0.13], `target` equals `hdquantiles(..., prob=[0.75])` to 1e-12.
- **`test_verdicts`:** 4 synthetic cases, 1 for each branch of B.2.
- **`test_seed_independent_of_order`:** shuffling the input rows gives identical BENCH output.

**`tests/test_gaps.py`:** see B.4.

---

## C. Steps

- **4.1 `bpb/peers.py`.**
  - Review evidence:
    - PEERS for 2023, 2024 and 2025 in full;
    - the feature table per year;
    - the cluster means per feature;
    - k and silhouette for each candidate k;
    - the ARI between years;
    - every `assigned_nearest` and `borderline` bank.
- **4.2 `bpb/benchmark.py`.**
  - Review evidence:
    - BENCH for rote, cost_income and nim at 2025-12-31 and 2026-06-30, cluster group, underlying basis, for every bank;
    - counts of status by group.
- **4.3 `bpb/gaps.py` and the hand check.**
  - Review evidence:
    - GAPS, GAPS_JOINT and gaps_range at 2026-06-30 for every bank;
    - the hand check workbook's 3 sheets printed as values;
    - the pycel results next to `size_gaps`.
- **4.4 Profiles for LLOY, ISP and SWED.**
  - Review evidence: the 3 PNG renders, embedded in the review.

---

## D. End of section

- Run the fresh clone check (rule 12).
- Write `review/section_4.md` with the TEMPLATE headings.
- Push, then write `instructions/04_section_4.status.md` (rule 11), commit it, push it and stop.
