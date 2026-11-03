# Section 3

Outcome: **stopped under rule 4 at step 3.7** (instruction 03c). Under the coupon rule of 03c B.1, at1_coupons is the amount charged to equity or reserves, and is 0 only where at1_coupon_in_pl is 1. BMPS holds no AT1 at all, and NDA at 2026-06-30 charges no coupon to equity, so neither has a printed coupon nor a flag of 1. Their at1_coupons, and rote, are blank; a 0 there would be a design choice (OPEN-34). Every other part of step 3.7 is done: decisions 1 to 4 applied to all 31 banks, rote recomputed, the yields test passing unchanged. The earlier stops (step 3.4 FRED, step 3.6 NO 2025-12) were resolved by instructions 03b B.1 and 03c B.3.

## Steps completed

- 3.0 apply section 2 review decisions (064a109)
- 3.1 UK banks: GLEIF LEIs, 120 UK documents, entries per bank: LLOY (5086b75), NWG (d93fb73), BARC (f4b3170), HSBA (a6b93fe), SANUK (c9bcd11); UK merger ratios (50de460)
- 3.2 B.1 fields for all 31 banks, 1 commit per bank in universe order: LLOY 0924116, NWG 0591a57, BARC bf9e651, HSBA 2f7271a, SANUK 56c14d8, NDA 865d866, DNB 327d768, DANSKE 18397e6, SEB bcecc34, SHB 8028bb3, SWED 6e0b668, INGA 640d117, ABN d99d18e, KBC d575921, RABO b9d7cb6, BNP b7a803c, GLE 42b2cd5, CAG 2c1db2c, DBK 2cae2d7, CBK 6f49f3b, SAN b96f026, BBVA d24ba1f, CABK 3d2b7d2, SAB 64b3ac0, BKT a21ee33, UNI 5bceead, UCG 95188d6, ISP 6ab7a50, BAMI 618fbb6, BPE f9c667a, BMPS 016249a (see Deviation 9 on the NDA, SEB order)
- 3.3 one offs and underlying KPIs (7f4b399)
- 3.4 rote and market data; fred pull failed, rule 4 stop (d4c41c9)
- open questions OPEN-27 to OPEN-30 (b1827f3); review and status of session 3 (be68a18, f933596)
- 3.5 at1_in_equity UK (deb80cb), at1_in_equity EU (e89d51c), decisions 3 to 6 applied and rote recomputed (e7bef6e)
- 3.6 yields from ECB, BoE and Norges Bank; NO 2025-12 missing, rule 4 stop (10aa994)
- open questions OPEN-32 and OPEN-33 (9e19da4); review and status of session 3b (42145f7, 1c2358c)
- 3.7 coupon location, nci and NO yields (5dabeef)
- open questions OPEN-34 and OPEN-35 (56292fe)

## Evidence

### E3.0a Every `p3_from_report` row (A.1 item 2) in data/processed/facts.parquet

lcr and nsfr are `report` family: the source map has no p3 rule for them (Deviation 4).


```
bank_id   ref_date               field        value ccy family         status
    CBK 2025-06-30                cet1 2.560000e+10 EUR     p3 p3_from_report
    CBK 2025-06-30 cet1_ratio_reported 1.460000e-01         p3 p3_from_report
    CBK 2025-06-30   leverage_exposure 6.730000e+11 EUR     p3 p3_from_report
    CBK 2025-06-30                 rwa 1.761000e+11 EUR     p3 p3_from_report
    CBK 2025-06-30               tier1 2.910000e+10 EUR     p3 p3_from_report
    CBK 2025-12-31                cet1 2.590000e+10 EUR     p3 p3_from_report
    CBK 2025-12-31 cet1_ratio_reported 1.470000e-01         p3 p3_from_report
    CBK 2025-12-31                 lcr 1.428000e+00     report p3_from_report
    CBK 2025-12-31   leverage_exposure 6.780000e+11 EUR     p3 p3_from_report
    CBK 2025-12-31                 rwa 1.758000e+11 EUR     p3 p3_from_report
    CBK 2025-12-31               tier1 2.940000e+10 EUR     p3 p3_from_report
    CBK 2026-06-30                cet1 2.620000e+10 EUR     p3 p3_from_report
    CBK 2026-06-30 cet1_ratio_reported 1.440000e-01         p3 p3_from_report
    CBK 2026-06-30                 lcr 1.410000e+00     report p3_from_report
    CBK 2026-06-30   leverage_exposure 6.940000e+11 EUR     p3 p3_from_report
    CBK 2026-06-30                 rwa 1.824000e+11 EUR     p3 p3_from_report
    CBK 2026-06-30               tier1 2.970000e+10 EUR     p3 p3_from_report
    DNB 2026-06-30                cet1 2.071900e+11 NOK     p3 p3_from_report
    DNB 2026-06-30 cet1_ratio_reported 1.740000e-01         p3 p3_from_report
    DNB 2026-06-30                nsfr 1.160000e+00     report p3_from_report
    DNB 2026-06-30                 rwa 1.191480e+12 NOK     p3 p3_from_report
    DNB 2026-06-30               tier1 2.288100e+11 NOK     p3 p3_from_report
    SHB 2026-06-30                cet1 1.400450e+11 SEK     p3 p3_from_report
    SHB 2026-06-30 cet1_ratio_reported 1.720000e-01         p3 p3_from_report
    SHB 2026-06-30                 lcr 1.860000e+00     report p3_from_report
    SHB 2026-06-30   leverage_exposure 3.664705e+12 SEK     p3 p3_from_report
    SHB 2026-06-30                nsfr 1.220000e+00     report p3_from_report
    SHB 2026-06-30                 rwa 8.123270e+11 SEK     p3 p3_from_report
    SHB 2026-06-30               tier1 1.557400e+11 SEK     p3 p3_from_report
    UCG 2026-06-30                cet1 4.403900e+10 EUR     p3 p3_from_report
    UCG 2026-06-30 cet1_ratio_reported 1.426000e-01         p3 p3_from_report
    UCG 2026-06-30                 rwa 3.088520e+11 EUR     p3 p3_from_report
    UCG 2026-06-30               tier1 4.899700e+10 EUR     p3 p3_from_report
```

### E3.0b SHB KPIs at 2025-12-31 and 2026-06-30 (reported basis, current kpi.csv)

```
      date            kpi         value     numerator  denominator    family                              status
2025-12-31           rote           NaN           NaN          NaN       NaN           missing_input:at1_coupons
2025-12-31            roa      0.006851  2.372700e+10 3.463370e+12    report                                  ok
2025-12-31     ppp_assets      0.008786  3.042900e+10 3.463370e+12    report                                  ok
2025-12-31            nim      0.014169  4.254200e+10 3.002436e+12    report                                  ok
2025-12-31      fee_share      0.208870  1.186300e+10 5.679600e+10    report                                  ok
2025-12-31    cost_income      0.464240  2.636700e+10 5.679600e+10    report                                  ok
2025-12-31    cost_assets      0.007613  2.636700e+10 3.463370e+12    report                                  ok
2025-12-31   cost_of_risk     -0.000137 -3.130000e+08 2.284868e+12    report                                  ok
2025-12-31      npl_ratio      0.002824  6.535000e+09 2.313841e+12    report                                  ok
2025-12-31   npl_coverage      0.090436  5.910000e+08 6.535000e+09    report                                  ok
2025-12-31     cet1_ratio      0.175810  1.370840e+11 7.797290e+11        p3                                  ok
2025-12-31 leverage_ratio      0.045784  1.462330e+11 3.193942e+12        p3                                  ok
2025-12-31    rwa_density      0.230174  7.797290e+11 3.387566e+12 p3+report                                  ok
2025-12-31   loan_deposit      1.751981  2.266685e+12 1.293784e+12    report                                  ok
2025-12-31            lcr      1.907000  1.907000e+00 1.000000e+00    report                                  ok
2025-12-31           nsfr      1.191000  1.191000e+00 1.000000e+00    report                                  ok
2025-12-31     income_fte 435386.494200  5.132336e+09 1.178800e+04    report                                  ok
2025-12-31       cost_fte 202124.017400  2.382638e+09 1.178800e+04    report                                  ok
2025-12-31  cost_customer           NaN           NaN          NaN       NaN             missing_input:customers
2026-06-30           rote           NaN           NaN          NaN       NaN           missing_input:at1_coupons
2026-06-30            roa      0.006240  2.350300e+10 3.766604e+12    report                                  ok
2026-06-30     ppp_assets      0.008055  3.034000e+10 3.766604e+12    report                                  ok
2026-06-30            nim           NaN           NaN          NaN       NaN       missing_input:debt_securities
2026-06-30      fee_share      0.217338  1.230500e+10 5.661700e+10    report                                  ok
2026-06-30    cost_income      0.464119  2.627700e+10 5.661700e+10    report                                  ok
2026-06-30    cost_assets      0.006976  2.627700e+10 3.766604e+12    report                                  ok
2026-06-30   cost_of_risk           NaN           NaN          NaN       NaN missing_input:loans_customers_gross
2026-06-30      npl_ratio           NaN           NaN          NaN       NaN             missing_input:npl_gross
2026-06-30   npl_coverage           NaN           NaN          NaN       NaN         missing_input:npl_allowance
2026-06-30     cet1_ratio      0.172400  1.400450e+11 8.123270e+11        p3                      p3_from_report
2026-06-30 leverage_ratio      0.042497  1.557400e+11 3.664705e+12        p3                      p3_from_report
2026-06-30    rwa_density      0.209771  8.123270e+11 3.872440e+12 p3+report                      p3_from_report
2026-06-30   loan_deposit           NaN           NaN          NaN       NaN   missing_input:loans_customers_net
2026-06-30            lcr      1.860000  1.860000e+00 1.000000e+00    report                      p3_from_report
2026-06-30           nsfr      1.220000  1.220000e+00 1.000000e+00    report                      p3_from_report
2026-06-30     income_fte           NaN           NaN          NaN       NaN                   missing_input:fte
2026-06-30       cost_fte           NaN           NaN          NaN       NaN                   missing_input:fte
2026-06-30  cost_customer           NaN           NaN          NaN       NaN             missing_input:customers
```

### E3.0c Check 8b_scope_gate (informational: threshold and passed blank)

```
bank_id      value_a      value_b     diff_rel  threshold passed
    ABN 4.142951e+11 4.142950e+11 2.933633e-07        NaN    NaN
   BAMI 1.942171e+11 1.942170e+11 5.766742e-07        NaN    NaN
   BBVA 7.469548e+11 7.469540e+11 1.029513e-06        NaN    NaN
   BMPS 1.255844e+11 1.255844e+11 4.491005e-09        NaN    NaN
    BNP 2.573934e+12 2.573934e+12 2.992812e-08        NaN    NaN
    BPE 1.445282e+11 1.445280e+11 1.177258e-06        NaN    NaN
   CABK 5.798973e+11 5.798973e+11 0.000000e+00        NaN    NaN
    CAG 2.187749e+12 2.187749e+12 5.082943e-08        NaN    NaN
 DANSKE 4.291889e+11 4.291889e+11 6.878863e-12        NaN    NaN
    DBK 1.395880e+12 1.395880e+12 9.523034e-08        NaN    NaN
    DNB 2.926278e+11 2.925535e+11 2.537854e-04        NaN    NaN
    GLE 1.380480e+12 1.380480e+12 1.221353e-08        NaN    NaN
   INGA 1.086760e+12 1.086760e+12 0.000000e+00        NaN    NaN
    ISP 7.705184e+11 7.705190e+11 7.869442e-07        NaN    NaN
    KBC 3.565054e+11 3.565054e+11 0.000000e+00        NaN    NaN
    NDA 5.469076e+11 5.469070e+11 1.081929e-06        NaN    NaN
   RABO 6.358652e+11 6.358650e+11 3.242401e-07        NaN    NaN
    SAB 2.523766e+11 2.523766e+11 0.000000e+00        NaN    NaN
    SAN 1.797910e+12 1.797910e+12 4.449611e-08        NaN    NaN
    SEB 3.258115e+11 3.258115e+11 6.050847e-14        NaN    NaN
    SHB 3.025829e+11 3.284230e+11 8.539821e-02        NaN    NaN
   SWED 2.433942e+11 2.433942e+11 1.297460e-07        NaN    NaN
    UCG 8.168161e+11 8.168170e+11 1.084553e-06        NaN    NaN
    UNI 9.515042e+10 9.515042e+10 1.603649e-16        NaN    NaN
```

### E3.0d Seam 1 after step 3.0: 77 of 78 within 0.1%; the rows not within:

```
         check bank_id   ref_date field      value_a      value_b    diff_abs  diff_rel  threshold passed            note
7_seam_capital     CBK 2025-06-30  cet1 2.564199e+10 2.560000e+10 41989856.26  0.001638      0.001  False p3 EUR 2.56e+10
```

xlrd in requirements-lock.txt: `xlrd==2.0.2` (line 256).

### E3.1a UK banks: entries per field and date (all report_entries rows)

**LLOY** (624 entries)

```
ref_date                   2020-12-31  2021-06-30  2021-12-31  2022-06-30  2022-12-31  2023-06-30  2023-12-31  2024-06-30  2024-12-31  2025-06-30  2025-12-31  2026-06-30
field                                                                                                                                                                    
admin_expenses                      1           1           1           1           1           1           1           1           1           1           1           1
at1_instruments                     1           1           1           1           1           1           1           1           1           1           1           1
cash_cb                             1           1           1           1           1           1           1           1           1           1           1           1
cet1                                1           1           1           1           1           1           1           1           1           1           1           1
cet1_ratio_reported                 1           1           1           1           1           1           1           1           1           1           1           1
debt_securities                     2           2           2           2           2           2           2           2           2           2           2           2
deposits_customers                  1           1           1           1           1           1           1           1           1           1           1           1
gains_held_for_trading              1           1           1           1           1           1           1           1           1           1           1           1
impairments_fin                     1           1           1           1           1           1           1           1           1           1           1           1
intangibles_deduction               1           1           1           1           1           1           1           1           1           1           1           1
interest_expense                    1           1           1           1           1           1           1           1           1           1           1           1
interest_income                     1           1           1           1           1           1           1           1           1           1           1           1
lcr                                 1           1           1           1           1           1           1           1           1           1           1           1
leverage_exposure                   1           1           1           1           1           1           1           1           1           1           1           1
loans_all                           2           2           2           2           2           2           2           2           2           2           2           2
loans_customers_allowance           8           8           8           8           8           8           8           8           8           8           8           8
loans_customers_gross               8           8           8           8           8           8           8           8           8           8           8           8
loans_households_gross              2           2           2           2           2           2           2           2           2           2           2           2
net_fees                            1           1           1           1           1           1           1           1           1           1           1           1
npl_allowance                       1           1           1           1           1           1           1           1           1           1           1           1
npl_gross                           1           1           1           1           1           1           1           1           1           1           1           1
nsfr                                0           0           0           0           0           1           1           1           1           1           1           1
other_operating_net                 3           3           3           3           3           5           5           3           3           3           3           3
pat                                 1           1           1           1           1           1           1           1           1           1           1           1
pbt                                 1           1           1           1           1           1           1           1           1           1           1           1
profit_owners                       2           2           2           2           2           2           2           2           2           2           2           2
provisions                          1           0           0           0           0           0           0           0           0           0           0           0
rwa                                 1           1           1           1           1           1           1           1           1           1           1           1
tier1                               1           1           1           1           1           1           1           1           1           1           1           1
total_assets                        1           1           1           1           1           1           1           1           1           1           1           1
total_equity                        1           1           1           1           1           1           1           1           1           1           1           1
total_liabilities                   1           1           1           1           1           1           1           1           1           1           1           1
total_operating_income              1           1           1           1           1           1           1           1           1           1           1           1
```

**NWG** (664 entries)

```
ref_date                   2020-12-31  2021-06-30  2021-12-31  2022-06-30  2022-12-31  2023-06-30  2023-12-31  2024-06-30  2024-12-31  2025-06-30  2025-12-31  2026-06-30
field                                                                                                                                                                    
admin_expenses                      3           3           3           3           3           3           3           3           3           3           3           3
at1_instruments                     1           1           1           1           1           1           1           1           1           1           1           1
cash_cb                             1           1           1           1           1           1           1           1           1           1           1           1
cet1                                1           1           1           1           1           1           1           1           1           1           1           1
cet1_ratio_reported                 1           1           1           1           1           1           1           1           1           1           1           1
debt_securities                     2           2           2           2           2           2           2           2           2           2           2           2
deposits_customers                  1           1           1           1           1           1           1           1           1           1           1           1
depreciation                        2           1           1           1           1           1           1           1           1           1           1           1
gains_held_for_trading              1           1           1           1           1           1           1           1           1           1           1           1
impairments_fin                     1           1           1           1           1           1           1           1           1           1           1           1
intangibles_deduction               1           1           1           1           1           1           1           1           1           1           1           1
interest_expense                    1           1           1           1           1           1           1           1           1           1           1           1
interest_income                     1           1           1           1           1           1           1           1           1           1           1           1
lcr                                 1           1           1           1           1           1           1           1           1           1           1           1
leverage_exposure                   1           1           1           1           1           1           1           1           1           1           1           1
loans_all                           2           2           2           2           2           2           2           2           2           2           2           2
loans_customers_allowance           8           8           8           8           8           8           8           8           8           8           8           8
loans_customers_gross               8           8           8           8           8           8           8           8           8           8           8           8
loans_households_gross              2           2           2           2           2           2           2           2           2           2           2           2
net_fees                            2           2           2           2           2           2           2           2           2           2           2           2
npl_allowance                       1           1           1           1           1           1           1           1           1           1           1           1
npl_gross                           1           1           1           1           1           1           1           1           1           1           1           1
nsfr                                1           1           1           1           1           1           1           1           1           1           1           1
other_operating_net                 1           1           1           1           1           1           1           1           1           1           1           1
pat                                 1           1           1           1           1           1           1           1           1           1           1           1
pbt                                 1           1           1           1           1           1           1           1           1           1           1           1
profit_owners                       3           3           3           2           2           2           2           2           2           2           2           2
rwa                                 1           1           1           1           1           1           1           1           1           1           1           1
tier1                               1           1           1           1           1           1           1           1           1           1           1           1
total_assets                        1           1           1           1           1           1           1           1           1           1           1           1
total_equity                        1           1           1           1           1           1           1           1           1           1           1           1
total_liabilities                   1           1           1           1           1           1           1           1           1           1           1           1
total_operating_income              1           1           1           1           1           1           1           1           1           1           1           1
trading_assets                      1           1           1           1           1           1           1           1           1           1           1           1
```

**BARC** (647 entries)

```
ref_date                   2020-12-31  2021-06-30  2021-12-31  2022-06-30  2022-12-31  2023-06-30  2023-12-31  2024-06-30  2024-12-31  2025-06-30  2025-12-31  2026-06-30
field                                                                                                                                                                    
admin_expenses                      3           2           3           2           3           2           3           2           3           2           3           2
at1_instruments                     1           1           1           1           1           1           1           1           1           1           1           1
cash_cb                             1           1           1           1           1           1           1           1           1           1           1           1
cet1                                1           1           1           1           1           1           1           1           1           1           1           1
cet1_ratio_reported                 1           1           1           1           1           1           1           1           1           1           1           1
debt_securities                     2           2           2           2           2           2           2           2           2           2           2           2
deposits_customers                  1           1           1           1           1           1           1           1           1           1           1           1
gains_held_for_trading              1           1           1           1           1           1           1           1           1           1           1           1
impairments_fin                     1           1           1           1           1           1           1           1           1           1           1           1
intangibles_deduction               2           2           2           1           1           1           1           1           1           1           1           1
interest_expense                    1           1           1           1           1           1           1           1           1           1           1           1
interest_income                     1           1           1           1           1           1           1           1           1           1           1           1
lcr                                 1           1           1           1           1           1           1           1           1           1           1           1
leverage_exposure                   1           1           1           1           1           1           1           1           1           1           1           1
loans_all                           2           2           2           2           2           2           2           2           2           2           2           2
loans_customers_allowance           8           8           8           8           8           8           8           8           8           8           8           8
loans_customers_gross               8           8           8           8           8           8           8           8           8           8           8           8
loans_households_gross              2           2           2           2           2           2           2           2           2           2           2           2
net_fees                            1           1           1           1           1           1           1           1           1           1           1           1
npl_allowance                       1           1           1           1           1           1           1           1           1           1           1           1
npl_gross                           1           1           1           1           1           1           1           1           1           1           1           1
nsfr                                0           0           0           0           1           1           1           1           1           1           1           1
other_operating_net                 2           2           2           2           2           2           2           2           3           2           2           2
pat                                 1           1           1           1           1           1           1           1           1           1           1           1
pbt                                 1           1           1           1           1           1           1           1           1           1           1           1
profit_owners                       1           1           1           1           1           1           1           1           1           1           1           1
provisions                          1           1           1           1           1           1           1           1           1           1           1           1
resolution_dgs_contrib              0           0           0           0           0           0           0           1           1           1           1           1
rwa                                 1           1           1           1           1           1           1           1           1           1           1           1
tier1                               1           1           1           1           1           1           1           1           1           1           1           1
total_assets                        1           1           1           1           1           1           1           1           1           1           1           1
total_equity                        1           1           1           1           1           1           1           1           1           1           1           1
total_liabilities                   1           1           1           1           1           1           1           1           1           1           1           1
total_operating_income              1           1           1           1           1           1           1           1           1           1           1           1
trading_assets                      1           1           1           1           1           1           1           1           1           1           1           1
```

**HSBA** (714 entries)

