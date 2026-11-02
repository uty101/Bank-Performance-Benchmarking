# Section 1

Session 1 **stopped at step 1.3** under rules 4 and 5. Steps 1.0, 1.1 and 1.2 are complete and committed. The unit test fixed for step 1.3 (`test_load_eba_synthetic`, "read the unit from `SDD.xlsx`") cannot be written, because no release's `SDD.xlsx` states a unit (OPEN-25). The same finding shows that EBA amounts are in EUR millions for every bank, including the SEK, NOK and DKK reporters, which conflicts with Convention 4.1. Steps 1.3 to 1.7 were not started, and nothing of them is committed.

## Steps completed

- 1.0 apply section 0 review decisions (117db5a)
- 1.1 EBA download, country filter and manifest (5eeb4e2)
- 1.2 EU LEIs from the 2025 release and EBA field maps (e028dab)
- 1.3 not completed: stopped, OPEN-25
- 1.4 to 1.7 not started (rule 4)

## Evidence

### 1.0: decisions applied

`decisions/section_0_review.md` holds instruction 01 Sections B and B.1 verbatim (sliced from the instruction file by heading, not retyped). OPEN-01 to OPEN-16 each carry a `DECIDED (see decisions/section_0_review.md)` line. `CLAUDE.md` has the 6 amendments under `## Amendments`. `PLAN.md` steps touched by the decisions were edited by exact string replacement, and no `**OPEN-NN**` marker remains in it. `config/source_map.yaml` encodes OPEN-03 (role `bridge_input`), OPEN-04 (b) and OPEN-05 (a). `config/fields.yaml` has `cet1_ratio_reported` and `income_components_other`. `universe.csv` after step 1.2:

```
bank_id                  lei                            name country  market listed    ticker price_ccy report_ccy
   LLOY                                 Lloyds Banking Group      GB      UK      1    LLOY.L       GBP        GBP
    NWG                                        NatWest Group      GB      UK      1     NWG.L       GBP        GBP
   BARC                                             Barclays      GB      UK      1    BARC.L       GBP        GBP
   HSBA                                        HSBC Holdings      GB      UK      1    HSBA.L       GBP        USD
  SANUK                          Santander UK Group Holdings      GB      UK      0                            GBP
    NDA 529900ODI3047E2LIV03                     Nordea Bank      FI Nordics      1 NDA-FI.HE       EUR        EUR
    DNB 549300GKFG0RYRRQ1414                        DNB Bank      NO Nordics      1    DNB.OL       NOK        NOK
 DANSKE MAES062Z21O4RZ2U7M96                     Danske Bank      DK Nordics      1 DANSKE.CO       DKK        DKK
    SEB F3JS33DEI6XQ4ZBPTN86   Skandinaviska Enskilda Banken      SE Nordics      1  SEB-A.ST       SEK        SEK
    SHB NHBDILHZTYCNBV5UYZ31           Svenska Handelsbanken      SE Nordics      1  SHB-A.ST       SEK        SEK
   SWED M312WZV08Y7LYUC71685                        Swedbank      SE Nordics      1 SWED-A.ST       SEK        SEK
   INGA 549300NYKK9MWM7GGW15                       ING Groep      NL Benelux      1   INGA.AS       EUR        EUR
    ABN BFXS5XCH7N0Y05NIXW11                   ABN AMRO Bank      NL Benelux      1    ABN.AS       EUR        EUR
    KBC 213800X3Q9LSAKRUWY91                       KBC Group      BE Benelux      1    KBC.BR       EUR        EUR
   RABO DG3RU1DBUFHT4ZF9WN62                        Rabobank      NL Benelux      0                            EUR
    BNP R0MUWSFPU8MPRO8K5P83                     BNP Paribas      FR  France      1    BNP.PA       EUR        EUR
    GLE O2RNE8IBXP4R0TD8PU41                Société Générale      FR  France      1    GLE.PA       EUR        EUR
    CAG FR969500TJ5KRTCJQWXH           Crédit Agricole Group      FR  France      0                            EUR
    DBK                                        Deutsche Bank      DE Germany      1    DBK.DE       EUR        EUR
    CBK 851WYGNLUQLFZBSYGB56                     Commerzbank      DE Germany      1    CBK.DE       EUR        EUR
    SAN 5493006QMFDDMYWIAM13                 Banco Santander      ES   Spain      1    SAN.MC       EUR        EUR
   BBVA K8MS7FD7N5Z2WQ51AZ71                            BBVA      ES   Spain      1   BBVA.MC       EUR        EUR
   CABK 7CUNS533WID6K7DGFI87                       CaixaBank      ES   Spain      1   CABK.MC       EUR        EUR
    SAB SI5RG2M0WQQLZCXKRM20                  Banco Sabadell      ES   Spain      1    SAB.MC       EUR        EUR
    BKT VWMYAEQSTOPNV0SUGU82                       Bankinter      ES   Spain      1    BKT.MC       EUR        EUR
    UNI 5493007SJLLCTM6J6M37                   Unicaja Banco      ES   Spain      1    UNI.MC       EUR        EUR
    UCG 549300TRUWO2CD2G5692                       UniCredit      IT   Italy      1    UCG.MI       EUR        EUR
    ISP 2W8N8UU78PMDQKZENC08                 Intesa Sanpaolo      IT   Italy      1    ISP.MI       EUR        EUR
   BAMI 815600E4E6DCD2D25E30                       Banco BPM      IT   Italy      1   BAMI.MI       EUR        EUR
    BPE N747OI7JINV7RUUH6190                      BPER Banca      IT   Italy      1    BPE.MI       EUR        EUR
   BMPS J4CP7MHCXR8DAQMKIL78 Banca Monte dei Paschi di Siena      IT   Italy      1   BMPS.MI       EUR        EUR
```

### 1.1: URLs, manifest and reference dates

The release pages, as fetched on 2026-11-02:

- **2022 and 2023.** The pages sit under `.../risk-analysis/eu-wide-transparency-exercise/`, which is the `...` of instruction 01 B item 1.
- **2021.** The literal path `.../eu-wide-transparency-exercise/2021-eu-wide-transparency-exercise` returns 404. The EBA hub page links the 2021 release as `.../eu-wide-transparency-exercise/2021-eu-wide-transparency`, and that page was used.
- **2025.** `.../2025-eu-wide-transparency-exercise` returns 404. The 2025 `Full_database` links sit on the hub page `.../eu-wide-transparency-exercise` itself, so the hub is recorded as the 2025 release page. Every 2024 and 2025 URL read from the pages equals the URL fixed in kickoff Section 3.2.

Every release publishes `tr_oth.csv` and `tr_cre.csv` under those names, so no split was recorded. Each also publishes `tr_mrk.csv` and `tr_sov.csv`, which are outside `[eba] files` and were not pulled.

The country filter keeps rows whose `NSA` is one of FI, NO, DK, SE, NL, BE, FR, DE, ES and IT. `NSA` is the bank's home supervisor country. In `tr_cre.csv`, the `Country` column is the exposure's country, so it is not used. The 2021 CSVs are cp1252, not UTF-8. The filter copies rows byte for byte, and the manifest records each file's encoding.

### data/manual/eba_urls.csv

```
 release             file                                                                           url                                                                                                                release_page_url
    2021       tr_oth.csv              https://www.eba.europa.eu/assets/TE2021/Full_database/tr_oth.csv          https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise/2021-eu-wide-transparency
    2021       tr_cre.csv              https://www.eba.europa.eu/assets/TE2021/Full_database/tr_cre.csv          https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise/2021-eu-wide-transparency
    2021 TR_Metadata.xlsx        https://www.eba.europa.eu/assets/TE2021/Full_database/TR_Metadata.xlsx          https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise/2021-eu-wide-transparency
    2021         SDD.xlsx                https://www.eba.europa.eu/assets/TE2021/Full_database/SDD.xlsx          https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise/2021-eu-wide-transparency
    2022       tr_oth.csv              https://www.eba.europa.eu/assets/TE2022/Full_database/tr_oth.csv https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise/2022-eu-wide-transparency-exercise
    2022       tr_cre.csv              https://www.eba.europa.eu/assets/TE2022/Full_database/tr_cre.csv https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise/2022-eu-wide-transparency-exercise
    2022 TR_Metadata.xlsx        https://www.eba.europa.eu/assets/TE2022/Full_database/TR_Metadata.xlsx https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise/2022-eu-wide-transparency-exercise
    2022         SDD.xlsx                https://www.eba.europa.eu/assets/TE2022/Full_database/SDD.xlsx https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise/2022-eu-wide-transparency-exercise
    2023       tr_oth.csv       https://www.eba.europa.eu/assets/TE2023/Full_database/837203/tr_oth.csv https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise/2023-eu-wide-transparency-exercise
    2023       tr_cre.csv       https://www.eba.europa.eu/assets/TE2023/Full_database/837203/tr_cre.csv https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise/2023-eu-wide-transparency-exercise
    2023 TR_Metadata.xlsx https://www.eba.europa.eu/assets/TE2023/Full_database/837203/TR_Metadata.xlsx https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise/2023-eu-wide-transparency-exercise
    2023         SDD.xlsx         https://www.eba.europa.eu/assets/TE2023/Full_database/837203/SDD.xlsx https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise/2023-eu-wide-transparency-exercise
    2024       tr_oth.csv       https://www.eba.europa.eu/assets/TE2024/Full_database/256109/tr_oth.csv https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise/2024-eu-wide-transparency-exercise
    2024       tr_cre.csv       https://www.eba.europa.eu/assets/TE2024/Full_database/256109/tr_cre.csv https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise/2024-eu-wide-transparency-exercise
    2024 TR_Metadata.xlsx https://www.eba.europa.eu/assets/TE2024/Full_database/256109/TR_Metadata.xlsx https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise/2024-eu-wide-transparency-exercise
    2024         SDD.xlsx         https://www.eba.europa.eu/assets/TE2024/Full_database/256109/SDD.xlsx https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise/2024-eu-wide-transparency-exercise
    2025       tr_oth.csv       https://www.eba.europa.eu/assets/TE2025/Full_database/883401/tr_oth.csv                                    https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise
    2025       tr_cre.csv       https://www.eba.europa.eu/assets/TE2025/Full_database/883401/tr_cre.csv                                    https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise
    2025 TR_Metadata.xlsx https://www.eba.europa.eu/assets/TE2025/Full_database/883401/TR_Metadata.xlsx                                    https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise
    2025         SDD.xlsx         https://www.eba.europa.eu/assets/TE2025/Full_database/883401/SDD.xlsx                                    https://www.eba.europa.eu/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise
```

