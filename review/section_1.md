# Section 1

Section 1 is complete. Session 1 built steps 1.0 to 1.2 and stopped at step 1.3 (OPEN-25). Session 1b applied the decisions of `instructions/01b_section_1_completion.md` (step 1.2b) and built steps 1.3 to 1.7. This file replaces the stopped version. Its stop evidence is kept under Deviations from PLAN.md.

## Steps completed

- 1.0 apply section 0 review decisions (117db5a)
- 1.1 EBA download, country filter and manifest (5eeb4e2)
- 1.2 EU LEIs from the 2025 release and EBA field maps (e028dab)
- 1.2b apply section 1 review decisions (e43a65d)
- 1.3 EBA ingest, source map and lineage (f7fc13f)
- 1.4 ECB FX pull and conversion (6d9980b)
- 1.5 KPI engine and EU KPI table (31de065)
- 1.6 checks 2 to 6 and 9 on EBA rows (30ce5b6)
- 1.7 mergers (0f8971c)

```
0f8971c step 1.7: mergers and materiality
30ce5b6 step 1.6: checks 2 to 6 and 9 on EBA rows
31de065 step 1.5: KPI engine and EU KPI table
6d9980b step 1.4: ECB FX pull and conversion
f7fc13f step 1.3: EBA ingest, source map and lineage
e43a65d step 1.2b: apply section 1 review decisions
cda78ce Add instructions to finish section 1
fd538b1 section 1: status (stopped at step 1.3)
0c5a655 section 1: review (stopped at step 1.3, OPEN-25)
e028dab step 1.2: EU LEIs from the 2025 release and EBA field maps
5eeb4e2 step 1.1: EBA download, country filter and manifest
117db5a step 1.0: apply section 0 review decisions
```

## Evidence

### 1.0 to 1.2 (session 1, unchanged except where 1.2b says)

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

### 1.2b to 1.6 (session 1b)

The unit rule printed for step 1.3 is instruction 01b B item 9. Every `eba` amount is EUR millions, stored as value × 1e6 with `unit_scale` 1e6 and `ccy` `EUR`, for every bank. Every field with `kind: ratio` (cet1_ratio_reported) is a decimal stored as reported, with `unit_scale` 1 and `ccy` blank. `SDD.xlsx` states no unit (OPEN-25), so the unit comes from that decision, not from the file.

A line labelled `(-) ...` is a deduction the EBA reports negative. `load_eba` stores it positive, which affects intangibles_deduction only.

### 1.2b: new map rows, config/eba_map_2021.csv

```
                    field    item    template                                                                                                                                                                         label                                         dim_filter
                     cet1 2120102     Capital                                                                                  COMMON EQUITY TIER 1 CAPITAL (net of deductions and after applying transitional adjustments)                                                 {}
      cet1_ratio_reported 2120140     Capital                                                                                                                      COMMON EQUITY TIER 1 CAPITAL RATIO (transitional period)                                                 {}
        leverage_exposure 2120903    Leverage                                                                                            Total leverage ratio exposures - using a transitional definition of Tier 1 capital                                                 {}
          debt_securities 2120602         NPE                                                                                        Gross carrying amount on Debt securities (including at amortised cost  and fair value)                                                 {}
    loans_customers_gross 2120605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "102"}
    loans_customers_gross 2120605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "202"}
    loans_customers_gross 2120605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "301"}
    loans_customers_gross 2120605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "401"}
loans_customers_allowance 2120615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "102", "Perf_Status": "1"}
loans_customers_allowance 2120615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "102", "Perf_Status": "2"}
loans_customers_allowance 2120615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "202", "Perf_Status": "1"}
loans_customers_allowance 2120615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "202", "Perf_Status": "2"}
loans_customers_allowance 2120615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "301", "Perf_Status": "1"}
loans_customers_allowance 2120615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "301", "Perf_Status": "2"}
loans_customers_allowance 2120615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "401", "Perf_Status": "1"}
loans_customers_allowance 2120615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "401", "Perf_Status": "2"}
       deposits_customers 2121215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "102", "Financial_instruments": "30"}
       deposits_customers 2121215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "202", "Financial_instruments": "30"}
       deposits_customers 2121215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "301", "Financial_instruments": "30"}
       deposits_customers 2121215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "401", "Financial_instruments": "30"}
```

### 1.2b: new map rows, config/eba_map_2025.csv

```
                    field    item    template                                                                                                                                                                         label                                         dim_filter
                     cet1 2520102     Capital                                                                                  COMMON EQUITY TIER 1 CAPITAL (net of deductions and after applying transitional adjustments)                                                 {}
      cet1_ratio_reported 2520140     Capital                                                                                                                      COMMON EQUITY TIER 1 CAPITAL RATIO (transitional period)                                                 {}
        leverage_exposure 2520903    Leverage                                                                                            Total leverage ratio exposures - using a transitional definition of Tier 1 capital                                                 {}
          debt_securities 2520602         NPE                                                                                        Gross carrying amount on Debt securities (including at amortised cost  and fair value)                                                 {}
    loans_customers_gross 2520605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "102"}
    loans_customers_gross 2520605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "202"}
    loans_customers_gross 2520605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "301"}
    loans_customers_gross 2520605         NPE                                                                       Gross carrying amount on Loans and advances (including at amortised cost  and fair value) - by exposure                                {"Exposure": "401"}
loans_customers_allowance 2520615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "102", "Perf_Status": "1"}
loans_customers_allowance 2520615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "102", "Perf_Status": "2"}
loans_customers_allowance 2520615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "202", "Perf_Status": "1"}
loans_customers_allowance 2520615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "202", "Perf_Status": "2"}
loans_customers_allowance 2520615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "301", "Perf_Status": "1"}
loans_customers_allowance 2520615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "301", "Perf_Status": "2"}
loans_customers_allowance 2520615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "401", "Perf_Status": "1"}
loans_customers_allowance 2520615         NPE Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on Loans and advances (including at amortised cost  and fair value) - by exposure            {"Exposure": "401", "Perf_Status": "2"}
       deposits_customers 2521215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "102", "Financial_instruments": "30"}
       deposits_customers 2521215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "202", "Financial_instruments": "30"}
       deposits_customers 2521215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "301", "Financial_instruments": "30"}
       deposits_customers 2521215 Liabilities                                                                                                             Financial liabilities -  by instrument and by counterparty sector {"Exposure": "401", "Financial_instruments": "30"}
```

Rows of the step 1.2 maps that changed or disappeared in step 1.2b (2025): 0

### 1.2b: DBK

```
bank_id                  lei          name country  market listed ticker price_ccy report_ccy
    DBK 7LTWFZYICNSX8D621K86 Deutsche Bank      DE Germany      1 DBK.DE       EUR        EUR
```

### 1.3: FACTS rows by release and status

```
release status  rows
   2021     ok  3760
   2022     ok  3960
   2023     ok  4080
   2024     ok  4094
   2025     ok  4087
```

### 1.3: FACTS rows by bank and release

```
bank_id  2021  2022  2023  2024  2025
    ABN   160   160   160   160   160
   BAMI   160   160   160   160   160
   BBVA   160   160   160   160   160
    BKT   160   160   160   160   160
   BMPS   160   160   160   160   160
    BNP   160   160   160   160   160
    BPE     0   160   160   160   160
   CABK   160   160   160   160   160
    CAG   160   160   160   160   160
    CBK   160   160   160   160   160
 DANSKE   160   160   160   160   160
    DBK   160   160   160   160   160
    DNB     0    40   160   160   153
    GLE   160   160   160   160   160
   INGA   160   160   160   160   160
    ISP   160   160   160   160   160
    KBC   160   160   160   160   160
    NDA   160   160   160   160   160
   RABO    80    80    80    94    94
    SAB   160   160   160   160   160
    SAN   160   160   160   160   160
    SEB   160   160   160   160   160
    SHB   160   160   160   160   160
   SWED   160   160   160   160   160
    UCG   160   160   160   160   160
    UNI   160   160   160   160   160
```

### 1.3: rejected rows (source map)

```
(none: 0 rows rejected)
```

### 1.3: Intesa Sanpaolo at 2024-12-31, every FACTS row

```
bank_id                  lei   ref_date                         field         value ccy  unit_scale  period_months family      locator   lineage_id status
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31                admin_expenses  1.181997e+10 EUR   1000000.0             12    eba 2520317@2025 b76c4347f68d     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31               at1_instruments  7.551470e+09 EUR   1000000.0           <NA>    eba 2520129@2025 a97293d5717b     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31                       cash_cb  4.759690e+10 EUR   1000000.0           <NA>    eba 2521001@2025 662c7b24bc1a     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31                          cet1  3.930679e+10 EUR   1000000.0           <NA>    eba 2520102@2025 857872582e4e     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31           cet1_ratio_reported  1.326293e-01             1.0           <NA>    eba 2520140@2025 ac444f2b647b     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31               debt_securities  1.431531e+11 EUR   1000000.0           <NA>    eba 2520602@2025 c2eb09c0c919     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31            deposits_customers  4.453134e+11 EUR   1000000.0           <NA>    eba 2521215@2025 ee0abbe2c0cf     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31                  depreciation  1.693318e+09 EUR   1000000.0             12    eba 2520318@2025 13d8a26ab155     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31               dividend_income  2.813025e+08 EUR   1000000.0             12    eba 2520308@2025 89b304da571e     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31          exchange_differences  6.760572e+08 EUR   1000000.0             12    eba 2520314@2025 00a08547b411     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31 gains_derecognition_not_fvtpl  3.351574e+08 EUR   1000000.0             12    eba 2520310@2025 b4ea2ed42514     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31        gains_designated_fvtpl -7.853387e+08 EUR   1000000.0             12    eba 2520312@2025 1063800137fa     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31        gains_hedge_accounting  7.460002e+06 EUR   1000000.0             12    eba 2520313@2025 bfebaf054da7     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31        gains_held_for_trading -1.350834e+08 EUR   1000000.0             12    eba 2520311@2025 40d1ac10c1d1     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31               impairments_fin  1.170441e+09 EUR   1000000.0             12    eba 2520324@2025 169afc571078     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31            impairments_nonfin  8.754692e+07 EUR   1000000.0             12    eba 2520327@2025 8e50c29b35ac     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31         intangibles_deduction  7.529214e+09 EUR   1000000.0           <NA>    eba 2520110@2025 e56ce9488f0a     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31              interest_expense  1.634452e+10 EUR   1000000.0             12    eba 2520304@2025 65e032c48b4e     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31               interest_income  3.204491e+10 EUR   1000000.0             12    eba 2520301@2025 69d2cc3ceba1     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31             leverage_exposure  8.218529e+11 EUR   1000000.0           <NA>    eba 2520903@2025 67d636bd0158     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31                     loans_all  4.541430e+11 EUR   1000000.0           <NA>    eba 2520603@2025 fcc8438abc23     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31     loans_customers_allowance  6.960861e+09 EUR   1000000.0           <NA>    eba 2520615@2025 062cf4fc9440     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31         loans_customers_gross  4.256263e+11 EUR   1000000.0           <NA>    eba 2520605@2025 f4c8f71ea2a0     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31        loans_households_gross  1.785654e+11 EUR   1000000.0           <NA>    eba 2520605@2025 f8635edaa46a     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31                      net_fees  9.445551e+09 EUR   1000000.0             12    eba 2520309@2025 60917b3d5152     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31                 npl_allowance  4.822992e+09 EUR   1000000.0           <NA>    eba 2520613@2025 0aaaf27eeb58     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31                     npl_gross  9.782696e+09 EUR   1000000.0           <NA>    eba 2520603@2025 3731440ce889     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31           other_operating_net  1.098130e+09 EUR   1000000.0             12    eba 2520315@2025 b22e1977c705     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31                           pat  8.683185e+09 EUR   1000000.0             12    eba 2520333@2025 2a655b9ce203     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31                           pbt  1.198158e+10 EUR   1000000.0             12    eba 2520332@2025 24eef8ea3d70     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31                 profit_owners  8.666349e+09 EUR   1000000.0             12    eba 2520336@2025 78db41b3648e     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31                    provisions  6.263838e+08 EUR   1000000.0             12    eba 2520319@2025 d2584e3397ae     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31        resolution_dgs_contrib  3.942406e+08 EUR   1000000.0             12    eba 2520339@2025 b12c443cacab     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31                           rwa  2.963658e+11 EUR   1000000.0           <NA>    eba 2520220@2025 c7d7300e6ff2     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31                         tier1  4.685826e+10 EUR   1000000.0           <NA>    eba 2520133@2025 49ab95d6d5ef     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31                  total_assets  7.592120e+11 EUR   1000000.0           <NA>    eba 2521010@2025 1010f0f40d58     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31                  total_equity  6.531826e+10 EUR   1000000.0           <NA>    eba 2521216@2025 ca3a15901663     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31             total_liabilities  6.938937e+11 EUR   1000000.0           <NA>    eba 2521214@2025 c69704e013c3     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31        total_operating_income  2.662363e+10 EUR   1000000.0             12    eba 2520316@2025 99e30e0c9313     ok
    ISP 2W8N8UU78PMDQKZENC08 2024-12-31                trading_assets  4.146479e+10 EUR   1000000.0           <NA>    eba 2521002@2025 7576990239df     ok
```

