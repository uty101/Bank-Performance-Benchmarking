# Section 0

## Steps completed

- 0.0 plan and scaffolding (7e06f94)

## Evidence

Session 0 makes no numeric claim about data; it pulls no data and writes no analysis code. The checks below are the structural evidence for the scaffolding.

### Config files parse and agree with each other

Command: `.venv/Scripts/python -c` loading `config/fields.yaml`, `config/kpis.yaml`, `config/source_map.yaml` and `data/manual/peer_overrides.yaml`. The script checks that every field has a source map entry and that every KPI input is a field or a derived quantity.

```
fields 40 derived 9 kpis 19 source_map fields 40
fields missing from source map: set() extra: set()
kpi inputs not defined: set()
overrides []
```

`config.toml` was extracted byte for byte from the fenced block in kickoff Section 7 and parses with `tomllib`. Its tables are `bench, checks, drivers, eba, fx, gaps, merger, peers, run, sources, sovereign, tax_fallback, tolerances, valuation`.

### CLAUDE.md is verbatim

`CLAUDE.md` was assembled from kickoff lines 12 to 33 (Section 0), 122 to 136 (Section 4) and 289 to 380 (Section 6), with CR stripped, separated by `---`, then an empty `## Amendments` heading. The Section 4 block was diffed against the kickoff with no difference.

### Universe

`data/manual/universe.csv`: 31 banks plus header, 9 columns. The Section 3.1 columns are in order, then `lei` (blank, last column; position is OPEN-16). UTF-8.

## Tests run

Command, in the working checkout's venv built from the lock:

```
.venv/Scripts/ruff check . && .venv/Scripts/pytest -p socket --disable-socket -q
```

Output:

```
All checks passed!
.                                                                        [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\_pytest\config\__init__.py:894
  C:\Utkarsh\10. Quant Projects\15) Bank Benchmarking Project\Bank-Performance-Benchmarking\.venv\Lib\site-packages\_pytest\config\__init__.py:894: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; socket
    self.import_plugin(arg, consider_entry_points=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
1 passed, 1 warning in 0.05s
```

The warning appears because `-p socket` names the pytest-socket plugin, which pytest already autoloads through its entry point. Sockets are still disabled. The command is fixed by rule 7, so it was not changed.

## Fresh-clone check

Rule 12 applies from Section 1 on. For session 0 the placeholder suite was run in a fresh venv built from the lock, on a clean clone of commit 7e06f94 taken before the push. The clone path was `C:\Users\astha\AppData\Local\Temp\bpb0`. Windows 11, uv 0.11.6.

```
$ git clone <local repo at 7e06f94> /c/Users/astha/AppData/Local/Temp/bpb0
7e06f94 step 0.0: plan and scaffolding
$ uv venv --python 3.12
Using CPython 3.12.13
Creating virtual environment at: .venv
Activate with: .venv\Scripts\activate
$ uv pip install -r requirements-lock.txt
 + wrapt==2.5.2
 + yfinance==1.7.0
$ uv pip install -e . --no-deps
Installed 1 package in 162ms
 + bpb==0.1.0 (from file:///C:/Users/astha/AppData/Local/Temp/bpb0)
$ ruff check .
All checks passed!
$ pytest -p socket --disable-socket -q
.                                                                        [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\_pytest\config\__init__.py:894
  C:\Users\astha\AppData\Local\Temp\bpb0\.venv\Lib\site-packages\_pytest\config\__init__.py:894: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; socket
    self.import_plugin(arg, consider_entry_points=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
1 passed, 1 warning in 0.08s
$ bpb
usage: bpb <command> [args]

commands:
  build               rebuild every output from raw files
  trace <lineage_id>  print the chain behind a figure
  bank <bank_id>      build one bank profile
exit=0
$ git status --porcelain
```

The `uv pip install -r` output is truncated to its last 2 lines; the lock pins 86 packages. `git status --porcelain` printed nothing.

## Runtime per step