```
ref_date                       2020-12-31  2021-06-30  2021-12-31  2022-06-30  2022-12-31  2023-06-30  2023-12-31  2024-06-30  2024-12-31  2025-06-30  2025-12-31  2026-06-30
field                                                                                                                                                                        
admin_expenses                          2           2           2           2           2           2           2           2           2           2           2           2
at1_instruments                         1           1           1           1           1           1           1           1           1           1           1           1
cash_cb                                 1           1           1           1           1           1           1           1           1           1           1           1
cet1                                    1           1           1           1           1           1           1           1           1           1           1           1
cet1_ratio_reported                     1           1           1           1           1           1           1           1           1           1           1           1
debt_securities                         2           2           2           2           2           2           2           2           2           2           2           2
deposits_customers                      1           1           1           1           1           1           1           1           1           1           1           1
depreciation                            2           2           2           2           2           2           2           2           2           2           2           2
gains_derecognition_not_fvtpl           1           1           1           1           1           0           0           0           0           0           0           0
gains_designated_fvtpl                  2           2           2           2           2           0           0           0           0           0           0           0
gains_held_for_trading                  1           1           1           1           1           1           1           1           1           1           1           1
impairments_fin                         1           1           1           1           1           1           1           1           1           1           1           1
impairments_nonfin                      1           0           1           0           0           0           1           0           0           1           1           0
intangibles_deduction                   1           1           1           1           1           1           1           1           1           1           1           1
interest_expense                        1           1           1           1           1           1           1           1           1           1           1           1
interest_income                         1           1           1           1           1           1           1           1           1           1           1           1
lcr                                     1           1           1           1           1           1           1           1           1           1           1           1
leverage_exposure                       1           1           1           1           1           1           1           1           1           1           1           1
loans_all                               2           2           2           2           2           2           2           2           2           2           2           2
loans_customers_allowance               8           8           8           8           8           8           8           8           8           8           8           8
loans_customers_gross                   8           8           8           8           8           8           8           8           8           8           8           8
loans_households_gross                  2           2           2           2           2           2           2           2           2           2           2           2
net_fees                                1           1           1           1           1           1           1           1           1           1           1           1
npl_allowance                           1           1           1           1           1           1           1           1           1           1           1           1
npl_gross                               1           1           1           1           1           1           1           1           1           1           1           1
nsfr                                    0           0           0           1           1           1           1           1           1           1           1           1
other_operating_net                     4           4           4           4           5           6           6           5           5           5           5           5
pat                                     1           1           1           1           1           1           1           1           1           1           1           1
pbt                                     1           1           1           1           1           1           1           1           1           1           1           1
profit_owners                           3           3           3           2           2           2           2           2           2           2           2           2
rwa                                     1           1           1           1           1           1           1           1           1           1           1           1
tier1                                   1           1           1           1           1           1           1           1           1           1           1           1
total_assets                            1           1           1           1           1           1           1           1           1           1           1           1
total_equity                            1           1           1           1           1           1           1           1           1           1           1           1
total_liabilities                       1           1           1           1           1           1           1           1           1           1           1           1
total_operating_income                  1           1           1           1           1           1           1           1           1           1           1           1
trading_assets                          1           1           1           1           1           1           1           1           1           1           1           1
```

**SANUK** (563 entries)

```
ref_date                   2020-12-31  2021-06-30  2021-12-31  2022-06-30  2022-12-31  2023-06-30  2023-12-31  2024-06-30  2024-12-31  2025-06-30  2025-12-31  2026-06-30
field                                                                                                                                                                    
admin_expenses                      1           1           1           1           1           1           1           1           1           1           1           1
at1_instruments                     1           1           1           1           1           1           1           1           1           1           1           1
cash_cb                             1           1           1           1           1           1           1           1           1           1           1           1
cet1                                1           1           1           1           1           1           1           1           1           1           1           1
cet1_ratio_reported                 1           1           1           1           1           1           1           1           1           1           1           1
debt_securities                     0           2           2           2           2           2           2           2           2           2           2           2
deposits_customers                  1           1           1           1           1           1           1           1           1           1           1           1
impairments_fin                     1           1           1           1           1           1           1           1           1           1           1           1
intangibles_deduction               1           1           1           1           1           1           1           1           1           1           1           1
interest_expense                    1           1           1           1           1           1           1           1           1           1           1           1
interest_income                     1           1           1           1           1           1           1           1           1           1           1           1
lcr                                 1           1           1           1           1           1           1           1           1           1           1           1
leverage_exposure                   1           1           1           1           1           1           1           1           1           1           1           1
loans_all                           0           2           2           2           2           2           2           2           2           2           2           2
loans_customers_allowance           0           8           8           8           8           8           8           8           8           8           8           8
loans_customers_gross               0           8           8           8           8           8           8           8           8           8           8           8
loans_households_gross              0           2           2           2           2           2           2           2           2           2           2           2
net_fees                            1           1           1           1           1           1           1           1           1           1           1           1
npl_allowance                       0           1           1           1           1           1           1           1           1           1           1           1
npl_gross                           0           1           1           1           1           1           1           1           1           1           1           1
nsfr                                0           0           0           1           1           1           1           1           1           1           1           1
other_operating_net                 1           1           1           1           1           1           1           1           1           1           1           1
pat                                 1           1           1           1           1           1           1           1           1           1           1           1
pbt                                 1           1           1           1           1           1           1           1           1           1           1           1
profit_owners                       1           1           1           1           1           1           1           1           1           1           0           0
provisions                          1           1           1           1           1           1           1           1           1           1           1           1
resolution_dgs_contrib              0           0           0           0           0           0           0           0           0           0           0           1
rwa                                 1           1           1           1           1           1           1           1           1           1           1           1
tier1                               1           1           1           1           1           1           1           1           1           1           1           1
total_assets                        1           1           1           1           1           1           1           1           1           1           1           1
total_equity                        1           1           1           1           1           1           1           1           1           1           1           1
total_liabilities                   1           1           1           1           1           1           1           1           1           1           1           1
total_operating_income              1           1           1           1           1           1           1           1           1           1           1           4
```

### E3.1b Provenance by bank (check 1, all report_entries rows)

```
         rows passed
bank_id             
ABN       267    267
BAMI      285    285
BARC      691    691
BBVA      313    313
BKT       171    171
BMPS      251    251
BNP       269    269
BPE       251    251
CABK      300    300
CAG       233    233
CBK       193    193
DANSKE    229    229
DBK       289    289
DNB       233    233
GLE       250    250
HSBA      764    764
INGA      225    225
ISP       243    243
KBC       268    268
LLOY      668    668
NDA       265    265
NWG       715    715
RABO      276    276
SAB       279    279
SAN       309    309
SANUK     598    598
SEB       227    227
SHB       215    215
SWED      261    261
UCG       242    242
UNI       294    294
```


### E3.1c UK LEIs from GLEIF (data/raw/gleif/{bank_id}.json)

```
bank_id               universe_name                gleif_legal_name                  lei entity_status registration  search_results
   LLOY        Lloyds Banking Group        LLOYDS BANKING GROUP PLC 549300PPXHEU2JF0AM85        ACTIVE       ISSUED               3
    NWG               NatWest Group               NATWEST GROUP PLC 2138005O9XJIJN4JPN90        ACTIVE       ISSUED               5
   BARC                    Barclays                    BARCLAYS PLC 213800LBQA1Y9L22JB70        ACTIVE       ISSUED              70
   HSBA               HSBC Holdings               HSBC HOLDINGS PLC MLU0ZO3ML4LN2LL2TL39        ACTIVE       ISSUED              13
  SANUK Santander UK Group Holdings SANTANDER UK GROUP HOLDINGS PLC 549300F5XIFGNNW4CF72        ACTIVE       ISSUED               1
```

### E3.1d UK banks: fields missing, with reason

| bank | field | dates | reason |
|---|---|---|---|
| all 5 | dividend_income, gains_* lines not printed | all | no such line on the income statement (each printed line is entered) |
| LLOY, BARC, SANUK | depreciation | all | no depreciation line; admin_expenses as printed (`dep_in_admin`) |
| LLOY, NWG, HSBA, SANUK | resolution_dgs_contrib | all (SANUK to 2025-12-31) | levy not a separate line (`levies_in_admin`) |
| BARC | resolution_dgs_contrib | 2020-12-31 to 2023-12-31 | levy a separate line only from H1 2024 |
| LLOY | provisions | from 2021-06-30 | regulatory provisions inside operating expenses |
| LLOY, SANUK | trading_assets | all | no held-for-trading line |
| SANUK | profit_owners | 2025-12-31, 2026-06-30 | no attributable line printed (OPEN-30) |
| all 5 | nsfr | to 2021-12-31 (BARC to 2022-06-30, LLOY to 2022-12-31) | KM1 has no NSFR row |
| SANUK | CR1 fields | 2020-12-31 | page has row labels but no numbers in its text layer |
| HSBA | impairments_nonfin | 7 dates | printed as a dash |


### E3.1e UK merger rows (scripts/merger_materiality.py)

```
acquirer_id                                                          target_name completion_date  target_total_assets target_ccy   ref_date  acquirer_total_assets_eur  target_total_assets_eur    ratio break                                note
       HSBA                                       Silicon Valley Bank UK Limited      2023-03-13          11490000000        USD 2022-12-31               2.781296e+12             1.077255e+10 0.003873 False                                    
       BARC                                   Tesco Bank retail banking business      2024-11-01           8400000000        GBP 2024-06-30               1.862797e+12             9.924620e+09 0.005328 False                                    
        NWG                             Sainsbury's Bank retail banking business      2025-05-01           2500000000        GBP 2024-12-31               8.538375e+11             3.015027e+09 0.003531 False                                    
      SANUK                                                TSB Banking Group plc      2026-04-30          45286000000        GBP 2025-12-31               3.139445e+11             5.189778e+10 0.165309  True
```

### E3.2 B.1 values per bank, date x field (own units: amounts in reporting currency units, counts as counts, rote_reported decimal)

**LLOY**

```
field       at1_coupons    fte  minority_interests  rote_reported  shares_out
ref_date                                                                     
2020-12-31     4.53e+08 61,576            2.29e+08            NaN  7.0812e+10
2021-06-30     2.13e+08    NaN            2.19e+08            NaN  7.0956e+10
2021-12-31     4.29e+08 57,955            2.35e+08            NaN  7.0996e+10
2022-06-30     2.14e+08    NaN            2.19e+08            NaN  6.8702e+10
2022-12-31     4.38e+08 59,354            2.44e+08            NaN  6.6944e+10
2023-06-30     2.55e+08    NaN            2.51e+08            NaN  6.4571e+10
2023-12-31     5.27e+08 62,569            2.01e+08            NaN  6.3508e+10
2024-06-30     2.69e+08    NaN            2.26e+08            NaN  6.2458e+10
2024-12-31     4.98e+08 61,228            1.72e+08            NaN  6.0491e+10
2025-06-30     2.45e+08    NaN            1.54e+08            NaN  5.9938e+10
2025-12-31     4.63e+08 60,061            1.99e+08          0.129  5.8799e+10
2026-06-30     2.29e+08    NaN            2.25e+08          0.171  5.8081e+10
```

**NWG**

```
field       at1_coupons    fte  minority_interests  rote_reported  shares_out
ref_date                                                                     
2020-12-31     3.55e+08 59,915            -3.6e+07            NaN 1.21132e+10
2021-06-30     1.78e+08 59,200               1e+07            NaN  1.1569e+10
2021-12-31     2.99e+08 58,735               7e+06            NaN  1.1272e+10
2022-06-30     1.21e+08 58,900               1e+07            NaN  1.0436e+10
2022-12-31     2.49e+08 61,857               8e+06            NaN   9.659e+09
2023-06-30     1.21e+08 61,500               4e+07            NaN   8.929e+09
2023-12-31     2.42e+08 61,253             3.1e+07            NaN   8.792e+09
2024-06-30     1.29e+08 60,600             4.2e+07            NaN   8.307e+09
2024-12-31     2.83e+08 59,223             2.8e+07            NaN   8.043e+09
2025-06-30     1.86e+08 59,200             1.8e+07            NaN   8.088e+09
2025-12-31     3.52e+08 58,720             1.4e+07          0.192   7.995e+09
2026-06-30     1.49e+08 60,500               1e+07          0.197   7.959e+09
```

**BARC**

```
field       at1_coupons    fte  minority_interests  rote_reported  shares_out
ref_date                                                                     
2020-12-31     8.57e+08 83,000           1.085e+09            NaN  1.7359e+10
2021-06-30     3.89e+08    NaN           1.064e+09            NaN  1.6998e+10
2021-12-31     8.04e+08 81,600            9.89e+08            NaN  1.6752e+10
2022-06-30     4.14e+08    NaN            9.69e+08            NaN  1.6531e+10
2022-12-31     9.05e+08 87,400            9.68e+08            NaN  1.5871e+10
2023-06-30     5.07e+08    NaN            8.76e+08            NaN  1.5556e+10
2023-12-31     9.85e+08 92,400             6.6e+08            NaN  1.5155e+10
2024-06-30      5.1e+08    NaN             6.6e+08            NaN  1.4826e+10
2024-12-31     9.91e+08 93,000             6.6e+08            NaN   1.442e+10
2025-06-30     4.84e+08    NaN            4.49e+08            NaN   1.418e+10
2025-12-31     9.97e+08 93,000            4.52e+08          0.113  1.3867e+10
2026-06-30     4.87e+08    NaN            4.53e+08          0.148  1.3507e+10
```

**HSBA**

```
field       at1_coupons     fte  minority_interests  rote_reported  shares_out
ref_date                                                                      
2020-12-31    1.241e+09 226,059           8.552e+09            NaN  2.0184e+10
2021-06-30     6.66e+08 222,550           8.546e+09            NaN  2.0223e+10
2021-12-31    1.303e+09 219,697           8.527e+09            NaN  2.0073e+10
2022-06-30     6.26e+08 218,866           8.308e+09            NaN  1.9819e+10
2022-12-31    1.214e+09 219,199           8.544e+09            NaN  1.9739e+10
2023-06-30     5.42e+08 221,764           7.481e+09            NaN  1.9534e+10
2023-12-31    1.101e+09 220,861           7.281e+09            NaN  1.9006e+10
2024-06-30     5.26e+08 213,978           7.121e+09            NaN   1.833e+10
2024-12-31    1.062e+09 211,304             7.3e+09            NaN  1.7918e+10
2025-06-30     5.47e+08 211,130           7.315e+09            NaN  1.7397e+10
2025-12-31    1.183e+09 208,720           7.441e+09          0.133   1.714e+10
2026-06-30     6.33e+08 206,161            3.99e+08          0.182  1.7164e+10
```

**SANUK**

```
field       at1_coupons  customers    fte  minority_interests  rote_reported  shares_out
ref_date                                                                                
2020-12-31     1.47e+08    1.4e+07 22,000            3.97e+08            NaN    7.06e+09
2021-06-30      7.3e+07        NaN    NaN            4.15e+08            NaN         NaN
2021-12-31     1.43e+08    1.4e+07 18,000            2.35e+08            NaN    7.06e+09
2022-06-30      7.6e+07        NaN    NaN                 NaN            NaN         NaN
2022-12-31     1.43e+08    1.4e+07 19,000                 NaN            NaN    7.06e+09
2023-06-30      6.7e+07        NaN    NaN                 NaN            NaN         NaN
2023-12-31     1.33e+08    1.4e+07 19,800                 NaN            NaN    7.06e+09
2024-06-30      7.2e+07        NaN    NaN                 NaN            NaN         NaN
2024-12-31     1.39e+08    1.4e+07 18,000                 NaN            NaN    7.06e+09
2025-06-30      7.2e+07        NaN    NaN                 NaN            NaN         NaN
2025-12-31     1.42e+08   1.36e+07 15,400                 NaN            0.1    7.06e+09
2026-06-30      8.1e+07        NaN    NaN                 NaN          0.091         NaN
```

**NDA**

```
field       at1_coupons    fte  minority_interests  rote_reported  shares_out
ref_date                                                                     
2020-12-31      2.7e+07 28,051               9e+06            NaN         NaN
2021-06-30      2.6e+07 27,510               9e+06            NaN  4.0394e+09
2021-12-31      2.6e+07 26,894               9e+06            NaN  3.9332e+09
2022-06-30      2.6e+07 27,350                 NaN            NaN  3.7469e+09
2022-12-31      2.6e+07 28,268                 NaN            NaN  3.6406e+09
2023-06-30      2.6e+07 29,317                 NaN            NaN   3.575e+09
2023-12-31      2.6e+07 29,153                 NaN            NaN  3.5189e+09
2024-06-30      2.6e+07 29,680                 NaN            NaN  3.4994e+09
2024-12-31      2.6e+07 30,157                 NaN            NaN  3.4883e+09
2025-06-30      2.6e+07 29,844                 NaN            NaN  3.4586e+09
2025-12-31      2.6e+07 28,989                 NaN            NaN    3.42e+09
2026-06-30          NaN 28,412                 NaN          0.169  3.3919e+09
```

**DNB**

```
field       at1_coupons    fte  minority_interests  shares_out
ref_date                                                      
2020-12-31    1.578e+09  9,050            1.19e+08 1.55037e+09
2021-06-30     5.13e+08    NaN             2.7e+08         NaN
2021-12-31     9.26e+08  9,410            2.66e+08 1.55037e+09
2022-06-30        5e+08    NaN            3.99e+08         NaN
2022-12-31    1.056e+09 10,351            2.27e+08 1.55037e+09
2023-06-30     2.76e+08    NaN            2.32e+08         NaN
2023-12-31    1.225e+09 10,617            1.68e+08 1.51684e+09
2024-06-30     4.81e+08    NaN            1.57e+08 1.49103e+09
2024-12-31    1.866e+09 10,603            2.18e+08 1.48268e+09
2025-06-30     3.79e+08    NaN            6.71e+08 1.47593e+09
2025-12-31    1.589e+09 10,829            7.05e+08 1.46097e+09
2026-06-30     3.91e+08    NaN            5.32e+08         NaN
```

**DANSKE**

```
field       at1_coupons    fte  shares_out
ref_date                                  
2020-12-31     6.25e+08 22,376 8.53649e+08
2021-06-30     2.33e+08 21,926 8.53064e+08
2021-12-31     4.66e+08 21,754 8.53352e+08
2022-06-30     1.64e+08 21,663 8.51334e+08
2022-12-31     1.64e+08 21,022 8.50947e+08
2023-06-30          NaN 21,339 8.58778e+08
2023-12-31          NaN 20,021 8.59774e+08
2024-06-30          NaN 20,079 8.48792e+08
2024-12-31          NaN 19,916 8.33817e+08
2025-06-30          NaN 20,204         NaN
2025-12-31          NaN 20,026 8.14998e+08
2026-06-30          NaN 19,472 8.08199e+08
```

**SEB**

```
field         fte  shares_out
ref_date                     
2020-12-31    NaN 2.16196e+09
2021-06-30 15,548 2.16613e+09
2021-12-31    NaN  2.1564e+09
2022-06-30 16,277 2.13791e+09
2022-12-31    NaN 2.11344e+09
2023-06-30 17,428 2.09403e+09
2023-12-31    NaN 2.07285e+09
2024-06-30 17,810 2.05084e+09
2024-12-31    NaN 2.02043e+09
2025-06-30 19,102 1.98941e+09
2025-12-31    NaN 1.96158e+09
2026-06-30 18,491 1.94953e+09
```

**SHB**

```
field         fte  minority_interests  shares_out
ref_date                                         
2020-12-31 12,474               9e+06    1.98e+09
2021-06-30    NaN             1.1e+07 1.98003e+09
2021-12-31 10,793             2.5e+07    1.98e+09
2022-06-30    NaN             1.2e+07 1.98003e+09
2022-12-31    NaN               3e+06    1.98e+09
2023-06-30    NaN               2e+06 1.98003e+09
2023-12-31    NaN               8e+06    1.98e+09
2024-06-30 12,229               2e+06 1.98003e+09
2024-12-31 11,976               6e+06    1.98e+09
2025-06-30 11,608               2e+06 1.98003e+09
2025-12-31 11,600               3e+06    1.98e+09
2026-06-30    NaN               2e+06         NaN
```

**SWED**

```
field       customers    fte  minority_interests  shares_out
ref_date                                                    
2020-12-31  7.616e+06 16,213             2.5e+07 1.11999e+09
2021-06-30        NaN 16,356             2.5e+07 1.12143e+09
2021-12-31   7.62e+06 16,565             2.6e+07 1.12143e+09
2022-06-30        NaN 16,688             2.6e+07 1.12307e+09
2022-12-31   7.62e+06 16,803             2.9e+07 1.12307e+09
2023-06-30        NaN 16,865             2.8e+07  1.1248e+09
2023-12-31  7.618e+06 17,275               3e+07  1.1248e+09
2024-06-30        NaN 17,538                 NaN 1.12532e+09
2024-12-31  7.612e+06 17,209             2.8e+07 1.12532e+09
2025-06-30        NaN 16,792                 NaN 1.12423e+09
2025-12-31  7.602e+06 17,300             2.5e+07 1.12423e+09
2026-06-30        NaN 17,293                 NaN 1.12371e+09
```

**INGA**

```
field       minority_interests  rote_reported  shares_out
ref_date                                                 
2020-12-31           1.022e+09            NaN  3.9001e+09
2021-06-30            9.87e+08            NaN         NaN
2021-12-31            7.36e+08            NaN  3.7758e+09
2022-06-30            4.13e+08            NaN         NaN
2022-12-31            5.04e+08            NaN  3.6191e+09
2023-06-30            7.21e+08            NaN         NaN
2023-12-31            9.44e+08            NaN  3.3436e+09
2024-06-30            8.16e+08            NaN         NaN
2024-12-31            9.95e+08            NaN  3.0963e+09
2025-06-30           1.031e+09            NaN         NaN
2025-12-31           1.255e+09          0.136   2.902e+09
2026-06-30           1.141e+09          0.153         NaN
```

**ABN**