### 1.4: FX manifest rows

```
               path   rows first_date  last_date  bytes                                                           sha256
data/raw/fx/DKK.csv 1686.0 2020-01-02 2026-07-31 360956 0e88b5cd7eda62fe6c404781634e58f79e54a10051fa0798f6cfe1110221dfd4
data/raw/fx/GBP.csv 1686.0 2020-01-02 2026-07-31 368943 6854d03c862bc480c73aa62f45290442866b44757cd287895543af96e1f33818
data/raw/fx/NOK.csv 1686.0 2020-01-02 2026-07-31 372132 64fab2602fe09e7f71b9027af5b23e3e81b6d13ab9333660b20579122c16a2e0
data/raw/fx/SEK.csv 1686.0 2020-01-02 2026-07-31 365497 4a8a716c8722d76770f167f3ca9c4f902fed3c1a325edcca0df8bec3f609813f
data/raw/fx/USD.csv 1686.0 2020-01-02 2026-07-31 350826 e74a73fa578f678bf0176eb46f077dacb4fdcda6d91d6f1208d68f4dad1596d7
```

### 1.4: round trip of 1234567.89 (tolerance 1e-9)

```
ccy       date kind          eur  roundtrip_error
GBP 2021-12-31   bs 1.469234e+06              0.0
GBP 2021-12-31   pl 1.436206e+06              0.0
GBP 2023-06-30   bs 1.438421e+06              0.0
GBP 2023-06-30   pl 1.408718e+06              0.0
GBP 2025-12-31   bs 1.414815e+06              0.0
GBP 2025-12-31   pl 1.440918e+06              0.0
SEK 2021-12-31   bs 1.204421e+05              0.0
SEK 2021-12-31   pl 1.216747e+05              0.0
SEK 2023-06-30   bs 1.045757e+05              0.0
SEK 2023-06-30   pl 1.089366e+05              0.0
SEK 2025-12-31   bs 1.140847e+05              0.0
SEK 2025-12-31   pl 1.115610e+05              0.0
NOK 2021-12-31   bs 1.235952e+05              0.0
NOK 2021-12-31   pl 1.214728e+05              0.0
NOK 2023-06-30   bs 1.054826e+05              0.0
NOK 2023-06-30   pl 1.090652e+05              0.0
NOK 2025-12-31   bs 1.042445e+05              0.0
NOK 2025-12-31   pl 1.053629e+05              0.0
DKK 2021-12-31   bs 1.660169e+05              0.0
DKK 2021-12-31   pl 1.660028e+05              0.0
DKK 2023-06-30   bs 1.657717e+05              0.0
DKK 2023-06-30   pl 1.657979e+05              0.0
DKK 2025-12-31   bs 1.652945e+05              0.0
DKK 2025-12-31   pl 1.654164e+05              0.0
USD 2021-12-31   bs 1.090030e+06              0.0
USD 2021-12-31   pl 1.043820e+06              0.0
USD 2023-06-30   bs 1.136175e+06              0.0
USD 2023-06-30   pl 1.142423e+06              0.0
USD 2025-12-31   bs 1.050696e+06              0.0
USD 2025-12-31   pl 1.092554e+06              0.0
```

### 1.6: KPI table, ISP, every date (reported basis; underlying is identical while one_offs.csv is empty)