| step | measured |
|---|---|
| 0.0 | `uv pip compile` 3.7 s; fresh-clone check 32 s end to end. Authoring time was not measured separately; the session ran from about 12:56 to 13:10 local time. |

## Deviations from PLAN.md

None. One choice in the scaffolding is flagged rather than decided: the position of `lei` in `universe.csv` (OPEN-16).

The source map marks every undecided family as `OPEN-04` or `OPEN-05` instead of choosing one.

## Not verified

- The CI workflow `.github/workflows/ci.yml` has not run yet. It runs on this push, and its result is visible on GitHub Actions.
- The lock was compiled with `--universal`, but installed and tested only on Windows (CPython 3.12.13), not on Linux.
- No EBA, ECB, FRED, yfinance or bank report URL was opened; session 0 pulls no data.

## Open questions

All are in `decisions/OPEN.md` with 2 options each:

- OPEN-01: where the 2021 to 2023 EBA URLs are recorded before step 1.1 downloads them.
- OPEN-02: step 1.1 filters EBA CSVs by LEI before step 1.2 has filled any LEI, and no staging path is fixed for the unfiltered originals.
- OPEN-03: how EU report rows at 2024-12-31 (comparatives) and 2025-06-30 ("seam test only") may serve as opening balances and rolling components.
- OPEN-04: the family (`p3` or `report`) for at1_instruments, intangibles_deduction, lcr and nsfr in the EU bridge, and for every capital field of UK banks.
- OPEN-05: lcr and nsfr for EU banks at EBA-period dates.
- OPEN-06: the components of the income identity (check 3) for EBA rows.
- OPEN-07: no field holds the reported CET1 ratio that check 4 needs.
- OPEN-08: `peers.features` has no rates argument for ln(total_assets in EUR).
- OPEN-09: `benchmark` needs each bank's market, which PEERS does not carry.
- OPEN-10: `valuation.uplift` needs the joint RoTE gap and the pooled fit.
- OPEN-11: how UK LEIs are fetched from GLEIF under rule 8.
- OPEN-12: how the formula results in `hand_check.xlsx` are evaluated.
- OPEN-13: unfixed output paths (PDFs, PNG renders, HTML pages, charts).
- OPEN-14: the trace and README tests read outputs, which rule 7 forbids.
- OPEN-15: test inputs the kickoff leaves unfixed.
- OPEN-16: the column position of `lei` in `universe.csv`.

OPEN-01 and OPEN-02 block step 1.1, OPEN-06 and OPEN-07 affect step 1.6, and OPEN-03 to OPEN-05 shape `config/source_map.yaml`. Deciding these in instruction 01 lets Section 1 run without stopping.

## Files changed

Step 0.0 (7e06f94) added 34 files:

```
.gitattributes
.github/workflows/ci.yml
.gitignore
CLAUDE.md
PLAN.md
README.md
bpb/__init__.py
bpb/cli.py
config.toml
config/fields.yaml
config/kpis.yaml
config/source_map.yaml
data/manual/fx_events.csv
data/manual/mergers.csv
data/manual/one_offs.csv
data/manual/peer_overrides.yaml
data/manual/report_entries.csv
data/manual/report_urls.csv
data/manual/universe.csv
data/raw/.gitkeep
decisions/OPEN.md
decisions/data_sources.md
decisions/periods_and_seam.md
decisions/valuation_inputs.md
docs/CONVENTIONS_RESOLVED.md
outputs/figures/.gitkeep
outputs/reports/.gitkeep
outputs/tables/.gitkeep
pyproject.toml
requirements-lock.txt
review/.gitkeep
review/TEMPLATE.md
tests/fixtures/.gitkeep
tests/test_placeholder.py
```

The review commit adds `review/section_0.md`. The status commit adds `instructions/00_kickoff.status.md`.

## Reviewer reads

1. `decisions/OPEN.md`
2. `PLAN.md`
3. `config/source_map.yaml`
4. `config/fields.yaml`, `config/kpis.yaml`
5. `CLAUDE.md` (check that it is verbatim)
