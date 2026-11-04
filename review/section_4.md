# Section 4

**Stopped under rule 4 at step 4.1.** No k qualifies for the 2024 clusters (kickoff 5.4, OPEN-36). Step 3.8 is complete, so Section 3 is closed. Steps 4.2, 4.3 and 4.4 are not built.

## Steps completed

3.8 section 3 review decisions: OPEN-34 and OPEN-35 applied, rote recomputed, amendments 28 to 32 added (da5d6e6)
4.1 peer features, clusters and stability: code and tests complete, `peers.csv` not written because of the stop (606dcb0)
Open questions OPEN-36 to OPEN-38 (ab3f25f)
4.2 not started
4.3 not started
4.4 not started

## Evidence

### E3.8a The 31 entries added in step 3.8 (value 0 in every row)

```
   bank_id    ref_date               field value_as_printed                   doc page   decision_status                                                                                                                  snippet
0     BMPS  2020-12-31         at1_coupons            blank     annual:2020-12-31  339     no_at1_coupon                                                            As at 31 December 2020, the Group held no equity instruments.
1     BMPS  2021-06-30         at1_coupons            blank     annual:2021-12-31  353     no_at1_coupon                                                            As at 31 December 2021, the Group held no equity instruments.
2     BMPS  2021-12-31         at1_coupons            blank     annual:2021-12-31  353     no_at1_coupon                                                            As at 31 December 2021, the Group held no equity instruments.
3     BMPS  2022-06-30         at1_coupons            blank     annual:2022-12-31  348     no_at1_coupon                                                            As at 31 December 2022, the Group held no equity instruments.
4     BMPS  2022-12-31         at1_coupons            blank     annual:2022-12-31  348     no_at1_coupon                                                            As at 31 December 2022, the Group held no equity instruments.
5     BMPS  2023-06-30         at1_coupons            blank     annual:2023-12-31  310     no_at1_coupon              As at 31 December 2023, as in the financial year used for comparison, the Group held no equity instruments.
6     BMPS  2023-12-31         at1_coupons            blank     annual:2023-12-31  310     no_at1_coupon              As at 31 December 2023, as in the financial year used for comparison, the Group held no equity instruments.
7     BMPS  2024-06-30         at1_coupons            blank     annual:2024-12-31  471     no_at1_coupon              As at 31 December 2024, as in the financial year used for comparison, the Group held no equity instruments.
8     BMPS  2024-12-31         at1_coupons            blank     annual:2024-12-31  471     no_at1_coupon              As at 31 December 2024, as in the financial year used for comparison, the Group held no equity instruments.
9     BMPS  2025-06-30         at1_coupons            blank     annual:2025-12-31  524     no_at1_coupon       As at 31 December 2025, as in the (cid:470)nancial year used for comparison, the Group held no equity instruments.
10    BMPS  2025-12-31         at1_coupons            blank     annual:2025-12-31  524     no_at1_coupon       As at 31 December 2025, as in the (cid:470)nancial year used for comparison, the Group held no equity instruments.
11    BMPS  2026-06-30         at1_coupons            blank     annual:2025-12-31  524     no_at1_coupon       As at 31 December 2025, as in the (cid:470)nancial year used for comparison, the Group held no equity instruments.
12     NDA  2026-06-30         at1_coupons                -  half_year:2026-06-30   37     no_at1_coupon                                                                     Paid interest on Additional Tier 1 capital - -26 -26
13   SANUK  2022-06-30  minority_interests                —  half_year:2023-06-30   59  from_comparative                                                             At 30 June 2022 7,060 2,196 21 (669) 2 7,339 15,949 — 15,949
14   SANUK  2022-12-31  minority_interests                —     annual:2023-12-31  186  from_comparative                                                        At 31 December 2022 7,060 2,196 6 (1,116) 2 6,563 14,711 — 14,711
15   SANUK  2023-06-30  minority_interests            blank  half_year:2024-06-30   55  from_comparative                                                                     At 30 June 2023 7,060 2,196 3 (1,168) 2 6,820 14,913
16   SANUK  2023-12-31  minority_interests                —     annual:2024-12-31  171  from_comparative                                                        At 31 December 2023 7,060 2,196 (5) (334) 2 6,047 14,966 — 14,966
17   SANUK  2024-12-31  minority_interests            blank     annual:2025-12-31  163  from_comparative                                                              At 31 December 2024 7,060 2,100 (16) (311) — 2 5,258 14,093
18  DANSKE  2022-06-30  minority_interests                -  half_year:2023-06-30   38  from_comparative                                          Total equity as at 30 June 2022 8,622 -1,801 -1,270 165,224 - 170,775 - 170,775
19  DANSKE  2022-12-31  minority_interests                -     annual:2023-12-31   70  from_comparative                                      Total equity as at 31 December 2022 8,622 -2,630 -1,526 155,812 - 160,278 - 160,278
20  DANSKE  2023-06-30  minority_interests            blank  half_year:2024-06-30   32  from_comparative                                                    Total equity as at 30 June 2023 8,622 -4,903 -1,600 166,529 - 168,648
21  DANSKE  2023-12-31  minority_interests            blank     annual:2024-12-31  126  from_comparative                                              Total equity as at 31 December 2023 8,622 -2,639 -306 163,596 6,466 175,739
22     ABN  2020-12-31  minority_interests            blank     annual:2021-12-31  267  from_comparative                                              Balance at 31 December 2020 940 12,970 6,870 -1,733 -45 1,987 20,989 20,989
23     BKT  2020-12-31  minority_interests                -     annual:2020-12-31   17       no_nci_line                                                                       Minority interests [Non-controlling interests] - -
24     BKT  2021-12-31  minority_interests                -     annual:2021-12-31   15       no_nci_line                                                                       Minority interests [Non-controlling interests] - -
25     BKT  2022-12-31  minority_interests                -     annual:2022-12-31   13       no_nci_line                                                                       Minority interests [non-controlling interests] - -
26     BKT  2023-12-31  minority_interests                —     annual:2023-12-31   13       no_nci_line                                                                       Minority interests (non-controlling interests) — —
27     BKT  2024-12-31  minority_interests                —     annual:2025-12-31   14       no_nci_line                                                                       Minority interests (non-controlling interests) — —
28     BKT  2025-12-31  minority_interests                —     annual:2025-12-31   14       no_nci_line                                                                       Minority interests (non-controlling interests) — —
29     BKT  2026-06-30  minority_interests                —  half_year:2026-06-30   13       no_nci_line                                                                       MINORITY INTERESTS (non-controlling interests) — —
30     BKT  2025-06-30  minority_interests                —  half_year:2026-06-30   17  from_comparative  Closing balance at 30/06/2025 (*) 269,660 — — 17,238 5,504,166 — (9,168) (2,246) 541,693 (135,068) 25,128 — — 6,211,403
```