```
      date            kpi    value    numerator  denominator  unit family             status
2021-12-31           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2021-12-31            roa 0.004957 4.185304e+09 8.442738e+11   bps    eba                 ok
2021-12-31     ppp_assets 0.008811 7.439064e+09 8.442738e+11   bps    eba                 ok
2021-12-31            nim 0.010860 7.906720e+09 7.280735e+11   bps    eba                 ok
2021-12-31      fee_share 0.471913 9.678232e+09 2.050850e+10   pct    eba                 ok
2021-12-31    cost_income 0.637269 1.306943e+10 2.050850e+10   pct    eba                 ok
2021-12-31    cost_assets 0.015480 1.306943e+10 8.442738e+11   bps    eba                 ok
2021-12-31   cost_of_risk 0.006128 2.883517e+09 4.705211e+11   bps    eba                 ok
2021-12-31      npl_ratio 0.030775 1.559643e+10 5.067944e+11   pct    eba                 ok
2021-12-31   npl_coverage 0.529493 8.258201e+09 1.559643e+10   pct    eba                 ok
2021-12-31     cet1_ratio 0.144531 4.724749e+10 3.269028e+11   pct    eba                 ok
2021-12-31 leverage_ratio 0.066427 5.351134e+10 8.055607e+11   pct    eba                 ok
2021-12-31    rwa_density 0.379111 3.269028e+11 8.622885e+11   pct    eba                 ok
2021-12-31   loan_deposit 1.001297 4.607277e+11 4.601309e+11   pct    eba                 ok
2021-12-31            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2021-12-31           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2021-12-31     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2021-12-31       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2021-12-31  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2022-06-30           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2022-06-30            roa 0.004129 3.515871e+09 8.514443e+11   bps    eba                 ok
2022-06-30     ppp_assets 0.008668 7.380276e+09 8.514443e+11   bps    eba                 ok
2022-06-30            nim 0.010687 7.958678e+09 7.447138e+11   bps    eba                 ok
2022-06-30      fee_share 0.467445 9.480657e+09 2.028187e+10   pct    eba                 ok
2022-06-30    cost_income 0.636115 1.290160e+10 2.028187e+10   pct    eba                 ok
2022-06-30    cost_assets 0.015153 1.290160e+10 8.514443e+11   bps    eba                 ok
2022-06-30   cost_of_risk 0.006537 3.093275e+09 4.731892e+11   bps    eba                 ok
2022-06-30      npl_ratio 0.022753 1.149821e+10 5.053482e+11   pct    eba                 ok
2022-06-30   npl_coverage 0.443849 5.103465e+09 1.149821e+10   pct    eba                 ok
2022-06-30     cet1_ratio 0.127008 4.132109e+10 3.253412e+11   pct    eba                 ok
2022-06-30 leverage_ratio 0.052922 4.852801e+10 9.169772e+11   pct    eba                 ok
2022-06-30    rwa_density 0.382309 3.253412e+11 8.509901e+11   pct    eba                 ok
2022-06-30   loan_deposit 1.010475 4.676054e+11 4.627582e+11   pct    eba                 ok
2022-06-30            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2022-06-30           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2022-06-30     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2022-06-30       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2022-06-30  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2022-12-31           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2022-12-31            roa 0.005231 4.354486e+09 8.323741e+11   bps    eba                 ok
2022-12-31     ppp_assets 0.009303 7.743714e+09 8.323741e+11   bps    eba                 ok
2022-12-31            nim 0.013131 9.585144e+09 7.299789e+11   bps    eba                 ok
2022-12-31      fee_share 0.437406 8.969001e+09 2.050500e+10   pct    eba                 ok
2022-12-31    cost_income 0.622350 1.276129e+10 2.050500e+10   pct    eba                 ok
2022-12-31    cost_assets 0.015331 1.276129e+10 8.323741e+11   bps    eba                 ok
2022-12-31   cost_of_risk 0.005851 2.702991e+09 4.619563e+11   bps    eba                 ok
2022-12-31      npl_ratio 0.023057 1.103163e+10 4.784489e+11   pct    eba                 ok
2022-12-31   npl_coverage 0.481574 5.312541e+09 1.103163e+10   pct    eba                 ok
2022-12-31     cet1_ratio 0.138004 4.077234e+10 2.954429e+11   pct    eba                 ok
2022-12-31 leverage_ratio 0.056098 4.797923e+10 8.552823e+11   pct    eba                 ok
2022-12-31    rwa_density 0.368172 2.954429e+11 8.024596e+11   pct    eba                 ok
2022-12-31   loan_deposit 0.974198 4.445647e+11 4.563393e+11   pct    eba                 ok
2022-12-31            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2022-12-31           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2022-12-31     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2022-12-31       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2022-12-31  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2023-06-30           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2023-06-30            roa 0.007621 6.222282e+09 8.164755e+11   bps    eba                 ok
2023-06-30     ppp_assets 0.011695 9.548499e+09 8.164755e+11   bps    eba                 ok
2023-06-30            nim 0.017483 1.240227e+10 7.093719e+11   bps    eba                 ok
2023-06-30      fee_share 0.389409 8.735186e+09 2.243192e+10   pct    eba                 ok
2023-06-30    cost_income 0.574334 1.288342e+10 2.243192e+10   pct    eba                 ok
2023-06-30    cost_assets 0.015779 1.288342e+10 8.164755e+11   bps    eba                 ok
2023-06-30   cost_of_risk 0.004616 2.118066e+09 4.589024e+11   bps    eba                 ok
2023-06-30      npl_ratio 0.022478 1.049209e+10 4.667780e+11   pct    eba                 ok
2023-06-30   npl_coverage 0.486831 5.107876e+09 1.049209e+10   pct    eba                 ok
2023-06-30     cet1_ratio 0.137312 4.061504e+10 2.957863e+11   pct    eba                 ok
2023-06-30 leverage_ratio 0.057032 4.782193e+10 8.385094e+11   pct    eba                 ok
2023-06-30    rwa_density 0.378262 2.957863e+11 7.819610e+11   pct    eba                 ok
2023-06-30   loan_deposit 0.989089 4.348213e+11 4.396181e+11   pct    eba                 ok
2023-06-30            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2023-06-30           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2023-06-30     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2023-06-30       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2023-06-30  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2023-12-31           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2023-12-31            roa 0.009691 7.723947e+09 7.969817e+11   bps    eba                 ok
2023-12-31     ppp_assets 0.014043 1.119190e+10 7.969817e+11   bps    eba                 ok
2023-12-31            nim 0.021220 1.468392e+10 6.919776e+11   bps    eba                 ok
2023-12-31      fee_share 0.349373 8.579855e+09 2.455788e+10   pct    eba                 ok
2023-12-31    cost_income 0.544264 1.336597e+10 2.455788e+10   pct    eba                 ok
2023-12-31    cost_assets 0.016771 1.336597e+10 7.969817e+11   bps    eba                 ok
2023-12-31   cost_of_risk 0.003105 1.376983e+09 4.434514e+11   bps    eba                 ok
2023-12-31      npl_ratio 0.021830 9.999775e+09 4.580687e+11   pct    eba                 ok
2023-12-31   npl_coverage 0.495971 4.959602e+09 9.999775e+09   pct    eba                 ok
2023-12-31     cet1_ratio 0.137289 4.147636e+10 3.021096e+11   pct    eba                 ok
2023-12-31 leverage_ratio 0.057814 4.918342e+10 8.507181e+11   pct    eba                 ok
2023-12-31    rwa_density 0.381691 3.021096e+11 7.915037e+11   pct    eba                 ok
2023-12-31   loan_deposit 0.966197 4.270423e+11 4.419824e+11   pct    eba                 ok
2023-12-31            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2023-12-31           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2023-12-31     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2023-12-31       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2023-12-31  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2024-06-30           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2024-06-30            roa 0.010686 8.267798e+09 7.737029e+11   bps    eba                 ok
2024-06-30     ppp_assets 0.015471 1.196977e+10 7.737029e+11   bps    eba                 ok
2024-06-30            nim 0.023715 1.576777e+10 6.648880e+11   bps    eba                 ok
2024-06-30      fee_share 0.349067 8.895097e+09 2.548246e+10   pct    eba                 ok
2024-06-30    cost_income 0.530274 1.351270e+10 2.548246e+10   pct    eba                 ok
2024-06-30    cost_assets 0.017465 1.351270e+10 7.737029e+11   bps    eba                 ok
2024-06-30   cost_of_risk 0.002918 1.266434e+09 4.340519e+11   bps    eba                 ok
2024-06-30      npl_ratio 0.021548 9.735822e+09 4.518252e+11   pct    eba                 ok
2024-06-30   npl_coverage 0.505483 4.921295e+09 9.735822e+09   pct    eba                 ok
2024-06-30     cet1_ratio 0.135496 4.050287e+10 2.989230e+11   pct    eba                 ok
2024-06-30 leverage_ratio 0.059483 4.920427e+10 8.271937e+11   pct    eba                 ok
2024-06-30    rwa_density 0.390522 2.989230e+11 7.654447e+11   pct    eba                 ok
2024-06-30   loan_deposit 0.936294 4.185513e+11 4.470298e+11   pct    eba                 ok
2024-06-30            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2024-06-30           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2024-06-30     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2024-06-30       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2024-06-30  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2024-12-31           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2024-12-31            roa 0.011177 8.666349e+09 7.753578e+11   bps    eba                 ok
2024-12-31     ppp_assets 0.016400 1.271610e+10 7.753578e+11   bps    eba                 ok
2024-12-31            nim 0.023615 1.570039e+10 6.648346e+11   bps    eba                 ok
2024-12-31      fee_share 0.354781 9.445551e+09 2.662363e+10   pct    eba                 ok
2024-12-31    cost_income 0.522375 1.390753e+10 2.662363e+10   pct    eba                 ok
2024-12-31    cost_assets 0.017937 1.390753e+10 7.753578e+11   bps    eba                 ok
2024-12-31   cost_of_risk 0.002722 1.170441e+09 4.300283e+11   bps    eba                 ok
2024-12-31      npl_ratio 0.021541 9.782696e+09 4.541430e+11   pct    eba                 ok
2024-12-31   npl_coverage 0.493013 4.822992e+09 9.782696e+09   pct    eba                 ok
2024-12-31     cet1_ratio 0.132629 3.930679e+10 2.963658e+11   pct    eba                 ok
2024-12-31 leverage_ratio 0.057015 4.685826e+10 8.218529e+11   pct    eba                 ok
2024-12-31    rwa_density 0.390360 2.963658e+11 7.592120e+11   pct    eba                 ok
2024-12-31   loan_deposit 0.940159 4.186654e+11 4.453134e+11   pct    eba                 ok
2024-12-31            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2024-12-31           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2024-12-31     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2024-12-31       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2024-12-31  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2025-06-30           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2025-06-30            roa 0.011872 9.117185e+09 7.679816e+11   bps    eba                 ok
2025-06-30     ppp_assets 0.017321 1.330186e+10 7.679816e+11   bps    eba                 ok
2025-06-30            nim 0.023196 1.522854e+10 6.565065e+11   bps    eba                 ok
2025-06-30      fee_share 0.357156 9.638949e+09 2.698804e+10   pct    eba                 ok
2025-06-30    cost_income 0.507120 1.368617e+10 2.698804e+10   pct    eba                 ok
2025-06-30    cost_assets 0.017821 1.368617e+10 7.679816e+11   bps    eba                 ok
2025-06-30   cost_of_risk 0.002779 1.176057e+09 4.231346e+11   bps    eba                 ok
2025-06-30      npl_ratio 0.022027 9.902829e+09 4.495866e+11   pct    eba                 ok
2025-06-30   npl_coverage 0.499884 4.950265e+09 9.902829e+09   pct    eba                 ok
2025-06-30     cet1_ratio 0.129715 4.001800e+10 3.085076e+11   pct    eba                 ok
2025-06-30 leverage_ratio 0.057888 4.768556e+10 8.237507e+11   pct    eba                 ok
2025-06-30    rwa_density 0.400390 3.085076e+11 7.705184e+11   pct    eba                 ok
2025-06-30   loan_deposit 0.945458 4.135395e+11 4.373961e+11   pct    eba                 ok
2025-06-30            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2025-06-30           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2025-06-30     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2025-06-30       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2025-06-30  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
```

### 1.6: KPI table, SWED, every date (reported basis; underlying is identical while one_offs.csv is empty)

