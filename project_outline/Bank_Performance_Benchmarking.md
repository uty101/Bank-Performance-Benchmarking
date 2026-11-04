# Bank Performance Benchmarking

Final project outline, 2 November 2026. Repo: https://github.com/uty101/Bank-Performance-Benchmarking

## Purpose

Benchmark around 30 European banks against peers with a similar business mix on profitability, efficiency, margin, risk and capital. For each bank, find where it sits against the best quartile, size what closing each gap is worth in euros of profit and in its valuation multiple, and show which driver causes the gap.

Three rules hold everywhere. Every figure traces to an EBA row, a Pillar 3 cell or an annual report page. Every ratio is recomputed from its stored parts. Every output is rebuilt from raw files by one command.

## Data sources

The panel has two periods. History, Sep 2020 to Jun 2025, comes from the EBA transparency exercise, which was discontinued after its June 2025 reference date. The bridge, Jun 2025 onward, takes capital and asset quality from the Pillar 3 Data Hub and P&L and balance sheet lines from interim and annual reports for every bank.

Seven sources feed one long table keyed on bank, reference date, field and source. A source map fixes which source may fill which field in which period, so two sources never silently overwrite each other.

| Source | Period | Fields | Format |
| --- | --- | --- | --- |
| EBA transparency exercise, 2021 to 2025 releases | Sep 2020 to Jun 2025, quarterly | P&L, balance sheet, capital, RWAs, leverage, asset quality | CSV with item codes and a metadata dictionary per release |
| EBA Pillar 3 Data Hub | Jun 2025 onward, quarterly | Key metrics (KM1), own funds, RWAs, leverage, LCR, NSFR, credit quality | Bulk download, XBRL csv |
| Interim and annual reports, every bank | H1 2025 onward, plus all UK history | Net interest income, fees, costs, impairments, tax, loans, deposits, interest earning assets, intangibles, FTEs, branches, customers | Hand built CSV, one row per figure with source file, page and date |
| UK Pillar 3 disclosures | FY2020 onward | UK KM1, own funds, RWAs, leverage | Hand built CSV, same rules |
| Market data (yfinance) | Every reference date | Share price and shares outstanding only | Parquet snapshot, pinned |
| ECB reference rates | Every reference date | EUR, GBP, SEK, NOK, DKK | Parquet snapshot, pinned |
| OECD long term rates (FRED) | Every reference date, monthly | 10 year sovereign yields for the 7 markets and Germany | Parquet snapshot, pinned |

Tangible book value per share is computed from the project's own tangible equity and share count, never taken from yfinance. Prices are matched to the reporting date, with a second series at the results release date for the valuation module.

Pinned snapshots of every raw file are committed (or hashed and fetched by a script where size prevents committing), so tests run without network access.

## Universe and calendar

The starting universe is 31 banks across 7 markets, covering FY2021 to FY2025 plus H1 2026 as the latest point. Phase 1 confirms each EU bank's LEI against the 2025 EBA bank list and drops any bank that is missing.

| Market | Banks | Listed |
| --- | --- | --- |
| UK | Lloyds, NatWest, Barclays, HSBC, Santander UK | 4 of 5 |
| Nordics | Nordea, DNB, Danske Bank, SEB, Handelsbanken, Swedbank | 6 of 6 |
| Benelux | ING, ABN AMRO, KBC, Rabobank | 3 of 4 |
| France | BNP Paribas, Société Générale, Crédit Agricole SA | 3 of 3 |
| Germany | Deutsche Bank, Commerzbank | 2 of 2 |
| Spain | Santander, BBVA, CaixaBank, Sabadell, Bankinter, Unicaja | 6 of 6 |
| Italy | UniCredit, Intesa Sanpaolo, Banco BPM, BPER, Monte dei Paschi | 5 of 5 |

Unlisted banks are benchmarked but left out of the valuation module.

**Calendar rules.**

- EBA and FINREP P&L is year to date at each reference date. Annual figures use the December value; half years use June.
- Rankings use rolling 12 month P&L at June dates (H1 this year plus FY last year minus H1 last year), never annualised half years, because year end impairment and fee true ups make H1 times 2 wrong.
- Balance sheet denominators are averages of opening and closing values for the period.
- Banks with a non December year end are not in the universe.

