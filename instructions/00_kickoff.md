# instructions/00_kickoff.md: Session 0 instructions for Claude Code

Repo: https://github.com/uty101/Bank-Performance-Benchmarking
Project: Bank Performance Benchmarking (quant project 15 of the home-built series)
Source doc: `Project Outline/Bank_Performance_Benchmarking.md`
Workflow: `WORKFLOW.md` (already committed by the owner; do not rewrite it)

This document is the specification. Nothing in it is yours to redesign. Where it corrects or tightens the source doc, this document wins.

---

## 0. How this repo is run

Session 0 writes the plan and scaffolding only. It pulls no data and writes no analysis code. After session 0, session number equals section number: Session N builds all of Section N of `PLAN.md`, every step in it, in one session, and nothing from any other section. A reviewer (Claude in chat) reads the repo once per section and either approves it or returns fixes. You never start the next section until a new session tells you to. No section waits on anything outside the repo: there are no scheduled jobs and no waiting for data to arrive.

Rules that hold for every session:

1. **No design choices.** Every parameter, definition, signature, schema, convention and file path is fixed in this document, in `PLAN.md` or in a later instruction file. If something is genuinely unspecified, append it to `decisions/OPEN.md` with 2 concrete options, finish every other step in the section that does not depend on it, and report it in the review file. Do not pick an option yourself.
2. **Commits.** One commit per step, message `step X.Y: <one line>`, on `main`. Push once at the end of the section. Never force push, never rewrite history, never amend a pushed commit. Stage files by explicit path; never `git add -A` or `git add .`.
3. **One review file per section**: `review/section_N.md`, following `review/TEMPLATE.md` exactly.
4. **Stop conditions.** Stop the section, write the review and status files, and push if any of these happen: a data pull fails; a test from an earlier section fails; a check or gate in this document fails its stated threshold; a result can only be produced by making a design choice; a step would need a file or function outside that section's scope. Do not work around any of them.
5. **Tests are fixed.** Never loosen a tolerance, skip, xfail, or rewrite a test so that it passes. If a test in this document is wrong, stop under rule 4 and say why. A tolerance marked **MEASURE** is not yet fixed: the step measures the quantity, prints the measurement in the review file, and the test asserts the bound the reviewer sets in the next instruction file. Until then that test asserts only that the measurement is finite.
6. **Config is fixed.** Every parameter lives in `config.toml`. No numeric parameter is hard-coded in `bpb/`. The only exception is a constant written inside a formula in this document or an instruction file, which may be a literal with a comment citing the section where the formula is written. Do not change a value set in this document.
7. **Tests build what they read.** No test may depend on `outputs/` or `data/processed/` already existing. Tests read only `data/raw/` (committed), `data/manual/` (committed), `tests/fixtures/` (committed) or synthetic data they generate. The full suite runs offline: `pytest -p socket --disable-socket` must pass.
8. **No network outside `scripts/`.** Only `scripts/pull_data.py` and `scripts/fetch_reports.py` touch the network. Nothing in `bpb/` or `tests/` does.
9. **Determinism.** Every random draw uses `numpy.random.default_rng(seed)` with a seed from `config.toml`. Running the same section twice produces byte-identical CSV and Parquet outputs and byte-identical PDFs (reportlab `invariant=1`). CSV float format is `%.10g`, line endings LF, UTF-8, no index column.
10. **Evidence, not summaries.** Every numeric claim in a review file is backed by raw rows printed with `DataFrame.to_string()`, never by a description of them.
11. **Instructions and status live in the repo.** Every session's instructions are a file committed to `instructions/` before the session starts. The session prompt only names the file. Read it from the repo and follow it; never edit an instruction file. Reviewer comments arrive inside the next instruction file. Every session ends by writing `instructions/NN_<name>.status.md` with: outcome (completed or stopped), the last step reached, the reason for any stop, every question or blocker for the reviewer, and the output of `git log origin/main --oneline -3`; then commit and push it and stop. This applies to sessions that stop early: the status file is always written and always pushed. Nothing is relayed by chat.
12. **Fresh-clone check at the end of every section from Section 1 on.** Clone the pushed repo into a short temp path, `uv venv --python 3.12`, install from `requirements-lock.txt` then `pip install -e . --no-deps`, run `pytest -p socket --disable-socket -q`, and paste the full output into the review file.
13. **Precedence.** A later instruction file beats `PLAN.md`, which beats this document, which beats the source doc.
14. **Do not stage `CLAUDE.md` or `PLAN.md`** after session 0 unless an instruction file says to. If your own safety check refuses to edit `CLAUDE.md`, report it in the status file and the owner will commit it.
15. **Python 3.12 everywhere.** The lock is built with `uv pip compile pyproject.toml --extra dev --universal --python-version 3.12 -o requirements-lock.txt`; every venv with `uv venv --python 3.12`.
16. **Hand entered figures.** Every figure taken from a bank report is entered by you into `data/manual/report_entries.csv` (schema in Section 6.2) from the PDF that `scripts/fetch_reports.py` downloaded and hashed. You never type a figure from memory, from a news article or from a data vendor. A figure you cannot find on a page of a hashed PDF is left out and listed in the review file as missing.

---

## 1. What the project answers

1. For each of 31 European banks, where does it sit against peers with a similar business model on profitability, efficiency, margin, risk and capital, from FY2021 to the latest half year (H1 2026)?
2. Which gaps to the best quartile are larger than the noise in a peer group of 6 to 10 banks, and what is each worth in euros of pre tax profit and in RoTE points, standalone and closed together?
3. Which of 7 drivers (NII, fees, other income, costs, impairments, tax, leverage) explain each bank's RoTE gap to its peers, and how did cost to income and NII change year on year (cost against income growth, volume against rate)?
4. Across the listed banks, how much does a point of RoTE add to price to tangible book, what cost of equity does that imply, and is the relationship stable from year to year?
5. How large is the difference between the EBA supervisory figures and the banks' own published figures for the same bank and period, which is the error introduced by joining the 2 sources?

---

## 2. Corrections to the source doc (already applied below)