### data/raw/MANIFEST.json entries

```
                              path  committed     bytes     rows first_date  last_date encoding           pulled_utc
 data/eba_download/2021/tr_cre.csv      False 139781047 802844.0 2020-09-30 2021-06-30   cp1252 2026-11-02T13:49:29Z
 data/eba_download/2021/tr_oth.csv      False  14756442  95307.0 2020-09-30 2021-06-30   cp1252 2026-11-02T13:49:17Z
 data/eba_download/2022/tr_cre.csv      False 118289012 683340.0 2021-09-30 2022-06-30    utf-8 2026-11-02T13:50:31Z
 data/eba_download/2022/tr_oth.csv      False  16141420  95914.0 2021-09-30 2022-06-30    utf-8 2026-11-02T13:50:24Z
 data/eba_download/2023/tr_cre.csv      False 122882620 610325.0 2022-09-30 2023-06-30    utf-8 2026-11-02T13:51:52Z
 data/eba_download/2023/tr_oth.csv      False  17950303 100223.0 2022-09-30 2023-06-30    utf-8 2026-11-02T13:51:43Z
 data/eba_download/2024/tr_cre.csv      False 119032803 606922.0 2023-09-30 2024-06-30    utf-8 2026-11-02T13:52:59Z
 data/eba_download/2024/tr_oth.csv      False  17977156  99324.0 2023-09-30 2024-06-30    utf-8 2026-11-02T13:52:48Z
 data/eba_download/2025/tr_cre.csv      False 123180326 648951.0 2024-09-30 2025-06-30    utf-8 2026-11-02T13:53:55Z
 data/eba_download/2025/tr_oth.csv      False  15110064  91277.0 2024-09-30 2025-06-30    utf-8 2026-11-02T13:53:48Z
        data/raw/eba/2021/SDD.xlsx       True     36034      NaN        NaN        NaN      NaN 2026-11-02T13:50:24Z
data/raw/eba/2021/TR_Metadata.xlsx       True    139809      NaN        NaN        NaN      NaN 2026-11-02T13:50:24Z
   data/raw/eba/2021/tr_cre.csv.gz       True   3821270 523838.0 2020-09-30 2021-06-30   cp1252 2026-11-02T13:49:29Z
   data/raw/eba/2021/tr_oth.csv.gz       True    725631  60056.0 2020-09-30 2021-06-30   cp1252 2026-11-02T13:49:17Z
        data/raw/eba/2022/SDD.xlsx       True     40502      NaN        NaN        NaN      NaN 2026-11-02T13:51:43Z
data/raw/eba/2022/TR_Metadata.xlsx       True    146409      NaN        NaN        NaN      NaN 2026-11-02T13:51:43Z
   data/raw/eba/2022/tr_cre.csv.gz       True   3418703 472122.0 2021-09-30 2022-06-30    utf-8 2026-11-02T13:50:31Z
   data/raw/eba/2022/tr_oth.csv.gz       True    757545  62248.0 2021-09-30 2022-06-30    utf-8 2026-11-02T13:50:24Z
        data/raw/eba/2023/SDD.xlsx       True     39045      NaN        NaN        NaN      NaN 2026-11-02T13:52:48Z
data/raw/eba/2023/TR_Metadata.xlsx       True    143450      NaN        NaN        NaN      NaN 2026-11-02T13:52:48Z
   data/raw/eba/2023/tr_cre.csv.gz       True   4349674 418373.0 2022-09-30 2023-06-30    utf-8 2026-11-02T13:51:52Z
   data/raw/eba/2023/tr_oth.csv.gz       True   1004963  65255.0 2022-09-30 2023-06-30    utf-8 2026-11-02T13:51:43Z
        data/raw/eba/2024/SDD.xlsx       True     56448      NaN        NaN        NaN      NaN 2026-11-02T13:53:48Z
data/raw/eba/2024/TR_Metadata.xlsx       True   2790861      NaN        NaN        NaN      NaN 2026-11-02T13:53:47Z
   data/raw/eba/2024/tr_cre.csv.gz       True   4412159 424062.0 2023-09-30 2024-06-30    utf-8 2026-11-02T13:52:59Z
   data/raw/eba/2024/tr_oth.csv.gz       True   1012171  65224.0 2023-09-30 2024-06-30    utf-8 2026-11-02T13:52:48Z
        data/raw/eba/2025/SDD.xlsx       True     58751      NaN        NaN        NaN      NaN 2026-11-02T13:54:54Z
data/raw/eba/2025/TR_Metadata.xlsx       True   2782361      NaN        NaN        NaN      NaN 2026-11-02T13:54:52Z
   data/raw/eba/2025/tr_cre.csv.gz       True   5056084 466055.0 2024-09-30 2025-06-30    utf-8 2026-11-02T13:53:55Z
   data/raw/eba/2025/tr_oth.csv.gz       True   1299425  62443.0 2024-09-30 2025-06-30    utf-8 2026-11-02T13:53:48Z
```

```
                              path                                                           sha256
 data/eba_download/2021/tr_cre.csv 4d560b4ee59795cc438e0d1d236b799c9d76c3d35f10fc3fc8f2bfd632a75742
 data/eba_download/2021/tr_oth.csv 610daa2c0bfe58d0aa12f834f800370b6bad749a07f6fab59a22d1048fb19f8e
 data/eba_download/2022/tr_cre.csv 9136ac100df67e1b93d7c5c79e3baa6af9c247e98a108a13396150c25226689b
 data/eba_download/2022/tr_oth.csv e198483336ea41bd2a764d4692cbb1b11303acf4395e5d4bb47c06efbe4e9caf
 data/eba_download/2023/tr_cre.csv 191214efada8c065ea2dfe3477d1231b69b785ac7a97304a77bc6dfef8243249
 data/eba_download/2023/tr_oth.csv 841b5a6ee3823194118eaebde77447e2afc8158e8db4616b615a07e7f99f9e73
 data/eba_download/2024/tr_cre.csv 4175521fbbe352e7e8973c37f419f16a8fe3b6fc5974ea7955baf67aadf2060e
 data/eba_download/2024/tr_oth.csv e2c6d0b9ddb887f96ff0af7a51bbbd7d8e7b467a9e9e1110514660aecbcaa584
 data/eba_download/2025/tr_cre.csv a29ca3b808d4f51b6aa2d74ccb3cd39d05f416e10d26e16340cce45842637c99
 data/eba_download/2025/tr_oth.csv 1785417e172907b3a49623eb13e2cc6c7af26a02ae982bfe2ba3a70f782e4104
        data/raw/eba/2021/SDD.xlsx 7341155629b9d269e35422c07a13524a6c941c6b189ca952db52c92ea51b1753
data/raw/eba/2021/TR_Metadata.xlsx 8821d2f9c9cf318bc44156012ad7f844ffd5a78f259b97066347c4b8e40df88d
   data/raw/eba/2021/tr_cre.csv.gz 2487575c8de35a1f671b693c96c369bcd4e8b853e387083a764be663b1c549a3
   data/raw/eba/2021/tr_oth.csv.gz cc3fdb90908f8b6a62d1d760f3efddd5ac3bd4f7b8cf44e90550a3d838e4f01c
        data/raw/eba/2022/SDD.xlsx fc3ecd20f069ad30d3bf5b64fee7c4f72f4294ad622ca12cbe8dc13f11933737
data/raw/eba/2022/TR_Metadata.xlsx 8b16b61160d22d8a4b5345b6e1e3334bdfa5285187b586c0b1680089f01243f4
   data/raw/eba/2022/tr_cre.csv.gz 64a0c1add7ac69cfb6e4257a9e8895cdd58e69d8321d8025442d71fdfe95b08c
   data/raw/eba/2022/tr_oth.csv.gz e6307997e2135e4fd663a22c541a4b2cc439123c03c78d5b0561db43835be384
        data/raw/eba/2023/SDD.xlsx 9225586072e3e206f268a508280c706ce7953243e0d914c8d1de9658148c10ae
data/raw/eba/2023/TR_Metadata.xlsx ae3ca2c744dd403de6743242801906e251d2e1ab12ac5251adddc51e6f1bde92
   data/raw/eba/2023/tr_cre.csv.gz b4c020a242375a59b053f88fc21d1653a580a3d6fde3e7ae71f387bd2f7ec8ee
   data/raw/eba/2023/tr_oth.csv.gz c72c8819ec1e550babfbd0191f65671b00662b0a6b228d896fc87b196de47b19
        data/raw/eba/2024/SDD.xlsx 9f350211b2d54ae7a273526a0402ab43965822ff527dc2e587149c98bd13d6a9
data/raw/eba/2024/TR_Metadata.xlsx ecd488dffa578dabb89594ccc00409303b14446e7b0eaebab2bdaa7a65e7bc21
   data/raw/eba/2024/tr_cre.csv.gz 60c46cd02b8a3bb513a30053f826b4a34cd9c2d613ad4757bcc4278f8ea82150
   data/raw/eba/2024/tr_oth.csv.gz 14d82a853c30deb62d8358d49a6d58b112f7976d8ad594c2e37581b9ac6a643a
        data/raw/eba/2025/SDD.xlsx 8b7fdf40bacb79d0bd51564c4cc157f68261a2290a209db18df9fa8eb6ee66cb
data/raw/eba/2025/TR_Metadata.xlsx 8110aea2ed614bc86cb5e00058787e8fe2b5e1ce816a5ec1f9346647668eb5df
   data/raw/eba/2025/tr_cre.csv.gz 212ab51d0535162db9b94e5616ce55a04ea781d6803c325ba5c3ebcdd90329e2
   data/raw/eba/2025/tr_oth.csv.gz 20ff5b533a852c3c9c28ff70f8e90164d7aab8fe0ae66a5384c1568d384c90ff
```