```
field       at1_coupons    fte  minority_interests  shares_out
ref_date                                                      
2020-12-31     1.17e+08 19,234                 NaN     9.4e+08
2021-06-30      4.6e+07 19,639               5e+06     9.4e+08
2021-12-31      9.1e+07 19,957               5e+06     9.4e+08
2022-06-30      4.6e+07 20,079               5e+06 8.97522e+08
2022-12-31      9.1e+07 20,038               2e+06    8.98e+08
2023-06-30      4.6e+07 20,153               3e+06 8.65575e+08
2023-12-31      9.1e+07 20,872               3e+06    8.66e+08
2024-06-30      4.6e+07 21,047               3e+06 8.33049e+08
2024-12-31      1.2e+08 21,976               3e+06    8.33e+08
2025-06-30      9.7e+07 22,278               3e+06 8.33049e+08
2025-12-31     2.17e+08 23,126               3e+06    8.23e+08
2026-06-30      9.5e+07 22,905               3e+06 8.14936e+08
```

**KBC**

```
field       at1_coupons  customers    fte  minority_interests  rote_reported  shares_out
ref_date                                                                                
2020-12-31        5e+07    1.2e+07 37,696                   0            NaN 4.16674e+08
2021-06-30      2.5e+07        NaN    NaN                 NaN            NaN    4.17e+08
2021-12-31        5e+07    1.2e+07 37,207                   0            NaN 4.16884e+08
2022-06-30      2.5e+07        NaN    NaN                   0            NaN    4.17e+08
2022-12-31        5e+07    1.3e+07 39,288                   0            NaN 4.17169e+08
2023-06-30      2.5e+07        NaN    NaN               1e+06            NaN 4.17165e+08
2023-12-31        5e+07    1.3e+07 38,678                   0            NaN 4.08505e+08
2024-06-30      4.7e+07        NaN    NaN               1e+06            NaN 3.98394e+08
2024-12-31      8.4e+07    1.3e+07    NaN                   0            NaN 3.96563e+08
2025-06-30      4.6e+07        NaN    NaN             2.7e+07            NaN 3.96563e+08
2025-12-31          NaN    1.3e+07    NaN             8.1e+07           0.16 3.96682e+08
2026-06-30          NaN        NaN    NaN            1.28e+08           0.18 3.96682e+08
```

**RABO**

```
field       at1_coupons  customers    fte  minority_interests
ref_date                                                     
2020-12-31     2.34e+08    8.9e+06 43,272            4.76e+08
2021-06-30      9.9e+07        NaN 43,263            5.39e+08
2021-12-31     1.78e+08    8.9e+06 43,361            5.02e+08
2022-06-30      8.8e+07        NaN 45,415            5.69e+08
2022-12-31      1.9e+08    9.1e+06 46,959            5.33e+08
2023-06-30     1.01e+08        NaN 48,946            5.94e+08
2023-12-31     2.03e+08    9.1e+06 49,132            5.99e+08
2024-06-30          NaN        NaN 49,878            6.23e+08
2024-12-31     2.03e+08    9.2e+06 49,272            6.21e+08
2025-06-30     1.01e+08        NaN 48,850            6.16e+08
2025-12-31     1.95e+08    9.1e+06 48,202            6.39e+08
2026-06-30      6.8e+07    9.1e+06 48,069            5.48e+08
```

**BNP**

```
field       at1_coupons     fte  minority_interests  rote_reported  shares_out
ref_date                                                                      
2020-12-31     4.26e+08 193,319            4.55e+09            NaN  1.2481e+09
2021-06-30     2.13e+08     NaN           4.472e+09            NaN 1.24908e+09
2021-12-31     4.12e+08 189,765           4.621e+09            NaN 1.23361e+09
2022-06-30     1.88e+08     NaN           4.584e+09            NaN 1.23232e+09
2022-12-31     3.74e+08 193,122           4.763e+09            NaN 1.23345e+09
2023-06-30     3.29e+08     NaN           5.003e+09            NaN 1.19676e+09
2023-12-31     6.54e+08 182,656           5.125e+09            NaN 1.14653e+09
2024-06-30      3.7e+08     NaN           5.585e+09            NaN  1.1299e+09
2024-12-31     7.43e+08 177,952           6.004e+09            NaN 1.12955e+09
2025-06-30     4.12e+08     NaN           5.954e+09            NaN 1.11784e+09
2025-12-31     8.22e+08 180,994            6.66e+09          0.116  1.1001e+09
2026-06-30     4.36e+08     NaN           6.524e+09          0.133 1.09564e+09
```

**GLE**

```
field       at1_coupons  customers     fte  minority_interests  rote_reported  shares_out
ref_date                                                                                 
2024-06-30     3.53e+08        NaN     NaN                 NaN            NaN         NaN
2024-12-31     7.13e+08        NaN     NaN           9.332e+09            NaN 7.96498e+08
2025-06-30     3.87e+08        NaN     NaN           9.168e+09            NaN 7.76296e+08
2025-12-31     7.19e+08    2.7e+07 102,351           9.383e+09          0.102 7.54887e+08
2026-06-30     3.74e+08        NaN     NaN           8.904e+09           0.12 7.30035e+08
```

**CAG**

```
field       at1_coupons  customers     fte  minority_interests
ref_date                                                      
2020-12-31          NaN    5.2e+07     NaN                 NaN
2021-12-31          NaN    5.3e+07     NaN                 NaN
2022-12-31          NaN    5.3e+07     NaN                 NaN
2023-12-31          NaN    5.4e+07     NaN                 NaN
2024-12-31     4.73e+08    5.4e+07 157,714           6.875e+09
2025-06-30      2.6e+08        NaN     NaN           7.278e+09
2025-12-31     5.54e+08        NaN 160,200           6.451e+09
2026-06-30     2.69e+08        NaN     NaN           6.983e+09
```

**DBK**

```
field       at1_coupons    fte  minority_interests  rote_reported  shares_out
ref_date                                                                     
2020-12-31     3.49e+08 84,659           1.587e+09            NaN 2.06543e+09
2021-06-30     3.63e+08 83,797           1.591e+09            NaN  2.0638e+09
2021-12-31     3.63e+08 82,969           1.698e+09            NaN 2.06609e+09
2022-06-30     4.79e+08 82,915           1.769e+09            NaN   2.033e+09
2022-12-31     4.79e+08 84,930           1.791e+09            NaN 2.03784e+09
2023-06-30     4.98e+08 87,055           1.723e+09            NaN  2.0356e+09
2023-12-31     4.98e+08 90,130           1.763e+09            NaN 1.99205e+09
2024-06-30     5.74e+08 89,470           1.583e+09            NaN  1.9477e+09
2024-12-31     5.74e+08 89,753           1.606e+09            NaN 1.94513e+09
2025-06-30     7.28e+08 89,426           1.457e+09            NaN  1.9262e+09
2025-12-31     7.61e+08 89,879           1.562e+09          0.103 1.90287e+09
2026-06-30     7.96e+08 89,742           1.575e+09          0.119  1.8791e+09
```

**CBK**

```
field       at1_coupons    fte  minority_interests  rote_reported  shares_out
ref_date                                                                     
2020-12-31      4.8e+07    NaN           1.119e+09            NaN  1.2524e+09
2021-06-30      1.4e+08 38,671           1.129e+09            NaN  1.2524e+09
2021-12-31      1.4e+08 40,181            9.75e+08            NaN  1.2524e+09
2022-06-30      1.9e+08 38,465             9.4e+08            NaN  1.2524e+09
2022-12-31      1.9e+08 37,852            8.88e+08            NaN  1.2524e+09
2023-06-30     1.94e+08 37,487            9.74e+08            NaN  1.2402e+09
2023-12-31     1.94e+08 38,565           1.016e+09            NaN  1.2402e+09
2024-06-30     1.95e+08 38,708           1.123e+09            NaN  1.1847e+09
2024-12-31     2.12e+08 39,040           1.249e+09            NaN  1.1536e+09
2025-06-30     2.59e+08    NaN           1.394e+09            NaN  1.1275e+09
2025-12-31     3.21e+08 39,867           1.535e+09          0.087  1.0965e+09
2026-06-30     2.22e+08 40,110           1.668e+09          0.126  1.0808e+09
```

**SAN**

```
field       at1_coupons   customers  minority_interests  rote_reported  shares_out
ref_date                                                                          
2020-12-31     5.52e+08 1.48256e+08           9.846e+09            NaN  1.7312e+10
2021-06-30          NaN 1.50447e+08          1.0374e+10            NaN  1.7306e+10
2021-12-31     5.66e+08 1.52862e+08          1.0123e+10            NaN  1.7063e+10
2022-06-30          NaN 1.56896e+08           7.951e+09            NaN  1.6791e+10
2022-12-31     5.29e+08 1.59843e+08           8.481e+09            NaN  1.6551e+10
2023-06-30     2.29e+08 1.63756e+08           8.575e+09            NaN   1.617e+10
2023-12-31     4.92e+08 1.64542e+08           8.818e+09            NaN  1.5886e+10
2024-06-30     3.09e+08 1.68243e+08           7.775e+09            NaN  1.5492e+10
2024-12-31      6.2e+08 1.72537e+08           8.726e+09            NaN  1.5137e+10
2025-06-30      3.1e+08 1.76431e+08           8.484e+09            NaN  1.4884e+10
2025-12-31     6.22e+08 1.80221e+08           9.578e+09          0.171  1.4678e+10
2026-06-30     3.18e+08 1.82488e+08           6.552e+09          0.174  1.4321e+10
```

**BBVA**

```
field       at1_coupons  customers  minority_interests  rote_reported  shares_out
ref_date                                                                         
2020-12-31     3.87e+08   8.07e+07           5.472e+09            NaN 6.65353e+09
2021-06-30     2.01e+08        NaN           5.428e+09            NaN   6.659e+09
2021-12-31     3.59e+08   8.17e+07           4.853e+09            NaN 6.54025e+09
2022-06-30     1.62e+08        NaN           3.351e+09            NaN   6.377e+09
2022-12-31     3.13e+08   8.93e+07           3.624e+09            NaN 6.02463e+09
2023-06-30     1.48e+08   6.96e+07           3.517e+09            NaN   5.962e+09
2023-12-31     3.45e+08   7.15e+07           3.564e+09            NaN 5.83355e+09
2024-06-30     1.89e+08   7.55e+07           3.851e+09            NaN   5.752e+09
2024-12-31     3.88e+08   7.72e+07           4.359e+09            NaN 5.75662e+09
2025-06-30        2e+08   7.91e+07           4.059e+09            NaN   5.755e+09
2025-12-31     3.97e+08   8.12e+07           4.441e+09          0.193 5.69136e+09
2026-06-30     2.11e+08   8.28e+07           4.839e+09          0.222   5.575e+09
```

**CABK**

```
field       at1_coupons  customers  minority_interests  rote_reported  shares_out
ref_date                                                                         
2020-12-31     1.43e+08   1.52e+07             2.5e+07            NaN   5.977e+09
2021-06-30     1.08e+08    2.1e+07             2.9e+07            NaN   8.053e+09
2021-12-31     2.44e+08   2.07e+07             3.1e+07            NaN   8.053e+09
2022-06-30      1.4e+08   2.04e+07             3.1e+07            NaN 7.86223e+09
2022-12-31     2.61e+08   2.02e+07             3.2e+07            NaN   7.494e+09
2023-06-30     1.35e+08   2.01e+07             3.2e+07            NaN   7.495e+09
2023-12-31     2.77e+08   2.01e+07             3.2e+07            NaN   7.367e+09
2024-06-30     1.38e+08   2.02e+07             3.2e+07            NaN    7.26e+09
2024-12-31     2.67e+08   2.03e+07             3.4e+07            NaN   7.118e+09
2025-06-30     1.36e+08   2.05e+07             1.1e+07            NaN   7.069e+09
2025-12-31     2.78e+08   2.07e+07             1.6e+07          0.175   7.008e+09
2026-06-30     1.43e+08   2.09e+07             1.4e+07           0.18   6.959e+09
```

**SAB**

```
field       at1_coupons  minority_interests  rote_reported  shares_out
ref_date                                                              
2020-12-31    7.325e+07          7.1634e+07            NaN  5.5784e+09
2021-06-30   4.5096e+07          7.5876e+07            NaN         NaN
2021-12-31  1.00593e+08           2.498e+07            NaN 5.58629e+09
2022-06-30   6.3795e+07          3.8197e+07            NaN         NaN
2022-12-31  1.10374e+08          3.4344e+07            NaN 5.60219e+09
2023-06-30   5.8711e+07          3.5048e+07            NaN         NaN
2023-12-31  1.15391e+08          3.4213e+07            NaN   5.403e+09
2024-06-30   5.6445e+07          3.4939e+07            NaN   5.361e+09
2024-12-31   9.8155e+07          3.4416e+07            NaN   5.361e+09
2025-06-30   5.6563e+07            3.55e+07            NaN    5.12e+09
2025-12-31  1.45625e+08          3.4603e+07          0.143   4.998e+09
2026-06-30   8.1875e+07           3.769e+07          0.149   4.781e+09
```

**BKT**

```
field       rote_reported  shares_out
ref_date                             
2020-12-31            NaN 8.97974e+08
2021-12-31            NaN 8.98639e+08
2022-12-31            NaN 8.98645e+08
2023-12-31            NaN 8.98646e+08
2024-12-31            NaN 8.98677e+08
2025-12-31         0.2003 8.98696e+08
2026-06-30         0.2036 8.98685e+08
```

**UNI**

```
field       at1_coupons  minority_interests  rote_reported  shares_out
ref_date                                                              
2020-12-31     6.85e+06             473,000            NaN 1.57958e+09
2021-06-30          NaN             520,000            NaN         NaN
2021-12-31     6.58e+06             426,000            NaN 2.65067e+09
2022-06-30          NaN             446,000            NaN         NaN
2022-12-31   3.1223e+07             445,000            NaN 2.65455e+09
2023-06-30   1.8937e+07            2.61e+06            NaN 2.65473e+09
2023-12-31   3.1225e+07           2.431e+06            NaN 2.65191e+09
2024-06-30   1.8937e+07           2.315e+06            NaN 2.61806e+09
2024-12-31   3.1225e+07             436,000            NaN 2.56928e+09
2025-06-30   1.8937e+07          1.4814e+07            NaN 2.56962e+09
2025-12-31   3.1225e+07          1.7394e+07          0.098 2.56888e+09
2026-06-30   1.9038e+07          1.7304e+07            0.1  2.5693e+09
```

**UCG**

```
field       at1_coupons    fte  minority_interests  rote_reported  shares_out
ref_date                                                                     
2020-12-31     3.26e+08 82,107            4.35e+08            NaN   2.237e+09
2021-06-30     1.65e+08 80,879            4.47e+08            NaN   2.226e+09
2021-12-31     3.43e+08 78,571            4.65e+08            NaN   2.211e+09
2022-06-30     1.57e+08 76,671            4.24e+08            NaN   2.081e+09
2022-12-31     2.98e+08 75,040            1.58e+08            NaN   1.935e+09
2023-06-30      1.4e+08 73,108            1.48e+08            NaN   1.816e+09
2023-12-31      2.5e+08 70,752            1.64e+08            NaN   1.712e+09
2024-06-30      1.1e+08 69,454            1.58e+08            NaN    1.63e+09
2024-12-31     1.96e+08 69,722               4e+08            NaN   1.551e+09
2025-06-30     1.53e+08 68,710            3.95e+08            NaN   1.558e+09
2025-12-31     2.92e+08 67,118            3.98e+08          0.192   1.513e+09
2026-06-30     1.61e+08 66,180            3.93e+08          0.237   1.508e+09
```

**ISP**

```
field       minority_interests  shares_out
ref_date                                  
2020-12-31             4.5e+08 1.93883e+10
2021-06-30            3.18e+08         NaN
2021-12-31            2.91e+08 1.93998e+10
2022-06-30            2.48e+08         NaN
2022-12-31            1.66e+08 1.89649e+10
2023-06-30            1.52e+08 1.82737e+10
2023-12-31            1.64e+08 1.82569e+10
2024-06-30            1.25e+08 1.80849e+10
2024-12-31            1.45e+08  1.7778e+10
2025-06-30            1.39e+08 1.76311e+10
2025-12-31            1.52e+08 1.73877e+10
2026-06-30            1.26e+08 1.76521e+10
```

**BAMI**

```
field       at1_coupons  minority_interests  rote_reported  shares_out
ref_date                                                              
2020-12-31     3.86e+07           1.894e+06            NaN 1.50906e+09
2021-06-30          NaN           1.289e+06            NaN 1.51154e+09
2021-12-31     6.38e+07           1.108e+06            NaN 1.51161e+09
2022-06-30     3.84e+07           1.402e+06            NaN 1.50897e+09
2022-12-31     8.73e+07             720,000            NaN 1.50902e+09
2023-06-30     4.89e+07             383,000            NaN  1.5082e+09
2023-12-31     9.67e+07              68,000            NaN 1.50822e+09
2024-06-30     5.34e+07              74,000            NaN 1.50384e+09
2024-12-31    1.033e+08              69,000            NaN 1.50138e+09
2025-06-30      5.9e+07          5.7641e+07            NaN 1.50474e+09
2025-12-31    1.238e+08          8.0487e+07         0.2238 1.50337e+09
2026-06-30     6.47e+07          8.3105e+07            NaN 1.50584e+09
```

**BPE**

```
field       minority_interests  rote_reported  shares_out
ref_date                                                 
2020-12-31         1.33935e+08            NaN 1.41281e+09
2021-06-30         1.46354e+08            NaN 1.41283e+09
2021-12-31         1.62497e+08            NaN 1.41109e+09
2022-06-30         1.78919e+08            NaN 1.41223e+09
2022-12-31         1.80356e+08            NaN 1.41414e+09
2023-06-30         1.82941e+08            NaN 1.41504e+09
2023-12-31         1.99328e+08            NaN 1.41517e+09
2024-06-30         1.91819e+08            NaN 1.41366e+09
2024-12-31         2.10413e+08            NaN 1.41551e+09
2025-06-30         1.99852e+08            NaN 1.42078e+09
2025-12-31         1.03045e+09         0.2005   1.962e+09
2026-06-30          5.6331e+07          0.206 2.08592e+09
```

**BMPS**

```
field       customers  minority_interests  rote_reported  shares_out
ref_date                                                            
2020-12-31    3.9e+06            1.31e+06            NaN 9.66125e+08
2021-06-30        NaN             1.4e+06            NaN         NaN
2021-12-31    3.7e+06           1.346e+06            NaN         NaN
2022-06-30        NaN             1.4e+06            NaN 1.00241e+09
2022-12-31    3.7e+06             936,000            NaN 1.25969e+09
2023-06-30        NaN             800,000            NaN 1.25969e+09
2023-12-31    3.6e+06             651,000            NaN 1.25969e+09
2024-06-30        NaN             400,000            NaN 1.25969e+09
2024-12-31    3.6e+06             336,000            NaN 1.25969e+09
2025-06-30        NaN             200,000            NaN 1.25969e+09
2025-12-31    7.5e+06         2.24848e+09          0.224 3.03819e+09
2026-06-30        NaN           2.252e+09          0.095 3.03842e+09
```


### E3.2b B.1 fields: missing values, with reason (all 31 banks)

| bank | field | dates | reason |
|---|---|---|---|
| LLOY, NWG, BARC, HSBA, SANUK, NDA, SEB, SHB, DNB, INGA, DANSKE, ISP, CBK, DBK, UCG, BNP, CAG, GLE, RABO, ABN, BAMI, BPE | customers | all, or all 30 Jun | only rounded narrative counts, segment counts or nothing printed |
| LLOY, BARC, NWG (H1), SANUK, DNB, SEB (31 Dec), SHB (6 dates), BNP, GLE, CAG, KBC, CBK (2 dates), CABK 2022-06-30, UNI | fte | 30 Jun dates or as listed | no FTE at the reference date printed (average only, or none) |
| SAN, BBVA, CABK, SAB, BKT, ISP, BPE, BMPS, BAMI | fte | all | headcount only; removed (OPEN-29) |
| SEB, SHB, SWED, INGA | at1_coupons | all | AT1 booked as a liability (OPEN-27) |
| DANSKE | at1_coupons | from 2023-06-30 | equity AT1 redeemed in H1 2022 |
| NDA | at1_coupons | 2026-06-30 | AT1 redeemed in H1 2025 |
| BMPS, BPE | at1_coupons | all | no AT1 in equity (BMPS) / only a parent-company figure (BPE) |
| ISP | at1_coupons | all | no B.1 source; accrued net figure in an own-funds note only (OPEN-28) |
| BKT | at1_coupons | all | net of tax only (OPEN-28) |
| KBC | at1_coupons | 2025-12-31, 2026-06-30 | net of tax only (OPEN-28) |
| BAMI | at1_coupons | 2021-06-30 | net of tax only (OPEN-28) |
| SAN | at1_coupons | 2021-06-30, 2022-06-30 | quarterly reports print no coupon |
| RABO | at1_coupons | 2024-06-30 | equity statement prints no current-period row |
| CAG | minority_interests, at1_coupons | to 2023-12-31 | documents hold CASA statements only |
| CAG | at1_coupons | 2024-06-30 | only a later comparative; removed (Deviation 10) |
| GLE | all B.1 fields | 2020-12-31 to 2023-12-31 | documents not obtainable |
| BKT | all B.1 fields | 2021-06-30 to 2024-06-30 | documents not obtainable |
| SHB, SEB, DANSKE, BKT | minority_interests | all | no NCI line, or printed as a dash |
| NDA | minority_interests | from 2022-06-30 | dash or not printed |
| SWED | minority_interests | 30 Jun from 2024 | no NCI line in the interim balance sheet |
| UNI | at1_coupons, shares_out | 2021-06-30, 2022-06-30 | decimal comma documents: not entered (decimal_mark set in this session, after the entries were made) |
| RABO | shares_out | all | cooperative, no ordinary shares |
| CAG | shares_out, rote_reported | all | only Credit Agricole S.A. figures |
| NDA | shares_out | 2020-12-31 | text layer prints `11 .9`; fails provenance |
| BMPS | shares_out | 2021-06-30, 2021-12-31 | treasury shares only as a percentage / text layer splits the number |
| DNB, ISP, SEB (31 Dec 2020-2023 gross), SAB, BBVA (H1) | shares_out | 30 Jun dates | no period-end net count printed |
| DNB, DANSKE, SEB, SHB, SWED, ISP, RABO, ABN, CAG | rote_reported | 2025-12-31 and/or 2026-06-30 | bank publishes ROE only, or no RoTE for the period |