1. **The EBA exercise has stopped.** The last release (December 2025) covers reference dates to 30 June 2025. The history period, Sep 2020 to Jun 2025, comes from the 2021 to 2025 releases. The bridge period, H1 2025 to H1 2026, comes from bank reports. Capital in the bridge period comes from the Pillar 3 Data Hub if its data can be pulled by script, else from each bank's own Pillar 3 report; the reviewer fixes which in instruction 02.
2. **Phase count.** The source doc's 6 phases are Sections 1 to 6 here, one session each.
3. **First KPI year is FY2021.** Averaged denominators need the opening balance, and the EBA history starts at Sep 2020, so FY2020 has no opening balance. Rolling 12 month figures at June need H1 of the prior year, so the first EBA rolling point is Jun 2022.
4. **RoTE waits for Section 3.** The EBA templates carry no AT1 coupons and no share counts. RoTE and every valuation input are computed once Section 3 has entered AT1 coupons and share counts from reports. Section 1 computes every other KPI.
5. **Shares outstanding come from reports, not yfinance,** because yfinance share count history is unreliable. yfinance supplies the share price only.
6. **HSBC reports in USD.** USD is added to the FX set.
7. **LSE prices are quoted in pence** in yfinance (`GBp`). Prices are divided by 100 before any use.
8. **Large raw files.** An EBA CSV over 50 MB is not committed whole. `data/raw/eba/` holds the rows for universe banks only, gzipped, and `MANIFEST.json` records the sha256 and row count of both the original download and the filtered file.

---

## 3. Universe, data and sample

### 3.1 Universe (`data/manual/universe.csv`, written in session 0 with `lei` blank)

| bank_id | name | country | market | listed | ticker | price_ccy | report_ccy |
|---|---|---|---|---|---|---|---|
| LLOY | Lloyds Banking Group | GB | UK | 1 | LLOY.L | GBP | GBP |
| NWG | NatWest Group | GB | UK | 1 | NWG.L | GBP | GBP |
| BARC | Barclays | GB | UK | 1 | BARC.L | GBP | GBP |
| HSBA | HSBC Holdings | GB | UK | 1 | HSBA.L | GBP | USD |
| SANUK | Santander UK Group Holdings | GB | UK | 0 | | | GBP |
| NDA | Nordea Bank | FI | Nordics | 1 | NDA-FI.HE | EUR | EUR |
| DNB | DNB Bank | NO | Nordics | 1 | DNB.OL | NOK | NOK |
| DANSKE | Danske Bank | DK | Nordics | 1 | DANSKE.CO | DKK | DKK |
| SEB | Skandinaviska Enskilda Banken | SE | Nordics | 1 | SEB-A.ST | SEK | SEK |
| SHB | Svenska Handelsbanken | SE | Nordics | 1 | SHB-A.ST | SEK | SEK |
| SWED | Swedbank | SE | Nordics | 1 | SWED-A.ST | SEK | SEK |
| INGA | ING Groep | NL | Benelux | 1 | INGA.AS | EUR | EUR |
| ABN | ABN AMRO Bank | NL | Benelux | 1 | ABN.AS | EUR | EUR |
| KBC | KBC Group | BE | Benelux | 1 | KBC.BR | EUR | EUR |
| RABO | Rabobank | NL | Benelux | 0 | | | EUR |
| BNP | BNP Paribas | FR | France | 1 | BNP.PA | EUR | EUR |
| GLE | Société Générale | FR | France | 1 | GLE.PA | EUR | EUR |
| ACA | Crédit Agricole SA | FR | France | 1 | ACA.PA | EUR | EUR |
| DBK | Deutsche Bank | DE | Germany | 1 | DBK.DE | EUR | EUR |
| CBK | Commerzbank | DE | Germany | 1 | CBK.DE | EUR | EUR |
| SAN | Banco Santander | ES | Spain | 1 | SAN.MC | EUR | EUR |
| BBVA | BBVA | ES | Spain | 1 | BBVA.MC | EUR | EUR |
| CABK | CaixaBank | ES | Spain | 1 | CABK.MC | EUR | EUR |
| SAB | Banco Sabadell | ES | Spain | 1 | SAB.MC | EUR | EUR |
| BKT | Bankinter | ES | Spain | 1 | BKT.MC | EUR | EUR |
| UNI | Unicaja Banco | ES | Spain | 1 | UNI.MC | EUR | EUR |
| UCG | UniCredit | IT | Italy | 1 | UCG.MI | EUR | EUR |
| ISP | Intesa Sanpaolo | IT | Italy | 1 | ISP.MI | EUR | EUR |
| BAMI | Banco BPM | IT | Italy | 1 | BAMI.MI | EUR | EUR |
| BPE | BPER Banca | IT | Italy | 1 | BPE.MI | EUR | EUR |
| BMPS | Banca Monte dei Paschi di Siena | IT | Italy | 1 | BMPS.MI | EUR | EUR |

`lei` is filled in Section 1 by matching each EU bank's name against the bank names in the 2025 release, and printed for the reviewer. A bank with no match in the 2025 release is listed in the review file and in `decisions/OPEN.md`; it is not dropped until the reviewer says so. UK banks are not in any release from 2021 on; their `lei` is filled from GLEIF in Section 3.

### 3.2 Sources

| need | source | stored as |
|---|---|---|
| EBA history | `tr_oth.csv` and `tr_cre.csv` of the 2021, 2022, 2023, 2024 and 2025 releases, with `TR_Metadata.xlsx` and `SDD.xlsx` of each. Confirmed by the reviewer on 2026-11-02: 2025 files at `https://www.eba.europa.eu/assets/TE2025/Full_database/883401/{file}`, 2024 files at `https://www.eba.europa.eu/assets/TE2024/Full_database/256109/{file}`. The 2021 to 2023 URLs are read from each year's release page on eba.europa.eu and recorded in the manifest. | `data/raw/eba/{year}/` |
| Bridge capital | Pillar 3 Data Hub or bank Pillar 3 reports, fixed in instruction 02 | fixed in instruction 02 |
| Bank reports | Annual reports, half year reports and Pillar 3 reports from each bank's investor relations site, downloaded by `scripts/fetch_reports.py` from URLs listed in `data/manual/report_urls.csv` | PDFs in `data/reports/` (gitignored), hashes in `data/raw/report_manifest.csv` |
| Share prices | yfinance `Ticker(t).history(start, end, auto_adjust=False)`, column `Close` | `data/raw/market/prices.parquet` |
| FX | ECB `https://data-api.ecb.europa.eu/service/data/EXR/D.{CCY}.EUR.SP00.A?format=csvdata` for GBP, SEK, NOK, DKK, USD | `data/raw/fx/{CCY}.csv` |
| Sovereign yields | FRED `https://fred.stlouisfed.org/graph/fredgraph.csv?id=IRLTLT01{CC}M156N` for GB, SE, NO, DK, FI, NL, BE, FR, DE, ES, IT | `data/raw/fred/{CC}.csv` |

