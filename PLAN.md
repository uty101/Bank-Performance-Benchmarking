# PLAN.md: Bank Performance Benchmarking

Expanded from `instructions/00_kickoff.md` Section 8. One paragraph per step. No step is added or removed. Session N builds all of Section N and nothing else. Section numbers in brackets, such as [5.4], refer to the kickoff. Items marked **OPEN-NN** are undecided and listed in `decisions/OPEN.md`; any step that depends on one finishes everything else and reports it (rule 1).

Every step obeys the standing rules in `CLAUDE.md`. Each step gets one commit, `step X.Y: <one line>`. Only `scripts/` touches the network. Every parameter comes from `config.toml`. CSV output uses `%.10g`, LF line endings, UTF-8 and no index. Each section ends with `review/section_N.md`, the fresh-clone check, a push and `instructions/NN_<name>.status.md`.

Test names below are fixed by this plan. A test listed as "none in the kickoff" means the step's acceptance is its review evidence only.

---

## Section 1: Foundation and EBA history

**1.1 EBA download.** Builds `scripts/pull_data.py` with a `--stage` argument (repeatable), and implements stage `eba`. For every release in `[eba] releases` and every file in `[eba] files`, it downloads the file. The 2025 and 2024 files come from the URLs fixed in [3.2]. The 2021 to 2023 URLs are read from each release page on eba.europa.eu and recorded in the committed `data/manual/eba_urls.csv` (release, file, url, release_page_url), which the stage reads (OPEN-01 decided (a)); a release that publishes its CSVs under other names has every CSV recorded under its real name. Each file goes into `data/raw/eba/{year}/`. Every CSV is filtered on the country column to banks from FI, NO, DK, SE, NL, BE, FR, DE, ES and IT and written as `data/raw/eba/{release}/{file}.csv.gz`; the `[eba] max_commit_mb` limit applies to the gzipped file, and a filtered file still over it is a stop (rule 4). Unfiltered downloads go to the gitignored `data/eba_download/` (OPEN-02 decided (b), with a change). The stage writes `data/raw/MANIFEST.json`, one entry per file: pull time UTC, URL, sha256, bytes, row count, and first and last date where the file has dates. For a filtered file it holds both the original download and the filtered file. No signature from [6.1] is implemented here. Tests in `tests/test_eba_raw.py`: `test_manifest_hashes` recomputes the sha256 of every committed file under `data/raw/eba/` and compares it with the manifest. `test_reference_dates` asserts that each release holds exactly 4 reference dates and that the 20 dates together are the quarter ends from 2020-09-30 to 2025-06-30 with no gap and no duplicate. Outputs: `data/raw/eba/{2021..2025}/`, `data/raw/MANIFEST.json`. Review evidence: the manifest entries as a table, and the reference dates per release.

**1.2 LEIs and EBA field maps.** Fills `lei` in `data/manual/universe.csv` for the EU banks. Each bank's name is matched against the bank names in the 2025 release [3.1], and the match is printed for review. A bank with no match is listed in the review file and in `decisions/OPEN.md` and is not dropped. UK banks are left blank until step 3.1. The step writes `config/eba_map_{year}.csv` for every release, with columns field, item code, template, and label as printed in `TR_Metadata.xlsx`. Each internal field of [5.1] that the EBA templates carry is matched to its metadata label exactly, with case and spacing normalised. A field with no exact match, or more than 1, is listed in `decisions/OPEN.md` with the candidate items and labels and is not guessed. The extra income components (every EBA P&L line between net fees and TOTAL OPERATING INCOME, NET, listed under `income_components_other` in `config/fields.yaml`, OPEN-06 decided (a)) and `cet1_ratio_reported` (OPEN-07 decided (a)) are mapped here too. The universe row for Crédit Agricole is `CAG`, Crédit Agricole Group (instruction 01 B.1); any other entity at a different consolidation level goes to OPEN. No signature from [6.1] is implemented here. Tests: none in the kickoff. Outputs: `data/manual/universe.csv` (lei filled for EU banks), `config/eba_map_2021.csv` to `config/eba_map_2025.csv`. Review evidence: the universe table with LEIs and matched EBA names, every map in full with item codes and labels, and every OPEN field.

