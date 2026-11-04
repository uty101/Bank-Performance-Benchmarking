# Section 4 review decisions

Written in step 4.5 from `instructions/05_section_5.md` Sections A and A.1, verbatim.

---

## A. Approval of Section 4

Section 4 is approved once step 4.5 is done.

### What the reviewer checked

**Benchmark targets.** 3 targets were recomputed with the reviewer's own code: scipy `hdquantiles` on the peer values taken from `kpi.csv` and `peers.csv`, at 2026-06-30, cluster group, underlying basis. All 3 match `bench.csv` to 6 decimals, with the same peer counts.

| bank | KPI | target | peers |
|---|---|---|---|
| LLOY | cost_income | 0.412153 | 25 |
| ISP | rote | 0.177295 | 16 |
| SWED | nim | 0.023271 | 20 |

**Hand check.** The hand check workbook matches.

**Profile.** The LLOY profile render is clear: the KPI table, the strip chart, the gap table and the footnote.

### The finding that changes the method

LLOY's largest sized gap is fee_share, at EUR 7.4bn and 13.4 RoTE points.

fee_share is one of the 6 features that define the peer groups. A gap in it measures business mix, not performance. LLOY sits at the 4th percentile because it is a UK retail bank, not because it fails at something it could fix. Sizing that gap as profit left on the table contradicts using it to form the groups.

The kickoff made the same mistake, and the reviewer missed it.

### A.1 Decisions

1. **fee_share is no longer sized.** `[gaps] sized` becomes `["cost_income", "cost_of_risk", "nim"]` (a reviewer change to `config.toml`). fee_share stays benchmarked, keeps its verdict and stays in the KPI table. The joint gap uses F′ = F always.

   This also settles open questions 1 and 3 of the Section 4 review: the negative overlap, and the joint gap left blank where a fee gap met a blank NIM.

   The hand check workbook is rebuilt without the fee lines, and its test must still pass.

2. **Broad cluster 2.** The README will say that the cluster group for 26 banks is broad. It will also say that every sized gap is shown with its range across the 3 groups, which the profile already prints. No change in code.

3. **The tax rate t̄ with fewer than 3 fiscal years** uses the `[tax_fallback]` country rate, with status `tax_fallback`, not a blank. Convention 4.11 is amended to cover this case. t̄ at 30 Jun using 3 rolling periods is confirmed.

4. **T̄E.** T̄E comes from the averaged tangible_equity directly, not from the rote row. ΔRoTE is then filled wherever tangible equity exists, even when rote's numerator is missing.

5. **Deviation 7** (`target_interval` applying the weights directly, tested equal to 1e-12) is accepted.

6. **Housekeeping accepted.** The networkx downgrade for pycel, and the slow `tests/test_gaps.py`, are accepted.