```
                           path                     filtered_from                               filter
data/raw/eba/2021/tr_cre.csv.gz data/eba_download/2021/tr_cre.csv NSA in BE,DE,DK,ES,FI,FR,IT,NL,NO,SE
data/raw/eba/2021/tr_oth.csv.gz data/eba_download/2021/tr_oth.csv NSA in BE,DE,DK,ES,FI,FR,IT,NL,NO,SE
data/raw/eba/2022/tr_cre.csv.gz data/eba_download/2022/tr_cre.csv NSA in BE,DE,DK,ES,FI,FR,IT,NL,NO,SE
data/raw/eba/2022/tr_oth.csv.gz data/eba_download/2022/tr_oth.csv NSA in BE,DE,DK,ES,FI,FR,IT,NL,NO,SE
data/raw/eba/2023/tr_cre.csv.gz data/eba_download/2023/tr_cre.csv NSA in BE,DE,DK,ES,FI,FR,IT,NL,NO,SE
data/raw/eba/2023/tr_oth.csv.gz data/eba_download/2023/tr_oth.csv NSA in BE,DE,DK,ES,FI,FR,IT,NL,NO,SE
data/raw/eba/2024/tr_cre.csv.gz data/eba_download/2024/tr_cre.csv NSA in BE,DE,DK,ES,FI,FR,IT,NL,NO,SE
data/raw/eba/2024/tr_oth.csv.gz data/eba_download/2024/tr_oth.csv NSA in BE,DE,DK,ES,FI,FR,IT,NL,NO,SE
data/raw/eba/2025/tr_cre.csv.gz data/eba_download/2025/tr_cre.csv NSA in BE,DE,DK,ES,FI,FR,IT,NL,NO,SE
data/raw/eba/2025/tr_oth.csv.gz data/eba_download/2025/tr_oth.csv NSA in BE,DE,DK,ES,FI,FR,IT,NL,NO,SE
```

### Reference dates per release and file (rows per date)

```
 release          file period   rows
    2021 tr_cre.csv.gz 202009 126481
    2021 tr_cre.csv.gz 202012 133053
    2021 tr_cre.csv.gz 202103 128866
    2021 tr_cre.csv.gz 202106 135438
    2021 tr_oth.csv.gz 202009  14270
    2021 tr_oth.csv.gz 202012  15002
    2021 tr_oth.csv.gz 202103  14912
    2021 tr_oth.csv.gz 202106  15872
    2022 tr_cre.csv.gz 202109 112619
    2022 tr_cre.csv.gz 202112 120408
    2022 tr_cre.csv.gz 202203 115825
    2022 tr_cre.csv.gz 202206 123270
    2022 tr_oth.csv.gz 202109  14601
    2022 tr_oth.csv.gz 202112  15562
    2022 tr_oth.csv.gz 202203  15345
    2022 tr_oth.csv.gz 202206  16740
    2023 tr_cre.csv.gz 202209 101846
    2023 tr_cre.csv.gz 202212 106740
    2023 tr_cre.csv.gz 202303 102815
    2023 tr_cre.csv.gz 202306 106972
    2023 tr_oth.csv.gz 202209  15779
    2023 tr_oth.csv.gz 202212  16616
    2023 tr_oth.csv.gz 202303  16058
    2023 tr_oth.csv.gz 202306  16802
    2024 tr_cre.csv.gz 202309 103792
    2024 tr_cre.csv.gz 202312 108092
    2024 tr_cre.csv.gz 202403 103939
    2024 tr_cre.csv.gz 202406 108239
    2024 tr_oth.csv.gz 202309  15934
    2024 tr_oth.csv.gz 202312  16585
    2024 tr_oth.csv.gz 202403  16027
    2024 tr_oth.csv.gz 202406  16678
    2025 tr_cre.csv.gz 202409 113423
    2025 tr_cre.csv.gz 202412 118026
    2025 tr_cre.csv.gz 202503 113520
    2025 tr_cre.csv.gz 202506 121086
    2025 tr_oth.csv.gz 202409  15284
    2025 tr_oth.csv.gz 202412  15899
    2025 tr_oth.csv.gz 202503  15195
    2025 tr_oth.csv.gz 202506  16065
```

### tr_oth reference dates held per universe bank and release (banks with a 2025 LEI)

```
release  2021  2022  2023  2024  2025
bank_id                              
ABN         4     4     4     4     4
BAMI        4     4     4     4     4
BBVA        4     4     4     4     4
BKT         4     4     4     4     4
BMPS        4     4     4     4     4
BNP         4     4     4     4     4
BPE         0     4     4     4     4
CABK        4     4     4     4     4
CAG         4     4     4     4     4
CBK         4     4     4     4     4
DANSKE      4     4     4     4     4
DNB         0     1     4     4     4
GLE         4     4     4     4     4
INGA        4     4     4     4     4
ISP         4     4     4     4     4
KBC         4     4     4     4     4
NDA         4     4     4     4     4
RABO        2     2     2     4     4
SAB         4     4     4     4     4
SAN         4     4     4     4     4
SEB         4     4     4     4     4
SHB         4     4     4     4     4
SWED        4     4     4     4     4
UCG         4     4     4     4     4
UNI         4     4     4     4     4
```

```
bank_id  release  periods          list
    DNB     2021        0              
   RABO     2021        2 202012,202106
    BPE     2021        0              
    DNB     2022        1        202206
   RABO     2022        2 202112,202206
   RABO     2023        2 202212,202306
```

### 1.2: universe, maps and OPEN fields

Matching follows instruction 01 step 1.2. Punctuation becomes a space, so `A/S` reads `a s` and `S.p.A.` reads `s p a`. "Contained" means the normalised universe name appears as a run of whole words in exactly 1 normalised 2025 name. With plain substring matching, `ing` would hit names such as "Holding". 25 of the 26 EU banks matched, and DBK did not (OPEN-17). Every matched 2025 name is at the same level of consolidation as its universe row. CAG matches `Groupe Crédit Agricole`, the group level, as B.1 requires. No other bank differs in level.

Each field names its template and its label as printed in the 2025 `SDD.xlsx`. It is matched exactly, after casefolding and collapsing whitespace, within that template in each release. Dimension values are matched on the labels in that release's `TR_Metadata.xlsx`, and `dim_filter` stores the matched codes. Every dimension column not named in `dim_filter` is 0, "Total / No breakdown". All 33 fields matched the same label in all 5 releases. The 2025 SDD crosswalk (`Item_TR_{year}`) was never needed, and no label differs between releases.

The kickoff writes `TOTAL OPERATING INCOME, NET`, and every SDD prints `TOTAL OPERATING INCOME_ NET`. Every SDD prints commas as `_` ("held for trading_ net", "subsidaries_ joint ventures"), so this is the same line.

### LEI matches against the 2025 release

```
bank_id                            name                    normalised                  lei                                eba_name     match                                                                                                                                                                                                                                                                                                                candidates
    NDA                     Nordea Bank                        nordea 529900ODI3047E2LIV03                         Nordea Bank Abp contained                                                                                                                                                                                                                                                                                                                          
    DNB                        DNB Bank                           dnb 549300GKFG0RYRRQ1414                            DNB BANK ASA     exact                                                                                                                                                                                                                                                                                                                          
 DANSKE                     Danske Bank                        danske MAES062Z21O4RZ2U7M96                         Danske Bank A/S     exact                                                                                                                                                                                                                                                                                                                          
    SEB   Skandinaviska Enskilda Banken skandinaviska enskilda banken F3JS33DEI6XQ4ZBPTN86 Skandinaviska Enskilda Banken - gruppen contained                                                                                                                                                                                                                                                                                                                          
    SHB           Svenska Handelsbanken         svenska handelsbanken NHBDILHZTYCNBV5UYZ31         Svenska Handelsbanken - gruppen contained                                                                                                                                                                                                                                                                                                                          
   SWED                        Swedbank                      swedbank M312WZV08Y7LYUC71685                        Swedbank - Grupp contained                                                                                                                                                                                                                                                                                                                          
   INGA                       ING Groep                           ing 549300NYKK9MWM7GGW15                          ING Groep N.V.     exact                                                                                                                                                                                                                                                                                                                          
    ABN                   ABN AMRO Bank                      abn amro BFXS5XCH7N0Y05NIXW11                      ABN AMRO Bank N.V.     exact                                                                                                                                                                                                                                                                                                                          
    KBC                       KBC Group                           kbc 213800X3Q9LSAKRUWY91                              KBC Groupe contained                                                                                                                                                                                                                                                                                                                          
   RABO                        Rabobank                      rabobank DG3RU1DBUFHT4ZF9WN62             Coöperatieve Rabobank U.A.2 contained                                                                                                                                                                                                                                                                                                                          
    BNP                     BNP Paribas                   bnp paribas R0MUWSFPU8MPRO8K5P83                             BNP Paribas     exact                                                                                                                                                                                                                                                                                                                          
    GLE                Société Générale              societe generale O2RNE8IBXP4R0TD8PU41                   Société générale S.A.     exact                                                                                                                                                                                                                                                                                                                          
    CAG           Crédit Agricole Group               credit agricole FR969500TJ5KRTCJQWXH                  Groupe Crédit Agricole contained                                                                                                                                                                                                                                                                                                                          
    DBK                   Deutsche Bank                      deutsche                                                                   OPEN DEUTSCHE APOTHEKER- UND ÄRZTEBANK EG (5299007S3UH5RKUYDA52); DEUTSCHE BANK AKTIENGESELLSCHAFT (7LTWFZYICNSX8D621K86); DZ BANK AG Deutsche Zentral-Genossenschaftsbank, Frankfurt am Main (529900HNOAA1KXQJUQ27); DekaBank Deutsche Girozentrale (0W2PZJM8XOY22M4GG883); Deutsche Pfandbriefbank AG (DZZ47B9A52ZJ6LT6VV95)
    CBK                     Commerzbank                   commerzbank 851WYGNLUQLFZBSYGB56          COMMERZBANK Aktiengesellschaft contained                                                                                                                                                                                                                                                                                                                          
    SAN                 Banco Santander                     santander 5493006QMFDDMYWIAM13                   Banco Santander, S.A.     exact                                                                                                                                                                                                                                                                                                                          
   BBVA                            BBVA     bilbao vizcaya argentaria K8MS7FD7N5Z2WQ51AZ71   Banco Bilbao Vizcaya Argentaria, S.A.     exact                                                                                                                                                                                                                                                                                                                          
   CABK                       CaixaBank                     caixabank 7CUNS533WID6K7DGFI87                         CaixaBank, S.A.     exact                                                                                                                                                                                                                                                                                                                          
    SAB                  Banco Sabadell                      sabadell SI5RG2M0WQQLZCXKRM20                 Banco de Sabadell, S.A. contained                                                                                                                                                                                                                                                                                                                          
    BKT                       Bankinter                     bankinter VWMYAEQSTOPNV0SUGU82                         Bankinter, S.A.     exact                                                                                                                                                                                                                                                                                                                          
    UNI                   Unicaja Banco                       unicaja 5493007SJLLCTM6J6M37                     Unicaja Banco, S.A.     exact                                                                                                                                                                                                                                                                                                                          
    UCG                       UniCredit                     unicredit 549300TRUWO2CD2G5692          UNICREDIT, SOCIETA' PER AZIONI contained                                                                                                                                                                                                                                                                                                                          
    ISP                 Intesa Sanpaolo               intesa sanpaolo 2W8N8UU78PMDQKZENC08                  Intesa Sanpaolo S.p.A.     exact                                                                                                                                                                                                                                                                                                                          
   BAMI                       Banco BPM                           bpm 815600E4E6DCD2D25E30           BANCO BPM SOCIETA' PER AZIONI contained                                                                                                                                                                                                                                                                                                                          
    BPE                      BPER Banca                          bper N747OI7JINV7RUUH6190                       BPER Banca S.p.A.     exact                                                                                                                                                                                                                                                                                                                          
   BMPS Banca Monte dei Paschi di Siena     monte dei paschi di siena J4CP7MHCXR8DAQMKIL78  Banca Monte dei Paschi di Siena S.p.A.     exact
```