### E3.3a one_offs.csv rows by bank at step 3.3 (616 rows; step 3.5 removed 40 under 03b B.6, E3b.3, leaving 576)

```
bank_id
LLOY      49
NWG       91
BARC      22
HSBA      56
SANUK     23
NDA        9
DNB        0
DANSKE     2
SEB        3
SHB       32
SWED       4
INGA       2
ABN       48
KBC       14
RABO      33
BNP       37
GLE       10
CAG       36
DBK       47
CBK       13
SAN        8
BBVA       2
CABK       9
SAB        5
BKT        0
UNI        3
UCG        4
ISP        0
BAMI      40
BPE       14
BMPS       0
```


### E3.3b The 10 largest one offs by |amount| / total operating income of the same bank and date (report row where present, else eba; amount converted to the TOI currency at the year to date P&L rate)

```
bank_id   ref_date                  field       amount  amount_in_toi_ccy          toi toi_ccy toi_family      rel                                                                                                                                             description
   CABK 2021-06-30         admin_expenses 1.970000e+09       1.970000e+09 4.380311e+09     EUR        eba 0.449740 Extraordinary expenses (Bankia merger: labour agreement and integration costs) excluded from pre-impairment income stripping out extraordinary expenses
    UNI 2021-12-31             provisions 3.990000e+08       3.990000e+08 1.145512e+09     EUR        eba 0.348316                                    Provisions for personnel / office / IT restructuring (Liberbank merger) - deducted in the pro-forma income statement
 DANSKE 2022-12-31             provisions 1.380000e+10       1.854947e+09 5.970360e+09     EUR        eba 0.310693                                                       Provision for Estonia matter (excluded from Adj. return on avg. shareholders equity and Adj. C/I)
    SAN 2020-12-31     impairments_nonfin 1.010000e+10       1.010000e+10 4.540651e+10     EUR        eba 0.222435                                                                           Adjustment to the valuation of goodwill arising from the Group's acquisitions
    CBK 2021-06-30         admin_expenses 9.760000e+08       9.760000e+08 4.539684e+09     EUR        eba 0.214993                                                                                                         Restructuring expenses (below operating profit)
   CABK 2021-12-31         admin_expenses 1.884000e+09       1.884000e+09 9.642348e+09     EUR        eba 0.195388                                                                            M&A one off: extraordinary expenses - estimated cost of the labour agreement
    CBK 2020-12-31     impairments_nonfin 1.578000e+09       1.578000e+09 8.469237e+09     EUR        eba 0.186321                                                                            Impairments on goodwill and other intangible assets (below operating profit)
   BARC 2022-06-30             provisions 1.857000e+09       1.857000e+09 1.320400e+10     GBP     report 0.140639                                                            Litigation and conduct (incl. Over-issuance of Securities rescission losses and SEC penalty)
    ABN 2021-06-30         admin_expenses 4.800000e+08       4.800000e+08 3.650509e+09     EUR        eba 0.131489                                                                                                                                          AML settlement
    NDA 2022-06-30 gains_held_for_trading 5.290000e+08       5.290000e+08 4.259999e+09     EUR        eba 0.124178           IAC Q1 2022 non-deductible loss from recycling of accumulated FX losses related to operations in Russia (Net result from items at fair value)
```


### E3.4a, E3.4b

Superseded by E3b.1 and E3b.5 (rote after instruction 03b).

### E3.4c Hand checks (recomputed after instruction 03c B.1)

```
#### LLOY: rote at 2025-12-31
at1_in_equity: 2024-12-31 = 1, 2025-12-31 = 1 (report entries)
at1_coupon_in_pl: 2024-12-31 = 0, 2025-12-31 = 0 (report entries)
profit_to_ordinary = profit_owners 4,659,000,000 (report) - at1_coupons 463,000,000 (report) = 4,196,000,000
tangible_equity 2024-12-31 = total_equity 45,888,000,000 (report) - minority_interests 172,000,000 - at1_instruments 6,170,000,000 - intangibles_deduction 5,679,000,000 = 33,867,000,000
tangible_equity 2025-12-31 = total_equity 47,867,000,000 (report) - minority_interests 199,000,000 - at1_instruments 5,947,000,000 - intangibles_deduction 5,996,000,000 = 35,725,000,000
average tangible_equity = 34,796,000,000.0; rote (hand) = 4,196,000,000 / 34,796,000,000.0 = 0.120589
kpi.csv: value 0.120589, numerator 4,196,000,000, denominator 34,796,000,000.0, family report, status ok; difference 7.59e-13

#### BBVA: rote at 2024-12-31
at1_in_equity: 2023-12-31 = 0, 2024-12-31 = 0 (report entries)
at1_coupon_in_pl: 2023-12-31 = 0, 2024-12-31 = 0 (report entries)
profit_to_ordinary = profit_owners 10,040,349,000 (eba) - at1_coupons 388,000,000 (report) = 9,652,349,000
tangible_equity 2023-12-31 = total_equity 55,128,346,000 (eba) - minority_interests 3,564,000,000 - at1_instruments 0 (at1_in_equity 0) - intangibles_deduction 1,421,125,000 = 50,143,221,000
tangible_equity 2024-12-31 = total_equity 59,828,484,000 (eba) - minority_interests 4,359,000,000 - at1_instruments 0 (at1_in_equity 0) - intangibles_deduction 1,553,379,000 = 53,916,105,000
average tangible_equity = 52,029,663,000.0; rote (hand) = 9,652,349,000 / 52,029,663,000.0 = 0.185516
kpi.csv: value 0.185516, numerator 9,652,349,000, denominator 52,029,663,000.0, family eba+report, status at1_liability; difference 2.48e-11

#### SEB: rote at 2025-12-31
at1_in_equity: 2024-12-31 = 0, 2025-12-31 = 0 (report entries)
at1_coupon_in_pl: 2024-12-31 = 1, 2025-12-31 = 1 (report entries)
profit_to_ordinary = profit_owners 31,063,000,000 (report) - at1_coupons 0 (at1_coupon_in_pl 1: status coupon_in_pl) = 31,063,000,000
tangible_equity 2024-12-31 = total_equity 231,148,000,000 (report) - minority_interests 0 - at1_instruments 0 (at1_in_equity 0) - intangibles_deduction 6,654,000,000 = 224,494,000,000
tangible_equity 2025-12-31 = total_equity 230,263,000,000 (report) - minority_interests 0 - at1_instruments 0 (at1_in_equity 0) - intangibles_deduction 6,052,000,000 = 224,211,000,000
average tangible_equity = 224,352,500,000.0; rote (hand) = 31,063,000,000 / 224,352,500,000.0 = 0.138456
kpi.csv: value 0.138456, numerator 31,063,000,000, denominator 224,352,500,000.0, family report, status at1_liability;no_nci_line;coupon_in_pl; difference 2.25e-11
```

### E3.4d Market coverage per ticker

```
ticker      first       last  rows currency
   ABN.AS 2020-12-01 2026-07-31  1451      EUR
  BAMI.MI 2020-12-01 2026-07-31  1439      EUR
   BARC.L 2020-12-01 2026-07-31  1428      GBp
  BBVA.MC 2020-12-01 2026-07-31  1449      EUR
   BKT.MC 2020-12-01 2026-07-31  1449      EUR
  BMPS.MI 2020-12-01 2026-07-31  1439      EUR
   BNP.PA 2020-12-01 2026-07-31  1451      EUR
   BPE.MI 2020-12-01 2026-07-31  1439      EUR
  CABK.MC 2020-12-01 2026-07-31  1449      EUR
   CBK.DE 2020-12-01 2026-07-31  1442      EUR
DANSKE.CO 2020-12-01 2026-07-31  1415      DKK
   DBK.DE 2020-12-01 2026-07-31  1442      EUR
   DNB.OL 2020-12-01 2026-07-31  1421      NOK
   GLE.PA 2020-12-01 2026-07-31  1451      EUR
   HSBA.L 2020-12-01 2026-07-31  1428      GBp
  INGA.AS 2020-12-01 2026-07-31  1451      EUR
   ISP.MI 2020-12-01 2026-07-31  1439      EUR
   KBC.BR 2020-12-01 2026-07-31  1451      EUR
   LLOY.L 2020-12-01 2026-07-31  1429      GBp
NDA-FI.HE 2020-12-01 2026-07-31  1422      EUR
    NWG.L 2020-12-01 2026-07-31  1429      GBp
   SAB.MC 2020-12-01 2026-07-31  1449      EUR
   SAN.MC 2020-12-01 2026-07-31  1449      EUR
 SEB-A.ST 2020-12-01 2026-07-31  1422      SEK
 SHB-A.ST 2020-12-01 2026-07-31  1422      SEK
SWED-A.ST 2020-12-01 2026-07-31  1422      SEK
   UCG.MI 2020-12-01 2026-07-31  1439      EUR
   UNI.MC 2020-12-01 2026-07-31  1449      EUR
```

### E3.4e FRED coverage

None: the FRED stage failed (Deviation 1) and was replaced by the yields stage (E3b.4).

### E3b.1 (superseded by E3c.6) rote for every bank at every date (pct; a blank shows its status, mi: = missing_input:)

**reported**

```
date                2021-12-31             2022-06-30             2022-12-31             2023-06-30             2023-12-31             2024-06-30             2024-12-31             2025-06-30             2025-12-31                2026-06-30
bank_id                                                                                                                                                                                                                                         
ABN         mi:tangible_equity                   7.90                   8.75                  11.60                  12.17                  11.74                  10.27                   9.49                   8.88                      9.79
BAMI                      4.71                   4.67                   5.62                   7.93                  10.73                  11.60                  15.39                  20.90                  16.96                     16.60
BARC                     13.03                  10.27                  10.36                  11.99                   8.82                   8.26                  10.47                  11.55                  11.41                     12.25
BBVA                     11.06                  13.14                  14.60                  15.99                  16.71                  18.38                  19.30                  19.65                  19.15                     19.81
BKT         mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary  mi:minority_interests     mi:minority_interests
BMPS                      5.28                   2.31                  -2.98                   5.49                  23.41                  27.19                  18.26                  15.28                  16.42                     18.71
BNP                       9.41                   9.99                   9.91                  11.73                  10.35                   9.51                  10.70                  10.61                  11.19                     12.46
BPE         mi:tangible_equity  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons            mi:at1_coupons
CABK                     19.76                   8.39                  10.10                  11.99                  15.15                  17.14                  17.51                  18.42                  17.28                     17.84
CAG         mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:at1_instruments        mi:at1_instruments
CBK                       1.17                   5.58                   4.84                   6.10                   7.44                   7.81                   8.57                   8.34     mi:at1_instruments        mi:at1_instruments
DANSKE      mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity  mi:minority_interests     mi:minority_interests
DBK                       3.86                   4.59                   8.72                   8.28                   7.23                   5.72                   4.62                   8.24                  10.03                     10.60
DNB      mi:profit_to_ordinary  mi:profit_to_ordinary     mi:tangible_equity                  15.86                  15.96                  17.65                  16.82                  17.87                  16.83        mi:at1_instruments
GLE         mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity     mi:tangible_equity                   9.85                     10.70
HSBA                      7.62                   8.48                   9.20                  15.32                  14.48                  14.53                  14.92                  11.51                  13.32                     15.24
INGA                      8.96                   7.38                   7.19                  11.54                  14.66                  13.93                  12.84                  12.68                  12.94                     13.80
ISP             mi:at1_coupons  mi:profit_to_ordinary                   8.43  mi:profit_to_ordinary                  15.53                  16.39                  16.70                  17.43                  18.09                     17.99
KBC                      12.68     mi:tangible_equity                  16.44                  18.80                  17.67                  15.21                  16.37                  16.49                  15.68                     16.03
LLOY                     12.72                  10.48                  12.39                  14.03                  13.79                  13.88                  11.47                  11.91                  12.06                     13.50
NDA                      13.60     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity  mi:minority_interests     mi:minority_interests
NWG                       9.23                  10.08                  11.70                  14.61                  17.18                  17.23                  17.31                  18.26                  19.16                     21.00
RABO                      9.29                   7.39                   6.39                   8.40                   9.72  mi:profit_to_ordinary                  10.77  mi:profit_to_ordinary                   9.63                      9.32
SAB                       5.06                   6.61                   7.88                   9.27                  11.74                  13.26                  14.96                  16.47                  14.44                     15.85
SAN                      11.90                  13.17                  13.46                  13.45                  14.76                  15.38                  15.64                  16.25                  16.51                     18.12
SANUK                     9.85  mi:minority_interests  mi:minority_interests  mi:minority_interests  mi:minority_interests  mi:minority_interests  mi:minority_interests  mi:minority_interests  mi:minority_interests     mi:minority_interests
SEB         mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity  mi:minority_interests     mi:minority_interests
SHB                      10.85                  11.14                  11.11                  12.92                  14.34                  15.22                  12.68                  13.18                  12.06  mi:intangibles_deduction
SWED                     14.68                  13.60                  13.93                  18.36                  20.18     mi:tangible_equity                  18.01     mi:tangible_equity                  16.14     mi:minority_interests
UCG                       2.22                   2.83                  11.10                  14.73                  16.09                  17.92                  16.62                  17.67                  18.46        mi:at1_instruments
UNI                      22.89  mi:profit_to_ordinary                   3.95  mi:profit_to_ordinary                   3.97                   6.43                   8.94                   9.47                   9.58              mixed_family
```

**underlying**

```
date                2021-12-31             2022-06-30             2022-12-31             2023-06-30             2023-12-31             2024-06-30             2024-12-31             2025-06-30             2025-12-31                2026-06-30
bank_id                                                                                                                                                                                                                                         
ABN         mi:tangible_equity                   7.19                  10.35                  13.18                  12.71                  12.25                  10.69                  10.07                   9.13                      9.80
BAMI                      6.66                   6.80                   7.00                   8.21                  11.49                  12.43                  17.56                  23.12                  17.25                     16.98
BARC                     14.71                  13.99                  13.06                  12.50                  10.81                  10.84                  10.72                  11.38                  12.14                     12.99
BBVA                     12.87                  13.14                  14.60                  15.99                  16.71                  18.38                  19.30                  19.65                  19.15                     19.81
BKT         mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary  mi:minority_interests     mi:minority_interests
BMPS                      5.28                   2.31                  -2.98                   5.49                  23.41                  27.19                  18.26                  15.28                  16.42                     18.71
BNP                       9.79                  10.15                  10.38                  12.90                  13.01                  11.77                  11.18                  11.11                  11.78                     12.87
BPE         mi:tangible_equity  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons            mi:at1_coupons
CABK                     28.51                   9.57                  10.26                  12.09                  15.18                  17.15                  17.51                  18.42                  17.28                     17.84
CAG         mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:at1_instruments        mi:at1_instruments
CBK                       1.17                   5.58                   4.84                   6.10                   7.44                   7.81                   8.57                   8.34     mi:at1_instruments        mi:at1_instruments
DANSKE      mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity  mi:minority_interests     mi:minority_interests
DBK                       7.47                   7.29                   8.97                   9.58                   9.20                   9.74                   8.93                   9.43                  10.62                     11.12
DNB      mi:profit_to_ordinary  mi:profit_to_ordinary     mi:tangible_equity                  15.86                  15.96                  17.65                  16.82                  17.87                  16.83        mi:at1_instruments
GLE         mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity     mi:tangible_equity                  10.53                     11.30
HSBA                      9.26                  10.47                  13.07                  16.25                  16.32                  16.26                  16.10                  16.94                  17.55                     18.04
INGA                      8.96                   7.38                   7.19                  11.54                  14.66                  13.93                  12.84                  12.68                  12.94                     13.80
ISP             mi:at1_coupons  mi:profit_to_ordinary                   8.43  mi:profit_to_ordinary                  15.53                  16.39                  16.70                  17.43                  18.09                     17.99
KBC                      13.77     mi:tangible_equity                  17.43                  19.82                  18.32                  15.88                  16.84                  16.96                  16.52                     16.85
LLOY                     15.42                  13.06                  13.68                  15.72                  14.65                  14.83                  12.56                  12.66                  12.39                     13.45
NDA                      13.60     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity  mi:minority_interests     mi:minority_interests
NWG                      12.37                  11.92                  12.71                  15.41                  16.95                  17.84                  18.23                  19.62                  18.90                     19.91
RABO                     10.29                   8.76                   7.84                   9.20                   9.05  mi:profit_to_ordinary                  10.88  mi:profit_to_ordinary                   9.34                      8.98
SAB                       5.06                   6.61                   7.88                   9.27                  11.74                  13.26                  14.96                  16.47                  14.44                     15.85
SAN                      12.94                  13.17                  13.46                  13.45                  14.76                  15.38                  15.64                  16.82                  17.06                     18.12
SANUK                    12.55  mi:minority_interests  mi:minority_interests  mi:minority_interests  mi:minority_interests  mi:minority_interests  mi:minority_interests  mi:minority_interests  mi:minority_interests     mi:minority_interests
SEB         mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity  mi:minority_interests     mi:minority_interests
SHB                      10.65                  10.24                  10.74                  13.10                  14.41                  15.52                  13.04                  13.44                  12.18  mi:intangibles_deduction
SWED                     14.68                  13.60                  13.93                  18.93                  20.69     mi:tangible_equity                  18.01     mi:tangible_equity                  16.14     mi:minority_interests
UCG                       2.22                   2.60                  11.10                  14.73                  16.09                  17.92                  16.62                  17.67                  18.46        mi:at1_instruments
UNI                      31.50  mi:profit_to_ordinary                   3.95  mi:profit_to_ordinary                   3.97                   6.43                   8.94                   9.47                   9.58              mixed_family
```

Blank rote by status (reported):

```
status
missing_input:at1_coupons               6
missing_input:at1_instruments           6
missing_input:intangibles_deduction     1
missing_input:minority_interests       18
missing_input:profit_to_ordinary       23
missing_input:tangible_equity          42
mixed_family                            1
```

### E3b.2 (superseded by E3c.1d) at1_in_equity, bank x date (blank = not entered)

```
ref_date  2020-12-31  2021-06-30  2021-12-31  2022-06-30  2022-12-31  2023-06-30  2023-12-31  2024-06-30  2024-12-31  2025-06-30  2025-12-31  2026-06-30
bank_id                                                                                                                                                 
ABN                1           1           1           1           1           1           1           1           1           1           1           1
BAMI               1           1           1           1           1           1           1           1           1           1           1           1
BARC               1           1           1           1           1           1           1           1           1           1           1           1
BBVA               0           0           0           0           0           0           0           0           0           0           0           0
BKT                0         NaN           0         NaN           0         NaN           0         NaN           0           0           0           0
BMPS               0           0           0           0           0           0           0           0           0           0           0           0
BNP                1           1           1           1           1           1           1           1           1           1           1           1
BPE                1           1           1           1           1           1           1           1           1           1           1           1
CABK               0           0           0           0           0           0           0           0           0           0           0           0
CAG              NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN           1           1           1           1
CBK                1           1           1           1           1           1           1           1           1           1           1           1
DANSKE             1           1           1           0           0           0           0           0           0           0           0           0
DBK                1           1           1           1           1           1           1           1           1           1           1           1
DNB                1           1           1           1           1           1           1           1           1           1           1           1
GLE              NaN         NaN         NaN         NaN         NaN         NaN           1           1           1           1           1           1
HSBA               1           1           1           1           1           1           1           1           1           1           1           1
INGA               0           0           0           0           0           0           0           0           0           0           0           0
ISP                1           1           1           1           1           1           1           1           1           1           1           1
KBC                1           1           1           1           1           1           1           1           1           1           1           1
LLOY               1           1           1           1           1           1           1           1           1           1           1           1
NDA                1           1           1           1           1           1           1           1           1           0           0           0
NWG                1           1           1           1           1           1           1           1           1           1           1           1
RABO               1           1           1           1           1           1           1           1           1           1           1           1
SAB                0           0           0           0           0           0           0           0           0           0           0           0
SAN                0           0           0           0           0           0           0           0           0           0           0           0
SANUK              1           1           1           1           1           1           1           1           1           1           1           1
SEB                0           0           0           0           0           0           0           0           0           0           0           0
SHB                0           0           0           0           0           0           0           0           0           0           0           0
SWED               0           0           0           0           0           0           0           0           0           0           0           0
UCG                1           1           1           1           1           1           1           1           1           1           1           1
UNI                1           1           1           1           1           1           1           1           1           1           1           1
```

### E3b.3 Every one off removed under decision 6 (40 rows)

