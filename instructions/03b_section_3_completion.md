# instructions/03b_section_3_completion.md: finish Section 3

Finish Section 3 by applying the decisions below, then end the section. Entries already committed stand unless Section B says otherwise. Precedence (rule 13): this file beats `instructions/03_section_3.md`.

---

## A. Review

The stop was correct: FRED refused the connection. You were also right not to retry with a browser user agent.

The reviewer read rote at reported basis for every bank and date. Where it is filled, it is plausible:

| bank | date | rote | reviewer's comment |
|---|---|---|---|
| NWG | 2025-12-31 | 19.2% | |
| HSBA | 2023-12-31 | 14.5% | |
| LLOY | 2025-12-31 | 12.1% | |
| BBVA | 2024-12-31 | 21.0% | |
| CABK | 2021-12-31 | 22.2% | reported value; Bankia negative goodwill |
| UNI | 2021-12-31 | 22.9% | reported value; Liberbank negative goodwill |

The CABK and UNI items are what the underlying basis should remove, where the banks list them.

The 2 hand checks (LLOY and BBVA) match `kpi.csv`.

The gaps are almost entirely the AT1 question, OPEN-27. SEB, SHB, SWED, INGA, DANSKE and BMPS have no rote at all, and NDA has 1 date.

---

## B. Decisions

### 1. Sovereign yields come from central bank sources, not FRED

Use these sources; nothing from FRED. These hosts serve plain API requests, and none needs a browser user agent. If a pull fails, it is a rule 4 stop as usual.

| countries | source | series |
|---|---|---|
| SE, DK, FI, NL, BE, FR, DE, ES, IT | ECB Data Portal (the same host as the FX pull) | `https://data-api.ecb.europa.eu/service/data/IRS/M.{CC}.L.L40.CI.0000.{CCY}.N.Z?format=csvdata`, where CCY is EUR for euro area members, SEK for SE and DKK for DK |
| GB | Bank of England database | the monthly average yield from British Government Securities, 10 year nominal par yield, series IUMAMNPY, as CSV from the BoE IADB download endpoint |
| NO | Norges Bank data API | the 10 year government bond yield, monthly (dataset GOVT_GENERIC_RATES), as CSV |

- The ECB series are the Maastricht convergence criterion yields, the same basis the OECD series used.
- For GB and NO, record the exact URL used in `MANIFEST.json`.
- If the BoE or Norges Bank series code differs from what is written above, use the series with the same description and print its code and title in the review.
- Rename the stage to `--stage yields`, write `data/raw/yields/{CC}.csv`, and update kickoff 3.2's source in `decisions/data_sources.md`.

### 2. OPEN-27: AT1 classified as a liability

Add a field `at1_in_equity`:
- kind flag, values 1 or 0;
- `report` family;
- entered at every date in B.2 of instruction 03 for every bank, from the equity note or the AT1 note.

When `at1_in_equity` is 0:
- the coupons are already inside interest expense, so profit_owners is already net of them. at1_coupons is 0, with status `at1_liability`.
- AT1 is not in total_equity. tangible_equity therefore does not deduct at1_instruments: the term is 0, with status `at1_liability`.

Applying this deduction anyway would subtract AT1 twice.

When it is 1, nothing changes.

### 3. OPEN-28: coupons printed only net of tax

Enter the net amount as printed, with status `at1_net_of_tax`. Do not gross it up. The effect on rote is the coupon times the tax rate, a few basis points.

### 4. OPEN-29: headcount instead of FTE

Enter headcount into `fte`, with status `headcount`. income_fte and cost_fte keep the status. The README states that these banks use headcount.

### 5. OPEN-30: Santander UK

- **profit_owners:** where no attributable line is printed and the bank has no non controlling interests, enter profit after tax as printed, with status `no_nci_line`.
- **The H1 2026 levy:** if it is printed as its own line, it is resolution_dgs_contrib. If it sits inside another line, the levies rule applies (status `levies_in_admin`).

### 6. One offs to confirm

For each item listed in Open question 6 of the review, keep it only if its row in `one_offs.csv` cites the page of the bank's own alternative performance measure reconciliation table, and the description matches a line of that table. Otherwise remove it and list it. BMPS's removal stands.

### 7. Housekeeping

Accepted as they stand:
- the commit order slip (Deviation 9);
- the removed rows (Deviation 10);
- the comparative fallbacks for documents not obtained.

---

## C. Steps

### Step 3.5: apply decisions

1. Add `at1_in_equity` to `fields.yaml` and `source_map.yaml`, and enter it for every bank and date (1 commit per bank group is enough: `step 3.5: at1_in_equity EU` and `step 3.5: at1_in_equity UK`).
2. Apply decisions 3 to 6, and recompute rote on both bases.

**Test** `tests/test_kpi.py::test_at1_liability`:
- A synthetic bank with at1_in_equity 0, at1_instruments 50, total_equity 1,050 and intangibles 0 at both dates has tangible_equity 1,050 at both dates.
- With profit_owners 100, rote is 100/1,050.
- The same bank with at1_in_equity 1 has tangible_equity 1,000 and rote (100 − coupons)/1,000.

### Step 3.6: yields

Pull the yields per decision 1.

**Test** `tests/test_yields.py::test_coverage`: every country in `[sovereign] countries` has a value for every December from 2020 to 2025, and for 2026-06.

---

## D. Review evidence

1. The rote table, reported and underlying, for every bank at every date, in pct, with each blank's status.
2. The `at1_in_equity` table, bank × date.
3. Every one off removed under decision 6.
4. Yield coverage per country, with the 2025-12 value.
5. The rote and rote_reported comparison at 2025-12-31, for every bank that prints one.

---

## E. End of section

1. Run the fresh clone check.
2. Rewrite `review/section_3.md` for the whole section, with the stop under Deviations.
3. Push.
4. Write `instructions/03b_section_3_completion.status.md`, commit it, push it and stop.