### config/eba_map_2021.csv (33 rows)

```
field    item    template                                                                                                                                                           label           dim_filter
              interest_income 2120301         P&L                                                                                                                                                 Interest income                   {}
             interest_expense 2120304         P&L                                                                                                                                               Interest expenses                   {}
              dividend_income 2120308         P&L                                                                                                                                                 Dividend income                   {}
                     net_fees 2120309         P&L                                                                                                                                   Net Fee and commission income                   {}
       total_operating_income 2120316         P&L                                                                                                                                     TOTAL OPERATING INCOME_ NET                   {}
               admin_expenses 2120317         P&L                                                                                                                                       (Administrative expenses)                   {}
       resolution_dgs_contrib 2120339         P&L                                                                                          (Cash contributions to resolution funds and deposit guarantee schemes)                   {}
                 depreciation 2120318         P&L                                                                                                                                                  (Depreciation)                   {}
              impairments_fin 2120324         P&L                                                (Impairment or (-) reversal of impairment on financial assets not measured at fair value through profit or loss)                   {}
                   provisions 2120319         P&L                                                                                                                      (Provisions or (-) reversal of provisions)                   {}
           impairments_nonfin 2120327         P&L                             (Impairment or (-) reversal of impairment of investments in subsidaries_ joint ventures and associates and on non-financial assets)                   {}
                          pbt 2120332         P&L                                                                                                        PROFIT OR (-) LOSS BEFORE TAX FROM CONTINUING OPERATIONS                   {}
                          pat 2120333         P&L                                                                                                         PROFIT OR (-) LOSS AFTER TAX FROM CONTINUING OPERATIONS                   {}
                profit_owners 2120336         P&L                                                                                 PROFIT OR (-) LOSS FOR THE YEAR - Of which attributable to owners of the parent                   {}
                 total_assets 2121010      Assets                                                                                                                                                    Total Assets                   {}
            total_liabilities 2121214 Liabilities                                                                                                                                               TOTAL LIABILITIES                   {}
                 total_equity 2121216 Liabilities                                                                                                                                                    TOTAL EQUITY                   {}
                      cash_cb 2121001      Assets                                                                                                  Cash, cash balances at central banks and other demand deposits                   {}
                    loans_all 2120603         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value)                   {}
       loans_households_gross 2120605         NPE                                                         Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure  {"Exposure": "401"}
                    npl_gross 2120603         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) {"Perf_Status": "2"}
                npl_allowance 2120613         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) {"Perf_Status": "2"}
               trading_assets 2121002      Assets                                                                                                                               Financial assets held for trading                   {}
                        tier1 2120133     Capital                                                                                           TIER 1 CAPITAL (net of deductions and after transitional adjustments)                   {}
                          rwa 2120220     RWA OV1                                                                                                                                      Total Risk exposure amount                   {}
              at1_instruments 2120129     Capital                                                                                                                           Additional Tier 1 Capital instruments                   {}
        intangibles_deduction 2120110     Capital                                                                                                                      (-) Intangible assets (including Goodwill)                   {}
gains_derecognition_not_fvtpl 2120310         P&L    Gains or (-) losses on derecognition of financial assets and liabilities not measured at fair value through profit or loss_ and of non financial assets_ net                   {}
       gains_held_for_trading 2120311         P&L                                                                                   Gains or (-) losses on financial assets and liabilities held for trading_ net                   {}
       gains_designated_fvtpl 2120312         P&L                                                    Gains or (-) losses on financial assets and liabilities designated at fair value through profit or loss_ net                   {}
       gains_hedge_accounting 2120313         P&L                                                                                                                  Gains or (-) losses from hedge accounting_ net                   {}
         exchange_differences 2120314         P&L                                                                                                                    Exchange differences [gain or (-) loss]_ net                   {}
          other_operating_net 2120315         P&L                                                                                                                          Net other operating income /(expenses)                   {}
```

### config/eba_map_2022.csv (33 rows)

```
field    item    template                                                                                                                                                           label           dim_filter
              interest_income 2220301         P&L                                                                                                                                                 Interest income                   {}
             interest_expense 2220304         P&L                                                                                                                                               Interest expenses                   {}
              dividend_income 2220308         P&L                                                                                                                                                 Dividend income                   {}
                     net_fees 2220309         P&L                                                                                                                                   Net Fee and commission income                   {}
       total_operating_income 2220316         P&L                                                                                                                                     TOTAL OPERATING INCOME_ NET                   {}
               admin_expenses 2220317         P&L                                                                                                                                       (Administrative expenses)                   {}
       resolution_dgs_contrib 2220339         P&L                                                                                          (Cash contributions to resolution funds and deposit guarantee schemes)                   {}
                 depreciation 2220318         P&L                                                                                                                                                  (Depreciation)                   {}
              impairments_fin 2220324         P&L                                                (Impairment or (-) reversal of impairment on financial assets not measured at fair value through profit or loss)                   {}
                   provisions 2220319         P&L                                                                                                                      (Provisions or (-) reversal of provisions)                   {}
           impairments_nonfin 2220327         P&L                             (Impairment or (-) reversal of impairment of investments in subsidaries_ joint ventures and associates and on non-financial assets)                   {}
                          pbt 2220332         P&L                                                                                                        PROFIT OR (-) LOSS BEFORE TAX FROM CONTINUING OPERATIONS                   {}
                          pat 2220333         P&L                                                                                                         PROFIT OR (-) LOSS AFTER TAX FROM CONTINUING OPERATIONS                   {}
                profit_owners 2220336         P&L                                                                                 PROFIT OR (-) LOSS FOR THE YEAR - Of which attributable to owners of the parent                   {}
                 total_assets 2221010      Assets                                                                                                                                                    Total Assets                   {}
            total_liabilities 2221214 Liabilities                                                                                                                                               TOTAL LIABILITIES                   {}
                 total_equity 2221216 Liabilities                                                                                                                                                    TOTAL EQUITY                   {}
                      cash_cb 2221001      Assets                                                                                                  Cash, cash balances at central banks and other demand deposits                   {}
                    loans_all 2220603         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value)                   {}
       loans_households_gross 2220605         NPE                                                         Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure  {"Exposure": "401"}
                    npl_gross 2220603         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) {"Perf_Status": "2"}
                npl_allowance 2220613         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) {"Perf_Status": "2"}
               trading_assets 2221002      Assets                                                                                                                               Financial assets held for trading                   {}
                        tier1 2220133     Capital                                                                                           TIER 1 CAPITAL (net of deductions and after transitional adjustments)                   {}
                          rwa 2220220     RWA OV1                                                                                                                                      Total Risk exposure amount                   {}
              at1_instruments 2220129     Capital                                                                                                                           Additional Tier 1 Capital instruments                   {}
        intangibles_deduction 2220110     Capital                                                                                                                      (-) Intangible assets (including Goodwill)                   {}
gains_derecognition_not_fvtpl 2220310         P&L    Gains or (-) losses on derecognition of financial assets and liabilities not measured at fair value through profit or loss_ and of non financial assets_ net                   {}
       gains_held_for_trading 2220311         P&L                                                                                   Gains or (-) losses on financial assets and liabilities held for trading_ net                   {}
       gains_designated_fvtpl 2220312         P&L                                                    Gains or (-) losses on financial assets and liabilities designated at fair value through profit or loss_ net                   {}
       gains_hedge_accounting 2220313         P&L                                                                                                                  Gains or (-) losses from hedge accounting_ net                   {}
         exchange_differences 2220314         P&L                                                                                                                    Exchange differences [gain or (-) loss]_ net                   {}
          other_operating_net 2220315         P&L                                                                                                                          Net other operating income /(expenses)                   {}
```

### config/eba_map_2023.csv (33 rows)

