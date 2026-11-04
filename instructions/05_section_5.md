# instructions/05_section_5.md: Session 5 instructions for Claude Code

Apply the Section 4 review decisions as step 4.5, then build all of Section 5 of `PLAN.md` (steps 5.1 to 5.3) with the amendments below. Precedence (rule 13): this file beats `PLAN.md`, which beats the kickoff.

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

### Step 4.5 (commit `step 4.5: section 4 review decisions`)

1. Write Sections A and A.1 to `decisions/section_4_review.md`.
2. Apply A.1.
3. Rebuild BENCH, GAPS, GAPS_JOINT, `gaps_range` and the 3 profiles.
4. Append A.1 items 1, 3 and 4 to CLAUDE.md Amendments. Rule 14 is lifted for this step.

**Review evidence:**
- GAPS and GAPS_JOINT at 2026-06-30 for every bank, cluster group, underlying basis;
- the LLOY profile render again.

---

## B. Section 5 decisions

### B.1 Driver decomposition (`bpb/drivers.py`)

#### Tree

For each bank and KPI date, on both bases:
- A = average total_assets;
- O = other_income (amendment 35);
- OTH = total_operating_income − opex − impairments_fin − pbt, everything between operating income and pbt other than credit impairments;
- t = tax / pbt for the period.

```
rote_tree = (NII/A + F/A + O/A − C/A − LLP/A − OTH/A) × (1 − t) × (A / T̄E)
```

The bracket equals pbt / A exactly.

`minorities_and_at1_pts` = (KPI rote − rote_tree) × 100, reported and never decomposed.

#### Reference banks

The reference bank for each driver is taken over the cluster peers (excluding the bank), same date and basis:

| run | NII/A, F/A, O/A, A/T̄E | C/A, LLP/A, t |
|---|---|---|
| `median` | median | median |
| `target` | Harrell Davis p = 0.75 | Harrell Davis p = 0.25 |