```
      date            kpi    value    numerator  denominator  unit family             status
2021-12-31           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2021-12-31            roa 0.008666 2.036134e+09 2.349499e+11   bps    eba                 ok
2021-12-31     ppp_assets 0.009995 2.348369e+09 2.349499e+11   bps    eba                 ok
2021-12-31            nim 0.013133 2.857259e+09 2.175650e+11   bps    eba                 ok
2021-12-31      fee_share 0.301280 1.361138e+09 4.517858e+09   pct    eba                 ok
2021-12-31    cost_income 0.480203 2.169489e+09 4.517858e+09   pct    eba                 ok
2021-12-31    cost_assets 0.009234 2.169489e+09 2.349499e+11   bps    eba                 ok
2021-12-31   cost_of_risk 0.000508 8.498044e+07 1.672259e+11   bps    eba                 ok
2021-12-31      npl_ratio 0.004883 8.237292e+08 1.687062e+11   pct    eba                 ok
2021-12-31   npl_coverage 0.410489 3.381316e+08 8.237292e+08   pct    eba                 ok
2021-12-31     cet1_ratio 0.183177 1.264785e+10 6.904703e+10   pct    eba                 ok
2021-12-31 leverage_ratio 0.054450 1.395293e+10 2.562502e+11   pct    eba                 ok
2021-12-31    rwa_density 0.292066 6.904703e+10 2.364091e+11   pct    eba                 ok
2021-12-31   loan_deposit 1.341041 1.666106e+11 1.242397e+11   pct    eba                 ok
2021-12-31            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2021-12-31           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2021-12-31     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2021-12-31       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2021-12-31  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2022-06-30           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2022-06-30            roa 0.007352 1.863293e+09 2.534445e+11   bps    eba                 ok
2022-06-30     ppp_assets 0.008520 2.159340e+09 2.534445e+11   bps    eba                 ok
2022-06-30            nim 0.012184 2.850582e+09 2.339704e+11   bps    eba                 ok
2022-06-30      fee_share 0.306906 1.341571e+09 4.371283e+09   pct    eba                 ok
2022-06-30    cost_income 0.506017 2.211943e+09 4.371283e+09   pct    eba                 ok
2022-06-30    cost_assets 0.008728 2.211943e+09 2.534445e+11   bps    eba                 ok
2022-06-30   cost_of_risk 0.000395 6.657240e+07 1.686509e+11   bps    eba                 ok
2022-06-30      npl_ratio 0.004290 7.428586e+08 1.731795e+11   pct    eba                 ok
2022-06-30   npl_coverage 0.392792 2.917886e+08 7.428586e+08   pct    eba                 ok
2022-06-30     cet1_ratio 0.182776 1.266940e+10 6.931663e+10   pct    eba                 ok
2022-06-30 leverage_ratio 0.051961 1.354256e+10 2.606276e+11   pct    eba                 ok
2022-06-30    rwa_density 0.282538 6.931663e+10 2.453352e+11   pct    eba                 ok
2022-06-30   loan_deposit 1.391407 1.701743e+11 1.223038e+11   pct    eba                 ok
2022-06-30            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2022-06-30           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2022-06-30     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2022-06-30       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2022-06-30  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2022-12-31           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2022-12-31            roa 0.008426 1.967061e+09 2.334635e+11   bps    eba                 ok
2022-12-31     ppp_assets 0.010854 2.534070e+09 2.334635e+11   bps    eba                 ok
2022-12-31            nim 0.014818 3.242126e+09 2.187961e+11   bps    eba                 ok
2022-12-31      fee_share 0.259944 1.218575e+09 4.687831e+09   pct    eba                 ok
2022-12-31    cost_income 0.459437 2.153761e+09 4.687831e+09   pct    eba                 ok
2022-12-31    cost_assets 0.009225 2.153761e+09 2.334635e+11   bps    eba                 ok
2022-12-31   cost_of_risk 0.001017 1.701841e+08 1.672582e+11   bps    eba                 ok
2022-12-31      npl_ratio 0.004018 6.788395e+08 1.689397e+11   pct    eba                 ok
2022-12-31   npl_coverage 0.417214 2.832213e+08 6.788395e+08   pct    eba                 ok
2022-12-31     cet1_ratio 0.178034 1.295719e+10 7.277945e+10   pct    eba                 ok
2022-12-31 leverage_ratio 0.056058 1.378558e+10 2.459151e+11   pct    eba                 ok
2022-12-31    rwa_density 0.315722 7.277945e+10 2.305179e+11   pct    eba                 ok
2022-12-31   loan_deposit 1.402162 1.665929e+11 1.188115e+11   pct    eba                 ok
2022-12-31            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2022-12-31           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2022-12-31     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2022-12-31       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2022-12-31  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2023-06-30           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2023-06-30            roa 0.010568 2.510987e+09 2.376066e+11   bps    eba                 ok
2023-06-30     ppp_assets 0.013775 3.272929e+09 2.376066e+11   bps    eba                 ok
2023-06-30            nim 0.017924 3.943986e+09 2.200359e+11   bps    eba                 ok
2023-06-30      fee_share 0.219057 1.197375e+09 5.466050e+09   pct    eba                 ok
2023-06-30    cost_income 0.401226 2.193121e+09 5.466050e+09   pct    eba                 ok
2023-06-30    cost_assets 0.009230 2.193121e+09 2.376066e+11   bps    eba                 ok
2023-06-30   cost_of_risk 0.001420 2.327678e+08 1.639672e+11   bps    eba                 ok
2023-06-30      npl_ratio 0.004303 6.885811e+08 1.600130e+11   pct    eba                 ok
2023-06-30   npl_coverage 0.398332 2.742839e+08 6.885811e+08   pct    eba                 ok
2023-06-30     cet1_ratio 0.186211 1.291865e+10 6.937623e+10   pct    eba                 ok
2023-06-30 leverage_ratio 0.057880 1.418341e+10 2.450498e+11   pct    eba                 ok
2023-06-30    rwa_density 0.301796 6.937623e+10 2.298780e+11   pct    eba                 ok
2023-06-30   loan_deposit 1.405967 1.564347e+11 1.112648e+11   pct    eba                 ok
2023-06-30            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2023-06-30           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2023-06-30     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2023-06-30       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2023-06-30  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2023-12-31           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2023-12-31            roa 0.013460 3.075710e+09 2.285074e+11   bps    eba                 ok
2023-12-31     ppp_assets 0.016839 3.847940e+09 2.285074e+11   bps    eba                 ok
2023-12-31            nim 0.021928 4.643859e+09 2.117795e+11   bps    eba                 ok
2023-12-31      fee_share 0.205356 1.312045e+09 6.389134e+09   pct    eba                 ok
2023-12-31    cost_income 0.397737 2.541194e+09 6.389134e+09   pct    eba                 ok
2023-12-31    cost_assets 0.011121 2.541194e+09 2.285074e+11   bps    eba                 ok
2023-12-31   cost_of_risk 0.001089 1.815930e+08 1.667921e+11   bps    eba                 ok
2023-12-31      npl_ratio 0.005182 8.650142e+08 1.669337e+11   pct    eba                 ok
2023-12-31   npl_coverage 0.317051 2.742536e+08 8.650142e+08   pct    eba                 ok
2023-12-31     cet1_ratio 0.189653 1.447903e+10 7.634472e+10   pct    eba                 ok
2023-12-31 leverage_ratio 0.065016 1.575771e+10 2.423673e+11   pct    eba                 ok
2023-12-31    rwa_density 0.337067 7.634472e+10 2.264969e+11   pct    eba                 ok
2023-12-31   loan_deposit 1.473426 1.655271e+11 1.123416e+11   pct    eba                 ok
2023-12-31            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2023-12-31           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2023-12-31     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2023-12-31       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2023-12-31  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2024-06-30           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2024-06-30            roa 0.013604 3.161036e+09 2.323655e+11   bps    eba                 ok
2024-06-30     ppp_assets 0.016660 3.871218e+09 2.323655e+11   bps    eba                 ok
2024-06-30            nim 0.021833 4.621393e+09 2.116655e+11   bps    eba                 ok
2024-06-30      fee_share 0.209798 1.395541e+09 6.651831e+09   pct    eba                 ok
2024-06-30    cost_income 0.418022 2.780614e+09 6.651831e+09   pct    eba                 ok
2024-06-30    cost_assets 0.011967 2.780614e+09 2.323655e+11   bps    eba                 ok
2024-06-30   cost_of_risk 0.000623 9.980212e+07 1.601322e+11   bps    eba                 ok
2024-06-30      npl_ratio 0.006279 1.028149e+09 1.637465e+11   pct    eba                 ok
2024-06-30   npl_coverage 0.270190 2.777959e+08 1.028149e+09   pct    eba                 ok
2024-06-30     cet1_ratio 0.201092 1.501039e+10 7.464432e+10   pct    eba                 ok
2024-06-30 leverage_ratio 0.066887 1.692584e+10 2.530516e+11   pct    eba                 ok
2024-06-30    rwa_density 0.317834 7.464432e+10 2.348529e+11   pct    eba                 ok
2024-06-30   loan_deposit 1.415426 1.623800e+11 1.147216e+11   pct    eba                 ok
2024-06-30            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2024-06-30           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2024-06-30     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2024-06-30       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2024-06-30  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2024-12-31           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2024-12-31            roa 0.013446 3.042972e+09 2.263111e+11   bps    eba                 ok
2024-12-31     ppp_assets 0.016132 3.650876e+09 2.263111e+11   bps    eba                 ok
2024-12-31            nim 0.020976 4.301294e+09 2.050536e+11   bps    eba                 ok
2024-12-31      fee_share 0.221842 1.408212e+09 6.347820e+09   pct    eba                 ok
2024-12-31    cost_income 0.424861 2.696944e+09 6.347820e+09   pct    eba                 ok
2024-12-31    cost_assets 0.011917 2.696944e+09 2.263111e+11   bps    eba                 ok
2024-12-31   cost_of_risk 0.000228 3.713387e+07 1.628980e+11   bps    eba                 ok
2024-12-31      npl_ratio 0.007638 1.225455e+09 1.604432e+11   pct    eba                 ok
2024-12-31   npl_coverage 0.251626 3.083561e+08 1.225455e+09   pct    eba                 ok
2024-12-31     cet1_ratio 0.197981 1.506415e+10 7.608886e+10   pct    eba                 ok
2024-12-31 leverage_ratio 0.068011 1.656423e+10 2.435512e+11   pct    eba                 ok
2024-12-31    rwa_density 0.336490 7.608886e+10 2.261253e+11   pct    eba                 ok
2024-12-31   loan_deposit 1.404669 1.587961e+11 1.130487e+11   pct    eba                 ok
2024-12-31            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2024-12-31           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2024-12-31     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2024-12-31       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2024-12-31  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2025-06-30           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2025-06-30            roa 0.012495 2.987766e+09 2.391236e+11   bps    eba                 ok
2025-06-30     ppp_assets 0.014941 3.572862e+09 2.391236e+11   bps    eba                 ok
2025-06-30            nim 0.020594 4.355012e+09 2.114737e+11   bps    eba                 ok
2025-06-30      fee_share 0.226032 1.405261e+09 6.217089e+09   pct    eba                 ok
2025-06-30    cost_income 0.425316 2.644226e+09 6.217089e+09   pct    eba                 ok
2025-06-30    cost_assets 0.011058 2.644226e+09 2.391236e+11   bps    eba                 ok
2025-06-30   cost_of_risk 0.000351 5.771199e+07 1.642643e+11   bps    eba                 ok
2025-06-30      npl_ratio 0.006842 1.160160e+09 1.695585e+11   pct    eba                 ok
2025-06-30   npl_coverage 0.291169 3.378024e+08 1.160160e+09   pct    eba                 ok
2025-06-30     cet1_ratio 0.197044 1.570728e+10 7.971472e+10   pct    eba                 ok
2025-06-30 leverage_ratio 0.066812 1.710479e+10 2.560123e+11   pct    eba                 ok
2025-06-30    rwa_density 0.327513 7.971472e+10 2.433942e+11   pct    eba                 ok
2025-06-30   loan_deposit 1.359582 1.647259e+11 1.211592e+11   pct    eba                 ok
2025-06-30            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2025-06-30           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2025-06-30     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2025-06-30       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2025-06-30  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
```

### 1.6: KPI table, BBVA, every date (reported basis; underlying is identical while one_offs.csv is empty)