**1.3 EBA ingest and lineage.** Builds `bpb/config.py` (`Config`, `load_config`), `bpb/ingest.py` (`load_eba`, `apply_source_map`, `build_facts` for EBA rows) and `bpb/lineage.py` (`lineage_id`; `trace` is built in step 6.2). `load_eba` turns one release into FACTS rows using that release's map and the universe:

- columns bank_id, lei, ref_date, field, value, ccy, unit_scale, period_months, family = `eba`, locator = item code and release year, lineage_id and status;
- values in reporting-currency units (Convention 4.1);
- signs normalised per Convention 4.2.

`apply_source_map` keeps each row only where `config/source_map.yaml` allows its family for that field, bank and date, and returns (kept, rejected). `build_facts` loads every release, applies the source map and writes `data/processed/facts.parquet` (gitignored). `lineage_id` is the first 12 hex characters of sha256 of `bank_id|ref_date|field|source_family|locator` (Convention 4.13).

Tests in `tests/test_ingest.py`:

- `test_load_eba_synthetic`: the synthetic EBA frame fixed in instruction 01 Section C loads to the exact FACTS columns in order.
- `test_source_map_rejects`: a `report` family row for an EU bank at 2023-12-31 lands in the rejected frame.

Test in `tests/test_ingest.py`: `test_lineage_stable`, the same inputs give the same 12 hex characters in 2 calls and changing any 1 of the 5 inputs changes the result. The test inputs are fixed in instruction 01 (OPEN-15 decided (a)). Outputs: `data/processed/facts.parquet`. Review evidence: FACTS row counts by release, bank and status, and the rejected rows.

**1.4 FX.** Implements stage `fx` in `scripts/pull_data.py`. It downloads the ECB EXR daily series for each of `[fx] currencies` from the URL in [3.2] to `data/raw/fx/{CCY}.csv`, with manifest rows. It also builds `bpb/fx.py`:

- `ecb_rates(raw_root)` returns date, ccy and per_eur.
- `to_eur` and `from_eur`, where kind `bs` uses the rate at the date and kind `pl` uses the mean of daily ECB rates from `period_start` to the date (Convention 4.6).

EUR maps to 1. Tests in `tests/test_fx.py`:

- `test_roundtrip`: local to EUR to local within `[tolerances] fx_roundtrip`, for every currency on 2021-12-31, 2023-06-30 and 2025-12-31, for both kinds.
- `test_pl_rate_is_mean`: the P&L rate equals the arithmetic mean of the daily rates in the period.

Outputs: `data/raw/fx/{GBP,SEK,NOK,DKK,USD}.csv`, manifest rows. Review evidence: the first and last date and row count per currency, from the manifest.

**1.5 KPI engine.** Builds `bpb/kpi.py`:

- `derived(facts)` computes the 9 derived quantities of [5.1].
- `rolling_12m(pl)` gives R(y) = H1(y) + FY(y − 1) − H1(y − 1), all 3 from one family, per Convention 4.3.
- `averages(bs)` gives opening plus closing over 2, with both ends from one family, per Convention 4.4.
- `compute_kpis(facts, kpis, one_offs, rates)` covers every KPI in `config/kpis.yaml` except `rote` (Correction 4), for EU banks, at every KPI date of [3.3] where inputs exist, on both bases (Convention 4.8).

The underlying basis equals the reported basis while `one_offs.csv` is empty. P&L numerators are FY at 31 Dec and rolling 12 months at 30 Jun, so the first EBA rolling point is 2022-06-30 (Correction 3). `income_fte`, `cost_fte` and `cost_customer` convert their numerator to EUR at the P&L rate. A KPI with a missing input is blank with status `missing_input` naming the field. rote, income_fte, cost_fte and cost_customer are blank here with status `pending_section_3`; lcr and nsfr are blank for EU banks to 2025-06-30 with `missing_input` (OPEN-05 decided (a)). The KPI table also stores numerator, denominator and `inputs_lineage`.

Tests in `tests/test_kpi.py`, built from committed raw data or synthetic data:

- `test_recompute`: each KPI equals its numerator / denominator × unit factor within `[tolerances] ratio_recompute`.
- `test_rolling_hand`: H1 2023 = 60, FY2022 = 100, H1 2022 = 40 gives R(2023) = 120; a missing H1 2022 gives a blank with `missing_input`.
- `test_averages_one_family`: an average whose ends come from 2 families is blank with status `mixed_family`.
- `test_missing_input`.

Outputs: `outputs/tables/kpi.csv` (KPI schema). Review evidence: given in step 1.6.