```
bank_id   ref_date                         field     amount page verdict                                                                                                                               reason
   INGA 2020-12-31                admin_expenses  310000000  373  remove                                                                Capital management narrative text on resilient net profit not a table
   INGA 2020-12-31           other_operating_net  230000000  373  remove                                                                Capital management narrative text on resilient net profit not a table
    KBC 2021-12-31                admin_expenses   97000000  299  remove                                                KBC cost/income APM table lists only aggregate a1*/b2*; item appears only in footnote
    KBC 2021-12-31                admin_expenses   18000000  299  remove                                                KBC cost/income APM table lists only aggregate a1*/b2*; item appears only in footnote
    KBC 2021-12-31                admin_expenses   -9000000  299  remove                                                KBC cost/income APM table lists only aggregate a1*/b2*; item appears only in footnote
    KBC 2021-12-31           other_operating_net   45000000  299  remove                                                KBC cost/income APM table lists only aggregate a1*/b2*; item appears only in footnote
    KBC 2021-12-31           other_operating_net  -28000000  299  remove                                                KBC cost/income APM table lists only aggregate a1*/b2*; item appears only in footnote
    CBK 2020-12-31            impairments_nonfin 1578000000  169  remove                                                                   IFRS consolidated income statement not an APM reconciliation table
    CBK 2020-12-31                admin_expenses  814000000  169  remove                                                                   IFRS consolidated income statement not an APM reconciliation table
    CBK 2021-12-31                admin_expenses 1078000000  151  remove                                                                   IFRS consolidated income statement not an APM reconciliation table
    CBK 2022-12-31                admin_expenses   94000000  157  remove                                                                   IFRS consolidated income statement not an APM reconciliation table
    CBK 2023-12-31                admin_expenses   18000000  270  remove                                                                   IFRS consolidated income statement not an APM reconciliation table
    CBK 2024-12-31                admin_expenses    3000000  389  remove                                                                   IFRS consolidated income statement not an APM reconciliation table
    CBK 2025-12-31                admin_expenses  562000000  287  remove                                                                   IFRS consolidated income statement not an APM reconciliation table
    CBK 2021-06-30                admin_expenses  976000000   39  remove                                                                   IFRS consolidated income statement not an APM reconciliation table
    CBK 2022-06-30                admin_expenses   39000000   40  remove                                                                   IFRS consolidated income statement not an APM reconciliation table
    CBK 2023-06-30                admin_expenses    8000000   37  remove                                                                   IFRS consolidated income statement not an APM reconciliation table
    CBK 2024-06-30                admin_expenses    2000000   37  remove                                                                   IFRS consolidated income statement not an APM reconciliation table
    CBK 2025-06-30                admin_expenses  534000000   38  remove                                                                   IFRS consolidated income statement not an APM reconciliation table
    CBK 2026-06-30                admin_expenses    1000000   38  remove                                                                   IFRS consolidated income statement not an APM reconciliation table
    SAB 2020-12-31                admin_expenses  426000000  318  remove Directors report management income statement (Profit/(loss) for the year) with memorandum cost split not an APM reconciliation table
    SAB 2021-12-31                admin_expenses  320000000  297  remove Directors report management income statement (Profit/(loss) for the year) with memorandum cost split not an APM reconciliation table
    SAB 2023-12-31                admin_expenses   33000000  282  remove Directors report management income statement (Profit/(loss) for the year) with memorandum cost split not an APM reconciliation table
    SAB 2024-12-31                admin_expenses   21000000  301  remove Directors report management income statement (Profit/(loss) for the year) with memorandum cost split not an APM reconciliation table
    SAB 2026-06-30                admin_expenses   88000000  108  remove Directors report management income statement (Profit/(loss) for the year) with memorandum cost split not an APM reconciliation table
    UNI 2023-12-31           other_operating_net   63800000  311  remove                                                          Management report key figures table; levy only in footnote not a table line
    BPE 2025-12-31                admin_expenses  177500000   62  remove                                              Report on Operations narrative bullet list (Integration Costs / PPA Impact) not a table
    BPE 2025-12-31                admin_expenses   57000000   62  remove                                              Report on Operations narrative bullet list (Integration Costs / PPA Impact) not a table
    BPE 2025-12-31                    provisions   12200000   62  remove                                              Report on Operations narrative bullet list (Integration Costs / PPA Impact) not a table
    BPE 2025-12-31           other_operating_net   11200000   62  remove                                              Report on Operations narrative bullet list (Integration Costs / PPA Impact) not a table
    BPE 2025-12-31                  depreciation   30600000   62  remove                                              Report on Operations narrative bullet list (Integration Costs / PPA Impact) not a table
    BPE 2025-12-31                  depreciation   11300000   62  remove                                              Report on Operations narrative bullet list (Integration Costs / PPA Impact) not a table
    BPE 2025-12-31               impairments_fin  180000000   62  remove                                              Report on Operations narrative bullet list (Integration Costs / PPA Impact) not a table
    BPE 2025-12-31               impairments_fin  -37900000   62  remove                                              Report on Operations narrative bullet list (Integration Costs / PPA Impact) not a table
    BPE 2026-06-30                admin_expenses   11400000   52  remove                                              Report on Operations narrative bullet list (Integration Costs / PPA Impact) not a table
    BPE 2026-06-30                admin_expenses   29900000   52  remove                                              Report on Operations narrative bullet list (Integration Costs / PPA Impact) not a table
    BPE 2026-06-30                  depreciation   12700000   52  remove                                              Report on Operations narrative bullet list (Integration Costs / PPA Impact) not a table
    BPE 2026-06-30 gains_derecognition_not_fvtpl    7200000   52  remove                                              Report on Operations narrative bullet list (Integration Costs / PPA Impact) not a table
    BPE 2026-06-30                  depreciation   11800000   52  remove                                              Report on Operations narrative bullet list (Integration Costs / PPA Impact) not a table
    BPE 2026-06-30               impairments_fin  -25800000   52  remove                                              Report on Operations narrative bullet list (Integration Costs / PPA Impact) not a table
```

### E3b.4 (NO superseded by E3c.4) Yield coverage per country, with the 2025-12 value

```
country   first    last  rows 2025-12  2026-06                                    series
     GB 2020-01 2026-07    79  4.4826    4.796                         BoE IADB IUMAMNPY
     SE 2020-01 2026-07    79    2.82    2.780            IRS.M.SE.L.L40.CI.0000.SEK.N.Z
     NO 2020-01 2026-07    78 missing    4.302 Norges Bank GOVT_GENERIC_RATES M.10Y.GBON
     DK 2020-01 2026-07    79   2.707    2.807            IRS.M.DK.L.L40.CI.0000.DKK.N.Z
     FI 2020-01 2026-07    79   3.165    3.310            IRS.M.FI.L.L40.CI.0000.EUR.N.Z
     NL 2020-01 2026-07    79   2.968    3.077            IRS.M.NL.L.L40.CI.0000.EUR.N.Z
     BE 2020-01 2026-07    79    3.32    3.510            IRS.M.BE.L.L40.CI.0000.EUR.N.Z
     FR 2020-01 2026-07    79    3.56    3.680            IRS.M.FR.L.L40.CI.0000.EUR.N.Z
     DE 2020-01 2026-07    79   2.813    2.964            IRS.M.DE.L.L40.CI.0000.EUR.N.Z
     ES 2020-01 2026-07    79   3.271    3.413            IRS.M.ES.L.L40.CI.0000.EUR.N.Z
     IT 2020-01 2026-07    79   3.552    3.734            IRS.M.IT.L.L40.CI.0000.EUR.N.Z
```

Exact URLs (MANIFEST.json):

```
GB: https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp?csv.x=yes&Datefrom=01/Jan/2020&Dateto=31/Jul/2026&SeriesCodes=IUMAMNPY&CSVF=TN&UsingCodes=Y&VPD=Y&VFD=N
NO: https://data.norges-bank.no/api/data/GOVT_GENERIC_RATES/M.10Y.GBON.?format=csv&startPeriod=2020-01&endPeriod=2026-07&locale=en
DE: https://data-api.ecb.europa.eu/service/data/IRS/M.DE.L.L40.CI.0000.EUR.N.Z?format=csvdata&startPeriod=2020-01&endPeriod=2026-07
```

### E3b.5 (superseded by E3c.5a) rote against rote_reported at 2025-12-31, every bank that prints one (pct; no threshold)

```
bank_id  rote  rote_reported  difference_pts                           status
   BAMI 16.96          22.38           -5.42                               ok
   BARC 11.41          11.30            0.11                               ok
   BBVA 19.15          19.30           -0.15                    at1_liability
    BKT   NaN          20.03             NaN missing_input:minority_interests
   BMPS 16.42          22.40           -5.98                    at1_liability
    BNP 11.19          11.60           -0.41                 from_comparative
    BPE   NaN          20.05             NaN        missing_input:at1_coupons
   CABK 17.28          17.50           -0.22                    at1_liability
    CBK   NaN           8.70             NaN    missing_input:at1_instruments
    DBK 10.03          10.30           -0.27                               ok
    GLE  9.85          10.20           -0.35                               ok
   HSBA 13.32          13.30            0.02                               ok
   INGA 12.94          13.60           -0.66                    at1_liability
    KBC 15.68          16.00           -0.32                   at1_net_of_tax
   LLOY 12.06          12.90           -0.84                               ok
    NWG 19.16          19.20           -0.04                               ok
    SAB 14.44          14.30            0.14                    at1_liability
    SAN 16.51          17.10           -0.59                    at1_liability
  SANUK   NaN          10.00             NaN missing_input:minority_interests
    UCG 18.46          19.20           -0.74                               ok
    UNI  9.58           9.80           -0.22                               ok
```


### E3c.1a at1_coupon_in_pl, bank x date (blank = not entered; half year dates are class_from_annual copies)

```
ref_date 2020-12-31 2021-06-30 2021-12-31 2022-06-30 2022-12-31 2023-06-30 2023-12-31 2024-06-30 2024-12-31 2025-06-30 2025-12-31 2026-06-30
bank_id                                                                                                                                     
LLOY              0          0          0          0          0          0          0          0          0          0          0          0
NWG               0          0          0          0          0          0          0          0          0          0          0          0
BARC              0          0          0          0          0          0          0          0          0          0          0          0
HSBA              0          0          0          0          0          0          0          0          0          0          0          0
SANUK             0          0          0          0          0          0          0          0          0          0          0          0
NDA               0          0          0          0          0          0          0          0          0          0          0          0
DNB               0          0          0          0          0          0          0          0          0          0          0          0
DANSKE            0          0          0          0          0          1          1          1          1          1          1          1
SEB               1          1          1          1          1          1          1          1          1          1          1          1
SHB               1          1          1          1          1          1          1          1          1          1          1          1
SWED              1          1          1          1          1          1          1          1          1          1          1          1
INGA              1          1          1          1          1          1          1          1          1          1          1          1
ABN               0          0          0          0          0          0          0          0          0          0          0          0
KBC               0          0          0          0          0          0          0          0          0          0          0          0
RABO              0          0          0          0          0          0          0          0          0          0          0          0
BNP               0          0          0          0          0          0          0          0          0          0          0          0
GLE                                                                                 0                     0          0          0          0
CAG                                                                                                       0          0          0          0
DBK               0          0          0          0          0          0          0          0          0          0          0          0
CBK               0          0          0          0          0          0          0          0          0          0          0          0
SAN               0          0          0          0          0          0          0          0          0          0          0          0
BBVA              0          0          0          0          0          0          0          0          0          0          0          0
CABK              0          0          0          0          0          0          0          0          0          0          0          0
SAB               0          0          0          0          0          0          0          0          0          0          0          0
BKT               0          0          0          0          0          0          0          0          0          0          0          0
UNI               0          0          0          0          0          0          0          0          0          0          0          0
UCG               0          0          0          0          0          0          0          0          0          0          0          0
ISP               0          0          0          0          0          0          0          0          0          0          0          0
BAMI              0          0          0          0          0          0          0          0          0          0          0          0
BPE               0          0          0          0          0          0          0          0          0          0          0          0
BMPS
```

### E3c.1b at1_coupon_in_pl annual entries: page and cited line