### E3.8b BMPS EU CC1 row 30, every entered date (OPEN-34)

```
         ref_date value_as_printed doc_type page                                                          snippet
10781  2024-12-31                -  pillar3   34  30 Capital instruments and the related share premium accounts -
10783  2025-06-30                -  pillar3   16  30 Capital instruments and the related share premium accounts -
10785  2025-12-31                -  pillar3   41  30 Capital instruments and the related share premium accounts -
10787  2026-06-30                -  pillar3   15  30 Capital instruments and the related share premium accounts -
```

### E3.8c rote, reported basis, after step 3.8 (pct)

```
bank_id      BMPS    NDA  SANUK  DANSKE    ABN    BKT
date                                                 
2021-12-31   5.28  13.60   9.85     NaN   5.88  28.33
2022-06-30   2.31    NaN  11.28     NaN   7.90    NaN
2022-12-31  -2.98    NaN  10.68     NaN   8.75  11.64
2023-06-30   5.49    NaN  11.80    0.34  11.60    NaN
2023-12-31  23.41    NaN  13.11   13.04  12.17  16.70
2024-06-30  27.19    NaN  10.80   13.40  11.74    NaN
2024-12-31  18.26    NaN   7.43   13.88  10.27  17.14
2025-06-30  15.28  18.60   6.97   13.75   9.49    NaN
2025-12-31  16.42  17.45   8.64   13.42   8.88    NaN
2026-06-30  18.71  16.87   6.43   14.51   9.79    NaN
```

### E3.8d rote status, reported basis, after step 3.8

```
bank_id                            BMPS                                      NDA                         SANUK                                  DANSKE               ABN                                       BKT
date                                                                                                                                                                                                              
2021-12-31  at1_liability;no_at1_coupon                                       ok                            ok           missing_input:tangible_equity  from_comparative  at1_liability;at1_net_of_tax;no_nci_line
2022-06-30  at1_liability;no_at1_coupon            missing_input:tangible_equity              from_comparative           missing_input:tangible_equity                ok          missing_input:profit_to_ordinary
2022-12-31  at1_liability;no_at1_coupon            missing_input:tangible_equity              from_comparative           missing_input:tangible_equity                ok  at1_liability;at1_net_of_tax;no_nci_line
2023-06-30  at1_liability;no_at1_coupon            missing_input:tangible_equity              from_comparative                             fx_combined                ok          missing_input:profit_to_ordinary
2023-12-31  at1_liability;no_at1_coupon            missing_input:tangible_equity              from_comparative                             fx_combined                ok  at1_liability;at1_net_of_tax;no_nci_line
2024-06-30  at1_liability;no_at1_coupon            missing_input:tangible_equity  from_comparative;no_nci_line                             fx_combined                ok          missing_input:profit_to_ordinary
2024-12-31  at1_liability;no_at1_coupon            missing_input:tangible_equity              from_comparative                             fx_combined                ok  at1_liability;at1_net_of_tax;no_nci_line
2025-06-30  at1_liability;no_at1_coupon                at1_liability;no_nci_line                   no_nci_line                             fx_combined                ok          missing_input:profit_to_ordinary
2025-12-31  at1_liability;no_at1_coupon                at1_liability;no_nci_line  from_comparative;no_nci_line  at1_liability;no_nci_line;coupon_in_pl                ok       missing_input:intangibles_deduction
2026-06-30  at1_liability;no_at1_coupon  at1_liability;no_nci_line;no_at1_coupon                   no_nci_line  at1_liability;no_nci_line;coupon_in_pl                ok                              mixed_family
```

### E3.8e rote, reported basis, before step 3.8 (pct)

```
bank_id     BMPS    NDA  SANUK  DANSKE    ABN  BKT
date                                              
2021-12-31   NaN  13.60   9.85     NaN    NaN  NaN
2022-06-30   NaN    NaN    NaN     NaN   7.90  NaN
2022-12-31   NaN    NaN    NaN     NaN   8.75  NaN
2023-06-30   NaN    NaN    NaN     NaN  11.60  NaN
2023-12-31   NaN    NaN    NaN     NaN  12.17  NaN
2024-06-30   NaN    NaN    NaN     NaN  11.74  NaN
2024-12-31   NaN    NaN    NaN     NaN  10.27  NaN
2025-06-30   NaN  18.60   6.97   13.75   9.49  NaN
2025-12-31   NaN  17.45    NaN   13.42   8.88  NaN
2026-06-30   NaN    NaN   6.43   14.51   9.79  NaN
```

