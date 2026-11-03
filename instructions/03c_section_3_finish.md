# instructions/03c_section_3_finish.md: close Section 3

Apply the decisions below, finish step 3.6, then end Section 3. Precedence (rule 13): this file beats instructions 03 and 03b.

## A. Review

The stop was correct. OPEN-32 is a real error in the reviewer's 03b rule, and you caught it.

The 03b rule took "AT1 is a liability" to mean "the coupons are already inside interest expense". That holds for SEB, SHB, SWED and INGA. It does not hold for SAN, BBVA, CABK, SAB and BKT: they classify AT1 as a financial liability, but they charge the coupons to reserves and deduct them in their EPS notes. Under the 03b rule, their rote never had the coupons deducted at all.

**Yields.** BoE IUMAMNPY and Norges Bank GOVT_GENERIC_RATES are accepted as the sources.

## B. Decisions

### 1. OPEN-32: coupon location is separate from instrument location

Where the bond sits and where its coupon is charged are 2 separate questions. Each now has its own rule.

| question | depends on | rule |
|---|---|---|
| Is AT1 deducted from tangible_equity? | `at1_in_equity` only | 1: deduct at1_instruments. 0: the term is 0, status `at1_liability`. |
| What is at1_coupons? | where the coupon is charged | the coupons charged directly to equity or reserves in the period, entered positive from the statement of changes in equity or the EPS note. If the coupons are charged through interest expense in the income statement, at1_coupons is 0, status `coupon_in_pl`. |

Add a flag field `at1_coupon_in_pl`:
- 1 if the coupons are in interest expense;
- 0 if they are charged to equity or reserves;
- `report` family, entered at the same dates as `at1_in_equity`.

`at1_coupons` stays the amount, and is 0 when the flag is 1.

**Re-enter at every date.** SAN, BBVA, CABK, SAB and BKT: the coupons charged to reserves.

**Check the other flag-0 banks.** For SEB, SHB, SWED, INGA, BMPS, DANSKE from 2022-06-30, and NDA from 2025-06-30, confirm from each bank's notes that the coupons are in interest expense. Any that are not get re-entered the same way.

### 2. OPEN-33: no non controlling interests line

minority_interests is 0, with status `no_nci_line`, when both of these hold:
- the balance sheet prints no non controlling interests line;
- the statement of changes in equity shows no non controlling interests column, or one holding only zeros or dashes.

Cite the statement of changes in equity page. If either document shows any amount for non controlling interests, the field stays missing.

### 3. OPEN-31: Norway

NO uses the business day series `B.10Y.GBON` for every month. The monthly value is the arithmetic mean of that month's business day yields, with status `monthly_from_daily`. Apply it to all NO months, not only 2025-12, so the series has one definition. Record the URL in the manifest.

### 4. Weak at1_in_equity citations

The classification is read from the annual report: the accounting policy for AT1, or the balance sheet line. A half year date takes the classification from the annual report of the same year, with status `class_from_annual`, unless the half year report itself states a different one. Apply the same rule to `at1_coupon_in_pl`. Replace the weak citations listed in the review.

### 5. BAMI and BMPS against their own rote

BAMI's rote is 5.4 points from its published figure, and BMPS's is 6.0 points. No change is required, but print evidence in the review:
- each bank's published RoTE definition page;
- the numerator and denominator it uses, next to ours.

If the gap traces to an entry error, fix the entry.

## C. Steps

### Step 3.7 (commit `step 3.7: coupon location, nci and NO yields`)

Apply decisions 1 to 4 and recompute rote.

**Tests.** Update `tests/test_kpi.py::test_at1_liability` so it covers 3 cases. Each case uses a synthetic bank with profit_owners 100 and total_equity 1,050 at both dates, coupons 20, and intangibles 0.

| case | at1_in_equity | at1_coupon_in_pl | at1_instruments | tangible_equity | rote |
|---|---|---|---|---|---|
| (a) | 1 | 0 | 50 | 1,000 | 80/1,000 |
| (b) | 0 | 1 | | 1,050 | 100/1,050 |
| (c), the Spanish case | 0 | 0 | | 1,050 | 80/1,050 |

Adding a case is a reviewer change to the test, allowed here.

The yields test must pass unchanged.

## D. Review evidence

1. The `at1_coupon_in_pl` table, bank × date, with the page for each bank's annual report entry.
2. rote before and after this step for SAN, BBVA, CABK, SAB and BKT at every date.
3. Every `no_nci_line` row with its statement of changes in equity page.
4. NO yields for every month in 2025 and 2026, with the count of business days averaged.
5. The BAMI and BMPS comparison (decision 5).
6. The full rote table, reported and underlying, at every date, with each blank's status.

## E. End

Run the fresh clone check, then update `review/section_3.md`. Push, then write `instructions/03c_section_3_finish.status.md`, commit it, push it and stop.