```
field    item    template                                                                                                                                                           label           dim_filter
              interest_income 2320301         P&L                                                                                                                                                 Interest income                   {}
             interest_expense 2320304         P&L                                                                                                                                               Interest expenses                   {}
              dividend_income 2320308         P&L                                                                                                                                                 Dividend income                   {}
                     net_fees 2320309         P&L                                                                                                                                   Net Fee and commission income                   {}
       total_operating_income 2320316         P&L                                                                                                                                     TOTAL OPERATING INCOME_ NET                   {}
               admin_expenses 2320317         P&L                                                                                                                                       (Administrative expenses)                   {}
       resolution_dgs_contrib 2320339         P&L                                                                                          (Cash contributions to resolution funds and deposit guarantee schemes)                   {}
                 depreciation 2320318         P&L                                                                                                                                                  (Depreciation)                   {}
              impairments_fin 2320324         P&L                                                (Impairment or (-) reversal of impairment on financial assets not measured at fair value through profit or loss)                   {}
                   provisions 2320319         P&L                                                                                                                      (Provisions or (-) reversal of provisions)                   {}
           impairments_nonfin 2320327         P&L                             (Impairment or (-) reversal of impairment of investments in subsidaries_ joint ventures and associates and on non-financial assets)                   {}
                          pbt 2320332         P&L                                                                                                        PROFIT OR (-) LOSS BEFORE TAX FROM CONTINUING OPERATIONS                   {}
                          pat 2320333         P&L                                                                                                         PROFIT OR (-) LOSS AFTER TAX FROM CONTINUING OPERATIONS                   {}
                profit_owners 2320336         P&L                                                                                 PROFIT OR (-) LOSS FOR THE YEAR - Of which attributable to owners of the parent                   {}
                 total_assets 2321010      Assets                                                                                                                                                    Total Assets                   {}
            total_liabilities 2321214 Liabilities                                                                                                                                               TOTAL LIABILITIES                   {}
                 total_equity 2321216 Liabilities                                                                                                                                                    TOTAL EQUITY                   {}
                      cash_cb 2321001      Assets                                                                                                  Cash, cash balances at central banks and other demand deposits                   {}
                    loans_all 2320603         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value)                   {}
       loans_households_gross 2320605         NPE                                                         Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure  {"Exposure": "401"}
                    npl_gross 2320603         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) {"Perf_Status": "2"}
                npl_allowance 2320613         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) {"Perf_Status": "2"}
               trading_assets 2321002      Assets                                                                                                                               Financial assets held for trading                   {}
                        tier1 2320133     Capital                                                                                           TIER 1 CAPITAL (net of deductions and after transitional adjustments)                   {}
                          rwa 2320220     RWA OV1                                                                                                                                      Total Risk exposure amount                   {}
              at1_instruments 2320129     Capital                                                                                                                           Additional Tier 1 Capital instruments                   {}
        intangibles_deduction 2320110     Capital                                                                                                                      (-) Intangible assets (including Goodwill)                   {}
gains_derecognition_not_fvtpl 2320310         P&L    Gains or (-) losses on derecognition of financial assets and liabilities not measured at fair value through profit or loss_ and of non financial assets_ net                   {}
       gains_held_for_trading 2320311         P&L                                                                                   Gains or (-) losses on financial assets and liabilities held for trading_ net                   {}
       gains_designated_fvtpl 2320312         P&L                                                    Gains or (-) losses on financial assets and liabilities designated at fair value through profit or loss_ net                   {}
       gains_hedge_accounting 2320313         P&L                                                                                                                  Gains or (-) losses from hedge accounting_ net                   {}
         exchange_differences 2320314         P&L                                                                                                                    Exchange differences [gain or (-) loss]_ net                   {}
          other_operating_net 2320315         P&L                                                                                                                          Net other operating income /(expenses)                   {}
```

### config/eba_map_2024.csv (33 rows)

```
field    item    template                                                                                                                                                           label           dim_filter
              interest_income 2420301         P&L                                                                                                                                                 Interest income                   {}
             interest_expense 2420304         P&L                                                                                                                                               Interest expenses                   {}
              dividend_income 2420308         P&L                                                                                                                                                 Dividend income                   {}
                     net_fees 2420309         P&L                                                                                                                                   Net Fee and commission income                   {}
       total_operating_income 2420316         P&L                                                                                                                                     TOTAL OPERATING INCOME_ NET                   {}
               admin_expenses 2420317         P&L                                                                                                                                       (Administrative expenses)                   {}
       resolution_dgs_contrib 2420339         P&L                                                                                          (Cash contributions to resolution funds and deposit guarantee schemes)                   {}
                 depreciation 2420318         P&L                                                                                                                                                  (Depreciation)                   {}
              impairments_fin 2420324         P&L                                                (Impairment or (-) reversal of impairment on financial assets not measured at fair value through profit or loss)                   {}
                   provisions 2420319         P&L                                                                                                                      (Provisions or (-) reversal of provisions)                   {}
           impairments_nonfin 2420327         P&L                             (Impairment or (-) reversal of impairment of investments in subsidaries_ joint ventures and associates and on non-financial assets)                   {}
                          pbt 2420332         P&L                                                                                                        PROFIT OR (-) LOSS BEFORE TAX FROM CONTINUING OPERATIONS                   {}
                          pat 2420333         P&L                                                                                                         PROFIT OR (-) LOSS AFTER TAX FROM CONTINUING OPERATIONS                   {}
                profit_owners 2420336         P&L                                                                                 PROFIT OR (-) LOSS FOR THE YEAR - Of which attributable to owners of the parent                   {}
                 total_assets 2421010      Assets                                                                                                                                                    Total Assets                   {}
            total_liabilities 2421214 Liabilities                                                                                                                                               TOTAL LIABILITIES                   {}
                 total_equity 2421216 Liabilities                                                                                                                                                    TOTAL EQUITY                   {}
                      cash_cb 2421001      Assets                                                                                                  Cash, cash balances at central banks and other demand deposits                   {}
                    loans_all 2420603         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value)                   {}
       loans_households_gross 2420605         NPE                                                         Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure  {"Exposure": "401"}
                    npl_gross 2420603         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) {"Perf_Status": "2"}
                npl_allowance 2420613         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) {"Perf_Status": "2"}
               trading_assets 2421002      Assets                                                                                                                               Financial assets held for trading                   {}
                        tier1 2420133     Capital                                                                                           TIER 1 CAPITAL (net of deductions and after transitional adjustments)                   {}
                          rwa 2420220     RWA OV1                                                                                                                                      Total Risk exposure amount                   {}
              at1_instruments 2420129     Capital                                                                                                                           Additional Tier 1 Capital instruments                   {}
        intangibles_deduction 2420110     Capital                                                                                                                      (-) Intangible assets (including Goodwill)                   {}
gains_derecognition_not_fvtpl 2420310         P&L    Gains or (-) losses on derecognition of financial assets and liabilities not measured at fair value through profit or loss_ and of non financial assets_ net                   {}
       gains_held_for_trading 2420311         P&L                                                                                   Gains or (-) losses on financial assets and liabilities held for trading_ net                   {}
       gains_designated_fvtpl 2420312         P&L                                                    Gains or (-) losses on financial assets and liabilities designated at fair value through profit or loss_ net                   {}
       gains_hedge_accounting 2420313         P&L                                                                                                                  Gains or (-) losses from hedge accounting_ net                   {}
         exchange_differences 2420314         P&L                                                                                                                    Exchange differences [gain or (-) loss]_ net                   {}
          other_operating_net 2420315         P&L                                                                                                                          Net other operating income /(expenses)                   {}
```

### config/eba_map_2025.csv (33 rows)

```
field    item    template                                                                                                                                                           label           dim_filter
              interest_income 2520301         P&L                                                                                                                                                 Interest income                   {}
             interest_expense 2520304         P&L                                                                                                                                               Interest expenses                   {}
              dividend_income 2520308         P&L                                                                                                                                                 Dividend income                   {}
                     net_fees 2520309         P&L                                                                                                                                   Net Fee and commission income                   {}
       total_operating_income 2520316         P&L                                                                                                                                     TOTAL OPERATING INCOME_ NET                   {}
               admin_expenses 2520317         P&L                                                                                                                                       (Administrative expenses)                   {}
       resolution_dgs_contrib 2520339         P&L                                                                                          (Cash contributions to resolution funds and deposit guarantee schemes)                   {}
                 depreciation 2520318         P&L                                                                                                                                                  (Depreciation)                   {}
              impairments_fin 2520324         P&L                                                (Impairment or (-) reversal of impairment on financial assets not measured at fair value through profit or loss)                   {}
                   provisions 2520319         P&L                                                                                                                      (Provisions or (-) reversal of provisions)                   {}
           impairments_nonfin 2520327         P&L                             (Impairment or (-) reversal of impairment of investments in subsidaries_ joint ventures and associates and on non-financial assets)                   {}
                          pbt 2520332         P&L                                                                                                        PROFIT OR (-) LOSS BEFORE TAX FROM CONTINUING OPERATIONS                   {}
                          pat 2520333         P&L                                                                                                         PROFIT OR (-) LOSS AFTER TAX FROM CONTINUING OPERATIONS                   {}
                profit_owners 2520336         P&L                                                                                 PROFIT OR (-) LOSS FOR THE YEAR - Of which attributable to owners of the parent                   {}
                 total_assets 2521010      Assets                                                                                                                                                    Total Assets                   {}
            total_liabilities 2521214 Liabilities                                                                                                                                               TOTAL LIABILITIES                   {}
                 total_equity 2521216 Liabilities                                                                                                                                                    TOTAL EQUITY                   {}
                      cash_cb 2521001      Assets                                                                                                  Cash, cash balances at central banks and other demand deposits                   {}
                    loans_all 2520603         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value)                   {}
       loans_households_gross 2520605         NPE                                                         Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure  {"Exposure": "401"}
                    npl_gross 2520603         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) {"Perf_Status": "2"}
                npl_allowance 2520613         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) {"Perf_Status": "2"}
               trading_assets 2521002      Assets                                                                                                                               Financial assets held for trading                   {}
                        tier1 2520133     Capital                                                                                           TIER 1 CAPITAL (net of deductions and after transitional adjustments)                   {}
                          rwa 2520220     RWA OV1                                                                                                                                      Total Risk exposure amount                   {}
              at1_instruments 2520129     Capital                                                                                                                           Additional Tier 1 Capital instruments                   {}
        intangibles_deduction 2520110     Capital                                                                                                                      (-) Intangible assets (including Goodwill)                   {}
gains_derecognition_not_fvtpl 2520310         P&L    Gains or (-) losses on derecognition of financial assets and liabilities not measured at fair value through profit or loss_ and of non financial assets_ net                   {}
       gains_held_for_trading 2520311         P&L                                                                                   Gains or (-) losses on financial assets and liabilities held for trading_ net                   {}
       gains_designated_fvtpl 2520312         P&L                                                    Gains or (-) losses on financial assets and liabilities designated at fair value through profit or loss_ net                   {}
       gains_hedge_accounting 2520313         P&L                                                                                                                  Gains or (-) losses from hedge accounting_ net                   {}
         exchange_differences 2520314         P&L                                                                                                                    Exchange differences [gain or (-) loss]_ net                   {}
          other_operating_net 2520315         P&L                                                                                                                          Net other operating income /(expenses)                   {}
```

