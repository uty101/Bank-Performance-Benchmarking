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

## Amendments

### Amendments from instructions/01_section_1.md (step 1.0; decisions in `decisions/section_0_review.md`)

1. **Changed signatures.**
   - `bpb/peers.py`: `def features(kpi: pd.DataFrame, facts: pd.DataFrame, year: int, rates: pd.DataFrame) -> pd.DataFrame` (OPEN-08).
   - `bpb/benchmark.py`: `def benchmark(kpi: pd.DataFrame, peers: pd.DataFrame, universe: pd.DataFrame, cfg) -> pd.DataFrame` (OPEN-09).
   - `bpb/valuation.py`: `def uplift(gaps_joint: pd.DataFrame, fits: pd.DataFrame, pooled: dict, ptbv: pd.DataFrame) -> pd.DataFrame`, with `pooled` the dict returned by `fit_pooled` (OPEN-10).
2. **Convention 4.5 (OPEN-04).** For EU banks at bridge dates, cet1, tier1, rwa and leverage_exposure are `p3`; at1_instruments, intangibles_deduction, lcr and nsfr are `report`. For UK banks every field is `report`; a Pillar 3 PDF is entered as a document with doc_type `pillar3` and family `report`.
3. **New field (OPEN-07).** `cet1_ratio_reported` (kind ratio): mapped from the EBA capital template, later from KM1 and reports. Check 4 runs wherever it exists.
4. **Role `bridge_input` (OPEN-03).** `report` rows for EU banks at 2024-12-31 and 2025-06-30 may be opening balances and rolling components for report-family KPIs at 2025-12-31 and 2026-06-30. The KPI value at 2025-06-30 itself stays `eba`.
5. **Output paths (OPEN-13).** PDF profiles `outputs/reports/{bank_id}_{date}.pdf`; page renders `outputs/figures/{bank_id}_{date}.png`; league table pages `outputs/tables/league_{kpi}.html`; charts are drawn in memory and not saved separately.
6. **Crédit Agricole (B.1).** The universe row ACA is replaced by bank_id `CAG`, name `Crédit Agricole Group`, listed 0, ticker blank, price_ccy blank, report_ccy EUR. CAG is benchmarked and left out of valuation. Its bridge figures come from the Group figures published in Crédit Agricole SA's universal registration document and half year report.

### Amendments from instructions/01b_section_1_completion.md (step 1.2b; decisions in `decisions/section_1_review.md`)

7. **Convention 4.1 (OPEN-25).** `eba` rows are in EUR for every bank; `report` and `p3` rows are in the reporting currency. Every `eba` amount is EUR millions (`unit_scale` 1e6, `ccy` `EUR`); every `eba` item whose field has `kind: ratio` in `fields.yaml` is a decimal stored as reported (`unit_scale` 1, `ccy` blank).
8. **Map rules (B.1).**
   1. Unnamed dimensions: every dimension column of the source CSV that a map row does not name in `dim_filter` must equal 0 for the row to match. In `tr_oth.csv` the dimension columns are ASSETS_FV, ASSETS_Stages, Exposure and Financial_instruments. In `tr_cre.csv` they are Portfolio, Country, Exposure, Status, Perf_Status and NACE_codes.
   2. Summed fields: a field with several map rows is the sum of their amounts. If any listed row is absent for a bank and date, the field is missing for that bank and date. It is never a partial sum.
   3. Period length: for P&L items, period_months = 3 × `n_quarters`. Check 5 requires 6 at 30 Jun and 12 at 31 Dec.
9. **Mixed currencies (B.2).** When a derived quantity or check combines values with different `ccy`, the non EUR value is converted to EUR first, using the Convention 4.6 rates: balance sheet values at the reference date rate, P&L values at the mean over the period. The derived row's status gains `fx_combined`. README caveat: averages and rolling figures of `eba` balances for the 5 non EUR banks carry the currency move between their 2 ends.
10. **Changed signature (B.2).** `bpb/kpi.py`: `def derived(facts: pd.DataFrame, rates: pd.DataFrame) -> pd.DataFrame`.

### Amendments from instructions/02_section_2.md (step 2.0; decisions in `decisions/section_1_completion_review.md`)

11. **Bridge capital from bank Pillar 3 reports (B.1).**

The Pillar 3 Data Hub has no documented public bulk download. Its user guides describe only visual tools. Scraping it would be fragile, and that fragility is what this project avoids.

Each EU bank's own Pillar 3 report publishes the same templates, so those are used.