### E3.8c rote, underlying basis, after step 3.8 (pct)

```
bank_id      BMPS    NDA  SANUK  DANSKE    ABN    BKT
date                                                 
2021-12-31   5.28  13.60  12.55     NaN   8.45  28.33
2022-06-30   2.31    NaN  12.86     NaN   7.19    NaN
2022-12-31  -2.98    NaN  13.28     NaN  10.35  11.64
2023-06-30   5.49    NaN  14.38    9.70  13.18    NaN
2023-12-31  23.41    NaN  14.71   13.04  12.71  16.70
2024-06-30  27.19    NaN  11.54   13.40  12.25    NaN
2024-12-31  18.26    NaN   7.43   13.88  10.69  17.14
2025-06-30  15.28  18.60   6.97   13.75  10.07    NaN
2025-12-31  16.42  17.45   8.64   13.42   9.13    NaN
2026-06-30  18.71  17.55   6.43   14.51   9.80    NaN
```

### E3.8d rote status, underlying basis, after step 3.8

```
bank_id                            BMPS                                      NDA                         SANUK                                  DANSKE               ABN                                       BKT
date                                                                                                                                                                                                              
2021-12-31  at1_liability;no_at1_coupon                                       ok                            ok           missing_input:tangible_equity  from_comparative  at1_liability;at1_net_of_tax;no_nci_line
2022-06-30  at1_liability;no_at1_coupon            missing_input:tangible_equity              from_comparative           missing_input:tangible_equity                ok          missing_input:profit_to_ordinary
2022-12-31  at1_liability;no_at1_coupon            missing_input:tangible_equity              from_comparative           missing_input:tangible_equity                ok  at1_liability;at1_net_of_tax;no_nci_line
2023-06-30  at1_liability;no_at1_coupon            missing_input:tangible_equity              from_comparative                             fx_combined                ok          missing_input:profit_to_ordinary
2023-12-31  at1_liability;no_at1_coupon            missing_input:tangible_equity              from_comparative                             fx_combined                ok  at1_liability;at1_net_of_tax;no_nci_line
2024-06-30  at1_liability;no_at1_coupon            missing_input:tangible_equity  from_comparative;no_nci_line                             fx_combined                ok          missing_input:profit_to_ordinary
2024-12-31  at1_liability;no_at1_coupon            missing_input:tangible_equity              from_comparative                             fx_combined                ok  at1_liability;at1_net_of_tax;no_nci_line
2025-06-30  at1_liability;no_at1_coupon                at1_liability;no_nci_line                   no_nci_line                             fx_combined                ok          missing_input:profit_to_ordinary
2025-12-31  at1_liability;no_at1_coupon                at1_liability;no_nci_line  from_comparative;no_nci_line  at1_liability;no_nci_line;coupon_in_pl                ok       missing_input:intangibles_deduction
2026-06-30  at1_liability;no_at1_coupon  at1_liability;no_nci_line;no_at1_coupon                   no_nci_line  at1_liability;no_nci_line;coupon_in_pl                ok                              mixed_family
```

### E3.8e rote, underlying basis, before step 3.8 (pct)

```
bank_id     BMPS    NDA  SANUK  DANSKE    ABN  BKT
date                                              
2021-12-31   NaN  13.60  12.55     NaN    NaN  NaN
2022-06-30   NaN    NaN    NaN     NaN   7.19  NaN
2022-12-31   NaN    NaN    NaN     NaN  10.35  NaN
2023-06-30   NaN    NaN    NaN     NaN  13.18  NaN
2023-12-31   NaN    NaN    NaN     NaN  12.71  NaN
2024-06-30   NaN    NaN    NaN     NaN  12.25  NaN
2024-12-31   NaN    NaN    NaN     NaN  10.69  NaN
2025-06-30   NaN  18.60   6.97   13.75  10.07  NaN
2025-12-31   NaN  17.45    NaN   13.42   9.13  NaN
2026-06-30   NaN    NaN   6.43   14.51   9.80  NaN
```

### E3.8f rote coverage, every bank (filled bank-dates)

```
            before  after   of
basis                         
reported       218    245  310
underlying     218    245  310
```

### E3.8g DANSKE 2023-06-30 rote of 0.34%: the rolling profit holds the H2 2022 loss (EUR)

```
            date     value    numerator   denominator      family
4294  2023-06-30  0.003379  74817678.15  2.214339e+10  eba+report
```

```
         ref_date          field family         value
10665  2022-06-30  profit_owners    eba  6.116132e+08
10751  2022-12-31  profit_owners    eba -6.801109e+08
10836  2023-06-30  profit_owners    eba  1.366544e+09
```

### E4.1a Feature table, 2023