**1.6 Checks on EBA rows.** Builds `bpb/checks.py`:

- `identities(facts, cfg)`: the balance sheet identity within `bs_tol` (check 2); the income identity within `income_tol` (check 3, using `income_components_other`); CET1 within `cet1_tol_bps` (check 4, using `cet1_ratio_reported`); period length (check 5); currency (check 6, against `data/manual/fx_events.csv`).
- `outliers(facts, cfg)`: a quarter on quarter change more than `outlier_z` standard deviations from the bank's own mean change is flagged only (check 9).
- `run_checks(facts, cfg)`: writes CHECKS rows with failed rows kept and flagged.

Tests in `tests/test_checks.py`: `test_bs_identity` and `test_cet1`, inputs fixed in instruction 01. Outputs: `outputs/tables/checks.csv`. Review evidence:

- the full KPI table for ISP, SWED and BBVA at every date;
- every failed check row;
- KPI row counts by bank and status;
- check row counts by check and passed.

All are printed with `to_string()`.

**1.7 Mergers.** Writes `data/manual/mergers.csv` (acquirer_id, target_name, completion_date, target_total_assets, target_ccy, source_url): one row for every acquisition by a universe bank completed between 2020-09-30 and 2026-06-30, each with a source URL. Materiality is the target's total assets over the acquirer's total assets at the last reference date before completion, converted with `bpb/fx.py` where currencies differ. It is compared with `[merger] merger_materiality` (Convention 4.10), and a material deal sets a break at the completion date. No new signature. Tests: none in the kickoff. Outputs: `data/manual/mergers.csv`. Review evidence: the full table with the materiality ratio and the break flag.

---

## Section 2: Bridge data

**2.1 Pillar 3 loader.** Implements `load_p3(raw_root, universe)` in `bpb/ingest.py` per instruction 02. Instruction 02 fixes whether the source is the Pillar 3 Data Hub (pulled by a `scripts/pull_data.py` stage) or each bank's own Pillar 3 report, and the function body (Correction 1). It returns FACTS rows with family `p3` for cet1, tier1, rwa and leverage_exposure (OPEN-04 decided (b)), at 2025-06-30 (seam), 2025-12-31 and 2026-06-30. `build_facts` is extended to include them. Tests, outputs and review evidence: fixed in instruction 02.

**2.2 Report URLs and fetch.** Writes `data/manual/report_urls.csv` (bank_id, doc_type, period, url) for every EU bank: annual reports FY2024 and FY2025 and half year reports H1 2025 and H1 2026. It builds `scripts/fetch_reports.py`, which, for each row:

- downloads the PDF to `data/reports/` (gitignored);
- computes sha256, bytes and pages;
- extracts page text with pdfplumber to `data/raw/report_text/{sha256}.jsonl.gz`, one JSON line per page with page number and text;
- writes `data/raw/report_manifest.csv` (bank_id, doc_type, period, url, sha256, bytes, pages, downloaded_utc).

A failed download is a stop condition (rule 4). Tests: none in the kickoff. Outputs: `data/manual/report_urls.csv`, `data/raw/report_manifest.csv`, `data/raw/report_text/*.jsonl.gz`. Review evidence: the manifest in full.

**2.3 Report entries.** Enters into `data/manual/report_entries.csv` every field of [5.1] that the reports show, for 2024-12-31 (comparatives), 2025-06-30, 2025-12-31 and 2026-06-30. The columns are bank_id, ref_date, field, value_as_printed, unit_scale, value, ccy, period_months, doc_type, report_sha256, page, snippet and entered_utc. Every figure comes from a page of a hashed PDF (rule 16); a figure not found is left out and listed as missing. Signs follow Convention 4.2 and units Convention 4.1. Implements `load_report_entries(path, manifest)` in `bpb/ingest.py`, which returns FACTS rows with family `report` and locator = report sha256 and page. `build_facts` is extended to include them. Rows at 2024-12-31 and 2025-06-30 have the source-map role `bridge_input`: opening balances and rolling components for report-family KPIs at 2025-12-31 and 2026-06-30 (OPEN-03 decided (a)). at1_instruments, intangibles_deduction, lcr and nsfr at bridge dates are `report` (OPEN-04 decided (b)). Tests: none in the kickoff. Outputs: `data/manual/report_entries.csv`. Review evidence: the count of entries per bank and date, and every missing field per bank (step 2.4).