### Map notes (label differences and unmapped fields)

```
(none)
```

### OPEN fields: every candidate item per release

```
release                     field    item    template                                                                                                                                                                         label                                         dim_filter                                       found
    2021                      cet1 2120102     Capital                                                                                  COMMON EQUITY TIER 1 CAPITAL (net of deductions and after applying transitional adjustments)                                                 {}                                         yes
    2021                      cet1 2120143     Capital                                                                                                                                   COMMON EQUITY TIER 1 CAPITAL (fully loaded)                                                 {}                                         yes
    2021       cet1_ratio_reported 2120140     Capital                                                                                                                      COMMON EQUITY TIER 1 CAPITAL RATIO (transitional period)                                                 {}                                         yes
    2021       cet1_ratio_reported 2120146     Capital                                                                                                                             COMMON EQUITY TIER 1 CAPITAL RATIO (fully loaded)                                                 {}                                         yes
    2021       cet1_ratio_reported             Capital                                                                                                          COMMON EQUITY TIER 1 CAPITAL RATIO (transitional period - pre floor)                                                 {} 0 items with this label in template Capital
    2021         leverage_exposure 2120903    Leverage                                                                                            Total leverage ratio exposures - using a transitional definition of Tier 1 capital                                                 {}                                         yes
    2021         leverage_exposure 2120904    Leverage                                                                                         Total leverage ratio exposures - using a fully phased-in definition of Tier 1 capital                                                 {}                                         yes
    2021           debt_securities 2120602         NPE                                                                                        Gross carrying amount on Debt securities (including at amortised cost  and fair value)                                                 {}                                         yes
    2021           debt_securities 2121016      Assets                                                                     Gross carrying amount: Financial assets at fair value through other comprehensive income, Debt securities                                                 {}                                         yes
    2021           debt_securities 2121018      Assets                                                                                                    Gross carrying amount: Financial assets at amortised cost, Debt securities                                                 {}                                         yes
    2021     loans_customers_gross 2120605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "102"}                                         yes
    2021     loans_customers_gross 2120605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "202"}                                         yes
    2021     loans_customers_gross 2120605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "301"}                                         yes
    2021     loans_customers_gross 2120605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "401"}                                         yes
    2021 loans_customers_allowance 2120615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "102", "Perf_Status": "1"}                                         yes
    2021 loans_customers_allowance 2120615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "102", "Perf_Status": "2"}                                         yes
    2021 loans_customers_allowance 2120615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "202", "Perf_Status": "1"}                                         yes
    2021 loans_customers_allowance 2120615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "202", "Perf_Status": "2"}                                         yes
    2021 loans_customers_allowance 2120615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "301", "Perf_Status": "1"}                                         yes
    2021 loans_customers_allowance 2120615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "301", "Perf_Status": "2"}                                         yes
    2021 loans_customers_allowance 2120615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "401", "Perf_Status": "1"}                                         yes
    2021 loans_customers_allowance 2120615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "401", "Perf_Status": "2"}                                         yes
    2021        deposits_customers 2121215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "102", "Financial_instruments": "30"}                                         yes
    2021        deposits_customers 2121215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "202", "Financial_instruments": "30"}                                         yes
    2021        deposits_customers 2121215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "301", "Financial_instruments": "30"}                                         yes
    2021        deposits_customers 2121215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "401", "Financial_instruments": "30"}                                         yes
    2022                      cet1 2220102     Capital                                                                                  COMMON EQUITY TIER 1 CAPITAL (net of deductions and after applying transitional adjustments)                                                 {}                                         yes
    2022                      cet1 2220143     Capital                                                                                                                                   COMMON EQUITY TIER 1 CAPITAL (fully loaded)                                                 {}                                         yes
    2022       cet1_ratio_reported 2220140     Capital                                                                                                                      COMMON EQUITY TIER 1 CAPITAL RATIO (transitional period)                                                 {}                                         yes
    2022       cet1_ratio_reported 2220146     Capital                                                                                                                             COMMON EQUITY TIER 1 CAPITAL RATIO (fully loaded)                                                 {}                                         yes
    2022       cet1_ratio_reported             Capital                                                                                                          COMMON EQUITY TIER 1 CAPITAL RATIO (transitional period - pre floor)                                                 {} 0 items with this label in template Capital
    2022         leverage_exposure 2220903    Leverage                                                                                            Total leverage ratio exposures - using a transitional definition of Tier 1 capital                                                 {}                                         yes
    2022         leverage_exposure 2220904    Leverage                                                                                         Total leverage ratio exposures - using a fully phased-in definition of Tier 1 capital                                                 {}                                         yes
    2022           debt_securities 2220602         NPE                                                                                        Gross carrying amount on Debt securities (including at amortised cost  and fair value)                                                 {}                                         yes
    2022           debt_securities 2221016      Assets                                                                     Gross carrying amount: Financial assets at fair value through other comprehensive income, Debt securities                                                 {}                                         yes
    2022           debt_securities 2221018      Assets                                                                                                    Gross carrying amount: Financial assets at amortised cost, Debt securities                                                 {}                                         yes
    2022     loans_customers_gross 2220605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "102"}                                         yes
    2022     loans_customers_gross 2220605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "202"}                                         yes
    2022     loans_customers_gross 2220605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "301"}                                         yes
    2022     loans_customers_gross 2220605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "401"}                                         yes
    2022 loans_customers_allowance 2220615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "102", "Perf_Status": "1"}                                         yes
    2022 loans_customers_allowance 2220615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "102", "Perf_Status": "2"}                                         yes
    2022 loans_customers_allowance 2220615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "202", "Perf_Status": "1"}                                         yes
    2022 loans_customers_allowance 2220615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "202", "Perf_Status": "2"}                                         yes
    2022 loans_customers_allowance 2220615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "301", "Perf_Status": "1"}                                         yes
    2022 loans_customers_allowance 2220615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "301", "Perf_Status": "2"}                                         yes
    2022 loans_customers_allowance 2220615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "401", "Perf_Status": "1"}                                         yes
    2022 loans_customers_allowance 2220615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "401", "Perf_Status": "2"}                                         yes
    2022        deposits_customers 2221215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "102", "Financial_instruments": "30"}                                         yes
    2022        deposits_customers 2221215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "202", "Financial_instruments": "30"}                                         yes
    2022        deposits_customers 2221215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "301", "Financial_instruments": "30"}                                         yes
    2022        deposits_customers 2221215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "401", "Financial_instruments": "30"}                                         yes
    2023                      cet1 2320102     Capital                                                                                  COMMON EQUITY TIER 1 CAPITAL (net of deductions and after applying transitional adjustments)                                                 {}                                         yes
    2023                      cet1 2320143     Capital                                                                                                                                   COMMON EQUITY TIER 1 CAPITAL (fully loaded)                                                 {}                                         yes
    2023       cet1_ratio_reported 2320140     Capital                                                                                                                      COMMON EQUITY TIER 1 CAPITAL RATIO (transitional period)                                                 {}                                         yes
    2023       cet1_ratio_reported 2320146     Capital                                                                                                                             COMMON EQUITY TIER 1 CAPITAL RATIO (fully loaded)                                                 {}                                         yes
    2023       cet1_ratio_reported             Capital                                                                                                          COMMON EQUITY TIER 1 CAPITAL RATIO (transitional period - pre floor)                                                 {} 0 items with this label in template Capital
    2023         leverage_exposure 2320903    Leverage                                                                                            Total leverage ratio exposures - using a transitional definition of Tier 1 capital                                                 {}                                         yes
    2023         leverage_exposure 2320904    Leverage                                                                                         Total leverage ratio exposures - using a fully phased-in definition of Tier 1 capital                                                 {}                                         yes
    2023           debt_securities 2320602         NPE                                                                                        Gross carrying amount on Debt securities (including at amortised cost  and fair value)                                                 {}                                         yes
    2023           debt_securities 2321016      Assets                                                                     Gross carrying amount: Financial assets at fair value through other comprehensive income, Debt securities                                                 {}                                         yes
    2023           debt_securities 2321018      Assets                                                                                                    Gross carrying amount: Financial assets at amortised cost, Debt securities                                                 {}                                         yes
    2023     loans_customers_gross 2320605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "102"}                                         yes
    2023     loans_customers_gross 2320605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "202"}                                         yes
    2023     loans_customers_gross 2320605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "301"}                                         yes
    2023     loans_customers_gross 2320605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "401"}                                         yes
    2023 loans_customers_allowance 2320615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "102", "Perf_Status": "1"}                                         yes
    2023 loans_customers_allowance 2320615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "102", "Perf_Status": "2"}                                         yes
    2023 loans_customers_allowance 2320615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "202", "Perf_Status": "1"}                                         yes
    2023 loans_customers_allowance 2320615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "202", "Perf_Status": "2"}                                         yes
    2023 loans_customers_allowance 2320615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "301", "Perf_Status": "1"}                                         yes
    2023 loans_customers_allowance 2320615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "301", "Perf_Status": "2"}                                         yes
    2023 loans_customers_allowance 2320615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "401", "Perf_Status": "1"}                                         yes
    2023 loans_customers_allowance 2320615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "401", "Perf_Status": "2"}                                         yes
    2023        deposits_customers 2321215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "102", "Financial_instruments": "30"}                                         yes
    2023        deposits_customers 2321215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "202", "Financial_instruments": "30"}                                         yes
    2023        deposits_customers 2321215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "301", "Financial_instruments": "30"}                                         yes
    2023        deposits_customers 2321215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "401", "Financial_instruments": "30"}                                         yes
    2024                      cet1 2420102     Capital                                                                                  COMMON EQUITY TIER 1 CAPITAL (net of deductions and after applying transitional adjustments)                                                 {}                                         yes
    2024                      cet1 2420143     Capital                                                                                                                                   COMMON EQUITY TIER 1 CAPITAL (fully loaded)                                                 {}                                         yes
    2024       cet1_ratio_reported 2420140     Capital                                                                                                                      COMMON EQUITY TIER 1 CAPITAL RATIO (transitional period)                                                 {}                                         yes
    2024       cet1_ratio_reported 2420146     Capital                                                                                                                             COMMON EQUITY TIER 1 CAPITAL RATIO (fully loaded)                                                 {}                                         yes
    2024       cet1_ratio_reported             Capital                                                                                                          COMMON EQUITY TIER 1 CAPITAL RATIO (transitional period - pre floor)                                                 {} 0 items with this label in template Capital
    2024         leverage_exposure 2420903    Leverage                                                                                            Total leverage ratio exposures - using a transitional definition of Tier 1 capital                                                 {}                                         yes
    2024         leverage_exposure 2420904    Leverage                                                                                         Total leverage ratio exposures - using a fully phased-in definition of Tier 1 capital                                                 {}                                         yes
    2024           debt_securities 2420602         NPE                                                                                        Gross carrying amount on Debt securities (including at amortised cost  and fair value)                                                 {}                                         yes
    2024           debt_securities 2421016      Assets                                                                     Gross carrying amount: Financial assets at fair value through other comprehensive income, Debt securities                                                 {}                                         yes
    2024           debt_securities 2421018      Assets                                                                                                    Gross carrying amount: Financial assets at amortised cost, Debt securities                                                 {}                                         yes
    2024     loans_customers_gross 2420605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "102"}                                         yes
    2024     loans_customers_gross 2420605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "202"}                                         yes
    2024     loans_customers_gross 2420605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "301"}                                         yes
    2024     loans_customers_gross 2420605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "401"}                                         yes
    2024 loans_customers_allowance 2420615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "102", "Perf_Status": "1"}                                         yes
    2024 loans_customers_allowance 2420615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "102", "Perf_Status": "2"}                                         yes
    2024 loans_customers_allowance 2420615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "202", "Perf_Status": "1"}                                         yes
    2024 loans_customers_allowance 2420615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "202", "Perf_Status": "2"}                                         yes
    2024 loans_customers_allowance 2420615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "301", "Perf_Status": "1"}                                         yes
    2024 loans_customers_allowance 2420615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "301", "Perf_Status": "2"}                                         yes
    2024 loans_customers_allowance 2420615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "401", "Perf_Status": "1"}                                         yes
    2024 loans_customers_allowance 2420615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "401", "Perf_Status": "2"}                                         yes
    2024        deposits_customers 2421215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "102", "Financial_instruments": "30"}                                         yes
    2024        deposits_customers 2421215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "202", "Financial_instruments": "30"}                                         yes
    2024        deposits_customers 2421215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "301", "Financial_instruments": "30"}                                         yes
    2024        deposits_customers 2421215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "401", "Financial_instruments": "30"}                                         yes
    2025                      cet1 2520102     Capital                                                                                  COMMON EQUITY TIER 1 CAPITAL (net of deductions and after applying transitional adjustments)                                                 {}                                         yes
    2025                      cet1 2520143     Capital                                                                                                                                   COMMON EQUITY TIER 1 CAPITAL (fully loaded)                                                 {}                                         yes
    2025       cet1_ratio_reported 2520140     Capital                                                                                                                      COMMON EQUITY TIER 1 CAPITAL RATIO (transitional period)                                                 {}                                         yes
    2025       cet1_ratio_reported 2520146     Capital                                                                                                                             COMMON EQUITY TIER 1 CAPITAL RATIO (fully loaded)                                                 {}                                         yes
    2025       cet1_ratio_reported 2520155     Capital                                                                                                          COMMON EQUITY TIER 1 CAPITAL RATIO (transitional period - pre floor)                                                 {}                                         yes
    2025         leverage_exposure 2520903    Leverage                                                                                            Total leverage ratio exposures - using a transitional definition of Tier 1 capital                                                 {}                                         yes
    2025         leverage_exposure 2520904    Leverage                                                                                         Total leverage ratio exposures - using a fully phased-in definition of Tier 1 capital                                                 {}                                         yes
    2025           debt_securities 2520602         NPE                                                                                        Gross carrying amount on Debt securities (including at amortised cost  and fair value)                                                 {}                                         yes
    2025           debt_securities 2521016      Assets                                                                     Gross carrying amount: Financial assets at fair value through other comprehensive income, Debt securities                                                 {}                                         yes
    2025           debt_securities 2521018      Assets                                                                                                    Gross carrying amount: Financial assets at amortised cost, Debt securities                                                 {}                                         yes
    2025     loans_customers_gross 2520605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "102"}                                         yes
    2025     loans_customers_gross 2520605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "202"}                                         yes
    2025     loans_customers_gross 2520605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "301"}                                         yes
    2025     loans_customers_gross 2520605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "401"}                                         yes
    2025 loans_customers_allowance 2520615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "102", "Perf_Status": "1"}                                         yes
    2025 loans_customers_allowance 2520615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "102", "Perf_Status": "2"}                                         yes
    2025 loans_customers_allowance 2520615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "202", "Perf_Status": "1"}                                         yes
    2025 loans_customers_allowance 2520615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "202", "Perf_Status": "2"}                                         yes
    2025 loans_customers_allowance 2520615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "301", "Perf_Status": "1"}                                         yes
    2025 loans_customers_allowance 2520615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "301", "Perf_Status": "2"}                                         yes
    2025 loans_customers_allowance 2520615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "401", "Perf_Status": "1"}                                         yes
    2025 loans_customers_allowance 2520615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "401", "Perf_Status": "2"}                                         yes
    2025        deposits_customers 2521215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "102", "Financial_instruments": "30"}                                         yes
    2025        deposits_customers 2521215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "202", "Financial_instruments": "30"}                                         yes
    2025        deposits_customers 2521215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "301", "Financial_instruments": "30"}                                         yes
    2025        deposits_customers 2521215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "401", "Financial_instruments": "30"}                                         yes
```

