# Section 6

Section 6 is complete under instructions 06 and 06b. This file covers the whole section and replaces the version written at the stop.

## Steps completed

6.0 section 5 review decisions (37f943f)
6.1 31 profiles, league CSVs and HTML pages (735090e)
6.2 lineage tables, bpb trace and the dashboard (d4dcf83)
6.3 bpb build, answers.csv and the byte identical test (80f09f1)
6.4 README, METHODS, generated tables and answers.csv (43c346c)
6.5 MIT licence, project_outline rename, final spec_log stamp (0dcaffd), and removal of my dashboard test (77c368f)

## Evidence

### E6.0a: splits, prices either side, every P/TBV that changes, fits, stability, spec_log

```
ticker       date    ratio
BMPS.MI 2022-09-26 0.010000
  NWG.L 2022-08-30 0.928571
      date ticker   adjusted  unadjusted
2022-08-24  NWG.L 276.553802  256.799959
2022-08-25  NWG.L 272.353790  252.899948
2022-08-26  NWG.L 270.199890  250.899898
2022-08-30  NWG.L 249.000000  249.000000
2022-08-31  NWG.L 246.449997  246.449997
2022-09-01  NWG.L 242.899994  242.899994
      date  ticker  adjusted  unadjusted
2022-09-21 BMPS.MI  6.113580    0.061136
2022-09-22 BMPS.MI  6.163589    0.061636
2022-09-23 BMPS.MI  6.359457    0.063595
2022-09-26 BMPS.MI  6.359457    6.359457
2022-09-27 BMPS.MI  6.244854    6.244854
2022-09-28 BMPS.MI  6.230268    6.230268
price changes
      date bank_id  price_old  price_new  ptbv_old  ptbv_new
2021-12-31     NWG   2.430615   2.257000  0.866775  0.804863
2021-12-31    BMPS  18.586618   0.185866       NaN       NaN
ptbv changes
      date bank_id  ptbv_old  ptbv_new
2021-12-31     NWG  0.866775  0.804863
 year  n      beta  beta_se       r2  coe_implied  huber_beta cooks_named       status
 2021 22  1.047830 1.535046 0.094388          NaN    1.059015     CBK;UNI beta_ns_year
 2022 23  4.499947 1.718445 0.478576     0.242225    4.499947        BMPS           ok
 2023 25  4.526150 2.261670 0.399721     0.240938    5.872801        BMPS           ok
 2024 25  6.631913 1.230680 0.553407     0.170786    6.901687        BMPS           ok
 2025 25 10.433434 1.487395 0.740798     0.115846   10.770201        LLOY           ok
  n  n_banks   f_stat  df_num  df_denom  p_value
120       27 9.996745       4        26 0.000049
bank_id     ptbv  rote_gap_pts  uplift_ptbv  uplift_pooled_ptbv status
   INGA 1.435692     11.320586     1.181126            0.390935     ok
    ABN 1.045018     10.694187     1.115771            0.369304     ok
    SAN 1.677095      9.886008     1.031450            0.341395     ok
   LLOY 1.616911      9.031645     0.942311            0.311891     ok
   BMPS 1.287451      9.022351     0.941341            0.311570     ok
    BPE 1.699963      9.000751     0.939087            0.310824     ok
             run_utc       spec_id status
2026-11-04T15:54:13Z fit_year_2021     ok
2026-11-04T15:54:13Z fit_year_2022     ok
2026-11-04T15:54:13Z fit_year_2023     ok
2026-11-04T15:54:13Z fit_year_2024     ok
2026-11-04T15:54:13Z fit_year_2025     ok
2026-11-04T15:54:13Z    fit_pooled     ok
2026-11-04T15:54:13Z fit_stability     ok
['date', 'bank_id', 'basis', 'reference', 'driver', 'bank_value', 'ref_value', 'shapley_pts', 'other_below_line_pts', 'minorities_and_at1_pts', 'status']
status
ok               6592
missing_input    1504
too_few_peers    1024
rote_blank        416
merger_break      320
loss_year          64
```

yfinance also showed no split after the pull window, to 2026-11-03. The re-pull left all 40,266 prices equal to the committed ones, and `prices.parquet` unchanged.

The fix changes 1 P/TBV (NWG at 2021-12-31), which moves the 2021 fit only, and that fit's β stays not significant. BMPS's Cook's distance namings in 2022 to 2024 are unchanged.

### E6.0b: A.1 item 4, ISP and KBC lines between income and pbt, as printed

Sources: ISP annual report sha e29cff378441 page 388, ISP half year report sha 1c6ac5db2259 page 130, KBC annual report sha 8140183eb1d0 page 250, KBC quarterly report sha aa09c68c7770 page 14. EUR m.

```
===== ISP 2025-12-31 sha e29cff378441 page 388 annual
120. Net interest and other banking income 30,472 30,693 -221 -0.7
130. Net losses/recoveries for credit risk associated with: -1,843 -1,139 704 61.8
140. Profits (Losses) on changes in contracts without derecognition -30 -28 2 7.1
150. Net income from banking activities 28,599 29,526 -927 -3.1
160. Insurance service result 1,757 1,653 104 6.3
c) insurance revenue arising from reinsurance contracts held 70 99 -29 -29.3
d) insurance service expenses arising from reinsurance contracts held -145 -169 -24 -14.2
170. Balance of financial income and expenses related to insurance operations -5,306 -5,804 -498 -8.6
b) net financial expenses/revenue related to reinsurance contracts held 1 1 - -
180. Net income from banking and insurance activities 25,050 25,375 -325 -1.3
190. Administrative expenses: -11,364 -11,997 -633 -5.3
200. Net provisions for risks and charges -312 -667 -355 -53.2
210. Net adjustments to / recoveries on property and equipment -581 -647 -66 -10.2
220. Net adjustments to / recoveries on intangible assets -1,210 -1,111 99 8.9
230. Other operating expenses (income) 1,163 1,161 2 0.2
240. Operating expenses -12,304 -13,261 -957 -7.2
250. Profits (Losses) on investments in associates and companies subject to joint control -269 -32 237
260. Valuation differences on property, equipment and intangible assets measured at fair value -21 -23 -2 -8.7
270. Goodwill impairment - - -
280. Profits (Losses) on disposal of investments 189 -1 190
290. Income (Loss) before tax from continuing operations 12,645 12,058 587 4.9
===== ISP 2026-06-30 sha 1c6ac5db2259 page 130 half_year
120. Net interest and other banking income 17,768 14,614 3,154 21.6
130. Net losses/recoveries for credit risk associated with: -551 -645 -94 -14.6
140. Profits (Losses) on changes in contracts without derecognition -8 -9 -1 -11.1
150. Net income from banking activities 17,209 13,960 3,249 23.3
160. Insurance service result 983 900 83 9.2
c) insurance revenue arising from reinsurance contracts held 17 36 -19 -52.8
d) insurance service expenses arising from reinsurance contracts held -61 -77 -16 -20.8
170. Balance of financial income and expenses related to insurance operations -4,338 -1,882 2,456
b) net financial expenses/revenue related to reinsurance contracts held 1 1 - -
180. Net income from banking and insurance activities 13,854 12,978 876 6.7
190. Administrative expenses: -5,179 -5,065 114 2.3
200. Net provisions for risks and charges -57 -75 -18 -24.0
210. Net adjustments to / recoveries on property and equipment -272 -297 -25 -8.4
220. Net adjustments to / recoveries on intangible assets -568 -551 17 3.1
230. Other operating expenses (income) 496 558 -62 -11.1
240. Operating expenses -5,580 -5,430 150 2.8
250. Profits (Losses) on investments in associates and companies subject to joint control 22 3 19
260. value 1 - 1
270. Goodwill impairment - - -
280. Profits (Losses) on disposal of investments 1 57 -56 -98.2
290. Income (Loss) before tax from continuing operations 8,298 7,608 690 9.1
===== KBC 2025-12-31 sha 8140183eb1d0 page 250 annual
TOTAL INCOME 12 200 11 167
Operating expenses (excluding directly attributable to insurance contracts) 3.7 -4 706 -4 565
Insurance service expenses before reinsurance 3.6 -2 512 -2 475
Net result from reinsurance contracts held 3.6 -75 -17
Impairment 3.9 -334 -248
on financial assets at amortised cost and at fair value through OCI 3.9 -273 -199
on goodwill 3.9 -7 0
other 3.9 -53 -49
Share in the result of associates and joint ventures 3.10 6 80
RESULT BEFORE TAX 4 580 3 941
===== KBC 2026-06-30 sha aa09c68c7770 page 14 half_year
TOTAL INCOME 6 656 5 955 3 431 3 225 3 041
Operating expenses (excluding opex allocated
Insurance service expenses before reinsurance 3.6 -1 328 -1 230 - 683 - 644 - 608
Net result from reinsurance contracts held 3.6 - 42 - 24 - 14 - 27 - 15
Impairment 3.9 - 300 - 162 - 135 - 165 - 124
on FA at amortised cost and at FVOCI 3.9 - 231 - 155 - 66 - 164 - 116
on goodwill 3.9 0 0 0 0 0
other 3.9 - 70 - 8 - 69 - 1 - 8
Share in results of associated companies and
RESULT BEFORE TAX 2 264 2 022 1 473 791 1 275
```

Every entered line sits in the right field, so no entry was changed. The lines with no field reconcile to other_below_line:

```
bank       date  income  opex  llp   pbt  other_below_line  insurance  line_140  provisions  other_operating  associates_and_other  rounding
 ISP 2025-12-31   30472 13155 1843 12645              2829       3549        30         312            -1163                   101         0
 ISP 2026-06-30   17768  6019  551  8298              2900       3355         8          57             -496                   -24         0
 KBC 2025-12-31   12200  4706  273  4580              2641       2587         0           0                0                    55        -1
 KBC 2026-06-30    6656  2727  231  2264              1434       1370         0           0                0                    65        -1
```

Insurance is lines 160 and 170 for ISP, and insurance service expenses and reinsurance for KBC. So the size of other_below_line is the insurance effect, and the README says so.

### E6.0c: A.1 item 5, the waterfall date of every bank

```
bank waterfall_date status_at_latest
  LLOY     2026-06-30               ok
   NWG     2026-06-30               ok
  BARC     2026-06-30               ok
  HSBA     2026-06-30               ok
 SANUK     2025-12-31     merger_break
   NDA     2026-06-30               ok
   DNB     2025-12-31    missing_input
DANSKE     2026-06-30               ok
   SEB     2026-06-30               ok
   SHB     2025-12-31    missing_input
  SWED     2025-12-31    missing_input
  INGA     2026-06-30               ok
   ABN     2026-06-30               ok
   KBC     2026-06-30               ok
  RABO     2026-06-30               ok
   BNP     2026-06-30               ok
   GLE     2026-06-30               ok
   CAG            NaN    missing_input
   DBK     2026-06-30               ok
   CBK     2025-06-30    missing_input
   SAN     2026-06-30               ok
  BBVA     2026-06-30               ok
  CABK     2026-06-30               ok
   SAB     2026-06-30               ok
   BKT     2024-12-31    missing_input
   UNI     2025-12-31    missing_input
   UCG     2025-12-31    missing_input
   ISP     2026-06-30               ok
  BAMI     2026-06-30               ok
   BPE            NaN     merger_break
  BMPS     2025-06-30     merger_break
```

A blank date means no decomposition at any date. Those 2 panels state why.

### E6.1: outputs and profiles

```
folder  files    bytes
outputs/reports     32  1579404
outputs/figures     37  4472101
 outputs/tables    136 23384664
```

All 31 profiles are in `review/figures/section_6_contact.png`. Every bank has KPIs at 2026-06-30, so no header uses the fallback date. 102 league CSVs and 17 HTML pages exist.

`league_rote_cluster_2026-06-30.csv`:

```
rank bank_id                            name    value verdict inside_noise                                            status
  1.0     NWG                   NatWest Group 0.199090 leading        False                                                ok
  2.0    BBVA                            BBVA 0.190791 leading        False                                     family_switch
  3.0    BMPS Banca Monte dei Paschi di Siena 0.187050 in_line         True                                     family_switch
  4.0    HSBA                   HSBC Holdings 0.180439 leading        False                                     short_history
  5.0     ISP                 Intesa Sanpaolo 0.179911 in_line         True                                     family_switch
  6.0     NDA                     Nordea Bank 0.175516 in_line         True                                     short_history
  7.0     SAN                 Banco Santander 0.174129 in_line         True                                     family_switch
  8.0    CABK                       CaixaBank 0.170132 in_line         True                                     family_switch
  9.0    BAMI                       Banco BPM 0.169794 in_line         True                                     family_switch
 10.0     KBC                       KBC Group 0.168534 in_line         True                                     family_switch
 11.0     SEB   Skandinaviska Enskilda Banken 0.146618 lagging        False                                     family_switch
 12.0  DANSKE                     Danske Bank 0.145096 lagging        False                                     family_switch
 13.0     SAB                  Banco Sabadell 0.143166 lagging        False                                     family_switch
 14.0    INGA                       ING Groep 0.138017 lagging        False                                     family_switch
 15.0    LLOY            Lloyds Banking Group 0.134501 lagging        False                                                ok
 16.0    BARC                        Barclays 0.129936 in_line         True                                     short_history
 17.0     BNP                     BNP Paribas 0.128684 in_line         True                                     family_switch
 18.0     GLE                Société Générale 0.113007 lagging        False                                     short_history
 19.0     DBK                   Deutsche Bank 0.111167 lagging        False                                     family_switch
 20.0     ABN                   ABN AMRO Bank 0.097979 lagging        False                                     family_switch
 21.0    RABO                        Rabobank 0.089778 lagging        False                                     family_switch
 22.0   SANUK     Santander UK Group Holdings 0.064330 lagging        False                                                ok
  NaN     BKT                       Bankinter      NaN     NaN          NaN                        mixed_family;short_history
  NaN     BPE                      BPER Banca      NaN     NaN          NaN           missing_input:at1_coupons;short_history
  NaN     CAG           Crédit Agricole Group      NaN     NaN          NaN       missing_input:at1_instruments;short_history
  NaN     CBK                     Commerzbank      NaN     NaN          NaN       missing_input:at1_instruments;short_history
  NaN     DNB                        DNB Bank      NaN     NaN          NaN       missing_input:at1_instruments;family_switch
  NaN     SHB           Svenska Handelsbanken      NaN     NaN          NaN missing_input:intangibles_deduction;family_switch
  NaN    SWED                        Swedbank      NaN     NaN          NaN    missing_input:minority_interests;family_switch
  NaN     UCG                       UniCredit      NaN     NaN          NaN       missing_input:at1_instruments;family_switch
  NaN     UNI                   Unicaja Banco      NaN     NaN          NaN                        mixed_family;family_switch
```

`league_cost_income.html` (static, no JavaScript), first 1,500 characters:

```
<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Cost to income league table</title><style>body{font-family:Helvetica,Arial,sans-serif;margin:24px;color:#222}table{border-collapse:collapse;margin:0 0 24px}th,td{padding:3px 10px;border-bottom:1px solid #ccc;text-align:left;font-size:14px}td.n{text-align:right}h2{font-size:17px;margin-bottom:6px}</style></head><body><h1>Cost to income league table</h1><p>Underlying basis, best first. Each verdict is against the bank's own peers in the group, so a cluster table holds banks from every cluster.</p><h2>Cluster group at 2025-12-31</h2><table><tr><th>Rank</th><th>Bank</th><th>Value</th><th>Verdict</th><th>Inside noise</th><th>Status</th></tr><tr><td class="n">1</td><td>Bankinter</td><td class="n">36.09%</td><td>leading</td><td>False</td><td>family_switch</td></tr><tr><td class="n">2</td><td>KBC Group</td><td class="n">37.75%</td><td>leading</td><td>False</td><td>family_switch</td></tr><tr><td class="n">3</td><td>DNB Bank</td><td class="n">38.03%</td><td>leading</td><td>False</td><td>family_switch</td></tr><tr><td class="n">4</td><td>BBVA</td><td class="n">38.81%</td><td>leading</td><td>False</td><td>family_switch</td></tr><tr><td class="n">5</td><td>CaixaBank</td><td class="n">39.43%</td><td>leading</td><td>False</td><td>family_switch</td></tr><tr><td class="n">6</td><td>Swedbank</td><td class="n">40.03%</td><td>in_line</td><td>True</td><td>family_switch</td></tr><tr><td class="n">7</td><td>Banco Santander</td><td cl
```

### E6.2: the 20 sampled rows, and the trace of 3 (each cut at 2,200 characters)

```
bank_id          kpi         value family
   INGA cost_of_risk      0.001663 report
    SAN   income_fte 309592.437500 report
    SAN   cet1_ratio      0.140153     p3
    DNB  cost_assets      0.009145 report
    BNP  cost_income      0.597522 report
   SWED          lcr      1.616400 report
    NWG   ppp_assets      0.011976 report
   HSBA     cost_fte 140818.859000 report
    SEB          lcr      1.252700 report
   BMPS   cet1_ratio      0.163432     p3
    NWG          lcr      1.400000 report
 DANSKE         rote      0.145096 report
    BNP    fee_share      0.233573 report
    NDA  cost_income      0.462373 report
   INGA   ppp_assets      0.009920 report
   BMPS   income_fte 314669.544900 report
    ABN  cost_assets      0.012704 report
    ABN   ppp_assets      0.008221 report
    SAN          nim      0.029412 report
    DBK          nim      0.017148 report

$ bpb trace af7b420598d3
kpi af7b420598d3  INGA 2026-06-30 cost_of_risk underlying  value 0.001662582979
  facts 0f9d9f7d73e4  INGA 2025-12-31 impairments_fin   value 1304000000.0
    https://www.ing.com/binaries/content/assets/documents/annual-reports/2025-ing-groep-nv-annual-report.pdf
    sha256 a515adb27ab588ad3bef48da4afca1e9485a83869848a265e60ba954a0f5e4ea, page 219
    snippet: Interest income using effective interest rate method 43,481 49,220 44,486 Addition to loan loss provisions 1,304 1,194 520
  facts 1c92d6637f1b  INGA 2025-06-30 impairments_fin   value 612000000.0
    https://www.ing.com/binaries/content/assets/documents/files/1h2025_interim_accounts_ing_groep_n.v.pdf
    sha256 6f655069ab598f79e63494ec6971a93addfc0f8321ad25336d2cc86db1d1cc78, page 27
    snippet: Interest income using effective interest rate method 21,949 24,962 Addition to loan loss provisions 612 559
  facts 7d4b0c4f1e11  INGA 2026-06-30 loans_customers_gross   value 832018000000.0
    https://www.ing.com/binaries/content/assets/documents/results/2q2026/2q2026-ing-group-additional-pillar-iii-report.pdf
    sha256 198bf9c4c9505c770b7d3c63382328caba653ee59e2d286a65cf1dbbc5a6c804, page 23
    snippet: component 1/8: General governments 25,653 24,675 313 204 204 -9 -6 -3 -11 -11 8,307 184
  facts 7d4b0c4f1e11  INGA 2026-06-30 loans_customers_gross   value 832018000000.0
    https://www.ing.com/binaries/content/assets/documents/results/2q2026/2q2026-ing-group-additional-pillar-iii-report.pdf
    sha256 198bf9c4c9505c770b7d3c63382328caba653ee59e2d286a65cf1dbbc5a6c804, page 23
    snippet: component 2/8: General governments 25,653 24,675 313 204 204 -9 -6 -3 -11 -11 8,307 184
  facts 7d4b0c4f1e11  INGA 2026-06-30 loans_customers_gross   value 832018000000.0
    https://www.ing.com/binaries/content/assets/documents/results/2q2026/2q2026-ing-group-additional-pillar-iii-report.pdf
    sha256 198bf9c4c9505c770b7d3c63382328caba653ee59e2d286a65cf1dbbc5a6c804, page 23
    snippet: component 3/8: Other financial corporations 115,107 55,307 2,628 370 370 -29 -14 -15 -163 -163 91,150 44
  facts 7d4b0c4f1e11  INGA 2026-06-30 loans_customers_gross   value 832018000000.0
    https://www.ing.com/binaries/content/assets/docu

$ bpb trace 1ee68278b98e
kpi 1ee68278b98e  SAN 2026-06-30 income_fte underlying  value 309592.4375
  facts 111fc4568bc4  SAN 2026-06-30 fte   value 185279.0
    https://www.santander.com/content/dam/santander-com/en/documentos/informacion-sobre-resultados-semestrales-y-anuales-suministrada-a-la-sec/2026/sec-half-yearly-6-k-2026-fiscal-year-en.pdf
    sha256 d072554d21c19db1dd4e28a12236b4cd10b84ae618a7f4d0b53e9b698ccc1be6, page 7
    snippet: Number of employees 185,279 185,243 0.0 185,279 193,678 (4.3) 187,539
  facts 18b19eb084df  SAN 2025-12-31 total_operating_income   value 58670000000.0
    https://www.santander.com/content/dam/santander-com/en/documentos/informe-financiero-anual/2025/ifa-2025-consolidated-annual-financial-report-en.pdf
    sha256 b02503bc72b3fd115386eca4e4467340d49b576253e8eb0d973de7fcfe118bf9, page 625
    snippet: Total income 58,670 58,380 54,251
  facts 2911e08f6dc7  SAN 2026-06-30 total_operating_income   value 30822000000.0
    https://www.santander.com/content/dam/santander-com/en/documentos/informacion-sobre-resultados-semestrales-y-anuales-suministrada-a-la-sec/2026/sec-half-yearly-6-k-2026-fiscal-year-en.pdf
    sha256 d072554d21c19db1dd4e28a12236b4cd10b84ae618a7f4d0b53e9b698ccc1be6, page 99
    snippet: Total income 30,822 28,978
  facts 57f897aed80e  SAN 2025-06-30 total_operating_income   value 29182000000.0
    https://www.santander.com/content/dam/santander-com/en/documentos/informacion-sobre-resultados-semestrales-y-anuales-suministrada-a-la-sec/2025/sec-half-yearly-6-k-2025-fiscal-year-en.pdf
    sha256 5b3e8b579199b53ccf281d55b81763de8e166dd38c983287f4428a788b1763c6, page 104
    snippet: Total income 29,182 29,035
  facts e5e589ca4728  SAN 2025-06-30 fte   value 204330.0
    https://www.santander.com/content/dam/santander-com/en/documentos/informacion-sobre-resultados-semestrales-y-anuales-suministrada-a-la-sec/2025/sec-half-yearly-6-k-2025-fiscal-year-en.pdf
    sha256 5b3e8b579199b53ccf281d55b81763de8e166dd38c983287f4428a788b1763c6, page 7
    snippet: Number of employees 204,330 207,137 (1.4) 204,330 209,553 (2.5) 206,753

$ bpb trace 5004a020670a
kpi 5004a020670a  BNP 2026-06-30 cost_income underlying  value 0.5975217819
  one_off 2bceb521bddc  BNP 2025-06-30 admin_expenses   value 84000000.0
    https://invest.bnpparibas/en/document/2nd-amendment-to-the-2024-universal-registration-document-and-annual-financial-report
    sha256 4a9e520c9d8224f9e914dd6fde8f09fc7e50df73d8c1464a5e519a3db8d9301e, page 49
    snippet: Restructuring costs and adaptation costs (Corporate Centre) -84 -79
  one_off 2bceb521bddc  BNP 2025-06-30 admin_expenses   value 171000000.0
    https://invest.bnpparibas/en/document/2nd-amendment-to-the-2024-universal-registration-document-and-annual-financial-report
    sha256 4a9e520c9d8224f9e914dd6fde8f09fc7e50df73d8c1464a5e519a3db8d9301e, page 49
    snippet: IT reinforcement costs (Corporate Centre) -171 -172
  facts 4cc21143a8ae  BNP 2025-12-31 admin_expenses   value 29003000000.0
    https://invest.bnpparibas/en/document/universal-registration-document-annual-financial-report-2025-pdf
    sha256 65822993e7ad299d84f16bd4b495391bb670800bb9a0f301ef72e97b6f62a2e2, page 202
    snippet: Operating expenses 2.f (29,003) (27,803)
  facts 52e66f732162  BNP 2025-12-31 total_operating_income   value 51223000000.0
    https://invest.bnpparibas/en/document/universal-registration-document-annual-financial-report-2025-pdf
    sha256 65822993e7ad299d84f16bd4b495391bb670800bb9a0f301ef72e97b6f62a2e2, page 202
    snippet: REVENUES 51,223 48,831
  facts 52eb7e24f6b2  BNP 2025-06-30 depreciation   value 1145000000.0
    https://invest.bnpparibas/en/document/2nd-amendment-to-the-2024-universal-registration-document-and-annual-financial-report
    sha256 4a9e520c9d8224f9e914dd6fde8f09fc7e50df73d8c1464a5e519a3db8d9301e, page 76
    snippet: (1,145) (1,167)
  facts 5ae510146593  BNP 2026-06-30 depreciation   value 1195000000.0
    https://invest.bnpparibas/en/document/2nd-amendment-to-the-2025-universal-registration-document-and-annual-financial-report
    sha256 213831e3a723521ec48a99b12e19ce009ce9c97933c3a53f85240be98cba3969, page 38
    snippet: (1,195) (1,145)
  facts 727e34b17b5c  BNP 2025-06-30 total_operating_income   value 25541000000.0
    https://invest.bnpparibas/en/document/2nd-amendment-to-the-20
```

### E6.2b: dashboard smoke run, outside pytest

```
LLOY: exceptions 0 expanders 48 ['KPIs', '5 year trends', 'Sized gaps (EUR m, annual profit)', 'Shapley waterfall at 2026-06-30', 'Valuation']
CAG : exceptions 0 expanders 37 ['KPIs', '5 year trends', 'Sized gaps (EUR m, annual profit)', 'Shapley waterfall', 'Valuation']
SWED : exceptions 0 expanders 47 ['KPIs', '5 year trends', 'Sized gaps (EUR m, annual profit)', 'Shapley waterfall at 2025-12-31', 'Valuation']
market, reported, 2024-12-31: exceptions 0 expanders 46
```

### E6.3: build

`test_build_twice_identical` passed in the fresh clone and on CI (see below). `bpb build` in a fresh clone of 0dcaffd, then `git status --porcelain`, which printed nothing:

```
facts 27488 rows, kpi 11780 rows, checks 40742 rows
peers 93 rows, bench 31620 rows
gaps 5580 rows
drivers 9920 rows, yoy 992 rows
valuation 140 rows
profiles, league tables and answers written
build exit 0
git status after build:
end of git status
```

The same check on the final commit is in the fresh clone check below.

### E6.4: README, 14388 bytes

```
# Bank Performance Benchmarking

[![ci](https://github.com/uty101/Bank-Performance-Benchmarking/actions/workflows/ci.yml/badge.svg)](https://github.com/uty101/Bank-Performance-Benchmarking/actions/workflows/ci.yml) 62 tests

This project benchmarks 31 European banks against peers with a similar business model, sizes each gap in euros and RoTE points, and explains it with 7 drivers.
<!-- table:headline start -->
At 2026-06-30 the largest joint gap to the best quartile is CAG's, EUR 19,852m a year, and a point of RoTE added 0.104x of price to tangible book at the end of 2025, against 0.045x at the end of 2022.
<!-- table:headline end -->

See `outputs/reports/` for the 31 bank profiles, `outputs/tables/` for every table, and run `streamlit run bpb/dashboard.py` for the dashboard.

## What it does

It joins EBA transparency data, used to 2025-06-30, to figures hand entered from each bank's own reports, with every figure checked against the cached page it came from. From those it computes 19 KPIs from FY2021 to H1 2026, forms peer groups by business model, and measures each bank against the best quartile of its peers. It then says which gaps are larger than the noise, what they are worth, which drivers explain RoTE, and how the market prices RoTE.

## How to run it

```
uv venv --python 3.12
uv pip install -r requirements-lock.txt
uv pip install -e . --no-deps
bpb build
streamlit run bpb/dashboard.py
bpb trace <lineage_id>
```

`bpb build` rebuilds every output from `data/raw/` and `data/manual/`, with no network, and takes about 6 minutes. `bpb trace` prints the chain behind a figure, down to the EBA item or the report page. The dashboard shows the ID of every figure.

## Results

All results are at 2026-06-30, on the cluster group and the underlying basis, unless they say otherwise.

### Q1: where does each bank sit?

<!-- table:q1 start -->
NatWest Group leads on RoTE at 19.91% and Bankinter on cost to income at 35.30%. On RoTE, 3 banks are leading their peers and 10 are lagging. The table below ranks 22 banks on RoTE and 31 on cost to income, the rest being blank at this date. Each verdict is against the bank's own cluster, so the ranks and verdicts need not agree.

| Rank | RoTE: bank | RoTE | Verdict | Cost to income: bank | Cost to income | Verdict |
|---|---|---|---|---|---|---|
| 1 | NatWest Group | 19.91% | leading | Bankinter | 35.30% | leading |
| 2 | BBVA | 19.08% | leading | KBC Group | 37.32% | leading |
| 3 | Banca Monte dei Paschi di Siena | 18.71% | in_line | BBVA | 38.81% | leading |
| 4 | HSBC Holdings | 18.04% | leading | DNB Bank | 39.04% | leading |
| 5 | Intesa Sanpaolo | 17.99% | in_line | Intesa Sanpaolo | 39.44% | leading |
| 6 | Nordea Bank | 17.55% | in_line | CaixaBank | 39.58% | in_line |
| 7 | Banco Santander | 17.41% | in_line | Banco Santander | 41.26% | in_line |
| 8 | CaixaBank | 17.01% | in_line | Swedbank | 41.66% | in_line |
| 9 | Banco BPM | 16.98% | in_line | Danske Bank | 44.96% | in_line |
| 10 | KBC Group | 16.85% | in_line | UniCredit | 45.74% | in_line |
| 11 | Skandinaviska Enskilda Banken | 14.66% | lagging | Skandinaviska Enskilda Banken | 45.98% | in_line |
| 12 | Danske Bank | 14.51% | lagging | Unicaja Banco | 46.05% | in_line |
| 13 | Banco Sabadell | 14.32% | lagging | Nordea Bank | 46.24% | in_line |
| 14 | ING Groep | 13.80% | lagging | HSBC Holdings | 46.43% | leading |
| 15 | Lloyds Banking Group | 13.45% | lagging | Svenska Handelsbanken | 47.22% | lagging |
| 16 | Barclays | 12.99% | in_line | Banco BPM | 47.82% | lagging |
| 17 | BNP Paribas | 12.87% | in_line | NatWest Group | 48.34% | lagging |
| 18 | Société Générale | 11.30% | lagging | Banco Sabadell | 49.01% | lagging |
| 19 | Deutsche Bank | 11.12% | lagging | Santander UK Group Holdings | 53.05% | lagging |
| 20 | ABN AMRO Bank | 9.80% | lagging | ING Groep | 53.17% | lagging |
| 21 | Rabobank | 8.98% | lagging | Rabobank | 54.02% | lagging |
| 22 | Santander UK Group Holdings | 6.43% | lagging | BPER Banca | 54.55% | lagging |
| 23 |  |  |  | Commerzbank | 55.51% | lagging |
| 24 |  |  |  | Barclays | 57.92% | in_line |
| 25 |  |  |  | Crédit Agricole Group | 58.84% | lagging |
| 26 |  |  |  | Lloyds Banking Group | 59.03% | lagging |
| 27 |  |  |  | BNP Paribas | 59.75% | in_line |
| 28 |  |  |  | Banca Monte dei Paschi di Siena | 59.81% | lagging |
| 29 |  |  |  | Société Générale | 60.07% | lagging |
| 30 |  |  |  | ABN AMRO Bank | 60.71% | lagging |
| 31 |  |  |  | Deutsche Bank | 62.68% | lagging |
<!-- table:q1 end -->

### Q2: which gaps are larger than the noise, and what are they worth?

<!-- table:q2 start -->
10 banks have the largest joint gaps, led by CAG at EUR 19,852m. Min and max run over the 3 peer groups and 2 bases, and the joint figure closes every sized gap at once, so it can be less than the sum of the bank's rows. Amounts are EUR m of annual pre tax profit.

| Bank | Gap | Headline | Min | Max | Joint |
|---|---|---|---|---|---|
| CAG | NIM | 17,419 | 15,076 | 17,419 | 19,852 |
| CAG | Cost to income | 7,154 | 6,525 | 7,154 | 19,852 |
| CAG | Cost of risk | 2,458 | 2,047 | 2,458 | 19,852 |
| SAN | Cost of risk | 11,525 | 9,970 | 11,525 | 11,525 |
| INGA | NIM | 8,597 | 7,175 | 8,597 | 7,898 |
| INGA | Cost to income | 2,845 | 2,476 | 2,845 | 7,898 |
| BBVA | Cost of risk | 6,326 | 5,632 | 6,326 | 6,326 |
| BARC | NIM | 4,278 | 4,278 | 11,237 | 5,059 |
| BARC | Cost of risk | 781 | 781 | 1,921 | 5,059 |
| LLOY | Cost to income | 4,189 | 2,324 | 4,244 | 4,692 |
| LLOY | Cost of risk | 503 | 503 | 503 | 4,692 |
| ABN | NIM | 3,361 | 2,755 | 3,361 | 3,752 |
| ABN | Cost to income | 1,776 | 1,653 | 1,778 | 3,752 |
| DBK | Cost to income | 3,658 | 3,043 | 6,869 | 3,658 |
| GLE | Cost to income | 2,339 | 1,882 | 5,093 | 3,368 |
| GLE | NIM | 2,124 | 2,124 | 6,108 | 3,368 |
| DANSKE | NIM | 3,166 | 2,690 | 3,166 | 3,166 |
<!-- table:q2 end -->

### Q3: which drivers explain the RoTE gap?

Decomposition explains where a RoTE gap comes from, and business mix is a legitimate part of that, while sizing in Q2 is where mix must not count as opportunity.

<!-- table:q3 start -->
Of the banks with a decomposition at 2026-06-30, RABO sits furthest from its peer median, -7.31 points, and its largest step is assets / tangible equity at -5.66 points. Each row runs from the reference RoTE, every driver at the peer median, to the bank's RoTE, in points.

| Bank | Gap to median | Reference | NII / assets | Fees / assets | Other income / assets | Costs / assets | Credit losses / assets | Tax rate | Assets / tangible equity | Other below the line | Minorities and AT1 | Bank RoTE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RABO | -7.31 | 15.86 | +4.12 | -2.81 | +0.38 | -2.36 | -0.60 | +0.17 | -5.66 | +0.29 | -0.40 | 8.98 |
| ABN | -6.49 | 16.23 | -1.75 | -0.88 | -2.65 | -1.02 | +1.71 | -0.16 | -1.04 | +0.29 | -0.92 | 9.80 |
| HSBA | +5.97 | 14.38 | +4.58 | -1.01 | +3.26 | +1.63 | -0.12 | +0.60 | -5.81 | +1.66 | -1.13 | 18.04 |
| NWG | +4.20 | 14.94 | +4.25 | -4.38 | -1.82 | +1.73 | +0.83 | +0.36 | +4.82 | +0.28 | -1.09 | 19.91 |
| BBVA | +3.37 | 15.40 | +21.73 | +5.52 | +0.78 | -7.53 | -8.20 | -1.41 | -4.92 | -0.34 | -1.94 | 19.08 |
<!-- table:q3 end -->

### Q4: what is a point of RoTE worth?

<!-- table:q4 start -->
The market paid more for each point of RoTE every year: β rises from 4.50 in 2022 to 10.43 in 2025, and the implied cost of equity falls from 24.2% to 11.6%. The cost of equity is blank in 2021, where the 90% interval of β contains 0. The test that the year slopes are equal is rejected: F(4, 26) = 10.00, p = 0.00005, over 120 bank years. So 1 pooled slope is the wrong model for anything but the significance gate, and the choice of slope matters: LLOY's uplift at the end of 2025 is +0.94x on that year's β and +0.31x on the pooled β. The figure below shows 2025, the tightest fit.

| Year | β | R² | n | Implied CoE |
|---|---|---|---|---|
| 2021 | 1.05 | 0.09 | 22 | blank |
| 2022 | 4.50 | 0.48 | 23 | 24.2% |
| 2023 | 4.53 | 0.40 | 25 | 24.1% |
| 2024 | 6.63 | 0.55 | 25 | 17.1% |
| 2025 | 10.43 | 0.74 | 25 | 11.6% |

![P/TBV against RoTE](outputs/figures/valuation_2025.png)
<!-- table:q4 end -->

### Q5: how far apart are the 2 sources?

<!-- table:q5 start -->
Fields the 2 sources define alike agree closely: the median absolute difference is 0.0000% for loans and 0.02% for profit after tax. Total assets differ by a median of 8.54%, because the supervisory scope leaves out entities such as insurers. Small residual lines differ the most, since each source draws them differently. The table covers 2025-06-30, the date both sources report.

| Field | Banks | Median | 90th percentile |
|---|---|---|---|
| admin_expenses | 26 | 1.91% | 13.08% |
| at1_instruments | 22 | 0.55% | 4.12% |
| cash_cb | 25 | 2.94% | 12.21% |
| debt_securities | 24 | 0.00% | 0.00% |
| deposits_customers | 23 | 2.04% | 9.15% |
| depreciation | 21 | 1.14% | 6.75% |
| dividend_income | 15 | 0.70% | 62.13% |
| exchange_differences | 6 | 0.07% | 7.50% |
| gains_derecognition_not_fvtpl | 18 | 36.35% | 149.02% |
| gains_designated_fvtpl | 9 | 59.03% | 187.56% |
| gains_hedge_accounting | 12 | 0.23% | 46.05% |
| gains_held_for_trading | 26 | 33.47% | 305.20% |
| impairments_fin | 26 | 3.34% | 87.21% |
| impairments_nonfin | 8 | 79.56% | 534.66% |
| intangibles_deduction | 22 | 0.00% | 0.05% |
| interest_expense | 26 | 0.97% | 23.33% |
| interest_income | 26 | 1.33% | 12.30% |
| loans_all | 24 | 0.00% | 0.00% |
| loans_customers_allowance | 24 | 0.00% | 0.03% |
| loans_customers_gross | 24 | 0.00% | 0.00% |
| loans_households_gross | 24 | 0.00% | 0.00% |
| net_fees | 26 | 0.80% | 14.41% |
| npl_allowance | 24 | 0.00% | 0.02% |
| npl_gross | 24 | 0.00% | 0.01% |
| other_operating_net | 26 | 127.58% | 1093.47% |
| pat | 26 | 0.02% | 2.81% |
| pbt | 26 | 0.46% | 5.00% |
| profit_owners | 26 | 0.01% | 2.29% |
| provisions | 11 | 0.47% | 32.61% |
| resolution_dgs_contrib | 6 | 15.87% | 105.51% |
| total_assets | 25 | 8.54% | 16.65% |
| total_equity | 24 | 0.02% | 1.41% |
| total_liabilities | 19 | 9.89% | 17.47% |
| total_operating_income | 26 | 3.12% | 7.86% |
| trading_assets | 17 | 0.40% | 59.54% |

**Bank insurer scope.** NDA, DANSKE, SWED, SEB, SHB, KBC, BNP, GLE, CAG, BAMI, CABK, DNB, ISP, UCG carry a scope difference between the 2 sources, as bank insurers or with a total assets seam above 5%. For ISP and KBC, the income statement lines were read line by line and every one sits in the right field, so the size of other below the line is the insurance effect: -7.85 points of RoTE for ISP and -10.11 for KBC at 2026-06-30. The same treatment flatters their cost to income.
<!-- table:q5 end -->

## Peer groups

<!-- table:peers start -->
The clustering splits the 31 banks into 5 and 26. The 5 are BARC, BNP, DBK, GLE, HSBA: global banks, far larger than the rest, with a much higher share of trading assets and a lower share of loans. Everyone else, from Lloyds to Unicaja, is 1 broad group of retail and commercial banks, so the cluster says more about what the global banks are than about how the others differ. That is why every sized gap is shown with its range across the 3 groups. The silhouette is 0.29, and mean stability is 0.57 for the 5 bank cluster and 0.78 for the other.
<!-- table:peers end -->

## Caveats

- **Accounting scope.** Bank insurers report insurance lines that the supervisory scope leaves out, so their cost and income ratios are not like for like.
- **FX inside averages.** Averages and rolling figures of EBA balances for the 5 non EUR banks carry the currency move between their 2 ends.
- **The 2 seams.** Seam 1 sets EBA capital against Pillar 3, and seam 2 sets EBA against the banks' own reports. EBA feeds the history and reports the latest dates, so no time comparison crosses the switch, and such a cell is blank with status `family_switch`.
- **One offs.** Underlying figures adjust only for what each bank discloses, never for judgement.
- **Broad cluster 2.** The cluster group for most banks is broad, so read every sized gap with its range across the 3 groups.
- **Small peer groups.** Market groups hold few banks, intervals are wide, and a group that is too small gives no benchmark.
- **Valuation slope.** The slope changes every year, so an uplift holds only at the date of its fit.
- **BMPS prices.** Earlier BMPS prices may carry a rights issue adjustment that `Stock Splits` does not undo. It touches no P/TBV, since BMPS's 2021 TBV per share is blank.
<!-- table:headcount start -->
- **Headcount.** 9 banks publish only headcount, which stands in for FTE.
<!-- table:headcount end -->
<!-- table:coverage start -->
- **Coverage.** 92 of 589 KPI cells are blank at 2026-06-30 on the underlying basis, because an input is not published or not comparable. The largest causes are customers (27), fte (24), mixed_family (7).
<!-- table:coverage end -->

## What it does not do

- It does not forecast. Every figure is historical, and a sized gap says what a bank would earn at peer levels on today's balance sheet.
- It does not say a gap can be closed. Some gaps are structural, and the peer grouping reduces that without removing it.
- It does not harmonise accounting across countries beyond what FINREP and Pillar 3 already standardise. The seam table shows the difference that remains.
- It does not adjust for one offs on judgement, only for those the bank itself discloses.
- It does not cover banks outside the 7 markets, or smaller banks outside the EBA sample.
- It does not give investment advice. The valuation describes a cross sectional relationship with its uncertainty, not a target price.

## Repository map

- `bpb/`: the package: ingestion, KPIs, checks, peers, benchmarks, gaps, drivers, valuation, reports, trace and the dashboard.
- `config/`: field, KPI and source maps. `config.toml` holds every parameter.
- `data/raw/`: pulled data, the cached report pages and their hashes.
- `data/manual/`: hand entered figures, one offs, mergers and the universe.
- `docs/`: `METHODS.md` and the resolved conventions.
- `outputs/`: profiles, figures and tables, all rebuilt by `bpb build`.
- `project_outline/`: the original outline.
- `scripts/`: data pulls and the README table writer.
- `tests/`: the test suite, which runs offline.
- `instructions/`, `review/`, `decisions/` and `PLAN.md`: the build record.
```