Every pull writes `data/raw/MANIFEST.json` (pull time UTC, URL, sha256, bytes, row count, first and last date where the file has dates). `data/reports/` is gitignored because of size; `data/raw/report_manifest.csv` (bank_id, doc_type, period, url, sha256, bytes, pages, downloaded_utc) is committed, and the provenance test (Section 5.3) reads the committed page text cache `data/raw/report_text/{sha256}.jsonl.gz` (one JSON line per page: page number, extracted text), so the suite runs offline without the PDFs.

### 3.3 Periods

- **EBA reference dates:** 2020-09-30 to 2025-06-30, quarterly.
- **Fiscal years:** FY2021 to FY2025. **Half years:** H1 2022 to H1 2026.
- **KPI dates:** every 31 Dec (fiscal year) and every 30 Jun (rolling 12 months) from 2021-12-31 to 2026-06-30, where the inputs exist.
- **Source by period** (`config.toml [sources]`, enforced by the source map, Section 5.1): EBA for EU banks for reference dates to 2025-06-30; bank reports for EU banks for 2025-06-30 (seam test only), 2025-12-31 and 2026-06-30; bank reports for UK banks for every date.

---

## 4. Conventions

1. **Units.** All monetary values stored in units of the reporting currency (not thousands or millions). The scale stated on the source page is applied on entry and recorded in `unit_scale`.
2. **Signs.** Expenses, impairments and tax are stored as positive numbers. A reversal (a net release) is stored negative. The internal formulas in Section 5.2 then add and subtract as written.
3. **Year to date.** EBA and report P&L values are year to date. FY = the 31 Dec value. H1 = the 30 Jun value. Rolling 12 months at 30 Jun of year y: R(y) = H1(y) + FY(y − 1) − H1(y − 1), all 3 from one source family.
4. **Averages.** Average balance for a fiscal year = (closing balance at 31 Dec of y − 1 + closing balance at 31 Dec of y) / 2. Average for a rolling 12 months at 30 Jun of y = (balance at 30 Jun of y − 1 + balance at 30 Jun of y) / 2. Both ends from one source family; a report's comparative column counts as the same source family as its current column.
5. **Source family.** `eba`, `p3` (Pillar 3 data, Data Hub or bank Pillar 3 report), `report` (annual or half year report). Section 5.1 says which family fills which field.
6. **Local currency first.** Every KPI is computed in reporting currency. Conversion to EUR is applied only to sized values (Section 5.6) and only after the KPI is computed: 31 Dec or 30 Jun ECB rate for balance sheet values, the mean of daily ECB rates over the period for P&L values.
7. **Basis points and percent.** Code holds decimals. Tables show % to 2 decimals and bps to 1 decimal.
8. **Underlying figures.** Underlying = reported adjusted for the one offs in `data/manual/one_offs.csv` only, each added back or removed before tax at the amount the bank discloses. Tax on one offs is not adjusted. KPIs are computed on both bases with a `basis` column.
9. **Failed or missing values** keep their rows with a `status` column and a blank value, never a fallback number.
10. **Merger breaks.** A bank with a row in `data/manual/mergers.csv` whose target total assets exceed `merger_materiality` of the acquirer's total assets at the last reference date before completion gets a break at the completion date. Year on year changes that span a break, and the driver decomposition for the fiscal year containing it, are blank with status `merger_break`.
11. **Tax rate for sizing.** t̄ = (sum of tax over the 3 fiscal years ending at the KPI date) / (sum of profit before tax over the same years). If the sum of profit before tax is ≤ 0, or t̄ falls outside [0, 0.6], use the country rate in `[tax_fallback]` and set status `tax_fallback`.
12. **Prices.** Close on the last trading day on or before the KPI date, in price currency, divided by 100 when yfinance reports the currency as `GBp`.
13. **Lineage ID.** `lineage_id` = first 12 hex characters of sha256 of `bank_id|ref_date|field|source_family|locator`, where `locator` is the EBA item code and release year, or the report sha256 and page number. Every derived row stores the lineage IDs of its inputs, `;` separated.

---

## 5. Methods (fixed)

### 5.1 Fields and the source map (`config/fields.yaml`, `config/source_map.yaml`)

Internal fields (all stored at reference dates):

| field | meaning |
|---|---|
| interest_income, interest_expense | as in the EBA P&L template |
| dividend_income, net_fees | as in the EBA P&L template |
| total_operating_income | TOTAL OPERATING INCOME, NET |
| admin_expenses, resolution_dgs_contrib, depreciation | as in the EBA P&L template |
| impairments_fin | impairment or reversal on financial assets not at fair value through profit or loss |
| provisions, impairments_nonfin | as in the EBA P&L template |
| pbt | profit or loss before tax from continuing operations |
| pat | profit or loss after tax from continuing operations |
| profit_owners | profit attributable to owners of the parent |
| total_assets, total_liabilities, total_equity | as in the EBA balance sheet templates |
| minority_interests | non controlling interests in equity |
| cash_cb | cash, cash balances at central banks and other demand deposits |
| debt_securities | debt securities, all accounting portfolios, carrying amount |
| loans_all | loans and advances, all accounting portfolios, gross carrying amount |
| loans_customers_gross, loans_customers_allowance | loans and advances to counterparties other than central banks and credit institutions, gross and accumulated impairment |
| loans_households_gross | loans and advances to households, gross |
| npl_gross, npl_allowance | non performing loans and advances, gross and accumulated impairment |
| deposits_customers | deposits from households, non financial corporations, other financial corporations and general governments |
| trading_assets | financial assets held for trading |
| cet1, tier1, rwa, leverage_exposure | as in the EBA capital, RWA and leverage templates |
| at1_instruments | capital instruments eligible as AT1 |
| intangibles_deduction | the CET1 deduction for intangible assets including goodwill (stored positive) |
| lcr, nsfr | as reported in KM1 (p3 and report families only) |
| fte, customers | period end headcount (full time equivalent) and customer count, where reported |
| at1_coupons | AT1 coupons paid in the period, from the statement of changes in equity |
| shares_out | ordinary shares outstanding net of treasury shares at the reference date |

