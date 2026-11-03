# Section 3

Outcome: **stopped under rule 4 at step 3.4.** The `fred` data pull failed (read timeout, then the connection closed by fred.stlouisfed.org, on all 3 attempts). Steps 3.0 to 3.3 are complete for all 31 banks; step 3.4 is complete except the FRED series (rote for every bank, market data for 27 tickers, both tests).

## Steps completed

- 3.0 apply section 2 review decisions (064a109)
- 3.1 UK banks: GLEIF LEIs, 120 UK documents, entries per bank: LLOY (5086b75), NWG (d93fb73), BARC (f4b3170), HSBA (a6b93fe), SANUK (c9bcd11); UK merger ratios (50de460)
- 3.2 B.1 fields for all 31 banks, 1 commit per bank in universe order: LLOY 0924116, NWG 0591a57, BARC bf9e651, HSBA 2f7271a, SANUK 56c14d8, NDA 865d866, DNB 327d768, DANSKE 18397e6, SEB bcecc34, SHB 8028bb3, SWED 6e0b668, INGA 640d117, ABN d99d18e, KBC d575921, RABO b9d7cb6, BNP b7a803c, GLE 42b2cd5, CAG 2c1db2c, DBK 2cae2d7, CBK 6f49f3b, SAN b96f026, BBVA d24ba1f, CABK 3d2b7d2, SAB 64b3ac0, BKT a21ee33, UNI 5bceead, UCG 95188d6, ISP 6ab7a50, BAMI 618fbb6, BPE f9c667a, BMPS 016249a (see Deviation 9 on the NDA, SEB order)
- 3.3 one offs and underlying KPIs (7f4b399)
- 3.4 rote and market data; fred pull failed, rule 4 stop (d4c41c9)
- open questions OPEN-27 to OPEN-30 (b1827f3)

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


### E3.3a one_offs.csv rows by bank

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


### E3.4a rote for every bank at every date, pct

**reported**

```
date     2021-12-31  2022-06-30  2022-12-31  2023-06-30  2023-12-31  2024-06-30  2024-12-31  2025-06-30  2025-12-31  2026-06-30
bank_id                                                                                                                        
ABN             NaN        7.90        8.75       11.60       12.17       11.74       10.27        9.49        8.88        9.79
BAMI           4.71         NaN        5.62        7.93       10.73       11.60       15.39       20.90       16.96       16.60
BARC          13.03       10.27       10.36       11.99        8.82        8.26       10.47       11.55       11.41       12.25
BBVA          11.98       14.20       15.86       17.53       18.11       20.04       20.98       21.17       20.47       21.27
BKT             NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
BMPS            NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
BNP            9.41        9.99        9.91       11.73       10.35        9.51       10.70       10.61       11.19       12.46
BPE             NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
CABK          22.17        8.68       10.87       13.00       16.55       18.88       19.25       20.30       19.16       19.74
CAG             NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
CBK            1.17        5.58        4.84        6.10        7.44        7.81        8.57        8.34         NaN         NaN
DANSKE          NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
DBK            3.86        4.59        8.72        8.28        7.23        5.72        4.62        8.24       10.03       10.60
DNB             NaN         NaN         NaN       15.86       15.96       17.65       16.82       17.87       16.83         NaN
GLE             NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN        9.85       10.70
HSBA           7.62        8.48        9.20       15.32       14.48       14.53       14.92       11.51       13.32       15.24
INGA            NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
ISP             NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
KBC           12.68         NaN       16.44       18.80       17.67       15.21       16.37       16.49         NaN         NaN
LLOY          12.72       10.48       12.39       14.03       13.79       13.88       11.47       11.91       12.06       13.50
NDA           13.60         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
NWG            9.23       10.08       11.70       14.61       17.18       17.23       17.31       18.26       19.16       21.00
RABO           9.29        7.39        6.39        8.40        9.72         NaN       10.77         NaN        9.63        9.32
SAB            4.93        6.49        8.44        9.83       12.61       14.45       16.52       19.20       16.23       18.44
SAN           12.80         NaN       14.62         NaN       16.01       16.53       16.91       17.45       17.88       19.52
SANUK          9.85         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
SEB             NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
SHB             NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
SWED            NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
UCG            2.22        2.83       11.10       14.73       16.09       17.92       16.62       17.67       18.46         NaN
UNI           22.89         NaN        3.95         NaN        3.97        6.43        8.94        9.47        9.58         NaN
```

**underlying**