```
bank_id   ref_date value                  doc page                                  value_as_printed                                                                                                                                                                                             snippet
   LLOY 2020-12-31     0    annual:2020-12-31  221         Distributions on other equity instruments                                                                                                                                     Distributions on other equity instruments — — — — (453) — (453)
   LLOY 2021-12-31     0    annual:2021-12-31  212         Distributions on other equity instruments                                                                                                                                     Distributions on other equity instruments — — — — (429) — (429)
   LLOY 2022-12-31     0    annual:2022-12-31  216         Distributions on other equity instruments                                                                                                                                     Distributions on other equity instruments – – – – (438) – (438)
   LLOY 2023-12-31     0    annual:2023-12-31  218         Distributions on other equity instruments                                                                                                                                     Distributions on other equity instruments – – – – (527) – (527)
   LLOY 2024-12-31     0    annual:2024-12-31  219         Distributions on other equity instruments                                                                                                                                     Distributions on other equity instruments – – – – (498) – (498)
   LLOY 2025-12-31     0    annual:2025-12-31  216                     Distributions on other equity                                                                                                                                                                       Distributions on other equity
    NWG 2020-12-31     0    annual:2020-12-31  261                     Paid-in equity dividends paid                                                                                                                                                     Paid-in equity dividends paid (355) (367) (355)
    NWG 2021-12-31     0    annual:2021-12-31  153                     Paid-in equity dividends paid                                                                                                                                                     Paid-in equity dividends paid (299) (355) (367)
    NWG 2022-12-31     0    annual:2022-12-31  153                     Paid-in equity dividends paid                                                                                                                                                     Paid-in equity dividends paid (249) (299) (355)
    NWG 2023-12-31     0    annual:2023-12-31  303                     Paid-in equity dividends paid                                                                                                                                                     Paid-in equity dividends paid (242) (242) (242)
    NWG 2024-12-31     0    annual:2024-12-31  298                     Paid-in equity dividends paid                                                                                                                                                     Paid-in equity dividends paid (283) (283) (283)
    NWG 2025-12-31     0    annual:2025-12-31  296                     Paid-in equity dividends paid                                                                                                                                                     Paid-in equity dividends paid (352) (352) (352)
   BARC 2020-12-31     0    annual:2020-12-31  284             Other equity instruments coupons paid                                                                                                                                     Other equity instruments coupons paid – (857) – – (857) – (857)
   BARC 2021-12-31     0    annual:2021-12-31  336                                      coupons paid                                                                                                                                                              coupons paid — (804) — — (804) — (804)
   BARC 2022-12-31     0    annual:2022-12-31  421             Other equity instruments coupons paid                                                                                                                                     Other equity instruments coupons paid — (905) — — (905) — (905)
   BARC 2023-12-31     0    annual:2023-12-31  417             Other equity instruments coupons paid                                                                                                                                     Other equity instruments coupons paid — (905) — — (905) — (905)
   BARC 2024-12-31     0    annual:2024-12-31  448             Other equity instruments coupons paid                                                                                                                                             Other equity instruments coupons paid — (990) — — (990)
   BARC 2025-12-31     0    annual:2025-12-31  404             Other equity instruments coupons paid                                                                                                                                             Other equity instruments coupons paid — (997) — — (997)
   HSBA 2020-12-31     0    annual:2020-12-31  284                         Dividends to shareholders                                                                                                                                 Dividends to shareholders — — (1,331) — — — — (1,331) (692) (2,023)
   HSBA 2021-12-31     0    annual:2021-12-31  314                         Dividends to shareholders                                                                                                                                 Dividends to shareholders — — (5,790) — — — — (5,790) (593) (6,383)
   HSBA 2022-12-31     0    annual:2022-12-31  330                         Dividends to shareholders                                                                                                                                 Dividends to shareholders — — (6,544) — — — — (6,544) (426) (6,970)
   HSBA 2023-12-31     0    annual:2023-12-31  334                         Dividends to shareholders                                                                                                                            Dividends to shareholders — — — — — — — (11,593) (11,593) (603) (12,196)
   HSBA 2024-12-31     0    annual:2024-12-31  346                         Dividends to shareholders                                                                                                                            Dividends to shareholders — — — — — — — (16,410) (16,410) (690) (17,100)
   HSBA 2025-12-31     0    annual:2025-12-31  267                         Dividends to shareholders                                                                                                                            Dividends to shareholders — — — — — — — (12,764) (12,764) (718) (13,482)
  SANUK 2020-12-31     0    annual:2020-12-31  211             Dividends on other equity instruments                                                                                                                                 Dividends on other equity instruments — — — — — (147) (147) — (147)
  SANUK 2021-12-31     0    annual:2021-12-31  219             Dividends on other equity instruments                                                                                                                                 Dividends on other equity instruments — — — — — (143) (143) — (143)
  SANUK 2022-12-31     0    annual:2022-12-31  200             Dividends on other equity instruments                                                                                                                                 Dividends on other equity instruments — — — — — (143) (143) — (143)
  SANUK 2023-12-31     0    annual:2023-12-31  186             Dividends on other equity instruments                                                                                                                                 Dividends on other equity instruments — — — — — (133) (133) — (133)
  SANUK 2024-12-31     0    annual:2024-12-31  171             Dividends on other equity instruments                                                                                                                                 Dividends on other equity instruments — — — — — (139) (139) — (139)
  SANUK 2025-12-31     0    annual:2025-12-31  163             Dividends on other equity instruments                                                                                                                                       Dividends on other equity instruments — — — — — — (142) (142)
    NDA 2020-12-31     0    annual:2020-12-31   75                                     Paid interest                                                                                                                                                                         Paid interest on Additional
    NDA 2021-12-31     0    annual:2021-12-31  103                                     Paid interest                                                                                                                                                                         Paid interest on Additional
    NDA 2022-12-31     0    annual:2022-12-31  189                  accounted for directly in equity                                                                      ty are accounted for directly in equity and presented as divi- For information about non-controlling interests, see Note G9.1.
    NDA 2023-12-31     0    annual:2023-12-31  206                  accounted for directly in equity                                                                   are accounted for directly in equity and presented as dividends. requirement for Nordea to pay interest if the instruments are no
    NDA 2024-12-31     0    annual:2024-12-31  275                  accounted for directly in equity                                            fied as equity are accounted for directly in equity Other reserves comprise income and expenses, shares in Nordea have no nominal value. Each share car-
    NDA 2025-12-31     0    annual:2025-12-31  272                  accounted for directly in equity                                                                                                                                                 fied as equity are accounted for directly in equity
    DNB 2020-12-31     0    annual:2020-12-31  145                       reduction in “Other equity” nised at fair value minus any directly attributable transaction costs. expenses from financial instruments belonging to the trading presented as a reduction in “Other equity”, while the advantage
    DNB 2021-12-31     0    annual:2021-12-31  159                     Interest payments AT1 capital                                                                                                                                                           Interest payments AT1 capital (926) (926)
    DNB 2022-12-31     0    annual:2022-12-31  190                     Interest payments AT1 capital                                                                                                                                                         Interest payments AT1 capital (1056) (1056)
    DNB 2023-12-31     0    annual:2023-12-31  139                       reduction in “Other equity”                                                                                                                                                                   as a reduction in “Other equity”.
    DNB 2024-12-31     0    annual:2024-12-31  292                       reduction in “Other equity”                                                       line “Additional Tier 1 Capital” within the Group’s equity. Transaction expenses and interest are presented as a reduction in “Other equity”.
    DNB 2025-12-31     0    annual:2025-12-31  288                       reduction in “Other equity”                                                       line “Additional Tier 1 Capital” within the Group’s equity. Transaction expenses and interest are presented as a reduction in “Other equity”.
 DANSKE 2020-12-31     0    annual:2020-12-31   77        Paid interest on additional tier 1 capital                                                                                                                                    Paid interest on additional tier 1 capital - - - - - - -625 -625
 DANSKE 2021-12-31     0    annual:2021-12-31   61        Paid interest on additional tier 1 capital                                                                                                                                    Paid interest on additional tier 1 capital - - - - - - -466 -466
 DANSKE 2022-12-31     0    annual:2022-12-31   71        Paid interest on additional tier 1 capital                                                                                                                                    Paid interest on additional tier 1 capital - - - - - - -164 -164
 DANSKE 2023-12-31     1    annual:2023-12-31   97                                 Subordinated debt                                                                                                                                                        Subordinated debt - 1,313 -1,313 -846 -2,159
 DANSKE 2024-12-31     1    annual:2024-12-31  144                                 Subordinated debt                                                                                                           Subordinated debt - 1,351 -1,351 -614 -1,965 Subordinated debt - 1,313 -1,313 -846 -2,159
 DANSKE 2025-12-31     1    annual:2025-12-31  154                                 Subordinated debt                                                                                                           Subordinated debt - 1,329 -1,329 -363 -1,692 Subordinated debt - 1,351 -1,351 -614 -1,965
    SEB 2020-12-31     1    annual:2020-12-31  122                          Subordinated liabilities                                                                                                                                  Subordinated liabilities 38,925 –1,348 –3.46% 38,475 –1,348 –3.50%
    SEB 2021-12-31     1    annual:2021-12-31  134                          Subordinated liabilities                                                                                                                                      Subordinated liabilities 27,667 –932 –3.37% 26,904 –932 –3.46%
    SEB 2022-12-31     1    annual:2022-12-31  134                          Subordinated liabilities                                                                                                                                      Subordinated liabilities 28,662 –952 –3.32% 27,760 –952 –3.43%
    SEB 2023-12-31     1    annual:2023-12-31  101                          Subordinated liabilities                                                                   Subordinated liabilities 30,583 –1,188 –3.89% 29,679 –1,188 –4.00% Subordinated liabilities 28,662 –952 –3.32% 27,760 –952 –3.43%
    SEB 2024-12-31     1    annual:2024-12-31  213                          Subordinated liabilities                                                               Subordinated liabilities 38,338 –1,791 –4.67% 37,433 –1,791 –4.78% Subordinated liabilities 30,583 –1,188 –3.89% 29,679 –1,188 –4.00%
    SEB 2025-12-31     1    annual:2025-12-31  224                          Subordinated liabilities                                                                                                                                  Subordinated liabilities 42,866 –1,960 –4.57% 38,338 –1,791 –4.67%
    SHB 2020-12-31     1    annual:2020-12-31  145                          Subordinated liabilities                                                                                                                                                              Subordinated liabilities -1,186 -1,282
    SHB 2021-12-31     1    annual:2021-12-31  152                          Subordinated liabilities                                                                                                                                                              Subordinated liabilities -1,097 -1,186
    SHB 2022-12-31     1    annual:2022-12-31  152                          Subordinated liabilities                                                                                                                                                              Subordinated liabilities -1,368 -1,097
    SHB 2023-12-31     1    annual:2023-12-31  141                          Subordinated liabilities                                                                                                                                                              Subordinated liabilities -1,615 -1,368
    SHB 2024-12-31     1    annual:2024-12-31  125                          Subordinated liabilities                                                                                                                                                              Subordinated liabilities -1,611 -1,615
    SHB 2025-12-31     1    annual:2025-12-31  209                          Subordinated liabilities                                                                                                                                                              Subordinated liabilities −1,581 −1,611
   SWED 2020-12-31     1    annual:2020-12-31  117                          Subordinated liabilities                                                                                                                                            Subordinated liabilities 821 26 800 3,06 993 30 627 3,24
   SWED 2021-12-31     1    annual:2021-12-31  123                          Subordinated liabilities                                                                                                                                                            Subordinated liabilities 764 764 821 821
   SWED 2022-12-31     1    annual:2022-12-31  124                          Subordinated liabilities                                                                                                                                                            Subordinated liabilities 911 911 764 764
   SWED 2023-12-31     1    annual:2023-12-31  129                          Subordinated liabilities                                                                                                                                                        Subordinated liabilities 1 807 1 807 911 911
   SWED 2024-12-31     1    annual:2024-12-31  287                          Subordinated liabilities                                                                                                                                                    Subordinated liabilities 2 278 2 278 1 807 1 807
   SWED 2025-12-31     1    annual:2025-12-31  239                          Subordinated liabilities                                                                                                                                                    Subordinated liabilities 2 061 2 061 2 278 2 278
   INGA 2020-12-31     1    annual:2020-12-31  305                                  Interest expense                                                                  Interest income on non-trading derivatives (hedge accounting) 3,392 4,319 4,497 Interest expense on subordinated loans 612 660 711
   INGA 2021-12-31     1    annual:2021-12-31  319                                  Interest expense                                                                  Interest income on non-trading derivatives (hedge accounting) 2,361 3,392 4,319 Interest expense on subordinated loans 571 612 660
   INGA 2022-12-31     1    annual:2022-12-31  234                                  Interest expense                                                                  Interest income on non-trading derivatives (hedge accounting) 4,011 2,361 3,392 Interest expense on subordinated loans 648 571 612
   INGA 2023-12-31     1    annual:2023-12-31  250                                  Interest expense                                                                 Interest income on non-trading derivatives (hedge accounting) 10,682 4,011 2,361 Interest expense on subordinated loans 708 648 571
   INGA 2024-12-31     1    annual:2024-12-31  267                                  Interest expense                                                                    Interest income on financial assets at fair value through OCI 1,481 1,078 511 Interest expense on subordinated loans 753 708 648
   INGA 2025-12-31     1    annual:2025-12-31  261                                  Interest expense                                                                  Interest income on financial assets at fair value through OCI 1,790 1,481 1,078 Interest expense on subordinated loans 813 753 708
    ABN 2020-12-31     0    annual:2020-12-31  209                              Paid interest on AT1                                                                                                                               Paid interest on AT1 capital securities -117 -117 -117 Company Annual
    ABN 2021-12-31     0    annual:2021-12-31  267                              Paid interest on AT1                                                                                                                                                 Paid interest on AT1 capital securities -91 -91 -91
    ABN 2022-12-31     0    annual:2022-12-31  335                                  impact on equity                                                                         considered part of equity. The payment of interest on the AT1 capital securities had an impact on equity of EUR 91 million.
    ABN 2023-12-31     0    annual:2023-12-31  412                                  impact on equity                                                                             considered part of equity. The payment of interest on the AT1 Capital securities had a EUR 91 million impact on equity.
    ABN 2024-12-31     0    annual:2024-12-31  366                                   Interest on AT1                                                                                                                                                   Interest on AT1 capital securities -120 -120 -120
    ABN 2025-12-31     0    annual:2025-12-31  298                              Paid interest on AT1                                                                                                                                              Paid interest on AT1 capital securities -217 -217 -217
    KBC 2020-12-31     0    annual:2020-12-31  172           Coupon on additional tier-1 instruments                                                                                                                                     Coupon on additional tier-1 instruments 0 0 0 -50 0 -50 0 0 -50
    KBC 2021-12-31     0    annual:2021-12-31  271                              coupon is treated as                                                              • Additional tier-1 (AT1) instruments (these securities are classified as equity instruments under IAS 32 and the coupon is treated as
    KBC 2022-12-31     0    annual:2022-12-31  265                                 coupon is treated                                                                 • Additional tier-1 (AT1) instruments (these securities are classified as equity instruments under IAS 32 and the coupon is treated
    KBC 2023-12-31     0    annual:2023-12-31  268                                 coupon is treated                                                                 • Additional tier-1 (AT1) instruments (these securities are classified as equity instruments under IAS 32 and the coupon is treated
    KBC 2024-12-31     0    annual:2024-12-31  249           Coupon on additional tier-1 instruments                                                                                                                                     Coupon on additional tier-1 instruments 0 0 0 -84 0 -84 0 0 -84
    KBC 2025-12-31     0    annual:2025-12-31  254           Coupon on additional tier-1 instruments                                                                                                                     Coupon on additional tier-1 instruments (net of tax) 0 0 0 -114 0 -114 0 0 -114
   RABO 2020-12-31     0    annual:2020-12-31  136                               recognized directly                                                              and dividends paid on these instruments are recognized directly committed itself to a plan to sell the asset, and the sale is expected
   RABO 2021-12-31     0    annual:2021-12-31  157                               recognized directly                                                                                                                                         dividends paid on these instruments are recognized directly
   RABO 2022-12-31     0    annual:2022-12-31  156                     recognized directly in equity          dividends paid on these instruments are recognized directly in equity. The Consolidated Statement of Cash Flows presents the cash flows from operating, investing and financing activities
   RABO 2023-12-31     0    annual:2023-12-31  198                     recognized directly in equity                                                                                                                              dividends paid on these instruments are recognized directly in equity.
   RABO 2024-12-31     0    annual:2024-12-31  258                     recognized directly in equity                                                                                                                              dividends paid on these instruments are recognized directly in equity.
   RABO 2025-12-31     0    annual:2025-12-31  296                     recognized directly in equity       dividends paid on these instruments are recognized directly in equity. acquisitions and disposals of subsidiaries, investments in associates and property and equipment. Financing activities
    BNP 2020-12-31     0    annual:2020-12-31  170                  Remuneration on preferred shares                                                                                                                                                  Remuneration on preferred shares and undated super
    BNP 2021-12-31     0    annual:2021-12-31  186                  undated super subordinated notes                                                                                                                                    and undated super subordinated notes (412) (412) - - (412) (412)
    BNP 2022-12-31     0    annual:2022-12-31  182                  Remuneration on preferred shares                                                                                                                                                  Remuneration on preferred shares and undated super
    BNP 2023-12-31     0    annual:2023-12-31  180  Remuneration on undated super subordinated notes                                                                                                                    Remuneration on undated super subordinated notes (654) (654) - - (654) (3) (657)
    BNP 2024-12-31     0    annual:2024-12-31  196  Remuneration on undated super subordinated notes                                                                                                                                        Remuneration on undated super subordinated notes (743) (743)
    BNP 2025-12-31     0    annual:2025-12-31  206  Remuneration on undated super subordinated notes                                                                                                                                        Remuneration on undated super subordinated notes (822) (822)
    GLE 2023-12-31     0    annual:2025-12-31  551                     directly reduces the retained                                                                                                 other equity instruments, it does not affect the income statement but directly reduces the retained
    GLE 2024-12-31     0    annual:2025-12-31  551                     directly reduces the retained                                                                                                 other equity instruments, it does not affect the income statement but directly reduces the retained
    GLE 2025-12-31     0    annual:2025-12-31  551                     directly reduces the retained                                                                                                 other equity instruments, it does not affect the income statement but directly reduces the retained
    CAG 2024-12-31     0 half_year:2025-06-30   12                 undated deeply subordinated notes                                                                             R se e m m e u s n te e r r a 2 t 0 io 24 n of undated deeply subordinated notes at 2nd ‐ (247) ‐ ‐ (247) ‐ ‐ ‐ ‐ (247)
    CAG 2025-12-31     0    annual:2025-12-31  849 Remuneration of undated deeply subordinated notes                                                                                                                   Remuneration of undated deeply subordinated notes - (554) - - (554) - - - - (554)
    DBK 2020-12-31     0    annual:2020-12-31  261            Coupon on additional equity components                                                                                                    Coupon on additional equity components, before tax 0 0 (349)5 0 0 0 0 0 0 0 0 0 (349)5 0 0 (349)
    DBK 2021-12-31     0    annual:2021-12-31  220            Coupon on additional equity components                                                                                                        Coupon on additional equity components, before tax 0 0 (363) 0 0 0 0 0 0 0 0 (363) 0 0 (363)
    DBK 2022-12-31     0    annual:2022-12-31  239            Coupon on additional equity components                                                                                                        Coupon on additional equity components, before tax 0 0 (479) 0 0 0 0 0 0 0 0 (479) 0 0 (479)
    DBK 2023-12-31     0    annual:2023-12-31  246            Coupon on additional equity components                                                                                                        Coupon on additional equity components, before tax 0 0 (498) 0 0 0 0 0 0 0 0 (498) 0 0 (498)
    DBK 2024-12-31     0    annual:2024-12-31  421            Coupon on additional equity components                                                                                                        Coupon on additional equity components, before tax 0 0 (574) 0 0 0 0 0 0 0 0 (574) 0 0 (574)
    DBK 2025-12-31     0    annual:2025-12-31  460            Coupon on additional equity components                                                                                                        Coupon on additional equity components, before tax — — (761) — — — — — — — — (761) — — (761)
    CBK 2020-12-31     0    annual:2020-12-31  174                                    Dividends paid                                                                                                                                                                        Dividends paid on additional
    CBK 2021-12-31     0    annual:2021-12-31  156                                    Dividends paid                                                                                                                                                                        Dividends paid on additional
    CBK 2022-12-31     0    annual:2022-12-31  161                                    Dividends paid                                                                                                                                                                        Dividends paid on additional
    CBK 2023-12-31     0    annual:2023-12-31  274                                    Dividends paid                                                                                                                                                                        Dividends paid on additional
    CBK 2024-12-31     0    annual:2024-12-31  393                       Distributions to Additional                                                                                                                                                                         Distributions to Additional
    CBK 2025-12-31     0    annual:2025-12-31  292                            Payments to Additional                                                                                                                                                                              Payments to Additional
    SAN 2020-12-31     0    annual:2020-12-31  579                                     deducted from                                                                                                                                         associated with CCPP, is directly added to or deducted from
    SAN 2021-12-31     0    annual:2021-12-31  585                                     deducted from                                                                 more likely than not the obligation will have to be settled. In associated with CCPP, is directly added to or deducted from equity.
    SAN 2022-12-31     0    annual:2022-12-31  576                                     deducted from                                                                                                                                         associated with CCPP, is directly added to or deducted from
    SAN 2023-12-31     0    annual:2023-12-31  576                                     deducted from                                                                         Grupo Santander’s consolidated financial statements include all associated with CCPP, is directly added to or deducted from
    SAN 2024-12-31     0    annual:2024-12-31  617                                     deducted from                                                                                                                                 associated with CCPP, is directly added to or deducted from equity.
    SAN 2025-12-31     0    annual:2025-12-31  664                                     deducted from                                                                                                                                 associated with CCPP, is directly added to or deducted from equity.
   BBVA 2020-12-31     0    annual:2020-12-31   55                              recognized in equity                                                                                    (1) Remuneration in the year related to contingent convertible securities, recognized in equity (see Note 22.4).
   BBVA 2021-12-31     0    annual:2021-12-31   56                              recognized in equity                                                                                    (*) Remuneration in the year related to contingent convertible securities, recognized in equity (see Note 22.4).
   BBVA 2022-12-31     0    annual:2022-12-31   61                              recognized in equity                                                                                    (1) Remuneration in the year related to contingent convertible securities, recognized in equity (see Note 22.4).
   BBVA 2023-12-31     0    annual:2023-12-31   62                              recognized in equity                                                                          (2) Remuneration in the year related to perpetual contingent convertible securities, recognized in equity (see Note 22.4).
   BBVA 2024-12-31     0    annual:2024-12-31   64                              recognized in equity                                                                          (1) Remuneration in the year related to perpetual contingent convertible securities, recognized in equity (see Note 22.4).
   BBVA 2025-12-31     0    annual:2025-12-31   76                              recognized in equity                                                                          (1) Remuneration in the year related to perpetual contingent convertible securities, recognized in equity (see Note 22.4).
   CABK 2020-12-31     0    annual:2020-12-31  142                              charged to voluntary                               (5) Remuneration of AT1 capital instruments corresponding to 2020, totalling EUR 143 million, will be deemed to have been paid, with this amount charged to voluntary
   CABK 2021-12-31     0    annual:2021-12-31  150                              charged to voluntary                               (4) Remuneration of AT1 capital instruments corresponding to 2021, totalling EUR 244 million, will be deemed to have been paid, with this amount charged to voluntary
   CABK 2022-12-31     0    annual:2022-12-31  151                     charged to voluntary reserves                                                                                                                                                                      charged to voluntary reserves.
   CABK 2023-12-31     0    annual:2023-12-31  155                     charged to voluntary reserves                                                                                                                                                                      charged to voluntary reserves.
   CABK 2024-12-31     0    annual:2024-12-31 1219                            recognised in reserves                                                                                                                           issuances, in which the discretionary coupons are recognised in reserves.
   CABK 2025-12-31     0    annual:2025-12-31  984                            recognised in reserves                                                                                                          amortised Tier 1 issuances, in which the discretionary coupons are recognised in reserves.
    SAB 2020-12-31     0    annual:2020-12-31  189                                    Other reserves                                                                                               euros in 2020 (73,250 thousand euros in 2019) and is recognised under the heading “Other reserves” of
    SAB 2021-12-31     0    annual:2021-12-31  172                                    Other reserves                                                                                                                                                            “Other reserves” of consolidated equity.
    SAB 2022-12-31     0    annual:2022-12-31  174                                    Other reserves                                                                                                                                                            “Other reserves” of consolidated equity.
    SAB 2023-12-31     0    annual:2023-12-31  174                                    Other reserves                                                                                                thousand euros in 2023 (110,374 thousand euros in 2022) and is recognised under the “Other reserves”
    SAB 2024-12-31     0    annual:2024-12-31  172                                    Other reserves                                                                                                thousand euros in 2024 (115,391 thousand euros in 2023) and is recognised under the “Other reserves”
    SAB 2025-12-31     0    annual:2025-12-31  175                  consolidated statement of equity                                                                                                                         reserves” heading in the consolidated statement of equity (see Note 1.3.3).
    BKT 2020-12-31     0    annual:2020-12-31   92                               decreases in equity                                                                                                        considered an equity item, recognised in “Other increases or (-) decreases in equity” in the
    BKT 2021-12-31     0    annual:2021-12-31   82                               decreases in equity                                                                                                   recognised in “Other increases or (-) decreases in equity” in the consolidated statement of total
    BKT 2022-12-31     0    annual:2022-12-31   75                               decreases in equity                                                                                                   recognised in “Other increases or (-) decreases in equity” in the consolidated statement of total
    BKT 2023-12-31     0    annual:2023-12-31   77                               decreases in equity                                                                  recognised in 'Other increases or (-) decreases in equity' in the consolidated statement of total Gross dividend per share for the
    BKT 2024-12-31     0    annual:2024-12-31   75                               decreases in equity                                                                                            recognised in “Other increases or (-) decreases in equity” in the consolidated statement of total euros)
    BKT 2025-12-31     0    annual:2025-12-31   75                               decreases in equity                                                                                                   recognised in 'Other increases or (-) decreases in equity' in the consolidated statement of total
    UNI 2020-12-31     0    annual:2020-12-31   21                          shareholder remuneration                                                                                                            Dividends (or shareholder remuneration) (Note 3) - - - - (6,850) - - - - - - - - (6,850)
    UNI 2021-12-31     0    annual:2021-12-31  178                         recorded directly against                                                                                                                                                       recorded directly against the Group’s equity.
    UNI 2022-12-31     0    annual:2022-12-31  176                         recorded directly against                                                                                                                                                       recorded directly against the Group’s equity.
    UNI 2023-12-31     0    annual:2023-12-31  195                         recorded directly against                                                                                    consolidated balance sheet. The discretionary remuneration of the CoCos is recorded directly against the Group’s
    UNI 2024-12-31     0    annual:2024-12-31  184                         recorded directly against                                                                                                                                          the CoCos is recorded directly against the Group’s equity.
    UNI 2025-12-31     0    annual:2025-12-31  188                         recorded directly against                                                                                                                                           recorded directly against the Group’s shareholder equity.
    UCG 2020-12-31     0    annual:2020-12-31  166                                     150. Reserves                                                                     Any coupon paid, net of related taxes, reduces item “150. Reserves” (item “140. Reserves” in the Company financial statements).
    UCG 2021-12-31     0    annual:2021-12-31  204                                     150. Reserves                                                                     Any coupon paid, net of related taxes, reduces item “150. Reserves” (item “140. Reserves” in the Company financial statements).
    UCG 2022-12-31     0    annual:2022-12-31  260                                     150. Reserves                                                                     Any coupon paid, net of related taxes, reduces item “150. Reserves” (item “140. Reserves” in the Company financial statements).
    UCG 2023-12-31     0    annual:2023-12-31  290                                     150. Reserves                                                                     Any coupon paid, net of related taxes, reduces item “150. Reserves” (item “140. Reserves” in the Company financial statements).
    UCG 2024-12-31     0    annual:2024-12-31  419                                     150. Reserves                                                                     Any coupon paid, net of related taxes, reduces item “150. Reserves” (item “140. Reserves” in the Company financial statements).
    UCG 2025-12-31     0    annual:2025-12-31  416                                     150. Reserves                                                                     Any coupon paid, net of related taxes, reduces item “150. Reserves” (item “140. Reserves” in the Company financial statements).
    ISP 2020-12-31     0    annual:2020-12-31  769                      allocation to Other reserves                                                                             − allocation to Other reserves of the total net negative amount of 237,601,478 euro for the coupons paid to subscribers
    ISP 2021-12-31     0    annual:2021-12-31  810                      allocation to other reserves                                                                          − allocation to other reserves of the total net negative amount of 304,780,687 euro for the coupons paid to subscribers of
    ISP 2022-12-31     0    annual:2022-12-31  815                      allocation to other reserves                                                                          − allocation to other reserves of the total net negative amount of 300,085,408 euro for the coupons paid to subscribers of
    ISP 2023-12-31     0    annual:2023-12-31  812                      allocation to other reserves                                                                          − allocation to other reserves of the total net negative amount of 318,709,932 euro for the coupons paid to subscribers of
    ISP 2024-12-31     0    annual:2024-12-31 1016                      allocation to other reserves                                                                          − allocation to other reserves of the total net negative amount of 400,819,796 euro for the coupons paid to subscribers of
    ISP 2025-12-31     0    annual:2025-12-31  979                      allocation to other reserves                                                                      ‒ allocation to other reserves of the total net negative amount of 417,245,254 euro for the coupons paid to subscribers of the
   BAMI 2020-12-31     0    annual:2020-12-31  216                             posted as a reduction                                                                                    Any coupons paid, after taxes, are posted as a reduction of item “150. Reserves”, if and for the amount at which
   BAMI 2021-12-31     0    annual:2021-12-31  218                             posted as a reduction                                                                                    Any coupons paid, after taxes, are posted as a reduction of item “150. Reserves”, if and for the amount at which
   BAMI 2022-12-31     0    annual:2022-12-31  233                             posted as a reduction                                                                                    Any coupons paid, after taxes, are posted as a reduction of item “150. Reserves”, if and for the amount at which
   BAMI 2023-12-31     0    annual:2023-12-31  254                             posted as a reduction                                                                                    Any coupons paid, after taxes, are posted as a reduction of item “150. Reserves”, if and for the amount at which
   BAMI 2024-12-31     0    annual:2024-12-31  446                             posted as a reduction                                                                               Any coupons paid, after taxes, are posted as a reduction of item "150. Reserves", if and for the amount at which they
   BAMI 2025-12-31     0    annual:2025-12-31  410                             posted as a reduction                                                                               Any coupons paid, after taxes, are posted as a reduction of item "150. Reserves", if and for the amount at which they
    BPE 2020-12-31     0    annual:2020-12-31  668                interest on AT1 equity instruments                                                                                                                                                 - interest on AT1 equity instruments (13,125) - - -
    BPE 2021-12-31     0    annual:2021-12-31  669                interest on AT1 equity instruments                                                                                                                                                 - interest on AT1 equity instruments (25,159) - - -
    BPE 2022-12-31     0    annual:2022-12-31  583                interest on AT1 equity instruments                                                                                                                                                 - interest on AT1 equity instruments (38,284) - - -
    BPE 2023-12-31     0    annual:2023-12-31  751                interest on AT1 equity instruments                                                                                                                                                 - interest on AT1 equity instruments (51,409) - - -
    BPE 2024-12-31     0    annual:2024-12-31  840                interest on AT1 equity instruments                                                                                                                                                 - interest on AT1 equity instruments (85,318) - - -
    BPE 2025-12-31     0    annual:2025-12-31  774                interest on AT1 equity instruments                                                                                                                                                - interest on AT1 equity instruments (165,220) - - -
```