```
         ln_assets  loans_assets  fee_share  household_share  trading_assets  loan_deposit
bank_id                                                                                   
ABN        26.6785        0.7005     0.2165           0.5997          0.0141        1.0246
BAMI       25.9720        0.5617     0.4157           0.3164          0.0234        0.9662
BARC       28.1525        0.3804     0.2905           0.4014          0.1043        1.0472
BBVA       27.2622        0.5068     0.2345           0.4554          0.1817        0.8815
BKT        25.4177        0.6465     0.2723           0.5253          0.0384        0.9330
BMPS       25.5648        0.6122     0.4128           0.4468          0.0557        1.0007
BNP        28.4962        0.3697     0.2685           0.3756          0.2900        0.7411
BPE        25.6892        0.6003     0.4132           0.4473          0.0039        0.8387
CABK       27.0459        0.6252     0.3524           0.5162          0.0271        0.8799
CAG        28.3152        0.5617     0.4440           0.5404          0.1298        0.9496
CBK        26.9353        0.5245     0.3629           0.4899          0.0665        0.8455
DANSKE     26.8224        0.5998     0.2659           0.4424          0.1722        1.5816
DBK        27.9133        0.4603     0.3754           0.3451          0.2932        1.0333
DNB            NaN           NaN        NaN              NaN             NaN           NaN
GLE        27.9273        0.3887     0.2506           0.3991          0.2543        0.8536
HSBA       28.6292        0.3887     0.2217           0.3844          0.0843        0.7118
INGA       27.5952        0.6931     0.1811           0.5319          0.0595        0.9915
ISP        27.4303        0.5426     0.4196           0.3991          0.0520        0.9806
KBC        26.4786        0.5501     0.3161           0.4841          0.0270        0.8042
LLOY       27.6502        0.5596     0.0893           0.7256             NaN        1.0404
NDA        26.9699        0.6350     0.2971           0.5575          0.1321        1.5223
NWG        27.4620        0.5123     0.1781           0.5909          0.0682        0.8252
RABO       27.1645        0.7054     0.1614           0.4598          0.0413        1.1839
SAB        26.2287        0.6347     0.2657           0.5709          0.0118        0.9625
SAN        28.1573        0.5972     0.2173           0.5796          0.0879        1.0276
SANUK      26.5355        0.7854     0.0612           0.8465             NaN        1.1645
SEB        26.3671        0.6215     0.3041           0.3764          0.1391        1.1529
SHB        26.4155        0.7054     0.1915           0.5452          0.0114        1.7322
SWED       26.1661        0.7194     0.2555           0.6441          0.0595        1.4055
UCG        27.4703        0.5192     0.3245           0.2936          0.0785        0.8735
UNI        25.3584        0.5203     0.3173           0.6717          0.0029        0.6942
```

### E4.1a Feature table, 2024

```
         ln_assets  loans_assets  fee_share  household_share  trading_assets  loan_deposit
bank_id                                                                                   
ABN        26.6667        0.7150     0.2158           0.6034          0.0163        1.0275
BAMI       25.9400        0.5671     0.3748           0.3183          0.0268        0.9608
BARC       28.1877        0.3821     0.2641           0.3914          0.1054        1.0654
BBVA       27.3116        0.5261     0.2341           0.4473          0.1663        0.8857
BKT        25.4596        0.6519     0.2481           0.5301          0.0351        0.9198
BMPS       25.5257        0.6298     0.3707           0.4467          0.0500        0.9782
BNP        28.5050        0.3757     0.2576           0.3722          0.3054        0.7462
BPE        25.6994        0.6210     0.3748           0.4632          0.0047        0.8511
CABK       27.0144        0.6481     0.3193           0.5059          0.0248        0.8641
CAG        28.3590        0.5576     0.4429           0.5393          0.1452        0.9373
CBK        26.9986        0.5140     0.3309           0.4743          0.0583        0.7971
DANSKE     26.8026        0.6060     0.2548           0.4087          0.1778        1.6241
DBK        27.9290        0.4677     0.3452           0.3282          0.2949        1.0204
DNB        26.3467        0.6763     0.1456           0.5156          0.0645        1.4236
GLE        27.9538        0.3651     0.2602           0.3820          0.2645        0.7950
HSBA       28.6646        0.3773     0.1958           0.3850          0.0910        0.7040
INGA       27.6187        0.7006     0.1768           0.5308          0.0655        0.9907
ISP        27.3879        0.5483     0.3805           0.4113          0.0520        0.9602
KBC        26.5127        0.5653     0.3109           0.4791          0.0277        0.8170
LLOY       27.6621        0.5562     0.0928           0.7350             NaN        1.0371
NDA        26.9879        0.6244     0.2680           0.5559          0.1450        1.4576
NWG        27.4333        0.5480     0.1667           0.5844          0.0661        0.8840
RABO       27.1591        0.7255     0.1532           0.4494          0.0419        1.1639
SAB        26.2120        0.6475     0.2452           0.5699          0.0139        0.9512
SAN        28.2039        0.5816     0.2126           0.5774          0.1055        0.9955
SANUK      26.5083        0.7932     0.0581           0.8502             NaN        1.1540
SEB        26.3763        0.6182     0.2790           0.3661          0.1658        1.1798
SHB        26.3941        0.7083     0.1711           0.5413          0.0119        1.7497
SWED       26.1513        0.7186     0.2290           0.6395          0.0701        1.4268
UCG        27.4181        0.5381     0.2935           0.3043          0.0727        0.8664
UNI        25.3016        0.5224     0.2993           0.6922          0.0063        0.6834
```

### E4.1a Feature table, 2025