```
date     2021-12-31  2022-06-30  2022-12-31  2023-06-30  2023-12-31  2024-06-30  2024-12-31  2025-06-30  2025-12-31  2026-06-30
bank_id                                                                                                                        
ABN             NaN        7.19       10.35       13.18       12.71       12.25       10.69       10.07        9.13        9.80
BAMI           6.66         NaN        7.00        8.21       11.49       12.43       17.56       23.12       17.25       16.98
BARC          14.71       13.99       13.06       12.50       10.81       10.84       10.72       11.38       12.14       12.99
BBVA          14.11       14.20       15.86       17.53       18.11       20.04       20.98       21.17       20.47       21.27
BKT             NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
BMPS            NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
BNP            9.79       10.15       10.38       12.90       13.01       11.77       11.18       11.11       11.78       12.87
BPE             NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
CABK          32.48       10.05       11.06       13.12       16.59       18.90       19.25       20.30       19.16       19.74
CAG             NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
CBK            5.54        6.14        5.21        6.33        7.51        7.86        8.58       10.19         NaN         NaN
DANSKE          NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
DBK            7.47        7.29        8.97        9.58        9.20        9.74        8.93        9.43       10.62       11.12
DNB             NaN         NaN         NaN       15.86       15.96       17.65       16.82       17.87       16.83         NaN
GLE             NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN       10.53       11.30
HSBA           9.26       10.47       13.07       16.25       16.32       16.26       16.10       16.94       17.55       18.04
INGA            NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
ISP             NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
KBC           14.45         NaN       17.43       19.82       18.32       15.88       16.84       16.96         NaN         NaN
LLOY          15.42       13.06       13.68       15.72       14.65       14.83       12.56       12.66       12.39       13.45
NDA           13.60         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
NWG           12.37       11.92       12.71       15.41       16.95       17.84       18.23       19.62       18.90       19.91
RABO          10.29        8.76        7.84        9.20        9.05         NaN       10.88         NaN        9.34        8.98
SAB            8.61       10.06        8.44        9.83       12.95       14.78       16.72       19.41       16.23       19.46
SAN           14.00         NaN       14.62         NaN       16.01       16.53       16.91       18.09       18.50       19.52
SANUK         12.55         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
SEB             NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
SHB             NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
SWED            NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
UCG            2.22        2.60       11.10       14.73       16.09       17.92       16.62       17.67       18.46         NaN
UNI           31.50         NaN        3.95         NaN        5.04        7.51        8.94        9.47        9.58         NaN
```

Blank reported rote by status:

```
status
missing_input:at1_coupons           44
missing_input:at1_instruments        6
missing_input:minority_interests     8
missing_input:profit_owners          2
missing_input:profit_to_ordinary    51
missing_input:tangible_equity       33
mixed_family                         1
```

### E3.4b rote against rote_reported at 2025-12-31 (pct; no threshold)

```
bank_id  rote  rote_reported  difference_pts
   BAMI 16.96          22.38           -5.42
   BARC 11.41          11.30            0.11
   BBVA 20.47          19.30            1.17
    BKT   NaN          20.03             NaN
   BMPS   NaN          22.40             NaN
    BNP 11.19          11.60           -0.41
    BPE   NaN          20.05             NaN
   CABK 19.16          17.50            1.66
    CBK   NaN           8.70             NaN
    DBK 10.03          10.30           -0.27
    GLE  9.85          10.20           -0.35
   HSBA 13.32          13.30            0.02
   INGA   NaN          13.60             NaN
    KBC   NaN          16.00             NaN
   LLOY 12.06          12.90           -0.84
    NWG 19.16          19.20           -0.04
    SAB 16.23          14.30            1.93
    SAN 17.88          17.10            0.78
  SANUK   NaN          10.00             NaN
    UCG 18.46          19.20           -0.74
    UNI  9.58           9.80           -0.22
```

### E3.4c Hand checks