### E3c.1d at1_in_equity after step 3.7, bank x date (half year dates class_from_annual; supersedes E3b.2)

```
ref_date 2020-12-31 2021-06-30 2021-12-31 2022-06-30 2022-12-31 2023-06-30 2023-12-31 2024-06-30 2024-12-31 2025-06-30 2025-12-31 2026-06-30
bank_id                                                                                                                                     
LLOY              1          1          1          1          1          1          1          1          1          1          1          1
NWG               1          1          1          1          1          1          1          1          1          1          1          1
BARC              1          1          1          1          1          1          1          1          1          1          1          1
HSBA              1          1          1          1          1          1          1          1          1          1          1          1
SANUK             1          1          1          1          1          1          1          1          1          1          1          1
NDA               1          1          1          1          1          1          1          1          1          0          0          0
DNB               1          1          1          1          1          1          1          1          1          1          1          1
DANSKE            1          1          1          0          0          0          0          0          0          0          0          0
SEB               0          0          0          0          0          0          0          0          0          0          0          0
SHB               0          0          0          0          0          0          0          0          0          0          0          0
SWED              0          0          0          0          0          0          0          0          0          0          0          0
INGA              0          0          0          0          0          0          0          0          0          0          0          0
ABN               1          1          1          1          1          1          1          1          1          1          1          1
KBC               1          1          1          1          1          1          1          1          1          1          1          1
RABO              1          1          1          1          1          1          1          1          1          1          1          1
BNP               1          1          1          1          1          1          1          1          1          1          1          1
GLE                                                                                 1          1          1          1          1          1
CAG                                                                                                       1          1          1          1
DBK               1          1          1          1          1          1          1          1          1          1          1          1
CBK               1          1          1          1          1          1          1          1          1          1          1          1
SAN               0          0          0          0          0          0          0          0          0          0          0          0
BBVA              0          0          0          0          0          0          0          0          0          0          0          0
CABK              0          0          0          0          0          0          0          0          0          0          0          0
SAB               0          0          0          0          0          0          0          0          0          0          0          0
BKT               0          0          0          0          0          0          0          0          0          0          0          0
UNI               1          1          1          1          1          1          1          1          1          1          1          1
UCG               1          1          1          1          1          1          1          1          1          1          1          1
ISP               1          1          1          1          1          1          1          1          1          1          1          1
BAMI              1          1          1          1          1          1          1          1          1          1          1          1
BPE               1          1          1          1          1          1          1          1          1          1          1          1
BMPS              0          0          0          0          0          0          0          0          0          0          0          0
```

### E3c.1c class_from_annual rows per flag (instruction 03c B.4)

```
field       at1_coupon_in_pl  at1_in_equity
ref_date                                   
2021-06-30                28             29
2022-06-30                28             29
2023-06-30                28             29
2024-06-30                28             29
2025-06-30                30             31
2026-06-30                30             31
```

### E3c.2 rote before and after step 3.7, reported basis (pct)

```
                    before  after  change_pts                      status_after
bank_id date                                                                   
BBVA    2021-12-31   11.06  10.20       -0.86                     at1_liability
        2022-06-30   13.14  12.40       -0.74                     at1_liability
        2022-12-31   14.60  13.89       -0.71                     at1_liability
        2023-06-30   15.99  15.33       -0.66                     at1_liability
        2023-12-31   16.71  15.99       -0.72                     at1_liability
        2024-06-30   18.38  17.60       -0.78                     at1_liability
        2024-12-31   19.30  18.55       -0.75                     at1_liability
        2025-06-30   19.65  18.90       -0.75                     at1_liability
        2025-12-31   19.15  18.43       -0.72                     at1_liability
        2026-06-30   19.81  19.08       -0.73                     at1_liability
CABK    2021-12-31   19.76  18.83       -0.93                     at1_liability
        2022-06-30    8.39   7.50       -0.89                     at1_liability
        2022-12-31   10.10   9.26       -0.84                     at1_liability
        2023-06-30   11.99  11.16       -0.83                     at1_liability
        2023-12-31   15.15  14.28       -0.87                     at1_liability
        2024-06-30   17.14  16.24       -0.90                     at1_liability
        2024-12-31   17.51  16.70       -0.81                     at1_liability
        2025-06-30   18.42  17.62       -0.80                     at1_liability
        2025-12-31   17.28  16.46       -0.82                     at1_liability
        2026-06-30   17.84  17.01       -0.83                     at1_liability
SAB     2021-12-31    5.06   4.10       -0.96                     at1_liability
        2022-06-30    6.61   5.49       -1.12                     at1_liability
        2022-12-31    7.88   6.87       -1.01                     at1_liability
        2023-06-30    9.27   8.32       -0.95                     at1_liability
        2023-12-31   11.74  10.72       -1.02                     at1_liability
        2024-06-30   13.26  12.30       -0.96                     at1_liability
        2024-12-31   14.96  14.15       -0.81                     at1_liability
        2025-06-30   16.47  15.66       -0.81                     at1_liability
        2025-12-31   14.44  13.26       -1.18                     at1_liability
        2026-06-30   15.85  14.32       -1.53                     at1_liability
SAN     2021-12-31   11.90  11.07       -0.83                     at1_liability
        2022-06-30   13.17    NaN         NaN  missing_input:profit_to_ordinary
        2022-12-31   13.46  12.72       -0.74                     at1_liability
        2023-06-30   13.45    NaN         NaN  missing_input:profit_to_ordinary
        2023-12-31   14.76  14.11       -0.65                     at1_liability
        2024-06-30   15.38  14.64       -0.74                     at1_liability
        2024-12-31   15.64  14.87       -0.77                     at1_liability
        2025-06-30   16.25  15.50       -0.75                     at1_liability
        2025-12-31   16.51  15.79       -0.72                     at1_liability
        2026-06-30   18.12  17.41       -0.71                     at1_liability
```

### E3c.2 rote before and after step 3.7, underlying basis (pct)

```
                    before  after  change_pts                      status_after
bank_id date                                                                   
BBVA    2021-12-31   12.87  12.01       -0.86                     at1_liability
        2022-06-30   13.14  12.40       -0.74                     at1_liability
        2022-12-31   14.60  13.89       -0.71                     at1_liability
        2023-06-30   15.99  15.33       -0.66                     at1_liability
        2023-12-31   16.71  15.99       -0.72                     at1_liability
        2024-06-30   18.38  17.60       -0.78                     at1_liability
        2024-12-31   19.30  18.55       -0.75                     at1_liability
        2025-06-30   19.65  18.90       -0.75                     at1_liability
        2025-12-31   19.15  18.43       -0.72                     at1_liability
        2026-06-30   19.81  19.08       -0.73                     at1_liability
CABK    2021-12-31   28.51  27.59       -0.92                     at1_liability
        2022-06-30    9.57   8.69       -0.88                     at1_liability
        2022-12-31   10.26   9.42       -0.84                     at1_liability
        2023-06-30   12.09  11.27       -0.82                     at1_liability
        2023-12-31   15.18  14.31       -0.87                     at1_liability
        2024-06-30   17.15  16.25       -0.90                     at1_liability
        2024-12-31   17.51  16.70       -0.81                     at1_liability
        2025-06-30   18.42  17.62       -0.80                     at1_liability
        2025-12-31   17.28  16.46       -0.82                     at1_liability
        2026-06-30   17.84  17.01       -0.83                     at1_liability
SAB     2021-12-31    5.06   4.10       -0.96                     at1_liability
        2022-06-30    6.61   5.49       -1.12                     at1_liability
        2022-12-31    7.88   6.87       -1.01                     at1_liability
        2023-06-30    9.27   8.32       -0.95                     at1_liability
        2023-12-31   11.74  10.72       -1.02                     at1_liability
        2024-06-30   13.26  12.30       -0.96                     at1_liability
        2024-12-31   14.96  14.15       -0.81                     at1_liability
        2025-06-30   16.47  15.66       -0.81                     at1_liability
        2025-12-31   14.44  13.26       -1.18                     at1_liability
        2026-06-30   15.85  14.32       -1.53                     at1_liability
SAN     2021-12-31   12.94  12.11       -0.83                     at1_liability
        2022-06-30   13.17    NaN         NaN  missing_input:profit_to_ordinary
        2022-12-31   13.46  12.72       -0.74                     at1_liability
        2023-06-30   13.45    NaN         NaN  missing_input:profit_to_ordinary
        2023-12-31   14.76  14.11       -0.65                     at1_liability
        2024-06-30   15.38  14.64       -0.74                     at1_liability
        2024-12-31   15.64  14.87       -0.77                     at1_liability
        2025-06-30   16.82  16.06       -0.76                     at1_liability
        2025-12-31   17.06  16.33       -0.73                     at1_liability
        2026-06-30   18.12  17.41       -0.71                     at1_liability
```

### E3c.3 Every minority_interests row with status no_nci_line (value 0; SCE page cited, balance sheet page read)

```
bank_id   ref_date value                  doc sce_page  bs_page_no_nci_line value_as_printed                                                                                                                                                                                                                  snippet
  SANUK 2024-06-30     0 half_year:2024-06-30       55                   53            blank                                                                                                                                                                   capital instruments hedging translation earnings Total
  SANUK 2025-06-30     0 half_year:2025-06-30       53                   51            blank                                                                                                                                                                   capital instruments hedging translation earnings Total
  SANUK 2025-12-31     0    annual:2025-12-31      163                  161            blank                                                                                                                                                capital instruments Fair value hedging hedging translation earnings Total
  SANUK 2026-06-30     0 half_year:2026-06-30       55                   53            blank                                                                                                                                                                             capital hedging hedging translation earnings
    NDA 2024-06-30     0 half_year:2024-06-30       36                   35            blank                                                                                                                                      EURm capital1 equity tions hedges income plans option earnings Total holders equity
    NDA 2024-12-31     0    annual:2024-12-31      201                  200            blank 2024, EURm Note capital1 equity ope ra tions2,3,4 hedges2,4 in come2 plans option earn ings Total tal holders equity Cash flow from operating activities before changes in operating assets and liabilities 7,436 10,757
    NDA 2025-06-30     0 half_year:2025-06-30       35                   34            blank                                                                                                                                      EURm capital1 equity tions hedges income plans option earnings Total holders equity
    NDA 2025-12-31     0    annual:2025-12-31      198                  197            blank  2025, EURm Note capital1 equity ope rat ions2,3,4 hedges2,4 in come2 plans option earn ings Total tal holders equity Cash flow from operating activities before changes in operating assets and liabilities 7,880 7,436
    NDA 2026-06-30     0 half_year:2026-06-30       36                   35            blank                                                                                                                                      EURm capital1 equity tions hedges income plans option earnings Total holders equity
 DANSKE 2024-06-30     0 half_year:2024-06-30       32                   31            blank                                                                                              (DKK millions) capital reserve (OCI) earnings dividends Total (DKK millions) capital reserve (OCI) earnings dividends Total
 DANSKE 2024-12-31     0    annual:2024-12-31      126                  125            blank                                                                      (DKK millions) Share capital reserve value (OCI) earnings dividends Total (DKK millions) Share capital reserve value (OCI) earnings dividends Total
 DANSKE 2025-06-30     0 half_year:2025-06-30       32                   31            blank                                                                                  (DKK millions) capital reserve value (OCI) earnings dividends Total (DKK millions) capital reserve value (OCI) earnings dividends Total
 DANSKE 2025-12-31     0    annual:2025-12-31      138                  137            blank                                                                                              (DKK millions) capital reserve (OCI) earnings dividends Total (DKK millions) capital reserve (OCI) earnings dividends Total
 DANSKE 2026-06-30     0 half_year:2026-06-30       32                   31            blank                                                                                  (DKK millions) capital reserve value (OCI) earnings dividends Total (DKK millions) capital reserve value (OCI) earnings dividends Total
    SEB 2020-12-31     0    annual:2020-12-31      104                  103            blank                                                                                                                                               2020 Share capital3) OCA6) hedges operations plans earnings Total equity4)
    SEB 2021-12-31     0    annual:2021-12-31      116                  115            blank                                                                                                                                               2021 Share capital3) OCA5) hedges operations plans earnings Total equity4)
    SEB 2022-12-31     0    annual:2022-12-31      116                  115            blank                                                                                                                                               2022 Share capital3) OCA5) hedges operations plans earnings Total equity4)
    SEB 2023-12-31     0    annual:2023-12-31       83                   83            blank                                                                                                                               Loans to central banks 18 97,691 73,962 4,454 Share flow of foreign benefit Retained Total
    SEB 2024-12-31     0    annual:2024-12-31      195                  195            blank                                                                                                          Loans to central banks 17 4,825 97,691 Share flow of foreign benefit Retained Total 07. Report of the directors
    SEB 2025-12-31     0    annual:2025-12-31      209                  209            blank                                                                                               Loans to central banks 17 51,513 4,825 SEK m Share flow f oreign benefit Retained Total 05. Financial statements and notes
    SEB 2021-06-30     0 half_year:2021-06-30       24                   23            blank                                                                                                                                                              SEK m capital OCA2) hedges operations plans earnings Equity
    SEB 2022-06-30     0 half_year:2022-06-30       23                   22            blank                                                                                                                                                              SEK m capital OCA2) hedges operations plans earnings Equity
    SEB 2023-06-30     0 half_year:2023-06-30       23                   22            blank                                                                                                                                                              SEK m capital OCA2) hedges operations plans earnings Equity
    SEB 2024-06-30     0 half_year:2024-06-30       24                   23            blank                                                                                                                                                              SEK m capital OCA²⁾ hedges operations plans earnings Equity
    SEB 2025-06-30     0 half_year:2025-06-30       20                   19            blank                                                                                                                                                              SEK m capital OCA²⁾ hedges operations plans earnings Equity
    SEB 2026-06-30     0 half_year:2026-06-30       25                   24            blank                                                                                                                                                              SEK m capital OCA²⁾ hedges operations plans earnings Equity
```

### E3c.4 NO yields, every month of 2025 and 2026 (data/raw/yields/NO.csv)

```
 period  yield_pct                                    series             status  n_days
2025-01   3.908955 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      22
2025-02   3.892950 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      20
2025-03   4.052524 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      21
2025-04   3.916158 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      19
2025-05   4.026850 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      20
2025-06   3.991650 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      20
2025-07   3.912957 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      23
2025-08   3.911905 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      21
2025-09   3.985364 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      22
2025-10   4.009043 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      23
2025-11   4.073750 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      20
2025-12   4.153158 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      19
2026-01   4.174381 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      21
2026-02   4.218500 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      20
2026-03   4.334864 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      22
2026-04   4.386368 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      19
2026-05   4.446389 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      18
2026-06   4.302045 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      22
2026-07   4.372391 Norges Bank GOVT_GENERIC_RATES B.10Y.GBON monthly_from_daily      23
```

### E3c.5a rote against rote_reported at 2025-12-31, after step 3.7 (pct; no threshold)

```
bank_id  rote  rote_reported  difference_pts                           status
   BAMI 16.96          22.38           -5.42                               ok
   BARC 11.41          11.30            0.11                               ok
   BBVA 18.43          19.30           -0.87                    at1_liability
    BKT   NaN          20.03             NaN missing_input:minority_interests
   BMPS   NaN          22.40             NaN        missing_input:at1_coupons
    BNP 11.19          11.60           -0.41                 from_comparative
    BPE   NaN          20.05             NaN        missing_input:at1_coupons
   CABK 16.46          17.50           -1.04                    at1_liability
    CBK   NaN           8.70             NaN    missing_input:at1_instruments
    DBK 10.03          10.30           -0.27                               ok
    GLE  9.85          10.20           -0.35                               ok
   HSBA 13.32          13.30            0.02                               ok
   INGA 12.94          13.60           -0.66       at1_liability;coupon_in_pl
    KBC 15.68          16.00           -0.32                   at1_net_of_tax
   LLOY 12.06          12.90           -0.84                               ok
    NWG 19.16          19.20           -0.04                               ok
    SAB 13.26          14.30           -1.04                    at1_liability
    SAN 15.79          17.10           -1.31                    at1_liability
  SANUK   NaN          10.00             NaN missing_input:minority_interests
    UCG 18.46          19.20           -0.74                               ok
    UNI  9.58           9.80           -0.22                               ok
```

### E3c.5b BAMI and BMPS against their own RoTE at 2025-12-31 (decision 5; no entry error found)

Read from each bank's annual:2025-12-31 document. Amounts are EUR m; "ours" are the facts behind kpi.csv.

**BAMI (reported 22.38%, p21).** Definition, p45: "Group net profit (loss) for the year to shareholders' equity, determined by excluding the profit (loss) for the year, AT1 equity instruments, advances on dividends and intangible assets, net of the related tax effects". This is closing equity, not an average; the numerator is profit before AT1 coupons.

| item | bank (page) | ours | note |
|---|---|---|---|
| numerator | 2,081.987, profit for the year (p335) | 1,958.187 = 2,081.987 - coupons 123.8 (p557) | the bank does not deduct AT1 coupons |
| total equity 2025-12-31 | 15,585.163 (p335) | 15,585.16 | agrees |
| NCI 2025-12-31 / 2024-12-31 | 80.487 / 0.069 (p335) | 80.487 / 0.069 | agrees |
| AT1 | 1,787.145 / 1,608.773, "140. Equity instruments" (p335; p557 "outstanding 1,787.1") | 1,390.0 / 1,389.745, CC1 row 30 | accounting against regulatory amount |
| intangibles 2025-12-31 | 3,214.115 gross (p335); implied net of tax about 3,024 | 3,030.0, CC1 row 8 | agrees within 6 |
| denominator | not printed; implied 2,081.987 / 0.2238 = 9,303 | 11,547.51, average of 2024 and 2025 closing | |

Bridge from 16.96% to 22.38%: gross profit numerator +1.07 pts (18.03); closing rather than average equity, the average carrying the pre-Anima 2024 intangibles, +0.75 (18.78); accounting AT1 1,787 for regulatory 1,390, +0.70 (19.48); the year's profit excluded from equity and the interim dividend added back, +2.91 (22.39).

**BMPS (reported 22.4%, p14).** Definition, p15 and footnote 1: "Net profit (loss) for the year and the average between the tangible shareholders' equity at the end of year and that at the end of the previous year"; tangible equity is book Group shareholders' equity including profit, net of goodwill and other intangibles, and "the figure as at 31 December 2025 does not include the balances of the Mediobanca Group". The p14 footnote excludes Mediobanca from both numerator and denominator.

| item | bank (page) | ours | note |
|---|---|---|---|
| numerator | 2,749.9, parent company's net profit excluding Mediobanca (p13: "2,715.7 (34.2) 2,749.9") | 2,715.707 (p337) | the bank excludes Mediobanca's -34.2 |
| Group equity 2025-12-31 / 2024-12-31 | 27,961.2 / 11,649.0 (p14) | 30,209.68 - 2,248.475 = 27,961.2 / 11,649.282 - 0.336 | agrees |
| Mediobanca equity | 14,737.4 (p14) | included | consolidated only at 2025-12-31 |
| intangibles 2025-12-31 / 2024-12-31 | 3,336.130 / 156.066, "100. Intangible assets" (p336) | 6,415.81 / 125.258, CC1 row 8 | the regulatory deduction includes Mediobanca's |
| denominator | not printed; implied 2,749.9 / 0.224 = about 12,276, the average of 11,493 and about 13,060 (MPS excluding Mediobanca) | 16,534.54 | |

Bridge from 16.42% to 22.40%: profit excluding Mediobanca +0.21 pts; the rest is the denominator. Our 2025-12-31 tangible equity of 21,545 includes Mediobanca's 14,737 of equity, consolidated at year end only, less 6.4bn of regulatory intangibles; the bank's ex-Mediobanca figure is about 13,060. Since step 3.7, BMPS rote is blank (OPEN-34).

### E3c.6 rote for every bank at every date, reported (pct; a blank shows its status, mi: = missing_input:)