```
         ln_assets  loans_assets  fee_share  household_share  trading_assets  loan_deposit
bank_id                                                                                   
ABN        26.6946        0.7079     0.2214           0.6036          0.0126        1.0270
BAMI       25.9780        0.5339     0.3599           0.3186          0.0378        0.9346
BARC       28.1998        0.3887     0.2617           0.3850          0.1170        1.0783
BBVA       27.3854        0.5321     0.2305           0.4411          0.1601        0.8947
BKT        25.5256           NaN     0.2417              NaN          0.0338           NaN
BMPS       25.7585        0.6150     0.3639           0.4573          0.0653        1.0257
BNP        28.5523        0.3615     0.2454           0.3691             NaN        0.7751
BPE        25.7979        0.6311     0.3557           0.4615          0.0048        0.8520
CABK       27.0876        0.6158     0.2749           0.4996          0.0191        0.8445
CAG        28.4607        0.5178     0.4026           0.5370          0.1531        0.9533
CBK        27.0602           NaN     0.3187              NaN          0.0579           NaN
DANSKE     26.8437        0.5878     0.2515           0.3822          0.1520        1.6516
DBK        27.9520        0.4762     0.3357           0.3108          0.2332        1.0075
DNB        26.3862        0.6689     0.1541           0.4904             NaN        1.4949
GLE        28.0017        0.3342     0.2463           0.3831             NaN        0.7999
HSBA       28.6610        0.3784     0.1872           0.3907          0.1043        0.6960
INGA       27.6472        0.7142     0.1794           0.5314          0.0628        1.0197
ISP        27.4476        0.5093     0.3331           0.4191          0.0504        0.9352
KBC        26.5791        0.5569     0.2860           0.4779          0.0290        0.8460
LLOY       27.6918        0.5526     0.0959           0.7409             NaN        1.0407
NDA        27.0585        0.5943     0.2555           0.5633             NaN        1.4426
NWG        27.4361        0.5733     0.1589           0.5718          0.0667        0.9271
RABO       27.1646        0.7432     0.1439           0.4419          0.0281        1.1517
SAB        26.2040        0.6012     0.2392           0.5213          0.0130        0.9283
SAN        28.2312        0.5619     0.2119           0.5733          0.1203        0.9778
SANUK      26.4921        0.7946     0.0597           0.8364             NaN        1.1408
SEB        26.4372        0.5931     0.2903           0.3664             NaN        1.1932
SHB        26.4185        0.6915     0.1774           0.5427             NaN        1.7420
SWED       26.2197        0.6830     0.2215           0.6428             NaN        1.4420
UCG        27.4229        0.5271     0.2765           0.3153          0.0717        0.8389
UNI        25.3014        0.5025     0.2738           0.7000          0.0092        0.6540
```

### E4.1b k and silhouette for each candidate k, 2023 (28 banks with all 6 features)

```
   k             sizes  silhouette  qualifies
0  2          [16, 12]    0.235157       True
1  3       [12, 11, 5]    0.239339      False
2  4     [11, 8, 5, 4]    0.250090      False
3  5  [11, 5, 4, 4, 4]    0.239842      False
```

```
DNB: ['ln_assets', 'loans_assets', 'fee_share', 'household_share', 'trading_assets', 'loan_deposit']
LLOY: ['trading_assets']
SANUK: ['trading_assets']
```

### E4.1b k and silhouette for each candidate k, 2024 (29 banks with all 6 features)

```
   k            sizes  silhouette  qualifies
0  2          [24, 5]    0.308452      False
1  3       [15, 9, 5]    0.251105      False
2  4     [9, 8, 7, 5]    0.236474      False
3  5  [9, 8, 5, 4, 3]    0.238293      False
```

```
LLOY: ['trading_assets']
SANUK: ['trading_assets']
```

### E4.1b k and silhouette for each candidate k, 2025 (20 banks with all 6 features)

```
   k            sizes  silhouette  qualifies
0  2          [13, 7]    0.194308       True
1  3        [9, 7, 4]    0.223802      False
2  4     [9, 7, 3, 1]    0.211792      False
3  5  [8, 7, 3, 1, 1]    0.215556      False
```

```
BKT: ['loans_assets', 'household_share', 'loan_deposit']
BNP: ['trading_assets']
CBK: ['loans_assets', 'household_share', 'loan_deposit']
DNB: ['trading_assets']
GLE: ['trading_assets']
LLOY: ['trading_assets']
NDA: ['trading_assets']
SANUK: ['trading_assets']
SEB: ['trading_assets']
SHB: ['trading_assets']
SWED: ['trading_assets']
```

### E4.1c 2024 cluster membership at each candidate k (the stop)

```
    k  cut_label  size                                                                                                      banks
0   2          1     5                                                                                      BARC BNP DBK GLE HSBA
1   2          2    24  ABN BAMI BBVA BKT BMPS BPE CABK CAG CBK DANSKE DNB INGA ISP KBC NDA NWG RABO SAB SAN SEB SHB SWED UCG UNI
2   3          1     5                                                                                      BARC BNP DBK GLE HSBA
3   3          2     9                                                                     BAMI BMPS BPE CABK CAG CBK ISP KBC UCG
4   3          3    15                                         ABN BBVA BKT DANSKE DNB INGA NDA NWG RABO SAB SAN SEB SHB SWED UNI
5   4          1     5                                                                                      BARC BNP DBK GLE HSBA
6   4          2     9                                                                     BAMI BMPS BPE CABK CAG CBK ISP KBC UCG
7   4          3     8                                                                          ABN BKT INGA NWG RABO SAB SAN UNI
8   4          4     7                                                                           BBVA DANSKE DNB NDA SEB SHB SWED
9   5          1     5                                                                                      BARC BNP DBK GLE HSBA
10  5          2     9                                                                     BAMI BMPS BPE CABK CAG CBK ISP KBC UCG
11  5          3     8                                                                          ABN BKT INGA NWG RABO SAB SAN UNI
12  5          4     3                                                                                               DNB SHB SWED
13  5          5     4                                                                                        BBVA DANSKE NDA SEB
```