- **`load_p3(raw_root, universe)`** reads the `report_entries.csv` rows whose doc_type is `pillar3` and whose field the source map assigns to `p3`.
- **Family comes from the source map.** A row's family is decided by the source map, by bank group, field and date, never by doc_type. doc_type only says which document the figure came from.
- **The Data Hub** is out of scope. Record this in `decisions/data_sources.md`.

12. **Which template gives which field (B.2).**

Templates are the EU Pillar 3 templates (CRR3 versions where the 2025 and 2026 reports use them). Row numbers are as printed in the bank's own table, and the row label must match.

| field | template | row | column |
|---|---|---|---|
| cet1 | EU KM1 | 1 | the reference date's column |
| tier1 | EU KM1 | 2 | the reference date's column |
| rwa | EU KM1 | 4 (total risk exposure amount; never the pre floor row 4a) | the reference date's column |
| cet1_ratio_reported | EU KM1 | 5 | the reference date's column |
| leverage_exposure | EU KM1 | 13 | the reference date's column |
| lcr | EU KM1 | 17 | the reference date's column |
| nsfr | EU KM1 | 20 | the reference date's column |
| at1_instruments | EU CC1 | 30 (Additional Tier 1 capital: instruments, capital instruments and the related share premium) | amount |
| intangibles_deduction | EU CC1 | 8 (Intangible assets, net of related tax liability), entered positive | amount |
| loans_all | EU CR1 | 010 Loans and advances | gross carrying amount, performing + non performing |
| loans_customers_gross | EU CR1 | 030 + 050 + 060 + 080 | gross, performing + non performing, summed |
| loans_customers_allowance | EU CR1 | 030 + 050 + 060 + 080 | accumulated impairment, performing + non performing |
| loans_households_gross | EU CR1 | 080 Households | gross, performing + non performing |
| npl_gross | EU CR1 | 010 | gross, non performing |
| npl_allowance | EU CR1 | 010 | accumulated impairment, non performing |
| debt_securities | EU CR1 | 090 Debt securities | gross, performing + non performing |

**Summed fields.** A field summed over rows or columns is entered as 1 row per printed number, with the same field name and a `component` note in the snippet. `load_report_entries` sums them, and B.1 of `decisions/section_1_review.md` applies: if any component is missing, the field is missing.

**Signs.** Accumulated impairment is printed negative in CR1. Enter `value_as_printed` as printed and `value` positive (Convention 4.2).

**Row numbers that differ.** If a bank's CR1 numbers its rows differently, match on the row label and write the bank's row number in the snippet.

**Everything else comes from the annual and half year reports.** That covers every P&L field, total_assets, total_liabilities, total_equity, cash_cb, trading_assets and deposits_customers, from the consolidated statements and their notes:

- **total_operating_income:** the income statement's total operating income, or net revenue as the bank names it.
- **income_components_other:** each line between net fees and total operating income as printed, so check 3 can run.
- **admin_expenses:** staff expenses + other administrative expenses.
- **depreciation:** depreciation, amortisation and impairment of property, equipment and intangibles, as printed in operating expenses.
- **resolution_dgs_contrib:** entered only where the income statement shows it as its own line. Where it does not, the field is not entered. The derived opex then treats it as 0, with status `levies_in_admin`, so it is never a missing input.
- **impairments_fin:** credit impairment losses, or net impairment on financial assets, as printed.
- **deposits_customers:** deposits from customers as printed on the balance sheet. If the balance sheet splits customer deposits from deposits by banks, use the customer line only.
- **trading_assets:** financial assets held for trading. If not shown separately, the field is not entered.

13. **Documents and dates for EU banks (B.3).**

Per EU bank, in `report_urls.csv`:

- **annual:** FY2025 annual report or universal registration document. Its 2025-12-31 column, and its 2024-12-31 comparative column, supply both dates.
- **half_year:** H1 2025 report, for 2025-06-30, and H1 2026 report, for 2026-06-30.
- **pillar3:** 2024-12-31, 2025-06-30, 2025-12-31 and 2026-06-30.

**Comparative columns.** A figure is entered from the document where it is the current period, except 2024-12-31 balance sheet values, which come from the FY2025 comparative column. Restated comparatives are not used for any other date.