```
date                2021-12-31             2022-06-30             2022-12-31             2023-06-30             2023-12-31             2024-06-30             2024-12-31             2025-06-30             2025-12-31                2026-06-30
bank_id                                                                                                                                                                                                                                         
LLOY                     12.72                  10.48                  12.39                  14.03                  13.79                  13.88                  11.47                  11.91                  12.06                     13.50
NWG                       9.23                  10.08                  11.70                  14.61                  17.18                  17.23                  17.31                  18.26                  19.16                     21.00
BARC                     13.03                  10.27                  10.36                  11.99                   8.82                   8.26                  10.47                  11.55                  11.41                     12.25
HSBA                      7.62                   8.48                   9.20                  15.32                  14.48                  14.53                  14.92                  11.51                  13.32                     15.24
SANUK                     9.85  mi:minority_interests  mi:minority_interests  mi:minority_interests  mi:minority_interests  mi:minority_interests  mi:minority_interests                   6.97  mi:minority_interests                      6.43
NDA                      13.60     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity                  18.60                  17.45            mi:at1_coupons
DNB      mi:profit_to_ordinary  mi:profit_to_ordinary     mi:tangible_equity                  15.86                  15.96                  17.65                  16.82                  17.87                  16.83        mi:at1_instruments
DANSKE      mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity                  13.75                  13.42                     14.51
SEB                      14.27                  13.55                  13.41                  16.74                  18.37                  19.34                  16.01                  15.48                  13.85                     14.47
SHB                      10.85                  11.14                  11.11                  12.92                  14.34                  15.22                  12.68                  13.18                  12.06  mi:intangibles_deduction
SWED                     14.68                  13.60                  13.93                  18.36                  20.18     mi:tangible_equity                  18.01     mi:tangible_equity                  16.14     mi:minority_interests
INGA                      8.96                   7.38                   7.19                  11.54                  14.66                  13.93                  12.84                  12.68                  12.94                     13.80
ABN         mi:tangible_equity                   7.90                   8.75                  11.60                  12.17                  11.74                  10.27                   9.49                   8.88                      9.79
KBC                      12.68     mi:tangible_equity                  16.44                  18.80                  17.67                  15.21                  16.37                  16.49                  15.68                     16.03
RABO                      9.29                   7.39                   6.39                   8.40                   9.72  mi:profit_to_ordinary                  10.77  mi:profit_to_ordinary                   9.63                      9.32
BNP                       9.41                   9.99                   9.91                  11.73                  10.35                   9.51                  10.70                  10.61                  11.19                     12.46
GLE         mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity     mi:tangible_equity                   9.85                     10.70
CAG         mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:at1_instruments        mi:at1_instruments
DBK                       3.86                   4.59                   8.72                   8.28                   7.23                   5.72                   4.62                   8.24                  10.03                     10.60
CBK                       1.17                   5.58                   4.84                   6.10                   7.44                   7.81                   8.57                   8.34     mi:at1_instruments        mi:at1_instruments
SAN                      11.07  mi:profit_to_ordinary                  12.72  mi:profit_to_ordinary                  14.11                  14.64                  14.87                  15.50                  15.79                     17.41
BBVA                     10.20                  12.40                  13.89                  15.33                  15.99                  17.60                  18.55                  18.90                  18.43                     19.08
CABK                     18.83                   7.50                   9.26                  11.16                  14.28                  16.24                  16.70                  17.62                  16.46                     17.01
SAB                       4.10                   5.49                   6.87                   8.32                  10.72                  12.30                  14.15                  15.66                  13.26                     14.32
BKT         mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary  mi:minority_interests     mi:minority_interests
UNI                      22.89  mi:profit_to_ordinary                   3.95  mi:profit_to_ordinary                   3.97                   6.43                   8.94                   9.47                   9.58              mixed_family
UCG                       2.22                   2.83                  11.10                  14.73                  16.09                  17.92                  16.62                  17.67                  18.46        mi:at1_instruments
ISP             mi:at1_coupons  mi:profit_to_ordinary                   8.43  mi:profit_to_ordinary                  15.53                  16.39                  16.70                  17.43                  18.09                     17.99
BAMI                      4.71                   4.67                   5.62                   7.93                  10.73                  11.60                  15.39                  20.90                  16.96                     16.60
BPE         mi:tangible_equity  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons            mi:at1_coupons
BMPS            mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons            mi:at1_coupons
```

### E3c.6 rote for every bank at every date, underlying (pct; a blank shows its status, mi: = missing_input:)

```
date                2021-12-31             2022-06-30             2022-12-31             2023-06-30             2023-12-31             2024-06-30             2024-12-31             2025-06-30             2025-12-31                2026-06-30
bank_id                                                                                                                                                                                                                                         
LLOY                     15.42                  13.06                  13.68                  15.72                  14.65                  14.83                  12.56                  12.66                  12.39                     13.45
NWG                      12.37                  11.92                  12.71                  15.41                  16.95                  17.84                  18.23                  19.62                  18.90                     19.91
BARC                     14.71                  13.99                  13.06                  12.50                  10.81                  10.84                  10.72                  11.38                  12.14                     12.99
HSBA                      9.26                  10.47                  13.07                  16.25                  16.32                  16.26                  16.10                  16.94                  17.55                     18.04
SANUK                    12.55  mi:minority_interests  mi:minority_interests  mi:minority_interests  mi:minority_interests  mi:minority_interests  mi:minority_interests                   6.97  mi:minority_interests                      6.43
NDA                      13.60     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity                  18.60                  17.45            mi:at1_coupons
DNB      mi:profit_to_ordinary  mi:profit_to_ordinary     mi:tangible_equity                  15.86                  15.96                  17.65                  16.82                  17.87                  16.83        mi:at1_instruments
DANSKE      mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity     mi:tangible_equity                  13.75                  13.42                     14.51
SEB                      14.27                  13.55                  14.14                  17.49                  18.37                  19.34                  16.01                  15.48                  14.03                     14.66
SHB                      10.65                  10.24                  10.74                  13.10                  14.41                  15.52                  13.04                  13.44                  12.18  mi:intangibles_deduction
SWED                     14.68                  13.60                  13.93                  18.93                  20.69     mi:tangible_equity                  18.01     mi:tangible_equity                  16.14     mi:minority_interests
INGA                      8.96                   7.38                   7.19                  11.54                  14.66                  13.93                  12.84                  12.68                  12.94                     13.80
ABN         mi:tangible_equity                   7.19                  10.35                  13.18                  12.71                  12.25                  10.69                  10.07                   9.13                      9.80
KBC                      13.77     mi:tangible_equity                  17.43                  19.82                  18.32                  15.88                  16.84                  16.96                  16.52                     16.85
RABO                     10.29                   8.76                   7.84                   9.20                   9.05  mi:profit_to_ordinary                  10.88  mi:profit_to_ordinary                   9.34                      8.98
BNP                       9.79                  10.15                  10.38                  12.90                  13.01                  11.77                  11.18                  11.11                  11.78                     12.87
GLE         mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity     mi:tangible_equity                  10.53                     11.30
CAG         mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:at1_instruments        mi:at1_instruments
DBK                       7.47                   7.29                   8.97                   9.58                   9.20                   9.74                   8.93                   9.43                  10.62                     11.12
CBK                       1.17                   5.58                   4.84                   6.10                   7.44                   7.81                   8.57                   8.34     mi:at1_instruments        mi:at1_instruments
SAN                      12.11  mi:profit_to_ordinary                  12.72  mi:profit_to_ordinary                  14.11                  14.64                  14.87                  16.06                  16.33                     17.41
BBVA                     12.01                  12.40                  13.89                  15.33                  15.99                  17.60                  18.55                  18.90                  18.43                     19.08
CABK                     27.59                   8.69                   9.42                  11.27                  14.31                  16.25                  16.70                  17.62                  16.46                     17.01
SAB                       4.10                   5.49                   6.87                   8.32                  10.72                  12.30                  14.15                  15.66                  13.26                     14.32
BKT         mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary     mi:tangible_equity  mi:profit_to_ordinary  mi:minority_interests     mi:minority_interests
UNI                      31.50  mi:profit_to_ordinary                   3.95  mi:profit_to_ordinary                   3.97                   6.43                   8.94                   9.47                   9.58              mixed_family
UCG                       2.22                   2.60                  11.10                  14.73                  16.09                  17.92                  16.62                  17.67                  18.46        mi:at1_instruments
ISP             mi:at1_coupons  mi:profit_to_ordinary                   8.43  mi:profit_to_ordinary                  15.53                  16.39                  16.70                  17.43                  18.09                     17.99
BAMI                      6.66                   6.80                   7.00                   8.21                  11.49                  12.43                  17.56                  23.12                  17.25                     16.98
BPE         mi:tangible_equity  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons            mi:at1_coupons
BMPS            mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons  mi:profit_to_ordinary         mi:at1_coupons            mi:at1_coupons
```

### E3c.6b rote coverage (filled of bank-dates)

```
            count  size
basis                  
reported      218   310
underlying    218   310
```

## Tests run

```
$ .venv/Scripts/python.exe -m pytest -p socket --disable-socket -q
26 passed, 1 warning in 29.50s
$ .venv/Scripts/python.exe -m ruff check .
All checks passed!
```

New tests in this section: `test_one_offs.py::test_underlying`, `test_kpi.py::test_rote_hand`, `test_kpi.py::test_at1_liability` (3 cases since step 3.7, a reviewer change allowed by 03c C), `test_market.py::test_gbp_pence`, `test_yields.py::test_coverage` (unchanged; passes since step 3.7). Check 1: 10,936 of 10,936 report entries pass provenance.

## Fresh-clone check

Clone path `C:/bpbs3c`, at 56292fe.

```
$ git clone https://github.com/uty101/Bank-Performance-Benchmarking.git C:/bpbs3c
$ git log --oneline -1
56292fe section 3: open questions OPEN-34 and OPEN-35
$ uv venv --python 3.12
$ uv pip install -r requirements-lock.txt
$ uv pip install -e . --no-deps
$ .venv/Scripts/python.exe -m pytest -p socket --disable-socket -q
..........................                                               [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\_pytest\config\__init__.py:894
  C:\bpbs3c\.venv\Lib\site-packages\_pytest\config\__init__.py:894: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; socket
    self.import_plugin(arg, consider_entry_points=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
26 passed, 1 warning in 33.54s
```

## Runtime per step

- 3.0: about 25 minutes (decisions, 45 capital entries, KPI rerun).
- 3.1: URL search about 5 minutes per UK bank (5 in parallel); download of 120 documents about 30 minutes; entries about 8 to 13 minutes per bank and part (10 parts in parallel); merges about 2 minutes per bank.
- 3.2: URL search for 234 EU documents 15 to 48 minutes per group (4 in parallel); downloads about 40 minutes; entries 20 to 36 minutes per group of 2 or 3 banks (9 in parallel).
- 3.3: entered with 3.2; one off provenance and commit about 5 minutes.
- 3.4: market pull about 3 minutes; rote fixes and evidence about 30 minutes; fred pull failed after 3 attempts of 120 s.
- 3.5: at1_in_equity and fte entries 5 to 17 minutes per group (6 in parallel); one off verification 5 minutes; merges and recompute about 15 minutes.
- 3.6: yields pull under 1 minute.
- 3.7: coupon location and nci entries 3 to 11 minutes per group of banks (4 in parallel, after a usage limit pause); yields pull under 1 minute; merge with provenance about 3 minutes; recompute about 1.5 minutes.
- `scripts/run_all.py`: about 4 minutes.

## Deviations from PLAN.md

1. **Rule 4 stops.** (a) Session 3, step 3.4: `--stage fred` failed (read timeout, then the connection closed by fred.stlouisfed.org, 3 attempts); a diagnostic with a browser user agent was refused by this session's safety classifier and nothing more was tried. Instruction 03b B.1 replaced FRED. (b) Session 3b, step 3.6: Norges Bank's monthly series had no 2025-12; instruction 03c B.3 replaced it with the business-day mean, and `test_coverage` passes. (c) Session 3c, step 3.7: BMPS (every date) and NDA (2026-06-30) have no AT1 coupon charged to equity and no flag of 1, so at1_coupons and rote are blank there (OPEN-34). Every other step is done.
2. **GLEIF match rule.** GLEIF's `filter[entity.legalName]` is a text search ("Barclays" returns 396 records). The stage also filters entity status ACTIVE and legal address country GB, and keeps records whose legal name equals the universe name followed by `PLC`, case and spacing normalised. Each of the 5 UK banks then has exactly 1 record (Evidence E3.1c). Appending `PLC` is my reading of "exactly 1 active record per bank".
3. **Scope gate.** `8b_scope_gate` rows keep value_a, value_b and diff_rel, with threshold NaN and passed blank; `build_facts` no longer applies `scope_gate_failed`.
4. **lcr and nsfr from interim reports are `report` family** with status `p3_from_report`. A.1 item 2 says "family p3", but the source map has no p3 rule for lcr or nsfr, and the family comes from the source map (amendment 11).
5. **CBK seam 1.** The CBK p3 figures are printed in EUR bn to 1 decimal. cet1 at 2025-06-30 is 0.16% from EBA (flagged, not stopped; seam 1 is now 77 of 78 within 0.1% (E3.0d), as CBK and BKT are new).
6. **Underlying basis (Convention 4.8).** A one off's pre-tax amount is taken out of its own field and also out of pbt, pat and profit_owners (tax not adjusted), and an income component's effect also moves total_operating_income. "Fields not touched by one offs" are read as fields that neither hold the item nor total it. At EBA dates the amount (reporting currency) is converted to EUR at the year to date P&L rate for the eba row, status `fx_combined`.
7. **rote at EBA dates.** derived() builds profit_to_ordinary and tangible_equity as `eba+report` (eba first, report rows for at1_coupons and minority_interests) and compute_kpis accepts that family for these 2 quantities only (`EBA_MIXED` in bpb/kpi.py). At 2024-12-31 and 2025-06-30 the `report` family alone is also complete; rote there uses `eba+report`, matching the rest of the EBA series.
8. **income_fte, cost_fte and cost_customer** are now computed (they were `pending_section_3`), with the numerator converted to EUR at the P&L mean rate of its period (Section 5.2). PLAN 3.4 names only rote.
9. **Commit order.** The first step 3.2 merge loop stopped at NDA (1 provenance failure) but the merge tool had already written NDA's 51 rows; the SEB commit (bcecc34) therefore carries them, including the failing row. The failing NDA rows (shares_out 2020-12-31, own shares printed `11 .9` by the text layer) were removed and NDA committed in 865d866, with DNB and DANSKE after it. History was not rewritten. The tool now restores the file on a failed merge.
10. **Rows removed to keep B.1 and B.4 definitions** (listed in E3.2b): fte where only headcount is printed (OPEN-29); AT1 coupons printed only net of tax (OPEN-28); CAG at1_coupons 2024-06-30 (a comparative taken although the H1 2024 document was obtained); all 43 BMPS one offs (no reconciliation to an adjusted measure); SANUK's 10 operating-lease-depreciation rows (a reclassification with no profit effect, which NWG's list also leaves out); NDA shares_out 2020-12-31 and BMPS shares_out 2021-12-31 (text layer splits the number).
11. **Decimal marks.** `decimal_mark` = `,` was set in `report_urls.csv` for SAN half_year 2021-06-30 and UNI half_year 2021-06-30 and 2022-06-30 (Spanish documents printing `10.374` for 10,374).
12. **Document fallbacks (B.3, 02b B.9).** Taken from the next document's comparative column: SHB 2024-06-30 (H1 2024 PDF has no text layer), KBC 2021-06-30 (H1 2021 statements are images), BKT 2025-06-30 (H1 2025 report 403), GLE 2024-12-31 and 2024-06-30 (FY2020 to FY2024 and H1 2021 to H1 2024 not obtainable).
13. **New module `bpb/market.py`** (`in_price_ccy`, `load_prices`) holds the GBp rule tested by `test_gbp_pence`; no signature in kickoff 6.1 covers it.
14. **`report_urls.csv` re-sorted** by universe order, doc_type and period when the 354 new rows were added.
15. **mergers.csv.** Tesco Bank and Sainsbury's Bank are sized by gross lending (`size_basis` loans): no total assets are published (02b B.10 order). UK acquirer total assets are the report family's at the last 31 Dec or 30 Jun before completion.

16. **Flag fields (instruction 03b B.2).** `at1_in_equity` has kind `flag` in fields.yaml: value_as_printed is a phrase of the cited line, value is the entered 1 or 0, and provenance checks that the cited line is on the page (as the zero-cell rule of 02b B.4). The status decisions of 03b B.3 to B.5 (`at1_net_of_tax`, `headcount`, `no_nci_line`) are held in a new trailing column `decision_status` of report_entries.csv, blank for every other entry; `at1_liability` is set by the KPI code where at1_in_equity is 0.
17. **at1_liability rule (instruction 03b; replaced in step 3.7, Deviation 21).** Where at1_in_equity is 0 at a bank and date, every family's at1_coupons and at1_instruments row there is set to 0 (a report row is added where none exists). Danske's 2022 and Nordea's H1 2025 coupons, paid on equity AT1 before its redemption, are therefore 0 at dates flagged 0. For SAN, BBVA, CABK, SAB and BKT the coupons are charged to reserves, not interest expense (OPEN-32); the rule was applied as written.
18. **CAG at1_in_equity** at 2023-12-31 and 2024-06-30 left out: the comparative came from the H1 2025 report although that date's own document (CASA-only) was obtained, as for CAG's at1_coupons (Deviation 10).
19. **BMPS fte** at 2020-12-31, 2021-06-30, 2021-12-31 and 2022-06-30 failed provenance when re-entered under decision 4 (text layer) and were left out.
20. **Yields file format.** `data/raw/yields/{CC}.csv` holds the parsed rows (period, yield_pct, series), not the raw response; the exact URL and series of each file are in MANIFEST.json.

21. **Two AT1 rules (instruction 03c B.1).** `at1_rules` in bpb/kpi.py replaces `at1_liability_rule`: at1_in_equity 0 sets every family's at1_instruments row to 0 (status at1_liability); at1_coupon_in_pl 1 sets every family's at1_coupons row to 0 (status coupon_in_pl), adding a report row where none exists. at1_coupon_in_pl is 0 when any coupon of the year is charged to equity or reserves (Danske 2022 and Nordea 2025 had both kinds), so that the equity-charged amount, the field's definition, is still deducted.
22. **2026-06-30 flags from the 2025 annual report.** Decision 4 reads a half year date from "the annual report of the same year"; 2026 has none. Both flags at 2026-06-30 are copied from the 2025 annual report with status class_from_annual, since no H1 2026 report states a different classification (the agents read every half year report for that). Every flag value is the same as before the copy; only the citations changed. GLE (2021-06-30 to 2024-06-30) and CAG (2021-06-30 to 2024-06-30) keep their 03b citations, or stay absent, because their own annual reports for those years were not obtained or are not group scope. BKT's 2021-06-30 to 2024-06-30 at1_in_equity, absent before, are now filled from its annual reports.
23. **Weak citations for the value 1.** SEB, SHB, SWED, INGA and DANSKE (2023 to 2025) print no policy line naming the AT1 coupon; at1_coupon_in_pl 1 cites the interest expense note line for subordinated liabilities, which also holds Tier 2 interest. None of their statements of changes in equity has an AT1 coupon line.
24. **Citations from the parent company's notes or SCE.** ISP and BPE (separate notes of the AT1 issuer), BARC 2024 and 2025 (parent SCE; the consolidated row's label is not unique), ABN 2022 and 2023 (equity note of the company statements).
25. **SAN rote at 2022-06-30 and 2023-06-30 now blank.** The rolling 12 months need the H1 2022 coupon; the H1 2021 and H1 2022 documents are quarterly-style reports with no EPS note and no coupon figure (E3c.2). SAB's 2020 coupon was re-entered as 73,227 thousand from the EPS note (p79): the subordinated liabilities note's 73,250 repeats the 2019 amount.
26. **NO yields file.** `data/raw/yields/{CC}.csv` gains the columns `status` (ok, or monthly_from_daily for NO) and `n_days` (business days averaged); the other 10 countries' values are unchanged.

## Not verified

- **Société Générale** FY2020 to FY2024 and H1 2021 to H1 2024, and **Bankinter** H1 2021 to H1 2024 and H1 2025: not downloaded (bot challenge / 403 / no verified URL); their dates stay blank except the comparative fallbacks above.
- **Line mapping inside entries** was done by sub-agents working from `ENTRY_GUIDE.md`; I checked their check 2 to 5 output, the provenance of every row (100%) and the 2 hand checks, not each mapping choice. The choices they flagged are under Open questions.
- **One off placement.** Several banks' reconciliations do not name the income statement line; the field chosen for those items (named in Open questions 6) is a reading of the item's label.
- **H1 2021 to H1 2023 shares_out** for SEB, Sabadell and others where only gross shares are printed: entered as gross where the notes say no treasury shares are held.

## Open questions

1. **OPEN-34:** BMPS (no AT1 at all) and NDA at 2026-06-30 (no coupon charged to equity after the 2025 redemption) have no at1_coupons: 0 with a status, or missing as now. BMPS rote is blank at every date.
2. **OPEN-35:** the strict reading of "any amount" in 03c B.2 left these missing: SANUK at 2023-06-30, 2023-12-31 and 2024-12-31, DANSKE at 2023-06-30 and ABN at 2020-12-31 (comparative-period amounts only), and BKT at every date (a balance sheet NCI line of dashes). Should comparative blocks and dash-only lines count?
3. **INGA, SEB, SHB, SWED, DANSKE value 1** rests on the subordinated liabilities interest line (Deviation 23).
4. **rote against rote_reported** (E3c.5a): with the coupons now deducted, SAN, BBVA, CABK and SAB are 0.9 to 1.3 pts below their published figure; BAMI and BMPS are explained by definition differences (E3c.5b).
5. **As in session 3:** the UK leverage exposure break at 2022-06-30, SANUK's leverage exposure unit from 2022-06-30 to 2024-06-30, BARC deposits_customers to 2022-06-30 and BARC's gross shares_out.

## Files changed

`CLAUDE.md` (amendments 26, 27; rule 14 lifted for step 3.0), `decisions/section_2_review.md`, `decisions/OPEN.md`, `config/fields.yaml`, `config/source_map.yaml`, `bpb/checks.py`, `bpb/ingest.py`, `bpb/kpi.py`, `bpb/market.py` (new), `scripts/pull_data.py` (stages gleif, market, fred), `scripts/fetch_reports.py`, `scripts/run_all.py`, `scripts/merger_materiality.py`, `tests/test_kpi.py`, `tests/test_one_offs.py` (new), `tests/test_market.py` (new), `tests/test_yields.py` (new), `data/raw/yields/` (status and n_days columns, NO from daily), `decisions/data_sources.md`, `data/manual/universe.csv`, `data/manual/report_urls.csv`, `data/manual/report_entries.csv`, `data/manual/one_offs.csv`, `data/manual/mergers.csv`, `data/raw/report_manifest.csv`, `data/raw/report_text/`, `data/raw/gleif/`, `data/raw/market/`, `data/raw/MANIFEST.json`, `outputs/tables/kpi.csv`, `outputs/tables/checks.csv`.

## Reviewer reads

1. This file: Outcome, Deviations 1, 21, 22 and Open questions.
2. `decisions/OPEN.md`: OPEN-34 and OPEN-35.
3. Evidence E3c.1 (at1_coupon_in_pl), E3c.2 (Spanish rote before and after), E3c.3 (no_nci_line rows), E3c.6 (rote with blank statuses).
4. `bpb/kpi.py`: `at1_rules`, `AT1_RULES`.
5. E3c.4 (NO yields), E3c.5 (BAMI, BMPS and rote_reported).