```
      date            kpi    value    numerator  denominator  unit family             status
2021-12-31           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2021-12-31            roa 0.006779 4.601021e+09 6.786807e+11   bps    eba                 ok
2021-12-31     ppp_assets 0.015604 1.059029e+10 6.786807e+11   bps    eba                 ok
2021-12-31            nim 0.029132 1.435981e+10 4.929181e+11   bps    eba                 ok
2021-12-31      fee_share 0.243065 5.054303e+09 2.079404e+10   pct    eba                 ok
2021-12-31    cost_income 0.490706 1.020376e+10 2.079404e+10   pct    eba                 ok
2021-12-31    cost_assets 0.015035 1.020376e+10 6.786807e+11   bps    eba                 ok
2021-12-31   cost_of_risk 0.009341 3.050655e+09 3.265961e+11   bps    eba                 ok
2021-12-31      npl_ratio 0.041998 1.467139e+10 3.493315e+11   pct    eba                 ok
2021-12-31   npl_coverage 0.481393 7.062696e+09 1.467139e+10   pct    eba                 ok
2021-12-31     cet1_ratio 0.129791 3.994893e+10 3.077951e+11   pct    eba                 ok
2021-12-31 leverage_ratio 0.068007 4.568652e+10 6.717894e+11   pct    eba                 ok
2021-12-31    rwa_density 0.479797 3.077951e+11 6.415117e+11   pct    eba                 ok
2021-12-31   loan_deposit 0.879396 3.187089e+11 3.624177e+11   pct    eba                 ok
2021-12-31            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2021-12-31           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2021-12-31     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2021-12-31       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2021-12-31  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2022-06-30           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2022-06-30            roa 0.008626 5.691751e+09 6.598441e+11   bps    eba                 ok
2022-06-30     ppp_assets 0.016959 1.119043e+10 6.598441e+11   bps    eba                 ok
2022-06-30            nim 0.030703 1.592158e+10 5.185634e+11   bps    eba                 ok
2022-06-30      fee_share 0.247289 5.419243e+09 2.191462e+10   pct    eba                 ok
2022-06-30    cost_income 0.489362 1.072418e+10 2.191462e+10   pct    eba                 ok
2022-06-30    cost_assets 0.016253 1.072418e+10 6.598441e+11   bps    eba                 ok
2022-06-30   cost_of_risk 0.008440 2.905105e+09 3.442008e+11   bps    eba                 ok
2022-06-30      npl_ratio 0.038286 1.459987e+10 3.813396e+11   pct    eba                 ok
2022-06-30   npl_coverage 0.519434 7.583668e+09 1.459987e+10   pct    eba                 ok
2022-06-30     cet1_ratio 0.125617 4.156322e+10 3.308714e+11   pct    eba                 ok
2022-06-30 leverage_ratio 0.062269 4.682761e+10 7.520159e+11   pct    eba                 ok
2022-06-30    rwa_density 0.477752 3.308714e+11 6.925593e+11   pct    eba                 ok
2022-06-30   loan_deposit 0.911653 3.492026e+11 3.830433e+11   pct    eba                 ok
2022-06-30            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2022-06-30           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2022-06-30     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2022-06-30       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2022-06-30  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2022-12-31           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2022-12-31            roa 0.009631 6.407124e+09 6.652315e+11   bps    eba                 ok
2022-12-31     ppp_assets 0.019370 1.288562e+10 6.652315e+11   bps    eba                 ok
2022-12-31            nim 0.035992 1.873760e+10 5.206016e+11   bps    eba                 ok
2022-12-31      fee_share 0.233056 5.695720e+09 2.443932e+10   pct    eba                 ok
2022-12-31    cost_income 0.472750 1.155369e+10 2.443932e+10   pct    eba                 ok
2022-12-31    cost_assets 0.017368 1.155369e+10 6.652315e+11   bps    eba                 ok
2022-12-31   cost_of_risk 0.009704 3.387812e+09 3.491259e+11   bps    eba                 ok
2022-12-31      npl_ratio 0.034699 1.349684e+10 3.889710e+11   pct    eba                 ok
2022-12-31   npl_coverage 0.539785 7.285401e+09 1.349684e+10   pct    eba                 ok
2022-12-31     cet1_ratio 0.126795 4.273845e+10 3.370663e+11   pct    eba                 ok
2022-12-31 leverage_ratio 0.064948 4.793123e+10 7.379904e+11   pct    eba                 ok
2022-12-31    rwa_density 0.489245 3.370663e+11 6.889512e+11   pct    eba                 ok
2022-12-31   loan_deposit 0.890584 3.571577e+11 4.010378e+11   pct    eba                 ok
2022-12-31            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2022-12-31           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2022-12-31     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2022-12-31       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2022-12-31  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2023-06-30           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2023-06-30            roa 0.010213 7.296243e+09 7.144341e+11   bps    eba                 ok
2023-06-30     ppp_assets 0.020458 1.461586e+10 7.144341e+11   bps    eba                 ok
2023-06-30            nim 0.038896 2.155430e+10 5.541511e+11   bps    eba                 ok
2023-06-30      fee_share 0.219297 5.928436e+09 2.703384e+10   pct    eba                 ok
2023-06-30    cost_income 0.459350 1.241798e+10 2.703384e+10   pct    eba                 ok
2023-06-30    cost_assets 0.017382 1.241798e+10 7.144341e+11   bps    eba                 ok
2023-06-30   cost_of_risk 0.010641 3.948182e+09 3.710431e+11   bps    eba                 ok
2023-06-30      npl_ratio 0.034026 1.379206e+10 4.053429e+11   pct    eba                 ok
2023-06-30   npl_coverage 0.515262 7.106519e+09 1.379206e+10   pct    eba                 ok
2023-06-30     cet1_ratio 0.129937 4.514558e+10 3.474421e+11   pct    eba                 ok
2023-06-30 leverage_ratio 0.064789 5.131617e+10 7.920451e+11   pct    eba                 ok
2023-06-30    rwa_density 0.471870 3.474421e+11 7.363088e+11   pct    eba                 ok
2023-06-30   loan_deposit 0.895557 3.699567e+11 4.131023e+11   pct    eba                 ok
2023-06-30            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2023-06-30           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2023-06-30     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2023-06-30       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2023-06-30  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2023-12-31           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2023-12-31            roa 0.011116 7.987717e+09 7.185977e+11   bps    eba                 ok
2023-12-31     ppp_assets 0.021819 1.567934e+10 7.185977e+11   bps    eba                 ok
2023-12-31            nim 0.040112 2.262674e+10 5.640851e+11   bps    eba                 ok
2023-12-31      fee_share 0.227423 6.559897e+09 2.884442e+10   pct    eba                 ok
2023-12-31    cost_income 0.456417 1.316508e+10 2.884442e+10   pct    eba                 ok
2023-12-31    cost_assets 0.018321 1.316508e+10 7.185977e+11   bps    eba                 ok
2023-12-31   cost_of_risk 0.011739 4.448042e+09 3.789052e+11   bps    eba                 ok
2023-12-31      npl_ratio 0.034976 1.445216e+10 4.132059e+11   pct    eba                 ok
2023-12-31   npl_coverage 0.495519 7.161320e+09 1.445216e+10   pct    eba                 ok
2023-12-31     cet1_ratio 0.126723 4.611628e+10 3.639154e+11   pct    eba                 ok
2023-12-31 leverage_ratio 0.065360 5.214973e+10 7.978877e+11   pct    eba                 ok
2023-12-31    rwa_density 0.486359 3.639154e+11 7.482442e+11   pct    eba                 ok
2023-12-31   loan_deposit 0.874635 3.780860e+11 4.322789e+11   pct    eba                 ok
2023-12-31            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2023-12-31           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2023-12-31     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2023-12-31       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2023-12-31  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2024-06-30           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2024-06-30            roa 0.012408 9.107740e+09 7.340436e+11   bps    eba                 ok
2024-06-30     ppp_assets 0.024372 1.789002e+10 7.340436e+11   bps    eba                 ok
2024-06-30            nim 0.042403 2.422354e+10 5.712736e+11   bps    eba                 ok
2024-06-30      fee_share 0.236025 7.510812e+09 3.182210e+10   pct    eba                 ok
2024-06-30    cost_income 0.437811 1.393208e+10 3.182210e+10   pct    eba                 ok
2024-06-30    cost_assets 0.018980 1.393208e+10 7.340436e+11   bps    eba                 ok
2024-06-30   cost_of_risk 0.013489 5.306127e+09 3.933696e+11   bps    eba                 ok
2024-06-30      npl_ratio 0.033830 1.468173e+10 4.339869e+11   pct    eba                 ok
2024-06-30   npl_coverage 0.493802 7.249868e+09 1.468173e+10   pct    eba                 ok
2024-06-30     cet1_ratio 0.127514 4.886045e+10 3.831787e+11   pct    eba                 ok
2024-06-30 leverage_ratio 0.067703 5.477625e+10 8.090635e+11   pct    eba                 ok
2024-06-30    rwa_density 0.523627 3.831787e+11 7.317785e+11   pct    eba                 ok
2024-06-30   loan_deposit 0.876128 3.943029e+11 4.500517e+11   pct    eba                 ok
2024-06-30            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2024-06-30           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2024-06-30     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2024-06-30       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2024-06-30  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2024-12-31           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2024-12-31            roa 0.013456 1.004035e+10 7.461712e+11   bps    eba                 ok
2024-12-31     ppp_assets 0.026362 1.967046e+10 7.461712e+11   bps    eba                 ok
2024-12-31            nim 0.041789 2.467433e+10 5.904573e+11   bps    eba                 ok
2024-12-31      fee_share 0.241766 8.300865e+09 3.433425e+10   pct    eba                 ok
2024-12-31    cost_income 0.427089 1.466379e+10 3.433425e+10   pct    eba                 ok
2024-12-31    cost_assets 0.019652 1.466379e+10 7.461712e+11   bps    eba                 ok
2024-12-31   cost_of_risk 0.014206 5.779394e+09 4.068284e+11   bps    eba                 ok
2024-12-31      npl_ratio 0.031251 1.421658e+10 4.549114e+11   pct    eba                 ok
2024-12-31   npl_coverage 0.519007 7.378512e+09 1.421658e+10   pct    eba                 ok
2024-12-31     cet1_ratio 0.128779 5.079901e+10 3.944679e+11   pct    eba                 ok
2024-12-31 leverage_ratio 0.068092 5.682230e+10 8.344883e+11   pct    eba                 ok
2024-12-31    rwa_density 0.530129 3.944679e+11 7.440982e+11   pct    eba                 ok
2024-12-31   loan_deposit 0.892012 4.126040e+11 4.625544e+11   pct    eba                 ok
2024-12-31            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2024-12-31           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2024-12-31     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2024-12-31       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2024-12-31  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
2025-06-30           rote      NaN          NaN          NaN   pct    NaN  pending_section_3
2025-06-30            roa 0.014182 1.048573e+10 7.393666e+11   bps    eba                 ok
2025-06-30     ppp_assets 0.027510 2.033993e+10 7.393666e+11   bps    eba                 ok
2025-06-30            nim 0.040764 2.422019e+10 5.941629e+11   bps    eba                 ok
2025-06-30      fee_share 0.242576 8.477726e+09 3.494871e+10   pct    eba                 ok
2025-06-30    cost_income 0.418006 1.460878e+10 3.494871e+10   pct    eba                 ok
2025-06-30    cost_assets 0.019759 1.460878e+10 7.393666e+11   bps    eba                 ok
2025-06-30   cost_of_risk 0.013494 5.694388e+09 4.219959e+11   bps    eba                 ok
2025-06-30      npl_ratio 0.029976 1.413625e+10 4.715868e+11   pct    eba                 ok
2025-06-30   npl_coverage 0.525571 7.429600e+09 1.413625e+10   pct    eba                 ok
2025-06-30     cet1_ratio 0.133403 5.163361e+10 3.870507e+11   pct    eba                 ok
2025-06-30 leverage_ratio 0.069259 5.712264e+10 8.247687e+11   pct    eba                 ok
2025-06-30    rwa_density 0.518172 3.870507e+11 7.469548e+11   pct    eba                 ok
2025-06-30   loan_deposit 0.923630 4.267589e+11 4.620453e+11   pct    eba                 ok
2025-06-30            lcr      NaN          NaN          NaN   pct    NaN  missing_input:lcr
2025-06-30           nsfr      NaN          NaN          NaN   pct    NaN missing_input:nsfr
2025-06-30     income_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2025-06-30       cost_fte      NaN          NaN          NaN eur_k    NaN  pending_section_3
2025-06-30  cost_customer      NaN          NaN          NaN   eur    NaN  pending_section_3
```