### E4.1d OPEN-37 item 2: candidates on the underlying basis

```
2023
   k             sizes  silhouette  qualifies
0  2          [16, 12]    0.234796       True
1  3       [12, 11, 5]    0.238794      False
2  4     [11, 8, 5, 4]    0.249235      False
3  5  [11, 5, 4, 4, 4]    0.238332      False
```

```
2024
   k            sizes  silhouette  qualifies
0  2          [24, 5]    0.308831      False
1  3       [15, 9, 5]    0.251071      False
2  4    [11, 9, 5, 4]    0.215301      False
3  5  [9, 8, 5, 4, 3]    0.223768      False
```

```
2025
   k            sizes  silhouette  qualifies
0  2          [13, 7]    0.194130       True
1  3        [9, 7, 4]    0.223675      False
2  4     [9, 7, 3, 1]    0.211479      False
3  5  [8, 7, 3, 1, 1]    0.215301      False
```

### E4.1e OPEN-37 item 1: candidates with the mean of the values present

```
2023
   k             sizes  silhouette  qualifies
0  2          [16, 13]    0.246478       True
1  3       [13, 11, 5]    0.246949      False
2  4     [11, 8, 5, 5]    0.239615      False
3  5  [11, 5, 5, 4, 4]    0.233485      False
```

```
2024
   k            sizes  silhouette  qualifies
0  2          [24, 5]    0.308452      False
1  3       [15, 9, 5]    0.251105      False
2  4     [9, 8, 7, 5]    0.236474      False
3  5  [9, 8, 5, 4, 3]    0.238293      False
```

```
2025
   k            sizes  silhouette  qualifies
0  2          [24, 5]    0.293158      False
1  3       [15, 9, 5]    0.220608      False
2  4     [9, 9, 6, 5]    0.222573      False
3  5  [9, 6, 5, 5, 4]    0.225380      False
```

### E4.1f Diagnostic PEERS rows for 2023, k = 2 (not written to peers.csv)

```
    year bank_id cluster  k  silhouette  stability  borderline override_reason            status
0   2023     ABN       2  2    0.235157   0.628074       False                                ok
1   2023    BAMI       1  2    0.235157   0.577939        True                                ok
2   2023    BARC       1  2    0.235157   0.577939        True                                ok
3   2023    BBVA       1  2    0.235157   0.577939        True                                ok
4   2023     BKT       2  2    0.235157   0.628074       False                                ok
5   2023    BMPS       1  2    0.235157   0.577939        True                                ok
6   2023     BNP       1  2    0.235157   0.577939        True                                ok
7   2023     BPE       1  2    0.235157   0.577939        True                                ok
8   2023    CABK       1  2    0.235157   0.577939        True                                ok
9   2023     CAG       1  2    0.235157   0.577939        True                                ok
10  2023     CBK       1  2    0.235157   0.577939        True                                ok
11  2023  DANSKE       2  2    0.235157   0.628074       False                                ok
12  2023     DBK       1  2    0.235157   0.577939        True                                ok
13  2023     DNB    <NA>  2    0.235157        NaN       False                       no_features
14  2023     GLE       1  2    0.235157   0.577939        True                                ok
15  2023    HSBA       1  2    0.235157   0.577939        True                                ok
16  2023    INGA       2  2    0.235157   0.628074       False                                ok
17  2023     ISP       1  2    0.235157   0.577939        True                                ok
18  2023     KBC       1  2    0.235157   0.577939        True                                ok
19  2023    LLOY       2  2    0.235157        NaN       False                  assigned_nearest
20  2023     NDA       2  2    0.235157   0.628074       False                                ok
21  2023     NWG       2  2    0.235157   0.628074       False                                ok
22  2023    RABO       2  2    0.235157   0.628074       False                                ok
23  2023     SAB       2  2    0.235157   0.628074       False                                ok
24  2023     SAN       2  2    0.235157   0.628074       False                                ok
25  2023   SANUK       2  2    0.235157        NaN       False                  assigned_nearest
26  2023     SEB       1  2    0.235157   0.577939        True                                ok
27  2023     SHB       2  2    0.235157   0.628074       False                                ok
28  2023    SWED       2  2    0.235157   0.628074       False                                ok
29  2023     UCG       1  2    0.235157   0.577939        True                                ok
30  2023     UNI       2  2    0.235157   0.628074       False                                ok
```

### E4.1g Cluster means per feature, 2023

```
         ln_assets  loans_assets  fee_share  household_share  trading_assets  loan_deposit
cluster                                                                                   
1          27.2281        0.5134     0.3379           0.4170          0.1132         0.910
2          26.7030        0.6391     0.2350           0.5599          0.0583         1.157
```

### E4.1h assigned_nearest, no_features and borderline banks, 2023

```
   bank_id cluster  stability  borderline            status
1     BAMI       1   0.577939        True                ok
2     BARC       1   0.577939        True                ok
3     BBVA       1   0.577939        True                ok
5     BMPS       1   0.577939        True                ok
6      BNP       1   0.577939        True                ok
7      BPE       1   0.577939        True                ok
8     CABK       1   0.577939        True                ok
9      CAG       1   0.577939        True                ok
10     CBK       1   0.577939        True                ok
12     DBK       1   0.577939        True                ok
13     DNB    <NA>        NaN       False       no_features
14     GLE       1   0.577939        True                ok
15    HSBA       1   0.577939        True                ok
17     ISP       1   0.577939        True                ok
18     KBC       1   0.577939        True                ok
19    LLOY       2        NaN       False  assigned_nearest
25   SANUK       2        NaN       False  assigned_nearest
26     SEB       1   0.577939        True                ok
29     UCG       1   0.577939        True                ok
```