### Fields of [5.1] not taken from EBA

```
lcr            OPEN-05 (a): no family for EU banks to 2025-06-30
nsfr           OPEN-05 (a): no family for EU banks to 2025-06-30
fte                                           report family only
customers                                     report family only
at1_coupons                                   report family only
shares_out                                    report family only
```

### Map check: (bank, date) pairs each map row selects, and the most rows any pair gets

Every dimension column not in `dim_filter` is held at 0 (Total / No breakdown).

```
                               pairs_2021  pairs_2022  pairs_2023  pairs_2024  pairs_2025  max_rows_per_pair
admin_expenses                         90          95          98          98          98                  1
at1_instruments                        90          95          98         100          99                  1
cash_cb                                90          95          98          98          98                  1
depreciation                           90          95          98          98          98                  1
dividend_income                        90          95          98          98          98                  1
exchange_differences                   90          95          98          98          98                  1
gains_derecognition_not_fvtpl          90          95          98          98          98                  1
gains_designated_fvtpl                 90          95          98          98          98                  1
gains_hedge_accounting                 90          95          98          98          98                  1
gains_held_for_trading                 90          95          98          98          98                  1
impairments_fin                        90          95          98          98          98                  1
impairments_nonfin                     90          95          98          98          98                  1
intangibles_deduction                  90          95          98         100          99                  1
interest_expense                       90          95          98          98          98                  1
interest_income                        90          95          98          98          98                  1
loans_all                              90          95          98          98          98                  1
loans_households_gross                 90          95          98          98          98                  1
net_fees                               90          95          98          98          98                  1
npl_allowance                          90          95          98          98          98                  1
npl_gross                              90          95          98          98          98                  1
other_operating_net                    90          95          98          98          98                  1
pat                                    90          95          98          98          98                  1
pbt                                    90          95          98          98          98                  1
profit_owners                          90          95          98          98          98                  1
provisions                             90          95          98          98          98                  1
resolution_dgs_contrib                 90          95          98          98          98                  1
rwa                                    90          95          98         100          99                  1
tier1                                  90          95          98         100          99                  1
total_assets                           90          95          98          98          98                  1
total_equity                           90          95          98          98          98                  1
total_liabilities                      90          95          98          98          98                  1
total_operating_income                 90          95          98          98          98                  1
trading_assets                         90          95          98          98          98                  1
```


### Stop evidence: OPEN-25

#### OPEN-25: raw EBA rows (amounts in EUR millions for SEK, NOK and DKK banks; ratios as decimals)

```
bank_id             LEI_Code NSA Period    Item                                                    Label           Amount
    DNB 549300GKFG0RYRRQ1414  NO 202412 2521010                                             Total Assets 276393.428662484
   SWED M312WZV08Y7LYUC71685  SE 202412 2521010                                             Total Assets 226125.305436774
 DANSKE MAES062Z21O4RZ2U7M96  DK 202412 2521010                                             Total Assets 425547.216514122
    ISP 2W8N8UU78PMDQKZENC08  IT 202212 2320140 COMMON EQUITY TIER 1 CAPITAL RATIO (transitional period)     0.1380041507
```

Universe report_ccy for these banks:

```
bank_id report_ccy
    DNB        NOK
 DANSKE        DKK
   SWED        SEK
    ISP        EUR
```

#### OPEN-25: unit search in every committed SDD.xlsx and TR_Metadata.xlsx

Pattern `mln|million|unit(s)|EUR|euro` (whole words, any case) over every cell and comment.

```
 release             file  sheets  non_empty_cells  cell_comments  cells_naming_a_unit
    2021         SDD.xlsx       1             3741              0                    0
    2021 TR_Metadata.xlsx      17             4083              0                    1
    2022         SDD.xlsx       1             3783              0                    0
    2022 TR_Metadata.xlsx      17             4045              1                    1
    2023         SDD.xlsx       1             4370              0                    0
    2023 TR_Metadata.xlsx      17             4148              0                    1
    2024         SDD.xlsx       1             4717              0                    0
    2024 TR_Metadata.xlsx      17             4538              0                    1
    2025         SDD.xlsx       1             5253              0                    0
    2025 TR_Metadata.xlsx      17             4978              0                    1
```

#### OPEN-25: unit headings in 2025_EU-wide_Transparency_exercise_Mapped_templates.xlsx (not committed)

Downloaded once to a scratch folder from `https://www.eba.europa.eu/assets/TE2025/Full_database/883401/2025_EU-wide_Transparency_exercise_Mapped_templates.xlsx`.

