# Methods

This is how the project works today, with every amendment folded in. Parameters live in `config.toml`, field and KPI definitions in `config/`.

## 1. Conventions

1. **Units.** Monetary values are stored in units of their currency, never thousands or millions. The scale on the source page is applied on entry and recorded in `unit_scale`. `eba` rows are in EUR for every bank, as EUR millions with `unit_scale` 1e6. A ratio item is a decimal stored as reported. `report` and `p3` rows are in the reporting currency.
2. **Signs.** Expenses, impairments and tax are stored positive, and a net release is stored negative.
3. **Year to date.** EBA and report P&L values are year to date. FY is the 31 Dec value and H1 the 30 Jun value. Rolling 12 months at 30 Jun of year y: R(y) = H1(y) + FY(y − 1) − H1(y − 1), all 3 from 1 source family.
4. **Averages.** The average balance for a fiscal year is the mean of the closing balances at the 2 year ends. For a rolling 12 months at 30 Jun it is the mean of the balances at the 2 30 Junes. Both ends come from 1 family, and a report's comparative column counts as the same family as its current column.
5. **Source family.** `eba`, `p3` (a bank's Pillar 3 report) or `report` (annual or half year report).
   - EU banks use `eba` to 2025-06-30, and bank documents at 2025-12-31 and 2026-06-30. At 2025-06-30 report rows exist for the seam test only.
   - At those later dates, cet1, tier1, rwa and leverage_exposure are `p3`; at1_instruments, intangibles_deduction, lcr and nsfr are `report`.
   - For UK banks every field is `report`, and a Pillar 3 PDF counts as a `report` document.
   - `report` rows for EU banks at 2024-12-31 and 2025-06-30 may serve as opening balances and rolling components for the later KPIs (role `bridge_input`). FY2024 P&L comes from the FY2025 annual report's comparative column for this.
   - A row's family comes from the source map, never from the type of document.
6. **Local currency first.** Every KPI is computed in the currency of its rows. EUR conversion applies only to sized values and only after the KPI: the date's ECB rate for balance sheet values, the mean of daily ECB rates over the period for P&L values. When a derived quantity combines currencies, the non EUR value is converted first and the row's status gains `fx_combined`.
7. **Display.** Code holds decimals. Tables show % to 2 decimals and bps to 1 decimal.
8. **Underlying figures.** Underlying is reported, adjusted only for the one offs in `data/manual/one_offs.csv`, each added back or removed before tax at the amount the bank discloses. Tax on one offs is not adjusted. Every KPI exists on both bases.
9. **Failed or missing values** keep their rows, with a `status` and a blank value, never a fallback number.
10. **Merger breaks.** A merger whose target exceeds `merger_materiality` of the acquirer's total assets at the last date before completion gives a break at completion. Target size is total assets, else loans, else the consideration paid, whichever is published first in that order. Year on year changes that span a break, and any decomposition for a period holding it, are blank with status `merger_break`.
11. **Tax rate for sizing.** t̄ is the sum of tax over the sum of profit before tax over the 3 fiscal years ending at the KPI date, or 3 rolling periods at 30 Jun. With fewer than 3 years, a non positive sum of profit, or t̄ outside 0 to 0.6, the `[tax_fallback]` country rate applies with status `tax_fallback`.
12. **Prices.** The price is the close on the last trading day on or before the KPI date, in price currency, divided by 100 when yfinance reports `GBp`. yfinance adjusts `Close` for splits while shares_out is as printed, so the unadjusted price at t = Close(t) × the product of every split ratio dated after t. A consolidation has a ratio below 1, so a 1:10 consolidation puts earlier prices at 0.1 times the adjusted ones.
13. **Lineage ID.** The first 12 hex characters of sha256 of `bank_id|ref_date|field|source_family|locator`, where the locator is the EBA item code and release year, or the report sha256 and page. Every derived row stores the IDs of its inputs.
14. **No time comparison crosses the family switch.** Every year on year change, 3 year trend and decomposition comparing 2 dates uses 1 family. Where no same family pair exists, the result is blank with status `family_switch`.

## 2. Fields and sources

`config/fields.yaml` lists every field and `config/source_map.yaml` names the 1 family allowed to fill it at each date. EBA fields are mapped by an exact match on their label in `TR_Metadata.xlsx`. A field with several map rows is their sum, and if any row is absent the field is missing, never a partial sum. An unnamed dimension of a source row must equal 0 for the row to match.

**Report entries.** Every report figure is entered by hand into `data/manual/report_entries.csv` from a hashed document, with its page and a snippet holding the printed value. A summed figure is 1 row per printed number, with a `component n/m:` note in its snippet. If a component is missing, the field is missing. Cited pages are cached in `data/raw/report_text/`. A workbook counts as a document, and its `page` holds `sheet!cell`.

**Rules for entries.**

- A dash or empty cell in a printed template row is 0. A row that is not printed at all stays missing.
- EU capital and asset quality figures come from the EU KM1, CC1 and CR1 templates of each bank's Pillar 3 report. Where a Pillar 3 report cannot be obtained, the KM1 figures come from the capital note of the same date's report, as family `p3` with status `p3_from_report`.
- A figure from a later document's comparative column has status `from_comparative`.
- If no total operating income is printed, the printed lines are summed, with status `toi_summed`. If no total liabilities are printed, the field is not entered.
- Levies not on their own line are treated as 0 in opex, with status `levies_in_admin`. Depreciation not on its own line is taken as inside administrative expenses, with status `dep_in_admin`.
- admin_expenses is staff and other administrative expenses as printed. Insurance service expenses are never added in.
- profit_owners is net profit minus non controlling interests.
- Where only headcount is printed, it is entered into fte with status `headcount`.

**AT1.** `at1_in_equity` is a flag read from the annual report. Where it is 0, AT1 is not in total_equity, so its term in tangible equity is 0. `at1_coupon_in_pl` is a flag that is 1 if coupons sit in interest expense. `at1_coupons` holds the coupons charged directly to equity, and is 0 where they are in the P&L or where the bank had no AT1 in equity. For CAG, whose Pillar 3 reports do not print CC1, at1_instruments is the printed line "(-) AT1 instruments accounted as equity", status `at1_from_reconciliation`. That line is the AT1 held in accounting equity, which is the amount the tangible equity deduction needs.

**Derived quantities.**

- nii = interest_income − interest_expense
- other_income = total_operating_income − nii − net_fees, a residual that already holds dividends
- opex = admin_expenses + resolution_dgs_contrib + depreciation
- ppp = total_operating_income − opex
- iea = cash_cb + debt_securities + loans_all
- loans_customers_net = loans_customers_gross − loans_customers_allowance
- tangible_equity = total_equity − minority_interests − at1_instruments − intangibles_deduction
- tax = pbt − pat
- profit_to_ordinary = profit_owners − at1_coupons
- nii_net_llp = nii − impairments_fin, at the same bank, date, period and family, so a net release adds to it

## 3. KPIs

| kpi | numerator | denominator | average | unit | direction |
|---|---|---|---|---|---|
| rote | profit_to_ordinary | tangible_equity | yes | pct | higher |
| roa | profit_owners | total_assets | yes | bps | higher |
| ppp_assets | ppp | total_assets | yes | bps | higher |
| nim | nii | iea | yes | bps | higher |
| fee_share | net_fees | total_operating_income | no | pct | higher |
| cost_income | opex | total_operating_income | no | pct | lower |
| cost_assets | opex | total_assets | yes | bps | lower |
| cost_of_risk | impairments_fin | loans_customers_gross | yes | bps | lower |
| risk_adj_nim | nii_net_llp | iea | yes | bps | higher |
| npl_ratio | npl_gross | loans_all | no | pct | lower |
| npl_coverage | npl_allowance | npl_gross | no | pct | higher |
| cet1_ratio | cet1 | rwa | no | pct | higher |
| leverage_ratio | tier1 | leverage_exposure | no | pct | higher |
| rwa_density | rwa | total_assets | no | pct | context |
| loan_deposit | loans_customers_net | deposits_customers | no | pct | context |
| lcr | lcr | 1 | no | pct | higher |
| nsfr | nsfr | 1 | no | pct | higher |
| income_fte | total_operating_income | fte | yes | eur_k | higher |
| cost_fte | opex | fte | yes | eur_k | lower |
| cost_customer | opex | customers | no | eur | lower |

KPI dates are every 31 Dec and 30 Jun from 2021-12-31 to 2026-06-30. P&L numerators are FY at 31 Dec and rolling 12 months at 30 Jun. `income_fte`, `cost_fte` and `cost_customer` are the only KPIs converted to EUR before ranking. `context` KPIs are shown but never ranked, sized or given a verdict. A KPI with a missing input is blank with status `missing_input` naming the field.

## 4. Checks

Each check writes rows to `outputs/tables/checks.csv`.

1. **Provenance.** The snippet must hold `value_as_printed`, and the value divided by `unit_scale` must appear as a number on the cited page, at the decimals shown there, after thousands separators, brackets and currency signs are normalised. A dash cell or a flag needs its row label on the page instead. A failed row is excluded from every KPI. One offs get the same check.
2. **Balance sheet.** Assets less liabilities and equity, relative to assets, within `bs_tol`. With no liabilities line, the row has status `no_liabilities_line` and no pass or fail.
3. **Income.** The components against total operating income, within `income_tol`.
4. **CET1.** The reported ratio against cet1 / rwa, within `cet1_tol_bps`.
5. **Period length.** A P&L value covers 6 months at 30 Jun and 12 at 31 Dec.
6. **Currency.** A bank's `report_ccy` never changes without a row in `data/manual/fx_events.csv`.
7. **Seam 1, capital.** At 2025-06-30, cet1, rwa and leverage_exposure from `eba` and `p3` agree within `seam_capital_tol`.
8. **Seam 2, P&L.** At 2025-06-30, every field from `eba` and `report`, with absolute and relative differences. There is no threshold, because the table is the finding. Check `8b_scope_gate` adds the EU LR1 scope adjusted total assets, for information only, and blocks no bank.
9. **Outliers.** A quarter on quarter change of an EBA field more than `outlier_z` standard deviations from the bank's own mean change is flagged only.

## 5. Peer groups

**Features**, at each 31 Dec from FY2023: ln(total assets in EUR), net customer loans / assets, fee_share, household loans / customer loans, trading assets / assets, and loan_deposit. Each is the mean of the values present at the 3 latest year ends, if at least 2 are present, with status `two_of_three` where only 2 are. fee_share is read on the reported basis, since features describe business mix, not performance.

**Clustering.** Each feature is standardised across banks, then clustered with Ward linkage. For each k in `k_range`, the tree is cut. The k kept is the one whose every cluster holds at least `min_cluster_size` banks and whose silhouette is highest, with ties going to the smaller k. A bank with a missing feature joins the nearest cluster.

**Stability.** `stability_reps` bootstrap draws of banks with replacement, repeating the whole method within each draw, including the standardising. A bank's stability is the mean Jaccard similarity of its own cluster with the best matching draw cluster. Below `stability_flag` it is flagged `borderline`.

**Groups.** Each bank has 3: `cluster`, the primary one, `market` and `universe`. A peer set always leaves out the bank itself.

## 6. Benchmarks

- **Target:** the Harrell Davis quantile of the peers' values at p = 0.75 where higher is better, 0.25 where lower is better. The median is the same estimator at 0.5.
- **Interval:** `bench_reps` bootstrap draws of the peer values, the 5th and 95th percentiles of the estimator.
- **Position:** percentile rank is the share of peers the bank beats, ties counting half. A median based z score uses 1.4826 × MAD of the peers, signed so positive is better.
- **Trend:** the OLS slope per year of the KPI and of target less value over the latest 3 fiscal years, blank with fewer than 3.
- **Noise:** `inside_noise` means the bank's value lies inside the target's interval.
- **Verdict:** `leading` if better than the target, `lagging` if worse than the median, else `in_line`. Inside noise makes it `in_line`.
- **Small groups:** fewer than `min_peers` other banks with a value gives status `too_few_peers` and blanks.

## 7. Gap sizing

Gaps are sized for cost_income and risk_adj_nim where the bank is worse than its target and outside noise. nim and cost_of_risk stay benchmarked, with their verdicts, but are not sized apart: a high cost of risk is the price of a high margin, so sizing 1 side alone would count the price of lending in a high margin market as a gap. fee_share is benchmarked but never sized: it helps define the peer groups, so a gap in it measures business mix, not performance. cost_assets and cost_fte are never sized, since they measure the same cost base as cost_income.

With I = total operating income, F = net fees, O = other income, C = opex, LLP = impairments, RAM = risk_adj_nim, ĪEA = average iea, T̄E = average tangible equity, and starred values the targets:

- Δπ_CI = (CI − CI\*) × I
- Δπ_RAM = (RAM\* − RAM) × ĪEA
- ΔRoTE = Δπ × (1 − t̄) / T̄E, where T̄E comes from the averaged tangible equity directly

**Joint gap.** The margin gap closes through NII at the bank's current credit cost: d = RAM\* × ĪEA − (NII − LLP) if it is sized, else 0, with NII′ = NII + d and LLP′ = LLP. F′ = F always. I′ = NII′ + F′ + O. C′ = CI\* × I′ if the cost gap is sized, else C. Then Δπ_joint = (I′ − C′ − LLP′) − (I − C − LLP), and overlap is the sum of the standalone gaps less Δπ_joint.

**Excess capital** is max(0, cet1_ratio − peer median) × rwa, reported separately.

**Range.** For each bank and gap, min and max run over the 3 peer groups and 2 bases. The headline is the cluster group on the underlying basis. Every value is computed in local currency, then converted to EUR.

## 8. Drivers

With A = average total assets, the RoTE tree is:

RoTE = (NII/A + F/A + O/A − C/A − LLP/A − OTH/A) × (1 − t) × (A / T̄E)

OTH is every line between operating income and pbt that is not C or LLP, so the bracket equals pbt / A exactly. t = tax / pbt for the period. The tree gives profit before minorities and AT1 coupons, and the difference from the KPI `rote` is reported as `minorities_and_at1`, not as a driver.

**Shapley values.** The 7 drivers are NII/A, F/A, O/A, C/A, LLP/A, t and A/T̄E. Each bank is compared with a reference, which is the Harrell Davis median of each driver across its cluster peers, in 1 run, and the target level of each driver, by its effect on RoTE, in a second run. The exact Shapley value of driver i is the sum over subsets S without i of |S|!(7 − |S| − 1)!/7! × [f(S ∪ {i}) − f(S)]. OTH/A is held at the bank's own value, and the move from the reference's is reported as `other_below_line`.

**Blanks.** A driver with fewer than `min_peers` cluster peers holding a value is blank with status `too_few_peers`. A missing input gives `missing_input`, and assets and tangible equity in different currencies give `mixed_family`. In a loss year t is blank, the tax driver sits at the reference, and the status is `loss_year`. If the KPI `rote` is blank the bridge cannot close, and the status is `rote_blank`.

**Basis.** DRIVERS holds both bases, in a `basis` column.

**Mix.** F/A stays a driver. Decomposition explains where a gap comes from, and business mix is part of that. Sizing is where mix must not count as opportunity.

**Year on year** (`outputs/tables/yoy.csv`), between consecutive 31 Decs and consecutive 30 Junes:

- Cost to income: the 2 factor Shapley of CI = C / I, between cost and income.
- NII: volume = NIM(y − 1) × ΔĪEA, rate = ΔNIM × ĪEA(y − 1), cross = ΔNIM × ΔĪEA.

## 9. Valuation

Listed banks only, at each 31 Dec from FY2021.

- **P/TBV:** the unadjusted price over tangible equity / shares_out, with TBV per share converted to the price currency at the date's ECB cross rate.
- **Year fit:** OLS of P/TBV on underlying RoTE and the sovereign spread (home 10 year yield less DE, December value), with HC3 standard errors. The fit reports α, β, γ, their standard errors, R² and n.
- **Implied cost of equity:** `growth` + 1/β, blank if β ≤ 0. If the 90% interval of a year's β contains 0, it is blank with status `beta_ns_year`.
- **Checks:** a Huber fit, and Cook's distance from the OLS fit, naming banks above `cooks_factor` / n.
- **Pooled fit:** OLS over all years with year dummies, standard errors clustered by bank. Its β sets the significance gate: if its 90% interval contains 0, every uplift is blank with status `beta_not_significant`.
- **Slope stability:** the pooled fit with rote × year interactions, clustered by bank, and a Wald F test that the year slopes are equal, in `outputs/tables/valuation_stability.csv`.
- **Uplift:** at 2025-12-31 only, β × the joint RoTE gap of the cluster group on the underlying basis, with an interval from β ± 1.645 × se. It uses the year's own fit, which is the market's pricing at that date. `uplift_pooled_ptbv` gives the same uplift on the pooled β.

`outputs/tables/spec_log.csv` is rewritten on every build, with 1 row per fit specification. Its `run_utc` is the committer date of the last commit that touched a build input, and is blank with status `no_git` where git is not available, in a trailing `status` column.

## 10. Outputs

- **Profiles:** 1 A4 PDF and PNG per bank at 2026-06-30, or at the bank's latest date if it has no KPIs there, which the header then says. The waterfall uses the latest date with a decomposition, named in its title, and otherwise says why there is none.
- **League tables:** a CSV for every ranked KPI, group and the 2 latest dates, on the underlying basis, and 1 static HTML page per KPI. Banks are sorted by value, best first, and a blank value keeps its row at the end, with no rank. A cluster file has a `cluster` column after `rank`, the rank restarts at 1 within each cluster, and the HTML page shows 1 table per cluster.
- **Trace:** `outputs/tables/lineage.csv` holds every source row and `lineage_derived.csv` every derived row with its inputs. `bpb trace` walks from a row down to the EBA release and item, or the report URL, sha256, page and snippet. A sized gap or a driver stops at its own bank's inputs, since its target or reference comes from peers.
- **Dashboard:** `bpb/dashboard.py` reads only `outputs/`, under the path in `BPB_ROOT`, or the current directory if that is not set.
- **Determinism:** every random draw uses a seed from `config.toml`. CSVs use `%.10g`, LF and UTF-8, and PDFs are written with `invariant=1`, so 2 builds of a commit are byte identical.