**2.4 Provenance and seams.** Implements three functions in `bpb/checks.py`:

- `provenance(entries, text_root)` (check 1): normalise the value and the page text, then require value / unit_scale to appear on the cited page at the page's decimals. A failing row is excluded from every KPI.
- `seam_capital(facts, cfg)` (check 7): eba against p3 at 2025-06-30 for cet1, rwa and leverage_exposure, within `seam_capital_tol`.
- `seam_pl(facts)` (check 8): eba against report at 2025-06-30, every P&L and balance sheet field, absolute and relative difference, no threshold.

All three feed `run_checks`. Tests in `tests/test_checks.py`:

- `test_provenance_passes_on_separator_styles`: 3 synthetic pages written with comma, dot, and thin space or space separators, each with a bracketed negative and a currency sign.
- `test_provenance_fails_value_not_on_page`.

Outputs: `outputs/tables/checks.csv` rows for checks 1, 7 and 8. Review evidence:

- the provenance pass rate, which must be 100% for kept rows;
- both seam tables in full;
- every missing field per bank.

**2.5 EU KPIs to H1 2026.** Extends `compute_kpis` to 2025-12-31 and 2026-06-30 for EU banks from report and p3 rows, still excluding `rote`. Averages and rolling figures follow Conventions 4.3 and 4.4, with all pieces from one family. Their inputs at 2024-12-31 and 2025-06-30 are the `bridge_input` report rows (OPEN-03 decided (a)). Tests: the step 1.5 tests run on the extended table and must still pass. Outputs: `outputs/tables/kpi.csv`. Review evidence: the KPI table for ISP, SWED and BBVA at 2025-12-31 and 2026-06-30, and counts by status.

---

## Section 3: UK banks, valuation inputs and one offs

**3.1 UK banks.** Fills `lei` for LLOY, NWG, BARC, HSBA and SANUK from GLEIF: `scripts/pull_data.py --stage gleif` queries `https://api.gleif.org/api/v1/lei-records?filter[entity.legalName]=<name>` and writes `data/raw/gleif/{bank_id}.json` (OPEN-11 decided (a)). It adds report URLs for the UK banks to `data/manual/report_urls.csv`: FY2020 to FY2025 annual reports, H1 2021 to H1 2026 half year reports, and Pillar 3 reports, entered with doc_type `pillar3` and family `report`, since every UK field is `report` (OPEN-04 decided (b)). They are fetched with `scripts/fetch_reports.py`. Every [5.1] field the reports show is entered for every UK reference date, provenance is run, and the UK rows are loaded through `load_report_entries`. HSBA reports in USD (Correction 6). Tests: the step 2.4 tests must still pass. Outputs: `data/manual/universe.csv`, `data/manual/report_urls.csv`, `data/raw/report_manifest.csv`, `data/raw/report_text/`, `data/manual/report_entries.csv`. Review evidence: UK LEIs with their GLEIF source, the provenance pass rate for UK rows, and missing fields per UK bank.

**3.2 AT1 coupons, shares, FTE and customers.** Enters at1_coupons, shares_out, and fte and customers where shown, for every bank at every 31 Dec from 2020-12-31 and every 30 Jun from 2021-06-30, from reports (Correction 5). EU bank report URLs are extended to the earlier periods this needs. at1_coupons come from the statement of changes in equity. shares_out is net of treasury shares. Provenance is run on every row. Tests: none in the kickoff. Outputs: `data/manual/report_urls.csv`, `data/manual/report_entries.csv`, `data/raw/report_manifest.csv`, `data/raw/report_text/`. Review evidence: the coverage table of these 4 fields by bank and date, and missing values.

**3.3 One offs and underlying KPIs.** Writes `data/manual/one_offs.csv` (bank_id, ref_date, period_months, field, amount, description, report_sha256, page) from each bank's own disclosed adjusting items. Each is added back or removed before tax at the disclosed amount, and tax on one offs is not adjusted (Convention 4.8). `compute_kpis` then produces the `underlying` basis from it. Tests: none in the kickoff. Outputs: `data/manual/one_offs.csv`, `outputs/tables/kpi.csv`. Review evidence: the one offs table in full.

**3.4 RoTE and market data.** Adds `rote` to `compute_kpis` for every bank (profit_to_ordinary over average tangible_equity, Correction 4). It also implements two stages in `scripts/pull_data.py`:

- `market`: yfinance `Ticker(t).history(start, end, auto_adjust=False)` Close for every listed ticker, to `data/raw/market/prices.parquet`, with the currency recorded so `GBp` prices are divided by 100 on use (Correction 7). yfinance `end` is exclusive.
- `fred`: `IRLTLT01{CC}M156N` for every `[sovereign] countries` entry, to `data/raw/fred/{CC}.csv`.

Both stages write manifest rows. Tests: the step 1.5 tests must pass with rote included. Outputs: `outputs/tables/kpi.csv`, `data/raw/market/prices.parquet`, `data/raw/fred/*.csv`, `data/raw/MANIFEST.json`. Review evidence:

- rote for every bank at every date;
- the one offs table;
- market data coverage per ticker (first date, last date, rows, currency).

---

## Section 4: Peers, benchmarks and gaps

**4.1 Peer groups.** Builds `bpb/peers.py`:

- `features(kpi, facts, year, rates)`: the 6 features of [5.4] at each 31 Dec from `[peers] first_year`, each the mean of its 3 latest fiscal year values, total_assets converted to EUR with `rates` (OPEN-08 decided (a)).
- `cluster(features, cfg)`: standardise with ddof 0, Ward linkage, cut with `fcluster(criterion="maxclust")` for k in `k_range`. It keeps the k whose clusters all have at least `min_cluster_size` banks and whose silhouette is highest, with ties going to the smaller k. If no k qualifies, the section stops (rule 4).
- `stability(features, k, cfg)`: `stability_reps` bootstrap draws with `default_rng(peer_seed)`, Jaccard with the best matching cluster, and `borderline` below `stability_flag`.
- `peer_groups(kpi, facts, cfg)`: writes PEERS with the adjusted Rand index between consecutive years and applies `data/manual/peer_overrides.yaml` after clustering.

Tests in `tests/test_peers.py`:

- `test_synthetic_three_clusters_recovered`: on a synthetic 3 cluster dataset of 30 points with known labels, k = 3 and ARI = 1.
- `test_stability_perfectly_separated_is_one`.

Outputs: `outputs/tables/peers.csv`. Review evidence: given in step 4.4.

**4.2 Benchmarks.** Builds `bpb/benchmark.py`:

- `target(values, p)`: `scipy.stats.mstats.hdquantiles` at p.
- `target_interval(values, p, reps, rng)`: the 5th and 95th percentiles of `bench_reps` bootstrap targets with `default_rng(bench_seed)`.
- `benchmark(kpi, peers, universe, cfg)`: for every ranked KPI, date, basis and group (`cluster`, `market`, `universe`; market from `universe`, OPEN-09 decided (a)), with the bank always excluded from its own peers.

`benchmark` computes the target at 0.75 or 0.25 by direction, the median at 0.5, the interval, the percentile rank (ties count half), the robust z (1.4826 × MAD, signed so positive is better), and the 3-year OLS trends of the KPI and of the gap. It sets `inside_noise`, the verdict and the `too_few_peers` status below `min_peers`. `context` KPIs are not ranked. Tests in `tests/test_benchmark.py`:

- `test_leave_one_out_enforced`
- `test_target_matches_hdquantiles_hand_set`
- `test_verdict_rules_synthetic` (the values are fixed in instruction 04, OPEN-15 decided (a))

Outputs: `outputs/tables/bench.csv`. Review evidence: given in step 4.4.

**4.3 Gap sizing.** Builds `bpb/gaps.py`:

- `size_gaps(bench, kpi, facts, rates, cfg)`: for each of `[gaps] sized` where the bank is worse than its target and not inside noise, it computes Δπ_CI, Δπ_CoR, Δπ_NIM and Δπ_fee, then ΔRoTE with t̄ from Convention 4.11 (`tax_fallback` and status where it triggers). Values are computed in reporting currency, then converted to EUR (Convention 4.6).
- `joint_gap(bank, targets)`: Δπ_joint and the overlap, as given in [5.6].

Excess capital is max(0, cet1_ratio − peer median) × rwa, reported separately. The range is the min and max over 3 groups × 2 bases, and the headline is the cluster group on the underlying basis. cost_assets and cost_fte are never sized. The step builds `tests/fixtures/hand_check.xlsx` from the inputs of the 3 `[gaps] hand_check_banks` (LLOY, ISP, SWED) with spreadsheet formulas, not pasted values. The test evaluates the committed workbook's formulas with `pycel`, added to the dev extra in Section 4 (OPEN-12 decided (b)); its date and group scope is fixed in instruction 04 (OPEN-15 decided (a)). Tests in `tests/test_gaps.py`:

- `test_hand_check_matches_within_tol`: every sized value matches the workbook within `hand_check_tol_eur`.
- `test_joint_equals_standalone_single_gap`: the joint gap equals the sum of the standalones when only 1 gap is sized.

Outputs: `outputs/tables/gaps.csv`, `outputs/tables/gaps_joint.csv`, `tests/fixtures/hand_check.xlsx`. Review evidence: given in step 4.4.

**4.4 First PDF profiles.** Builds `bpb/report.py` `build_profile(bank_id, date, root, out)`, a one page A4 PDF using reportlab, Helvetica and `invariant=1`. It holds:

- a header with name, market, cluster label and stability;
- a KPI table with value, peer median, target, percentile and verdict;
- a quartile strip chart (matplotlib);
- the top 3 sized gaps outside noise, with their range;
- a Shapley waterfall slot, which shows its blank status until Section 5 fills it;
- the valuation uplift slot, which shows its blank status until Section 5;
- footnotes for overrides, merger breaks, seam flags and tax fallback.

The step produces PDFs for LLOY, ISP and SWED at the latest KPI date. File names are `outputs/reports/{bank_id}_{date}.pdf` and `outputs/figures/{bank_id}_{date}.png` (OPEN-13 decided (a)). Tests: none in the kickoff. Outputs: 3 PDFs and their PNG renders (pymupdf). Review evidence:

- PEERS for every year;
- the cluster feature means;
- BENCH and GAPS for the 3 banks;
- the 3 PDFs rendered to PNG.

---

## Section 5: Drivers and valuation

**5.1 Shapley drivers.** Builds `bpb/drivers.py`:

- `rote_tree(drivers)`: RoTE = (NII/A + F/A + O/A − C/A − LLP/A − OTH/A) × (1 − t) × (A / T̄E) on profit before minorities and AT1 coupons. The difference from the KPI `rote` is reported as `minorities_and_at1`.
- `shapley(f, bank, ref)`: exact Shapley over the 7 drivers NII/A, F/A, O/A, C/A, LLP/A, t and A/T̄E, with OTH/A held at the bank's value and reported as `other_below_line`.
- `decompose(kpi, facts, peers, cfg)`: run against a peer median reference and against a target quantile reference. In the target run, the direction of each driver follows its effect on RoTE. A loss year (pbt ≤ 0) sets t blank and the tax driver to the reference with status `loss_year`, and a merger break blanks the fiscal year containing it.

Tests in `tests/test_drivers.py`:

- `test_shapley_sums_to_gap`: for every bank and date, within `[drivers] tol_pts`, built from committed raw and manual data.
- `test_shapley_additive_equals_differences`
- `test_rote_tree_reproduces_pbt_rote`

Outputs: `outputs/tables/drivers.csv`. Review evidence: DRIVERS for the 3 hand check banks at the latest date.

**5.2 Year on year splits.** Adds 2 functions to `bpb/drivers.py`:

- `ci_change(c0, i0, c1, i1)`: a 2-factor Shapley of ΔCI between ΔC and ΔI.
- `nii_change(nim0, iea0, nim1, iea1)`: volume = NIM(y − 1) × ΔĪEA, rate = ΔNIM × ĪEA(y − 1), cross = ΔNIM × ΔĪEA.

Both are applied to every bank and fiscal year, blank with status `merger_break` across a break. Tests in `tests/test_drivers.py`:

- `test_ci_change_sums_exactly`
- `test_nii_change_sums_exactly`

Outputs: rows in `outputs/tables/drivers.csv`. Review evidence: both splits for the 3 hand check banks.

**5.3 Valuation.** Builds `bpb/valuation.py`:

- `ptbv(facts, prices, rates, universe)`: listed banks at each 31 Dec from FY2021. The price follows Convention 4.12 (`GBp` divided by 100). TBV per share is converted from report_ccy to price_ccy at that date's ECB cross rate.
- `fit_year(df)`: OLS of P/TBV on underlying rolling RoTE in pct and the sovereign spread (home 10-year yield minus DE, December monthly value, pp), with HC3 standard errors. It returns α, β, γ, their standard errors, R² and n, plus a `statsmodels.RLM` HuberT β and the banks with Cook's distance above `cooks_factor`/n.
- `fit_pooled(df)`: year dummies, standard errors clustered by bank. If its 90% interval for β contains 0, every uplift is blank with status `beta_not_significant`.
- `uplift(gaps_joint, fits, pooled, ptbv)`: β × joint cluster-group underlying RoTE gap × TBV per share, with β ± 1.645 × se; `pooled` is the dict returned by `fit_pooled` (OPEN-10 decided (b)).

The implied CoE is `growth` + 1/β, blank if β ≤ 0. Tests in `tests/test_valuation.py`:

- `test_ols_matches_lstsq`
- `test_implied_coe_known` (the synthetic set is fixed in instruction 05, OPEN-15 decided (a))

Outputs: `outputs/tables/valuation_fits.csv`, `outputs/tables/valuation.csv`. Review evidence: VALUATION_FITS in full, Cook's distance per year, and the pooled fit.

---

## Section 6: Outputs and write up

**6.1 Profiles, league tables, HTML.** Runs `build_profile` for every bank at the latest KPI date, now with the Shapley waterfall and the valuation uplift filled. It writes the league tables `outputs/tables/league_{kpi}_{group}_{date}.csv` for every ranked KPI, group and date, and one HTML page per KPI. PDFs go to `outputs/reports/{bank_id}_{date}.pdf` and the HTML page to `outputs/tables/league_{kpi}.html` (OPEN-13 decided (a)). Tests: none in the kickoff. Outputs: PDFs for all 31 banks, league CSVs, HTML pages. Review evidence: a list of every output file with its size, and 3 PDFs rendered to PNG.

**6.2 Dashboard and trace.** Builds `bpb/lineage.py` `trace(lineage_id, root)`, which prints the chain behind a figure: the KPI or sized value, its stored parts, the FACTS rows, and the EBA item code and release or the report sha256 and page. It builds the `bpb/cli.py` commands `trace` and `bank`, and the Streamlit app `bpb/dashboard.py`. The app reads only `outputs/`, and every figure has an expander listing its `bpb trace` output. Test in `tests/test_trace.py`: `test_sampled_pdf_numbers_trace_to_facts`, where 20 numbers sampled from the PDFs' source tables with `default_rng([run] seed)` each trace to a FACTS row with a locator. It runs `bpb build` into `tmp_path` from committed raw and manual files (OPEN-14 decided (a)). Outputs: `bpb/dashboard.py`. Review evidence: the trace output for 3 of the sampled numbers.

**6.3 One command build.** Builds `bpb build` in `bpb/cli.py`. It rebuilds FACTS, KPI, CHECKS, PEERS, BENCH, GAPS, GAPS_JOINT, DRIVERS, VALUATION_FITS, VALUATION, the league tables, the HTML pages and every PDF from raw and manual files only, appending to `outputs/tables/spec_log.csv`. Running it twice leaves `git status` clean: CSV and Parquet are byte-identical, and PDFs are byte-identical through `invariant=1` (rule 9). Tests: none in the kickoff. Outputs: every file under `outputs/`. Review evidence: `git status` after 2 consecutive runs, and the runtime.

**6.4 README and methods.** Writes `README.md`:

- what the project is and how to run it;
- answers to the 5 questions of [1];
- tables generated from the CSVs;
- figures, each with one callout in the prose before it;
- the seam table;
- honest caveats: accounting differences across countries, the seam, one offs, small peer groups, the valuation interval;
- what the project does not do.

It also writes `docs/METHODS.md`, holding kickoff Sections 4 and 5. Both follow the writing rules at the end of [8]. Test in `tests/test_readme.py`: `test_readme_tables_match_csvs`, which runs `bpb build` into `tmp_path` from committed raw and manual files (OPEN-14 decided (a)). Outputs: `README.md`, `docs/METHODS.md`. Review evidence: the test output and a grep showing that none of the banned words appears.

**6.5 Final fresh clone and tidy.** Runs the fresh-clone check (rule 12), `ruff check .`, the full suite with sockets disabled and `bpb build` on the clone, confirming that every output is byte-identical to the committed files. It removes stray files and confirms that `decisions/OPEN.md` has no undecided item. Tests: the full suite. Outputs: none new. Review evidence: the full fresh-clone output and the `git status` of the clone after the build.