```
             sheet       heading
          Leverage (mln EUR,  %)
           Capital (mln EUR,  %)
           RWA OV1 (mln EUR,  %)
               P&L     (mln EUR)
            Assets     (mln EUR)
       Liabilities     (mln EUR)
       Market Risk     (mln EUR)
 Credit Risk_STA_a (mln EUR,  %)
 Credit Risk_STA_b (mln EUR,  %)
 Credit Risk_IRB_a (mln EUR,  %)
 Credit Risk_IRB_b (mln EUR,  %)
         Sovereign     (mln EUR)
               NPE     (mln EUR)
Forborne exposures     (mln EUR)
              NACE     (mln EUR)
        Collateral     (mln EUR)
```


The 1 TR_Metadata hit per release is `FEMIP (Facility for Euro-Mediterranean Investment and Partnership)` on the Country sheet. The 2022 cell comment is Excel's threaded-comment notice on an institution row. Neither states a unit.

## Tests run

```
$ pytest -p socket --disable-socket -q
...                                                                      [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\_pytest\config\__init__.py:894
  C:\Utkarsh\10. Quant Projects\15) Bank Benchmarking Project\Bank-Performance-Benchmarking\.venv\Lib\site-packages\_pytest\config\__init__.py:894: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; socket
    self.import_plugin(arg, consider_entry_points=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
3 passed, 1 warning in 20.49s
$ ruff check .
All checks passed!

```

## Fresh-clone check

The step commits were pushed first, so that the clone is of the pushed repo (rule 12). Clone path `C:\Users\astha\AppData\Local\Temp\bpb1`, Windows 11, uv 0.11.6. The `uv pip install -r` output is cut to its last 2 lines.

```
$ git clone https://github.com/uty101/Bank-Performance-Benchmarking.git /c/Users/astha/AppData/Local/Temp/bpb1
e028dab step 1.2: EU LEIs from the 2025 release and EBA field maps
$ uv venv --python 3.12
Using CPython 3.12.13
Creating virtual environment at: .venv
Activate with: .venv\Scripts\activate
$ uv pip install -r requirements-lock.txt
 + wrapt==2.5.2
 + yfinance==1.7.0
$ uv pip install -e . --no-deps
Installed 1 package in 105ms
 + bpb==0.1.0 (from file:///C:/Users/astha/AppData/Local/Temp/bpb1)
$ ruff check .
All checks passed!
$ pytest -p socket --disable-socket -q
...                                                                      [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\_pytest\config\__init__.py:894
  C:\Users\astha\AppData\Local\Temp\bpb1\.venv\Lib\site-packages\_pytest\config\__init__.py:894: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; socket
    self.import_plugin(arg, consider_entry_points=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
3 passed, 1 warning in 32.41s
$ git status --porcelain

```

`git status --porcelain` printed nothing.

## Runtime per step

- 1.0: no computation (file edits).
- 1.1: `python scripts/pull_data.py --stage eba` took 5 m 38 s (wall), mostly download of 679 MB.
- 1.2: `python scripts/build_eba_maps.py` took 29.7 s (wall).
- Test suite: 20.5 s locally, 32.4 s on the fresh clone, most of it in `test_reference_dates` reading the gzipped CSVs.

## Deviations from PLAN.md

1. The 2021 release page is `.../eu-wide-transparency-exercise/2021-eu-wide-transparency`, since the path in instruction 01 returns 404, and the 2025 release page is the hub (see 1.1).
2. The country filter reads `NSA`, the bank's country. Instruction 01 says "the country column", and `tr_cre.csv` also has an exposure `Country` column, which is not used.
3. `MANIFEST.json` is `{"files": [...]}`, one entry per file with path, committed, url, pulled_utc, sha256, bytes, rows, first_date, last_date and encoding. A filtered file also has filtered_from and filter. Rows and dates are null for the xlsx files.
4. The map builder is `scripts/build_eba_maps.py`, with no network access. No file was named for it.
5. Name containment is matched on whole words (see 1.2).
6. `dim_filter` holds dimension codes, and unnamed dimensions are held at 0.
7. The 6 OPEN-06 components are named `gains_derecognition_not_fvtpl`, `gains_held_for_trading`, `gains_designated_fvtpl`, `gains_hedge_accounting`, `exchange_differences` and `other_operating_net`. Each was added to `fields.yaml` (kind pl) and to `source_map.yaml` with the standard rules, so `load_eba` can carry them.
8. `cet1_ratio_reported` was given the `capital` source-map rules in step 1.0: eba to 2025-06-30, p3 at EU bridge dates, report for UK banks. Instruction 01 fixed its EBA source only.
9. There were 3 pushes rather than 1: the step commits (for the fresh-clone check), the review, then the status file.

## Not verified

- Steps 1.3 to 1.7: not built.
- The NPE line used for `loans_all` and `npl_gross` (2520603, "including at amortised cost and fair value") covers every portfolio other than held for trading. It has not been reconciled with any bank's reported total loans.
- Whether a re-run of the filter on another machine gives the same gzip bytes. The gzip header is fixed (mtime 0, no file name), but the deflate stream depends on the zlib build. `test_manifest_hashes` checks the committed bytes, not a re-run.
- The P&L and capital signs seen in the raw rows were checked by eye only, since load_eba is not built. Expenses are positive (Intesa Sanpaolo administrative expenses 10,463.6 at 2022-12-31), and `(-)` deductions are negative (intangibles −8,200.8).

## Open questions

All are in `decisions/OPEN.md` with 2 options each.

1. **OPEN-25 (stop):** where the EBA unit is read from, and whether EBA amounts stay in EUR for SEK, NOK and DKK banks.
2. OPEN-17: DBK's LEI (no unique name match).
3. OPEN-18: `cet1`, transitional or fully loaded.
4. OPEN-19: `cet1_ratio_reported`, transitional or fully loaded (or pre-floor in 2025).
5. OPEN-20: `leverage_exposure`, transitional or fully phased-in.
6. OPEN-21: `debt_securities`: no all-portfolio carrying amount line (blocks iea and nim).
7. OPEN-22: `loans_customers_gross` and `_allowance` need a sum over Exposure rows (blocks cost_of_risk and loan_deposit).
8. OPEN-23: `deposits_customers` needs a sum over 4 sectors (blocks loan_deposit).
9. OPEN-24: `minority_interests` has no EBA line (blocks tangible_equity, for Section 3).

Data facts for the reviewer, not decisions: DNB's first EBA date is 2022-06-30, BPER is absent from the 2021 release, and Rabobank reports only at 30 Jun and 31 Dec in the 2021 to 2023 releases (see the coverage table). For DNB, every averaged KPI for FY2022 needs a 2021-12-31 balance, which no release holds, so DNB's first averaged EBA KPI will be the rolling 12 months at 2023-06-30. BPER's first averaged KPI is FY2022, for the same reason.

## Files changed

```
 .gitignore                         |   1 +
 CLAUDE.md                          |  12 ++
 PLAN.md                            |  59 +++---
 config/eba_map_2021.csv            |  34 ++++
 config/eba_map_2022.csv            |  34 ++++
 config/eba_map_2023.csv            |  34 ++++
 config/eba_map_2024.csv            |  34 ++++
 config/eba_map_2025.csv            |  34 ++++
 config/fields.yaml                 |  13 +-
 config/source_map.yaml             |  36 ++--
 data/manual/eba_urls.csv           |  21 +++
 data/manual/universe.csv           |  64 +++----
 data/raw/MANIFEST.json             | 374 +++++++++++++++++++++++++++++++++++++
 data/raw/eba/2021/SDD.xlsx         | Bin 0 -> 36034 bytes
 data/raw/eba/2021/TR_Metadata.xlsx | Bin 0 -> 139809 bytes
 data/raw/eba/2021/tr_cre.csv.gz    | Bin 0 -> 3821270 bytes
 data/raw/eba/2021/tr_oth.csv.gz    | Bin 0 -> 725631 bytes
 data/raw/eba/2022/SDD.xlsx         | Bin 0 -> 40502 bytes
 data/raw/eba/2022/TR_Metadata.xlsx | Bin 0 -> 146409 bytes
 data/raw/eba/2022/tr_cre.csv.gz    | Bin 0 -> 3418703 bytes
 data/raw/eba/2022/tr_oth.csv.gz    | Bin 0 -> 757545 bytes
 data/raw/eba/2023/SDD.xlsx         | Bin 0 -> 39045 bytes
 data/raw/eba/2023/TR_Metadata.xlsx | Bin 0 -> 143450 bytes
 data/raw/eba/2023/tr_cre.csv.gz    | Bin 0 -> 4349674 bytes
 data/raw/eba/2023/tr_oth.csv.gz    | Bin 0 -> 1004963 bytes
 data/raw/eba/2024/SDD.xlsx         | Bin 0 -> 56448 bytes
 data/raw/eba/2024/TR_Metadata.xlsx | Bin 0 -> 2790861 bytes
 data/raw/eba/2024/tr_cre.csv.gz    | Bin 0 -> 4412159 bytes
 data/raw/eba/2024/tr_oth.csv.gz    | Bin 0 -> 1012171 bytes
 data/raw/eba/2025/SDD.xlsx         | Bin 0 -> 58751 bytes
 data/raw/eba/2025/TR_Metadata.xlsx | Bin 0 -> 2782361 bytes
 data/raw/eba/2025/tr_cre.csv.gz    | Bin 0 -> 5056084 bytes
 data/raw/eba/2025/tr_oth.csv.gz    | Bin 0 -> 1299425 bytes
 decisions/OPEN.md                  | 126 +++++++++++++
 decisions/section_0_review.md      |  62 ++++++
 scripts/build_eba_maps.py          | 304 ++++++++++++++++++++++++++++++
 scripts/pull_data.py               | 223 ++++++++++++++++++++++
 tests/test_eba_raw.py              |  55 ++++++
 38 files changed, 1443 insertions(+), 77 deletions(-)
```

Plus `review/section_1.md` (this file), `decisions/OPEN.md` (OPEN-25) and `instructions/01_section_1.status.md`.

## Reviewer reads

1. `instructions/01_section_1.status.md`
2. `decisions/OPEN.md`, OPEN-17 to OPEN-25
3. This file: Stop evidence: OPEN-25, then 1.2's LEI table and `config/eba_map_2025.csv`
4. `scripts/build_eba_maps.py` (SPEC and OPEN_CANDIDATES tables at the top)
5. `scripts/pull_data.py` (stage `eba`) and `tests/test_eba_raw.py`