### 1.6: KPI rows by bank and status (both bases)

```
bank_id  missing_input:cet1  missing_input:iea  missing_input:impairments_fin  missing_input:lcr  missing_input:loans_customers_gross  missing_input:loans_customers_net  missing_input:net_fees  missing_input:nii  missing_input:npl_allowance  missing_input:npl_gross  missing_input:nsfr  missing_input:opex  missing_input:ppp  missing_input:profit_owners  missing_input:rwa  missing_input:tier1  missing_input:total_assets  ok  pending_section_3
    ABN                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
   BAMI                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
   BBVA                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
    BKT                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
   BMPS                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
    BNP                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
    BPE                   0                  2                              2                 16                                    2                                  0                       2                  2                            0                        0                  16                   4                  2                            2                  0                    0                           6 184                 64
   CABK                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
    CAG                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
    CBK                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
 DANSKE                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
    DBK                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
    DNB                   2                  2                              4                 16                                    2                                  2                       4                  4                            2                        2                  16                   8                  4                            4                  2                    2                           6 158                 64
    GLE                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
   INGA                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
    ISP                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
    KBC                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
    NDA                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
   RABO                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
    SAB                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
    SAN                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
    SEB                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
    SHB                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
   SWED                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
    UCG                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
    UNI                   0                  0                              0                 16                                    0                                  0                       0                  0                            0                        0                  16                   0                  0                            0                  0                    0                           0 208                 64
```

### 1.6: coverage, non-blank KPIs per bank and date (reported basis, 19 KPIs per date)

```
bank_id  2021-12-31  2022-06-30  2022-12-31  2023-06-30  2023-12-31  2024-06-30  2024-12-31  2025-06-30
    ABN          13          13          13          13          13          13          13          13
   BAMI          13          13          13          13          13          13          13          13
   BBVA          13          13          13          13          13          13          13          13
    BKT          13          13          13          13          13          13          13          13
   BMPS          13          13          13          13          13          13          13          13
    BNP          13          13          13          13          13          13          13          13
    BPE           8           6          13          13          13          13          13          13
   CABK          13          13          13          13          13          13          13          13
    CAG          13          13          13          13          13          13          13          13
    CBK          13          13          13          13          13          13          13          13
 DANSKE          13          13          13          13          13          13          13          13
    DBK          13          13          13          13          13          13          13          13
    DNB           0           6           8          13          13          13          13          13
    GLE          13          13          13          13          13          13          13          13
   INGA          13          13          13          13          13          13          13          13
    ISP          13          13          13          13          13          13          13          13
    KBC          13          13          13          13          13          13          13          13
    NDA          13          13          13          13          13          13          13          13
   RABO          13          13          13          13          13          13          13          13
    SAB          13          13          13          13          13          13          13          13
    SAN          13          13          13          13          13          13          13          13
    SEB          13          13          13          13          13          13          13          13
    SHB          13          13          13          13          13          13          13          13
   SWED          13          13          13          13          13          13          13          13
    UCG          13          13          13          13          13          13          13          13
    UNI          13          13          13          13          13          13          13          13
```

### 1.6: check rows by check and passed

```
          check  False  True
2_balance_sheet      0   499
       3_income      0   499
         4_cet1      0   502
5_period_length      0  5100
     6_currency      0    26
      9_outlier     14 18588
```

### 1.6: every failed check row

```
    check bank_id   ref_date                     field       value_a       value_b     diff_abs  diff_rel  threshold  passed      note
9_outlier     ABN 2021-03-31           impairments_fin -2.194929e+09 -9.844685e+07 2.096482e+09  4.072343        4.0   False flag only
9_outlier    BAMI 2025-06-30     intangibles_deduction  1.833951e+09  1.067005e+08 1.727250e+09  4.081935        4.0   False flag only
9_outlier    BBVA 2020-12-31        impairments_nonfin -1.995369e+09 -1.245560e+08 1.870813e+09  4.008463        4.0   False flag only
9_outlier    CABK 2021-03-31                 loans_all  1.242546e+11  7.577785e+09 1.166768e+11  4.040698        4.0   False flag only
9_outlier    CABK 2021-03-31 loans_customers_allowance  3.421327e+09  4.101958e+07 3.380307e+09  4.048204        4.0   False flag only
9_outlier    CABK 2021-03-31     loans_customers_gross  1.210492e+11  7.030153e+09 1.140190e+11  4.045117        4.0   False flag only
9_outlier    CABK 2021-03-31    loans_households_gross  7.127608e+10  3.359332e+09 6.791674e+10  4.057597        4.0   False flag only
9_outlier     CBK 2020-12-31     intangibles_deduction -2.147996e+09 -9.532225e+07 2.052673e+09  4.055962        4.0   False flag only
9_outlier     SAN 2021-03-31        impairments_nonfin -1.022442e+10 -5.311819e+08 9.693233e+09  4.119649        4.0   False flag only
9_outlier     UNI 2021-09-30                 loans_all  2.798209e+10  1.189764e+09 2.679232e+10  4.034366        4.0   False flag only
9_outlier     UNI 2021-09-30     loans_customers_gross  2.826554e+10  1.162994e+09 2.710255e+10  4.093634        4.0   False flag only
9_outlier     UNI 2021-09-30    loans_households_gross  1.796932e+10  8.450948e+08 1.712422e+10  4.088734        4.0   False flag only
9_outlier     UNI 2021-09-30                       rwa  1.607247e+10  3.118240e+08 1.576064e+10  4.039740        4.0   False flag only
9_outlier     UNI 2021-12-31           at1_instruments  4.999937e+08  2.630858e+07 4.736851e+08  4.129483        4.0   False flag only
```

### 1.6: check 3, the 10 largest relative misses

```
   check bank_id   ref_date                  field      value_a      value_b    diff_abs     diff_rel  threshold  passed note
3_income     UNI 2022-03-31 total_operating_income  377837000.0  377838000.0 1000.000000 2.646644e-06      0.005    True  eba
3_income     UNI 2021-06-30 total_operating_income  452721000.0  452722000.0 1000.000000 2.208866e-06      0.005    True  eba
3_income    CABK 2021-03-31 total_operating_income 1755152000.0 1755151000.0 1000.000000 5.697512e-07      0.005    True  eba
3_income    CABK 2022-03-31 total_operating_income 2481958000.0 2481959000.0 1000.000000 4.029077e-07      0.005    True  eba
3_income    CABK 2023-03-31 total_operating_income 2808523000.0 2808522000.0 1000.000000 3.560590e-07      0.005    True  eba
3_income    CABK 2024-03-31 total_operating_income 3186686000.0 3186687000.0 1000.000000 3.138056e-07      0.005    True  eba
3_income    CABK 2025-03-31 total_operating_income 3678243000.0 3678244000.0  999.999999 2.718689e-07      0.005    True  eba
3_income    CABK 2022-06-30 total_operating_income 5238950000.0 5238951000.0 1000.000000 1.908779e-07      0.005    True  eba
3_income    CABK 2020-09-30 total_operating_income 5518359000.0 5518360000.0 1000.000000 1.812133e-07      0.005    True  eba
3_income    CABK 2023-06-30 total_operating_income 6299222000.0 6299223000.0 1000.000000 1.587498e-07      0.005    True  eba
```

### 1.7: mergers

The deal list and figures were gathered by a research subagent that fetched each page. It was told to use only the acquirer's own announcements and reports, or the target's last report before completion, never news or memory. The figures on deals 12 to 21 of its list were checked by 2 further subagents, and not every page was re-fetched in the main session.

`source_url` in `mergers.csv` is the acquirer's own completion announcement, or its report or filing stating completion. The page each `target_total_assets` comes from is cited below. `mergers.csv` has no page column. Amounts are stored in units (Convention 4.1), so "209,841,949 EUR thousand" is stored as 209841949000.

#### Materiality (`python scripts/merger_materiality.py`)

The acquirer's EBA total_assets is taken at the last EBA reference date strictly before completion. A non-EUR target is converted at that date's ECB rate (`bpb/fx.py`, kind bs). break = ratio > merger_materiality (0.10).

```
acquirer_id                                                          target_name completion_date  target_total_assets target_ccy   ref_date  acquirer_total_assets_eur  target_total_assets_eur    ratio break                                                         note
        KBC                                             OTP Banka Slovensko a.s.      2020-11-26         1.433000e+09        EUR 2020-09-30               2.891225e+11             1.433000e+09 0.004956 False                                                             
        BPE           UBI Banca business unit sold by Intesa Sanpaolo (branches)      2021-02-22                  NaN        EUR                                   NaN                      NaN      NaN                            no EBA reference date before completion
       CABK                                                          Bankia S.A.      2021-03-26         2.098419e+11        EUR 2020-12-31               3.846868e+11             2.098419e+11 0.545488  True                                                             
        CAG                                          Credito Valtellinese S.p.A.      2021-04-30         2.388167e+10        EUR 2021-03-31               1.880920e+12             2.388167e+10 0.012697 False                                                             
        ISP                                                      REYL & Cie S.A.      2021-05-28         2.060198e+09        CHF 2021-03-31               8.228038e+11                      NaN      NaN                                      CHF is not in [fx] currencies
        UNI                                                       Liberbank S.A.      2021-07-30         4.751010e+10        EUR 2021-06-30               6.569767e+10             4.751010e+10 0.723163  True                                                             
        DNB                                                          Sbanken ASA      2022-03-30         1.022736e+11        NOK                                   NaN                      NaN      NaN                            no EBA reference date before completion
        BPE                                                  Banca Carige S.p.A.      2022-06-03                  NaN        EUR 2022-03-31               1.358219e+11                      NaN      NaN        target total assets not found on an acquirer or target page
        KBC                                        Raiffeisenbank (Bulgaria) EAD      2022-07-07         5.200000e+09        EUR 2022-06-30               3.386249e+11             5.200000e+09 0.015356 False                                                             
       HSBA                                       Silicon Valley Bank UK Limited      2023-03-13         1.149000e+10        USD                                   NaN                      NaN      NaN       UK acquirer: total assets from reports, entered in Section 3
        GLE                          LeasePlan Corporation N.V. (via ALD/Ayvens)      2023-05-22                  NaN        EUR 2023-03-31               1.406657e+12                      NaN      NaN        target total assets not found on an acquirer or target page
        DBK                                                Numis Corporation plc      2023-10-13                  NaN        GBP 2023-09-30               1.360647e+12                      NaN      NaN        target total assets not found on an acquirer or target page
        ISP                                                      First Bank S.A.      2024-05-31         1.500000e+09        EUR 2024-03-31               7.593786e+11             1.500000e+09 0.001975 False                                                             
        CAG                                         Banque Degroof Petercam S.A.      2024-06-04         8.129909e+09        EUR 2024-03-31               2.078287e+12             8.129909e+09 0.003912 False                                                             
       BARC                                   Tesco Bank retail banking business      2024-11-01                  NaN        GBP                                   NaN                      NaN      NaN       UK acquirer: total assets from reports, entered in Section 3
        UCG                                              Alpha Bank Romania S.A.      2024-11-04                  NaN        NaN 2024-09-30               8.034220e+11                      NaN      NaN        target total assets not found on an acquirer or target page
        NDA Danske Bank personal customer and private banking business in Norway      2024-11-18                  NaN        EUR 2024-09-30               5.331477e+11                      NaN      NaN        target total assets not found on an acquirer or target page
        UCG                                Aion Bank SA/NV and Vodeno Sp. z o.o.      2025-03-07         1.283866e+09        EUR 2024-12-31               7.839719e+11             1.283866e+09 0.001638 False                                                             
        DNB                                                  Carnegie Holding AB      2025-03-06         1.632599e+10        SEK 2024-12-31               2.763934e+11             1.424731e+09 0.005155 False                                                             
        NWG                             Sainsbury's Bank retail banking business      2025-05-01                  NaN        GBP                                   NaN                      NaN      NaN       UK acquirer: total assets from reports, entered in Section 3
        ABN                                  Hauck Aufhäuser Lampe Privatbank AG      2025-07-01         1.177700e+10        EUR 2025-06-30               4.142951e+11             1.177700e+10 0.028427 False                                                             
        BNP                     AXA Investment Managers (via BNP Paribas Cardif)      2025-07-01                  NaN        EUR 2025-06-30               2.573934e+12                      NaN      NaN        target total assets not found on an acquirer or target page
        BPE                                     Banca Popolare di Sondrio S.p.A.      2025-07-18         5.662858e+10        EUR 2025-06-30               1.445282e+11             5.662858e+10 0.391817  True                                                             
       BMPS                                                    Mediobanca S.p.A.      2025-09-15         9.991165e+10        EUR 2025-06-30               1.255844e+11             9.991165e+10 0.795574  True                                                             
        KBC                                                        365.bank a.s.      2026-01-15         4.700000e+09        EUR 2025-06-30               3.565054e+11             4.700000e+09 0.013184 False                                                             
      SANUK                                                TSB Banking Group plc      2026-04-30         4.528600e+10        GBP                                   NaN                      NaN      NaN       UK acquirer: total assets from reports, entered in Section 3
```