**Crédit Agricole Group (CAG).** Use the Group columns of Crédit Agricole SA's universal registration document and half year report, and the Group Pillar 3 report, never the CASA columns. Seam 2 shows whether this was done right: CAG total_assets at 2025-06-30 from report and from eba must agree within 2%. If not, stop under rule 4. *Superseded by the scope adjusted gate in amendments from instruction 02b.* *The scope adjusted gate is itself superseded: it is informational (amendment 26).*

14. **Page text cache and provenance (B.4).**

- **Cache.** `data/raw/report_text/{sha256}.jsonl.gz` holds only the pages cited by at least 1 entry, to keep the repo small. Each line is `{"page": n, "text": ...}`, where page is the 1 based physical page index of the PDF, not the printed folio. `scripts/fetch_reports.py --cache-pages` rebuilds it from the entries and the PDFs.
- **Snippet.** Each entry's `snippet` must contain `value_as_printed` verbatim.
- **Provenance rule.** Kickoff 5.3 item 1 applies. A failed row is excluded and listed.

15. **Step 2.3 commits (B.5).** Commit after each bank with message `step 2.3: <bank_id> entries`. The rule 2 one-commit-per-step limit is lifted for step 2.3 only. Work in universe order.

### Amendments from instructions/02b_section_2_continue.md (step 2.0b; decisions in `decisions/section_2_stop_review.md`)

16. **The CAG gate becomes a scope adjusted gate.** Enter 2 new fields from EU LR1 at 2025-06-30 for every EU bank (both `report` family, used by checks only):
   - `lr1_total_assets` (row 1)
   - `lr1_scope_adjustment` (row 2, the adjustment for entities consolidated for accounting purposes but outside the regulatory scope), entered with the sign as printed.

   The gate: |(lr1_total_assets + lr1_scope_adjustment) − eba total_assets| / eba total_assets ≤ 0.02 for every EU bank where LR1 is entered. Use the sign convention so that a printed negative reduces assets. This replaces the CAG only gate. A failure is a rule 4 stop for that bank only: leave its bridge entries out of the KPIs, finish every other bank, and report it. Seam 2 adds a column with the scope adjusted report total assets.

   *Superseded by amendment 26: the gate is informational and blocks no bank.*

17. **No time comparison crosses the family switch.** From this section on, every year on year change, every 3 year trend and every driver decomposition that compares 2 dates uses values from 1 family.
   - FY2024 P&L is entered from the FY2025 annual report's comparative column (role `bridge_input`, all P&L fields and `income_components_other`). FY2024 against FY2025 is then report against report.
   - Where a comparison must span the switch and no same family pair exists, the result is blank with status `family_switch`.

   Record this rule in `decisions/` and CLAUDE.md Amendments. Sections 4 and 5 will apply it.

18. **OPEN-26: (b).** A Pillar 3 workbook (.xlsx) is a valid source.
   - Download and hash it like a PDF.
   - `page` holds `sheet!cell` (for example `KM1!D12`).
   - The text cache stores, per cited sheet, one JSON line `{"page": "<sheet>", "text": ...}` holding the sheet's cell values row by row, tab separated.
   - Provenance checks the value against that text.
   - A report on the Data Hub only: use it if the hub offers a per bank file download (PDF, xlsx or csv) at a URL you can fetch with a script. Treat it as a hashed document with doc_type `pillar3`. Otherwise leave it blank and list it.

19. **Blank and dash cells in a printed template row are 0.**
   - When a template row is printed and a cell in it is `-`, `–` or empty, the component is entered with value 0, and `value_as_printed` holds the dash or `blank`.
   - For these rows, provenance checks that the row label appears on the cited page.
   - A row that is not printed at all stays missing, and B.1 of `decisions/section_1_review.md` still applies.
   - Go back over the committed banks and add the zero components this unlocks (debt_securities, customer loans and allowances).

20. **Depreciation inside administrative expenses.** When the income statement prints no depreciation line, the bank's administrative expenses line is taken to include it. admin_expenses is entered as printed (DBK: compensation and benefits + general and administrative expenses). depreciation is not entered, and opex treats it as 0 with status `dep_in_admin`, exactly like the levies rule.

21. **Insurance lines.** admin_expenses is staff and other administrative expenses as printed on the income statement. Insurance service expenses and technical charges are never added in. Where a bank nets them into revenue under IFRS 17, take the lines as printed. The seam table shows the effect, and the README caveat covers it.

22. **profit_owners is net profit minus non controlling interests,** matching FINREP and the EBA history. For RABO this includes the amounts attributed to Rabobank Certificates and Capital Securities holders: enter them as components summed into profit_owners. AT1 coupons are deducted later, through at1_coupons.

