# Section 6

Section 6 is stopped under rules 4 and 5 at step 6.0, before any code or data changed. The test that instruction 06 A.1 item 1 specifies contradicts the formula it tests (OPEN-42). This file covers the stop only.

## Steps completed

None. Step 6.0 was started and not committed. Steps 6.1 to 6.5 were not run.

The only repo changes this session are `decisions/OPEN.md` (OPEN-42 to OPEN-44), this file and the status file.

## Evidence

The tables below come from a read only yfinance query and the committed files. They are a preview: `data/raw/` and `outputs/` are unchanged, and `splits.csv` is not written.

### E1 to E5: splits, the contradiction and the size of the fix

```
E1 split rows found, yfinance 1.7.0, 2020-12-01 to 2026-11-03, 28 tickers
 ticker bank_id       date    ratio
  NWG.L     NWG 2022-08-30 0.928571
BMPS.MI    BMPS 2022-09-26 0.010000

E2 the formula and the test on a synthetic 1:10 consolidation
date  adjusted_close  ratio_after_t  formula_close_x_ratio  test_as_written_10x
  d1            10.0            0.1                    1.0                100.0
  d2            10.0            0.1                    1.0                100.0
  d3            10.0            1.0                   10.0                 10.0
  d4            10.0            1.0                   10.0                 10.0

E3 NWG.L either side of the consolidation, pence
      date ticker     close  formula_x_ratio  test_direction_div_ratio
2022-08-26  NWG.L 270.19989       250.899898                290.984497
2022-08-30  NWG.L 249.00000       249.000000                249.000000

E4 every bank and year-end the fix touches, under the formula (preview; no output changed)
bank_id       date split_date    ratio     price  price_after    tbvps     ptbv  ptbv_after
    NWG 2021-12-31 2022-08-30 0.928571  2.430615     2.257000 2.804205 0.866775    0.804863
   BMPS 2021-12-31 2022-09-26 0.010000 18.586618     0.185866      NaN      NaN         NaN

E5 valuation_fits.csv as committed
 year  n      beta  beta_se       r2  coe_implied cooks_named status
 2021 22  1.041093 1.541212 0.089965     0.980529     CBK;UNI     ok
 2022 23  4.499947 1.718445 0.478576     0.242225        BMPS     ok
 2023 25  4.526150 2.261670 0.399721     0.240938        BMPS     ok
 2024 25  6.631913 1.230680 0.553407     0.170786        BMPS     ok
 2025 25 10.433434 1.487395 0.740798     0.115846        LLOY     ok
```

- **E1:** the query ran to 2026-11-03, past the `MARKET_END` of 2026-08-01, so a later split would have shown. There is none. For all 28 tickers, Close today matches the committed `prices.parquet` with a maximum relative difference of 0.0 on every shared date.
- **E2:** the formula and the test give different answers on the same input.
- **E3:** the formula's 250.90p runs into the next close of 249.00p. The test's direction gives 290.98p.
- **E4:** the fix touches 2 rows. Only NWG 2021-12-31 changes a P/TBV, from 0.866775 to 0.804863. BMPS 2021-12-31 has no tbvps, so its P/TBV stays blank.
- **E5:** BMPS is named in Cook's distance in 2022 to 2024, and all 3 year ends fall after its split. The split fix cannot change those namings.

### E6: snippets on their cited pages (OPEN-44)

```
report_entries.csv rows                                   10967
snippet on the cited cached page, verbatim                 6184
snippet not on the page                                    4783
  of which start with a "component n/m:" note              4783
  of which match after dropping it, whitespace normalised  4783
```

## Tests run

```
$ .venv/Scripts/python -m pytest -p socket --disable-socket -q
52 passed, 130 warnings in 499.05s (0:08:19)
$ .venv/Scripts/ruff check .
All checks passed!
```

The tail of the output was kept. `test_unsplit` was not added.

## Fresh-clone check

Clone path `C:/bpbs6`, at:

```
a485b37 Add instructions for section 6
```

This commit holds the same code as the end of this session, because only records were added after it.

```
$ git clone https://github.com/uty101/Bank-Performance-Benchmarking.git C:/bpbs6
$ uv venv --python 3.12
$ uv pip install -r requirements-lock.txt
$ uv pip install -e . --no-deps
$ .venv/Scripts/ruff check .
$ .venv/Scripts/python -m pytest -p socket --disable-socket -q
============================== warnings summary ===============================
.venv\Lib\site-packages\_pytest\config\__init__.py:894
  C:\bpbs6\.venv\Lib\site-packages\_pytest\config\__init__.py:894: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; socket
    self.import_plugin(arg, consider_entry_points=True)

tests/test_gaps.py: 65 warnings
  C:\bpbs6\.venv\Lib\site-packages\pycel\excelformula.py:995: DeprecationWarning: ast.Str is deprecated and will be removed in Python 3.14; use ast.Constant instead
    op = ast.Str(s=type(node_op).__name__)

tests/test_gaps.py: 64 warnings
  C:\Users\astha\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none\Lib\ast.py:587: DeprecationWarning: Attribute s is deprecated and will be removed in Python 3.14; use value instead
    return Constant(*args, **kwargs)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
52 passed, 130 warnings in 403.39s (0:06:43)
```

The commands ran as an `&&` chain with only the last 15 lines kept, so ruff's own line is cut off. pytest ran, so ruff exited 0.

## Runtime per step

No step ran. The test suite took 8m19s locally and 6m43s in the fresh clone.

## Deviations from PLAN.md

None. No PLAN step was run.

## Not verified

- **BMPS 2021-12-31 price.** Yahoo's series may also carry an adjustment for the October 2022 rights issue, which `Stock Splits` would not undo. The formula gives 0.185866, which looks low for that date, but no hashed document was checked. It affects no P/TBV, because tbvps is blank at that date.
- **A.1 items 2 to 5, 8, 9 and 10** were not applied, and the item 4 income statement lines were not printed.
- **The rest of instruction 06** was read for conflicts, not built, so step 6.1 onwards may raise more.

## Open questions

1. **OPEN-42 (blocking):** which of the formula and `test_unsplit` stands?
2. **OPEN-43 (before step 6.3):** `run_utc` as `HEAD`'s committer date cannot leave `git status` empty, because `spec_log.csv` is itself committed.
3. **OPEN-44 (before step 6.2):** 4,783 snippets carry a `component n/m:` note that is not on the page.

## Files changed

- `decisions/OPEN.md`
- `review/section_6.md`
- `instructions/06_section_6.status.md`

## Reviewer reads

1. `instructions/06_section_6.status.md`
2. `decisions/OPEN.md`, OPEN-42 to OPEN-44
3. This file, E1 to E4
