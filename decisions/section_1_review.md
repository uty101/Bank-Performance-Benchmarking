# Section 1 review decisions

Copied verbatim from `instructions/01b_section_1_completion.md` Sections A, B, B.1 and B.2 in step 1.2b.

## A. Review of the stopped session

The stop was correct, and the reviewer confirmed it from the committed files:

- **Amounts are EUR millions for every bank.** In `tr_oth.csv` of the 2025 release, total assets (2521010) at 2025-06-30 are 243,394.19 for Swedbank and 292,627.76 for DNB, which is EUR millions, not SEK or NOK.
- **Ratios are decimals.** Intesa Sanpaolo's CET1 ratio (2520140) is 0.129715.
- **Fully loaded lines are empty.** In the 2025 release, the fully phased in leverage exposure (2520904) is 0.000000 at every date for Swedbank, DNB, Intesa and Deutsche Bank. The fully loaded lines are no longer filled now that the transition has ended.
- **Clean install.** A fresh clone on Linux, Python 3.12, from the lock: ruff clean, 3 passed.
- **One reviewer error.** The 2021 release page path in instruction 01 was wrong. Using the hub link instead was right.

**Encoding.** The 2021 to 2025 CSVs are not valid UTF-8: byte 0x96 appears in labels. Read them with `encoding="latin-1"`, and state this in `load_eba`'s docstring.

---

## B. Decisions on OPEN-17 to OPEN-25

Step 1.2b (Section C) copies this section into `decisions/section_1_review.md` and marks each item decided in `decisions/OPEN.md`.

1. **OPEN-17: (a).** Add a second alias: DBK is matched as `Deutsche Bank Aktiengesellschaft`. Expected LEI: 7LTWFZYICNSX8D621K86.

2. **OPEN-18: (a).** `cet1` is the transitional line, 2520102 and its counterpart in each release. Reason: it matches tier1 and rwa, and the fully loaded lines stop being filled once the transition ends.

3. **OPEN-19: (a).** `cet1_ratio_reported` is 2520140 and its counterpart in each release. The 2025 pre floor ratio is not used.

4. **OPEN-20: (a).** `leverage_exposure` is 2520903 and its counterparts. It is transitional, and the fully phased in line is 0 in 2025.

5. **OPEN-21: (a).** `debt_securities` is NPE 2520602 with every dimension at 0. That is the gross amount, all portfolios other than held for trading. The Section 5.1 definitions become:
   - debt_securities: gross carrying amount, all accounting portfolios other than held for trading;
   - loans_all: the same basis.

   Reason: iea then excludes the trading book on both lines, which is the right base for a net interest margin.

6. **OPEN-22: (a).** Several map rows may share a field, and `load_eba` sums them.
   - **loans_customers_gross:** 2520605 at Exposure 102, 202, 301 and 401, Perf_Status 0, 4 rows.
   - **loans_customers_allowance:** 2520615 at the same 4 Exposures × Perf_Status 1 and 2, 8 rows.
   - **Sub-codes excluded.** Exposure sub-codes 311, 312, 431 and 432 sit inside 301 and 401 and must never be summed. Name them in a comment in the map builder.

7. **OPEN-23: (a).** `deposits_customers` is 2521215 at Financial_instruments 30 × Exposure 102, 202, 301 and 401, 4 rows summed.

8. **OPEN-24: (a).** `minority_interests` comes from the `report` family at every EU date. It is entered in Section 3 alongside at1_coupons and shares_out, and the source map changes accordingly.

9. **OPEN-25: (a), without downloading the mapped templates.** The unit is fixed here, with the evidence in Section A:
   - Every `eba` amount is EUR millions: `unit_scale` 1e6, `ccy` `EUR`, for every bank.
   - Every `eba` item whose field has `kind: ratio` in `fields.yaml` is a decimal stored as reported: `unit_scale` 1, `ccy` blank.
   - Convention 4.1 is amended: "`eba` rows are in EUR for every bank; `report` and `p3` rows are in the reporting currency."

### B.1 Map rules made explicit

These apply to every map file and to `load_eba`:

1. **Unnamed dimensions.** Every dimension column of the source CSV that a map row does not name in `dim_filter` must equal 0 for the row to match. In `tr_oth.csv` the dimension columns are ASSETS_FV, ASSETS_Stages, Exposure and Financial_instruments. In `tr_cre.csv` they are Portfolio, Country, Exposure, Status, Perf_Status and NACE_codes.
2. **Summed fields.** A field with several map rows is the sum of their amounts. If any listed row is absent for a bank and date, the field is missing for that bank and date. It is never a partial sum.
3. **Period length.** For P&L items, period_months = 3 × `n_quarters`. Check 5 requires 6 at 30 Jun and 12 at 31 Dec.

### B.2 Mixed currencies

From Section 2 on, some derived quantities combine an `eba` value in EUR with a `report` value in the reporting currency. Examples are tangible_equity with minority_interests, and profit_to_ordinary with at1_coupons.

**Rule.** When a derived quantity or check combines values with different `ccy`, the non EUR value is converted to EUR first, using the Convention 4.6 rates:
- balance sheet values at the reference date rate;
- P&L values at the mean over the period.

The derived row's status gains `fx_combined`.

**Signature change.** The signature becomes `derived(facts: pd.DataFrame, rates: pd.DataFrame) -> pd.DataFrame`. Apply this in Section 1 so the code is ready, even though no Section 1 row triggers it.

**Caveat for the README.** Averages and rolling figures of `eba` balances for the 5 non EUR banks carry the currency move between their 2 ends.