### E4.1f Diagnostic PEERS rows for 2025, k = 2 (not written to peers.csv)

```
    year bank_id  cluster  k  silhouette  stability  borderline override_reason            status
0   2025     ABN        2  2    0.194308   0.745158       False                                ok
1   2025    BAMI        2  2    0.194308   0.745158       False                                ok
2   2025    BARC        1  2    0.194308   0.633754       False                                ok
3   2025    BBVA        1  2    0.194308   0.633754       False                                ok
4   2025     BKT        2  2    0.194308        NaN       False                  assigned_nearest
5   2025    BMPS        2  2    0.194308   0.745158       False                                ok
6   2025     BNP        1  2    0.194308        NaN       False                  assigned_nearest
7   2025     BPE        2  2    0.194308   0.745158       False                                ok
8   2025    CABK        2  2    0.194308   0.745158       False                                ok
9   2025     CAG        1  2    0.194308   0.633754       False                                ok
10  2025     CBK        2  2    0.194308        NaN       False                  assigned_nearest
11  2025  DANSKE        2  2    0.194308   0.745158       False                                ok
12  2025     DBK        1  2    0.194308   0.633754       False                                ok
13  2025     DNB        2  2    0.194308        NaN       False                  assigned_nearest
14  2025     GLE        1  2    0.194308        NaN       False                  assigned_nearest
15  2025    HSBA        1  2    0.194308   0.633754       False                                ok
16  2025    INGA        2  2    0.194308   0.745158       False                                ok
17  2025     ISP        2  2    0.194308   0.745158       False                                ok
18  2025     KBC        2  2    0.194308   0.745158       False                                ok
19  2025    LLOY        1  2    0.194308        NaN       False                  assigned_nearest
20  2025     NDA        2  2    0.194308        NaN       False                  assigned_nearest
21  2025     NWG        1  2    0.194308   0.633754       False                                ok
22  2025    RABO        2  2    0.194308   0.745158       False                                ok
23  2025     SAB        2  2    0.194308   0.745158       False                                ok
24  2025     SAN        1  2    0.194308   0.633754       False                                ok
25  2025   SANUK        2  2    0.194308        NaN       False                  assigned_nearest
26  2025     SEB        2  2    0.194308        NaN       False                  assigned_nearest
27  2025     SHB        2  2    0.194308        NaN       False                  assigned_nearest
28  2025    SWED        2  2    0.194308        NaN       False                  assigned_nearest
29  2025     UCG        2  2    0.194308   0.745158       False                                ok
30  2025     UNI        2  2    0.194308   0.745158       False                                ok
```

### E4.1g Cluster means per feature, 2025

```
         ln_assets  loans_assets  fee_share  household_share  trading_assets  loan_deposit
cluster                                                                                   
1          28.0466        0.4898     0.2555           0.4585          0.1364        0.9335
2          26.6098        0.6035     0.2738           0.4715          0.0428        0.9776
```

### E4.1h assigned_nearest, no_features and borderline banks, 2025

```
   bank_id  cluster  stability  borderline            status
4      BKT        2        NaN       False  assigned_nearest
6      BNP        1        NaN       False  assigned_nearest
10     CBK        2        NaN       False  assigned_nearest
13     DNB        2        NaN       False  assigned_nearest
14     GLE        1        NaN       False  assigned_nearest
19    LLOY        1        NaN       False  assigned_nearest
20     NDA        2        NaN       False  assigned_nearest
25   SANUK        2        NaN       False  assigned_nearest
26     SEB        2        NaN       False  assigned_nearest
27     SHB        2        NaN       False  assigned_nearest
28    SWED        2        NaN       False  assigned_nearest
```

### E4.1i OPEN-36 option (a) measured: min_cluster_size 5 (a measurement only; config.toml is unchanged)

```
      k  silhouette  borderline  min_stability
year                                          
2023  3    0.239339           0       0.694706
2024  2    0.308452           0       0.603891
2025  2    0.194308           0       0.633754
```

```
year     2023 2024 2025
bank_id                
ABN         3    2    2
BAMI        2    2    2
BARC        1    1    1
BBVA        2    2    1
BKT         3    2    2
BMPS        2    2    2
BNP         1    1    1
BPE         2    2    2
CABK        2    2    2
CAG         2    2    1
CBK         2    2    2
DANSKE      3    2    2
DBK         1    1    1
DNB      <NA>    2    2
GLE         1    1    1
HSBA        1    1    1
INGA        3    2    2
ISP         2    2    2
KBC         2    2    2
LLOY        3    2    1
NDA         3    2    2
NWG         3    2    1
RABO        3    2    2
SAB         3    2    2
SAN         3    2    1
SANUK       3    2    2
SEB         2    2    2
SHB         3    2    2
SWED        3    2    2
UCG         2    2    2
UNI         3    2    2
```

```
   from    to   n       ari
0  2023  2024  30  0.367959
1  2024  2025  31  0.415942
```


## Tests run

```
$ pytest -p socket --disable-socket -q
.............................                                            [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\_pytest\config\__init__.py:894
  C:\Utkarsh\10. Quant Projects\15) Bank Benchmarking Project\Bank-Performance-Benchmarking\.venv\Lib\site-packages\_pytest\config\__init__.py:894: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; socket
    self.import_plugin(arg, consider_entry_points=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
29 passed, 1 warning in 109.47s (0:01:49)
```

