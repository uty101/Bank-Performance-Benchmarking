# Status: instructions/02_section_2.md (session 2)

## Outcome

Stopped under rule 4. The review is `review/section_2.md` (a5c5bc0).

## Last step reached

Step 2.3, bank CAG (25ecc99). Commits this session:

- **2.0:** 6efb278
- **2.1:** eb9aecc, with a fix in 92cda21
- **2.2:** 71154d8, with a fix in 811eec3
- **2.3:**
  - NDA 1e8959e
  - DNB c0b5c60
  - DANSKE da57e5b
  - SEB 982c977
  - SHB 0652103
  - SWED f246388
  - INGA efe4b74
  - ABN 23b15dc
  - KBC 8376a6c
  - RABO 26d7e4a
  - BNP fd99099
  - GLE 642a65d
  - CAG 25ecc99

Steps 2.4 and 2.5 were not run.

## Stop reason

The B.3 gate failed. CAG total_assets at 2025-06-30 is 2,614,010m in the report against 2,187,749m from EBA, a relative difference of 0.1948. The limit is 0.02, and B.3 says "If not, stop under rule 4."

The entries are Group figures, not CASA:
- pat and profit_owners agree with EBA within 0.02%.
- Seam 1 agrees within 0.0003%.

The gap is the scope of consolidation. CAG's own EU LR1 (Pillar 3 30/06/2025, p11) bridges it exactly: published total assets of 2 614 011, less 426 262 for entities outside the prudential scope (insurance), gives 2,187,749.

## Questions and blockers for the reviewer

1. **CAG gate.**
   - (a) Use report total_assets as printed, and drop or widen the gate.
   - (b) Gate on report total_assets less LR1 row 2.
   - The same scope gap of about 10-17% shows for the other bank-insurers: NDA, DANSKE, SWED, SEB, KBC, BNP and GLE.
2. **OPEN-26: Pillar 3 only as Excel, or only on the EBA Pillar 3 Data Hub.**
   - (a) Leave these pairs blank, as now.
   - (b) Accept hashed workbooks as sources.
   - The banks affected:
     - Excel only: DNB, DANSKE and KBC at every date. SEB, SHB, INGA, CABK, SAB and UNI at June dates.
     - Data Hub only at 2026-06-30: DNB, SHB, SWED and UCG.
3. **Blank cells in CR1.** A blank or `-` component makes the field missing under decision B.1 (no partial sums).
   - debt_securities is therefore missing for NDA, SEB, SHB, SWED, INGA, ABN and RABO, and for GLE at 2 dates.
   - The customer-loan fields are missing for SHB and SWED, and the customer-loan allowance for ABN.
   - Should a blank template cell count as 0?
4. **DBK admin_expenses and depreciation.** G&A includes depreciation and no depreciation line is printed, so both fields are missing.
5. **Insurance-related lines in admin_expenses.** GLE, BNP and KBC treat them differently.
6. **RABO profit_owners.** It excludes Certificates and Capital Securities holders; EBA's figure includes them.
7. **CBK and UCG.** CBK prints no total operating income or total liabilities, and UCG prints no total liabilities.
8. **Documents not obtained.**
   - Bankinter's H1 2025 report and all its Pillar 3 reports: the site returns 403 bot protection, which was not circumvented.
   - Commerzbank's Pillar 3 PDFs: no direct link found.
9. **Mergers.**
   - BPER–Carige is a new material break, ratio 0.164.
   - BPER–UBI branch unit and BNP–AXA IM remain unsized.
   - Alpha Bank Romania is in RON, which is not in `[fx]`.
10. **Uncommitted work.**
    - In the working tree, not committed because steps 2.4 and 2.5 were not reached:
      - `tests/test_checks.py` (`test_provenance_styles`)
      - `scripts/run_all.py`
    - Scratchpad only (temporary, not in the repo):
      - entries for DBK, CBK, SAN, BBVA, CABK, SAB, BKT and UCG, each checked;
      - partial entries for UNI, ISP, BAMI, BPE and BMPS.
    - The next session starts from DBK.

Other notes:

- **Merger re-check.** The 4 material deals were re-checked, and each source line is printed in the review.
- **CHF.** Added to `[fx]`. REYL's ratio is now 0.0023.
- **Provenance.** 1,889 of 1,889 entries pass, and all 9 hashed merger sizes pass.
- **Checks 2 to 5.** No failures on the entry rows.
- **Fresh clone at 92cda21.** ruff clean, 20 passed.

## git log origin/main --oneline -3

```
a5c5bc0 section 2: review (stopped at step 2.3, CAG total_assets gate)
92cda21 step 2.1: provenance reads ASCII digits only; provenance on mergers.csv rows
811eec3 step 2.2: fix ruff PLW1510 in fetch_reports.py
```