### E6.5: CI

Run 41900902469 on 77c368f: conclusion `success`, on Linux.

```
62 passed, 130 warnings in 525.53s (0:08:45)
```

The run before it, on 0dcaffd, failed on `test_dashboard_runs` only (Deviation 1). No lock change was needed.

## Tests run

The fresh clone run below is the full suite with sockets disabled.

## Fresh-clone check

Clone path `C:/bpbs6c`. The first line below is the commit. Commands: `git clone`, `uv venv --python 3.12`, `uv pip install -r requirements-lock.txt`, `uv pip install -e . --no-deps`, `ruff check .`, `pytest -p socket --disable-socket -q`, `bpb build`, `git status --porcelain`.

**Run 1** (clone, ruff, suite, build, git status). The suite gave 7 errors, all from the shared build fixture: `pandas.errors.ParserError: out of memory`. It ran while my own build in `C:/bpbs6b` and another project's run were using the machine, with 2.4 GB of 15.7 GB free soon after. The build and the empty `git status` at the end of this run are valid. Failure lines only:

```
77c368f step 6.5: drop my dashboard test, which needs a socket under rule 7
All checks passed!
ruff exit 0
All checks passed!
ruff exit 0
ERROR tests/test_build.py::test_build_twice_identical - pandas.errors.ParserE...
ERROR tests/test_readme.py::test_tables_match - pandas.errors.ParserError: Er...
ERROR tests/test_readme.py::test_no_dashes - pandas.errors.ParserError: Error...
ERROR tests/test_readme.py::test_no_banned_words - pandas.errors.ParserError:...
ERROR tests/test_readme.py::test_answers_cover_every_question - pandas.errors...
ERROR tests/test_trace.py::test_trace_sample - pandas.errors.ParserError: Err...
ERROR tests/test_trace.py::test_trace_command - pandas.errors.ParserError: Er...
55 passed, 130 warnings, 7 errors in 2150.39s (0:35:50)
pytest exit 1
build exit 0
git status after build:
end of git status
```

**Run 2**, the same clone with nothing else of mine running, full output:

```
77c368f step 6.5: drop my dashboard test, which needs a socket under rule 7
..............................................................           [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\_pytest\config\__init__.py:894
  C:\bpbs6c\.venv\Lib\site-packages\_pytest\config\__init__.py:894: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; socket
    self.import_plugin(arg, consider_entry_points=True)

tests/test_gaps.py: 65 warnings
  C:\bpbs6c\.venv\Lib\site-packages\pycel\excelformula.py:995: DeprecationWarning: ast.Str is deprecated and will be removed in Python 3.14; use ast.Constant instead
    op = ast.Str(s=type(node_op).__name__)

tests/test_gaps.py: 64 warnings
  C:\Users\astha\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none\Lib\ast.py:587: DeprecationWarning: Attribute s is deprecated and will be removed in Python 3.14; use value instead
    return Constant(*args, **kwargs)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
62 passed, 130 warnings in 948.83s (0:15:48)
pytest exit 0
```

## Runtime per step

- `bpb build`: 6 min 16 s on a quiet machine, 14 min 33 s with another project's run sharing it.
- Full suite: 8 min 46 s on CI, 15 min 49 s in the fresh clone.

## Deviations from PLAN.md

1. **I added `tests/test_dashboard.py` and removed it.** It was not specified. Streamlit's `AppTest` needs an event loop socket, so it failed under `--disable-socket` locally and on CI. Exempting it would have got round rule 7, so the check is now the smoke run in E6.2b, and no test covers the dashboard.
2. **I committed step 6.3 before reading its test result, and that run had failed.** Its 4 fixture errors were `OSError: [Errno 22]`, and I had by mistake started 2 copies of the same pytest run at once. The commit was not pushed. A later clone run hit `out of memory` the same way under load (see the fresh clone check). So memory pressure is the likely cause of both, but `Errno 22` was not reproduced.
3. **`spec_log.csv` gains a trailing `status` column.** 06b B.2 asks for status `no_git`, and the schema has no status column. Please confirm.
4. **League tables, 3 readings.** They use the underlying basis, as B.1 names no basis. A cluster file holds all 31 banks ranked together, with each verdict against the bank's own cluster, since the fixed columns have no cluster label. A blank value keeps its row at the end, with no rank.
5. **README readings.** Q2's "10 largest by joint" is read as the 10 banks with the largest joint gap, so the table has more than 10 rows. Q3's "largest RoTE gaps to the median" is read in either direction, among banks with a decomposition at 2026-06-30.
6. **New outputs for trace:** `lineage.csv` and `lineage_derived.csv`, so that the dashboard reads only `outputs/`. Derived rows get an ID from `row_id`, the Convention 4.13 hash with the table as the family.
7. **Trace stops at the bank's own inputs for a gap or driver.** A target or reference comes from peers, and the peers' facts are not listed. KPI rows trace in full.
8. **`test_trace_sample` also checks one offs,** which are not FACTS rows but appear as inputs on the underlying basis. They get the same 2 checks.
9. **The tests share 1 build** through a session fixture, so the suite runs 2 builds, not 1 per test.
10. **Extra tests:** `test_year_not_significant`, `test_stability_separates_slopes`, `test_trace_command`, `test_no_banned_words`, `test_answers_cover_every_question`.
11. **`scripts/run_all.py` now calls `bpb build`,** which replaces its body. `build_facts` gained an optional output root. The `bpb build` code is in the step 6.2 commit, since `bpb trace` shares its file.
12. **PLAN names `test_sampled_pdf_numbers_trace_to_facts` and `test_readme_tables_match_csvs`.** The instruction's names are used (rule 13).

## Not verified

- **The dashboard in a real browser.** It ran through Streamlit's `AppTest` only.
- **BMPS's earlier prices.** The rights issue adjustment is suspected, not checked. The README caveat says "may".
- **Byte identity across machines.** Builds are identical on Windows. The README tables match a Linux build on CI, but the Linux outputs were not compared byte for byte.
- **The cause of `Errno 22`** (Deviation 2).
- **Peak memory of a build.** It was not measured. A build can fail on a machine short of memory, though not on CI or on this one when it is otherwise quiet.

## Open questions

No blockers. `decisions/OPEN.md` has no undecided item: OPEN-42 to OPEN-44 are decided in instruction 06b. To confirm or correct:

1. **The headline gap is CAG's.** Its joint gap of EUR 19.9bn is the largest, but CAG is a bank insurer with a scope caveat, and its joint RoTE gap is blank. Is it the right lead for the README?
2. **Deviation 3** (the `status` column) and **Deviations 4 and 5** (the readings).

## Files changed

218 files, of which those outside `outputs/` are:

```
CLAUDE.md
LICENSE
README.md
bpb/answers.py
bpb/cli.py
bpb/dashboard.py
bpb/ingest.py
bpb/lineage.py
bpb/market.py
bpb/report.py
bpb/valuation.py
data/raw/MANIFEST.json
data/raw/market/splits.csv
decisions/section_5_review.md
docs/METHODS.md
instructions/06b_section_6_continue.md
instructions/06b_section_6_continue.status.md
project_outline/Bank_Performance_Benchmarking.md
review/figures/section_6_contact.png
review/section_6.md
scripts/pull_data.py
scripts/run_all.py
scripts/write_readme_tables.py
tests/conftest.py
tests/test_build.py
tests/test_market.py
tests/test_readme.py
tests/test_trace.py
tests/test_valuation.py
```

Under `outputs/`: every table, 31 PDFs and 31 PNGs, the valuation figures, 102 league CSVs and 17 HTML pages.

## Reviewer reads

1. `instructions/06b_section_6_continue.status.md`
2. `README.md`
3. Deviations above
4. E6.0a and E6.0b
5. `bpb/lineage.py` and `bpb/cli.py`

## Commits this session

```
31f34ae section 6: status of instruction 06b (completed)
a61681d section 6: review of the whole section
77c368f step 6.5: drop my dashboard test, which needs a socket under rule 7
0dcaffd step 6.5: MIT licence, project_outline rename, final spec_log stamp
43c346c step 6.4: README, METHODS, generated tables and answers.csv
80f09f1 step 6.3: bpb build, answers.csv and the byte identical test
d4dcf83 step 6.2: lineage tables, bpb trace and the dashboard
735090e step 6.1: 31 profiles, league CSVs and HTML pages
37f943f step 6.0: section 5 review decisions
```

---

# Instruction 06c (stopped at step 6.6)

Step 6.6 stopped under rules 4 and 5: `test_hand_check` fails, because ISP no longer has a sized gap (OPEN-46). Steps 6.7 and 6.8 were not run. Section 6 is not yet approved.

## Steps completed

6.6 section 6 review decisions, stopped (7e055ed). B.1 and B.5 are applied, everything is rebuilt, and the amendments, `decisions/section_6_review.md` and `docs/METHODS.md` are written. The README tables and `answers.csv` are regenerated from the new tables, as B.1 item 7 asks, in the old format, since B.2 belongs to step 6.7.

## Evidence

### E6.6a: risk_adj_nim, gaps, joint gaps and valuation, before and after

The first table is the pipeline next to A.1: the largest difference is below 1e-6. SAN is `in_line` and BBVA `leading`, and neither has a margin gap, so the EUR 17.8bn is gone from Q2.

