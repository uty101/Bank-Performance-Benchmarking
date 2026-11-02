# Data sources (kickoff Section 2, corrections 1, 6 and 8)

- The EBA transparency exercise stopped; its last release (Dec 2025) runs to 30 Jun 2025, and history Sep 2020 to Jun 2025 comes from the 2021 to 2025 releases.
- The bridge, H1 2025 to H1 2026, comes from bank reports; bridge capital comes from the Pillar 3 Data Hub if it can be pulled by script, else bank Pillar 3 reports (fixed in instruction 02).
- HSBC reports in USD, so USD is in the FX set. An EBA CSV over 50 MB is committed as universe-bank rows only, gzipped, with both files' sha256 and row count in `MANIFEST.json`.
