# Data sources (kickoff Section 2, corrections 1, 6 and 8)

- The EBA transparency exercise stopped; its last release (Dec 2025) runs to 30 Jun 2025, and history Sep 2020 to Jun 2025 comes from the 2021 to 2025 releases.
- The bridge, H1 2025 to H1 2026, comes from bank reports; bridge capital comes from the Pillar 3 Data Hub if it can be pulled by script, else bank Pillar 3 reports (fixed in instruction 02).
- HSBC reports in USD, so USD is in the FX set. An EBA CSV over 50 MB is committed as universe-bank rows only, gzipped, with both files' sha256 and row count in `MANIFEST.json`.
- **Bridge capital (instruction 02 B.1).** Bridge capital comes from each EU bank's own Pillar 3 report (EU KM1, CC1 and CR1), read by `load_p3` from the `report_entries.csv` rows whose doc_type is `pillar3` and whose field the source map assigns to `p3`. The EBA Pillar 3 Data Hub is out of scope: it has no documented public bulk download, its user guides describe only visual tools, and scraping it would be fragile.
- **Sovereign yields (instruction 03b B.1).** Kickoff 3.2's FRED source (`IRLTLT01{CC}M156N`) is replaced: FRED refused the connection in session 3. `scripts/pull_data.py --stage yields` writes `data/raw/yields/{CC}.csv` (period, yield_pct, series) from central bank sources, with the exact URLs in `MANIFEST.json`:
  - SE, DK, FI, NL, BE, FR, DE, ES, IT: ECB Data Portal, `IRS/M.{CC}.L.L40.CI.0000.{CCY}.N.Z` (Maastricht convergence criterion long-term yields; CCY EUR, SEK for SE, DKK for DK);
  - GB: Bank of England IADB, series IUMAMNPY (monthly average yield from British Government Securities, 10 year nominal par yield);
  - NO: Norges Bank data API, `GOVT_GENERIC_RATES/M.10Y.GBON` (government bonds, 10 years, monthly).