OTH/A is set at the bank's own value in both the bank and the reference. Separately, `other_below_line_pts` = (rote_tree evaluated with the reference's OTH/A, all other drivers at reference) − (the same with the bank's OTH/A), × 100.

#### Shapley values

Exact Shapley over the 7 drivers: NII/A, F/A, O/A, C/A, LLP/A, t and A/T̄E. f is rote_tree with the drivers in S at the bank's values and the rest at the reference.

#### Blanks

| case | status |
|---|---|
| pbt ≤ 0 | tax driver held at the reference value, `loss_year` |
| fiscal year containing a material merger break | blank, `merger_break` |
| any driver input missing | blank, `missing_input` |

#### Year on year changes (`ci_change`, `nii_change`)

- Consecutive fiscal years at 31 Dec, and consecutive 30 Jun rolling periods, at the same basis.
- Both periods must come from the same family (amendment 17); otherwise blank, `family_switch`.
- They must not span a merger break; otherwise blank, `merger_break`.
- `ci_change`: the 2 factor Shapley on CI = C / I gives the cost effect and the income effect in percentage points, summing exactly to ΔCI.
- `nii_change`:

  | component | formula |
  |---|---|
  | volume | NIM₀ × ΔĪEA |
  | rate | ΔNIM × ĪEA₀ |
  | cross | ΔNIM × ΔĪEA |

  Each in reporting currency and in EUR.

**Output.** A new table `outputs/tables/yoy.csv` with columns:
- date, bank_id, basis, kind (`ci` or `nii`)
- cost_effect_pts, income_effect_pts
- volume_lc, rate_lc, cross_lc, volume_eur, rate_eur, cross_eur
- status

### B.2 Valuation (`bpb/valuation.py`)

#### Sample and P/TBV

- Listed banks only, at each 31 Dec from 2021 to 2025.
- TBV per share = closing tangible_equity / shares_out at the date, not averaged. The family is whatever the KPI uses at that date. It is converted to price currency at the date's ECB cross rate: an `eba` row is EUR; HSBA's report rows are USD, converted to GBP.
- Price per Convention 4.12, using `data/raw/market/currency.csv` for the GBp rule.

#### Yearly fit

`fit_year` is an OLS of P/TBV on:
- underlying rote at that 31 Dec, as a decimal;
- the home country 10 year spread over DE in December, in decimal (percent ÷ 100).

The fit uses statsmodels HC3 standard errors. Banks with any input missing are dropped and counted in `n`.

#### Implied cost of equity

Implied CoE = growth + 1/β, with rote in decimals, so β is the change in P/TBV per unit of RoTE. It is blank if β ≤ 0.

#### Checks

- **Huber fit:** `statsmodels.RLM` with `HuberT()`, β reported as `huber_beta`.
- **Influence:** Cook's distance from the OLS. Every bank above `cooks_factor` / n is named in `cooks_named`, `;` separated.
- **Pooled fit (`fit_pooled`):** an OLS over all years with year dummies and standard errors clustered by bank (`cov_type="cluster"`). If the 90% interval of the pooled β contains 0, every uplift is blank with status `beta_not_significant`.

#### Uplift

`uplift` is computed at 2025-12-31 only, using that year's fit and GAPS_JOINT at 2025-12-31, cluster group, underlying basis:
- uplift_ptbv = β × joint_rote_pts / 100;
- lo and hi from β ∓ 1.645 × β_se.

#### Spec log

Every fit appends a row to `outputs/tables/spec_log.csv` (kickoff 6.2).

#### Figures

For each year, `outputs/figures/valuation_{year}.png`: P/TBV against underlying rote with the OLS line, 1 labelled point per bank. These are review figures; amendment 5 still governs profile charts.

### B.3 Profiles

Fill the 2 placeholder panels for LLOY, ISP and SWED:
- **Waterfall:** the median run Shapley values at 2026-06-30, cluster group, underlying basis, as a horizontal waterfall from the reference rote to the bank's rote. A bar for `other_below_line` and a bar for `minorities_and_at1` make it close.
- **Valuation:** β, n and R² for 2025. Then the bank's uplift with its interval, or the blank status in words.

LLOY's valuation panel uses its 2025-12-31 uplift, as the latest fit.

---

## C. Steps and tests

### 5.1 `bpb/drivers.py`

Tests in `tests/test_drivers.py`:
- **`test_shapley_sums`:** for every bank, date and run in DRIVERS, the sum of `shapley_pts` equals (rote_tree(bank) − rote_tree(reference with the bank's OTH/A)) × 100 within `tol_pts`.
- **`test_shapley_additive`:** on f(x) = Σ wᵢxᵢ, each Shapley value equals wᵢ(xᵢ − refᵢ) to 1e-12.
- **`test_tree_exact`:** on a synthetic bank, the bracket equals pbt / A to 1e-12, and rote_tree equals pat / T̄E to 1e-12.

**Review evidence:**
- DRIVERS for LLOY, ISP, SWED, BBVA and DBK at 2025-12-31, both runs, underlying basis;
- counts of status.

### 5.2 Year on year

Tests:
- **`test_ci_change_exact`:** cost effect + income effect = ΔCI to 1e-12 on 3 synthetic cases.
- **`test_nii_change_exact`:** volume + rate + cross = ΔNII to 1e-9 relative.

**Review evidence:**
- `yoy.csv` for the 5 banks above;
- counts of `family_switch` and `merger_break`.

### 5.3 `bpb/valuation.py`

Tests in `tests/test_valuation.py`:
- **`test_ols_matches_lstsq`:** on synthetic data with seed 3, the coefficients equal `numpy.linalg.lstsq` to 1e-10.
- **`test_coe_recovery`:**
  - 30 synthetic banks, seed 4;
  - rote uniform on [0.05, 0.20];
  - spread normal with sd 0.01;
  - P/TBV = (rote − 0.02) / (0.10 − 0.02), exactly, with no spread term.

  Implied CoE = 0.10 to 1e-9, and γ = 0 to 1e-9.
- **`test_gbp_pence_in_ptbv`:** a GBp price of 500 and a TBV per share of £4 give P/TBV 1.25.

**Review evidence:**
- VALUATION_FITS in full;
- the pooled fit;
- Cook's distance per bank per year;
- VALUATION at 2025-12-31;
- the 5 valuation figures, embedded;
- the 3 profile renders, embedded.

---

## D. End of section

- Run the fresh clone check (rule 12).
- Write `review/section_5.md` with the TEMPLATE headings.
- Push, then write `instructions/05_section_5.status.md` (rule 11), commit it, push it and stop.
- The partial rule applies.