**Mergers.** A bank that completes a material acquisition (target over 10% of the acquirer's assets) gets a break flag at the completion date. KPIs on either side of the break are not compared year on year, and the driver decomposition skips that year. Phase 1 lists every deal in the window with its completion date and source.

## Module 1: Ingestion

Each source gets its own loader that writes one long Parquet table with the same columns: bank LEI, reference date, field, value, currency, unit, source, source locator. Raw files are never edited in place; DuckDB queries the Parquet layer.

- **EBA loader.** One mapping file per release from EBA item code to internal field name, because item codes and template layouts change between releases. A test fails if any mapped item code is absent from that release's metadata dictionary.
- **Pillar 3 loader.** Maps KM1 and the other templates by template, row and column. Units and signs are normalised on load.
- **Report extraction loader.** Claude Code downloads each report PDF, stores its SHA256, extracts the page text with pdfplumber, and writes candidate figures to the hand built CSV with file, page and a verbatim snippet. Every row is checked by the provenance test in Module 3 before it can be used.
- **Market and FX loaders.** Write dated snapshots once; later runs read the snapshot, so results never shift because a vendor revised history.
- **Source map.** A YAML file naming which source fills each field in each period. The loader rejects any value that arrives from a source the map does not allow.

## Module 2: Definitions and KPI engine

A single definitions file holds every KPI: its numerator and denominator fields, unit, whether higher is better, and whether the denominator is averaged. The engine computes every KPI from stored parts in local currency and stores the parts beside the result, so any ratio can be recomputed by hand.

| KPI | Formula | Unit | Better |
| --- | --- | --- | --- |
| RoTE | Net profit to shareholders after AT1 coupons / average tangible equity | % | Higher |
| RoA | Net profit / average total assets | bps | Higher |
| Pre provision profit / assets | (Total operating income − operating expenses) / average total assets | bps | Higher |
| NIM | Net interest income / average interest earning assets | bps | Higher |
| Fee share | Net fees and commissions / total operating income | % | Higher |
| Cost to income | Operating expenses / total operating income | % | Lower |
| Cost to assets | Operating expenses / average total assets | bps | Lower |
| Cost of risk | Loan impairment charges / average gross loans | bps | Lower |
| NPL ratio | Non performing loans / gross loans | % | Lower |
| NPL coverage | Loan loss allowances / non performing loans | % | Higher |
| CET1 ratio | CET1 capital / RWAs | % | Higher |
| Leverage ratio | Tier 1 capital / leverage exposure | % | Higher |
| RWA density | RWAs / total assets | % | Context only |
| Loan to deposit | Net customer loans / customer deposits | % | Context only |
| LCR and NSFR | As reported in KM1 | % | Higher |
| Income per FTE | Total operating income / average FTEs | EUR thousands | Higher |
| Cost per FTE | Operating expenses / average FTEs | EUR thousands | Lower |
| Cost per customer | Operating expenses / customers, where reported | EUR | Lower |

Tangible equity is shareholders' equity minus AT1 instruments minus goodwill and intangibles. Where a bank does not report AT1 coupons separately, the engine uses the coupon disclosed in the capital instruments note and flags the row.

"Context only" KPIs feed peer grouping and the driver tree but are never ranked, because a higher RWA density or loan to deposit ratio is not better or worse on its own.

FX conversion happens only after ratios are computed, and only for sized values in euros: period end rates for balance sheet items, period average rates for P&L items.

## Module 3: Cleaning and reconciliation

Nothing reaches the KPI engine until it passes these checks. Failures are written to a checks report with the bank, field, date and reason; flagged rows are kept and marked, never dropped silently.

- **Provenance.** For every report row, the cited page's extracted text must contain the value after normalising thousands separators, brackets for negatives and stated units. A row that fails cannot be used.
- **Identities.** Total assets equal liabilities plus equity within 0.5%. Total operating income equals the sum of its components. Reported CET1 ratio equals recomputed CET1 / RWAs within 5 bps. Every P&L value covers the period length its reference date implies, and a bank's reporting currency never changes between dates without an entry in an FX events file.
- **Seam 1, capital.** At June 2025, CET1 capital, RWAs and leverage exposure from EBA and from the Pillar 3 Data Hub must agree within 0.1%, bank by bank.
- **Seam 2, P&L.** H1 2025 is entered from half year reports for every EU bank and compared with EBA, field by field. The table of differences is published in the README. No adjustment is applied; the size of the seam is the finding.
- **One source per calculation.** A rolling 12 month figure takes all 3 of its pieces from the same source, so H1 2025 from EBA is never mixed with FY2025 from a report.
- **Outliers.** A quarter on quarter move more than 4 standard deviations from the bank's own history is flagged for review, not removed.
- **One offs.** A separate CSV holds one offs that banks themselves disclose (restructuring charges, disposal gains, levies), each with its source page. KPIs are computed both reported and underlying. No adjustment is ever made on judgement alone.

## Module 4: Peer groups

The primary peer group is a business model cluster, so a Spanish retail lender is not told to look like a Swedish wholesale funded mortgage bank. Every bank also gets 2 secondary groups: its home market and the full universe.

- **Features.** Log total assets, loans to assets, fee share, retail share of credit exposures, trading assets to total assets, loan to deposit ratio. Each is a 3 year average, so a single odd year does not move a bank between groups.
- **Method.** Standardise the features, run Ward hierarchical clustering, and pick the number of clusters by silhouette score subject to a minimum of 6 banks per group. With 31 banks that allows 5 groups at most; expect 3 or 4.
- **Stability.** Bootstrap the banks 1,000 times and report each bank's Jaccard stability with its cluster. Report the Adjusted Rand Index between consecutive years' clusters. A bank below 0.6 stability is flagged on its profile as a borderline member.
- **Override file.** A hand override is allowed only with a written reason in a YAML file, and every override is shown on the bank's PDF.

The cluster labels are named after the features that drive them (for example "large universal", "domestic retail") once the result is in, not before.

## Module 5: Benchmarking and quartiles

Each bank's target on each ranked KPI is the best quartile of its peers (the 75th percentile where higher is better, the 25th where lower is better) with the bank itself left out, so a bank never pulls its own target towards it.

- **Estimator.** The quartile uses the Harrell Davis estimator, which behaves better than the plain sample quantile at 6 to 10 observations. A 90% bootstrap interval is reported beside every threshold.
- **Position.** Percentile rank within the peer group, distance to the median and to the best quartile, and a robust z score using median and MAD.
- **Trend.** The 3 year slope of each KPI and of the gap itself, so the profile says whether the gap is closing or widening.
- **Significance.** A gap is marked "inside the noise" when the bank's value lies within the bootstrap interval of the threshold. Inside the noise gaps are shown but never sized. Each KPI gets a one line verdict per bank: leading (better than the best quartile), in line, or lagging (worse than the median), with the size of the gap.
- **League tables.** One per ranked KPI, per peer group, per reference date.

## Module 6: Gap sizing

Each gap is sized as the extra pre tax profit the bank would earn at the best quartile value, holding its own balance sheet fixed, then taken through tax to a RoTE uplift. Gaps inside the noise (Module 5) are not sized. Every sized gap is shown as a range across the 3 peer groups and across reported and underlying figures, with the primary group's underlying figure as the headline.

```latex
\Delta\pi_{CI} = (CI_{bank} - CI^{*}) \cdot I \qquad \Delta\pi_{CoR} = (CoR_{bank} - CoR^{*}) \cdot \bar{L} \qquad \Delta\pi_{NIM} = (NIM^{*} - NIM_{bank}) \cdot \overline{IEA}
```

For fee share, the extra fees needed to reach the target share s* while other income stays fixed:

```latex
\Delta F = \frac{s^{*}(I - F)}{1 - s^{*}} - F
```

```latex
\Delta RoTE = \frac{\Delta\pi \cdot (1 - \bar{t})}{\overline{TE}}
```

I is total operating income, F net fees, L gross loans, IEA interest earning assets, TE tangible equity, and t the bank's 3 year average effective tax rate, so a one off tax charge does not distort the uplift.

- **Standalone and joint.** Each gap is sized on its own, then all are closed together by setting every driver to target and recomputing the full tree. The joint figure is reported beside the sum of standalones, and the difference is labelled as overlap. A higher NIM, for example, also lowers cost to income, so the 2 cannot be added. Cost to assets and cost per FTE measure the same cost base as cost to income, so only cost to income is sized and the other 2 are context.
- **Capital is not profit.** CET1 above the peer median is sized as excess capital, (CET1 ratio minus peer median) times RWAs, and reported as capital return capacity, never added to the profit figures.
- **Hand check.** For 3 banks, every sized figure is recomputed in a spreadsheet and the test requires a match within EUR 0.1 million.

## Module 7: Driver decomposition

The RoTE gap between a bank and its peer reference (a synthetic bank built from the peer median of each component; a second run uses the best quartile of each) is split across 7 drivers with Shapley values, so the result does not depend on the order the drivers are changed in and the parts add up exactly to the gap.

```latex
RoTE = \left(\frac{NII}{A} + \frac{F}{A} + \frac{O}{A} - \frac{C}{A} - \frac{LLP}{A}\right) \cdot (1 - t) \cdot \frac{A}{TE}
```

The 7 drivers are NII, fees, other income, costs and impairments (each over average assets), the tax rate and leverage. The tree uses the period's actual tax rate so it reproduces reported RoTE exactly; the 3 year average rate is only for gap sizing. Shapley needs 2 to the power 7, or 128, evaluations of the tree per bank, which is trivial to compute. Banks with a loss in the period are decomposed the same way, because Shapley does not need logs.

Driver tree, read left to right: RoTE = pre tax RoA × (1 − tax rate) × leverage (assets / tangible equity); pre tax RoA = NII / assets + fees / assets + other income / assets − operating costs / assets − impairments / assets.

Each bank's PDF shows the gap as a waterfall over these 7 drivers, read left to right from RoTE.

- **Cost to income, year on year.** The change is split into cost growth and income growth with 2 factor Shapley, reported in percentage points.
- **Net interest income, year on year.** The change is split into volume (growth in interest earning assets at last year's NIM), rate (change in NIM on last year's assets) and the cross term, which is reported separately rather than hidden inside either effect.
- **Test.** For every bank and year, the driver contributions sum to the total change within 0.01 percentage points.

## Module 8: Valuation link

A cross sectional regression of price to tangible book on RoTE, refitted at each year end, turns a RoTE gap into a valuation multiple gap. The slope also gives an implied cost of equity, which is a useful sense check on whether the fit means anything.

```latex
\frac{P}{TBV}_{i} = \alpha + \beta \, RoTE_{i} + \gamma \, \text{SovSpread}_{i} + \varepsilon_{i}
```

The justified multiple, P/TBV = (RoTE − g) / (CoE − g), is linear in RoTE with slope 1 / (CoE − g). So with growth g set at 2%, the implied cost of equity is g + 1/β, reported each year.

- **RoTE input.** Rolling 12 month underlying RoTE, because the market prices sustainable earnings, not one offs.
- **Country term.** About 27 listed banks across 7 markets cannot carry 6 country dummies, so a single continuous term is used: the 10 year sovereign spread over Bunds, from the OECD long term rate series on FRED, pinned.
- **Uncertainty.** The valuation uplift is β times the RoTE gap times TBV, with its interval from the standard error of β. R squared, n and the interval sit next to every figure on every output.
- **Checks.** Huber regression as a check on outliers, Cook's distance to name any bank that drives the fit, and a pooled fit across years with year effects to test whether β is stable. If the pooled β interval includes 0, the outputs say so and drop the valuation figures for that year.

## Module 9: Outputs

Every number on every output carries a lineage ID, and one command prints the chain behind it: KPI, its stored parts, the source rows, and the EBA item code or the report file and page.

- **One page PDF per bank (reportlab).** Header with peer group and stability score; KPI table against peer median and best quartile with percentile rank; a quartile strip chart; the top 3 sized gaps that are outside the noise; a Shapley waterfall of the RoTE gap; the valuation uplift with its interval; footnotes for overrides, merger breaks and seam flags.
- **League tables.** One per ranked KPI and peer group, as CSV and as an HTML page.
- **Streamlit dashboard.** Pick a bank and a peer group; see its position on every KPI, 5 year trends, sized gaps and the driver waterfall. Clicking any figure shows its lineage chain.
- **Seam report.** The 2 reconciliation tables from Module 3, published as they come out.
- **CLI.** `bpb build` rebuilds everything from raw files; `bpb trace <lineage id>` prints a figure's chain; `bpb bank <name>` builds one profile.

## Engineering standard and invariants

The repo uses uv with a lockfile, ruff, pytest and GitHub Actions on every push. CLAUDE.md lists the invariants below, and each one has a test written before the code it guards.

1. Every ratio recomputes from its stored parts to machine precision.
2. Every report figure is found in the extracted text of the page it cites.
3. Balance sheets balance within 0.5%; income components sum to total income.
4. FX round trips (local to EUR and back) return the original value within 1e-9.
5. No ratio is computed on converted values.
6. A rolling figure takes all its pieces from one source.
7. Every value arrives from a source the source map allows for that field and period.
8. Shapley contributions sum to the total gap within 0.01 percentage points.
9. Sized gaps match the hand built spreadsheet for 3 banks within EUR 0.1 million.
10. A bank's own value never enters its own peer threshold.
11. Every number in a PDF or the dashboard resolves through `bpb trace` to a raw row or page.
12. `bpb build` on a fresh clone with pinned snapshots reproduces every output byte for byte, except PDF timestamps.

The README covers what it does, how to run it, the findings with honest caveats (accounting differences across countries, the seam table, one offs, small peer groups, the valuation interval), and what it does not do.

## Build order

Six phases, one Claude Code session per phase, reviewed in chat between sessions. Each phase ends with its gate met and a pushed status file; no phase waits on anything outside the repo.

| Phase | Builds | Gate |
| --- | --- | --- |
| 1. Foundation and EBA history | Scaffolding, CLAUDE.md, definitions file, source map, EBA loader for the 2021 to 2025 releases, KPI engine | KPIs for every EU bank, Sep 2020 to Jun 2025; invariants 1, 3, 4, 5 and 7 green |
| 2. Bridge data | Pillar 3 Data Hub loader, report extraction pipeline, H1 2025 to H1 2026 entries for every EU bank, provenance and seam tests | Provenance at 100%; both seam tables produced |
| 3. UK, market data and one offs | UK report and Pillar 3 entries FY2020 onward, one offs CSV, merger breaks, market, FX and sovereign snapshots | All 31 banks complete to H1 2026; invariant 6 green |
| 4. Peers, benchmarks and gaps | Clustering with stability, leave one out quartiles with intervals, gap sizing standalone and joint, first PDF for 3 banks | Hand check spreadsheet matches; invariants 8 to 10 green |
| 5. Drivers and valuation | Shapley RoTE tree, cost to income and NII splits, valuation regression with its checks | Contributions sum to gaps; implied cost of equity reported per year |
| 6. Outputs and write up | PDFs for every bank, league tables, Streamlit dashboard, trace CLI, README with findings | Invariants 11 and 12 green on a fresh clone |

Phase 2 is the heaviest: roughly 26 EU banks times 3 report periods times about 15 fields, around 1,200 extracted figures. The provenance test is what makes that volume safe to trust.

## What it does not do

- It does not forecast. Every figure is historical; sized gaps say what a bank would earn at peer levels on today's balance sheet, not what it will earn.
- It does not say a gap can be closed. Some gaps are structural (a domestic market's rate level, a regulatory floor), and the peer grouping reduces that but cannot remove it.
- It does not harmonise accounting across countries beyond what FINREP and Pillar 3 already standardise. The seam table shows how large the residual difference is.
- It does not adjust for one offs on judgement, only for those the bank itself discloses.
- It does not cover banks outside the 7 markets, or smaller banks outside the EBA sample.
- It does not give investment advice. The valuation module describes a cross sectional relationship with its uncertainty, not a target price.

## Sources

- EBA, EU wide transparency exercise (discontinued notice): https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise
- EBA, 2025 EU wide transparency exercise: https://www.eba.europa.eu/node/18852
- EBA, The Pillar 3 data hub goes live, 28 January 2026: https://www.eba.europa.eu/node/19224
- EBA, Pillar 3 data hub: https://www.eba.europa.eu/node/18415