```
bank_id  rev_value  rev_target    value   target verdict  n_peers  d_value  d_target
    SAN   0.020965    0.019887 0.020965 0.019887 in_line       20 0.000000  0.000000
   BBVA   0.032541    0.019569 0.032541 0.019569 leading       20 0.000000  0.000000
GAPS before: sized rows
bank_id          gap         m  delta_rote_pts                              status
    ABN  cost_income  1,776.47            5.59                                  ok
    ABN          nim  3,360.80           10.57                                  ok
   BAMI  cost_income    427.20            2.90                                  ok
   BAMI cost_of_risk    250.96            1.70                                  ok
   BARC cost_of_risk    780.89            0.97                                  ok
   BARC          nim  4,277.90            5.33                                  ok
   BBVA cost_of_risk  6,326.28            7.72                                  ok
   BMPS  cost_income  1,124.78            5.15                                  ok
   BMPS cost_of_risk    846.63            3.88                                  ok
    BNP cost_of_risk    904.89            0.68                                  ok
    BPE  cost_income    990.80            5.83                                  ok
    BPE cost_of_risk    361.67            2.13                                  ok
   CABK cost_of_risk    560.82            1.17                                  ok
   CABK          nim  1,963.08            4.10                                  ok
    CAG  cost_income  7,154.02             NaN       missing_input:at1_instruments
    CAG cost_of_risk  2,458.41             NaN       missing_input:at1_instruments
    CAG          nim 17,418.72             NaN       missing_input:at1_instruments
    CBK  cost_income  1,801.11             NaN       missing_input:at1_instruments
 DANSKE          nim  3,166.32           11.04                                  ok
    DBK  cost_income  3,657.85            4.72                                  ok
    GLE  cost_income  2,339.49            3.43                                  ok
    GLE          nim  2,123.86            3.12                                  ok
   INGA  cost_income  2,844.53            4.19                                  ok
   INGA          nim  8,597.07           12.66                                  ok
    ISP cost_of_risk  1,318.70            1.87                                  ok
    KBC          nim  1,419.09            5.25                                  ok
   LLOY  cost_income  4,189.06            7.62                                  ok
   LLOY cost_of_risk    503.14            0.91                                  ok
    NDA  cost_income    591.88            1.65                                  ok
    NDA          nim  3,531.17            9.86                                  ok
    NWG  cost_income  1,402.81            3.27                                  ok
   RABO  cost_income  2,139.05            3.09                                  ok
   RABO cost_of_risk    696.24            1.01                                  ok
    SAB  cost_income    320.70            2.00                                  ok
    SAB cost_of_risk    376.34            2.34                                  ok
    SAB          nim  2,038.81           12.69                                  ok
    SAN cost_of_risk 11,525.41            9.60                                  ok
  SANUK  cost_income    683.33            3.61                                  ok
  SANUK          nim  2,398.11           12.68                                  ok
    SEB  cost_income    331.32            1.33                                  ok
    SEB          nim  2,195.96            8.82                                  ok
    SHB  cost_income    305.32             NaN missing_input:intangibles_deduction
   SWED          nim  1,097.19             NaN    missing_input:minority_interests
    UCG  cost_income  1,154.66             NaN       missing_input:at1_instruments
    UNI  cost_income    102.40             NaN                        mixed_family
    UNI cost_of_risk     57.19             NaN                        mixed_family
    UNI          nim    537.02             NaN                        mixed_family
GAPS after: sized rows
bank_id          gap         m  delta_rote_pts                              status
    ABN  cost_income  1,776.47            5.59                                  ok
    ABN risk_adj_nim  2,260.29            7.11                                  ok
   BAMI  cost_income    427.20            2.90                                  ok
   BARC risk_adj_nim  4,722.65            5.88                                  ok
   BMPS  cost_income  1,124.78            5.15                                  ok
   BMPS risk_adj_nim    713.83            3.27                                  ok
    BPE  cost_income    990.80            5.83                                  ok
   CABK risk_adj_nim  1,358.00            2.84                                  ok
    CAG  cost_income  7,154.02             NaN       missing_input:at1_instruments
    CAG risk_adj_nim 16,221.28             NaN       missing_input:at1_instruments
    CBK  cost_income  1,801.11             NaN       missing_input:at1_instruments
 DANSKE risk_adj_nim  2,209.34            7.71                                  ok
    DBK  cost_income  3,657.85            4.72                                  ok
    GLE  cost_income  2,339.49            3.43                                  ok
    GLE risk_adj_nim  2,213.95            3.25                                  ok
   INGA  cost_income  2,844.53            4.19                                  ok
   INGA risk_adj_nim  6,942.65           10.23                                  ok
    KBC risk_adj_nim    782.56            2.90                                  ok
   LLOY  cost_income  4,189.06            7.62                                  ok
    NDA  cost_income    591.88            1.65                                  ok
    NDA risk_adj_nim  2,225.86            6.22                                  ok
    NWG  cost_income  1,402.81            3.27                                  ok
   RABO  cost_income  2,139.05            3.09                                  ok
    SAB  cost_income    320.70            2.00                                  ok
    SAB risk_adj_nim  1,963.09           12.21                                  ok
  SANUK  cost_income    683.33            3.61                                  ok
  SANUK risk_adj_nim  1,878.77            9.94                                  ok
    SEB  cost_income    331.32            1.33                                  ok
    SEB risk_adj_nim  1,599.10            6.42                                  ok
    SHB  cost_income    305.32             NaN missing_input:intangibles_deduction
   SWED risk_adj_nim    506.75             NaN    missing_input:minority_interests
    UCG  cost_income  1,154.66             NaN       missing_input:at1_instruments
    UNI  cost_income    102.40             NaN                        mixed_family
    UNI risk_adj_nim    395.70             NaN                        mixed_family
rows not sized: before 46 after 28
GAPS_JOINT, EUR m
bank_id  joint_eur_before  joint_rote_pts_before  joint_eur_after  joint_rote_pts_after  overlap_eur
    CAG         19,851.98                    NaN        16,689.66                   NaN     6,685.64
   INGA          7,898.30                  11.63         6,925.75                 10.20     2,861.43
   BARC          5,058.79                   6.30         4,722.65                  5.88         0.00
   LLOY          4,692.20                   8.53         4,189.06                  7.62         0.00
    DBK          3,657.85                   4.72         3,657.85                  4.72         0.00
    GLE          3,367.65                   4.94         3,411.27                  5.01     1,142.17
    ABN          3,752.10                  11.80         3,105.17                  9.77       931.58
 DANSKE          3,166.32                  11.04         2,209.34                  7.71        -0.00
   RABO          2,835.29                   4.10         2,139.05                  3.09         0.00
    NDA          2,667.46                   7.45         1,900.21                  5.31       917.53
    CBK          1,801.11                    NaN         1,801.11                   NaN         0.00
  SANUK          2,093.05                  11.07         1,787.76                  9.45       774.34
   BMPS          1,971.42                   9.03         1,544.41                  7.07       294.21
    SAB          1,895.55                  11.79         1,474.70                  9.18       809.09
    NWG          1,402.81                   3.27         1,402.81                  3.27         0.00
   CABK          2,523.90                   5.28         1,358.00                  2.84         0.00
    SEB          1,621.98                   6.52         1,271.18                  5.11       659.24
    UCG          1,154.66                    NaN         1,154.66                   NaN        -0.00
    BPE          1,352.47                   7.95           990.80                  5.83        -0.00
    KBC          1,419.09                   5.25           782.56                  2.90        -0.00
   SWED          1,097.19                    NaN           506.75                   NaN         0.00
   BAMI            678.16                   4.60           427.20                  2.90         0.00
    UNI            475.23                    NaN           334.98                   NaN       163.12
    SHB            305.32                    NaN           305.32                   NaN        -0.00
   BBVA          6,326.28                   7.72              NaN                   NaN          NaN
    BKT               NaN                    NaN              NaN                   NaN          NaN
    BNP            904.89                   0.68              NaN                   NaN          NaN
    DNB               NaN                    NaN              NaN                   NaN          NaN
   HSBA               NaN                    NaN              NaN                   NaN          NaN
    ISP          1,318.70                   1.87              NaN                   NaN          NaN
    SAN         11,525.41                   9.60              NaN                   NaN          NaN
VALUATION at 2025-12-31
bank_id  rote_gap_pts_b  uplift_ptbv_b  uplift_lo_b  uplift_hi_b     status_b  rote_gap_pts_a  uplift_ptbv_a  uplift_lo_a  uplift_hi_a  uplift_pooled_ptbv     status_a
   LLOY            9.03           0.94         0.72         1.16           ok            8.06           0.84         0.64         1.04                0.28           ok
    NWG            4.44           0.46         0.35         0.57           ok            3.37           0.35         0.27         0.43                0.12           ok
   BARC            4.25           0.44         0.34         0.55           ok            3.89           0.41         0.31         0.50                0.13           ok
   HSBA             NaN            NaN          NaN          NaN no_joint_gap             NaN            NaN          NaN          NaN                 NaN no_joint_gap
    NDA            5.86           0.61         0.47         0.75           ok            4.43           0.46         0.35         0.57                0.15           ok
    DNB             NaN            NaN          NaN          NaN no_joint_gap             NaN            NaN          NaN          NaN                 NaN no_joint_gap
 DANSKE            6.42           0.67         0.51         0.83           ok            5.15           0.54         0.41         0.66                0.18           ok
    SEB            4.19           0.44         0.33         0.54           ok            3.48           0.36         0.28         0.45                0.12           ok
    SHB            6.50           0.68         0.52         0.84           ok            5.06           0.53         0.40         0.65                0.17           ok
   SWED            3.12           0.33         0.25         0.40           ok            1.27           0.13         0.10         0.16                0.04           ok
   INGA           11.32           1.18         0.90         1.46           ok            9.60           1.00         0.77         1.24                0.33           ok
    ABN           10.69           1.12         0.85         1.38           ok            9.26           0.97         0.74         1.19                0.32           ok
    KBC            5.61           0.58         0.45         0.72           ok            3.58           0.37         0.29         0.46                0.12           ok
    BNP            0.60           0.06         0.05         0.08           ok             NaN            NaN          NaN          NaN                 NaN no_joint_gap
    GLE            5.32           0.56         0.42         0.69           ok            5.38           0.56         0.43         0.69                0.19           ok
    DBK            4.44           0.46         0.35         0.57           ok            4.44           0.46         0.35         0.57                0.15           ok
    CBK             NaN            NaN          NaN          NaN no_joint_gap             NaN            NaN          NaN          NaN                 NaN no_joint_gap
    SAN            9.89           1.03         0.79         1.27           ok             NaN            NaN          NaN          NaN                 NaN no_joint_gap
   BBVA            7.22           0.75         0.58         0.93           ok             NaN            NaN          NaN          NaN                 NaN no_joint_gap
   CABK            1.46           0.15         0.12         0.19           ok            1.77           0.18         0.14         0.23                0.06           ok
    SAB            6.89           0.72         0.55         0.89           ok            4.92           0.51         0.39         0.63                0.17           ok
    BKT             NaN            NaN          NaN          NaN no_joint_gap             NaN            NaN          NaN          NaN                 NaN no_joint_gap
    UNI            1.96           0.20         0.16         0.25           ok            0.91           0.10         0.07         0.12                0.03           ok
    UCG            2.02           0.21         0.16         0.26           ok            2.02           0.21         0.16         0.26                0.07           ok
    ISP            2.34           0.24         0.19         0.30           ok             NaN            NaN          NaN          NaN                 NaN no_joint_gap
   BAMI            5.34           0.56         0.43         0.69           ok            3.42           0.36         0.27         0.44                0.12           ok
    BPE            9.00           0.94         0.72         1.16           ok            6.46           0.67         0.52         0.83                0.22           ok
   BMPS            9.02           0.94         0.72         1.16           ok            7.09           0.74         0.57         0.91                0.24           ok
```

### E6.6b: CAG at1_instruments (B.5): every date left out

CC1 is not printed in any of the 4 hashed Group documents, so no entry was made and CAG's joint RoTE gap stays blank. Each says the full tables are on the website, for example: "For clarity, the full tables of the composition of capital (EU CC1 and EU CC2) are available at https://www.credit-agricole.com/...".

```
date        document                      page with the statement
2024-12-31  CAG_pillar3_2024-12-31.pdf    69
2025-06-30  CAG_pillar3_2025-06-30.pdf    5
2025-12-31  CAG_pillar3_2025-12-31.pdf    243
2026-06-30  CAG_pillar3_2026-06-30.pdf    90
```

Those pages print "(-) AT1 instruments accounted as equity" at 7,218, 8,612, 8,143 and 8,020 (EUR m). That line is not CC1 row 30, so it was not entered (OPEN-45).

### E6.6c: why ISP has no sized gap at 2025-12-31

ISP is `leading` on risk_adj_nim in every group. On cost_income it is inside noise in the cluster and universe groups and `leading` in the market group. All 12 GAPS rows are `not_sized`.

### E6.6d: the other hand check sheets, and the banks with both gaps

`test_hand_check` stops at ISP, so LLOY and SWED were evaluated apart from it, with the same pycel calls. Both match. Each has 1 sized gap, so neither exercises the joint formula on 2 gaps. The second table lists the banks with both gaps at 2025-12-31, cluster group, underlying basis, EUR m.