```
#### LLOY: rote at 2025-12-31

  ref_date                 field family        value ccy                                                              locator status
2024-12-31           at1_coupons report 4.980000e+08 GBP c39a7befff281d349c5ccfe8a29db6cc6adb42ad29e335e72d282e0eaad2b602@219     ok
2024-12-31       at1_instruments report 6.170000e+09 GBP  3cd7dc96f380d7810aa10b87a7e0c34d8b67c5271ab13071fe7b8895f7132df0@37     ok
2024-12-31 intangibles_deduction report 5.679000e+09 GBP  3cd7dc96f380d7810aa10b87a7e0c34d8b67c5271ab13071fe7b8895f7132df0@37     ok
2024-12-31    minority_interests report 1.720000e+08 GBP c39a7befff281d349c5ccfe8a29db6cc6adb42ad29e335e72d282e0eaad2b602@218     ok
2024-12-31         profit_owners report 4.421000e+09 GBP c39a7befff281d349c5ccfe8a29db6cc6adb42ad29e335e72d282e0eaad2b602@216     ok
2024-12-31          total_equity report 4.588800e+10 GBP c39a7befff281d349c5ccfe8a29db6cc6adb42ad29e335e72d282e0eaad2b602@218     ok
2025-12-31           at1_coupons report 4.630000e+08 GBP 9c7eeb9f6877c6be1fe991f2f776ede30c65043fab5a3f32475e9bc59a7a9ace@216     ok
2025-12-31       at1_instruments report 5.947000e+09 GBP  7bdd2a718e77dbee96773774bcb6b1ec28b92221d0cd5db80f4d50e2a3afc436@25     ok
2025-12-31 intangibles_deduction report 5.996000e+09 GBP  7bdd2a718e77dbee96773774bcb6b1ec28b92221d0cd5db80f4d50e2a3afc436@25     ok
2025-12-31    minority_interests report 1.990000e+08 GBP 9c7eeb9f6877c6be1fe991f2f776ede30c65043fab5a3f32475e9bc59a7a9ace@215     ok
2025-12-31         profit_owners report 4.659000e+09 GBP 9c7eeb9f6877c6be1fe991f2f776ede30c65043fab5a3f32475e9bc59a7a9ace@213     ok
2025-12-31          total_equity report 4.786700e+10 GBP 9c7eeb9f6877c6be1fe991f2f776ede30c65043fab5a3f32475e9bc59a7a9ace@215     ok

profit_to_ordinary = profit_owners 4,659,000,000 (report) - at1_coupons 463,000,000 (report) = 4,196,000,000
tangible_equity 2024-12-31 = total_equity 45,888,000,000 (report) - minority_interests 172,000,000 - at1_instruments 6,170,000,000 - intangibles_deduction 5,679,000,000 = 33,867,000,000
tangible_equity 2025-12-31 = total_equity 47,867,000,000 (report) - minority_interests 199,000,000 - at1_instruments 5,947,000,000 - intangibles_deduction 5,996,000,000 = 35,725,000,000
average tangible_equity = (33,867,000,000 + 35,725,000,000) / 2 = 34,796,000,000.0
rote (hand) = 4,196,000,000 / 34,796,000,000.0 = 0.120589
kpi.csv:
   value    numerator  denominator family status
0.120589 4196000000.0 3.479600e+10 report     ok
difference = 7.59e-13

#### BBVA: rote at 2024-12-31

  ref_date                 field family        value ccy                                                              locator status
2023-12-31           at1_coupons report 3.450000e+08 EUR  806b2b1bebeca5b007265b8346d2b3d4e73d65594c027dca6fb52b36c4184c0e@62     ok
2023-12-31       at1_instruments    eba 6.033455e+09 EUR                                                         2420129@2024     ok
2023-12-31 intangibles_deduction    eba 1.421125e+09 EUR                                                         2420110@2024     ok
2023-12-31    minority_interests report 3.564000e+09 EUR  806b2b1bebeca5b007265b8346d2b3d4e73d65594c027dca6fb52b36c4184c0e@18     ok
2023-12-31         profit_owners    eba 7.987717e+09 EUR                                                         2420336@2024     ok
2023-12-31          total_equity    eba 5.512835e+10 EUR                                                         2421216@2024     ok
2024-12-31           at1_coupons report 3.880000e+08 EUR  f345f5556b89e26cd27d421b6f8993cfa24c52191326874dea39463843c0363d@64     ok
2024-12-31       at1_instruments    eba 6.023283e+09 EUR                                                         2520129@2025     ok
2024-12-31       at1_instruments report 5.638000e+09 EUR 5c70ff881de178cb8e0c0879404619d7e6d83aff9b66f67147a17a686ddb392c@325     ok
2024-12-31 intangibles_deduction    eba 1.553379e+09 EUR                                                         2520110@2025     ok
2024-12-31 intangibles_deduction report 1.553000e+09 EUR 5c70ff881de178cb8e0c0879404619d7e6d83aff9b66f67147a17a686ddb392c@324     ok
2024-12-31    minority_interests report 4.359000e+09 EUR  f345f5556b89e26cd27d421b6f8993cfa24c52191326874dea39463843c0363d@21     ok
2024-12-31         profit_owners    eba 1.004035e+10 EUR                                                         2520336@2025     ok
2024-12-31         profit_owners report 1.005400e+10 EUR  5a932fd4c871df1d940492611fd2055386a052b7c90cfc322d88866b5f54e3c0@22     ok
2024-12-31          total_equity    eba 5.982848e+10 EUR                                                         2521216@2025     ok
2024-12-31          total_equity report 6.001400e+10 EUR  5a932fd4c871df1d940492611fd2055386a052b7c90cfc322d88866b5f54e3c0@21     ok

profit_to_ordinary = profit_owners 10,040,349,000 (eba) - at1_coupons 388,000,000 (report) = 9,652,349,000
tangible_equity 2023-12-31 = total_equity 55,128,346,000 (eba) - minority_interests 3,564,000,000 - at1_instruments 6,033,455,000 - intangibles_deduction 1,421,125,000 = 44,109,766,000
tangible_equity 2024-12-31 = total_equity 59,828,484,000 (eba) - minority_interests 4,359,000,000 - at1_instruments 6,023,283,000 - intangibles_deduction 1,553,379,000 = 47,892,822,000
average tangible_equity = (44,109,766,000 + 47,892,822,000) / 2 = 46,001,294,000.0
rote (hand) = 9,652,349,000 / 46,001,294,000.0 = 0.209828
kpi.csv:
   value    numerator  denominator     family status
0.209828 9652349000.0 4.600129e+10 eba+report     ok
difference = 3.34e-11
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

None: the stage failed (Deviation 1); data/raw/fred/ is empty and MANIFEST.json has no fred entry.

## Tests run

```
$ .venv/Scripts/python.exe -m pytest -p socket --disable-socket -q
24 passed, 1 warning in 71.04s (0:01:11)
$ .venv/Scripts/python.exe -m ruff check .
All checks passed!
```

New tests: `tests/test_one_offs.py::test_underlying`, `tests/test_kpi.py::test_rote_hand`, `tests/test_market.py::test_gbp_pence`. The warning is the pytest-socket "module already imported" notice seen in every earlier section.

## Fresh-clone check

Clone path `C:/bpbs3`, at b1827f3 (the push before this review).

```
$ git clone https://github.com/uty101/Bank-Performance-Benchmarking.git C:/bpbs3
$ git log --oneline -1
b1827f3 section 3: open questions OPEN-27 to OPEN-30
$ uv venv --python 3.12
Using CPython 3.12.13
Creating virtual environment at: .venv
Activate with: .venv\Scripts\activate
$ uv pip install -r requirements-lock.txt
 + xlrd==2.0.2
 + yfinance==1.7.0