Derived quantities (`bpb/kpi.py`):

- nii = interest_income − interest_expense
- other_income = total_operating_income − nii − net_fees
- opex = admin_expenses + resolution_dgs_contrib + depreciation
- ppp = total_operating_income − opex
- iea = cash_cb + debt_securities + loans_all
- loans_customers_net = loans_customers_gross − loans_customers_allowance
- tangible_equity = total_equity − minority_interests − at1_instruments − intangibles_deduction
- tax = pbt − pat
- profit_to_ordinary = profit_owners − at1_coupons

Section 1 maps each EBA field by matching its label in `TR_Metadata.xlsx` exactly (case and spacing normalised) and writes `config/eba_map_{year}.csv` (field, item code, template, label as printed in the metadata). A field with no exact label match, or more than 1, is listed in `decisions/OPEN.md` with the candidate items and labels; it is not guessed. The source map names, for each field and each period in Section 3.3, the one source family allowed to fill it.

### 5.2 KPIs (`config/kpis.yaml`, `bpb/kpi.py`)

| kpi | numerator | denominator | average denominator | unit | direction |
|---|---|---|---|---|---|
| rote | profit_to_ordinary | tangible_equity | yes | pct | higher |
| roa | profit_owners | total_assets | yes | bps | higher |
| ppp_assets | ppp | total_assets | yes | bps | higher |
| nim | nii | iea | yes | bps | higher |
| fee_share | net_fees | total_operating_income | no | pct | higher |
| cost_income | opex | total_operating_income | no | pct | lower |
| cost_assets | opex | total_assets | yes | bps | lower |
| cost_of_risk | impairments_fin | loans_customers_gross | yes | bps | lower |
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

P&L numerators are FY values at 31 Dec and rolling 12 month values at 30 Jun (Convention 4.3). Balance sheet ratios with no average use the reference date value. `income_fte`, `cost_fte` and `cost_customer` are the only KPIs converted to EUR before ranking (Convention 4.6, P&L rate for the numerator); every other KPI is a pure ratio. `context` KPIs are computed and shown but never ranked, sized or given a verdict. A KPI with any missing input is blank with status `missing_input` naming the field.

### 5.3 Checks (`bpb/checks.py`)

Each check writes rows to CHECKS (Section 6.2). A failed row keeps its data with a flag.

1. **Provenance** (report and p3 families): normalise the value and the page text (remove thousands separators of the form `,`, `.`, thin space or space between digit groups; brackets mean negative; strip currency signs), then the value divided by `unit_scale` must appear as a number on the cited page, compared to the number of decimals shown on the page. Fail = the row is excluded from every KPI.
2. **Balance sheet:** |total_assets − total_liabilities − total_equity| / total_assets ≤ `bs_tol`.
3. **Income:** |total_operating_income − (nii + dividend_income + net_fees + other components listed in fields.yaml)| / total_operating_income ≤ `income_tol`. For report rows, only the components the bank's income statement shows.
4. **CET1:** |reported CET1 ratio − cet1 / rwa| ≤ `cet1_tol_bps` / 10000, where a reported ratio exists.
5. **Period length:** a P&L value at 30 Jun is a 6 month year to date figure and at 31 Dec a 12 month figure; report entries carry `period_months` and must match.
6. **Currency:** a bank's `report_ccy` never changes; any change needs a row in `data/manual/fx_events.csv` (bank_id, date, from, to, source_url).
7. **Seam 1, capital:** at 2025-06-30, cet1, rwa and leverage_exposure from eba and from p3 agree within `seam_capital_tol`, per bank.
8. **Seam 2, P&L:** at 2025-06-30, every P&L and balance sheet field from eba and from report, per bank: absolute and relative difference. No threshold; the table is the finding.
9. **Outliers:** quarter on quarter change of each EBA field more than `outlier_z` standard deviations from that bank's own mean change over the history; flagged only.

### 5.4 Peer groups (`bpb/peers.py`)

- Features per bank at each 31 Dec from FY2023 on, each the mean of its 3 latest fiscal year values: ln(total_assets in EUR), loans_customers_net / total_assets, fee_share, loans_households_gross / loans_customers_gross, trading_assets / total_assets, loan_deposit.
- Standardise each feature across banks (mean 0, standard deviation with ddof 0). `scipy.cluster.hierarchy.linkage(method="ward")`. For k in `k_range`, cut with `fcluster(criterion="maxclust")`; keep the k whose every cluster has at least `min_cluster_size` banks and whose `sklearn.metrics.silhouette_score` is highest; ties go to the smaller k. If no k qualifies, stop (rule 4).
- Stability: `stability_reps` bootstrap draws of banks with replacement (seed `peer_seed`); duplicates removed; recluster the drawn set with the same k; for each original cluster, its Jaccard similarity with the best matching bootstrap cluster over the drawn banks. A bank's stability = the mean over draws of its own cluster's Jaccard. Below `stability_flag` → flagged `borderline`.
- Adjusted Rand Index (`sklearn.metrics.adjusted_rand_score`) between consecutive years' labels over banks present in both.
- Groups per bank: `cluster` (primary), `market` (Section 3.1 market column), `universe` (all banks). `data/manual/peer_overrides.yaml` (bank_id, year, cluster, reason) applies after clustering; empty at start.
- Peer sets always exclude the bank itself.

### 5.5 Benchmarks (`bpb/benchmark.py`)

- Target for a bank on a ranked KPI = `scipy.stats.mstats.hdquantiles` of its peers' values at p = 0.75 (higher is better) or p = 0.25 (lower is better). Median = the same estimator at p = 0.5.
- Interval: `bench_reps` bootstrap draws of the peer values with replacement (seed `bench_seed`), the same estimator each time, 5th and 95th percentiles.
- Position: percentile rank = share of peers the bank beats, ties count half; robust z = (value − peer median) / (1.4826 × MAD of peers), signed so positive is better.
- Trend: OLS slope per year of the KPI and of (target − value) over the latest 3 fiscal years; blank if fewer than 3.
- Noise: `inside_noise` = the bank's value lies inside the target's interval.
- Verdict: `leading` if better than the target; `lagging` if worse than the median; else `in_line`. Inside noise overrides to `in_line`.
- Peer groups with fewer than `min_peers` other banks with a value → status `too_few_peers`, blank.