```
bank   group         item  workbook_eur  pipeline_eur  workbook_pts  pipeline_pts
LLOY cluster  cost_income  4.404501e+09  4404501377.0      8.055883      8.055883
LLOY cluster        joint  4.404501e+09  4404501377.0           NaN           NaN
SWED cluster risk_adj_nim  2.936684e+08   293668355.4      1.269417      1.269417
SWED cluster        joint  2.936684e+08   293668355.4           NaN           NaN
gap      cost_income  risk_adj_nim  te_ok
bank_id                                  
ABN           1906.2        1652.7   True
BMPS           863.5        1311.8   True
DANSKE         287.8        2142.9   True
GLE           2653.5        2232.5   True
INGA          2988.8        6081.7   True
NDA            512.5        1808.0   True
RABO          2134.3         989.4   True
SAB            248.9        1048.2   True
SANUK          579.2        1303.9   True
SEB            326.1         966.3   True
SHB            223.0        1619.3   True
```

### E6.6e: a trial of the B.4 test under `--disable-socket`

A probe outside the repo ran the dashboard with `AppTest` on the 06c outputs, selecting LLOY, ISP and SWED, under `pytest -p socket --disable-socket`, with `@pytest.mark.allow_hosts(["127.0.0.1"])`. It passed, with no exception, and an external connect in the same test was refused. Without that marker `AppTest` fails, as `test_dashboard_runs` did in step 6.5, because its event loop needs a loopback socket.

```
external connect blocked by: SocketConnectBlockedError
1 passed, 71 warnings in 36.37s
```

## Tests run

The fresh clone run below. CI on 7e055ed, conclusion `failure`:

```
FAILED tests/test_gaps.py::test_hand_check - assert 0 > 0
1 failed, 61 passed, 40 warnings in 756.78s (0:12:36)
```

## Fresh-clone check

Clone path `C:/bpbs6d`, with the same commands as above, without `bpb build`. Pass and fail lines only:

```
7e055ed step 6.6: section 6 review decisions (stopped: ISP has no sized gap, OPEN-46)
All checks passed!
ruff exit 0
E           assert 0 > 0
E            +  where 0 = len(Empty DataFrame\nColumns: [date, bank_id, group, basis, delta_pi_lc, delta_pi_eur, delta_rote_pts, tax_rate, tax_status,
FAILED tests/test_gaps.py::test_hand_check - assert 0 > 0
1 failed, 61 passed, 40 warnings in 2050.90s (0:34:10)
pytest exit 1
```

## Deviations from PLAN.md

1. **`joint_gap` keeps its `nim` and `cost_of_risk` branches.** B.1 item 5 says `risk_adj_nim` replaces them, and step 6.7 says existing tests pass unchanged. `test_joint_single_synthetic` passes those keys, so they stay, and the pipeline never uses them, since it passes only what `[gaps] sized` names.
2. **`bank_inputs` reads LLP as NII less the risk_adj_nim numerator,** where that numerator exists, so the margin and its parts agree.
3. **`main` has a failing test.** Rule 4 asks for the push, so CI is red until OPEN-46 is decided.

## Not verified

- **Steps 6.7 and 6.8.** B.2, B.3 and B.4 are not applied. The README still leads with CAG, in the old format.
- **The `spec_log.csv` stamp is stale** until step 6.8, since the build ran before the commit that changed its inputs.
- **The E6.6e trial ran on Windows only.** On Linux the event loop may use a different socket type.

## Open questions

1. **OPEN-46 (blocking):** replace ISP in `hand_check_banks`, or change the test?
2. **OPEN-45:** use the printed AT1 line for CAG, or fetch the website's CC1 tables? B.5 is met as written, so this is not blocking.
3. **Rule 7 and B.4:** is `allow_hosts(["127.0.0.1"])` on `test_dashboard_runs` acceptable? It is needed for the test to run under `--disable-socket`, and it keeps external connections blocked.

## Files changed

`CLAUDE.md`, `README.md`, `bpb/gaps.py`, `bpb/report.py`, `config.toml`, `config/fields.yaml`, `config/kpis.yaml`, `decisions/OPEN.md`, `decisions/section_6_review.md`, `docs/METHODS.md`, `scripts/build_hand_check.py`, `tests/fixtures/hand_check.xlsx`, and the rebuilt `outputs/`.

## Reviewer reads

1. `instructions/06c_section_6_finish.status.md`
2. `decisions/OPEN.md`, OPEN-45 and OPEN-46
3. E6.6a, E6.6c and E6.6d

---

# Instruction 06d (steps 6.6b, 6.7 and 6.8)

Steps 6.6b to 6.8 are done. The fresh clone and CI on the final commit give 65 passed, and a second `bpb build` leaves `git status --porcelain` empty. CAG's joint RoTE gap is still blank: the AT1 entries pass, but CAG also lacks intangibles_deduction (OPEN-47).

## Steps completed

- **6.6b** hand check bank and CAG AT1 (125e3e8). B.1: INGA replaces ISP in `[gaps] hand_check_banks`. B.2: CAG's at1_instruments from the printed line, status `at1_from_reconciliation`. B.4: the comment on the `joint_gap` branches. Amendments 51 to 54, the 06d decisions in `decisions/section_6_review.md`, `docs/METHODS.md`, OPEN-47.
- **6.7** readme, league tables and dashboard test (51f3f45). 06c B.2, B.3 and B.4, and 06d B.3.
- **6.8** build check (1588a2a). Only `spec_log.csv` moved, its `run_utc` now the date of the 6.7 commit.

## Evidence

### E6.6b-a: the 3 hand check sheets against the pipeline

2025-12-31, cluster group, underlying basis, EUR. Each sheet is evaluated with pycel, as in `test_hand_check`. INGA has both gaps, so its sheet tests the joint formula on 2 gaps. Every difference is below EUR 0.50, within `hand_check_tol_eur`.

```
bank  group    line                                        sheet EUR       pipeline EUR       diff
LLOY  cluster  delta_pi_eur cost_income             4,404,501,377.46   4,404,501,377.00     0.4567
LLOY  cluster  joint_delta_pi_eur                   4,404,501,377.46   4,404,501,377.00     0.4567
INGA  cluster  delta_pi_eur cost_income             2,988,753,379.64   2,988,753,380.00    -0.3607
INGA  cluster  delta_pi_eur risk_adj_nim            6,081,719,060.76   6,081,719,061.00    -0.2368
INGA  cluster  joint_delta_pi_eur                   6,537,127,779.51   6,537,127,780.00    -0.4950
SWED  cluster  delta_pi_eur risk_adj_nim              293,668,355.39     293,668,355.40    -0.0143
SWED  cluster  joint_delta_pi_eur                     293,668,355.39     293,668,355.40    -0.0143
```

### E6.6b-b: CAG at1_instruments and their pages

All 4 pass provenance (check 1). The 2024-12-31 value, 7,218, is also in the equity statement cited for at1_in_equity, so both pages are printed below the entries.

```
2024-12-31 (7,218) 7218000000 CAG_pillar3_2024-12-31.pdf page 69 977eda77a688 at1_from_reconciliation
    (-) AT1 instruments accounted as equity (7,218) (7,218) (7,220) (7,220)
2025-06-30 (8 612) 8612000000 CAG_pillar3_2025-06-30.pdf page 5 051e8846912f at1_from_reconciliation
    (-) AT1 instruments accounted as equity (8 612) (8 612) (7 218) (7 218)
2025-12-31 (8,143) 8143000000 CAG_pillar3_2025-12-31.pdf page 243 fbea4477bdcc at1_from_reconciliation
    (-) AT1 instruments accounted as equity (8,143) (8,143) (7,218) (7,218)
2026-06-30 (8 020) 8020000000 CAG_pillar3_2026-06-30.pdf page 90 11ee1c86d9bd at1_from_reconciliation
    (-) AT1 instruments accounted as equity (8 020) (8 020) (8 143) (8 143)

CAG_half_year_2025-06-30.pdf page 12 (cited for at1_in_equity): Equity at 31 December 2024 / 13,183 / 115,125 / (458) / 7,218
CAG_pillar3_2024-12-31.pdf page 69: (-) AT1 instruments accounted as equity / (7,218) / (7,218) / (7,220) / (7,220)
```

### E6.6b-c: CAG's joint RoTE gap at 2026-06-30

Still blank. at1_instruments is now filled at all 4 dates, so RoTE's missing input moves to intangibles_deduction, which CAG lacks in the report family at every date, since it is CC1 row 8 (OPEN-47). The same pages print "Goodwills and intangible assets", 19,143, 19,309, 19,604 and 20,747 (EUR m). That was not entered, because 06d B.2 covers at1_instruments only. CAG is on the scope list, so the headline is not affected either way.

```
date bank_id    joint_eur  joint_rote_pts
2026-06-30     CAG 1.668966e+10             NaN
      date  kpi  value                              status
2024-12-31 rote    NaN       missing_input:tangible_equity
2025-06-30 rote    NaN    missing_input:profit_to_ordinary
2025-12-31 rote    NaN missing_input:intangibles_deduction
2026-06-30 rote    NaN missing_input:intangibles_deduction
```

### E6.6b-d: `test_hand_check` at the final commit

```
LLOY cluster 
INGA cluster 
SWED cluster 
.
1 passed in 223.81s (0:03:43)
```

### E6.7a: the final README

14,844 bytes. With every B.2 and B.3 change it came to 15,051 bytes, over the 15,000 that `test_tables_match` allows. So, by B.2 item 5, Q5 lists only the 29 fields at least 15 banks report, and its callout says 6 are left out.

````
# Bank Performance Benchmarking