23. **No printed total.**
   - total_operating_income: if the income statement prints no total, it is derived as the sum of the printed income lines, with status `toi_summed`. Enter each line as a component. Applies to CBK and any similar bank.
   - total_liabilities: if no total is printed, it is not entered, and check 2 writes a row with status `no_liabilities_line` and no pass or fail. Applies to CBK and UCG.

24. **Documents you cannot get.**
   - Bankinter returns 403 to scripts. Do not circumvent it. When a current period document cannot be obtained, take the figures from the comparative column of the next document that has them (for H1 2025 P&L, the H1 2026 report), with status `from_comparative`. This applies to any bank. The Pillar 3 dates stay blank unless decision 3 finds a Data Hub file.
   - Commerzbank publishes its Pillar 3 as the "Disclosure Report" (Offenlegungsbericht) on its investor relations site under Reports. Search for those titles before listing it as missing.

25. **Mergers.** Use the first published of these, in order, as the size: total assets, else loans, else the consideration paid. Record which in `size_basis`.
    - Size the UBI branch unit and AXA IM this way.
    - Add RON to `[fx] currencies` (a reviewer change to `config.toml`), re-run the fx stage, and compute Alpha Bank Romania's ratio.
    - BPER and Carige (0.164) is accepted as a material break.

### Amendments from instructions/03_section_3.md (step 3.0; decisions in `decisions/section_2_review.md`)

26. **The scope gate is informational (A.1 item 1).** Check `8b_scope_gate` keeps its rows, with threshold blank and passed blank. No bank is blocked by it. This supersedes amendment 13's CAG gate and the gate rule of amendment 16 (instruction 02b B.1).
   - SHB's report and p3 rows are restored, and its KPIs at 2025-12-31 and 2026-06-30 are computed.
   - The entity check is the combination already in place: provenance on every report figure; seam 1 (p3 against EBA, 72 of 72 within 0.1%); the published seam 2 table.
   - The README states the scope difference for bank insurers as a caveat. Those banks are NDA, DANSKE, SWED, SEB, SHB, KBC, BNP, GLE and CAG, plus any with a total_assets seam above 5%.
27. **Pillar 3 not obtainable (A.1 item 2).** For DNB, SHB and UCG at 2026-06-30, and CBK at every date, take the KM1 figures from the capital adequacy note of the same date's interim or annual report:
   - cet1, tier1, rwa, cet1_ratio_reported and leverage_exposure;
   - lcr and nsfr where printed.

   These rows are family `p3`, with status `p3_from_report`. CR1 fields stay blank where no Pillar 3 exists.

### Amendments from instructions/04_section_4.md (step 3.8; decisions in `decisions/section_3_review.md`, with the 03b and 03c rules they complete)

28. **at1_in_equity (03b B.2, 03c B.1 and B.4).** A flag, 1 or 0, `report` family, read from the annual report: the accounting policy for AT1, or the balance sheet line. A half year date takes the classification from the annual report of the same year, status `class_from_annual`, unless the half year report states a different one. Where it is 0, AT1 is not in total_equity, so the at1_instruments term of tangible_equity is 0, status `at1_liability`. Where it is 1, at1_instruments is deducted.
29. **at1_coupon_in_pl (03c B.1 and B.4).** A flag, `report` family, entered at the same dates as at1_in_equity under the same `class_from_annual` rule: 1 if the coupons are in interest expense, 0 if they are charged to equity or reserves. Where the bond sits and where its coupon is charged are separate questions.
30. **at1_coupons (03b B.3, 03c B.1, OPEN-34).** The coupons charged directly to equity or reserves in the period, entered positive from the statement of changes in equity or the EPS note. It is 0 in 2 cases:
    - at1_coupon_in_pl is 1: status `coupon_in_pl`;
    - the bank had no AT1 in equity during the period, or the period's coupon line is printed as a dash or as nil: status `no_at1_coupon`, citing the page that says so (BMPS: the "no equity instruments" statement, with CC1 row 30 a dash; NDA H1 2026: the cash flow line).

    Coupons printed only net of tax are entered net, status `at1_net_of_tax`.
31. **Comparative columns (OPEN-35).** A comparative column in a later document counts as a printed amount for its date, with status `from_comparative`. This applies to SANUK, DANSKE and ABN.
32. **Dash-only lines (OPEN-35).** A balance sheet non controlling interests line printed only as dashes is 0 with status `no_nci_line`, the same as no line. This applies to BKT.