#### Source of each target_total_assets (PDF page numbers are physical pages)

| acquirer | target | figure as printed | ref date | document, page |
|---|---|---|---|---|
| KBC | OTP Banka Slovensko | 1 433 mil. EUR (bank only) | 2019-12-31 | https://www.csob.sk/documents/11005/1748111/otp-vyrocna-sprava-2019.pdf, p.9 |
| CABK | Bankia | TOTAL ASSETS 209,841,949 (EUR thousand) | 2020-12-31 | https://www.caixabank.com/deployedfiles/caixabank_com/Estaticos/PDFs/Accionistasinversores/consolidated-financial-statements-2020.pdf, p.15 |
| CAG | Creval | Totale dell'attivo 23.881.672 (EUR thousand) | 2020-12-31 | Creval FY2020 results release, https://web.archive.org/web/20240514163429id_/https://gruppo.credit-agricole.it/2021/Creval-Risultati-consolidati-al-31-dicembre-2020.pdf, p.12 |
| ISP | REYL & Cie | Total assets 2'060'197'900 (CHF) | 2020-12-31 | https://cdn.reyl.com/sites/default/files/reyl/REYL_RapportAnnuel2020.pdf, p.54 |
| UNI | Liberbank | 47.510.103 miles de euros (group) | 2020-12-31 | Liberbank 2020 annual accounts, https://www.unicajabanco.com/content/dam/unicaja/unicaja-corporacion/documentos-corporacion/junta-general-de-accionistas/2021-extraordinaria/2021-extraordinaria-Cuentas-anuales-individuales-consolidadas-liberbank-2020-en.pdf, p.33 |
| DNB | Sbanken | Total assets 102 273 586 (NOK thousand, group) | 2021-12-31 | Sbanken Annual Report 2021, https://web.archive.org/web/20220811235413id_/https://sbanken.no/globalassets/investor-relations/pdf/2021-annual-report/sbanken-asa-annual-report-2021.pdf, p.37 |
| KBC | Raiffeisenbank Bulgaria | 5.2bn EUR assets | 2021-06-30 | KBC announcement, https://cdn.assets.prezly.com/a292a36e-b30c-4fed-894f-31ee3f82d51d/-/inline/no/20211115_PB_RBI%20BG_%20ENG.pdf, p.1 |
| HSBA | SVB UK | Assets acquired 11,490 (USD million) | 2023-03-13 | HSBC 1Q23 earnings release, https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/1q/pdfs/hsbc-holdings-plc/230502-1q-2023-earnings-release.pdf, p.4 |
| ISP | First Bank | total assets of around €1.5 billion (undated) | not stated | Intesa announcement, https://group.intesasanpaolo.com/en/newsroom/press-releases/2023/10/-intesa-sanpaolo-to-acquire-first-bank-doubling-group-s-presence (HTML) |
| CAG | Degroof Petercam | Total de l'actif 8.129.909 (EUR thousand) | 2023-12-31 | https://annualreport.degroofpetercam.com/2023/public/2023/Downloads/FR/DP_AR2023_FR_6_FINANCIALSTATEMENTS.pdf, p.4 |
| UCG | Aion Bank (Vodeno not included) | TOTAL ASSETS 1.283.866 (EUR thousand, Belgian GAAP) | 2023-12-31 | https://aion.eu/dam/jcr:5e84c0cc-579c-4585-82da-3f1197e7f613/Aion%20Bank%20-%20Annual%20Report%202023%20-%20English%20-%20FINAL.pdf, p.37 |
| DNB | Carnegie Holding | Summa tillgångar 16 325 992 (SEK thousand) | 2023-12-31 | https://www.carnegie.se/app/uploads/file-manager/Finansiell%20Information/240410_Carnegie_Holding_2023_SWE_Final.pdf, p.33 |
| ABN | Hauck Aufhäuser Lampe | Assets 11,777 (EUR million, HGB, includes a unit not acquired) | 2023 | ABN AMRO announcement deck, https://assets.ctfassets.net/1u811bvgvthc/1XaBq6zLrngrAH1qVvPY1W/6d994f8671612eae630a5aae0fe0d230/Announcement_HAL.pdf, p.9 |
| BPE | Banca Popolare di Sondrio | TOTAL ASSETS 56,628,582 (EUR thousand) | 2024-12-31 | BPSO Annual Report 2024, https://web.archive.org/web/20250709045021id_/https://istituzionale.popso.it/sites/default/files/documents/Annual%20Report%202024_0.pdf, p.610 |
| BMPS | Mediobanca | Total assets 99,911,654 (EUR thousand) | 2024-12-31 | Mediobanca interim report, https://www.mediobanca.com/static/upload_new/med/0001/mediobanca-semestrale-2024-en_def.pdf, p.58 |
| KBC | 365.bank | total assets of €4.7bn | 2024-12 | KBC closing release (the source_url), p.2 |
| SANUK | TSB Banking Group | Total assets 45,286.0 (GBP million) | 2025-12-31 | https://www.tsb.co.uk/content/dam/tsb-public/documents/investors/financial-results-and-reports/2025/TSB-Banking-Group-ARA-2025.pdf, p.4 |

Blank `target_total_assets`, not found on an acquirer or target page:

- **BPER–Carige:** the mandatory-offer document of 8 Jul 2022 was not located.
- **UniCredit–Alpha Bank Romania**
- **BPER–UBI branch unit:** a business unit with no total assets published.
- **Nordea–Danske Norway:** a business transfer. Only lending of EUR 9bn and deposits of EUR 3bn are published.
- **Deutsche Bank–Numis:** no total line is printed.
- **Société Générale (Ayvens)–LeasePlan:** the report download was truncated.
- **Barclays–Tesco Bank and NatWest–Sainsbury's Bank:** not looked up.
- **BNP–AXA IM:** not looked up.

#### Deals considered and left out of `mergers.csv`

| deal | reason | source |
|---|---|---|
| ABN AMRO–NIBC | Completed 2026-08-01, after the window. | https://nibc.com/news/nibc-acquisition-by-abn-amro-completed (the ABN AMRO page returned 503) |
| Intesa Sanpaolo–UBI Banca | Offer settled 2020-08-05, before the window. | https://group.intesasanpaolo.com/en/newsroom/all-news/news/2020/opas-ubi-history |
| Nordea–Gjensidige Bank | Completed 2019-03-01, before the window. | https://www.nordea.com/en/press/2019-03-01/nordea-completes-acquisition-of-gjensidige-bank |
| Banco BPM (Vita)–Anima Holding | Completed 2025-04 in the window, but no Banco BPM page for the completion was found, so there is no acquirer source URL. | news only |
| BBVA–Sabadell; UniCredit–Banco BPM | Offers failed or were withdrawn. | not fetched |
| UniCredit–Commerzbank, UniCredit–Alpha Bank (Greece), Crédit Agricole–Banco BPM, BBVA–Garanti 2022 | Minority stakes, or no change of control. | not fetched |

## Tests run

```
$ pytest -p socket --disable-socket -q
.................                                                        [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\_pytest\config\__init__.py:894
  C:\Utkarsh\10. Quant Projects\15) Bank Benchmarking Project\Bank-Performance-Benchmarking\.venv\Lib\site-packages\_pytest\config\__init__.py:894: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; socket
    self.import_plugin(arg, consider_entry_points=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================= slowest 8 durations =============================
63.15s call     tests/test_kpi.py::test_recompute
15.40s call     tests/test_eba_raw.py::test_reference_dates
5.16s call     tests/test_ingest.py::test_summed_field_real
4.42s call     tests/test_ingest.py::test_summed_field_partial_missing
0.43s call     tests/test_eba_raw.py::test_manifest_hashes
0.38s call     tests/test_fx.py::test_roundtrip
0.18s call     tests/test_ingest.py::test_unnamed_dims_zero
0.17s call     tests/test_kpi.py::test_missing_input
17 passed, 1 warning in 92.50s (0:01:32)
$ ruff check .
All checks passed!
```

## Fresh-clone check

The section's commits were pushed first, so that the clone is of the pushed repo (rule 12). Clone path `C:\Users\astha\AppData\Local\Temp\bpb1b`, Windows 11, uv 0.11.6. The `uv pip install -r` output is cut to its last 2 lines.