$ uv pip install -e . --no-deps
 + bpb==0.1.0 (from file:///C:/bpbs3)
$ .venv/Scripts/python -m pytest -p socket --disable-socket -q
........................                                                 [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\_pytest\config\__init__.py:894
  C:\bpbs3\.venv\Lib\site-packages\_pytest\config\__init__.py:894: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; socket
    self.import_plugin(arg, consider_entry_points=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
24 passed, 1 warning in 87.64s (0:01:27)
```

## Runtime per step

- 3.0: about 25 minutes (decisions, 45 capital entries, KPI rerun).
- 3.1: URL search about 5 minutes per UK bank (5 in parallel); download of 120 documents about 30 minutes; entries about 8 to 13 minutes per bank and part (10 parts in parallel); merges about 2 minutes per bank.
- 3.2: URL search for 234 EU documents 15 to 48 minutes per group (4 in parallel); downloads about 40 minutes; entries 20 to 36 minutes per group of 2 or 3 banks (9 in parallel).
- 3.3: entered with 3.2; one off provenance and commit about 5 minutes.
- 3.4: market pull about 3 minutes; rote fixes and evidence about 30 minutes; fred pull failed after 3 attempts of 120 s.
- `scripts/run_all.py`: about 4 minutes.

## Deviations from PLAN.md

1. **Rule 4 stop at step 3.4.** `scripts/pull_data.py --stage fred` failed for GB, the first series: `Read timed out (read timeout=120)`, then twice `RemoteDisconnected('Remote end closed connection without response')`. A diagnostic request with a browser user agent was refused by this session's safety classifier as bot-check circumvention, so nothing further was tried. `data/raw/fred/` is empty; the stage code is committed. Every other step of the section is done.
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

## Not verified

- **Société Générale** FY2020 to FY2024 and H1 2021 to H1 2024, and **Bankinter** H1 2021 to H1 2024 and H1 2025: not downloaded (bot challenge / 403 / no verified URL); their dates stay blank except the comparative fallbacks above.
- **Line mapping inside entries** was done by sub-agents working from `ENTRY_GUIDE.md`; I checked their check 2 to 5 output, the provenance of every row (100%) and the 2 hand checks, not each mapping choice. The choices they flagged are under Open questions.
- **One off placement.** Several banks' reconciliations do not name the income statement line; the field chosen for those items (named in Open questions 6) is a reading of the item's label.
- **H1 2021 to H1 2023 shares_out** for SEB, Sabadell and others where only gross shares are printed: entered as gross where the notes say no treasury shares are held.

## Open questions

1. **FRED.** Retry `--stage fred` from another network, or confirm a fixed host/user agent for fred.stlouisfed.org, so step 3.4 item 2 can finish.
2. **OPEN-27:** at1_coupons where AT1 is not equity (SEB, SHB, SWED, INGA; DANSKE from 2023; NDA 2026-06-30; BMPS): 0 with a status, or blank.
3. **OPEN-28:** AT1 coupons printed only net of tax (BKT, KBC 2025-12-31 and 2026-06-30, BAMI 2021-06-30; UCG possibly; ISP accrued in an own-funds note).
4. **OPEN-29:** fte where only headcount is printed (SAN, BBVA, CABK, SAB, BKT, ISP, BPE, BMPS, BAMI 30 Jun).
5. **OPEN-30:** SANUK profit_owners at 2025-12-31 and 2026-06-30, and the H1 2026 levy line.
6. **One off sources to confirm.** SAB "non-recurrent costs" (feeds its core results measure, no profit reconciliation); CBK restructuring and the 2020 goodwill impairment (below its operating result); BPE integration costs and PPA lines (its recurring net profit); GLE "main exceptional items" (no adjusted profit published); UNI 2023 bank levy (removed only from its RoTE ratios); DBK litigation 2020 to 2022 (excluded from adjusted costs, not then from adjusted PBT); ING's 2020 resilient-profit items (printed as net result adjustments); KBC exceptional cost items (cost/income measure only).
7. **Leverage exposure break for UK banks** at 2022-06-30: before it, the CRR measure including central bank claims; from it, UK KM1 row 13 excluding them (BARC, HSBA, NWG, SANUK; LLOY excludes them throughout).
8. **SANUK leverage exposure 2022-06-30 to 2024-06-30** is printed with a "£m" header but in £bn; entered at 1e9.
9. **BARC deposits_customers** to 2022-06-30 is "Deposits at amortised cost" (includes banks); **BARC shares_out** is gross (trust holdings printed only in £).

## Files changed

`CLAUDE.md` (amendments 26, 27; rule 14 lifted for step 3.0), `decisions/section_2_review.md`, `decisions/OPEN.md`, `config/fields.yaml`, `config/source_map.yaml`, `bpb/checks.py`, `bpb/ingest.py`, `bpb/kpi.py`, `bpb/market.py` (new), `scripts/pull_data.py` (stages gleif, market, fred), `scripts/fetch_reports.py`, `scripts/run_all.py`, `scripts/merger_materiality.py`, `tests/test_kpi.py`, `tests/test_one_offs.py` (new), `tests/test_market.py` (new), `data/manual/universe.csv`, `data/manual/report_urls.csv`, `data/manual/report_entries.csv`, `data/manual/one_offs.csv`, `data/manual/mergers.csv`, `data/raw/report_manifest.csv`, `data/raw/report_text/`, `data/raw/gleif/`, `data/raw/market/`, `data/raw/MANIFEST.json`, `outputs/tables/kpi.csv`, `outputs/tables/checks.csv`.

## Reviewer reads

1. This file: Deviations 1, 6, 7, 10 and Open questions.
2. `decisions/OPEN.md`, OPEN-27 to OPEN-30.
3. `bpb/kpi.py`: `underlying_facts`, `EBA_MIXED`, `_one_kpi`.
4. Evidence E3.4a to E3.4c (rote, comparison, hand checks).
5. `data/manual/one_offs.csv` for the banks in Open question 6.