### 5.6 Gap sizing (`bpb/gaps.py`)

At each KPI date, for each bank and each peer group, for each of cost_income, cost_of_risk, nim, fee_share where the bank is worse than its target and not inside noise. I = total_operating_income, F = net_fees, O = other_income + dividend_income, C = opex, LLP = impairments_fin, L̄ = average loans_customers_gross, ĪEA = average iea, T̄E = average tangible_equity, starred values are targets:

- Δπ_CI = (CI − CI\*) × I
- Δπ_CoR = (CoR − CoR\*) × L̄
- Δπ_NIM = (NIM\* − NIM) × ĪEA
- Δπ_fee = s\*(I − F)/(1 − s\*) − F
- ΔRoTE = Δπ × (1 − t̄) / T̄E (t̄ from Convention 4.11)
- Joint: NII′ = NIM′ × ĪEA where NIM′ = NIM\* if the NIM gap is sized else NIM; F′ from s′ the same way with O fixed: F′ = s′(NII′ + O)/(1 − s′); I′ = NII′ + F′ + O; C′ = CI′ × I′; LLP′ = CoR′ × L̄; Δπ_joint = (I′ − C′ − LLP′) − (I − C − LLP). Overlap = sum of standalones − Δπ_joint.
- Excess capital = max(0, cet1_ratio − peer median) × rwa, reported separately.
- cost_assets and cost_fte are never sized (they measure the same cost base as cost_income).
- Every sized value is computed in reporting currency, then converted to EUR (Convention 4.6).
- Range: for each bank and gap, min and max over the 3 peer groups × 2 bases; headline = cluster group, underlying basis.

### 5.7 Drivers (`bpb/drivers.py`)

