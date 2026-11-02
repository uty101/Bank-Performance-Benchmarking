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
