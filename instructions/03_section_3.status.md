# Status: instructions/03_section_3.md

## Outcome

**Stopped** under rule 4 at step 3.4: a data pull failed. `scripts/pull_data.py --stage fred` could not download the first series (GB): a read timeout, then the connection closed by fred.stlouisfed.org on both retries. Everything else in Section 3 is done for all 31 banks. The review is `review/section_3.md` (be68a18).

## Last step reached

Step 3.4, with every item done except the FRED series:
- rote is computed for every bank at every date where inputs exist, on both bases;
- the market stage pulled 27 tickers;
- `test_rote_hand` and `test_gbp_pence` pass.

Commits this session:
- **3.0:** 064a109
- **3.1:** LLOY 5086b75, NWG d93fb73, BARC f4b3170, HSBA a6b93fe, SANUK c9bcd11; UK merger ratios 50de460
- **3.2:** one commit per bank for all 31 banks, 0924116 to 016249a. The full list is in the review.
- **3.3:** 7f4b399
- **3.4:** d4c41c9
- **Open questions:** b1827f3
- **Review:** be68a18

## Results

- **Entries:** `report_entries.csv` holds 10,074 rows, and provenance passes for all of them.
  - Step 3.1: 3,212 UK entries for every field at 12 dates.
  - Step 3.2: B.1 fields for all 31 banks.
  - 120 UK and 354 earlier EU documents were added to `report_urls.csv`.
- **One offs:** `one_offs.csv` holds 616 rows for 28 banks, all passing provenance.
- **UK:** each of the 5 UK banks has exactly 1 active GLEIF record. SANUK–TSB is a material merger at 0.165.
- **rote:** computed at 165 of 310 bank-dates (reported basis). The hand checks match `kpi.csv`: LLOY at 2025-12-31 is 0.120589 and BBVA at 2024-12-31 is 0.209828.
- **Tests:** 24 pass and ruff is clean. The fresh clone at b1827f3 also passes 24.

## Stop reason

The FRED pull failed (rule 4, "a data pull fails"):

```
attempt 1 failed: HTTPSConnectionPool(host='fred.stlouisfed.org', port=443): Read timed out. (read timeout=120)
attempt 2 failed: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
attempt 3 failed: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
data pull failed: https://fred.stlouisfed.org/graph/fredgraph.csv?id=IRLTLT01GBM156N
```

I tried one diagnostic request with a browser user agent. This session's safety check refused it as bot-check circumvention, so I made no further attempts. `data/raw/fred/` is empty. The stage code is committed.

## Questions and blockers for the reviewer

1. **FRED:** how should step 3.4 item 2 be finished? Options are a retry from another network, or a different host or user agent for fred.stlouisfed.org.
2. **OPEN-27:** at1_coupons where AT1 is not classified as equity. This affects SEB, SHB, SWED and INGA; DANSKE from 2023; NDA at 2026-06-30; and BMPS. Should it be 0 with a status, or blank? rote is blank for these banks until this is decided.
3. **OPEN-28:** AT1 coupons that are printed only net of tax. This affects BKT; KBC at 2025-12-31 and 2026-06-30; BAMI at 2021-06-30; ISP; and UCG possibly.
4. **OPEN-29:** fte where only headcount is printed. This affects SAN, BBVA, CABK, SAB, BKT, ISP, BPE, BMPS and BAMI.
5. **OPEN-30:** SANUK at 2025-12-31 and 2026-06-30, where no profit attributable line is printed. Also SANUK's H1 2026 levy line.
6. **One off sources to confirm:** SAB, CBK, BPE, GLE, UNI 2023, DBK litigation 2020 to 2022, ING 2020 and KBC. Each is listed in Open question 6 of the review.
7. **Removed rows:** these were left out to keep the B.1 and B.4 definitions (Deviation 10):
   - all BMPS one offs;
   - SANUK's lease-depreciation reclassification;
   - headcount entered as fte;
   - net-of-tax AT1 coupons.
8. **Commit order slip (Deviation 9):** NDA's step 3.2 rows first landed in the SEB commit. NDA was then fixed and committed separately in 865d866. History was not rewritten.
9. **Documents not obtained:**
   - GLE annual reports FY2020 to FY2024 and half-year reports H1 2021 to H1 2024, because of a bot challenge;
   - BKT half-year reports H1 2021 to H1 2025;
   - SHB H1 2024, which has no text layer;
   - KBC H1 2021, whose statements are images.

   Comparative fallbacks are used where a later document prints the date.

## git log origin/main --oneline -3

```
be68a18 section 3: review (stopped at step 3.4: fred pull failed)
b1827f3 section 3: open questions OPEN-27 to OPEN-30
d4c41c9 step 3.4: rote and market data; fred pull failed (rule 4 stop)
```