`ruff check .`: All checks passed!

## Fresh-clone check

Clone path `C:/bpbs4`, at ab3f25f.

```
$ git clone https://github.com/uty101/Bank-Performance-Benchmarking.git C:/bpbs4
$ uv venv --python 3.12
$ uv pip install -r requirements-lock.txt
$ uv pip install -e . --no-deps
$ pytest -p socket --disable-socket -q
.............................                                            [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\_pytest\config\__init__.py:894
  C:\bpbs4\.venv\Lib\site-packages\_pytest\config\__init__.py:894: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; socket
    self.import_plugin(arg, consider_entry_points=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
29 passed, 1 warning in 158.92s (0:02:38)
```

## Runtime per step

Not timed per step. The full suite took 109.47 s locally and 158.92 s in the fresh clone.

## Deviations from PLAN.md

1. **Rule 4 stop.** Step 4.1 stopped at the 2024 cut (E4.1b, E4.1c). `outputs/tables/peers.csv` does not exist, `scripts/run_all.py` is unchanged, and `pycel` is not added. `peer_groups` raises `StopSection` on the real data. The 2023 and 2025 rows in E4.1f to E4.1h are diagnostics.
2. **Comparative rule applied to more dates than OPEN-35 listed.** A.1 names banks, not dates, so its rule was applied wherever a later document prints the date: SANUK 2022-06-30 and 2022-12-31, DANSKE 2022-06-30, 2022-12-31 and 2023-12-31. All are 0. Without the SANUK and DANSKE 2022 and 2023 rows, their rote stays blank across 2023 and 2024.
3. **Comparative blocks with no NCI column.** SANUK 2023-06-30 and 2024-12-31, and DANSKE 2023-06-30 and 2023-12-31, cite a later comparative block that has no NCI column at all. ABN 2020-12-31 cites a blank cell. All are entered as `blank`, value 0, status `from_comparative`. These 5 rows have no printed amount in the strict sense; please confirm this is what A.1 intends.
4. **BKT 2025-06-30.** No H1 2025 report was obtained. The row cites the H1 2026 comparative block under amendment 24, status `from_comparative`, not `no_nci_line`. BKT 2021-06-30 to 2024-06-30 have no document and stay missing.
5. **`from_comparative` is now also an entered status.** The automatic rule in `entries_facts` does not mark the FY2025 column for 2024-12-31, so SANUK 2024-12-31 needed it stated.
6. **BMPS at1_coupons at half year dates** cite the annual report page of the at1_in_equity entry for that date, as those rows do. CC1 row 30 is shown in E3.8b.
7. **`PEERS` in code has a trailing `status` column,** which the fixed schema lacks (OPEN-37 item 3).
8. **Clone folders.** The safety check blocked removing `C:\bpbs3`, `C:\bpbs3b` and `C:\bpbs3c`, so they were left, as Section A allows. Each was checked first: a clean clone of a pushed commit. `C:\bpbs4` from this session is also left.

## Not verified

- Pages were read from the extracted text, not by eye on the PDF. For the blank cells this relies on the text keeping the column order; ABN 2020-12-31 was cross checked against the equal Total and Total equity figures (20,989).
- The stop was tested against the readings in OPEN-37 items 1 and 2. Items 3 and 4 cannot change which k qualifies.
- Steps 4.2 to 4.4 and every test in `tests/test_benchmark.py` and `tests/test_gaps.py` do not exist yet.

## Open questions

1. **OPEN-36 (blocking):** no k qualifies for 2024. Set `min_cluster_size` to 5, or keep 6 and carry the previous year's clusters?
2. **OPEN-37:** 4 unstated readings in the peer features. Item 1 matters most: under the mean of values present, 2025 also has no qualifying k.
3. **OPEN-38:** O in the joint gap counts dividends twice as written, and is blank for 16 banks including LLOY and SWED. Found by reading ahead; decide it before step 4.3.
4. **Deviation 3:** do the 5 rows with no printed NCI amount fit A.1?

## Files changed

```
CLAUDE.md                      |  12 +++
 bpb/ingest.py                  |   7 +-
 bpb/kpi.py                     |   5 +-
 bpb/peers.py                   | 199 +++++++++++++++++++++++++++++++++++++++++
 config/fields.yaml             |   2 +-
 data/manual/report_entries.csv |  31 +++++++
 decisions/OPEN.md              |  25 ++++++
 decisions/section_3_review.md  |  28 ++++++
 outputs/tables/checks.csv      |  44 +++++++++
 outputs/tables/kpi.csv         | 116 ++++++++++++------------
 tests/test_peers.py            |  46 ++++++++++
 11 files changed, 452 insertions(+), 63 deletions(-)
```

Also 8 page cache files in `data/raw/report_text/`.

Latest commits:

```
ab3f25f section 4: open questions OPEN-36 to OPEN-38
606dcb0 step 4.1: peer features, clusters and stability (stopped: no k qualifies for 2024, OPEN-36)
da5d6e6 step 3.8: section 3 review decisions
e0a557d Add instructions for section 4
```

## Reviewer reads

1. E4.1b and E4.1c: the stop.
2. `decisions/OPEN.md`: OPEN-36, OPEN-37, OPEN-38.
3. E4.1i: option (a) measured.
4. E3.8a and E3.8c: step 3.8 entries and rote.
5. Deviations 2 and 3.