```
$ git clone https://github.com/uty101/Bank-Performance-Benchmarking.git /c/Users/astha/AppData/Local/Temp/bpb1b
0f8971c step 1.7: mergers and materiality
$ uv venv --python 3.12
Using CPython 3.12.13
Creating virtual environment at: .venv
Activate with: .venv\Scripts\activate
$ uv pip install -r requirements-lock.txt
 + wrapt==2.5.2
 + yfinance==1.7.0
$ uv pip install -e . --no-deps
Installed 1 package in 103ms
 + bpb==0.1.0 (from file:///C:/Users/astha/AppData/Local/Temp/bpb1b)
$ ruff check .
All checks passed!
$ pytest -p socket --disable-socket -q
.................                                                        [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\_pytest\config\__init__.py:894
  C:\Users\astha\AppData\Local\Temp\bpb1b\.venv\Lib\site-packages\_pytest\config\__init__.py:894: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; socket
    self.import_plugin(arg, consider_entry_points=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
17 passed, 1 warning in 131.76s (0:02:11)
$ git status --porcelain
```

`git status --porcelain` printed nothing.

## Runtime per step

- 1.1: `pull_data.py --stage eba` took 5 m 38 s (session 1).
- 1.2: `build_eba_maps.py` took 29.7 s (session 1, about the same in 1.2b).
- 1.3: `eba_facts`, all 5 releases, took 27 s.
- 1.4: `pull_data.py --stage fx` took over 2 minutes (the ECB API is slow; the exact time was not captured).
- 1.5 and 1.6: `scripts/run_all.py` (facts, KPIs, checks) took 53.1 s. A second run gave byte-identical `kpi.csv` (sha256 025ed23a…) and `checks.csv` (sha256 2eafe0d1…), and `facts.parquet` was byte-identical across 2 runs (f6314435…).
- 1.7: `merger_materiality.py` took under 30 s.
- Test suite: 92.5 s locally and 131.8 s on the fresh clone. `test_recompute` alone takes 63 s, because it rebuilds every KPI from the raw files.

## Deviations from PLAN.md

1. **Session 1 stopped at step 1.3 (OPEN-25).** The original stop evidence follows, unchanged.

#### Stop evidence: OPEN-25

##### OPEN-25: raw EBA rows (amounts in EUR millions for SEK, NOK and DKK banks; ratios as decimals)

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

##### OPEN-25: unit search in every committed SDD.xlsx and TR_Metadata.xlsx

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

##### OPEN-25: unit headings in 2025_EU-wide_Transparency_exercise_Mapped_templates.xlsx (not committed)

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

2. **Release pages (session 1).** The 2021 release page is the hub's link `.../eu-wide-transparency-exercise/2021-eu-wide-transparency`, and the 2025 release page is the hub.
3. **Country filter.** The filter reads `NSA`, the bank's country, not the exposure `Country` of `tr_cre.csv`.
4. **Manifest layout.** `MANIFEST.json` is `{"files": [...]}`, with one entry per file: path, committed, url, pulled_utc, sha256, bytes, rows, first_date, last_date and encoding (plus filtered_from and filter on a filtered file).
5. **Map builder.** The builder is `scripts/build_eba_maps.py`, with no network. Name containment is matched on whole words. `dim_filter` holds dimension codes.
6. **Names of the OPEN-06 components.** `gains_derecognition_not_fvtpl`, `gains_held_for_trading`, `gains_designated_fvtpl`, `gains_hedge_accounting`, `exchange_differences` and `other_operating_net`, each with the standard source-map rules.
7. **`fields.yaml` layout.** `kind` is now `amount` or `ratio` (instruction 01b step 1.2b). The P&L or balance sheet split it used to carry moved to a new key, `period` (pl, bs, count). The 3 count fields (fte, customers, shares_out) have `kind: amount`, since only 2 kinds exist.
8. **`bank_groups` in the source map.** `config/source_map.yaml` gained `bank_groups: uk: [LLOY, NWG, BARC, HSBA, SANUK]`, because `apply_source_map(facts, source_map)` receives no universe. Every other bank is `eu`.
9. **Locator format.** The `eba` locator is `<item>@<release>`, for example `2521010@2025`. A summed field over 1 item and several dimension rows keeps the 1 item code. A field summed over several items would join them with `+`, though no current map does.
10. **New statuses.** Besides `missing_input:<field>`, `mixed_family` and `pending_section_3`, the KPI engine uses `zero_denominator` for a denominator of exactly 0 (no row hit it) and `ok` for a filled value. `missing_input` names the first missing base field: for an average, the averaged quantity; for a derived quantity, its missing input.
11. **Family choice.** When more than 1 family could fill a KPI at a date, the engine prefers eba, then p3, then report. In Section 1 there is only `eba`. The ordering matters only from Section 2, where it keeps 2025-06-30 KPIs on `eba` (OPEN-03).
12. **Synthetic frame size.** The step 1.3 synthetic frame has 16 rows and gives 12 FACTS rows, not the 12 and 8 of instruction 01, because instruction 01b adds I4 at both banks and dates.
13. **Check 6.** It compares each bank's `ccy` within one family over time. The `eba` family is EUR for every bank by decision, so it does not compare with `report_ccy`.
14. **Check 9.** It uses changes between consecutive quarter ends only, and the standard deviation with ddof 1.
15. **Output writer.** `scripts/run_all.py` writes `facts.parquet`, `kpi.csv` and `checks.csv` (WORKFLOW Part 5 names it), and `bpb/tables.py` holds the CSV writer.
16. **Pushes.** There were 3 pushes, as in session 1: the steps (for the fresh-clone check), the review, then the status file.

## Not verified

- **Merger figures were not all re-read in the main session.** They come from a research subagent, and its figures for deals 12 to 21 were checked by 2 further subagents. No page was re-fetched in the main session. List completeness was not checked exhaustively either: small portfolio and fintech purchases were not searched.
- **Some target figures are rounded or partial.** KBC's 365.bank (€4.7bn) and Raiffeisen Bulgaria (€5.2bn) and Intesa's First Bank (~€1.5bn, undated) are rounded acquirer figures. OTP Slovensko is bank-only. The HAL figure includes a unit that was not acquired. SVB UK is HSBC's "assets acquired", not a target report figure. None of these is near the 10% threshold.
- **Completion dates for the 2 exchange offers.** For BPER–Sondrio and MPS–Mediobanca, the completion date is the first settlement giving majority control, not the later settlements (80.69% and 86.3%).
- **Loans line.** `loans_all` and `debt_securities` (NPE, all portfolios other than held for trading) have not been reconciled with any bank's own report.
- **Filter re-runs.** Whether re-running the EBA filter on another machine gives the same gzip bytes was not checked. The committed bytes are what `test_manifest_hashes` checks.
- **Derived quantities across families.** The `fx_combined` path of `derived` (instruction 01b B.2) is coded but no Section 1 row triggers it, and no test covers it.

## Open questions

No new item was added to `decisions/OPEN.md`, and OPEN-17 to OPEN-25 are decided. Questions for the reviewer:

1. **Is BPER–Carige a merger break?** Carige's total assets were not found (deal completed 2022-06-03). BPER's EBA total assets at 2022-03-31 are EUR 135.8bn, so Carige is a break if its total assets exceed EUR 13.6bn. The figure is probably in BPER's mandatory-offer document of 8 Jul 2022, or in Carige's 2021 annual report.
2. **Should non-bank acquisitions stay in `mergers.csv`?** BNP–AXA IM (an asset manager), Société Générale–LeasePlan (a leasing group with a bank licence) and Deutsche Bank–Numis (a broker) are listed with blank target_total_assets. Banco BPM–Anima is left out, since no acquirer page was found.
3. **The 4 UK acquisitions wait for Section 3.** These are SANUK–TSB (GBP 45.3bn), HSBA–SVB UK, BARC–Tesco Bank and NWG–Sainsbury's Bank. Each needs UK total assets from reports.
4. **REYL is CHF.** CHF is not in `[fx] currencies`, so its ratio is blank. At CHF 2.06bn against ISP's EUR 823bn it is far below 10% at any plausible rate.
5. **Material breaks found:** CABK–Bankia (2021-03-26, ratio 0.545), UNI–Liberbank (2021-07-30, 0.723), BPE–Banca Popolare di Sondrio (2025-07-18, 0.392) and BMPS–Mediobanca (2025-09-15, 0.796). The Bankia and Liberbank quarters also appear among the 14 check 9 outlier flags.

## Files changed

```
 CLAUDE.md                                |    10 +
 bpb/checks.py                            |   129 +
 bpb/config.py                            |   150 +
 bpb/fx.py                                |    58 +
 bpb/ingest.py                            |   168 +
 bpb/kpi.py                               |   291 +
 bpb/lineage.py                           |     9 +
 bpb/tables.py                            |    13 +
 config/eba_map_2021.csv                  |    20 +
 config/eba_map_2022.csv                  |    20 +
 config/eba_map_2023.csv                  |    20 +
 config/eba_map_2024.csv                  |    20 +
 config/eba_map_2025.csv                  |    20 +
 config/fields.yaml                       |   100 +-
 config/source_map.yaml                   |     7 +-
 data/manual/mergers.csv                  |    26 +
 data/manual/universe.csv                 |     2 +-
 data/raw/MANIFEST.json                   |    60 +
 data/raw/fx/DKK.csv                      |  1687 ++
 data/raw/fx/GBP.csv                      |  1687 ++
 data/raw/fx/NOK.csv                      |  1687 ++
 data/raw/fx/SEK.csv                      |  1687 ++
 data/raw/fx/USD.csv                      |  1687 ++
 decisions/OPEN.md                        |    18 +
 decisions/section_1_review.md            |    71 +
 instructions/01b_section_1_completion.md |   132 +
 outputs/tables/checks.csv                | 25229 +++++++++++++++++++++++++++++
 outputs/tables/kpi.csv                   |  7905 +++++++++
 scripts/build_eba_maps.py                |    95 +-
 scripts/merger_materiality.py            |    68 +
 scripts/pull_data.py                     |    29 +-
 scripts/run_all.py                       |    47 +
 tests/test_checks.py                     |    40 +
 tests/test_fx.py                         |    33 +
 tests/test_ingest.py                     |   140 +
 tests/test_kpi.py                        |    65 +
 36 files changed, 43326 insertions(+), 104 deletions(-)
```

Plus `review/section_1.md` (this file) and `instructions/01b_section_1_completion.status.md`.

## Reviewer reads

1. `instructions/01b_section_1_completion.status.md`
2. This file: 1.7 mergers, the coverage table, every failed check row, then the ISP, SWED and BBVA KPI tables
3. `bpb/ingest.py` (`load_eba`) and `tests/test_ingest.py`
4. `bpb/kpi.py` (`compute_kpis`, `rolling_12m`, `averages`) and `tests/test_kpi.py`
5. `bpb/checks.py` and `data/manual/mergers.csv`