[![ci](https://github.com/uty101/Bank-Performance-Benchmarking/actions/workflows/ci.yml/badge.svg)](https://github.com/uty101/Bank-Performance-Benchmarking/actions/workflows/ci.yml) 65 tests

This project benchmarks 31 European banks against peers with a similar business model, sizes each gap in euros and RoTE points, and explains it with 7 drivers.
<!-- table:headline start -->
At 2026-06-30, outside the banks whose scope differs between sources, the largest joint gap to the best quartile is INGA's, 10.20 points of RoTE or EUR 6,926m a year, and a point of RoTE added 0.104x of price to tangible book at the end of 2025, against 0.045x at the end of 2022.
<!-- table:headline end -->

See `outputs/reports/` for the 31 bank profiles, `outputs/tables/` for every table, and run `streamlit run bpb/dashboard.py` for the dashboard.

## What it does

It joins EBA transparency data, used to 2025-06-30, to figures hand entered from each bank's own reports, with every figure checked against the cached page it came from. From those it computes 20 KPIs from FY2021 to H1 2026, forms peer groups by business model, and measures each bank against the best quartile of its peers. It then says which gaps are larger than the noise, what they are worth, which drivers explain RoTE, and how the market prices RoTE.

## How to run it

```
uv venv --python 3.12
uv pip install -r requirements-lock.txt
uv pip install -e . --no-deps
bpb build
streamlit run bpb/dashboard.py
bpb trace <lineage_id>
```

`bpb build` rebuilds every output from `data/raw/` and `data/manual/`, with no network, and takes about 6 minutes. `bpb trace` prints the chain behind a figure, down to the EBA item or the report page. The dashboard shows the ID of every figure.

## Results

All results are at 2026-06-30, on the cluster group and the underlying basis, unless they say otherwise.

### Q1: where does each bank sit?

<!-- table:q1 start -->
NatWest Group leads on RoTE at 19.91% and Bankinter on cost to income at 35.30%. On RoTE, 3 banks are leading their peers and 10 are lagging. The table below ranks 22 banks on RoTE and 31 on cost to income, the rest being blank at this date. Each verdict is against the bank's own cluster, named beside it, so the ranks and verdicts need not agree.

| Rank | RoTE: bank | Cluster | RoTE | Verdict | Cost to income: bank | Cluster | Cost to income | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | NatWest Group | 2 | 19.91% | leading | Bankinter | 2 | 35.30% | leading |
| 2 | BBVA | 2 | 19.08% | leading | KBC Group | 2 | 37.32% | leading |
| 3 | Banca Monte dei Paschi di Siena | 2 | 18.71% | in_line | BBVA | 2 | 38.81% | leading |
| 4 | HSBC Holdings | 1 | 18.04% | leading | DNB Bank | 2 | 39.04% | leading |
| 5 | Intesa Sanpaolo | 2 | 17.99% | in_line | Intesa Sanpaolo | 2 | 39.44% | leading |
| 6 | Nordea Bank | 2 | 17.55% | in_line | CaixaBank | 2 | 39.58% | in_line |
| 7 | Banco Santander | 2 | 17.41% | in_line | Banco Santander | 2 | 41.26% | in_line |
| 8 | CaixaBank | 2 | 17.01% | in_line | Swedbank | 2 | 41.66% | in_line |
| 9 | Banco BPM | 2 | 16.98% | in_line | Danske Bank | 2 | 44.96% | in_line |
| 10 | KBC Group | 2 | 16.85% | in_line | UniCredit | 2 | 45.74% | in_line |
| 11 | Skandinaviska Enskilda Banken | 2 | 14.66% | lagging | Skandinaviska Enskilda Banken | 2 | 45.98% | in_line |
| 12 | Danske Bank | 2 | 14.51% | lagging | Unicaja Banco | 2 | 46.05% | in_line |
| 13 | Banco Sabadell | 2 | 14.32% | lagging | Nordea Bank | 2 | 46.24% | in_line |
| 14 | ING Groep | 2 | 13.80% | lagging | HSBC Holdings | 1 | 46.43% | leading |
| 15 | Lloyds Banking Group | 2 | 13.45% | lagging | Svenska Handelsbanken | 2 | 47.22% | lagging |
| 16 | Barclays | 1 | 12.99% | in_line | Banco BPM | 2 | 47.82% | lagging |
| 17 | BNP Paribas | 1 | 12.87% | in_line | NatWest Group | 2 | 48.34% | lagging |
| 18 | Société Générale | 1 | 11.30% | lagging | Banco Sabadell | 2 | 49.01% | lagging |
| 19 | Deutsche Bank | 1 | 11.12% | lagging | Santander UK Group Holdings | 2 | 53.05% | lagging |
| 20 | ABN AMRO Bank | 2 | 9.80% | lagging | ING Groep | 2 | 53.17% | lagging |
| 21 | Rabobank | 2 | 8.98% | lagging | Rabobank | 2 | 54.02% | lagging |
| 22 | Santander UK Group Holdings | 2 | 6.43% | lagging | BPER Banca | 2 | 54.55% | lagging |
| 23 |  |  |  |  | Commerzbank | 2 | 55.51% | lagging |
| 24 |  |  |  |  | Barclays | 1 | 57.92% | in_line |
| 25 |  |  |  |  | Crédit Agricole Group | 2 | 58.84% | lagging |
| 26 |  |  |  |  | Lloyds Banking Group | 2 | 59.03% | lagging |
| 27 |  |  |  |  | BNP Paribas | 1 | 59.75% | in_line |
| 28 |  |  |  |  | Banca Monte dei Paschi di Siena | 2 | 59.81% | lagging |
| 29 |  |  |  |  | Société Générale | 1 | 60.07% | lagging |
| 30 |  |  |  |  | ABN AMRO Bank | 2 | 60.71% | lagging |
| 31 |  |  |  |  | Deutsche Bank | 1 | 62.68% | lagging |
<!-- table:q1 end -->

### Q2: which gaps are larger than the noise, and what are they worth?

<!-- table:q2 start -->
10 banks have the largest joint gaps, led by CAG at EUR 16,690m. Min and max run over the 3 peer groups and 2 bases, and the joint figure closes every sized gap at once, so it can be less than the sum of the bank's rows. Amounts are EUR m of annual pre tax profit. NIM and cost of risk are sized together as a risk adjusted margin, because a high cost of risk is the price of a high margin.

| Bank | Gap | Headline | Min | Max | Joint | Joint RoTE pts | Scope |
|---|---|---|---|---|---|---|---|
| CAG | Risk adjusted NIM | 16,221 | 14,536 | 16,221 | 16,690 |  | yes |
| CAG | Cost to income | 7,154 | 6,525 | 7,154 | 16,690 |  | yes |
| INGA | Risk adjusted NIM | 6,943 | 5,920 | 6,943 | 6,926 | 10.20 |  |
| INGA | Cost to income | 2,845 | 2,476 | 2,845 | 6,926 | 10.20 |  |
| BARC | Risk adjusted NIM | 4,723 | 4,723 | 11,782 | 4,723 | 5.88 |  |
| LLOY | Cost to income | 4,189 | 2,324 | 4,244 | 4,189 | 7.62 |  |
| DBK | Cost to income | 3,658 | 3,043 | 6,869 | 3,658 | 4.72 |  |
| GLE | Cost to income | 2,339 | 1,882 | 5,093 | 3,411 | 5.01 | yes |
| GLE | Risk adjusted NIM | 2,214 | 2,214 | 5,790 | 3,411 | 5.01 | yes |
| ABN | Risk adjusted NIM | 2,260 | 1,817 | 2,260 | 3,105 | 9.77 |  |
| ABN | Cost to income | 1,776 | 1,653 | 1,778 | 3,105 | 9.77 |  |
| DANSKE | Risk adjusted NIM | 2,209 | 1,866 | 2,209 | 2,209 | 7.71 | yes |
| RABO | Cost to income | 2,139 | 1,829 | 2,139 | 2,139 | 3.09 |  |
| NDA | Risk adjusted NIM | 2,226 | 1,779 | 2,226 | 1,900 | 5.31 | yes |
| NDA | Cost to income | 592 | 437 | 760 | 1,900 | 5.31 | yes |
<!-- table:q2 end -->

### Q3: which drivers explain the RoTE gap?

Decomposition explains where a RoTE gap comes from, and business mix is a legitimate part of that, while sizing in Q2 is where mix must not count as opportunity.

<!-- table:q3 start -->
Of the banks with a decomposition at 2026-06-30, RABO sits furthest from its peer median, -7.31 points, and its largest step is assets / tangible equity at -5.66 points. Each row runs from the reference RoTE, every driver at the peer median, to the bank's RoTE, in points.

| Bank | Gap to median | Reference | NII / assets | Fees / assets | Other income / assets | Costs / assets | Credit losses / assets | Tax rate | Assets / tangible equity | Other below the line | Minorities and AT1 | Bank RoTE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RABO | -7.31 | 15.86 | +4.12 | -2.81 | +0.38 | -2.36 | -0.60 | +0.17 | -5.66 | +0.29 | -0.40 | 8.98 |
| ABN | -6.49 | 16.23 | -1.75 | -0.88 | -2.65 | -1.02 | +1.71 | -0.16 | -1.04 | +0.29 | -0.92 | 9.80 |
| HSBA | +5.97 | 14.38 | +4.58 | -1.01 | +3.26 | +1.63 | -0.12 | +0.60 | -5.81 | +1.66 | -1.13 | 18.04 |
| NWG | +4.20 | 14.94 | +4.25 | -4.38 | -1.82 | +1.73 | +0.83 | +0.36 | +4.82 | +0.28 | -1.09 | 19.91 |
| BBVA | +3.37 | 15.40 | +21.73 | +5.52 | +0.78 | -7.53 | -8.20 | -1.41 | -4.92 | -0.34 | -1.94 | 19.08 |
<!-- table:q3 end -->

### Q4: what is a point of RoTE worth?

<!-- table:q4 start -->
β rose from 4.50 in 2022 to 10.43 in 2025, the first and last years with a significant β, and the implied cost of equity went from 24.22% to 11.58%. The cost of equity is blank in 2021, where the 90% interval of β contains 0. The test that the year slopes are equal is rejected: F(4, 26) = 10.00, p = 0.00005, over 120 bank years. So 1 pooled slope is the wrong model for anything but the significance gate, and the choice of slope matters: LLOY's uplift at the end of 2025 is +0.84x on that year's β and +0.28x on the pooled β. The figure below shows 2025, the tightest fit.

| Year | β | R² | n | Implied CoE |
|---|---|---|---|---|
| 2021 | 1.05 | 0.09 | 22 | blank |
| 2022 | 4.50 | 0.48 | 23 | 24.22% |
| 2023 | 4.53 | 0.40 | 25 | 24.09% |
| 2024 | 6.63 | 0.55 | 25 | 17.08% |
| 2025 | 10.43 | 0.74 | 25 | 11.58% |

![P/TBV against RoTE](outputs/figures/valuation_2025.png)
<!-- table:q4 end -->

### Q5: how far apart are the 2 sources?

<!-- table:q5 start -->
Fields the 2 sources define alike agree closely: the median absolute difference is 0.00% for loans and 0.02% for profit after tax. Total assets differ by a median of 8.54%, because the supervisory scope leaves out entities such as insurers. Small residual lines differ the most, since each source draws them differently. The table covers 2025-06-30, the date both sources report, and lists the 29 fields that at least 15 banks report, leaving out 6.

| Field | Banks | Median | 90th percentile |
|---|---|---|---|
| admin_expenses | 26 | 1.91% | 13.08% |
| at1_instruments | 23 | 0.99% | 4.08% |
| cash_cb | 25 | 2.94% | 12.21% |
| debt_securities | 24 | 0.00% | 0.00% |
| deposits_customers | 23 | 2.04% | 9.15% |
| depreciation | 21 | 1.14% | 6.75% |
| dividend_income | 15 | 0.70% | 62.13% |
| gains_derecognition_not_fvtpl | 18 | 36.35% | 149.02% |
| gains_held_for_trading | 26 | 33.47% | 305.20% |
| impairments_fin | 26 | 3.34% | 87.21% |
| intangibles_deduction | 22 | 0.00% | 0.05% |
| interest_expense | 26 | 0.97% | 23.33% |
| interest_income | 26 | 1.33% | 12.30% |
| loans_all | 24 | 0.00% | 0.00% |
| loans_customers_allowance | 24 | 0.00% | 0.03% |
| loans_customers_gross | 24 | 0.00% | 0.00% |
| loans_households_gross | 24 | 0.00% | 0.00% |
| net_fees | 26 | 0.80% | 14.41% |
| npl_allowance | 24 | 0.00% | 0.02% |
| npl_gross | 24 | 0.00% | 0.01% |
| other_operating_net | 26 | 127.58% | 1093.47% |
| pat | 26 | 0.02% | 2.81% |
| pbt | 26 | 0.46% | 5.00% |
| profit_owners | 26 | 0.01% | 2.29% |
| total_assets | 25 | 8.54% | 16.65% |
| total_equity | 24 | 0.02% | 1.41% |
| total_liabilities | 19 | 9.89% | 17.47% |
| total_operating_income | 26 | 3.12% | 7.86% |
| trading_assets | 17 | 0.40% | 59.54% |

**Bank insurer scope.** NDA, DANSKE, SWED, SEB, SHB, KBC, BNP, GLE, CAG, BAMI, CABK, DNB, ISP, UCG carry a scope difference between the 2 sources, as bank insurers or with a total assets seam above 5%. For ISP and KBC, the income statement lines were read line by line and every one sits in the right field, so the size of other below the line is the insurance effect: -7.85 points of RoTE for ISP and -10.11 for KBC at 2026-06-30. The same treatment flatters their cost to income.
<!-- table:q5 end -->

## Peer groups

<!-- table:peers start -->
The clustering splits the 31 banks into 5 and 26. The 5 are BARC, BNP, DBK, GLE, HSBA: global banks, far larger than the rest, with a much higher share of trading assets and a lower share of loans. Everyone else, from Lloyds to Unicaja, is 1 broad group of retail and commercial banks, so the cluster says more about what the global banks are than about how the others differ. That is why every sized gap is shown with its range across the 3 groups. The silhouette is 0.29, and mean stability is 0.57 for the 5 bank cluster and 0.78 for the other.
<!-- table:peers end -->

## Caveats

- **Accounting scope.** Bank insurers report insurance lines that the supervisory scope leaves out, so their cost and income ratios are not like for like.
- **FX inside averages.** Averages and rolling figures of EBA balances for the 5 non EUR banks carry the currency move between their 2 ends.
- **The 2 seams.** Seam 1 sets EBA capital against Pillar 3, and seam 2 sets EBA against the banks' own reports. EBA feeds the history and reports the latest dates, so no time comparison crosses the switch, and such a cell is blank with status `family_switch`.
- **One offs.** Underlying figures adjust only for what each bank discloses, never for judgement.
- **Broad cluster 2.** The cluster group for most banks is broad, so read every sized gap with its range across the 3 groups.
- **Small peer groups.** Market groups hold few banks, intervals are wide, and a group that is too small gives no benchmark.
- **Valuation slope.** The slope changes every year, so an uplift holds only at the date of its fit.
- **BMPS prices.** Earlier BMPS prices may carry a rights issue adjustment that `Stock Splits` does not undo. It touches no P/TBV, since BMPS's 2021 TBV per share is blank.
<!-- table:headcount start -->
- **Headcount.** 9 banks publish only headcount, which stands in for FTE.
<!-- table:headcount end -->
<!-- table:coverage start -->
- **Coverage.** 97 of 620 KPI cells are blank at 2026-06-30 on the underlying basis, because an input is not published or not comparable. The largest causes are customers (27), fte (24), mixed_family (8).
<!-- table:coverage end -->

## What it does not do

- It does not forecast. Every figure is historical, and a sized gap says what a bank would earn at peer levels on today's balance sheet.
- It does not say a gap can be closed. Some gaps are structural, and the peer grouping reduces that without removing it.
- It does not harmonise accounting across countries beyond what FINREP and Pillar 3 already standardise. The seam table shows the difference that remains.
- It does not adjust for one offs on judgement, only for those the bank itself discloses.
- It does not cover banks outside the 7 markets, or smaller banks outside the EBA sample.
- It does not give investment advice. The valuation describes a cross sectional relationship with its uncertainty, not a target price.

## Repository map

- `bpb/`: the package: ingestion, KPIs, checks, peers, benchmarks, gaps, drivers, valuation, reports, trace and the dashboard.
- `config/`: field, KPI and source maps. `config.toml` holds every parameter.
- `data/raw/`: pulled data, the cached report pages and their hashes.
- `data/manual/`: hand entered figures, one offs, mergers and the universe.
- `docs/`: `METHODS.md` and the resolved conventions.
- `outputs/`: profiles, figures and tables, all rebuilt by `bpb build`.
- `project_outline/`: the original outline.
- `scripts/`: data pulls and the README table writer.
- `tests/`: the test suite, which runs offline.
- `instructions/`, `review/`, `decisions/` and `PLAN.md`: the build record.
````

### E6.7b: 1 cluster league CSV

`outputs/tables/league_rote_cluster_2026-06-30.csv`. The rank restarts at 1 in each cluster, and a blank value keeps its row at the end of its cluster, with no rank.

```
rank,cluster,bank_id,name,value,verdict,inside_noise,status
1,1,HSBA,HSBC Holdings,0.1804393503,leading,False,short_history
2,1,BARC,Barclays,0.1299357126,in_line,True,short_history
3,1,BNP,BNP Paribas,0.1286840444,in_line,True,family_switch
4,1,GLE,Société Générale,0.1130067157,lagging,False,short_history
5,1,DBK,Deutsche Bank,0.1111670976,lagging,False,family_switch
1,2,NWG,NatWest Group,0.1990902912,leading,False,ok
2,2,BBVA,BBVA,0.1907909977,leading,False,family_switch
3,2,BMPS,Banca Monte dei Paschi di Siena,0.1870500564,in_line,True,family_switch
4,2,ISP,Intesa Sanpaolo,0.179910862,in_line,True,family_switch
5,2,NDA,Nordea Bank,0.1755164088,in_line,True,short_history
6,2,SAN,Banco Santander,0.1741288538,in_line,True,family_switch
7,2,CABK,CaixaBank,0.1701318667,in_line,True,family_switch
8,2,BAMI,Banco BPM,0.169794497,in_line,True,family_switch
9,2,KBC,KBC Group,0.168533708,in_line,True,family_switch
10,2,SEB,Skandinaviska Enskilda Banken,0.1466175988,lagging,False,family_switch
11,2,DANSKE,Danske Bank,0.1450961496,lagging,False,family_switch
12,2,SAB,Banco Sabadell,0.1431662651,lagging,False,family_switch
13,2,INGA,ING Groep,0.138017135,lagging,False,family_switch
14,2,LLOY,Lloyds Banking Group,0.1345007663,lagging,False,ok
15,2,ABN,ABN AMRO Bank,0.09797875985,lagging,False,family_switch
16,2,RABO,Rabobank,0.08977790852,lagging,False,family_switch
17,2,SANUK,Santander UK Group Holdings,0.06433013467,lagging,False,ok
,2,BKT,Bankinter,,,,mixed_family;short_history
,2,BPE,BPER Banca,,,,missing_input:at1_coupons;short_history
,2,CAG,Crédit Agricole Group,,,,missing_input:intangibles_deduction;short_history
,2,CBK,Commerzbank,,,,missing_input:at1_instruments;short_history
,2,DNB,DNB Bank,,,,missing_input:at1_instruments;family_switch
,2,SHB,Svenska Handelsbanken,,,,missing_input:intangibles_deduction;family_switch
,2,SWED,Swedbank,,,,missing_input:minority_interests;family_switch
,2,UCG,UniCredit,,,,missing_input:at1_instruments;family_switch
,2,UNI,Unicaja Banco,,,,mixed_family;family_switch
```

### E6.8: build check and CI

The first build after step 6.7 moved only `spec_log.csv`, committed as step 6.8. The second build, at 1588a2a:

```
build exit 0
git status --porcelain: 0 lines
```

CI on 1588a2a:

```
success 1588a2a1e3bb039ac4f45131029111d1397a8f32 (run 42613178468)
65 passed, 214 warnings in 790.70s (0:13:10)
```

## Tests run

The full suite, `pytest -p socket --disable-socket -q`, passed before each commit: 62 at 6.6b and 65 at 6.7. ruff is clean. The 6.6b run took 47 hours of wall time, because the machine slept during it, so its timing says nothing about the code.

## Fresh-clone check

Clone path `C:/bpbs6e`, with the commands of rule 12, plus ruff. Full output:

```
1588a2a step 6.8: build check
install ok
All checks passed!
ruff exit 0
.................................................................        [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\_pytest\config\__init__.py:894
  C:\bpbs6e\.venv\Lib\site-packages\_pytest\config\__init__.py:894: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; socket
    self.import_plugin(arg, consider_entry_points=True)

tests/test_dashboard.py: 69 warnings
  C:\bpbs6e\.venv\Lib\site-packages\streamlit\elements\lib\built_in_chart_utils.py:620: Pandas4Warning: The inplace keyword in DataFrame.reset_index is deprecated and will be removed in a future version (PDEP-8).
  See https://pandas.pydata.org/docs/dev/whatsnew/v3.1.0.html#deprecation-inplace for more details.
    df.reset_index(inplace=True)  # noqa: PD002

tests/test_dashboard.py::test_dashboard_no_external
  C:\bpbs6e\.venv\Lib\site-packages\pytest_socket\__init__.py:365: UserWarning: A test tried to use socket.socket.connect() with host "2606:4700:10::6814:179a" (allowed: "127.0.0.1").
    raise SocketConnectBlockedError(allowed_list, host)

tests/test_gaps.py: 72 warnings
  C:\bpbs6e\.venv\Lib\site-packages\pycel\excelformula.py:995: DeprecationWarning: ast.Str is deprecated and will be removed in Python 3.14; use ast.Constant instead
    op = ast.Str(s=type(node_op).__name__)

tests/test_gaps.py: 71 warnings
  C:\Users\astha\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none\Lib\ast.py:587: DeprecationWarning: Attribute s is deprecated and will be removed in Python 3.14; use value instead
    return Constant(*args, **kwargs)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
65 passed, 214 warnings in 1692.83s (0:28:12)
pytest exit 0
```

## Deviations from PLAN.md

1. **Q5 lists 29 of 35 fields**, by 06c B.2 item 5 (E6.7a).
2. **The headline** names INGA, 10.20 points and EUR 6,926m. The valuation clause now takes its first year from the fits, as the first year with a significant β, which is still 2022.
3. **Q4** reads "β rose from 4.50 in 2022 to 10.43 in 2025, the first and last years with a significant β". The implied cost of equity is now 2 decimals in the text, the table and `answers.csv` (Convention 4.7).
4. **`answers.csv`** has a second Q2 row for the headline bank. The Q1 sources read "largest value" and "lowest value", since rank 1 in a cluster file is now 1 per cluster.
5. **The page text cache** for the 4 cited CAG Pillar 3 documents was rebuilt with `scripts/fetch_reports.py --cache-pages`, which uses no network. Without it, the 4 entries failed provenance with "page not in cache".
6. **The venv left the lock once.** An early `uv run` synced 9 packages to newer versions, including pandas 3.1.1. I reinstalled from `requirements-lock.txt`, deleted the `uv.lock` it created, and rebuilt. Nothing built on those versions was committed.
7. **`test_dashboard_runs`** also asserts that each selection took, and `test_dashboard_no_external` expects `SocketConnectBlockedError`, the error pytest-socket raises.
8. **README limitations** keep "The slope changes every year". That bullet is about the F test, not Q4's wording.

## Not verified

Nothing left open from 06c. CI on Linux passed the dashboard test with the loopback marker, so the 06c concern about Linux is closed.

## Open questions

1. **OPEN-47:** enter CAG's printed "Goodwills and intangible assets" as intangibles_deduction, or leave CAG's RoTE blank? Option (a) would fill CAG's RoTE and joint RoTE gap.

## Files changed

6.6b: `CLAUDE.md`, `README.md`, `bpb/gaps.py`, `bpb/ingest.py`, `bpb/kpi.py`, `config.toml`, `data/manual/report_entries.csv`, 4 files in `data/raw/report_text/`, `decisions/OPEN.md`, `decisions/section_6_review.md`, `docs/METHODS.md`, `tests/fixtures/hand_check.xlsx`, rebuilt outputs. 6.7: `README.md`, `bpb/answers.py`, `bpb/dashboard.py`, `bpb/report.py`, `scripts/write_readme_tables.py`, `tests/test_gaps.py`, `tests/test_dashboard.py` (new), `outputs/tables/answers.csv`, the 36 cluster league CSVs and 18 league HTML pages, `outputs/tables/spec_log.csv`. 6.8: `outputs/tables/spec_log.csv`.

## Reviewer reads

1. `instructions/06d_section_6_finish.status.md`
2. E6.6b-c and `decisions/OPEN.md` OPEN-47
3. E6.7a, the README

---

# Instruction 06e (step 6.9)

**Stopped** under rules 4 and 5 at step 6.9. Instruction 06e B is applied and committed (849b84c), but README.md is 15,332 bytes. So `test_tables_match` fails on its size check, `assert 15332 < 15000`, and 06e says it passes unchanged (OPEN-48). Every other test passes, including `test_no_dashes`. `main` was already red before this step: commit f28cfae's badges took the README to 15,020 bytes (CI run 42833253149).

## Step completed, as far as the stop

- **6.9** readme lead (849b84c). B.1: `_headline` writes the bold result and the valuation sentence, using the universe's `name` column and the date in words. The shared sentence is `headline_claim` in `bpb/answers.py`. B.2: the opening sentence moves below the headline markers. B.3: the data line follows the outputs pointer. B.4: `answers.csv`'s headline row uses the same wording. OPEN-48 is in `decisions/OPEN.md`.
- **Not done:** the second `bpb build` check (C.3). The commit moves the date of the last input commit, so the next build will move `spec_log.csv`'s `run_utc`, as in step 6.8. That build check waits for the decision on OPEN-48.

## Evidence

### E6.9a: the README's first 15 lines, 15,332 bytes

```text
# Bank Performance Benchmarking

[![ci](https://github.com/uty101/Bank-Performance-Benchmarking/actions/workflows/ci.yml/badge.svg)](https://github.com/uty101/Bank-Performance-Benchmarking/actions/workflows/ci.yml) ![tests](https://img.shields.io/badge/tests-65%20passing-brightgreen) ![python](https://img.shields.io/badge/python-3.12-blue) ![licence](https://img.shields.io/badge/licence-MIT-blue)

<!-- table:headline start -->
**At 30 June 2026, ING Groep has the largest gap to the best quartile of its peers: 10.20 RoTE points, or EUR 6,926m of annual pre tax profit.** Each RoTE point was worth 0.104x of price to tangible book at the end of 2025, against 0.045x at the end of 2022, so the market now pays about 2.3 times as much for the same gap. Banks whose accounting scope differs between the 2 sources, mainly bank insurers, are left out of the headline (see Caveats).
<!-- table:headline end -->

This project benchmarks 31 European banks against peers with a similar business model, sizes each gap in euros and RoTE points, and explains it with 7 drivers.

See `outputs/reports/` for the 31 bank profiles, `outputs/tables/` for every table, and run `streamlit run bpb/dashboard.py` for the dashboard.

Data: EBA EU wide transparency exercise, the banks' own annual, half year and Pillar 3 reports, ECB exchange rates and Yahoo Finance prices.

## What it does
```

The ratio is 10.4334 ÷ 4.4999 = 2.32, from the unrounded slopes in `valuation_fits.csv`, shown to 1 decimal as 2.3.

### E6.9b: the size against Q5's threshold

With the 06e text in place, measured with `scripts/write_readme_tables.py`:

| `Q5_MIN_BANKS` | README bytes |
|---|---|
| 15 (as now) | 15,332 |
| 20 | 15,148 |
| 22 | 15,110 |
| 24 | 14,978 |
| 25 | 14,644 |

### E6.9c: the answers.csv headline row

```text
2,"At 30 June 2026, ING Groep has the largest gap to the best quartile of its peers: 10.20 RoTE points, or EUR 6,926m of annual pre tax profit. Banks whose accounting scope differs between the 2 sources are left out.","gaps_joint.csv, date == 2026-06-30, group == cluster, basis == underlying, bank_id not in the scope list, largest joint_rote_pts"
```

### E6.9d: CI on 849b84c

Run 42842974012, `failure`:

```text
FAILED tests/test_readme.py::test_tables_match - assert 15332 < 15000
1 failed, 64 passed, 214 warnings in 515.37s (0:08:35)
```

## Tests run

The full suite, `pytest -p socket --disable-socket -q`, before the commit: 1 failed, 64 passed. The 1 failure is `test_tables_match`, on the size check only. The README blocks match the build. ruff is clean.

## Fresh-clone check

Clone path `C:/bpbs6f`, with the commands of rule 12, plus ruff. Full output:

```text
849b84c step 6.9: readme lead (stopped: README over 15 KB, OPEN-48)
installed
E       assert 15332 < 15000
FAILED tests/test_readme.py::test_tables_match - assert 15332 < 15000
1 failed, 64 passed, 214 warnings in 1017.68s (0:16:57)
All checks passed!
```

## Deviations from PLAN.md

1. **The valuation multiples** keep 3 decimals, 0.104x and 0.045x, as before. 06e B.1 says "everything else is as now". At 2 decimals they would read 0.10x and 0.05x, and the ratio would no longer follow from the printed figures.
2. **The answers.csv headline row** ends "Banks whose accounting scope differs between the 2 sources are left out.", so the claim states the scope rule its source column applies.

## Open questions

1. **OPEN-48 (blocking):** raise `Q5_MIN_BANKS` to 24, leaving 22 bytes of headroom, or raise the test's 15 KB limit?

## Files changed

`README.md`, `bpb/answers.py`, `scripts/write_readme_tables.py`, `outputs/tables/answers.csv`, `decisions/OPEN.md`.

## Reviewer reads

1. `instructions/06e_readme_lead.status.md`
2. OPEN-48 in `decisions/OPEN.md`, and E6.9b
3. E6.9a