- RoTE tree, with A = average total_assets: RoTE = (NII/A + F/A + O/A − C/A − LLP/A − OTH/A) × (1 − t) × (A / T̄E), where O = other_income + dividend_income, OTH = provisions + impairments_nonfin + any other line between operating income and pbt (so the bracket equals pbt / A exactly), t = tax / pbt for that period, and RoTE here is computed on profit before minorities and AT1 coupons. The difference between this and the KPI `rote` is reported as `minorities_and_at1` and is not a driver.
- Drivers: NII/A, F/A, O/A, C/A, LLP/A, t, A/T̄E (OTH/A is held at the bank's own value and its difference is reported as `other_below_line`).
- Reference bank = peer median of each driver (and a second run at the target quantile of each, direction by its effect on RoTE). Exact Shapley value over the 7 drivers: φ_i = Σ over subsets S not containing i of |S|!(7 − |S| − 1)!/7! × [f(S ∪ {i}) − f(S)], f evaluated with drivers in S at the bank's values and the rest at the reference.
- Cost to income year on year: CI = C/I, two factor Shapley of ΔCI between ΔC and ΔI.
- NII year on year: volume = NIM(y − 1) × ΔĪEA, rate = ΔNIM × ĪEA(y − 1), cross = ΔNIM × ΔĪEA.
- Losses (pbt ≤ 0): t is blank and the tax driver is set to the reference value with status `loss_year`.

### 5.8 Valuation (`bpb/valuation.py`)

- Listed banks only. P/TBV at each 31 Dec from FY2021: price (Convention 4.12) / (tangible_equity / shares_out), with TBV per share converted from report_ccy to price_ccy at the same date's ECB cross rate.
- Per year: OLS of P/TBV on underlying rolling RoTE (pct) and sovereign spread (home country 10 year yield minus DE, December monthly value, percentage points), HC3 standard errors (statsmodels). Report α, β, γ, their standard errors, R², n.
- Implied cost of equity = g + 1/β with g = `growth`, blank if β ≤ 0.
- Checks: `statsmodels.RLM` with `HuberT()`; Cook's distance from the OLS fit, banks above 4/n named; pooled OLS over all years with year dummies and standard errors clustered by bank. If the 90% interval of the pooled β contains 0, every valuation uplift is blank with status `beta_not_significant`.
- Uplift for a bank = β × (RoTE gap in pct points, joint, cluster group, underlying) × TBV per share, with a 90% interval from β ± 1.645 × se.

### 5.9 Outputs (`bpb/report.py`, `bpb/dashboard.py`, `bpb/cli.py`)

- One page A4 PDF per bank at the latest KPI date (reportlab, Helvetica, `invariant=1`): header (name, market, cluster label and stability); KPI table (value, peer median, target, percentile, verdict); quartile strip chart; top 3 sized gaps outside noise with their range; Shapley waterfall; valuation uplift with interval or its blank status; footnotes for overrides, merger breaks, seam flags, tax fallback.
- League tables: `outputs/tables/league_{kpi}_{group}_{date}.csv` and one HTML page per KPI.
- Streamlit app `bpb/dashboard.py` reading only `outputs/`; every figure shows its lineage IDs on click (an expander listing `bpb trace` output).
- CLI (`[project.scripts] bpb = "bpb.cli:main"`): `bpb build`, `bpb trace <lineage_id>`, `bpb bank <bank_id>`.

---

## 6. Signatures and schemas (fixed)

### 6.1 Signatures

```python
# bpb/config.py
@dataclass(frozen=True)
class Config: ...                                    # one nested frozen dataclass per config table
def load_config(path: str | Path = "config.toml") -> Config

# bpb/ingest.py
def load_eba(release_year: int, raw_root: Path, eba_map: pd.DataFrame, universe: pd.DataFrame) -> pd.DataFrame   # FACTS rows
def load_report_entries(path: Path, manifest: pd.DataFrame) -> pd.DataFrame                                      # FACTS rows
def load_p3(raw_root: Path, universe: pd.DataFrame) -> pd.DataFrame                                              # FACTS rows, body in Section 2
def apply_source_map(facts: pd.DataFrame, source_map: dict) -> tuple[pd.DataFrame, pd.DataFrame]                 # (kept, rejected)
def build_facts(cfg) -> pd.DataFrame                                                                             # writes data/processed/facts.parquet

# bpb/fx.py
def ecb_rates(raw_root: Path) -> pd.DataFrame                    # date, ccy, per_eur
def to_eur(value: float, ccy: str, date: date, kind: str, rates: pd.DataFrame, period_start: date | None) -> float   # kind: "bs" or "pl"
def from_eur(value: float, ccy: str, date: date, kind: str, rates: pd.DataFrame, period_start: date | None) -> float

# bpb/kpi.py
def derived(facts: pd.DataFrame) -> pd.DataFrame
def rolling_12m(pl: pd.DataFrame) -> pd.DataFrame
def averages(bs: pd.DataFrame) -> pd.DataFrame
def compute_kpis(facts: pd.DataFrame, kpis: dict, one_offs: pd.DataFrame, rates: pd.DataFrame) -> pd.DataFrame   # KPI

# bpb/checks.py
def provenance(entries: pd.DataFrame, text_root: Path) -> pd.DataFrame
def identities(facts: pd.DataFrame, cfg) -> pd.DataFrame
def seam_capital(facts: pd.DataFrame, cfg) -> pd.DataFrame
def seam_pl(facts: pd.DataFrame) -> pd.DataFrame
def outliers(facts: pd.DataFrame, cfg) -> pd.DataFrame
def run_checks(facts: pd.DataFrame, cfg) -> pd.DataFrame          # CHECKS

# bpb/peers.py
def features(kpi: pd.DataFrame, facts: pd.DataFrame, year: int) -> pd.DataFrame
def cluster(features: pd.DataFrame, cfg) -> tuple[pd.Series, int, float]          # labels, k, silhouette
def stability(features: pd.DataFrame, k: int, cfg) -> pd.Series
def peer_groups(kpi: pd.DataFrame, facts: pd.DataFrame, cfg) -> pd.DataFrame      # PEERS

# bpb/benchmark.py
def target(values: np.ndarray, p: float) -> float
def target_interval(values: np.ndarray, p: float, reps: int, rng) -> tuple[float, float]
def benchmark(kpi: pd.DataFrame, peers: pd.DataFrame, cfg) -> pd.DataFrame          # BENCH

# bpb/gaps.py
def size_gaps(bench: pd.DataFrame, kpi: pd.DataFrame, facts: pd.DataFrame, rates: pd.DataFrame, cfg) -> pd.DataFrame   # GAPS
def joint_gap(bank: dict, targets: dict) -> float

# bpb/drivers.py
def rote_tree(drivers: dict) -> float
def shapley(f: Callable[[dict], float], bank: dict, ref: dict) -> dict
def decompose(kpi: pd.DataFrame, facts: pd.DataFrame, peers: pd.DataFrame, cfg) -> pd.DataFrame   # DRIVERS
def ci_change(c0, i0, c1, i1) -> dict
def nii_change(nim0, iea0, nim1, iea1) -> dict

# bpb/valuation.py
def ptbv(facts: pd.DataFrame, prices: pd.DataFrame, rates: pd.DataFrame, universe: pd.DataFrame) -> pd.DataFrame
def fit_year(df: pd.DataFrame) -> dict
def fit_pooled(df: pd.DataFrame) -> dict
def uplift(gaps: pd.DataFrame, fits: pd.DataFrame, ptbv: pd.DataFrame) -> pd.DataFrame          # VALUATION

# bpb/lineage.py
def lineage_id(bank_id: str, ref_date: str, field: str, family: str, locator: str) -> str
def trace(lineage_id: str, root: Path) -> pd.DataFrame

# bpb/report.py, bpb/cli.py
def build_profile(bank_id: str, date: date, root: Path, out: Path) -> Path
def main(argv: list[str] | None = None) -> int
```

Arguments this document does not imply go to OPEN; session 0 lists them in `PLAN.md`.

### 6.2 Schemas (column order fixed)

- **FACTS** (`data/processed/facts.parquet`): bank_id, lei, ref_date, field, value, ccy, unit_scale, period_months, family, locator, lineage_id, status
- **report_entries.csv** (`data/manual/`): bank_id, ref_date, field, value_as_printed, unit_scale, value, ccy, period_months, doc_type, report_sha256, page, snippet, entered_utc
- **report_urls.csv** (`data/manual/`): bank_id, doc_type (annual, half_year, pillar3), period, url
- **one_offs.csv** (`data/manual/`): bank_id, ref_date, period_months, field, amount, description, report_sha256, page
- **mergers.csv** (`data/manual/`): acquirer_id, target_name, completion_date, target_total_assets, target_ccy, source_url
- **KPI** (`outputs/tables/kpi.csv`): bank_id, date, kpi, basis, value, numerator, denominator, unit, family, inputs_lineage, status
- **CHECKS** (`outputs/tables/checks.csv`): check, bank_id, ref_date, field, value_a, value_b, diff_abs, diff_rel, threshold, passed, note
- **PEERS** (`outputs/tables/peers.csv`): year, bank_id, cluster, k, silhouette, stability, borderline, override_reason
- **BENCH** (`outputs/tables/bench.csv`): date, bank_id, kpi, basis, group, n_peers, value, median, target, target_lo, target_hi, pct_rank, robust_z, trend_kpi, trend_gap, inside_noise, verdict, status
- **GAPS** (`outputs/tables/gaps.csv`): date, bank_id, group, basis, gap, delta_pi_lc, delta_pi_eur, delta_rote_pts, tax_rate, tax_status, status
- **GAPS_JOINT** (`outputs/tables/gaps_joint.csv`): date, bank_id, group, basis, sum_standalone_eur, joint_eur, overlap_eur, joint_rote_pts, excess_capital_eur
- **DRIVERS** (`outputs/tables/drivers.csv`): date, bank_id, reference, driver, bank_value, ref_value, shapley_pts, other_below_line_pts, minorities_and_at1_pts, status
- **VALUATION_FITS** (`outputs/tables/valuation_fits.csv`): year, n, alpha, beta, beta_se, gamma, gamma_se, r2, coe_implied, huber_beta, cooks_named, status
- **VALUATION** (`outputs/tables/valuation.csv`): date, bank_id, price, price_ccy, tbvps, ptbv, rote_gap_pts, uplift_ptbv, uplift_lo, uplift_hi, status
- **spec_log.csv** (`outputs/tables/`): run_utc, spec_id, description, params_json, result_json

---

## 7. config.toml contents

```toml
[run]
seed = 20261102

[sources]
eba_first = "2020-09-30"
eba_last = "2025-06-30"
report_dates_eu = ["2025-06-30", "2025-12-31", "2026-06-30"]
report_first_uk = "2020-12-31"
latest = "2026-06-30"

[eba]
releases = [2021, 2022, 2023, 2024, 2025]
files = ["tr_oth.csv", "tr_cre.csv", "TR_Metadata.xlsx", "SDD.xlsx"]
max_commit_mb = 50

[fx]
currencies = ["GBP", "SEK", "NOK", "DKK", "USD"]

[sovereign]
countries = ["GB", "SE", "NO", "DK", "FI", "NL", "BE", "FR", "DE", "ES", "IT"]
benchmark = "DE"

[checks]
bs_tol = 0.005
income_tol = 0.005
cet1_tol_bps = 5
seam_capital_tol = 0.001
outlier_z = 4.0

[merger]
merger_materiality = 0.10

[peers]
first_year = 2023
k_range = [2, 3, 4, 5]
min_cluster_size = 6
stability_reps = 1000
stability_flag = 0.6
peer_seed = 20261103

[bench]
min_peers = 5
bench_reps = 2000
bench_seed = 20261104
ci = 0.90

[gaps]
sized = ["cost_income", "cost_of_risk", "nim", "fee_share"]
hand_check_banks = ["LLOY", "ISP", "SWED"]
hand_check_tol_eur = 100000

[drivers]
tol_pts = 0.01

[valuation]
growth = 0.02
ci = 0.90
cooks_factor = 4.0

[tax_fallback]
GB = 0.28
SE = 0.206
NO = 0.25
DK = 0.26
FI = 0.20
NL = 0.258
BE = 0.25
FR = 0.2583
DE = 0.30
ES = 0.30
IT = 0.28

[tolerances]
ratio_recompute = 1e-12
fx_roundtrip = 1e-9
```

`[tax_fallback]` values are approximate headline rates for banks, used only when Convention 4.11 triggers the fallback, and every use is reported.

---

## 8. Section list (PLAN.md expands exactly these; add or remove nothing)

### Section 1: Foundation and EBA history
- 1.1 `scripts/pull_data.py --stage eba`: download every file in `[eba] files` for every release, record URLs, filter oversized CSVs to universe banks (Correction 8), write `MANIFEST.json`. Test: manifest hashes match committed files; each release holds exactly 4 reference dates and they run from 2020-09-30 to 2025-06-30 with no gap.
- 1.2 Fill `lei` in `universe.csv` for EU banks (Section 3.1). Write `config/eba_map_{year}.csv` for every release (Section 5.1). Review evidence: the universe table with LEIs and matched EBA names; every map with item codes and labels; every OPEN field.
- 1.3 `bpb/ingest.py` `load_eba`, `apply_source_map`, `build_facts` for EBA rows; `bpb/lineage.py`. Tests: a synthetic EBA frame loads to the FACTS schema; a value from a disallowed family is rejected; lineage IDs are stable across runs.
- 1.4 `bpb/fx.py` with `scripts/pull_data.py --stage fx`. Tests: round trip local → EUR → local within `fx_roundtrip` for every currency on 3 dates; P&L rate is the period mean of daily rates.
- 1.5 `bpb/kpi.py`: derived quantities, rolling 12 months, averages, every KPI except rote (Correction 4) for EU banks. Tests: each KPI recomputed from its stored numerator and denominator within `ratio_recompute`; rolling formula on a hand example; averages use both ends from one family; a KPI with a missing input is blank with `missing_input`.
- 1.6 `bpb/checks.py` identities, period length, currency and outliers on EBA rows. Review evidence: the full KPI table for 3 banks (ISP, SWED, BBVA) at every date; every failed check row; counts of KPI rows by status.
- 1.7 `data/manual/mergers.csv` for every acquisition by a universe bank completed between 2020-09-30 and 2026-06-30, each with a source URL; materiality computed (Convention 4.10). Review evidence: the full table with the materiality ratio.

### Section 2: Bridge data
- 2.1 Pillar 3 loader per instruction 02.
- 2.2 `data/manual/report_urls.csv` for every EU bank: annual reports FY2024 and FY2025, half year reports H1 2025 and H1 2026. `scripts/fetch_reports.py`: download, hash, extract page text to `data/raw/report_text/`, write `report_manifest.csv`.
- 2.3 Enter every field of Section 5.1 that the reports show for 2024-12-31 (comparatives), 2025-06-30, 2025-12-31 and 2026-06-30 into `report_entries.csv` (rule 16).
- 2.4 `checks.provenance`, `seam_capital`, `seam_pl`. Tests: provenance passes on 3 synthetic pages written with different separator styles and fails on a value that is not on the page. Review evidence: provenance pass rate (must be 100% for kept rows), both seam tables in full, every missing field per bank.
- 2.5 KPIs extended to 2025-12-31 and 2026-06-30 for EU banks.

### Section 3: UK banks, valuation inputs and one offs
- 3.1 UK banks: LEIs from GLEIF, report URLs FY2020 to FY2025 and H1 2021 to H1 2026, entries, provenance.
- 3.2 AT1 coupons, shares outstanding and FTE and customers where shown, for every bank and every 31 Dec from 2020-12-31 and every 30 Jun from 2021-06-30, from reports.
- 3.3 `data/manual/one_offs.csv` from the banks' own disclosed adjusting items; underlying KPIs.
- 3.4 rote for every bank; `scripts/pull_data.py --stage market --stage fred`. Review evidence: rote for every bank at every date; one offs table; market data coverage per ticker.

### Section 4: Peers, benchmarks and gaps
- 4.1 `bpb/peers.py`. Tests: on a synthetic 3 cluster dataset of 30 points with known labels, the method returns k = 3 and ARI 1; stability of a perfectly separated set is 1.
- 4.2 `bpb/benchmark.py`. Tests: leave one out is enforced; Harrell Davis matches `hdquantiles` on a hand set; verdict rules on synthetic values.
- 4.3 `bpb/gaps.py` with `tests/fixtures/hand_check.xlsx` built by you from the 3 `hand_check_banks` inputs with spreadsheet formulas (not pasted values), and a test that every sized value matches within `hand_check_tol_eur`. Test: joint gap equals the sum of standalones when only 1 gap is sized.
- 4.4 First PDF profile for the 3 hand check banks. Review evidence: PEERS for every year, cluster feature means, BENCH and GAPS for the 3 banks, the 3 PDFs rendered to PNG.

### Section 5: Drivers and valuation
- 5.1 `bpb/drivers.py`. Tests: Shapley values sum to the gap within `tol_pts` for every bank and date; Shapley on a purely additive function equals the per driver differences; rote_tree reproduces pbt based RoTE exactly.
- 5.2 Cost to income and NII year on year splits. Tests: both sum exactly to the change.
- 5.3 `bpb/valuation.py`. Tests: OLS matches `numpy.linalg.lstsq` on the same data; implied CoE on a synthetic set built from a known CoE. Review evidence: VALUATION_FITS in full, Cook's distance per year, the pooled fit.

### Section 6: Outputs and write up
- 6.1 PDFs for every bank, league tables, HTML pages.
- 6.2 Streamlit dashboard and `bpb trace`. Test: 20 random numbers sampled from the PDFs' source tables (seed from config) each trace to a FACTS row with a locator.
- 6.3 `bpb build` from raw files; running it twice leaves `git status` clean.
- 6.4 `README.md`: what it is, how to run it, answers to Section 1 questions, tables generated from the CSVs (test that the README matches them), figures with one callout each in the prose before the figure, the seam table, honest caveats (accounting differences across countries, the seam, one offs, small peer groups, the valuation interval), and what the project does not do. `docs/METHODS.md`: Sections 4 and 5 of this document.
- 6.5 Final fresh clone run and tidy.

Writing rules for README, docs and report text: plain English, conversational but technical; numerals, not words, for numbers; no hyphens joining sentences; none of the words robust, resilient, rigorous, leveraging, grounded; no filler.

---

## 9. What session 0 must produce

`instructions/00_kickoff.md` (this file), `WORKFLOW.md` and `Project Outline/Bank_Performance_Benchmarking.md` are already committed. If any is missing, stop and say so in the status file; do not recreate them.

### Step 0.0: plan and scaffolding (commit `step 0.0: plan and scaffolding`)

1. `PLAN.md`: Sections 1 to 6 from Section 8. For each step, one paragraph stating what is built, the file, the signatures from Section 6 it implements, the tests (file and test name), the outputs, and the review evidence. Expand, do not summarise, add or remove no step. Anything left unspecified is marked OPEN in `PLAN.md` and listed in `decisions/OPEN.md` and the status file, not decided.
2. `CLAUDE.md`: Sections 0, 4 and 6 of this document verbatim, then an empty `## Amendments` heading.
3. `config.toml`: Section 7 exactly.
4. `config/fields.yaml` (Section 5.1 field table and derived quantities), `config/kpis.yaml` (Section 5.2 table), `config/source_map.yaml` (Section 3.3 source by period, one entry per field).
5. `review/TEMPLATE.md`, headings in this order: Section; Steps completed (one line each with commit hash); Evidence (one subsection per numeric claim, raw rows via `to_string()`); Tests run (exact command and full output); Fresh-clone check; Runtime per step; Deviations from PLAN.md; Not verified; Open questions; Files changed; Reviewer reads (ordered, shortest sufficient set).
6. `decisions/OPEN.md` (header only, items appended as found), and `decisions/data_sources.md`, `decisions/periods_and_seam.md`, `decisions/valuation_inputs.md`, each restating its decisions from Section 2 in 5 lines or fewer.
7. `docs/CONVENTIONS_RESOLVED.md`: Section 4 items 1 to 13 numbered as here.
8. `pyproject.toml`: `[build-system]` setuptools ≥ 68 with `setuptools.build_meta`; `[project]` name `bpb`, version `0.1.0`, requires-python ≥ 3.12; runtime numpy, pandas, scipy, statsmodels, scikit-learn, pyarrow, duckdb, openpyxl, pyyaml, requests, yfinance, pdfplumber, matplotlib, reportlab, streamlit; dev extra pytest, pytest-socket, ruff, pypdf, pymupdf; `[project.scripts] bpb = "bpb.cli:main"`; `[tool.setuptools] packages = ["bpb"]`; `[tool.pytest.ini_options] pythonpath = ["."]`.
9. `requirements-lock.txt` per rule 15.
10. `.gitattributes`: `* text=auto eol=lf`, `*.png binary`, `*.pdf binary`, `*.parquet binary`, `*.xlsx binary`, `*.gz binary`, `data/raw/** -text`, `tests/fixtures/** -text`.
11. `.gitignore`: `data/processed/**`, `data/reports/**`, `.env`, `__pycache__/`, `*.py[cod]`, `.venv/`, `venv/`, `.pytest_cache/`, `*.egg-info/`, `.DS_Store`, `Thumbs.db`, `~$*`, `.vscode/`, `.ruff_cache/`.
12. `.github/workflows/ci.yml`: on push and pull request, ubuntu-latest, Python 3.12 via `astral-sh/setup-uv`, install from the lock then `pip install -e . --no-deps`, run `ruff check .` and `pytest -p socket --disable-socket -q`.
13. `README.md` with a 5 line description and "results pending"; `bpb/__init__.py`; `bpb/cli.py` with a `main` that prints usage and returns 0; `tests/test_placeholder.py` that imports `bpb`; `data/manual/universe.csv` (Section 3.1, `lei` blank); `data/manual/report_entries.csv`, `report_urls.csv`, `one_offs.csv`, `mergers.csv`, `fx_events.csv` with headers only; `data/manual/peer_overrides.yaml` empty list; `.gitkeep` in `data/raw`, `outputs/tables`, `outputs/figures`, `outputs/reports`, `review`, `tests/fixtures`.

Then run the placeholder suite in a fresh venv built from the lock, write `review/section_0.md` (TEMPLATE headings), `instructions/00_kickoff.status.md` per rule 11, commit both, push, stop. Pull no data in session 0.
