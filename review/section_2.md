# Section 2

**Outcome: complete, with 1 bank stopped under rule 4 (SHB, scope gate).**

- **Session 1 (instruction 02)** stopped at the CAG total assets gate.
- **Session 2 (instruction 02b)** applied the stop decisions (step 2.0b) and added the 02b fields to the 13 committed banks. It then entered the other 13 EU banks in universe order and ran steps 2.4 and 2.5.

**Results:**
- `report_entries.csv` holds 5,589 entries for 26 banks, and all 5,589 pass provenance.
- Seam 1 passes on all 72 rows. Seam 2 has 738 rows; it has no threshold.
- The scope adjusted gate (02b B.1) passes for 23 banks and fails for SHB:
  - SHB's EU LR1 row 1 is already the prudential total (equal to EBA), and row 2 adds back +288,024m SEK.
  - Row 1 + row 2 is 8.5% above EBA.
- Following B.1, SHB's report and p3 rows stay in FACTS and in the checks with status `scope_gate_failed`. All of SHB's KPIs after 2025-06-30 are blank, and every other bank is finished.
- CBK and BKT have no LR1, because no Pillar 3 document was obtainable, so no gate row was written for them.

**Hand check:** ISP nim (0.026664) and cost_income (0.431708) at 2025-12-31 agree with `kpi.csv` to 1e-11.

## Steps completed

- 2.0 apply section 1 review decisions (6efb278)
- 2.1 load_p3 and load_report_entries (eb9aecc); fix: provenance reads ASCII digits only, provenance on mergers.csv rows (92cda21)
- 2.2 report URLs and fetch (71154d8); fix: ruff PLW1510 in fetch_reports.py (811eec3)
- 2.3, session 1: NDA (1e8959e), DNB (c0b5c60), DANSKE (da57e5b), SEB (982c977), SHB (0652103), SWED (f246388), INGA (efe4b74), ABN (23b15dc), KBC (8376a6c), RABO (26d7e4a), BNP (fd99099), GLE (642a65d), CAG (25ecc99). Stopped at the CAG gate (review a5c5bc0, status f174f81).
- 2.0b apply section 2 stop decisions (419f762)
- 2.3, session 2. The 13 committed banks gained B.4 zero cells, B.2 FY2024 P&L, B.1 LR1 fields and the new Pillar 3 workbooks; B.5 to B.8 were re-applied. Then the remaining 13 banks were entered. One commit per bank, in universe order: NDA (62c7620), DNB (9a76d43), DANSKE (f5c2d3f), SEB (7995fe1), SHB (6272787), SWED (5944351), INGA (a49491f), ABN (56814ec), KBC (b6d8b82), RABO (32f3e82), BNP (9496cc8), GLE (9a332ca), CAG (dfc1c22), DBK (14a2815), CBK (1109095), SAN (66af9b6), BBVA (f437e86), CABK (a47aa1d), SAB (012561d), BKT (bbddac1), UNI (714657f), UCG (0a87383), ISP (b056d49), BAMI (a8bbf85), BPE (df24aa1), BMPS (9c8b55f)
- 2.4 provenance and seams: test_provenance_styles, checks on every family, scope gate (fdf60a2)
- 2.5 KPIs at 2025-12-31 and 2026-06-30 for EU banks (f8adbcb)

## Evidence

### Step 2.0: mergers (session 1, as reviewed at a5c5bc0)

The 4 material deals, checked again this session. Each source PDF was fetched and the line giving total assets printed (PyMuPDF text):

| deal | document fetched | page | line as printed (pymupdf text) | figure confirmed |
|---|---|---|---|---|
| CABK–Bankia | https://www.caixabank.com/deployedfiles/caixabank_com/Estaticos/PDFs/Accionistasinversores/consolidated-financial-statements-2020.pdf ("BANKIA, S.A. AND SUBSIDIARIES ... Consolidated balance sheets at 31 December 2020 and 2019 (in thousands of euros)") | 15 | `TOTAL ASSETS` / `209,841,949` / `208,468,273` (2020, 2019) | 209,841,949 thousand = 209,841,949,000 |
| UNI–Liberbank | https://www.unicajabanco.com/content/dam/unicaja/unicaja-corporacion/documentos-corporacion/junta-general-de-accionistas/2021-extraordinaria/2021-extraordinaria-Cuentas-anuales-individuales-consolidadas-liberbank-2020-en.pdf | 33 | `31 de diciembre de 2020 y 2019 asciende a 47.510.103 y 41.947.134 miles de euros,` (activos consolidados del Grupo Liberbank) | 47,510,103 thousand = 47,510,103,000 |
| BPE–Sondrio | recorded URL (web.archive.org copy of istituzionale.popso.it Annual Report 2024) now refuses (archive bot block; direct URL returns HTML). Confirmed instead from BPSO FY2024 results release, https://emarketstorage.it/sites/default/files/comunicati/2025-02/20250206_160405.pdf | 40 | `CONSOLIDATED STATEMENT OF FINANCIAL POSITION` `(in thousands of euro)` `31/12/2024` ... `56.628.582` (total assets) | 56,628,582 thousand = 56,628,582,000 |
| BMPS–Mediobanca | https://www.mediobanca.com/static/upload_new/med/0001/mediobanca-semestrale-2024-en_def.pdf ("Consolidated Balance Sheet (€'000) Assets 31/12/24 30/6/24") | 58 | `Total assets` / ` 99,911,654 ` / ` 99,226,274 ` | 99,911,654 thousand = 99,911,654,000 |

The 9 hashed merger sources (doc_type `merger_target` in `report_urls.csv`) as cited on their page in the pdfplumber cache:

```
BPE   2021-12-31 p76  TOTALE DELL'ATTIVO 22.309.820 22.030.236          (Importi in migliaia di euro) Banca Carige FY2021
BAMI  2024-12-31 p38  TOTAL ASSETS 2,689,939 2,390,423                  (Thousands of euros) Anima Holding FY2024
GLE   2022-12-31 p118 TOTAL ASSETS 34,520,246 32,249,975                (In thousands of euros) LeasePlan FY2022
DBK   2022-09-30 p121 Total assets 523,785 36,093 62,918 622,796        (GBP'000, Total column) Numis FY2022 note 29
UCG   2023-12-31 p11  TOTAL ASSETS 23,571,025 21,130,620                (RON thousand) Alpha Bank Romania FY2023 separate statements
CABK  2020-12-31 p15  TOTAL ASSETS 209,841,949 208,468,273              (in thousands of euros) Bankia FY2020
UNI   2020-12-31 p33  47.510.103 y 41.947.134 miles de euros            Liberbank FY2020
BPE   2024-12-31 p40  TOTAL ASSETS 56.628.582 57.721.765                (in thousands of euro) BPSO FY2024 results release
BMPS  2024-12-31 p58  Total assets 99,911,654 99,226,274                (€'000) Mediobanca half-year at 31/12/24
```

Nordea–Danske Norway: the press release (source_url) reads "lending and deposit volumes of EUR 9bn and 3bn, respectively", so target_total_assets 9,000,000,000 EUR with size_basis `loans`. Banco BPM–Anima: final results 9 Apr 2025, settlement 11 Apr 2025 (source_url is Banco BPM's final-results release). Not sized: BPER–UBI branch unit (no document prints the unit's own total assets; the nearest figures are Intesa's FY2020 held-for-sale note, 26,395m, which also covers branches sold to BPPB, and UBI's table 11.1, 25,580,963k, which includes bad-loan portfolios) and BNP–AXA IM (no FY2024 consolidated accounts of AXA IM published; the AXA URD held-for-sale figure, 3,927m, is net of intra-group balances). Neither proxy was used.

Full mergers.csv with ratios and break flags (`scripts/merger_materiality.py`, CHF now in `[fx]`):

```
acquirer_id                                                          target_name completion_date  target_total_assets target_ccy   ref_date  acquirer_total_assets_eur  target_total_assets_eur    ratio break                                                         note
        KBC                                             OTP Banka Slovensko a.s.      2020-11-26         1.433000e+09        EUR 2020-09-30               2.891225e+11             1.433000e+09 0.004956 False                                                             
        BPE           UBI Banca business unit sold by Intesa Sanpaolo (branches)      2021-02-22                  NaN        EUR                                   NaN                      NaN      NaN                            no EBA reference date before completion
       CABK                                                          Bankia S.A.      2021-03-26         2.098419e+11        EUR 2020-12-31               3.846868e+11             2.098419e+11 0.545488  True                                                             
        CAG                                          Credito Valtellinese S.p.A.      2021-04-30         2.388167e+10        EUR 2021-03-31               1.880920e+12             2.388167e+10 0.012697 False                                                             
        ISP                                                      REYL & Cie S.A.      2021-05-28         2.060198e+09        CHF 2021-03-31               8.228038e+11             1.861064e+09 0.002262 False                                                             
        UNI                                                       Liberbank S.A.      2021-07-30         4.751010e+10        EUR 2021-06-30               6.569767e+10             4.751010e+10 0.723163  True                                                             
        DNB                                                          Sbanken ASA      2022-03-30         1.022736e+11        NOK                                   NaN                      NaN      NaN                            no EBA reference date before completion
        BPE                                                  Banca Carige S.p.A.      2022-06-03         2.230982e+10        EUR 2022-03-31               1.358219e+11             2.230982e+10 0.164258  True                                                             
        KBC                                        Raiffeisenbank (Bulgaria) EAD      2022-07-07         5.200000e+09        EUR 2022-06-30               3.386249e+11             5.200000e+09 0.015356 False                                                             
       HSBA                                       Silicon Valley Bank UK Limited      2023-03-13         1.149000e+10        USD                                   NaN                      NaN      NaN       UK acquirer: total assets from reports, entered in Section 3
        GLE                          LeasePlan Corporation N.V. (via ALD/Ayvens)      2023-05-22         3.452025e+10        EUR 2023-03-31               1.406657e+12             3.452025e+10 0.024541 False                                                             
        DBK                                                Numis Corporation plc      2023-10-13         6.227960e+08        GBP 2023-09-30               1.360647e+12             7.203451e+08 0.000529 False                                                             
        ISP                                                      First Bank S.A.      2024-05-31         1.500000e+09        EUR 2024-03-31               7.593786e+11             1.500000e+09 0.001975 False                                                             
        CAG                                         Banque Degroof Petercam S.A.      2024-06-04         8.129909e+09        EUR 2024-03-31               2.078287e+12             8.129909e+09 0.003912 False                                                             
       BARC                                   Tesco Bank retail banking business      2024-11-01                  NaN        GBP                                   NaN                      NaN      NaN       UK acquirer: total assets from reports, entered in Section 3
        UCG                                              Alpha Bank Romania S.A.      2024-11-04         2.357102e+10        RON 2024-09-30               8.034220e+11                      NaN      NaN                                      RON is not in [fx] currencies
        NDA Danske Bank personal customer and private banking business in Norway      2024-11-18         9.000000e+09        EUR 2024-09-30               5.331477e+11             9.000000e+09 0.016881 False                                                             
        DNB                                                  Carnegie Holding AB      2025-03-06         1.632599e+10        SEK 2024-12-31               2.763934e+11             1.424731e+09 0.005155 False                                                             
        UCG                                Aion Bank SA/NV and Vodeno Sp. z o.o.      2025-03-07         1.283866e+09        EUR 2024-12-31               7.839719e+11             1.283866e+09 0.001638 False                                                             
       BAMI                            Anima Holding S.p.A. (via Banco BPM Vita)      2025-04-11         2.689939e+09        EUR 2025-03-31               1.915734e+11             2.689939e+09 0.014041 False                                                             
        NWG                             Sainsbury's Bank retail banking business      2025-05-01                  NaN        GBP                                   NaN                      NaN      NaN       UK acquirer: total assets from reports, entered in Section 3
        ABN                                  Hauck Aufhäuser Lampe Privatbank AG      2025-07-01         1.177700e+10        EUR 2025-06-30               4.142951e+11             1.177700e+10 0.028427 False                                                             
        BNP                     AXA Investment Managers (via BNP Paribas Cardif)      2025-07-01                  NaN        EUR 2025-06-30               2.573934e+12                      NaN      NaN        target total assets not found on an acquirer or target page
        BPE                                     Banca Popolare di Sondrio S.p.A.      2025-07-18         5.662858e+10        EUR 2025-06-30               1.445282e+11             5.662858e+10 0.391817  True                                                             
       BMPS                                                    Mediobanca S.p.A.      2025-09-15         9.991165e+10        EUR 2025-06-30               1.255844e+11             9.991165e+10 0.795574  True                                                             
        KBC                                                        365.bank a.s.      2026-01-15         4.700000e+09        EUR 2025-06-30               3.565054e+11             4.700000e+09 0.013184 False                                                             
      SANUK                                                TSB Banking Group plc      2026-04-30         4.528600e+10        GBP                                   NaN                      NaN      NaN       UK acquirer: total assets from reports, entered in Section 3
```

`data/manual/mergers.csv` in full:

```
acquirer_id,target_name,completion_date,target_total_assets,target_ccy,source_url,source_sha256,source_page,size_basis
KBC,OTP Banka Slovensko a.s.,2020-11-26,1433000000,EUR,https://cdn.assets.prezly.com/8b650d62-c523-41df-b3ec-23bf419680d1/-/inline/no/20201126_PB_closing%20OTP_ENG.pdf,,,total_assets
BPE,UBI Banca business unit sold by Intesa Sanpaolo (branches),2021-02-22,,EUR,https://group.bper.it/documents/133577364/0/21.02.19_ComSt_Accordo_Gruppo_Intesa_ENG_.pdf/37706018-c10c-0719-33bf-cc9fb050841d?t=1613760496854,,,
CABK,Bankia S.A.,2021-03-26,209841949000,EUR,https://www.caixabank.com/StaticFiles/pdfs/210326_OIR_merger_registration_en.pdf,89d03b3cfde98980e10d005e88f08af9568aa9ad496bf36693d7a57ef9cb120f,15,total_assets
CAG,Credito Valtellinese S.p.A.,2021-04-30,23881672000,EUR,https://credit-agricole.it/media/filer_public/c5/ac/c5acfa20-7b56-47ae-87ca-e9aa5ae886db/cs-opa-creval-successo-dell-offerta-pubblica-di-acquisto-volontaria-promossa-da-credit-agricole-italia-sulla-totalita-delle-azioni-di-credito-valtellinese-eng-sito.pdf,,,total_assets
ISP,REYL & Cie S.A.,2021-05-28,2060197900,CHF,https://emarketstorage.it/sites/default/files/comunicati/2022-05/20210903_101936.pdf,,,total_assets
UNI,Liberbank S.A.,2021-07-30,47510103000,EUR,https://unicajabanco.com/en/sala-de-comunicacion/buscador-noticias/2021/07/unicaja-banco-culmina-la-integracion-legal-de-liberbank-que-conv,2a3b0df0f556b391f068928bf60b5efc68bcf9a887817f8e68f7194b5697fb2d,33,total_assets
DNB,Sbanken ASA,2022-03-30,102273586000,NOK,https://ir.dnb.no/sites/default/files/pr/202204281231-1.pdf,,,total_assets
BPE,Banca Carige S.p.A.,2022-06-03,22309820000,EUR,https://group.bper.it/documents/133577364/0/1654292264_22.06.03_-_BPER_-_Acquisizione_partecipazione_di_controllo_di_Carige_e_cessione_sportelli_h_1545_EN+s.pdf/5e409d8b-bf67-0235-e702-bfd17072ab3c?t=1654293236327,1e30783de2e9a1fc8465e39bde90a974b8fd682b33750cf89f05b3305434791c,76,total_assets
KBC,Raiffeisenbank (Bulgaria) EAD,2022-07-07,5200000000,EUR,https://www.kbc.com/content/dam/kbccom/doc/newsroom/pressreleases/2022/20220707_Closing%20KBC_Raiffeisenbank%20Bulgaria_EN.pdf,,,total_assets
HSBA,Silicon Valley Bank UK Limited,2023-03-13,11490000000,USD,https://www.hsbc.com/-/files/hsbc/media/media-release/2023/230313-hsbc-acquires-silicon-valley-bank-uk-limited.pdf,,,total_assets
GLE,LeasePlan Corporation N.V. (via ALD/Ayvens),2023-05-22,34520246000,EUR,https://www.ayvens.com/en-cp/news/newsroom/press-releases-2023/press-release-ald-successfully-completes-the-acquisition-of-leaseplan-and-announces-management-changes,65c0a58690b2f9306459cacb60e20e6f537f738ef1ec51a778074da85292ed6b,118,total_assets
DBK,Numis Corporation plc,2023-10-13,622796000,GBP,https://www.db.com/news/detail/20231013-deutsche-bank-completes-acquisition-of-numis,43e693fd5a144d8395edc584602b3f25547d307bae91d65213d661debbcd73b0,121,total_assets
ISP,First Bank S.A.,2024-05-31,1500000000,EUR,https://group.intesasanpaolo.com/en/newsroom/press-releases/2024/05/intesa-sanpaolo-finalizes-acquisition-of-first-bank,,,total_assets
CAG,Banque Degroof Petercam S.A.,2024-06-04,8129909000,EUR,https://ca-indosuez.com/press/press-releases/indosuez-wealth-management-finalises-the-acquisition-of-degroof-petercam,,,total_assets
BARC,Tesco Bank retail banking business,2024-11-01,,GBP,https://www.sec.gov/Archives/edgar/data/312069/000165495424013575/a5037k.htm,,,
UCG,Alpha Bank Romania S.A.,2024-11-04,23571025000,RON,https://www.unicreditgroup.eu/en/press-media/press-releases/2024/november/unicredit-and-alpha-services-and-holdings-announce-completion-of.html,bacb44c8e0a5730cd152a429083cd39c3934c654d4442901517080a38480988a,11,total_assets
NDA,Danske Bank personal customer and private banking business in Norway,2024-11-18,9000000000,EUR,https://www.nordea.com/en/press/2024-11-18/nordea-completes-the-acquisition-of-danske-banks-personal-customer-and-private-banking-business-in-norway,,,loans
DNB,Carnegie Holding AB,2025-03-06,16325992000,SEK,https://ir.dnb.no/press-and-reports/press-releases/fulfillment-conditions-dnb-bank-asas-acquisition-carnegie-2306571,,,total_assets
UCG,Aion Bank SA/NV and Vodeno Sp. z o.o.,2025-03-07,1283866000,EUR,https://www.unicreditgroup.eu/en/press-media/press-releases-price-sensitive/2025/march/unicredit-completes-acquisition-of-aion-bank-and-vodeno--kicking.html,,,total_assets
BAMI,Anima Holding S.p.A. (via Banco BPM Vita),2025-04-11,2689939000,EUR,https://www.emarketstorage.it/sites/default/files/comunicati/2025-04/20250409_164754.pdf,049915f5f8b264b652311a495b7f243c15c1878499dea1a2f08289bacb85897f,38,total_assets
NWG,Sainsbury's Bank retail banking business,2025-05-01,,GBP,https://www.sec.gov/Archives/edgar/data/844150/000165495425005032/a1510h.htm,,,
ABN,Hauck Aufhäuser Lampe Privatbank AG,2025-07-01,11777000000,EUR,https://www.abnamro.com/en/news/abn-amro-completes-acquisition-of-hauck-aufhaeuser-lampe-in-germany,,,total_assets
BNP,AXA Investment Managers (via BNP Paribas Cardif),2025-07-01,,EUR,https://group.bnpparibas/en/press-release/bnp-paribas-cardif-completes-the-acquisition-of-axa-investment-managers,,,
BPE,Banca Popolare di Sondrio S.p.A.,2025-07-18,56628582000,EUR,https://group.bper.it/documents/133577364/2795795058/Consolidated+Half-Year+Report+as+at+30+06+2025.pdf/ee8e303c-519c-d986-4655-01592227dfab?version=1.0&t=1758275603287,766c124b21821a3dc7829c1384361b8281075f0b57648c7c42e65994364194b4,40,total_assets
BMPS,Mediobanca S.p.A.,2025-09-15,99911654000,EUR,https://www.gruppomps.it/en/media-and-news/press-releases/pr-15-09-2025.html,0d1119ccb84dcd0bb91e9842b46ff3bf4b3e0621b0e68403bc6cbe78beafbf17,58,total_assets
KBC,365.bank a.s.,2026-01-15,4700000000,EUR,https://www.kbc.com/content/dam/kbccom/doc/newsroom/pressreleases/2026/20260115-pb-closing-365-bank-en-2.pdf,,,total_assets
SANUK,TSB Banking Group plc,2026-04-30,45286000000,GBP,https://www.santander.co.uk/about-santander/media-centre/press-releases/santander-uk-completes-cash-acquisition-of-tsb-banking,,,total_assets
```

New material break: BPER–Carige, 2022-06-03, ratio 0.164. REYL now has a ratio (0.0023). Alpha Bank Romania is in RON, which is not in `[fx] currencies`, so its ratio is blank.

### Step 2.0b: mergers (B.10)

- The UBI branch unit and AXA IM are sized by consideration (`size_basis` `consideration`). Both are cited from a hashed page 1 of the source and pass merger provenance (under Step 2.4).
- RON is now in `[fx]`, so Alpha Bank Romania's ratio is 0.0059: not material.
- The UBI unit's ratio stays blank: there is no EBA reference date before its completion (2021-02-22).
- Carige (0.164) is accepted as a material break.

#### `python scripts/merger_materiality.py`

```
acquirer_id                                                          target_name completion_date  target_total_assets target_ccy   ref_date  acquirer_total_assets_eur  target_total_assets_eur    ratio break                                                         note
        KBC                                             OTP Banka Slovensko a.s.      2020-11-26         1.433000e+09        EUR 2020-09-30               2.891225e+11             1.433000e+09 0.004956 False                                                             
        BPE           UBI Banca business unit sold by Intesa Sanpaolo (branches)      2021-02-22         6.440400e+08        EUR                                   NaN                      NaN      NaN                            no EBA reference date before completion
       CABK                                                          Bankia S.A.      2021-03-26         2.098419e+11        EUR 2020-12-31               3.846868e+11             2.098419e+11 0.545488  True                                                             
        CAG                                          Credito Valtellinese S.p.A.      2021-04-30         2.388167e+10        EUR 2021-03-31               1.880920e+12             2.388167e+10 0.012697 False                                                             
        ISP                                                      REYL & Cie S.A.      2021-05-28         2.060198e+09        CHF 2021-03-31               8.228038e+11             1.861064e+09 0.002262 False                                                             
        UNI                                                       Liberbank S.A.      2021-07-30         4.751010e+10        EUR 2021-06-30               6.569767e+10             4.751010e+10 0.723163  True                                                             
        DNB                                                          Sbanken ASA      2022-03-30         1.022736e+11        NOK                                   NaN                      NaN      NaN                            no EBA reference date before completion
        BPE                                                  Banca Carige S.p.A.      2022-06-03         2.230982e+10        EUR 2022-03-31               1.358219e+11             2.230982e+10 0.164258  True                                                             
        KBC                                        Raiffeisenbank (Bulgaria) EAD      2022-07-07         5.200000e+09        EUR 2022-06-30               3.386249e+11             5.200000e+09 0.015356 False                                                             
       HSBA                                       Silicon Valley Bank UK Limited      2023-03-13         1.149000e+10        USD                                   NaN                      NaN      NaN       UK acquirer: total assets from reports, entered in Section 3
        GLE                          LeasePlan Corporation N.V. (via ALD/Ayvens)      2023-05-22         3.452025e+10        EUR 2023-03-31               1.406657e+12             3.452025e+10 0.024541 False                                                             
        DBK                                                Numis Corporation plc      2023-10-13         6.227960e+08        GBP 2023-09-30               1.360647e+12             7.203451e+08 0.000529 False                                                             
        ISP                                                      First Bank S.A.      2024-05-31         1.500000e+09        EUR 2024-03-31               7.593786e+11             1.500000e+09 0.001975 False                                                             
        CAG                                         Banque Degroof Petercam S.A.      2024-06-04         8.129909e+09        EUR 2024-03-31               2.078287e+12             8.129909e+09 0.003912 False                                                             
       BARC                                   Tesco Bank retail banking business      2024-11-01                  NaN        GBP                                   NaN                      NaN      NaN       UK acquirer: total assets from reports, entered in Section 3
        UCG                                              Alpha Bank Romania S.A.      2024-11-04         2.357102e+10        RON 2024-09-30               8.034220e+11             4.737609e+09 0.005897 False                                                             
        NDA Danske Bank personal customer and private banking business in Norway      2024-11-18         9.000000e+09        EUR 2024-09-30               5.331477e+11             9.000000e+09 0.016881 False                                                             
        DNB                                                  Carnegie Holding AB      2025-03-06         1.632599e+10        SEK 2024-12-31               2.763934e+11             1.424731e+09 0.005155 False                                                             
        UCG                                Aion Bank SA/NV and Vodeno Sp. z o.o.      2025-03-07         1.283866e+09        EUR 2024-12-31               7.839719e+11             1.283866e+09 0.001638 False                                                             
       BAMI                            Anima Holding S.p.A. (via Banco BPM Vita)      2025-04-11         2.689939e+09        EUR 2025-03-31               1.915734e+11             2.689939e+09 0.014041 False                                                             
        NWG                             Sainsbury's Bank retail banking business      2025-05-01                  NaN        GBP                                   NaN                      NaN      NaN       UK acquirer: total assets from reports, entered in Section 3
        ABN                                  Hauck Aufhäuser Lampe Privatbank AG      2025-07-01         1.177700e+10        EUR 2025-06-30               4.142951e+11             1.177700e+10 0.028427 False                                                             
        BNP                     AXA Investment Managers (via BNP Paribas Cardif)      2025-07-01         5.100000e+09        EUR 2025-06-30               2.573934e+12             5.100000e+09 0.001981 False                                                             
        BPE                                     Banca Popolare di Sondrio S.p.A.      2025-07-18         5.662858e+10        EUR 2025-06-30               1.445282e+11             5.662858e+10 0.391817  True                                                             
       BMPS                                                    Mediobanca S.p.A.      2025-09-15         9.991165e+10        EUR 2025-06-30               1.255844e+11             9.991165e+10 0.795574  True                                                             
        KBC                                                        365.bank a.s.      2026-01-15         4.700000e+09        EUR 2025-06-30               3.565054e+11             4.700000e+09 0.013184 False                                                             
      SANUK                                                TSB Banking Group plc      2026-04-30         4.528600e+10        GBP                                   NaN                      NaN      NaN       UK acquirer: total assets from reports, entered in Section 3
```

#### the 2 rows sized this session, from `data/manual/mergers.csv`

```
BPE,UBI Banca business unit sold by Intesa Sanpaolo (branches),2021-02-22,644040000,EUR,https://group.bper.it/documents/133577364/0/21.02.19_ComSt_Accordo_Gruppo_Intesa_ENG_.pdf/37706018-c10c-0719-33bf-cc9fb050841d?t=1613760496854,79289deaf7981a4e0d54b495cb9523536b5cbaa63759b11e96059b6f3635dffe,1,consideration
BNP,AXA Investment Managers (via BNP Paribas Cardif),2025-07-01,5100000000,EUR,https://group.bnpparibas/en/press-release/bnp-paribas-cardif-completes-the-acquisition-of-axa-investment-managers,f45473228567c4c0f5022b050f0961ed0ef3afdf4b35c1cd17405ac3c7692161,1,consideration
```

### Steps 2.2 and 2.3: documents and entries

#### report_manifest.csv in full (182 documents)

```
bank_id      doc_type     period                                                           sha256    bytes pages       downloaded_utc                                                                                                                                                                                                                              url
    ABN        annual 2025-12-31 4857de6d9a62878b71065385f6cbf1c0aa1e84f1ab5d41623d16b7d17760ae2d 15874649   434 2026-11-02T16:17:20Z                                                                                      https://downloads.ctfassets.net/1u811bvgvthc/688tP3vcLbHAgEsUavbdMR/22bd74bf45996df3f6e76b0893ecc950/ABN_AMRO_Bank_-_Annual_Report_2025.pdf
    ABN     half_year 2025-06-30 379d266ce342b756c9e5346774b558bff688d7a55aca9b399556640c9c909f1a  1117462    68 2026-11-02T16:17:29Z                                                        https://assets.ctfassets.net/1u811bvgvthc/6mUVtNfRTqmDVAekBhbfXY/ca86f70b2ecdb64cc86ae5384a3606d5/ABN_AMRO_Bank_Interim_Report___Quarterly_Report_second_quarter_2025.pdf
    ABN     half_year 2026-06-30 dabc12aee705fdd72fa042938708cfc39dfa009873f9400274bdedd3d6fa7291  1139301    67 2026-11-02T16:17:30Z                                                         https://assets.ctfassets.net/1u811bvgvthc/XdAWhG6RCScxulxUI24zg/4437970f789fb52f232a0d7589427778/ABN_AMRO_Bank_Interim_Report___Quarterly_Report_second_quarter_2026.pdf
    ABN       pillar3 2024-12-31 a087a86fd781fc705c9c372512a2ad68dceb6576ed26a549952f11a5d8f50b36  6981576   286 2026-11-02T16:17:31Z                                                                                            https://assets.ctfassets.net/1u811bvgvthc/5rAPiaQlInFwlMKMjqGYyI/c740aaffc95803c6d08465d02de70503/ABN_AMRO___Pillar_3_Report_2024.pdf
    ABN       pillar3 2025-06-30 03540a74eaea01a4ffe06447cce42d6352288f51cab37ef0d5c1e3d903e570c2  1133309   121 2026-11-02T16:17:34Z                                                                          https://assets.ctfassets.net/1u811bvgvthc/39ziBx974PxxMccJFWDGxa/4696677ca102ea7cdf91dd4fc78d0aa2/ABN_AMRO_Bank_Pillar_3_Report_second_quarter_2025.pdf
    ABN       pillar3 2025-12-31 43a59832c5b19c4c9af308f2081aa11261659bc4ce783aced358de91eedad105  2673101   189 2026-11-02T16:17:35Z                                                                                       https://assets.ctfassets.net/1u811bvgvthc/6DHs3mjTrBlSb5H2ahUwf5/084cbcc8cd17f463f0067d79fa6a4c75/ABN_AMRO_Bank_-_Pillar_3_Report_2025.pdf
    ABN       pillar3 2026-06-30 e4d84de61c254ed738cd663a49b53bb99d6edddbf33dbc59454b7fcb8a41d56b  1677477    95 2026-11-02T16:17:37Z                                                                          https://assets.ctfassets.net/1u811bvgvthc/7Kv6fg3nENBr08ljcnW2yt/7ef8d274fc5f2d7e89f4dd2616f05b27/ABN_Amro_Bank_Pillar_3_Report_second_quarter_2026.pdf
   BAMI        annual 2025-12-31 b39943903faf6af9b238027d6abdabdba9c02cd7407ef27d626ccd8546aaa070 16051205   828 2026-11-02T16:35:05Z                                                                                                                                                              https://gruppo.bancobpm.it/media/dlm_uploads/Annual-Report-2025.pdf
   BAMI     half_year 2025-06-30 fb09152d33ed656bb248fdaff2311f810b9d9240666eeb0ec15d6a1a07101de9  2767152   248 2026-11-02T16:35:17Z                                                                                                                      https://gruppo.bancobpm.it/media/dlm_uploads/Consolidated-interim-financial-report-as-at-30-June-2025-1.pdf
   BAMI     half_year 2026-06-30 5503bb923b0bf528961414c455fa9d3c2cf224fe522cdfd408bb1f96e5fafa4d  2755080   246 2026-11-02T16:29:14Z                                                                                                                      https://gruppo.bancobpm.it/media/dlm_uploads/Consolidated-interim-financial-report-as-at-30-June-2026-1.pdf
   BAMI merger_target 2024-12-31 049915f5f8b264b652311a495b7f243c15c1878499dea1a2f08289bacb85897f  1961354   157 2026-11-02T16:09:30Z                                                                https://www.animasgr.it/d/EN/downloads/HoldingBilanciERelazioni/Consolidated%20Financial%20Statements%20at%2031%20December%202024%20(in%20english%20language).pdf
   BAMI       pillar3 2024-12-31 2685f119756aad5c9f05fd8fccaa4be14bfcd517d49ef34f2fd5e79ac497a37a  7801696   348 2026-11-02T16:29:47Z                                                                                                                                                   https://gruppo.bancobpm.it/media/dlm_uploads/Pillar-3-December-2024_Doc_EN.pdf
   BAMI       pillar3 2025-06-30 3ecf37e44133e9c598f8a81d7c79f6dc701fa72c01d06d6e1f7657a0cb5b5fa1  5403767   195 2026-11-02T16:31:17Z                                                                                                                                                     https://gruppo.bancobpm.it/media/dlm_uploads/P3-Giugno-2025_Documento_EN.pdf
   BAMI       pillar3 2025-12-31 c74252cae06112ff625ccbcc93f4b67d9459a0e912a12cfdb898e688d64d6039  7347008   404 2026-11-02T16:31:21Z                                                                                                                                                 https://gruppo.bancobpm.it/media/dlm_uploads/Pillar-3-BBPM-31.12.2025_Doc_EN.pdf
   BAMI       pillar3 2026-06-30 7fc32fc2a160e6c2054a510aacad17a5bd7c078506d984ca19bd52b9011eb01c  4355459   192 2026-11-02T16:31:26Z                                                                                                                           https://gruppo.bancobpm.it/media/dlm_uploads/Informativa-Pillar-3-giugno-2026_Documento_vdef_EN_v1.pdf
   BBVA        annual 2025-12-31 5a932fd4c871df1d940492611fd2055386a052b7c90cfc322d88866b5f54e3c0 24413931   725 2026-11-02T16:23:10Z                                                                                                 https://shareholdersandinvestors.bbva.com/wp-content/uploads/2026/02/5_2_BBVA_Group_Annual_Report_and_Management_Report_2025.pdf
   BBVA     half_year 2025-06-30 1d985240683aa9fbbbc5758332a29e29df3d46d3f819b390831bed3fd324d622  2388852   174 2026-11-02T16:23:23Z                                                                                                               https://shareholdersandinvestors.bbva.com/wp-content/uploads/2025/07/Interim-Consolidated-Report-June-2025_ENG.pdf
   BBVA     half_year 2026-06-30 dcb6a65e8f8dc281819d6ba9f90bc3b70afbf74088a0bf32bbbd60a5d00b29e6  3935238   179 2026-11-02T16:23:25Z                                                                                                               https://shareholdersandinvestors.bbva.com/wp-content/uploads/2026/07/ENG-Interim-Consolidated-Report-June-2026.pdf
   BBVA       pillar3 2024-12-31 5c70ff881de178cb8e0c0879404619d7e6d83aff9b66f67147a17a686ddb392c  7791864   379 2026-11-02T16:23:27Z                                                                                                                           https://shareholdersandinvestors.bbva.com/wp-content/uploads/2025/03/Pillar-3-Report-2024-BBVA_ENG.pdf
   BBVA       pillar3 2025-06-30 de4d5fda6cdbff1210bd59efbb780e7b7dfc72658941f8cb2fc3bcf70c69c1e9 13364940   215 2026-11-02T16:23:31Z                                                                                                                                    https://shareholdersandinvestors.bbva.com/wp-content/uploads/2025/09/Pillar-3-2Q-2025_ENG.pdf
   BBVA       pillar3 2025-12-31 4caaf74c922f1f155397074da8903f04e113fc276be29ff5ea1b7ef8b43d436b 10592971   441 2026-11-02T16:23:35Z                                                                                                                                    https://shareholdersandinvestors.bbva.com/wp-content/uploads/2026/05/Pillar-3-Report-2025.pdf
   BBVA       pillar3 2026-06-30 bdda3b8b8c9e9614e7080ad571e7ee47109fd211a4329ba74c529411c2fa7073  5356685   254 2026-11-02T16:23:39Z                                                                                                                                 https://shareholdersandinvestors.bbva.com/wp-content/uploads/2026/09/Pillar-3-Report-1H-2026.pdf
    BKT        annual 2025-12-31 ac77dad5439ce38bd906c36ac3ba2af5dba27fa98fe751c057dfc0f5ad00f781  8251506   438 2026-11-02T16:25:19Z                                       https://www.bankinter.com/file_source2/webcorporativa/estaticos/pdf/accionistas-e-inversores/informacion-financiera/informes-anuales/2025/ccaa_consolidadas_sostenibilidad_2025_en_web.pdf
    BKT     half_year 2026-06-30 f2545819677a2dd66722fd2efef3935870ea1b31cd735122486bab66d557ba8e  3324643    76 2026-11-02T16:25:34Z                                      https://www.bankinter.com/file_source2/webcorporativa/estaticos/pdf/accionistas-e-inversores/informacion-financiera/info-publica-periodica/2026/en_gb-informe-financiero-semestral-2026.pdf
    BKT       pillar3 2026-06-30 70b2f74c95af407ea3d778d9dbc4b983d3e9cba3b4aac7165c79641164fcdf41   286302    47 2026-11-03T11:00:18Z                                     https://www.bankinter.com/file_source2/webcorporativa/estaticos/pdf/accionistas-e-inversores/informacion-financiera/info-relevancia-prudencial/2026/pillar-3-disclosures-q2-2026-tables.xlsx
   BMPS        annual 2025-12-31 e35390a41b09f45f0a21be538499dc6f49c12186f5765627bdde73dc749552fe 11359888  1216 2026-11-02T16:31:58Z                                                                                                                                                                https://www.gruppomps.it/static/upload/ann/annual-report-2025.pdf
   BMPS     half_year 2025-06-30 84d7df338b99cc5a8eb472d8cfeda7594b99547e5c55bd8af95c4e8fc7e9fb30  4375884   145 2026-11-02T16:32:22Z                                                                                                                                          https://www.gruppomps.it/static/upload/_con/consolidate-half_yearly-report-30062025.pdf
   BMPS     half_year 2026-06-30 6fb43542d89140102c4e3be283160172b1468e70b6dd4dbf2b434ca05f025e3e  5488936   220 2026-11-02T16:32:30Z                                                                                                                                             https://www.gruppomps.it/static/upload/_con/consolidated-half-yearly-report-2026.pdf
   BMPS merger_target 2024-12-31 0d1119ccb84dcd0bb91e9842b46ff3bf4b3e0621b0e68403bc6cbe78beafbf17   868150   210 2026-11-02T16:09:37Z                                                                                                                                      https://www.mediobanca.com/static/upload_new/med/0001/mediobanca-semestrale-2024-en_def.pdf
   BMPS       pillar3 2024-12-31 68708350cc063a0305f49f64f82ff08754dcff9d3125f18485f4386efb93b43b  6119614   233 2026-11-02T16:32:36Z                                                                                                                                                 https://www.gruppomps.it/static/upload/pil/pillar-iii-report---december-2024.pdf
   BMPS       pillar3 2025-06-30 77457ff941a4dc6c7c979aea39caeaff76d2a9c79c91aa007e4fcb64d5440c94  4223157   105 2026-11-02T16:32:49Z                                                                                                                                                     https://www.gruppomps.it/static/upload/pil/pillar-iii-report---june-2025.pdf
   BMPS       pillar3 2025-12-31 5bde7cd552b4d911e8889e1c3e4ce949b4ce448cccb3530d212e6299fc5231e8  6594363   262 2026-11-02T16:32:58Z                                                                                                                                                      https://www.gruppomps.it/static/upload/pil/pillar3-report-december-2025.pdf
   BMPS       pillar3 2026-06-30 11fa0beb2ad535cc0c0693d9fd3b24cf9c89f42be8b5697983a3aa6b43d6f8a5  3837650   111 2026-11-02T16:33:10Z                                                                                                                                                        https://www.gruppomps.it/static/upload/pil/pillar3-report---june-2026.pdf
    BNP        annual 2025-12-31 65822993e7ad299d84f16bd4b495391bb670800bb9a0f301ef72e97b6f62a2e2 12235510   936 2026-11-03T10:41:07Z                                                                                                                           https://invest.bnpparibas/en/document/universal-registration-document-annual-financial-report-2025-pdf
    BNP     half_year 2025-06-30 4a9e520c9d8224f9e914dd6fde8f09fc7e50df73d8c1464a5e519a3db8d9301e 12399951   332 2026-11-03T10:41:46Z                                                                                                      https://invest.bnpparibas/en/document/2nd-amendment-to-the-2024-universal-registration-document-and-annual-financial-report
    BNP     half_year 2026-06-30 213831e3a723521ec48a99b12e19ce009ce9c97933c3a53f85240be98cba3969 14725323   316 2026-11-03T10:41:58Z                                                                                                      https://invest.bnpparibas/en/document/2nd-amendment-to-the-2025-universal-registration-document-and-annual-financial-report
    BNP merger_target 2025-07-01 f45473228567c4c0f5022b050f0961ed0ef3afdf4b35c1cd17405ac3c7692161   246870     3 2026-11-03T10:42:59Z                                                                                                                                              https://www-axa-com.cdn.prismic.io/www-axa-com/aN0fn55xUNkB1XJ6_axa_pr_20250701.pdf
    BNP       pillar3 2024-12-31 8af8bcabde1d1822c7193b26dfb2f1c41a40a159f20ae38469960244f05b48e2 17225487   952 2026-11-03T10:42:07Z                                                                                                                           https://invest.bnpparibas/en/document/universal-registration-document-annual-financial-report-2024-pdf
    BNP       pillar3 2025-06-30 4a9e520c9d8224f9e914dd6fde8f09fc7e50df73d8c1464a5e519a3db8d9301e 12399951   332 2026-11-03T10:42:39Z                                                                                                      https://invest.bnpparibas/en/document/2nd-amendment-to-the-2024-universal-registration-document-and-annual-financial-report
    BNP       pillar3 2025-12-31 65822993e7ad299d84f16bd4b495391bb670800bb9a0f301ef72e97b6f62a2e2 12235510   936 2026-11-03T10:42:46Z                                                                                                                           https://invest.bnpparibas/en/document/universal-registration-document-annual-financial-report-2025-pdf
    BNP       pillar3 2026-06-30 213831e3a723521ec48a99b12e19ce009ce9c97933c3a53f85240be98cba3969 14725323   316 2026-11-03T10:42:55Z                                                                                                      https://invest.bnpparibas/en/document/2nd-amendment-to-the-2025-universal-registration-document-and-annual-financial-report
    BPE        annual 2025-12-31 a23880a8af1feffafda72049bdc7e8e69e06c378be7909d254bbb97578666c2a 11440137  1064 2026-11-02T16:31:29Z                                                                                                                https://group.bper.it/documents/133577364/2795795058/2025+Annual+Reports.pdf/d62fc4b8-e447-b337-c81b-d518cf6d25a0
    BPE     half_year 2025-06-30 7701e4e05218c4b4b096f106c731d090d52a6ea3596917d9702ad3d5ffd5b77b  4215086   192 2026-11-02T16:31:37Z                                                                                     https://group.bper.it/documents/133577364/2795795058/Consolidated+Half-Year+Report+as+at+30+06+2025.pdf/ee8e303c-519c-d986-4655-01592227dfab
    BPE     half_year 2026-06-30 866a31842a1deb2b6b9dc1ce1088e9f876623cfafa44612e54a715342aeaf2da  5108805   184 2026-11-02T16:31:40Z                                                                              https://group.bper.it/documents/133577364/2801082007/CONSOLIDATED+INTERIM+FINANCIAL+REPORT+AT+30+JUNE+2026.pdf/aff85517-7264-dc67-1748-8f695a06bdcf
    BPE merger_target 2021-02-19 79289deaf7981a4e0d54b495cb9523536b5cbaa63759b11e96059b6f3635dffe    41568     1 2026-11-03T10:40:25Z                                                                                   https://group.bper.it/documents/133577364/0/21.02.19_ComSt_Accordo_Gruppo_Intesa_ENG_.pdf/37706018-c10c-0719-33bf-cc9fb050841d?t=1613760496854
    BPE merger_target 2021-12-31 1e30783de2e9a1fc8465e39bde90a974b8fd682b33750cf89f05b3305434791c  3927590   436 2026-11-02T16:09:39Z                                                                                                                                                            https://www.assilea.it/repository/doc/Bilanci/2021/BancaCarigeSpA.pdf
    BPE merger_target 2024-12-31 766c124b21821a3dc7829c1384361b8281075f0b57648c7c42e65994364194b4  1029171    45 2026-11-02T16:09:42Z                                                                                                                                             https://emarketstorage.it/sites/default/files/comunicati/2025-02/20250206_160405.pdf
    BPE       pillar3 2024-12-31 12215be0e00b5110f2e8c0053b88e88548379a09a21144b232b972a25c6c17aa  4660542   340 2026-11-02T16:31:44Z                                                                                           https://group.bper.it/documents/133577364/2792002788/Public+Disclosure+as+at+31+December+2024.pdf/bc60278f-2728-66a4-9e0d-63d8bde4fca6
    BPE       pillar3 2025-06-30 75539efc0c2b42ff9a25baec3f43e137c9535226f94668f673d24f91149603fd  3559008   170 2026-11-02T16:31:50Z                                                                                    https://group.bper.it/documents/133577364/2796734459/Public+Disclosure+as+at+30+June+2025+-+Pillar+3.pdf/4e345a02-0a6c-609f-eca6-4dadbbbe14c8
    BPE       pillar3 2025-12-31 6d278d08af8ebd1f11ebfd41800b635c658f397a94eda60ee129670f43d58a57  3144937   364 2026-11-02T16:31:53Z                                                                                https://group.bper.it/documents/133577364/2796734459/Public+Disclosure+as+at+31+December+2025+-+Pillar+3.pdf/718a9f07-b7d3-4eb0-bb70-bab820e0fa18
    BPE       pillar3 2026-06-30 ea79baa0e60a65b0aa46b225cb25c8e4849e704d0b5b4cdd7d33729f43054aae  2872000   172 2026-11-02T16:31:55Z                                                                                    https://group.bper.it/documents/133577364/2801082028/Public+Disclosure+as+at+30+June+2026+-+Pillar+3.pdf/85f99ea8-aca1-3351-9c0e-7ea4f3893b91
   CABK        annual 2025-12-31 dcc749c96c1ecca13ff66fa9278f8960542f1ce2cf30d9e6b3282cb1c2e04101 52540240  1179 2026-11-02T16:23:42Z                                                             https://www.caixabank.com/deployedfiles/caixabank_com/Estaticos/PDFs/Accionistasinversores/Informacion_economico_financiera/Consolidated-Annual-Financial-Report.pdf
   CABK     half_year 2025-06-30 62645c51adaf218e88a78d5c21ed56a089978ed0dca9559e2666ac2537971f1b 49145737   264 2026-11-02T16:24:01Z                                                           https://www.caixabank.com/deployedfiles/caixabank_com/Estaticos/PDFs/Accionistasinversores/Informacion_economico_financiera/Informe_Semestral_Consolidado_ING_2025.pdf
   CABK     half_year 2026-06-30 c7e6e17a291566078963e54e62d7c9f96f5c4d817c59e3a30e0f59658177a345 37210315   272 2026-11-02T16:24:16Z                                                              https://www.caixabank.com/deployedfiles/caixabank_com/Documentos/Accionistas_Inversores/Informacion_economico_financiera/Informe_Semestral_Consolidado_ENG_2026.pdf
   CABK merger_target 2020-12-31 89d03b3cfde98980e10d005e88f08af9568aa9ad496bf36693d7a57ef9cb120f  8174749   601 2026-11-02T16:09:43Z                                                                                            https://www.caixabank.com/deployedfiles/caixabank_com/Estaticos/PDFs/Accionistasinversores/consolidated-financial-statements-2020.pdf
   CABK       pillar3 2024-12-31 50379e2ac7ed66f635ecfa877cd290998cd397281d4fd86bf18b24dfbdbf4a33 17760876   507 2026-11-02T16:24:30Z                                                                             https://www.caixabank.com/deployedfiles/caixabank_com/Estaticos/PDFs/Accionistasinversores/Informacion_economico_financiera/Pillar_3_2024_Report.pdf
   CABK       pillar3 2025-06-30 48971449289c1c1718da6e8858b6b4ae02c6e36fdbb7f9be45dbeec726da67ae   371318    61 2026-11-03T10:59:54Z                                                                               https://www.caixabank.com/deployedfiles/caixabank_com/Estaticos/PDFs/Accionistasinversores/Informacion_economico_financiera/Pillar3DataJun-25.xlsx
   CABK       pillar3 2025-12-31 219948b6064e38a6d3317731980d6c75489c6e79cd34ebce4df05e1b00bfc6d7 13464323   521 2026-11-02T16:24:36Z                                                                             https://www.caixabank.com/deployedfiles/caixabank_com/Estaticos/PDFs/Accionistasinversores/Informacion_economico_financiera/Pillar_3_Report_2025.pdf
   CABK       pillar3 2026-06-30 ca75fcd067faa1fbf8d5fa01d31918d3629d5fac26c1ee35e66be1e26e4f1396   378969    61 2026-11-03T10:59:56Z                                                                               https://www.caixabank.com/deployedfiles/caixabank_com/Estaticos/PDFs/Accionistasinversores/Informacion_economico_financiera/Pillar3DataJun-26.xlsx
    CAG        annual 2025-12-31 d5cef261fb79d270d2812a39a19c8def42eb16c4e86828276502d68d961d732c 15865711  1082 2026-11-02T16:19:52Z                                                                                                                                                                             https://www.credit-agricole.com/en/pdfPreview/209967
    CAG     half_year 2025-06-30 c93b1b9b37b9b4abe8be27f3b480fa9260623fa2bd59c41e2394c936446b6403  3208572    95 2026-11-02T16:20:09Z                                                                                                                                                                             https://www.credit-agricole.com/en/pdfPreview/207491
    CAG     half_year 2026-06-30 2f262a4131bfcfc2dea25dbf9d73cb76c8e8b80d8f19295e784e26b1f133fe56  8795926   361 2026-11-02T16:20:11Z                                                                                                                                                                             https://www.credit-agricole.com/en/pdfPreview/211112
    CAG       pillar3 2024-12-31 977eda77a688dacae5bcac124b80925cb7819fac8e2453d51ca49c93ce3b7c9a  3392612   231 2026-11-02T16:20:16Z                                                                                                                                                                             https://www.credit-agricole.com/en/pdfPreview/206189
    CAG       pillar3 2025-06-30 051e8846912f3a1babbcf1d7fd6f816ab075ae1f4896de1937dae12738df7426  3320097    91 2026-11-02T16:20:22Z                                                                                                                                                                             https://www.credit-agricole.com/en/pdfPreview/207699
    CAG       pillar3 2025-12-31 fbea4477bdcc17f68b9a8b22e199c37d11ede950854710bbc00cb96257a6e5e3 10360208   405 2026-11-02T16:20:24Z                                                                                                                                                                             https://www.credit-agricole.com/en/pdfPreview/210136
    CAG       pillar3 2026-06-30 11ee1c86d9bd7ccbeb6334f6edf72ac7105349cbe1cb8a1bbe621b1c4585b8ba  3335827   177 2026-11-02T16:20:31Z                                                                                                                                                                             https://www.credit-agricole.com/en/pdfPreview/211275
    CBK        annual 2025-12-31 25b62a0e9a0ceb4b85f2923320744fa4e893c2e95d1306660bad79b8398e791f  6787584   444 2026-11-02T16:35:38Z                                                                                   https://investor-relations.commerzbank.com/media/document/630f424f-282e-4582-9276-a38357e911db/assets/Commerzbank_Group_Annual_Report_2025.pdf
    CBK     half_year 2025-06-30 8b29a471ca5ee6441257edb27fc5fa2359da10da1a37c553ef1b0f74d6b45c8d  1024136    90 2026-11-02T16:35:47Z                                                                                     https://investor-relations.commerzbank.com/media/document/32b987f7-88e5-4433-9260-233726a3d28d/assets/Commerzbank_Interim_Report_6M_2025.pdf
    CBK     half_year 2026-06-30 e159e7a1a0d76aa59891baae23ae8694ed91e0b981068840add73415162e9ab3  1064340    90 2026-11-02T16:35:49Z                                                                                     https://investor-relations.commerzbank.com/media/document/3dedc121-44ac-4ff5-80a8-d7c749860c3d/assets/Commerzbank_Interim_Report_6M_2026.pdf
 DANSKE        annual 2025-12-31 5003490703c721bd5474e1a5d3f3c60fe85835d23f545627114ced038dcaa944 13491233   286 2026-11-02T16:15:14Z                                                                                                                                          https://danskebank.com/-/media/danske-bank-com/file-cloud/2026/2/annual-report-2025.pdf
 DANSKE     half_year 2025-06-30 72d2436017d2d0fb3fe40fead95a6afc37f08df824b32b95e1b41d393a9b6829  4664974    74 2026-11-02T16:15:20Z                                                                                                                https://danskebank.com/-/media/danske-bank-com/file-cloud/2025/7/danske-bank-interim-report---first-half-2025.pdf
 DANSKE     half_year 2026-06-30 1baf0841a8fe48eff2ffe1cf741610a8b7255ba718f9285210c6f42cdddb76f8  4982624    75 2026-11-02T16:15:23Z                                                                                                                https://danskebank.com/-/media/danske-bank-com/file-cloud/2026/7/danske-bank-interim-report---first-half-2026.pdf
 DANSKE       pillar3 2024-12-31 0279099f2099dbac73d27d0d8cb1a388900bd6960406515e4f0a34233ae72853  1438720    76 2026-11-03T10:57:57Z                                                                                                                    https://danskebank.com/-/media/danske-bank-com/file-cloud/2025/2/additional-pillar-3-disclosures-q4-2024.xlsx
 DANSKE       pillar3 2025-06-30 588b4a81ba6a81d9760e6d0ab5589faeefb5f83193f8ca74bb991ec3ef0dbe6b   686080    58 2026-11-03T10:57:58Z                                                                                                                    https://danskebank.com/-/media/danske-bank-com/file-cloud/2025/7/additional-pillar-3-disclosures-q2-2025.xlsx
 DANSKE       pillar3 2025-12-31 8391f8fc7acaf448dbe0fdc9911b67254955e911a4d91212299116c2fe8b5c9a   812032    79 2026-11-03T10:57:59Z                                                                                                                    https://danskebank.com/-/media/danske-bank-com/file-cloud/2026/2/additional-pillar-3-disclosures-q4-2025.xlsx
 DANSKE       pillar3 2026-06-30 0249695f7abe5dd842b6634375f70d5d0db903ceb5b156ea0bd8bda22285a95a   924672    59 2026-11-03T10:58:00Z                                                                                                                    https://danskebank.com/-/media/danske-bank-com/file-cloud/2026/7/additional-pillar-3-disclosures-q2-2026.xlsx
    DBK        annual 2025-12-31 e0cb39de25bcbf5c3ecb493a791559326ceb249f7e2c27e7ebfebd83d05b00e3  8075373   756 2026-11-02T16:20:33Z                                                                                                                     https://investor-relations.db.com/files/documents/other-presentations-and-events/2025/Annual-Report-2025.pdf
    DBK     half_year 2025-06-30 24bbbcb3436fbe04fb8e636319435b0ecd0f92b3550a2868fe7cef85699453fb  2958422   110 2026-11-02T16:20:40Z                                                                                                                   https://investor-relations.db.com/files/documents/quarterly-results/2025/Interim-Report-as-of-June-30-2025.pdf
    DBK     half_year 2026-06-30 e08bfab8f8d2971019e47974a87e5ea031f4df52eaa64fa66e82bec6e3bcefcd  1172639   104 2026-11-02T16:20:43Z                                                                                                                   https://investor-relations.db.com/files/documents/quarterly-results/2026/Interim-Report-as-of-June-30-2026.pdf
    DBK merger_target 2022-09-30 43e693fd5a144d8395edc584602b3f25547d307bae91d65213d661debbcd73b0 17743326   140 2026-11-02T16:10:57Z                                                          https://web.archive.org/web/20240803225040id_/https://numisweb-prod-cd.azurewebsites.net/-/media/numiscorp/documents/financial-report-files/2022/annual-report-2022.pdf
    DBK       pillar3 2024-12-31 7ede18829c31fcc98ac07d69afb62b6af99f722132569d43b646018236f04548  7468385   280 2026-11-02T16:20:45Z                                                                                                                               https://investor-relations.db.com/files/documents/regulatory-reporting/Pillar-3-Report-Q4-2024.pdf
    DBK       pillar3 2025-06-30 aebac0e7012af6cdecd109b0271dccba0e24517f8b15c2a6ad72f2d1560150c1  5028661   162 2026-11-02T16:20:51Z                                                                                                                           https://investor-relations.db.com/files/documents/regulatory-reporting/2025/Pillar-3-Report-2Q2025.pdf
    DBK       pillar3 2025-12-31 c261f254d6ac82c3252caa957b1f3fb7fe8f780a1358d45d9f8adc42e180cf40  2860297   284 2026-11-02T16:20:55Z                                                                                                                           https://investor-relations.db.com/files/documents/regulatory-reporting/2025/Pillar-3-Report-Q42025.pdf
    DBK       pillar3 2026-06-30 32d8c640a5e21fd27076930c854199e58a51ff35e7ef307c0cfeb066fbb54742  1688587   164 2026-11-02T16:20:57Z                                                                                                                           https://investor-relations.db.com/files/documents/regulatory-reporting/2026/Pillar-3-Report-2Q2026.pdf
    DNB        annual 2025-12-31 929c49c76dac281ba2c10b3c04e142e4906403c7c03c12376d8b8ac3176d6e74 10019212   356 2026-11-02T16:15:02Z                                                                                                                                                                  https://www.ir.dnb.no/sites/default/files/pr/202603113411-1.pdf
    DNB     half_year 2025-06-30 4c12a153b6511a7eceeaa25952908d4c1e43dc4779f69159f253a8ee18a062bc  1141715    36 2026-11-02T16:15:09Z                                                                                                                                                                  https://www.ir.dnb.no/sites/default/files/pr/202507118454-3.pdf
    DNB     half_year 2026-06-30 fbacaea84d2c2fdb763a42975a4328bfe69b2dfb9775828ed99a083a0644039f  1110061    34 2026-11-02T16:15:10Z                                                                                                                                                                  https://www.ir.dnb.no/sites/default/files/pr/202607138455-2.pdf
    DNB       pillar3 2024-12-31 41280b1d6703b79251ccb8f0e14fc9d508dee69ac6abe4af93a98c83ce604040  1370473    80 2026-11-03T10:56:49Z                                                                                                               https://www.ir.dnb.no/sites/default/files/pr/Risk_and_capital_management_Pillar_3_attachment_%28Excel%29_4Q24.xlsx
    DNB       pillar3 2025-06-30 93c502c6dbffb2d6057de56d6450a1c7e11dfa8c7192d3b260365c1ec536ab27  1348637    84 2026-11-03T10:57:12Z                                                                                                                     https://www.ir.dnb.no/sites/default/files/pr/Risk-and-capital-management-Pillar-3-attachment-Excel-2Q25.xlsx
    DNB       pillar3 2025-12-31 67f7445e67ea69c1de175d874fc2b48c30106c668da6f3b34e48e1d250c3419e  1468789    86 2026-11-03T10:57:29Z                                                                                                               https://www.ir.dnb.no/sites/default/files/pr/Risk_and_capital_management_Pillar_3_attachment_%28Excel%29_4Q25.xlsx
    GLE        annual 2025-12-31 bd1beefb40e409300c3e20c34fb99cd97c51f7cf90dd91b5c13eb24470d7e17b  6183818   716 2026-11-02T16:19:33Z                                                                                                                   https://www.societegenerale.com/sites/default/files/documents/2026-03/universal-registration-document-2026.pdf
    GLE     half_year 2025-06-30 93389a7ddd719f61fc9a6a582757f0746db692d595d9131156efb123b4f6613b  3563252   165 2026-11-02T16:19:37Z                                                                                              https://www.societegenerale.com/sites/default/files/documents/2025-08/urd-2nd-amendment-01-08-2025-half-yearly-financial-report.pdf
    GLE     half_year 2026-06-30 474812e06404a43a922aecc6a4d5aa507690bdbca59d62f33beb97a5987f4173  3162219   166 2026-11-02T16:19:39Z                                                                                              https://www.societegenerale.com/sites/default/files/documents/2026-07/urd-2nd-amendment-31-07-2026-half-yearly-financial-report.pdf
    GLE merger_target 2022-12-31 65c0a58690b2f9306459cacb60e20e6f537f738ef1ec51a778074da85292ed6b 10009479   233 2026-11-02T16:10:04Z               https://www.ayvens.com/-/media/ayvens/public/cp/files/leaseplan-documents-and-publication-archives/white-papers-and-reports/2023/22-mar-2023-leaseplan-2022-annual-report.pdf?rev=c373f50c16c84083b79ca401e9c95dba
    GLE       pillar3 2024-12-31 c98cc70b6dd90ad8e50f49d845bca0e488666353aae1393b79449c8f389cb640  3446565   336 2026-11-02T16:19:41Z                                                                                                                                      https://www.societegenerale.com/sites/default/files/documents/2025-03/pillar-3-31122024.pdf
    GLE       pillar3 2025-06-30 9cec5d10c882d606d602f314b41f509fe513aa80e7cb2685f402f810639d1e98  2420244   166 2026-11-02T16:19:46Z                                                                                                                                      https://www.societegenerale.com/sites/default/files/documents/2025-09/pillar-3-30062025.pdf
    GLE       pillar3 2025-12-31 47dfd209029f77a9507fde9ff42911dc82d9759bcdb221709edce3f546aad2af  3136540   314 2026-11-02T16:19:48Z                                                                                                                                   https://www.societegenerale.com/sites/default/files/documents/2026-03/pillar-3-31122025-en.pdf
    GLE       pillar3 2026-06-30 80f96805167ccad1273d896d8e7b9fe46e16e46612ffe4cf4d5cd6a20a4d8f1c   828642   144 2026-11-02T16:19:51Z                                                                                                                                      https://www.societegenerale.com/sites/default/files/documents/2026-09/pillar-3-30062026.pdf
   INGA        annual 2025-12-31 a515adb27ab588ad3bef48da4afca1e9485a83869848a265e60ba954a0f5e4ea 20011936   412 2026-11-02T16:16:57Z                                                                                                                         https://www.ing.com/binaries/content/assets/documents/annual-reports/2025-ing-groep-nv-annual-report.pdf
   INGA     half_year 2025-06-30 6f655069ab598f79e63494ec6971a93addfc0f8321ad25336d2cc86db1d1cc78  1017650    68 2026-11-02T16:17:07Z                                                                                                                            https://www.ing.com/binaries/content/assets/documents/files/1h2025_interim_accounts_ing_groep_n.v.pdf
   INGA     half_year 2026-06-30 f0c1f440600860ab54b24c0aa5dbd3c94e4b8a11e8f2e67f7c20f66405865a23  1975452    65 2026-11-02T16:17:08Z                                                                                                                  https://www.ing.com/binaries/content/assets/documents/results/2q2026/1h2026-interim-accounts-ing-groep-n.v..pdf
   INGA       pillar3 2024-12-31 24b1a80acccbca3eea2937402949986953d8678a35bb48c828e69bdae8f957af  1561271   129 2026-11-02T16:17:09Z                                                                                                          https://www.ing.com/binaries/content/assets/documents/annual-reports/2024-ing-groep-nv-additional-pillar-iii-report.pdf
   INGA       pillar3 2025-06-30 0d0d77134dc830a2b99c3f43788e5bb804a1d58b19756f8ce92ce5ab0b8b89e1   768179    62 2026-11-03T10:58:22Z                                                                                                                          https://www.ing.com/binaries/content/assets/documents/files/2q2025-ing-group-pillar-iii-disclosures.xls
   INGA       pillar3 2025-12-31 bb732c3b4ef56ef16eaf8d6b0467dfc32b87085fee89376088e7ab045d8cffb1  5559164   190 2026-11-02T16:17:12Z                                                                                                          https://www.ing.com/binaries/content/assets/documents/annual-reports/2025-ing-groep-nv-additional-pillar-iii-report.pdf
   INGA       pillar3 2026-06-30 198bf9c4c9505c770b7d3c63382328caba653ee59e2d286a65cf1dbbc5a6c804  8229786    82 2026-11-02T16:17:16Z                                                                                                           https://www.ing.com/binaries/content/assets/documents/results/2q2026/2q2026-ing-group-additional-pillar-iii-report.pdf
    ISP        annual 2025-12-31 e29cff37844188bbc7ddb5a124b7867c5c6d9c253cf3c37fe1550926c3981c4c 13715164  1126 2026-11-02T16:27:39Z                                                                                https://group.intesasanpaolo.com/content/dam/portalgroup/repository-documenti/investor-relations/bilanci-relazioni-en/2025/2025_Annual_Report.pdf
    ISP     half_year 2025-06-30 21ec2df3b141095c09cffa34a6affa6107618241e116f5aaaa85dc4d2d009986  7430418   266 2026-11-02T16:27:57Z                                                                       https://group.intesasanpaolo.com/content/dam/portalgroup/repository-documenti/investor-relations/bilanci-relazioni-en/2025/30062025_Half-yearly_report.pdf
    ISP     half_year 2026-06-30 1c6ac5db2259ab6dc31fff49d1b9b878069afa7fc0d6bce690c338e5b23dcc82  7090896   270 2026-11-02T16:28:02Z                                                                       https://group.intesasanpaolo.com/content/dam/portalgroup/repository-documenti/investor-relations/bilanci-relazioni-en/2026/30062026_Half-yearly_report.pdf
    ISP       pillar3 2024-12-31 78a73f06d36c087855619aaf21092549b20d7654539d47ea1d57475982b1fd46  5715539   390 2026-11-02T16:28:06Z                                                            https://group.intesasanpaolo.com/content/dam/portalgroup/repository-documenti/investor-relations/Contenuti/RISORSE/Documenti%20PDF/en_governance/31122024_Pillar3.pdf
    ISP       pillar3 2025-06-30 5c3f76dff15ad7a832295d9866e98bd419799a6615d7a8759c4d0ff034127387  3137570   184 2026-11-02T16:28:11Z                                                            https://group.intesasanpaolo.com/content/dam/portalgroup/repository-documenti/investor-relations/Contenuti/RISORSE/Documenti%20PDF/en_governance/30062025_Pillar3.pdf
    ISP       pillar3 2025-12-31 57bac352dc538475ba859d4613189f5e4a0ef4de8d4832097f0f19719004fc90  5258681   388 2026-11-02T16:28:14Z                                                            https://group.intesasanpaolo.com/content/dam/portalgroup/repository-documenti/investor-relations/Contenuti/RISORSE/Documenti%20PDF/en_governance/31122025_Pillar3.pdf
    ISP       pillar3 2026-06-30 0961e247b5e3c3b9939206929d874774cf032e9a847507a20ee7276b3e38727a  4821989   174 2026-11-02T16:28:22Z                                                                  https://group.intesasanpaolo.com/content/dam/portalgroup/repository-documenti/investor-relations/Contenuti/RISORSE/Documenti%20PDF/Pillar3/Pillar3_30062026.pdf
    KBC        annual 2025-12-31 8140183eb1d03106183dbe1d4c291493fc7286281518b5b4b5d33fb830f688b6 16634083   432 2026-11-02T16:17:38Z                                                                                                                           https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/Results/jvs-2025/jvs-2025-gr-en.pdf
    KBC     half_year 2025-06-30 a0cb5fc721ea59da90d627306a7e977cb6b105d7cc811bbccfeed2c80a7d44c7  2163352    62 2026-11-02T16:17:47Z                                                                                                                 https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/Results/2q2025/2q2025-quarterly-report-en.pdf
    KBC     half_year 2026-06-30 aa09c68c7770571ac95d402d98730308d3440b38ae285958507b023d588ae210  2833004    64 2026-11-02T16:17:49Z                                                                                                                 https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/Results/2q2026/2q2026-quarterly-report-en.pdf
    KBC       pillar3 2024-12-31 9436747e53b2fd9f85bfeee98bef60c2617988368ffd4e5d1f46e54ffd53ae81  2461670    80 2026-11-03T10:58:25Z                                                                                                                       https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/3-Reports/20251020-pillar-3-4q2024.xlsx
    KBC       pillar3 2025-06-30 c0b89fbd4f654bd2937d5742b85e490eb5a932adc35be8aa088269204b4ccca7  1739598    56 2026-11-03T10:58:55Z                                                                                                                     https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/3-Reports/20251020-pillar-3-2q2025-2.xlsx
    KBC       pillar3 2025-12-31 e510fa79b1ade9c949f190ded60cda2f6428ed4bc7dd591cd7d3b84ff0c41dda  2637167    81 2026-11-03T10:59:09Z                                                                                                                       https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/3-Reports/20261030-pillar-3-4q2025.xlsx
    KBC       pillar3 2026-06-30 efef9b045c2529b1d5b3a333d2f42c347f73938b442e2b7e7f780dfc461e05ed  2469514    57 2026-11-03T10:59:27Z                                                                                                                       https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/3-Reports/20260904-pillar-3-2q2026.xlsx
    NDA        annual 2025-12-31 cce7c2004fbeca8b652ea9977be08500c1297c0cd307349bd016c1dc4de11e1e 16126401   378 2026-11-02T16:14:38Z                                                                                                                                                                      https://www.nordea.com/en/doc/nordea-annual-report-2025.pdf
    NDA     half_year 2025-06-30 2b182482997fc52d5a9afd5885ba22c6abc7dc22eb97cb7b85ec83624982ee5f  2601717    60 2026-11-02T16:14:51Z                                                                                                                                                             https://www.nordea.com/en/doc/interim-report-second-quarter-2025.pdf
    NDA     half_year 2026-06-30 507954f1ddb8941fafb841ac374b6c80beb975084dcd9dfb31d1274fcf071a02  6187598    62 2026-11-02T16:14:53Z                                                                                                                                                      https://www.nordea.com/en/doc/interim-report-second-quarter-2026-nordea.pdf
    NDA       pillar3 2024-12-31 bd58f8a6f73615f70ec27e13a37afe8e176585e9645aae359bde8c09ff243bf6  3368991   185 2026-11-02T16:14:55Z                                                                                                                                           https://www.nordea.com/en/doc/nordea-group-capital-and-risk-management-report-2024.pdf
    NDA       pillar3 2025-06-30 6dbff1cccce5d76068011b4e08f26fdf6215ea1dc89bb84e70d1867172a8d46b  1815643    73 2026-11-02T16:14:58Z                                                                                                                                        https://www.nordea.com/en/doc/nordea-group-capital-and-risk-management-report-q2-2025.pdf
    NDA       pillar3 2025-12-31 98b38ec2fb33c648f490a164d842ef1013851ae1554cc65815d10cda864a596a  3395909   187 2026-11-02T16:14:59Z                                                                                                                                         https://www.nordea.com/en/doc/nordea-group-capital-and-risk-management-report-2025-0.pdf
    NDA       pillar3 2026-06-30 db2a2ec98167ddd757bae1b653539a8328615751671284eaa93b5c7c57a2ac4c  1934464    70 2026-11-02T16:15:01Z                                                                                                                                        https://www.nordea.com/en/doc/nordea-group-capital-and-risk-management-report-q2-2026.pdf
   RABO        annual 2025-12-31 101675489ee13d6f97dd821f30352987f2d9d9ee5d969a18d6e2330487baedc8 17864343   425 2026-11-02T16:17:53Z                                                                                                                                     https://media.rabobank.com/asset/a35a8d2d-dbcf-4145-ba0a-7c9f2841d052/Annual-Report-2025.pdf
   RABO     half_year 2025-06-30 8a59ccf1288c214e4cdc9c181f4b337a47a9b7f28f7b3df48f8df6580f2e93c1  6409352    69 2026-11-02T16:18:02Z                                                                                                                                    https://media.rabobank.com/asset/f9f3987e-793a-48c8-ad43-ebcea191a969/Interim-Report-2025.pdf
   RABO     half_year 2026-06-30 1658385c45d5d5e50e913377dfe3bebf67f6abf441b72456a8c6c8b8c1f10f9a 13965795    70 2026-11-02T16:18:05Z                                                                                                                                    https://media.rabobank.com/asset/d0357317-6836-4a94-b712-eaa80371941e/Interim-Report-2026.pdf
   RABO       pillar3 2024-12-31 4edc63f8d2844f21b6db031e4ce9b41fa62a9a1d06244a2d7bceb0d81167e60a  2555782   190 2026-11-02T16:18:09Z                                                                                                                              https://media.rabobank.com/asset/d497b21d-d38d-40f9-8844-dcdd905d0a93/Pillar-3-Year-Report-2024.pdf
   RABO       pillar3 2025-06-30 4e60ed39ac4b164a6756dd365900d3b63c373732f730fa38a7e4a3c94ec04091  1168130    94 2026-11-02T16:18:11Z                                                                                                                                https://media.rabobank.com/asset/cca418be-008e-4f35-a74e-187241fd501f/Pillar-3-Report-2025-Q2.pdf
   RABO       pillar3 2025-12-31 ada908a519de8dbaaf8b3a7b91093ca3f51447fc8688eaccb6d911825079556a  1892219   168 2026-11-02T16:18:12Z                                                                                                                              https://media.rabobank.com/asset/77fd2f28-2a75-4b98-8e00-f7628e97f01f/Pillar-3-Year-Report-2025.pdf
   RABO       pillar3 2026-06-30 e057fb2e5e6030271989d3f7a9202a01bc6ffd19db5d409d0f975f6677bed236  1282038   102 2026-11-02T16:18:13Z                                                                                                                                https://media.rabobank.com/asset/9f881ef7-f80c-4cc7-934a-14333f9e9cc6/Pillar-3-Report-2026-Q2.pdf
    SAB        annual 2025-12-31 1d79279deb726a989ef2dba8e9ad64deea1adebf7d4ecdbe6927c86fe5a57730 38517943   697 2026-11-02T16:24:42Z                                                                                                                          https://www.grupbancsabadell.com/corp/files/6000333945830/annual_accounts_banco_sabadell_group_2025.pdf
    SAB     half_year 2025-06-30 9f715acb2a5f72ddc76599230aa5b5ea05f61ab3d45fa6fda751f880c0a0f8fc  1003599   131 2026-11-02T16:24:55Z                                                                                                               https://www.grupbancsabadell.com/corp/files/6000283590595/half_yearly_additional_financial_accounts_junio_2025.pdf
    SAB     half_year 2026-06-30 d3d043bb36facdb5281fcc802d6a53b7ae662a2915490359308cd28755554766  1024962   128 2026-11-02T16:24:57Z                                                                                                                https://www.grupbancsabadell.com/corp/files/6000363284975/half_yearly_additional_financial_accounts_june_2026.pdf
    SAB       pillar3 2024-12-31 4f4a13bd2a9088f7444e7aeb19c6543eee0bcb234429b5c14f212e2637234f08 18176730   423 2026-11-02T16:24:59Z                                                                                                                               https://www.grupbancsabadell.com/corp/files/6000252950050/en_pillariiidisclosures_bsgroup_2024.pdf
    SAB       pillar3 2025-06-30 40c2f61b565077180d145384ad66de643c1f2e277cd31b19977deaeb15bdf163   697489    62 2026-11-03T10:59:58Z                                                                                                                                             https://www.grupbancsabadell.com/corp/files/6000293693221/bs_irp_-_2025_2t_-_en.xlsx
    SAB       pillar3 2025-12-31 271e5c6cf51af263719151a4b021303f8fd069f6a4a26d4d60f8f44fe55ee767 33440729   442 2026-11-02T16:25:07Z                                                                                                                               https://www.grupbancsabadell.com/corp/files/6000340525667/en_pillariiidisclosures_bsgroup_2025.pdf
    SAB       pillar3 2026-06-30 75414db98ca35f56482c2ed2a8bd92f0e02e2e19617150c30f4254d6216445ee   746282    63 2026-11-03T11:00:01Z                                                                                                                                                   https://www.grupbancsabadell.com/corp/files/6000375089198/gbs_p3r_2026_q2.xlsx
    SAN        annual 2025-12-31 b02503bc72b3fd115386eca4e4467340d49b576253e8eb0d973de7fcfe118bf9 39600962   910 2026-11-02T16:22:03Z                                                                             https://www.santander.com/content/dam/santander-com/en/documentos/informe-financiero-anual/2025/ifa-2025-consolidated-annual-financial-report-en.pdf
    SAN     half_year 2025-06-30 5b3e8b579199b53ccf281d55b81763de8e166dd38c983287f4428a788b1763c6  7176517   208 2026-11-02T16:22:31Z                                      https://www.santander.com/content/dam/santander-com/en/documentos/informacion-sobre-resultados-semestrales-y-anuales-suministrada-a-la-sec/2025/sec-half-yearly-6-k-2025-fiscal-year-en.pdf
    SAN     half_year 2026-06-30 d072554d21c19db1dd4e28a12236b4cd10b84ae618a7f4d0b53e9b698ccc1be6  5980839   204 2026-11-02T16:22:36Z                                      https://www.santander.com/content/dam/santander-com/en/documentos/informacion-sobre-resultados-semestrales-y-anuales-suministrada-a-la-sec/2026/sec-half-yearly-6-k-2026-fiscal-year-en.pdf
    SAN       pillar3 2024-12-31 e5fd99979edd556bc1ca6cb64b99d660ffb952b63d1e8562de517e59812e258e 29640239   356 2026-11-02T16:22:39Z                                                                                                https://www.santander.com/content/dam/santander-com/en/documentos/informe-con-relevancia-prudencial/2024/irp-2024-irp-2024-en.pdf
    SAN       pillar3 2025-06-30 5cf09da14cd7adb6ca8ffb0f32bc1150457ced77b65268c64af0020a80c26d06 21858054   185 2026-11-02T16:22:53Z                                                                                            https://www.santander.com/content/dam/santander-com/en/documentos/informe-con-relevancia-prudencial/2025/irp-2025-Informe-2Q25-en.pdf
    SAN       pillar3 2025-12-31 4e33969a931125feea15623adb20cd5e52310e9149a778747c97836e19dbf94c 16783051   367 2026-11-02T16:23:00Z                                                                                                https://www.santander.com/content/dam/santander-com/en/documentos/informe-con-relevancia-prudencial/2025/irp-2025-irp-2025-en.pdf
    SAN       pillar3 2026-06-30 7d32df63d600302cb671bcaf047bbfcb0da2d2489afec42132cdbe7c9d020c80  9535494   189 2026-11-02T16:23:06Z                                                                                     https://www.santander.com/content/dam/santander-com/en/documentos/informe-con-relevancia-prudencial/2026/Santander_P3_2Q_2026_EN_v260831.pdf
    SEB        annual 2025-12-31 1bf07071afbab0269914a1a78d16e4e840e73e5efbe901af97b148d288b28083 14348731   350 2026-11-02T16:15:27Z                                                                                                     https://webapp.sebgroup.com/mb/mblib.nsf/alldocsbyunid/1C740093062958DDC1258DAE003DFAF7/$FILE/SEB_Annual_Report_2025_ENG.pdf
    SEB     half_year 2025-06-30 795c080b9966783368d0c3851f1a9e365d0ebe094295631745388775d97313d1   635098    52 2026-11-02T16:15:41Z                                                                                                          https://webapp.sebgroup.com/mb/mblib.nsf/alldocsbyunid/CFB4D728F35C4D3BC1258CC90018DB6A/$FILE/Q225_Quarterly_report.pdf
    SEB     half_year 2026-06-30 1c4ec9153ae6f40cad026879a5438654f843d728edf5b0e621ab160400147ded   690710    57 2026-11-02T16:15:42Z                                                                                                          https://webapp.sebgroup.com/mb/mblib.nsf/alldocsbyunid/E37F46ABC876FBADC1258E350018C72D/$FILE/Q226_Quarterly_report.pdf
    SEB       pillar3 2024-12-31 270728aea4319b649e5f1678401a07392f8f777d6c2752f75b305e2f212e31ad  2176150   129 2026-11-02T16:15:43Z                                                                                                  https://webapp.sebgroup.com/mb/mblib.nsf/alldocsbyunid/B45D3671B8E00C66C1258C490040ABB1/$FILE/cap_adequacy_seb_pillar3_2024.pdf
    SEB       pillar3 2025-06-30 37efc15c202eb67ca07ee685b9a9da0623d06eafe52b139070d7eaacc9e8413a   434340    54 2026-11-03T10:58:00Z                                                                                                       https://webapp.sebgroup.com/mb/mblib.nsf/alldocsbyunid/251456EC17C911C6C1258CC800373A83/$FILE/Pillar_3_tables_2025_Q2.xlsx
    SEB       pillar3 2025-12-31 996ae1dfdbe484cfee27a496d26054b17c51b6689ab84f4e04125d92e2f1f26b  1579788   113 2026-11-02T16:15:45Z                                                                                                        https://webapp.sebgroup.com/mb/mblib.nsf/alldocsbyunid/823997216F4EE08EC1258DBD002B9B86/$FILE/Pillar_3_tables_2025_Q4.pdf
    SEB       pillar3 2026-06-30 0f889290b29f56e75880ac5efb42a64f9e8c8141ab5a9454cdef74a904874944   234165    56 2026-11-03T10:58:02Z                                                                                                    https://webapp.sebgroup.com/mb/mblib.nsf/alldocsbyunid/81EB34F3D6595730C1258E3700396BE2/$FILE/Pillar_3_SEB_Group_Q2_2026.xlsx
    SHB        annual 2025-12-31 3b757bc166dedc47211dcfd6ffdc4c1da60c3dc034613dc654fe7005b1b6c148  5504887   352 2026-11-02T16:15:47Z                                                                                                                                                                              https://mb.cision.com/Main/3555/4313527/3954484.pdf
    SHB     half_year 2025-06-30 db337294e89c8feb0d9b205bf01afe03a4b084a467d0b17487728f5c2ca500e1   919868    67 2026-11-02T16:15:53Z                                                                                                                                                                              https://mb.cision.com/Main/3555/4207558/3581803.pdf
    SHB     half_year 2026-06-30 7983c15f2ab05af94a1c50b7220a89eb0571294c60b2c05d2360fce395ae0b26   883076    65 2026-11-02T16:15:54Z                                                                                                                                                                              https://mb.cision.com/Main/3555/4374686/4192694.pdf
    SHB       pillar3 2024-12-31 dd21c17ebab547222bd26cc33cae07919a59aa8884dfd08233aa041bd6902f8f  3051488   111 2026-11-02T16:15:55Z                                                                                                             https://storage.mfn.se/a/handelsbanken/98f8d9b9-60ae-4a36-8be2-c34713842cda/pillar-3-disclosures-pdf-annual-2024.pdf
    SHB       pillar3 2025-06-30 e564981691862ebb3434d2aa858cecb97b58cc359ba8bfb1fa7e3fd55e422a5c   297361    49 2026-11-03T10:58:04Z                                                                                                    https://storage.mfn.se/a/handelsbanken/1423ee80-cb8b-4be7-9d9f-91a179653520/pillar-203-20-xlsx-20-20interim-20-2025-20q2.xlsx
    SHB       pillar3 2025-12-31 1d3f71fab3c4e00373bbef549e7b335da3c5c5962f089eb65641b464746cece4 25634443   116 2026-11-02T16:16:00Z                                                                                                             https://storage.mfn.se/a/handelsbanken/ce9b5313-6d37-486c-89fc-582ae5ce34ad/pillar-3-disclosures-pdf-annual-2025.pdf
   SWED        annual 2025-12-31 d16afc74c782c77ccee2384423119d36d2687be5aa5ef33d56107740fe133dba 11234146   340 2026-11-02T16:16:17Z                                                                                                                                https://internetbank.swedbank.se/ConditionsEarchive/download?bankid=1111&id=WEBDOC-PRODE277903288
   SWED     half_year 2025-06-30 fd7458f5148948d722a6dc7f5faa15e18eae40b121e31fccb3ec744fb5f7d60a  5002284    58 2026-11-02T16:16:33Z                                                                                                                                https://internetbank.swedbank.se/ConditionsEarchive/download?bankid=1111&id=WEBDOC-PRODE234709540
   SWED     half_year 2026-06-30 8f41044f33a350646c2fd6c1da5cb52faaaa40fa20174caf178b40282f9b3904  5363968    62 2026-11-02T16:16:38Z                                                                                                                                https://internetbank.swedbank.se/ConditionsEarchive/download?bankid=1111&id=WEBDOC-PRODE307024995
   SWED       pillar3 2024-12-31 03f97ed60bfa8d7c84e47fd03aa19ae1e4d0a8fd12613240261dc4d29740156c  6760282   117 2026-11-02T16:16:44Z                                                                                                                                https://internetbank.swedbank.se/ConditionsEarchive/download?bankid=1111&id=WEBDOC-PRODE221684981
   SWED       pillar3 2025-06-30 614137b8f0e228b90e93ddb82ff1413ec4a9b343fb2d7fcf7a8d90328fcb9f4f  1455933    56 2026-11-02T16:16:51Z                                                                                                                                https://internetbank.swedbank.se/ConditionsEarchive/download?bankid=1111&id=WEBDOC-PRODE248869515
   SWED       pillar3 2025-12-31 f5657b3ebebe821efbd554cc3135f3b4f64a7dd4dc5e79e3733f20e7f559c2b3  1840378   120 2026-11-02T16:16:54Z                                                                                                                                https://internetbank.swedbank.se/ConditionsEarchive/download?bankid=1111&id=WEBDOC-PRODE278025941
   SWED       pillar3 2026-06-30 9a772e41705146d0157bec409b8b05b9e89b62225e836ef673abeddbd7d5614b  1475998    59 2026-11-03T10:58:14Z                                                                     https://errp.eba.europa.eu/public-documents/P3NONREMDISDOCS/input/M312WZV08Y7LYUC71685.CON_SE_PILLAR3010000_P3NONREMDISDOCS_2026-06-30_20260831092202363.zip
    UCG        annual 2025-12-31 96e7dc76b48f18a9a7c3effc6da36c5048aed335ca9083699126c086d1749893 23723704  1044 2026-11-02T16:27:09Z                                                                              https://www.unicreditgroup.eu/content/dam/unicreditgroup-eu/documents/en/investors/financial-reports/2025/4q25/2025-Annual-Reports-and-Accounts.pdf
    UCG     half_year 2025-06-30 b553b47884f5bb16f0239abc4ff6527bea86b7cc092392bc1cf31099e9ee1572  3054783   278 2026-11-02T16:27:24Z                                                   https://www.unicreditgroup.eu/content/dam/unicreditgroup-eu/documents/en/investors/financial-reports/2025/2q25/Consolidated-First-Half-Financial-Report-as-at-30-June-2025.pdf
    UCG     half_year 2026-06-30 5ac973eadb63348116180598412798a238fbe3d5bc97bacaefe9a5128804d83f  3277561   276 2026-11-02T16:27:26Z                                                   https://www.unicreditgroup.eu/content/dam/unicreditgroup-eu/documents/en/investors/financial-reports/2026/2q26/Consolidated-first-half-financial-report-as-at-30-June-2026.pdf
    UCG merger_target 2023-12-31 bacb44c8e0a5730cd152a429083cd39c3934c654d4442901517080a38480988a  2220716   157 2026-11-02T16:11:21Z                                                                                       https://www.alpha.gr/-/media/AlphaHoldings/Files/group/oikonomikes-katastaseis-etairion-omilou/2023/2023-ABR-IFRS-Financial-Statements.pdf
    UCG       pillar3 2024-12-31 9b1909bbb036c2f15f8d63d802442326dc3b8d2aa17947e602ca623c85916491  5921433   263 2026-11-02T16:27:28Z                                                      https://www.unicreditgroup.eu/content/dam/unicreditgroup-eu/documents/en/investors/third-pillar-basel/2024/UniCredit-Group-Disclosure-Pillar-III-as-at-31-December-2024.pdf
    UCG       pillar3 2025-06-30 99bb9654df6f1c06008add9c3dbc00ae8912acdf52fa2f71a4a2e538d4b1348c  4095527   169 2026-11-02T16:27:31Z                                                          https://www.unicreditgroup.eu/content/dam/unicreditgroup-eu/documents/en/investors/third-pillar-basel/2025/UniCredit-Group-Disclosure-Pillar-III-as-at-30-June-2025.pdf
    UCG       pillar3 2025-12-31 d121ec30f12b3127b537b5141f44d826ad91e899c5755a4614ab95a399d06f98  5456464   304 2026-11-02T16:27:33Z                                                      https://www.unicreditgroup.eu/content/dam/unicreditgroup-eu/documents/en/investors/third-pillar-basel/2025/UniCredit-Group-Disclosure-Pillar-III-as-at-31-December-2025.pdf
    UNI        annual 2025-12-31 b470722a2008eaf2d786343c7f755a096e6650948a4906f80ed9baa86c8b98fa 31234619   966 2026-11-02T16:25:44Z                                          https://www.unicajabanco.com/content/dam/unicaja/unicaja-corporacion/documentos-corporacion/inversores-y-accionistas/cuentas-anuales-auditadas/cuentas-anuales-consolidadas-2025-en.pdf
    UNI     half_year 2025-06-30 98f7a370f90e73a7e3aaff2408be5473691afc06f494a3ae8a4ea21f4e8e00c0  4812357   202 2026-11-02T16:26:02Z                              https://www.unicajabanco.com/content/dam/unicaja/unicaja-corporacion/documentos-corporacion/inversores-y-accionistas/informacion-semestral/2025-06-estados-financieros-intermedios-resumidos-en.pdf
    UNI     half_year 2026-06-30 f5231756a3c8140887627bd8ae5c7ec87e530a88b3e07e653f6db23339e91537  9917844   206 2026-11-02T16:26:15Z                              https://www.unicajabanco.com/content/dam/unicaja/unicaja-corporacion/documentos-corporacion/inversores-y-accionistas/informacion-semestral/2026-06-estados-financieros-intermedios-resumidos-en.pdf
    UNI merger_target 2020-12-31 2a3b0df0f556b391f068928bf60b5efc68bcf9a887817f8e68f7194b5697fb2d 28552408  1077 2026-11-02T16:10:17Z https://www.unicajabanco.com/content/dam/unicaja/unicaja-corporacion/documentos-corporacion/junta-general-de-accionistas/2021-extraordinaria/2021-extraordinaria-Cuentas-anuales-individuales-consolidadas-liberbank-2020-en.pdf
    UNI       pillar3 2024-12-31 fe8f5de4a7e67bb14d42df0e7fd41be5117ea02edf74d80cce8cfc719be03ddc  7162464   275 2026-11-02T16:26:28Z                                                 https://www.unicajabanco.com/content/dam/unicaja/unicaja-corporacion/documentos-corporacion/inversores-y-accionistas/informacion-relevancia-prudencial/2024-informe-anual-en.pdf
    UNI       pillar3 2025-06-30 a42079b8f44e35f8f49e4ecc5bdf98a268ab79fd80d2ad806e0f75de16cca2b2  1975231    46 2026-11-03T11:00:19Z                                               https://www.unicajabanco.com/content/dam/unicaja/unicaja-corporacion/documentos-corporacion/inversores-y-accionistas/informacion-relevancia-prudencial/2025-segundo-trimestre.xlsx
    UNI       pillar3 2025-12-31 a18359e4f9bcdc2b8fe7435c694b04315631141f0960735bceb973846a31216b  2746865   245 2026-11-02T16:26:49Z                                                 https://www.unicajabanco.com/content/dam/unicaja/unicaja-corporacion/documentos-corporacion/inversores-y-accionistas/informacion-relevancia-prudencial/2025-informe-anual-en.pdf
    UNI       pillar3 2026-06-30 28c2ac237807e8efa7f732849c1ec67a9a815f4f5ffdb59f0d288aced2bc560d  1802654    46 2026-11-03T11:00:48Z                                               https://www.unicajabanco.com/content/dam/unicaja/unicaja-corporacion/documentos-corporacion/inversores-y-accionistas/informacion-relevancia-prudencial/2026-segundo-trimestre.xlsx
```

#### documents in report_urls.csv not downloaded (11), with the URL tried and the note

```
bank_id  doc_type     period                                                                                                                                                                                         url                                                                                                                    note
    DNB   pillar3 2026-06-30                                                                                                    https://edap-public.eba.europa.eu/ExternalLinks/index?id=Mg==&rhversion=20260423085052-2                                         No bank-hosted file; DNB states 2Q26 Pillar 3 is only via EBA Pillar 3 Data Hub
    SHB   pillar3 2026-06-30                                                                                                              https://edap-public.eba.europa.eu/Report/index/MTE1?rhversion=20260706134722-2                                      No bank-hosted file for Q2 2026; handelsbanken.com points to EBA Pillar 3 Data Hub
    CBK   pillar3 2024-12-31                                                                                                                               https://investor-relations.commerzbank.com/disclosure-report/                                                      IR site is JS-rendered (EQS API); direct PDF link not discoverable
    CBK   pillar3 2025-06-30                                                                                                                               https://investor-relations.commerzbank.com/disclosure-report/                                                      IR site is JS-rendered (EQS API); direct PDF link not discoverable
    CBK   pillar3 2025-12-31                                                                                                                               https://investor-relations.commerzbank.com/disclosure-report/ Main PDF not found; only ESG annex found (media/document/be38c909-f7cd-41bb-89cd-200eb7cd619c/assets/Annex_4_-_ESG.pdf)
    CBK   pillar3 2026-06-30                                                                                                                               https://investor-relations.commerzbank.com/disclosure-report/                                                Listed on IR reports page (11 Sep 2026) but direct link not discoverable
    BKT half_year 2025-06-30 https://www.bankinter.com/file_source2/webcorporativa/estaticos/pdf/accionistas-e-inversores/informacion-financiera/info-publica-periodica/2025/en_gb-informe-financiero-semestral-2025.pdf                                                 Guessed from 2026 naming pattern; unconfirmed; site returns 403 to curl
    BKT   pillar3 2024-12-31                                                                               https://www.bankinter.com/webcorporativa/en/shareholders-investors/financial-information/pillar-3-disclosures                                              File link is on the page's 2024 year tab; not retrievable (bot protection)
    BKT   pillar3 2025-06-30                                                                               https://www.bankinter.com/webcorporativa/en/shareholders-investors/financial-information/pillar-3-disclosures                                File link is on the page's 2025 year tab; not retrievable (bot protection); likely Excel
    BKT   pillar3 2025-12-31                                                                               https://www.bankinter.com/webcorporativa/en/shareholders-investors/financial-information/pillar-3-disclosures                           2025 Prudential Relevance Report published 26 Mar 2026; link not retrievable (bot protection)
    UCG   pillar3 2026-06-30                                                                                                                               https://edap-public.eba.europa.eu/ExternalLinks/index?id=Mg==          Not on bank site: from 31-Mar-2026 UCG publishes Pillar 3 only on EBA Pillar 3 Data Hub (EDAP) per CRR art.434
```

#### entries per bank, universe order (5589 entries)

```
bank_id  entries
    NDA      216
    DNB      188
 DANSKE      201
    SEB      202
    SHB      179
   SWED      216
   INGA      205
    ABN      220
    KBC      213
   RABO      232
    BNP      213
    GLE      233
    CAG      218
    DBK      233
    CBK      128
    SAN      261
   BBVA      253
   CABK      249
    SAB      241
    BKT      143
    UNI      242
    UCG      188
    ISP      221
   BAMI      248
    BPE      225
   BMPS      221
```

#### NDA: entries per field and date

```
                    field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
           admin_expenses           2           2           2           2
          at1_instruments           1           1           1           1
                  cash_cb           1           1           1           1
                     cet1           0           1           1           1
      cet1_ratio_reported           0           1           1           1
          debt_securities           2           2           2           2
       deposits_customers           1           1           1           1
             depreciation           1           1           1           1
   gains_held_for_trading           1           1           1           1
          impairments_fin           1           1           1           1
    intangibles_deduction           1           1           1           1
         interest_expense           1           1           1           1
          interest_income           2           2           2           2
                      lcr           0           0           1           1
        leverage_exposure           0           1           1           1
                loans_all           2           2           2           2
loans_customers_allowance           8           8           8           8
    loans_customers_gross           8           8           8           8
   loans_households_gross           2           2           2           2
     lr1_scope_adjustment           0           1           0           0
         lr1_total_assets           0           1           0           0
                 net_fees           1           1           1           1
            npl_allowance           1           1           1           1
                npl_gross           1           1           1           1
                     nsfr           0           0           1           1
      other_operating_net           3           3           3           3
                      pat           1           1           1           1
                      pbt           1           1           1           1
            profit_owners           2           2           2           1
   resolution_dgs_contrib           1           1           1           1
                      rwa           0           1           1           1
                    tier1           0           1           1           1
             total_assets           1           1           1           1
             total_equity           1           1           1           1
        total_liabilities           1           1           1           1
   total_operating_income           1           1           1           1
```

#### DNB: entries per field and date

```
                    field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
           admin_expenses           3           2           3           2
          at1_instruments           1           1           1           0
                  cash_cb           1           1           1           1
                     cet1           0           1           1           0
      cet1_ratio_reported           0           1           1           0
          debt_securities           2           2           2           0
       deposits_customers           1           1           1           1
             depreciation           1           1           1           1
   gains_held_for_trading           1           1           1           1
          impairments_fin           1           1           1           1
    intangibles_deduction           1           1           1           0
         interest_expense           1           2           1           2
          interest_income           1           2           1           2
                      lcr           0           0           1           0
        leverage_exposure           0           1           1           0
                loans_all           2           2           2           0
loans_customers_allowance           8           8           8           0
    loans_customers_gross           8           8           8           0
   loans_households_gross           2           2           2           0
     lr1_scope_adjustment           0           1           0           0
         lr1_total_assets           0           1           0           0
                 net_fees           1           2           1           2
            npl_allowance           1           1           1           0
                npl_gross           1           1           1           0
                     nsfr           0           0           1           0
      other_operating_net           2           4           2           4
                      pat           2           2           2           2
                      pbt           1           1           1           1
            profit_owners           2           2           2           2
                      rwa           0           1           1           0
                    tier1           0           1           1           0
             total_assets           1           1           1           1
             total_equity           1           1           1           1
        total_liabilities           1           1           1           1
   total_operating_income           1           1           1           1
```

#### DANSKE: entries per field and date

```
                    field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
           admin_expenses           1           1           1           1
          at1_instruments           1           1           1           1
                  cash_cb           1           1           1           1
                     cet1           0           1           1           1
      cet1_ratio_reported           0           1           1           1
          debt_securities           2           2           2           2
       deposits_customers           1           1           1           1
   gains_held_for_trading           1           1           1           1
          impairments_fin           1           1           1           1
    intangibles_deduction           1           1           1           1
         interest_expense           1           1           1           1
          interest_income           2           2           2           2
                      lcr           0           0           1           1
        leverage_exposure           0           1           1           1
                loans_all           2           2           2           2
loans_customers_allowance           8           8           8           8
    loans_customers_gross           8           8           8           8
   loans_households_gross           2           2           2           2
     lr1_scope_adjustment           0           1           0           0
         lr1_total_assets           0           1           0           0
                 net_fees           1           1           1           1
            npl_allowance           1           1           1           1
                npl_gross           1           1           1           1
                     nsfr           0           0           1           1
      other_operating_net           2           2           2           2
                      pat           1           1           1           1
                      pbt           1           1           1           1
            profit_owners           1           1           1           1
                      rwa           0           1           1           1
                    tier1           0           1           1           1
             total_assets           1           1           1           1
             total_equity           1           1           1           1
        total_liabilities           1           1           1           1
   total_operating_income           1           1           1           1
           trading_assets           1           1           1           1
```

#### SEB: entries per field and date

```
                    field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
           admin_expenses           2           2           2           2
          at1_instruments           1           1           1           1
                  cash_cb           1           1           1           1
                     cet1           0           1           1           1
      cet1_ratio_reported           0           1           1           1
          debt_securities           2           2           2           2
       deposits_customers           1           1           1           1
             depreciation           1           1           1           1
   gains_held_for_trading           1           1           1           1
          impairments_fin           1           1           1           1
       impairments_nonfin           0           0           1           0
    intangibles_deduction           1           1           1           1
         interest_expense           1           1           1           1
          interest_income           1           1           1           1
                      lcr           0           0           1           1
        leverage_exposure           0           1           1           1
                loans_all           2           2           2           2
loans_customers_allowance           8           8           8           8
    loans_customers_gross           8           8           8           8
   loans_households_gross           2           2           2           2
     lr1_scope_adjustment           0           1           0           0
         lr1_total_assets           0           1           0           0
                 net_fees           1           1           1           1
            npl_allowance           1           1           1           1
                npl_gross           1           1           1           1
                     nsfr           0           0           1           1
      other_operating_net           1           1           1           1
                      pat           1           1           1           1
                      pbt           1           1           1           1
            profit_owners           1           1           1           1
   resolution_dgs_contrib           1           1           1           1
                      rwa           0           1           1           1
                    tier1           0           1           1           1
             total_assets           1           1           1           1
             total_equity           1           1           1           1
        total_liabilities           1           1           1           1
   total_operating_income           1           1           1           1
```

#### SHB: entries per field and date

```
                    field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
           admin_expenses           2           2           2           2
          at1_instruments           1           1           1           0
                  cash_cb           1           1           1           1
                     cet1           0           1           1           0
      cet1_ratio_reported           0           1           1           0
          debt_securities           2           2           2           0
       deposits_customers           1           1           1           1
             depreciation           1           1           1           1
          dividend_income           1           1           1           1
   gains_held_for_trading           1           1           1           1
          impairments_fin           1           1           1           1
    intangibles_deduction           1           0           1           0
         interest_expense           1           1           1           1
          interest_income           1           1           1           1
                      lcr           0           0           1           0
        leverage_exposure           0           1           1           0
                loans_all           2           2           2           0
loans_customers_allowance           8           8           8           0
    loans_customers_gross           8           8           8           0
   loans_households_gross           2           2           2           0
     lr1_scope_adjustment           0           1           0           0
         lr1_total_assets           0           1           0           0
                 net_fees           1           1           1           1
            npl_allowance           1           1           1           0
                npl_gross           1           1           1           0
                     nsfr           0           0           1           0
      other_operating_net           3           3           3           3
                      pat           1           1           1           1
                      pbt           1           1           1           1
            profit_owners           1           1           1           1
   resolution_dgs_contrib           1           1           1           1
                      rwa           0           1           1           0
                    tier1           0           1           1           0
             total_assets           1           1           1           1
             total_equity           1           1           1           1
        total_liabilities           1           1           1           1
   total_operating_income           1           1           1           1
```

#### SWED: entries per field and date

```
                    field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
           admin_expenses           2           2           3           3
          at1_instruments           1           1           1           1
                  cash_cb           1           1           1           1
                     cet1           0           1           1           1
      cet1_ratio_reported           0           1           1           1
          debt_securities           2           2           2           2
       deposits_customers           1           1           1           1
             depreciation           1           1           1           1
   gains_held_for_trading           1           1           1           1
          impairments_fin           1           1           1           1
       impairments_nonfin           2           1           1           1
    intangibles_deduction           1           1           1           1
         interest_expense           1           1           1           1
          interest_income           1           1           1           1
                      lcr           0           0           1           1
        leverage_exposure           0           1           1           1
                loans_all           2           2           2           2
loans_customers_allowance           8           8           8           8
    loans_customers_gross           8           8           8           8
   loans_households_gross           2           2           2           2
     lr1_scope_adjustment           0           1           0           0
         lr1_total_assets           0           1           0           0
                 net_fees           1           1           1           1
            npl_allowance           1           1           1           1
                npl_gross           1           1           1           1
                     nsfr           0           0           1           1
      other_operating_net           3           3           3           3
                      pat           1           1           1           1
                      pbt           1           1           1           1
            profit_owners           1           1           1           1
   resolution_dgs_contrib           1           1           1           1
                      rwa           0           1           1           1
                    tier1           0           1           1           1
             total_assets           1           1           1           1
             total_equity           1           1           1           1
        total_liabilities           1           1           1           1
   total_operating_income           1           1           1           1
```

#### INGA: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           2           2           2           2
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           2           2
           deposits_customers           1           1           1           1
gains_derecognition_not_fvtpl           1           0           1           0
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
        intangibles_deduction           1           1           1           1
             interest_expense           1           1           1           1
              interest_income           1           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
         lr1_scope_adjustment           0           1           0           0
             lr1_total_assets           0           1           0           0
                     net_fees           1           1           1           1
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           4           2           4           2
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
            total_liabilities           1           1           1           1
       total_operating_income           1           1           1           1
               trading_assets           1           0           1           0
```

#### ABN: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           2           2           2           2
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           2           2
           deposits_customers           1           4           1           1
                 depreciation           1           1           1           1
gains_derecognition_not_fvtpl           1           1           1           1
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
        intangibles_deduction           1           1           1           1
             interest_expense           2           2           2           2
              interest_income           2           2           2           2
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
         lr1_scope_adjustment           0           1           0           0
             lr1_total_assets           0           1           0           0
                     net_fees           1           1           1           1
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           2           2           2           2
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
            total_liabilities           1           1           1           1
       total_operating_income           1           1           1           1
               trading_assets           1           1           1           1
```

#### KBC: entries per field and date

```
                    field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
           admin_expenses           1           1           1           1
          at1_instruments           1           1           1           1
                  cash_cb           1           1           1           1
                     cet1           0           1           1           1
      cet1_ratio_reported           0           1           1           1
          debt_securities           2           2           2           2
       deposits_customers           1           1           1           1
          dividend_income           1           1           1           1
   gains_held_for_trading           1           1           1           1
          impairments_fin           1           1           1           1
       impairments_nonfin           2           2           2           2
    intangibles_deduction           1           1           1           1
         interest_expense           1           1           1           1
          interest_income           1           1           1           1
                      lcr           0           0           1           1
        leverage_exposure           0           1           1           1
                loans_all           2           2           2           2
loans_customers_allowance           8           8           8           8
    loans_customers_gross           8           8           8           8
   loans_households_gross           2           2           2           2
     lr1_scope_adjustment           0           1           0           0
         lr1_total_assets           0           1           0           0
                 net_fees           1           1           1           1
            npl_allowance           1           1           1           1
                npl_gross           1           1           1           1
                     nsfr           0           0           1           1
      other_operating_net           3           3           3           3
                      pat           1           1           1           1
                      pbt           1           1           1           1
            profit_owners           1           1           1           1
                      rwa           0           1           1           1
                    tier1           0           1           1           1
             total_assets           1           1           1           1
             total_equity           1           1           1           1
        total_liabilities           1           1           1           1
   total_operating_income           1           1           1           1
           trading_assets           1           1           1           1
```

#### RABO: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           2           2           2           2
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           2           2
           deposits_customers           1           1           1           1
                 depreciation           1           1           1           1
gains_derecognition_not_fvtpl           2           2           2           0
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
           impairments_nonfin           1           0           0           0
        intangibles_deduction           1           1           1           1
             interest_expense           1           1           1           1
              interest_income           2           2           2           2
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
         lr1_scope_adjustment           0           1           0           0
             lr1_total_assets           0           1           0           0
                     net_fees           1           1           1           1
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           3           3           3           3
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           3           3           3           3
       resolution_dgs_contrib           1           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
            total_liabilities           1           1           1           1
       total_operating_income           1           1           1           1
               trading_assets           1           1           1           1
```

#### BNP: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           1           1           1           1
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           2           2
           deposits_customers           1           1           1           1
                 depreciation           1           1           1           1
gains_derecognition_not_fvtpl           2           2           2           2
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
        intangibles_deduction           1           1           1           1
             interest_expense           1           1           1           1
              interest_income           1           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
         lr1_scope_adjustment           0           1           0           0
             lr1_total_assets           0           1           0           0
                     net_fees           2           2           2           2
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           3           3           3           3
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
            total_liabilities           1           1           1           1
       total_operating_income           1           1           1           1
```

#### GLE: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           1           1           1           1
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           2           2
           deposits_customers           1           1           1           1
                 depreciation           1           1           1           1
gains_derecognition_not_fvtpl           2           2           2           2
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
        intangibles_deduction           1           1           1           1
             interest_expense           1           1           1           1
              interest_income           1           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
         lr1_scope_adjustment           0           1           0           0
             lr1_total_assets           0           1           0           0
                     net_fees           2           2           2           2
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           8           8           8           8
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
            total_liabilities           1           1           1           1
       total_operating_income           1           1           1           1
```

#### CAG: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           2           2
           deposits_customers           1           1           1           1
                 depreciation           1           1           1           1
              dividend_income           1           1           1           1
gains_derecognition_not_fvtpl           2           2           2           2
       gains_designated_fvtpl           1           1           1           1
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
           impairments_nonfin           1           0           0           0
             interest_expense           1           1           1           1
              interest_income           1           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
         lr1_scope_adjustment           0           1           0           0
             lr1_total_assets           0           1           0           0
                     net_fees           2           2           2           2
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           3           3           3           3
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
            total_liabilities           1           1           1           1
       total_operating_income           1           1           1           1
               trading_assets           1           1           1           1
```

#### DBK: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           2           2           2           2
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           2           2
           deposits_customers           1           1           1           1
gains_derecognition_not_fvtpl           2           2           2           2
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
        intangibles_deduction           1           1           1           1
             interest_expense           1           1           1           1
              interest_income           1           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
         lr1_scope_adjustment           0           1           0           0
             lr1_total_assets           0           1           0           0
                     net_fees           1           1           1           1
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           2           2           2           2
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
            total_liabilities           1           1           1           1
       total_operating_income           7           7           7           7
               trading_assets           1           1           1           1
```

#### CBK: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           1           1           1           1
                      cash_cb           1           1           1           1
           deposits_customers           4           0           4           0
              dividend_income           1           1           1           1
gains_derecognition_not_fvtpl           2           2           2           2
       gains_hedge_accounting           1           1           1           1
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
             interest_expense           1           1           1           1
              interest_income           1           1           1           1
                     net_fees           1           1           1           1
          other_operating_net           2           2           2           2
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
       resolution_dgs_contrib           1           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
       total_operating_income          10          10          10          10
               trading_assets           1           1           1           1
```

#### SAN: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           2           2           2           2
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           2           2
           deposits_customers           3           3           3           3
                 depreciation           1           1           1           1
              dividend_income           1           1           1           1
         exchange_differences           1           1           1           1
gains_derecognition_not_fvtpl           1           1           1           1
       gains_designated_fvtpl           2           2           2           2
       gains_hedge_accounting           1           1           1           1
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
           impairments_nonfin           1           1           1           1
        intangibles_deduction           1           1           1           1
             interest_expense           1           1           1           1
              interest_income           1           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
         lr1_scope_adjustment           0           1           0           0
             lr1_total_assets           0           1           0           0
                     net_fees           2           2           2           2
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           5           5           5           5
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
                   provisions           1           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
            total_liabilities           1           1           1           1
       total_operating_income           1           1           1           1
               trading_assets           1           1           1           1
```

#### BBVA: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           2           2           2           2
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           2           2
           deposits_customers           1           1           1           1
                 depreciation           1           1           1           1
              dividend_income           1           1           1           1
         exchange_differences           1           1           1           1
gains_derecognition_not_fvtpl           1           1           1           1
       gains_designated_fvtpl           1           1           1           1
       gains_hedge_accounting           1           1           1           1
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
           impairments_nonfin           1           1           1           1
        intangibles_deduction           1           1           1           1
             interest_expense           1           1           1           1
              interest_income           1           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
         lr1_scope_adjustment           0           1           0           0
             lr1_total_assets           0           1           0           0
                     net_fees           2           2           2           2
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           6           6           6           6
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
                   provisions           1           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
            total_liabilities           1           1           1           1
       total_operating_income           1           1           1           1
               trading_assets           1           1           1           1
```

#### CABK: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           2           2           2           2
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           2           2
           deposits_customers           1           1           1           1
                 depreciation           1           1           1           1
              dividend_income           1           1           1           1
         exchange_differences           1           1           1           1
gains_derecognition_not_fvtpl           1           1           1           1
       gains_designated_fvtpl           1           1           1           1
       gains_hedge_accounting           1           1           1           1
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
           impairments_nonfin           1           1           1           1
        intangibles_deduction           1           1           1           1
             interest_expense           1           1           1           1
              interest_income           1           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
         lr1_scope_adjustment           0           1           0           0
             lr1_total_assets           0           1           0           0
                     net_fees           2           2           2           2
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           5           5           5           5
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
                   provisions           1           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
            total_liabilities           1           1           1           1
       total_operating_income           1           1           1           1
               trading_assets           1           1           1           1
```

#### SAB: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           2           2           2           2
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           2           2
           deposits_customers           1           1           1           1
                 depreciation           1           1           1           1
              dividend_income           1           1           1           1
         exchange_differences           1           1           1           1
gains_derecognition_not_fvtpl           1           1           1           1
       gains_hedge_accounting           1           1           1           1
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
           impairments_nonfin           1           1           1           1
        intangibles_deduction           1           1           1           1
             interest_expense           1           1           1           1
              interest_income           1           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
         lr1_scope_adjustment           0           1           0           0
             lr1_total_assets           0           1           0           0
                     net_fees           2           2           2           2
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           4           4           4           4
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
                   provisions           1           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
            total_liabilities           1           1           1           1
       total_operating_income           1           1           1           1
               trading_assets           1           1           1           1
```

#### BKT: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           2           2           2           2
              at1_instruments           0           0           0           1
                      cash_cb           1           0           1           1
                         cet1           0           0           0           1
          cet1_ratio_reported           0           0           0           1
              debt_securities           0           0           0           2
           deposits_customers           1           0           1           1
                 depreciation           1           1           1           1
              dividend_income           1           1           1           1
         exchange_differences           1           1           1           1
gains_derecognition_not_fvtpl           1           1           1           1
       gains_hedge_accounting           1           1           1           1
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
           impairments_nonfin           1           1           1           1
        intangibles_deduction           0           0           0           1
             interest_expense           1           1           1           1
              interest_income           1           1           1           1
                          lcr           0           0           0           1
            leverage_exposure           0           0           0           1
                    loans_all           0           0           0           2
    loans_customers_allowance           0           0           0           8
        loans_customers_gross           0           0           0           8
       loans_households_gross           0           0           0           2
                     net_fees           2           2           2           2
                npl_allowance           0           0           0           1
                    npl_gross           0           0           0           1
                         nsfr           0           0           0           1
          other_operating_net           4           4           4           4
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
                   provisions           1           1           1           1
                          rwa           0           0           0           1
                        tier1           0           0           0           1
                 total_assets           1           0           1           1
                 total_equity           1           0           1           1
            total_liabilities           1           0           1           1
       total_operating_income           1           1           1           1
               trading_assets           1           0           1           1
```

#### UNI: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           2           2           2           2
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           0           2           2           2
           deposits_customers           1           0           1           0
                 depreciation           1           1           1           1
              dividend_income           1           1           1           1
         exchange_differences           1           1           1           1
gains_derecognition_not_fvtpl           1           1           1           1
       gains_hedge_accounting           1           1           1           1
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
           impairments_nonfin           1           1           1           1
        intangibles_deduction           1           1           1           1
             interest_expense           1           1           1           1
              interest_income           1           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           0           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
         lr1_scope_adjustment           0           1           0           0
             lr1_total_assets           0           1           0           0
                     net_fees           2           2           2           2
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           6           6           6           6
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
                   provisions           1           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           0           1           1
            total_liabilities           1           1           1           1
       total_operating_income           1           1           1           1
               trading_assets           1           1           1           1
```

#### UCG: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           2           2           2           2
              at1_instruments           1           1           1           0
                      cash_cb           1           1           1           1
                         cet1           0           1           1           0
          cet1_ratio_reported           0           1           1           0
              debt_securities           2           2           2           0
           deposits_customers           1           1           1           1
                 depreciation           2           2           2           2
              dividend_income           1           1           1           1
gains_derecognition_not_fvtpl           1           1           1           1
       gains_designated_fvtpl           1           1           1           1
       gains_hedge_accounting           1           1           1           1
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
        intangibles_deduction           1           1           1           0
             interest_expense           1           1           1           1
              interest_income           1           1           1           1
                          lcr           0           0           1           0
            leverage_exposure           0           1           1           0
                    loans_all           2           2           2           0
    loans_customers_allowance           8           8           8           0
        loans_customers_gross           8           8           8           0
       loans_households_gross           2           2           2           0
         lr1_scope_adjustment           0           1           0           0
             lr1_total_assets           0           1           0           0
                     net_fees           1           1           1           1
                npl_allowance           1           1           1           0
                    npl_gross           1           1           1           0
                         nsfr           0           0           1           0
          other_operating_net           1           1           1           1
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
                   provisions           1           1           1           1
                          rwa           0           1           1           0
                        tier1           0           1           1           0
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
       total_operating_income           1           1           1           1
               trading_assets           1           1           1           1
```

#### ISP: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           2           2           2           2
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           2           2
           deposits_customers           1           1           1           1
                 depreciation           2           2           2           2
              dividend_income           1           1           1           1
gains_derecognition_not_fvtpl           1           1           1           1
       gains_designated_fvtpl           1           1           1           1
       gains_hedge_accounting           1           1           1           1
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
        intangibles_deduction           1           1           1           1
             interest_expense           1           1           1           1
              interest_income           1           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
         lr1_scope_adjustment           0           1           0           0
             lr1_total_assets           0           1           0           0
                     net_fees           1           1           1           1
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           1           1           1           1
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
                   provisions           1           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
       total_operating_income           1           1           1           1
               trading_assets           1           1           1           1
```

#### BAMI: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           2           2           2           2
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           2           2
           deposits_customers           1           1           1           1
                 depreciation           2           2           2           2
              dividend_income           1           1           1           1
gains_derecognition_not_fvtpl           1           1           1           1
       gains_designated_fvtpl           1           1           1           1
       gains_hedge_accounting           1           1           1           1
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
           impairments_nonfin           0           0           1           0
        intangibles_deduction           1           1           1           1
             interest_expense           1           1           1           1
              interest_income           1           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
         lr1_scope_adjustment           0           1           0           0
             lr1_total_assets           0           1           0           0
                     net_fees           1           1           1           1
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           1           1           1           1
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
                   provisions           1           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           8           7           8           7
       total_operating_income           1           1           1           1
               trading_assets           1           1           1           1
```

#### BPE: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           2           2           2           2
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           2           2
           deposits_customers           1           1           1           1
                 depreciation           2           2           2           2
              dividend_income           1           1           1           1
gains_derecognition_not_fvtpl           1           1           1           1
       gains_designated_fvtpl           1           1           1           1
       gains_hedge_accounting           1           1           1           1
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
        intangibles_deduction           1           1           1           1
             interest_expense           1           1           1           1
              interest_income           1           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
         lr1_scope_adjustment           0           1           0           0
             lr1_total_assets           0           1           0           0
                     net_fees           1           1           1           1
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           1           1           1           1
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
                   provisions           1           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           2           2           2           2
       total_operating_income           1           1           1           1
               trading_assets           1           1           1           1
```

#### BMPS: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           2           2           2           2
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           2           2
           deposits_customers           1           1           1           1
                 depreciation           2           2           2           2
              dividend_income           1           1           1           1
gains_derecognition_not_fvtpl           1           1           1           1
       gains_designated_fvtpl           1           1           1           1
       gains_hedge_accounting           1           1           1           1
       gains_held_for_trading           1           1           1           1
              impairments_fin           1           1           1           1
        intangibles_deduction           1           1           1           1
             interest_expense           1           1           1           1
              interest_income           1           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
         lr1_scope_adjustment           0           1           0           0
             lr1_total_assets           0           1           0           0
                     net_fees           1           1           1           1
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           1           1           1           1
                          pat           1           1           1           1
                          pbt           1           1           1           1
                profit_owners           1           1           1           1
                   provisions           1           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
       total_operating_income           1           1           1           1
               trading_assets           1           1           1           1
```

#### zero cells entered under B.4 (79), per bank

```
bank_id  zero_rows
    NDA          4
    DNB         12
    SEB          4
    SHB         12
   SWED         12
   INGA          4
    ABN         11
   RABO          5
    GLE          2
    BKT          2
    UNI          6
    BPE          1
   BMPS          4
```

### Step 2.4: provenance, seams and the scope gate

#### provenance (check 1) on report_entries.csv: 5589 of 5589 passed (100.00%)

```
bank_id  passed  rows
    NDA     216   216
    DNB     188   188
 DANSKE     201   201
    SEB     202   202
    SHB     179   179
   SWED     216   216
   INGA     205   205
    ABN     220   220
    KBC     213   213
   RABO     232   232
    BNP     213   213
    GLE     233   233
    CAG     218   218
    DBK     233   233
    CBK     128   128
    SAN     261   261
   BBVA     253   253
   CABK     249   249
    SAB     241   241
    BKT     143   143
    UNI     242   242
    UCG     188   188
    ISP     221   221
   BAMI     248   248
    BPE     225   225
   BMPS     221   221
```

#### provenance rows that failed

```
none
```

#### provenance on mergers.csv rows sized from a hashed document

```
bank_id   ref_date      value_a  passed                                                                                               note
    BPE 2021-02-22 6.440400e+08    True UBI Banca business unit sold by Intesa Sanpaolo (branches); 79289deaf798@1; printed at scale 1e+06
   CABK 2021-03-26 2.098419e+11    True                                                Bankia S.A.; 89d03b3cfde9@15; printed at scale 1000
    UNI 2021-07-30 4.751010e+10    True                                             Liberbank S.A.; 2a3b0df0f556@33; printed at scale 1000
    BPE 2022-06-03 2.230982e+10    True                                        Banca Carige S.p.A.; 1e30783de2e9@76; printed at scale 1000
    GLE 2023-05-22 3.452025e+10    True               LeasePlan Corporation N.V. (via ALD/Ayvens); 65c0a58690b2@118; printed at scale 1000
    DBK 2023-10-13 6.227960e+08    True                                     Numis Corporation plc; 43e693fd5a14@121; printed at scale 1000
    UCG 2024-11-04 2.357102e+10    True                                    Alpha Bank Romania S.A.; bacb44c8e0a5@11; printed at scale 1000
   BAMI 2025-04-11 2.689939e+09    True                  Anima Holding S.p.A. (via Banco BPM Vita); 049915f5f8b2@38; printed at scale 1000
    BNP 2025-07-01 5.100000e+09    True           AXA Investment Managers (via BNP Paribas Cardif); f45473228567@1; printed at scale 1e+09
    BPE 2025-07-18 5.662858e+10    True                           Banca Popolare di Sondrio S.p.A.; 766c124b2182@40; printed at scale 1000
   BMPS 2025-09-15 9.991165e+10    True                                          Mediobanca S.p.A.; 0d1119ccb84d@58; printed at scale 1000
```

#### entry FACTS rejected by the source map

```
none
```

#### seam 1 (check 7) at 2025-06-30 in full (72 rows, 72 passed; value_a eba EUR, value_b p3 in EUR)

```
         check bank_id   ref_date             field      value_a      value_b     diff_abs     diff_rel  threshold  passed                   note
7_seam_capital     ABN 2025-06-30              cet1 2.032130e+10 2.032100e+10 2.993825e+05 1.473245e-05      0.001    True      p3 EUR 2.0321e+10
7_seam_capital     ABN 2025-06-30 leverage_exposure 4.489414e+11 4.489410e+11 3.704166e+05 8.250891e-07      0.001    True     p3 EUR 4.48941e+11
7_seam_capital     ABN 2025-06-30               rwa 1.397895e+11 1.397890e+11 4.764839e+05 3.408582e-06      0.001    True     p3 EUR 1.39789e+11
7_seam_capital    BAMI 2025-06-30              cet1 9.098563e+09 9.099000e+09 4.367260e+05 4.799945e-05      0.001    True      p3 EUR 9099000000
7_seam_capital    BAMI 2025-06-30 leverage_exposure 2.148043e+11 2.148040e+11 2.800890e+05 1.303927e-06      0.001    True     p3 EUR 2.14804e+11
7_seam_capital    BAMI 2025-06-30               rwa 6.427977e+10 6.428000e+10 2.335930e+05 3.634005e-06      0.001    True       p3 EUR 6.428e+10
7_seam_capital    BBVA 2025-06-30              cet1 5.163361e+10 5.163400e+10 3.930000e+05 7.611322e-06      0.001    True      p3 EUR 5.1634e+10
7_seam_capital    BBVA 2025-06-30 leverage_exposure 8.247687e+11 8.247690e+11 2.560000e+05 3.103900e-07      0.001    True     p3 EUR 8.24769e+11
7_seam_capital    BBVA 2025-06-30               rwa 3.870507e+11 3.870510e+11 3.140000e+05 8.112633e-07      0.001    True     p3 EUR 3.87051e+11
7_seam_capital    BMPS 2025-06-30              cet1 8.996382e+09 8.996382e+09 9.800000e+01 1.089327e-08      0.001    True      p3 EUR 8996382000
7_seam_capital    BMPS 2025-06-30 leverage_exposure 1.300503e+11 1.300503e+11 2.190000e+02 1.683964e-09      0.001    True  p3 EUR 1.30050308e+11
7_seam_capital    BMPS 2025-06-30               rwa 4.586403e+10 4.586403e+10 5.000000e+01 1.090179e-09      0.001    True    p3 EUR 4.586403e+10
7_seam_capital     BNP 2025-06-30              cet1 9.828056e+10 9.828100e+10 4.355710e+05 4.431914e-06      0.001    True      p3 EUR 9.8281e+10
7_seam_capital     BNP 2025-06-30 leverage_exposure 2.604850e+12 2.604850e+12 2.307903e+05 8.860023e-08      0.001    True     p3 EUR 2.60485e+12
7_seam_capital     BNP 2025-06-30               rwa 7.888496e+11 7.888500e+11 4.445627e+05 5.635582e-07      0.001    True      p3 EUR 7.8885e+11
7_seam_capital     BPE 2025-06-30              cet1 9.017502e+09 9.018000e+09 4.976420e+05 5.518623e-05      0.001    True      p3 EUR 9018000000
7_seam_capital     BPE 2025-06-30 leverage_exposure 1.498945e+11 1.498940e+11 4.958750e+05 3.308160e-06      0.001    True     p3 EUR 1.49894e+11
7_seam_capital     BPE 2025-06-30               rwa 5.559721e+10 5.559700e+10 2.092290e+05 3.763300e-06      0.001    True      p3 EUR 5.5597e+10
7_seam_capital    CABK 2025-06-30              cet1 2.962480e+10 2.962480e+10 2.770000e+02 9.350275e-09      0.001    True   p3 EUR 2.9624796e+10
7_seam_capital    CABK 2025-06-30 leverage_exposure 6.182813e+11 6.182813e+11 1.670000e+02 2.701036e-10      0.001    True  p3 EUR 6.18281257e+11
7_seam_capital    CABK 2025-06-30               rwa 2.418353e+11 2.418353e+11 3.710000e+02 1.534102e-09      0.001    True  p3 EUR 2.41835281e+11
7_seam_capital     CAG 2025-06-30              cet1 1.141072e+11 1.141070e+11 2.489029e+05 2.181306e-06      0.001    True     p3 EUR 1.14107e+11
7_seam_capital     CAG 2025-06-30 leverage_exposure 2.190715e+12 2.190715e+12 3.458753e+04 1.578824e-08      0.001    True    p3 EUR 2.190715e+12
7_seam_capital     CAG 2025-06-30               rwa 6.490132e+11 6.490130e+11 1.823094e+05 2.809025e-07      0.001    True     p3 EUR 6.49013e+11
7_seam_capital  DANSKE 2025-06-30              cet1 2.017178e+10 2.017178e+10 4.577637e-05 2.269327e-15      0.001    True   p3 DKK 1.5049962e+11
7_seam_capital  DANSKE 2025-06-30 leverage_exposure 4.469787e+11 4.469787e+11 1.831055e-04 4.096514e-16      0.001    True  p3 DKK 3.33486342e+12
7_seam_capital  DANSKE 2025-06-30               rwa 1.080310e+11 1.080310e+11 8.697510e-04 8.050943e-15      0.001    True p3 DKK 8.060081214e+11
7_seam_capital     DBK 2025-06-30              cet1 4.852157e+10 4.852200e+10 4.270570e+05 8.801384e-06      0.001    True      p3 EUR 4.8522e+10
7_seam_capital     DBK 2025-06-30 leverage_exposure 1.276035e+12 1.276035e+12 4.939135e+04 3.870689e-08      0.001    True    p3 EUR 1.276035e+12
7_seam_capital     DBK 2025-06-30               rwa 3.408051e+11 3.408050e+11 6.175261e+04 1.811963e-07      0.001    True     p3 EUR 3.40805e+11
7_seam_capital     DNB 2025-06-30              cet1 1.749476e+10 1.749476e+10 6.484985e-05 3.706816e-15      0.001    True p3 NOK 2.070417368e+11
7_seam_capital     DNB 2025-06-30 leverage_exposure 3.091777e+11 3.091777e+11 1.226807e-02 3.967966e-14      0.001    True  p3 NOK 3.65896358e+12
7_seam_capital     DNB 2025-06-30               rwa 9.544277e+10 9.544277e+10 3.779587e+00 3.960056e-11      0.001    True  p3 NOK 1.12951748e+12
7_seam_capital     GLE 2025-06-30              cet1 5.253584e+10 5.253600e+10 1.550066e+05 2.950493e-06      0.001    True      p3 EUR 5.2536e+10
7_seam_capital     GLE 2025-06-30 leverage_exposure 1.405566e+12 1.405566e+12 3.395824e+05 2.415984e-07      0.001    True    p3 EUR 1.405566e+12
7_seam_capital     GLE 2025-06-30               rwa 3.880294e+11 3.880290e+11 4.110051e+05 1.059211e-06      0.001    True     p3 EUR 3.88029e+11
7_seam_capital    INGA 2025-06-30              cet1 4.453403e+10 4.453403e+10 0.000000e+00 0.000000e+00      0.001    True  p3 EUR 4.45340324e+10
7_seam_capital    INGA 2025-06-30 leverage_exposure 1.186761e+12 1.186761e+12 0.000000e+00 0.000000e+00      0.001    True p3 EUR 1.186760545e+12
7_seam_capital    INGA 2025-06-30               rwa 3.358038e+11 3.358038e+11 0.000000e+00 0.000000e+00      0.001    True p3 EUR 3.358037788e+11
7_seam_capital     ISP 2025-06-30              cet1 4.001800e+10 4.001800e+10 4.091000e+03 1.022290e-07      0.001    True      p3 EUR 4.0018e+10
7_seam_capital     ISP 2025-06-30 leverage_exposure 8.237507e+11 8.237510e+11 2.941290e+05 3.570607e-07      0.001    True     p3 EUR 8.23751e+11
7_seam_capital     ISP 2025-06-30               rwa 3.085076e+11 3.085080e+11 3.978640e+05 1.289641e-06      0.001    True     p3 EUR 3.08508e+11
7_seam_capital     KBC 2025-06-30              cet1 1.813809e+10 1.813809e+10 1.000000e+00 5.513261e-11      0.001    True p3 EUR 1.813808528e+10
7_seam_capital     KBC 2025-06-30 leverage_exposure 3.800482e+11 3.800482e+11 0.000000e+00 0.000000e+00      0.001    True  p3 EUR 3.80048211e+11
7_seam_capital     KBC 2025-06-30               rwa 1.243149e+11 1.243149e+11 0.000000e+00 0.000000e+00      0.001    True p3 EUR 1.243148569e+11
7_seam_capital     NDA 2025-06-30              cet1 2.396494e+10 2.396500e+10 5.516792e+04 2.302026e-06      0.001    True      p3 EUR 2.3965e+10
7_seam_capital     NDA 2025-06-30 leverage_exposure 5.613919e+11 5.613920e+11 5.346652e+04 9.523920e-08      0.001    True     p3 EUR 5.61392e+11
7_seam_capital     NDA 2025-06-30               rwa 1.585755e+11 1.585760e+11 4.759342e+05 3.001309e-06      0.001    True     p3 EUR 1.58576e+11
7_seam_capital    RABO 2025-06-30              cet1 4.602747e+10 4.602700e+10 4.690811e+05 1.019133e-05      0.001    True      p3 EUR 4.6027e+10
7_seam_capital    RABO 2025-06-30 leverage_exposure 6.746864e+11 6.746860e+11 4.413306e+05 6.541269e-07      0.001    True     p3 EUR 6.74686e+11
7_seam_capital    RABO 2025-06-30               rwa 2.315758e+11 2.315760e+11 1.606443e+05 6.937006e-07      0.001    True     p3 EUR 2.31576e+11
7_seam_capital     SAB 2025-06-30              cet1 1.034842e+10 1.034842e+10 9.918213e-05 9.584282e-15      0.001    True p3 EUR 1.034841524e+10
7_seam_capital     SAB 2025-06-30 leverage_exposure 2.521911e+11 2.521911e+11 0.000000e+00 0.000000e+00      0.001    True p3 EUR 2.521911338e+11
7_seam_capital     SAB 2025-06-30               rwa 7.923903e+10 7.926456e+10 2.552770e+07 3.221607e-04      0.001    True p3 EUR 7.926455766e+10
7_seam_capital     SAN 2025-06-30              cet1 8.125291e+10 8.125300e+10 9.317500e+04 1.146728e-06      0.001    True      p3 EUR 8.1253e+10
7_seam_capital     SAN 2025-06-30 leverage_exposure 1.850859e+12 1.850859e+12 4.006100e+05 2.164454e-07      0.001    True    p3 EUR 1.850859e+12
7_seam_capital     SAN 2025-06-30               rwa 6.257503e+11 6.257500e+11 2.676322e+05 4.276982e-07      0.001    True      p3 EUR 6.2575e+11
7_seam_capital     SEB 2025-06-30              cet1 1.568446e+10 1.568446e+10 2.479553e-05 1.580898e-15      0.001    True p3 SEK 1.748268135e+11
7_seam_capital     SEB 2025-06-30 leverage_exposure 3.443762e+11 3.443762e+11 4.882812e-04 1.417872e-15      0.001    True p3 SEK 3.838589323e+12
7_seam_capital     SEB 2025-06-30               rwa 8.881679e+10 8.881679e+10 1.525879e-05 1.718007e-16      0.001    True p3 SEK 9.899963804e+11
7_seam_capital     SHB 2025-06-30              cet1 1.331566e+10 1.331566e+10 4.189204e+03 3.146074e-07      0.001    True     p3 SEK 1.48423e+11
7_seam_capital     SHB 2025-06-30 leverage_exposure 3.128795e+11 3.128795e+11 1.470776e+04 4.700774e-08      0.001    True    p3 SEK 3.487511e+12
7_seam_capital     SHB 2025-06-30               rwa 7.252536e+10 7.252537e+10 1.031224e+04 1.421880e-07      0.001    True     p3 SEK 8.08404e+11
7_seam_capital    SWED 2025-06-30              cet1 1.570728e+10 1.570726e+10 1.363657e+04 8.681688e-07      0.001    True     p3 SEK 1.75081e+11
7_seam_capital    SWED 2025-06-30 leverage_exposure 2.560123e+11 2.560123e+11 8.253712e+03 3.223951e-08      0.001    True    p3 SEK 2.853641e+12
7_seam_capital    SWED 2025-06-30               rwa 7.971472e+10 7.971471e+10 1.545687e+04 1.939023e-07      0.001    True      p3 SEK 8.8854e+11
7_seam_capital     UCG 2025-06-30              cet1 4.609631e+10 4.609600e+10 3.071980e+05 6.664265e-06      0.001    True      p3 EUR 4.6096e+10
7_seam_capital     UCG 2025-06-30 leverage_exposure 8.967158e+11 8.967160e+11 2.360000e+05 2.631826e-07      0.001    True     p3 EUR 8.96716e+11
7_seam_capital     UCG 2025-06-30               rwa 2.877425e+11 2.877430e+11 4.680270e+05 1.626548e-06      0.001    True     p3 EUR 2.87743e+11
7_seam_capital     UNI 2025-06-30              cet1 4.591181e+09 4.591181e+09 0.000000e+00 0.000000e+00      0.001    True      p3 EUR 4591180859
7_seam_capital     UNI 2025-06-30 leverage_exposure 9.386412e+10 9.386412e+10 0.000000e+00 0.000000e+00      0.001    True   p3 EUR 9.3864116e+10
7_seam_capital     UNI 2025-06-30               rwa 2.873665e+10 2.873665e+10 0.000000e+00 0.000000e+00      0.001    True   p3 EUR 2.8736652e+10
```

#### seam 2 (check 8) at 2025-06-30 in full, sorted by |diff_rel| (738 rows; value_a eba EUR, value_b report in EUR; report_scope_adj = report total_assets + lr1_scope_adjustment, total_assets rows only)

```
bank_id                         field       value_a       value_b     diff_abs     diff_rel  report_scope_adj  diff_rel_scope_adj                     note
    BNP gains_derecognition_not_fvtpl -3.609968e+06  1.670000e+08 1.706100e+08 4.726080e+01               NaN                 NaN no threshold; report EUR
    KBC           other_operating_net  7.917970e+07  1.563000e+09 1.483820e+09 1.873991e+01               NaN                 NaN no threshold; report EUR
    DBK           other_operating_net  2.278342e+07  3.650000e+08 3.422166e+08 1.502042e+01               NaN                 NaN no threshold; report EUR
   INGA           other_operating_net -8.962000e+06  1.250000e+08 1.339620e+08 1.494778e+01               NaN                 NaN no threshold; report EUR
    UNI            impairments_nonfin  2.410000e+05  3.326000e+06 3.085000e+06 1.280083e+01               NaN                 NaN no threshold; report EUR
    DNB           other_operating_net  2.446616e+07  1.938118e+08 1.693456e+08 6.921626e+00               NaN                 NaN no threshold; report NOK
   CABK        gains_hedge_accounting -2.793000e+06  1.600000e+07 1.879300e+07 6.728607e+00               NaN                 NaN no threshold; report EUR
    UCG        gains_held_for_trading  1.442746e+08  1.019000e+09 8.747254e+08 6.062921e+00               NaN                 NaN no threshold; report EUR
    NDA           other_operating_net  2.122900e+07  1.300000e+08 1.087710e+08 5.123700e+00               NaN                 NaN no threshold; report EUR
   CABK           other_operating_net -1.498670e+08  6.150000e+08 7.648670e+08 5.103639e+00               NaN                 NaN no threshold; report EUR
   SWED        gains_held_for_trading -3.674553e+07  1.259905e+08 1.627360e+08 4.428731e+00               NaN                 NaN no threshold; report SEK
    CBK           other_operating_net -5.158588e+07 -2.530000e+08 2.014141e+08 3.904443e+00               NaN                 NaN no threshold; report EUR
    CAG           other_operating_net  1.270601e+09 -3.638000e+09 4.908601e+09 3.863212e+00               NaN                 NaN no threshold; report EUR
    SAB           other_operating_net -2.438200e+07  6.332900e+07 8.771100e+07 3.597367e+00               NaN                 NaN no threshold; report EUR
    SEB        gains_held_for_trading  1.069246e+08  4.697157e+08 3.627911e+08 3.392961e+00               NaN                 NaN no threshold; report SEK
 DANSKE           other_operating_net  3.390927e+07  1.380569e+08 1.041476e+08 3.071362e+00               NaN                 NaN no threshold; report DKK
    DNB        gains_held_for_trading  3.956233e+07  1.468167e+08 1.072544e+08 2.711022e+00               NaN                 NaN no threshold; report NOK
    CAG        gains_designated_fvtpl -1.404525e+09  2.293000e+09 3.697525e+09 2.632580e+00               NaN                 NaN no threshold; report EUR
    KBC            impairments_nonfin  2.538184e+06  8.000000e+06 5.461816e+06 2.151860e+00               NaN                 NaN no threshold; report EUR
    SAN           other_operating_net -1.126310e+08  1.260000e+08 2.386310e+08 2.118697e+00               NaN                 NaN no threshold; report EUR
    UNI           other_operating_net -3.269600e+07  3.619500e+07 6.889100e+07 2.107016e+00               NaN                 NaN no threshold; report EUR
    CAG gains_derecognition_not_fvtpl  3.729456e+08 -3.430000e+08 7.159456e+08 1.919705e+00               NaN                 NaN no threshold; report EUR
    UCG        gains_designated_fvtpl -1.232170e+08 -3.310000e+08 2.077830e+08 1.686318e+00               NaN                 NaN no threshold; report EUR
    ISP               dividend_income  2.134874e+08  5.300000e+08 3.165126e+08 1.482582e+00               NaN                 NaN no threshold; report EUR
    SHB        gains_held_for_trading -1.105219e+08  3.983391e+07 1.503559e+08 1.360416e+00               NaN                 NaN no threshold; report SEK
    ABN           other_operating_net  4.903068e+07  1.140000e+08 6.496932e+07 1.325075e+00               NaN                 NaN no threshold; report EUR
    SAN gains_derecognition_not_fvtpl -2.613400e+07  8.000000e+06 3.413400e+07 1.306115e+00               NaN                 NaN no threshold; report EUR
   BAMI           other_operating_net  1.510340e+08 -3.421700e+07 1.852510e+08 1.226552e+00               NaN                 NaN no threshold; report EUR
   BBVA            impairments_nonfin -2.648800e+07  5.000000e+06 3.148800e+07 1.188765e+00               NaN                 NaN no threshold; report EUR
    ISP                    provisions  3.427052e+07  7.500000e+07 4.072948e+07 1.188470e+00               NaN                 NaN no threshold; report EUR
   BBVA           other_operating_net -5.544730e+08  9.800000e+07 6.524730e+08 1.176744e+00               NaN                 NaN no threshold; report EUR
   RABO gains_derecognition_not_fvtpl  4.497332e+07 -7.000000e+06 5.197332e+07 1.155648e+00               NaN                 NaN no threshold; report EUR
   BAMI gains_derecognition_not_fvtpl  1.838340e+08 -2.788300e+07 2.117170e+08 1.151675e+00               NaN                 NaN no threshold; report EUR
   SWED        resolution_dgs_contrib  6.806235e+07  1.447359e+08 7.667353e+07 1.126519e+00               NaN                 NaN no threshold; report SEK
   BMPS           other_operating_net  1.195566e+08 -1.080000e+07 1.303566e+08 1.090334e+00               NaN                 NaN no threshold; report EUR
   BMPS        gains_designated_fvtpl -1.003805e+07  8.000000e+05 1.083805e+07 1.079697e+00               NaN                 NaN no threshold; report EUR
    SEB           other_operating_net  6.812394e+07 -2.883903e+06 7.100784e+07 1.042333e+00               NaN                 NaN no threshold; report SEK
    ABN               impairments_fin  3.604281e+07 -1.000000e+06 3.704281e+07 1.027745e+00               NaN                 NaN no threshold; report EUR
   SWED            impairments_nonfin  1.704571e+04  0.000000e+00 1.704571e+04 1.000000e+00               NaN                 NaN no threshold; report SEK
    SEB        resolution_dgs_contrib  8.386577e+07  1.663652e+08 8.249939e+07 9.837076e-01               NaN                 NaN no threshold; report SEK
   SWED               impairments_fin  3.985987e+07  8.110977e+05 3.904877e+07 9.796513e-01               NaN                 NaN no threshold; report SEK
    BPE           other_operating_net  2.355814e+08  1.336100e+07 2.222204e+08 9.432850e-01               NaN                 NaN no threshold; report EUR
    NDA               impairments_fin  1.877929e+07  2.000000e+06 1.677929e+07 8.934997e-01               NaN                 NaN no threshold; report EUR
   SWED           other_operating_net  1.212445e+08  2.282789e+08 1.070344e+08 8.827981e-01               NaN                 NaN no threshold; report SEK
    BNP        gains_held_for_trading  3.616000e+09  6.797000e+09 3.181000e+09 8.797015e-01               NaN                 NaN no threshold; report EUR
 DANSKE               impairments_fin  2.388016e+08  3.565353e+07 2.031480e+08 8.506981e-01               NaN                 NaN no threshold; report DKK
   RABO                trading_assets  2.476672e+10  3.773000e+09 2.099372e+10 8.476584e-01               NaN                 NaN no threshold; report EUR
    CBK        gains_held_for_trading -1.423788e+08 -2.500000e+07 1.173788e+08 8.244120e-01               NaN                 NaN no threshold; report EUR
   BBVA        gains_designated_fvtpl  1.616590e+08  2.900000e+07 1.326590e+08 8.206100e-01               NaN                 NaN no threshold; report EUR
    UCG gains_derecognition_not_fvtpl  8.865757e+08  2.340000e+08 6.525757e+08 7.360631e-01               NaN                 NaN no threshold; report EUR
    KBC               dividend_income  2.431761e+07  4.200000e+07 1.768239e+07 7.271435e-01               NaN                 NaN no threshold; report EUR
    SAB gains_derecognition_not_fvtpl  1.699800e+07  2.848200e+07 1.148400e+07 6.756089e-01               NaN                 NaN no threshold; report EUR
    SHB           other_operating_net  9.109882e+06  1.514049e+07 6.030609e+06 6.619855e-01               NaN                 NaN no threshold; report SEK
    ISP gains_derecognition_not_fvtpl  2.569141e+08  9.200000e+07 1.649141e+08 6.419036e-01               NaN                 NaN no threshold; report EUR
    ABN        gains_held_for_trading  3.052811e+08  1.110000e+08 1.942811e+08 6.364007e-01               NaN                 NaN no threshold; report EUR
    ISP        gains_held_for_trading  2.195448e+09  8.110000e+08 1.384448e+09 6.305993e-01               NaN                 NaN no threshold; report EUR
   RABO           other_operating_net  3.254081e+08  5.250000e+08 1.995919e+08 6.133588e-01               NaN                 NaN no threshold; report EUR
    DBK                trading_assets  4.060072e+11  1.581160e+11 2.478912e+11 6.105586e-01               NaN                 NaN no threshold; report EUR
   CABK            impairments_nonfin  7.092400e+07  2.900000e+07 4.192400e+07 5.911116e-01               NaN                 NaN no threshold; report EUR
    ISP        gains_designated_fvtpl -5.199213e+08 -2.130000e+08 3.069213e+08 5.903226e-01               NaN                 NaN no threshold; report EUR
    BKT           other_operating_net -4.392100e+07 -1.813200e+07 2.578900e+07 5.871679e-01               NaN                 NaN no threshold; report EUR
    ABN                trading_assets  7.140887e+09  2.961000e+09 4.179887e+09 5.853457e-01               NaN                 NaN no threshold; report EUR
    BNP           other_operating_net  2.116985e+09  3.349000e+09 1.232015e+09 5.819669e-01               NaN                 NaN no threshold; report EUR
    KBC        gains_held_for_trading  1.431433e+08  6.200000e+07 8.114326e+07 5.668675e-01               NaN                 NaN no threshold; report EUR
    UCG           other_operating_net  4.258843e+08  2.090000e+08 2.168843e+08 5.092564e-01               NaN                 NaN no threshold; report EUR
   BBVA        gains_hedge_accounting -1.418600e+07 -7.000000e+06 7.186000e+06 5.065558e-01               NaN                 NaN no threshold; report EUR
   RABO        gains_held_for_trading  2.906590e+08  4.350000e+08 1.443410e+08 4.965992e-01               NaN                 NaN no threshold; report EUR
   CABK                trading_assets  1.405967e+10  7.329000e+09 6.730667e+09 4.787217e-01               NaN                 NaN no threshold; report EUR
    CAG               dividend_income  1.675043e+08  2.450000e+08 7.749572e+07 4.626492e-01               NaN                 NaN no threshold; report EUR
    ISP           other_operating_net  5.688511e+08  3.160000e+08 2.528511e+08 4.444943e-01               NaN                 NaN no threshold; report EUR
    GLE gains_derecognition_not_fvtpl  2.935694e+08  1.650000e+08 1.285694e+08 4.379522e-01               NaN                 NaN no threshold; report EUR
   INGA              interest_expense  3.300594e+10  1.855300e+10 1.445294e+10 4.378891e-01               NaN                 NaN no threshold; report EUR
    GLE           other_operating_net  2.086930e+09  1.205000e+09 8.819304e+08 4.225969e-01               NaN                 NaN no threshold; report EUR
    KBC        total_operating_income  4.256054e+09  5.955000e+09 1.698946e+09 3.991833e-01               NaN                 NaN no threshold; report EUR
   INGA               interest_income  4.011180e+10  2.571200e+10 1.439980e+10 3.589917e-01               NaN                 NaN no threshold; report EUR
    CAG        gains_held_for_trading  3.595140e+09  4.845000e+09 1.249860e+09 3.476528e-01               NaN                 NaN no threshold; report EUR
   BMPS        gains_held_for_trading  4.935238e+07  6.620000e+07 1.684762e+07 3.413739e-01               NaN                 NaN no threshold; report EUR
    CAG                  depreciation  1.528801e+09  1.020000e+09 5.088011e+08 3.328105e-01               NaN                 NaN no threshold; report EUR
   BAMI        gains_held_for_trading  3.339500e+08  2.244050e+08 1.095450e+08 3.280281e-01               NaN                 NaN no threshold; report EUR
   BBVA                    provisions  1.002920e+08  1.330000e+08 3.270800e+07 3.261277e-01               NaN                 NaN no threshold; report EUR
   CABK gains_derecognition_not_fvtpl  8.534000e+06  1.100000e+07 2.466000e+06 2.889618e-01               NaN                 NaN no threshold; report EUR
    SHB               impairments_fin -1.909033e+07 -2.460330e+07 5.512969e+06 2.887833e-01               NaN                 NaN no threshold; report SEK
    CAG                      net_fees  8.882527e+09  6.398000e+09 2.484527e+09 2.797094e-01               NaN                 NaN no threshold; report EUR
   BAMI        gains_designated_fvtpl -1.490290e+08 -1.074000e+08 4.162900e+07 2.793349e-01               NaN                 NaN no threshold; report EUR
   CABK              interest_expense  3.066016e+09  3.902000e+09 8.359840e+08 2.726613e-01               NaN                 NaN no threshold; report EUR
    SHB        resolution_dgs_contrib  1.651768e+08  1.214844e+08 4.369237e+07 2.645188e-01               NaN                 NaN no threshold; report SEK
 DANSKE        gains_held_for_trading  1.857398e+08  2.326862e+08 4.694643e+07 2.527538e-01               NaN                 NaN no threshold; report DKK
   SWED              interest_expense  2.520164e+09  1.919958e+09 6.002058e+08 2.381614e-01               NaN                 NaN no threshold; report SEK
 DANSKE              interest_expense  3.536313e+09  2.728568e+09 8.077457e+08 2.284146e-01               NaN                 NaN no threshold; report DKK
    GLE                       cash_cb  1.922134e+11  1.487820e+11 4.343144e+10 2.259542e-01               NaN                 NaN no threshold; report EUR
    ISP                  total_assets  7.705184e+11  9.434520e+11 1.729336e+11 2.244380e-01      7.705190e+11        7.869442e-07 no threshold; report EUR
   INGA        gains_held_for_trading  1.512130e+09  1.839000e+09 3.268700e+08 2.161653e-01               NaN                 NaN no threshold; report EUR
    BNP            deposits_customers  1.297581e+12  1.024734e+12 2.728469e+11 2.102735e-01               NaN                 NaN no threshold; report EUR
    CAG             total_liabilities  2.036653e+12  2.461797e+12 4.251437e+11 2.087463e-01               NaN                 NaN no threshold; report EUR
   BAMI               dividend_income  1.295530e+08  1.562820e+08 2.672900e+07 2.063171e-01               NaN                 NaN no threshold; report EUR
    CAG                  total_assets  2.187749e+12  2.614010e+12 4.262609e+11 1.948399e-01      2.187748e+12        5.079202e-07 no threshold; report EUR
    KBC                           pbt  1.697203e+09  2.022000e+09 3.247967e+08 1.913717e-01               NaN                 NaN no threshold; report EUR
    KBC                admin_expenses  2.124480e+09  2.518000e+09 3.935199e+08 1.852312e-01               NaN                 NaN no threshold; report EUR
    BPE        gains_held_for_trading  1.175510e+08  1.388430e+08 2.129195e+07 1.811294e-01               NaN                 NaN no threshold; report EUR
    GLE            deposits_customers  6.320626e+11  5.183970e+11 1.136656e+11 1.798328e-01               NaN                 NaN no threshold; report EUR
   RABO               impairments_fin  1.655401e+08  1.360000e+08 2.954014e+07 1.784470e-01               NaN                 NaN no threshold; report EUR
 DANSKE             total_liabilities  4.060071e+11  4.780740e+11 7.206686e+10 1.775015e-01               NaN                 NaN no threshold; report DKK
    SHB                      net_fees  4.415778e+08  5.196433e+08 7.806550e+07 1.767877e-01               NaN                 NaN no threshold; report SEK
    GLE                      net_fees  3.142583e+09  2.594000e+09 5.485830e+08 1.745644e-01               NaN                 NaN no threshold; report EUR
    NDA             total_liabilities  5.165589e+11  6.064410e+11 8.988213e+10 1.740017e-01               NaN                 NaN no threshold; report EUR
    KBC                 profit_owners  1.334524e+09  1.564000e+09 2.294758e+08 1.719533e-01               NaN                 NaN no threshold; report EUR
    KBC                           pat  1.334656e+09  1.564000e+09 2.293437e+08 1.718373e-01               NaN                 NaN no threshold; report EUR
    CBK               dividend_income  2.052196e+07  1.700000e+07 3.521955e+06 1.716189e-01               NaN                 NaN no threshold; report EUR
 DANSKE                  total_assets  4.291889e+11  5.012307e+11 7.204178e+10 1.678556e-01      5.012307e+11        1.678556e-01 no threshold; report DKK
   SWED             total_liabilities  2.246680e+11  2.623012e+11 3.763321e+10 1.675059e-01               NaN                 NaN no threshold; report SEK
    NDA                  total_assets  5.469076e+11  6.368080e+11 8.990041e+10 1.643795e-01      5.469070e+11        1.081929e-06 no threshold; report EUR
    GLE        gains_held_for_trading  4.145146e+09  4.818000e+09 6.728541e+08 1.623234e-01               NaN                 NaN no threshold; report EUR
    CBK                admin_expenses  2.782845e+09  3.234000e+09 4.511547e+08 1.621199e-01               NaN                 NaN no threshold; report EUR
    UNI gains_derecognition_not_fvtpl -9.140000e+06 -7.666000e+06 1.474000e+06 1.612691e-01               NaN                 NaN no threshold; report EUR
   SWED               interest_income  4.693603e+09  3.939231e+09 7.543719e+08 1.607234e-01               NaN                 NaN no threshold; report SEK
    UCG                       cash_cb  4.950667e+10  4.180400e+10 7.702672e+09 1.555886e-01               NaN                 NaN no threshold; report EUR
   SWED                  total_assets  2.433942e+11  2.810247e+11 3.763053e+10 1.546073e-01      2.433942e+11        1.297460e-07 no threshold; report SEK
   CABK             total_liabilities  5.424626e+11  6.223870e+11 7.992438e+10 1.473362e-01               NaN                 NaN no threshold; report EUR
    SEB             total_liabilities  3.063817e+11  3.493384e+11 4.295673e+10 1.402066e-01               NaN                 NaN no threshold; report SEK
    CBK                trading_assets  2.914536e+10  3.321800e+10 4.072639e+09 1.397354e-01               NaN                 NaN no threshold; report EUR
   CABK                  total_assets  5.798973e+11  6.598220e+11 7.992473e+10 1.378257e-01      5.798974e+11        1.379555e-07 no threshold; report EUR
   SWED                admin_expenses  1.166686e+09  1.007383e+09 1.593022e+08 1.365426e-01               NaN                 NaN no threshold; report SEK
   BBVA          exchange_differences -1.082270e+08 -1.230000e+08 1.477300e+07 1.365001e-01               NaN                 NaN no threshold; report EUR
 DANSKE               interest_income  5.960038e+09  5.152338e+09 8.077004e+08 1.355193e-01               NaN                 NaN no threshold; report DKK
    DNB               impairments_fin  1.077933e+08  9.321832e+07 1.457498e+07 1.352123e-01               NaN                 NaN no threshold; report NOK
    BPE                    provisions  1.298306e+07  1.473400e+07 1.750938e+06 1.348633e-01               NaN                 NaN no threshold; report EUR
    SEB                  total_assets  3.258115e+11  3.687682e+11 4.295671e+10 1.318453e-01      3.258115e+11        6.856378e-08 no threshold; report SEK
    GLE             total_liabilities  1.304225e+12  1.474030e+12 1.698052e+11 1.301963e-01               NaN                 NaN no threshold; report EUR
    ISP                       cash_cb  4.785025e+10  4.186400e+10 5.986247e+09 1.251038e-01               NaN                 NaN no threshold; report EUR
    CAG                admin_expenses  1.239419e+10  1.084400e+10 1.550188e+09 1.250738e-01               NaN                 NaN no threshold; report EUR
    NDA        gains_held_for_trading  4.826859e+08  5.430000e+08 6.031406e+07 1.249551e-01               NaN                 NaN no threshold; report EUR
    GLE                  total_assets  1.380480e+12  1.551491e+12 1.710110e+11 1.238779e-01      1.380480e+12        1.221353e-08 no threshold; report EUR
    BPE        gains_designated_fvtpl -1.101570e+08 -1.235180e+08 1.336101e+07 1.212906e-01               NaN                 NaN no threshold; report EUR
    DBK                admin_expenses  9.099359e+09  1.018000e+10 1.080641e+09 1.187601e-01               NaN                 NaN no threshold; report EUR
    DNB             total_liabilities  2.690176e+11  3.007447e+11 3.172709e+10 1.179369e-01               NaN                 NaN no threshold; report NOK
   INGA                admin_expenses  5.577254e+09  6.234000e+09 6.567460e+08 1.177544e-01               NaN                 NaN no threshold; report EUR
    BPE                       cash_cb  8.596275e+09  7.585046e+09 1.011229e+09 1.176357e-01               NaN                 NaN no threshold; report EUR
    SEB                      net_fees  1.083625e+09  1.206733e+09 1.231077e+08 1.136073e-01               NaN                 NaN no threshold; report SEK
    BNP             total_liabilities  2.442546e+12  2.717736e+12 2.751902e+11 1.126653e-01               NaN                 NaN no threshold; report EUR
    NDA                      net_fees  1.425609e+09  1.585000e+09 1.593908e+08 1.118054e-01               NaN                 NaN no threshold; report EUR
   CABK               interest_income  8.269583e+09  9.184000e+09 9.144170e+08 1.105760e-01               NaN                 NaN no threshold; report EUR
    DNB                  total_assets  2.926278e+11  3.241186e+11 3.149079e+10 1.076138e-01      2.925535e+11        2.538954e-04 no threshold; report NOK
    BNP                  total_assets  2.573934e+12  2.849376e+12 2.754421e+11 1.070121e-01      2.573934e+12        2.992812e-08 no threshold; report EUR
   CABK        gains_designated_fvtpl  4.519000e+06  5.000000e+06 4.810000e+05 1.064395e-01               NaN                 NaN no threshold; report EUR
    SEB                       cash_cb  4.828169e+10  4.314592e+10 5.135772e+09 1.063710e-01               NaN                 NaN no threshold; report SEK
    BNP                      net_fees  5.967017e+09  5.349000e+09 6.180172e+08 1.035722e-01               NaN                 NaN no threshold; report EUR
    CAG               impairments_fin  1.751049e+09  1.575000e+09 1.760493e+08 1.005393e-01               NaN                 NaN no threshold; report EUR
   CABK                      net_fees  2.164948e+09  1.949000e+09 2.159480e+08 9.974743e-02               NaN                 NaN no threshold; report EUR
    KBC             total_liabilities  3.316397e+11  3.644400e+11 3.280027e+10 9.890333e-02               NaN                 NaN no threshold; report EUR
    ISP               interest_income  1.310987e+10  1.439800e+10 1.288127e+09 9.825628e-02               NaN                 NaN no threshold; report EUR
    CAG            deposits_customers  1.294336e+12  1.167898e+12 1.264379e+11 9.768552e-02               NaN                 NaN no threshold; report EUR
    KBC                  total_assets  3.565054e+11  3.906690e+11 3.416355e+10 9.582898e-02      3.565051e+11        1.070242e-06 no threshold; report EUR
    ISP                      net_fees  4.854823e+09  4.391000e+09 4.638232e+08 9.553864e-02               NaN                 NaN no threshold; report EUR
    CBK gains_derecognition_not_fvtpl  1.026265e+08  9.300000e+07 9.626526e+06 9.380154e-02               NaN                 NaN no threshold; report EUR
    SEB              interest_expense  4.010133e+09  3.647867e+09 3.622656e+08 9.033756e-02               NaN                 NaN no threshold; report SEK
    SHB             total_liabilities  2.860223e+11  3.115075e+11 2.548513e+10 8.910189e-02               NaN                 NaN no threshold; report SEK
   CABK        total_operating_income  7.390921e+09  8.040000e+09 6.490790e+08 8.782113e-02               NaN                 NaN no threshold; report EUR
   BAMI                  total_assets  1.942171e+11  2.109483e+11 1.673115e+10 8.614665e-02      1.942173e+11        7.929270e-07 no threshold; report EUR
    SHB                  total_assets  3.025829e+11  3.284230e+11 2.584008e+10 8.539833e-02      3.542629e+11        1.707961e-01 no threshold; report SEK
    DNB                  depreciation  1.740762e+08  1.593373e+08 1.473896e+07 8.466956e-02               NaN                 NaN no threshold; report NOK
 DANSKE                admin_expenses  1.566892e+09  1.698234e+09 1.313424e+08 8.382355e-02               NaN                 NaN no threshold; report DKK
    ISP               impairments_fin  5.961084e+08  6.450000e+08 4.889163e+07 8.201802e-02               NaN                 NaN no threshold; report EUR
    UCG        total_operating_income  1.340793e+10  1.233900e+10 1.068931e+09 7.972380e-02               NaN                 NaN no threshold; report EUR
    BKT gains_derecognition_not_fvtpl  1.114436e+07  1.027600e+07 8.683640e+05 7.791957e-02               NaN                 NaN no threshold; report EUR
    BPE        total_operating_income  2.999877e+09  2.767471e+09 2.324061e+08 7.747186e-02               NaN                 NaN no threshold; report EUR
    SHB                 profit_owners  9.889273e+08  1.064250e+09 7.532306e+07 7.616643e-02               NaN                 NaN no threshold; report SEK
    SHB                           pat  9.946130e+08  1.070289e+09 7.567552e+07 7.608540e-02               NaN                 NaN no threshold; report SEK
    BNP               impairments_fin  1.535170e+09  1.650000e+09 1.148305e+08 7.479986e-02               NaN                 NaN no threshold; report EUR
    ISP        total_operating_income  1.360074e+10  1.461400e+10 1.013263e+09 7.450060e-02               NaN                 NaN no threshold; report EUR
    BPE gains_derecognition_not_fvtpl  2.774114e+07  2.568300e+07 2.058137e+06 7.419079e-02               NaN                 NaN no threshold; report EUR
    UNI        total_operating_income  9.873240e+08  1.058450e+09 7.112600e+07 7.203917e-02               NaN                 NaN no threshold; report EUR
   BAMI                       cash_cb  1.264304e+10  1.173292e+10 9.101180e+08 7.198568e-02               NaN                 NaN no threshold; report EUR
   INGA               impairments_fin  6.573060e+08  6.120000e+08 4.530600e+07 6.892680e-02               NaN                 NaN no threshold; report EUR
    CAG               interest_income  2.936989e+10  3.136300e+10 1.993108e+09 6.786228e-02               NaN                 NaN no threshold; report EUR
    UCG                  depreciation  5.395702e+08  5.760000e+08 3.642976e+07 6.751625e-02               NaN                 NaN no threshold; report EUR
   BAMI            deposits_customers  1.132863e+11  1.057058e+11 7.580427e+09 6.691391e-02               NaN                 NaN no threshold; report EUR
   CABK                admin_expenses  2.990198e+09  2.791000e+09 1.991980e+08 6.661699e-02               NaN                 NaN no threshold; report EUR
   RABO              interest_expense  7.074570e+09  6.615000e+09 4.595699e+08 6.496083e-02               NaN                 NaN no threshold; report EUR
    SAN               at1_instruments  9.577581e+09  8.967000e+09 6.105809e+08 6.375106e-02               NaN                 NaN no threshold; report EUR
   RABO                  depreciation  1.548322e+08  1.450000e+08 9.832244e+06 6.350256e-02               NaN                 NaN no threshold; report EUR
    CAG        total_operating_income  2.118275e+10  1.985600e+10 1.326752e+09 6.263362e-02               NaN                 NaN no threshold; report EUR
    SEB               interest_income  5.891588e+09  5.523485e+09 3.681028e+08 6.247938e-02               NaN                 NaN no threshold; report SEK
   CABK               at1_instruments  4.436874e+09  4.712074e+09 2.751999e+08 6.202563e-02               NaN                 NaN no threshold; report EUR
    SHB                           pbt  1.299384e+09  1.378866e+09 7.948262e+07 6.116948e-02               NaN                 NaN no threshold; report SEK
   BAMI        total_operating_income  3.277962e+09  3.088297e+09 1.896650e+08 5.786065e-02               NaN                 NaN no threshold; report EUR
    CBK               impairments_fin  3.183864e+08  3.000000e+08 1.838636e+07 5.774859e-02               NaN                 NaN no threshold; report EUR
    CAG                       cash_cb  1.825775e+11  1.720850e+11 1.049250e+10 5.746875e-02               NaN                 NaN no threshold; report EUR
   BMPS        total_operating_income  2.106004e+09  1.986600e+09 1.194042e+08 5.669706e-02               NaN                 NaN no threshold; report EUR
   BBVA gains_derecognition_not_fvtpl  1.829540e+08  1.930000e+08 1.004600e+07 5.490998e-02               NaN                 NaN no threshold; report EUR
    KBC                  total_equity  2.486572e+10  2.622900e+10 1.363279e+09 5.482562e-02               NaN                 NaN no threshold; report EUR
    UCG                  total_assets  8.168161e+11  8.603280e+11 4.351189e+10 5.327011e-02      8.168170e+11        1.084553e-06 no threshold; report EUR
    ABN            deposits_customers  2.833446e+11  2.683230e+11 1.502156e+10 5.301518e-02               NaN                 NaN no threshold; report EUR
    NDA        resolution_dgs_contrib  7.708224e+07  7.300000e+07 4.082240e+06 5.295954e-02               NaN                 NaN no threshold; report EUR
    DBK        gains_held_for_trading  3.153997e+09  2.993000e+09 1.609975e+08 5.104553e-02               NaN                 NaN no threshold; report EUR
    BNP                       cash_cb  2.080043e+11  1.974190e+11 1.058528e+10 5.088971e-02               NaN                 NaN no threshold; report EUR
    CAG                           pbt  6.666819e+09  7.004000e+09 3.371811e+08 5.057601e-02               NaN                 NaN no threshold; report EUR
   INGA                       cash_cb  7.950929e+10  7.556500e+10 3.944293e+09 4.960795e-02               NaN                 NaN no threshold; report EUR
   CABK                           pbt  4.147700e+09  4.353000e+09 2.053000e+08 4.949731e-02               NaN                 NaN no threshold; report EUR
   BAMI               interest_income  2.888574e+09  3.030960e+09 1.423860e+08 4.929283e-02               NaN                 NaN no threshold; report EUR
    ABN                       cash_cb  4.923372e+10  4.681100e+10 2.422719e+09 4.920852e-02               NaN                 NaN no threshold; report EUR
    DBK                       cash_cb  1.438604e+11  1.371240e+11 6.736411e+09 4.682603e-02               NaN                 NaN no threshold; report EUR
    DNB                           pbt  2.188099e+09  2.290152e+09 1.020534e+08 4.664020e-02               NaN                 NaN no threshold; report NOK
   BMPS        gains_hedge_accounting -4.779880e+05 -5.000000e+05 2.201200e+04 4.605137e-02               NaN                 NaN no threshold; report EUR
    NDA        total_operating_income  5.627151e+09  5.885000e+09 2.578489e+08 4.582228e-02               NaN                 NaN no threshold; report EUR
   INGA            deposits_customers  7.734177e+11  7.380790e+11 3.533874e+10 4.569167e-02               NaN                 NaN no threshold; report EUR
   BMPS                       cash_cb  1.234600e+10  1.179430e+10 5.517042e+08 4.468686e-02               NaN                 NaN no threshold; report EUR
    NDA                admin_expenses  2.216054e+09  2.314000e+09 9.794576e+07 4.419827e-02               NaN                 NaN no threshold; report EUR
    DNB                           pat  1.755016e+09  1.832122e+09 7.710597e+07 4.393463e-02               NaN                 NaN no threshold; report NOK
   BBVA             total_liabilities  6.862710e+11  7.160880e+11 2.981705e+10 4.344792e-02               NaN                 NaN no threshold; report EUR
   CABK                    provisions -5.226000e+06 -5.000000e+06 2.260000e+05 4.324531e-02               NaN                 NaN no threshold; report EUR
    GLE               at1_instruments  8.896372e+09  8.524000e+09 3.723716e+08 4.185657e-02               NaN                 NaN no threshold; report EUR
    DNB                 profit_owners  1.753667e+09  1.825861e+09 7.219419e+07 4.116756e-02               NaN                 NaN no threshold; report NOK
   BAMI                trading_assets  1.033053e+10  1.074675e+10 4.162160e+08 4.028990e-02               NaN                 NaN no threshold; report EUR
   BBVA                  total_assets  7.469548e+11  7.769740e+11 3.001923e+10 4.018882e-02      7.469540e+11        1.029513e-06 no threshold; report EUR
   BBVA                      net_fees  4.177841e+09  4.011000e+09 1.668410e+08 3.993474e-02               NaN                 NaN no threshold; report EUR
    GLE                           pbt  4.353937e+09  4.524000e+09 1.700627e+08 3.905951e-02               NaN                 NaN no threshold; report EUR
    ABN              interest_expense  4.305666e+09  4.141000e+09 1.646660e+08 3.824404e-02               NaN                 NaN no threshold; report EUR
    SAN        gains_hedge_accounting -1.350800e+07 -1.300000e+07 5.080000e+05 3.760734e-02               NaN                 NaN no threshold; report EUR
   SWED                      net_fees  6.908508e+08  7.168301e+08 2.597938e+07 3.760491e-02               NaN                 NaN no threshold; report SEK
    SHB        total_operating_income  2.469968e+09  2.560636e+09 9.066775e+07 3.670807e-02               NaN                 NaN no threshold; report SEK
    GLE               interest_income  2.210313e+10  2.290900e+10 8.058713e+08 3.645960e-02               NaN                 NaN no threshold; report EUR
    SHB                  depreciation  8.919570e+07  9.237502e+07 3.179322e+06 3.564435e-02               NaN                 NaN no threshold; report SEK
    SEB               impairments_fin  8.345891e+07  8.642697e+07 2.968058e+06 3.556310e-02               NaN                 NaN no threshold; report SEK
 DANSKE               at1_instruments  1.027804e+09  1.064222e+09 3.641830e+07 3.543313e-02               NaN                 NaN no threshold; report DKK
   BBVA        total_operating_income  1.742251e+10  1.803400e+10 6.114920e+08 3.509782e-02               NaN                 NaN no threshold; report EUR
   RABO               interest_income  1.293989e+10  1.248700e+10 4.528851e+08 3.499916e-02               NaN                 NaN no threshold; report EUR
    SEB                  depreciation  1.039170e+08  1.075155e+08 3.598531e+06 3.462891e-02               NaN                 NaN no threshold; report SEK
    SAN        gains_designated_fvtpl  2.297150e+08  2.220000e+08 7.715000e+06 3.358509e-02               NaN                 NaN no threshold; report EUR
    DBK gains_derecognition_not_fvtpl  3.828406e+07  3.700000e+07 1.284055e+06 3.354021e-02               NaN                 NaN no threshold; report EUR
   BBVA               at1_instruments  5.489036e+09  5.310000e+09 1.790360e+08 3.261702e-02               NaN                 NaN no threshold; report EUR
    KBC               impairments_fin  1.502970e+08  1.550000e+08 4.702961e+06 3.129111e-02               NaN                 NaN no threshold; report EUR
    SAB        total_operating_income  3.116925e+09  3.214321e+09 9.739600e+07 3.124746e-02               NaN                 NaN no threshold; report EUR
    GLE        total_operating_income  1.345502e+10  1.387400e+10 4.189841e+08 3.113962e-02               NaN                 NaN no threshold; report EUR
   BBVA            deposits_customers  4.620453e+11  4.480180e+11 1.402728e+10 3.035909e-02               NaN                 NaN no threshold; report EUR
    ISP                           pbt  7.390166e+09  7.608000e+09 2.178343e+08 2.947624e-02               NaN                 NaN no threshold; report EUR
 DANSKE            deposits_customers  1.583335e+11  1.629994e+11 4.665831e+09 2.946837e-02               NaN                 NaN no threshold; report DKK
 DANSKE                       cash_cb  2.219819e+10  2.154485e+10 6.533328e+08 2.943181e-02               NaN                 NaN no threshold; report DKK
    BKT            impairments_nonfin  8.231850e+06  7.990000e+06 2.418500e+05 2.937979e-02               NaN                 NaN no threshold; report EUR
    CBK                  total_assets  5.990921e+11  5.818180e+11 1.727410e+10 2.883380e-02               NaN                 NaN no threshold; report EUR
   BMPS                  depreciation  7.643081e+07  7.860000e+07 2.169190e+06 2.838109e-02               NaN                 NaN no threshold; report EUR
    SHB                admin_expenses  9.660963e+08  9.929639e+08 2.686751e+07 2.781038e-02               NaN                 NaN no threshold; report SEK
    ISP                admin_expenses  5.204880e+09  5.065000e+09 1.398800e+08 2.687478e-02               NaN                 NaN no threshold; report EUR
    SAB                    provisions  2.503000e+06  2.570000e+06 6.700000e+04 2.676788e-02               NaN                 NaN no threshold; report EUR
   RABO            deposits_customers  4.115790e+11  4.223910e+11 1.081199e+10 2.626953e-02               NaN                 NaN no threshold; report EUR
    KBC            deposits_customers  2.429599e+11  2.366260e+11 6.333948e+09 2.606993e-02               NaN                 NaN no threshold; report EUR
    BNP        total_operating_income  2.490607e+10  2.554100e+10 6.349328e+08 2.549310e-02               NaN                 NaN no threshold; report EUR
   BBVA              interest_expense  1.547343e+10  1.586100e+10 3.875660e+08 2.504719e-02               NaN                 NaN no threshold; report EUR
   BBVA        gains_held_for_trading  1.179832e+09  1.151000e+09 2.883200e+07 2.443738e-02               NaN                 NaN no threshold; report EUR
   BBVA               interest_income  2.779507e+10  2.846800e+10 6.729300e+08 2.421041e-02               NaN                 NaN no threshold; report EUR
 DANSKE        total_operating_income  3.655121e+09  3.741879e+09 8.675786e+07 2.373598e-02               NaN                 NaN no threshold; report DKK
    BKT                  depreciation  4.547902e+07  4.444400e+07 1.035019e+06 2.275816e-02               NaN                 NaN no threshold; report EUR
    BNP                admin_expenses  1.402934e+10  1.434400e+10 3.146589e+08 2.242863e-02               NaN                 NaN no threshold; report EUR
    SHB              interest_expense  4.301442e+09  4.205181e+09 9.626127e+07 2.237883e-02               NaN                 NaN no threshold; report SEK
    NDA            deposits_customers  2.425217e+11  2.372060e+11 5.315658e+09 2.191828e-02               NaN                 NaN no threshold; report EUR
    SHB                  total_equity  1.656059e+10  1.691544e+10 3.548559e+08 2.142773e-02               NaN                 NaN no threshold; report SEK
    SEB        total_operating_income  3.474778e+09  3.549093e+09 7.431482e+07 2.138692e-02               NaN                 NaN no threshold; report SEK
   SWED        total_operating_income  3.026413e+09  3.090372e+09 6.395939e+07 2.113373e-02               NaN                 NaN no threshold; report SEK
    DNB            deposits_customers  1.339311e+11  1.311932e+11 2.737880e+09 2.044245e-02               NaN                 NaN no threshold; report NOK
    BKT                admin_expenses  5.018690e+08  4.918120e+08 1.005700e+07 2.003910e-02               NaN                 NaN no threshold; report EUR
    BKT               impairments_fin  1.534963e+08  1.504900e+08 3.006268e+06 1.958528e-02               NaN                 NaN no threshold; report EUR
   SWED            deposits_customers  1.211592e+11  1.188620e+11 2.297239e+09 1.896050e-02               NaN                 NaN no threshold; report SEK
    CBK        total_operating_income  6.208711e+09  6.092000e+09 1.167107e+08 1.879790e-02               NaN                 NaN no threshold; report EUR
    SEB                admin_expenses  1.379816e+09  1.354623e+09 2.519223e+07 1.825768e-02               NaN                 NaN no threshold; report SEK
   CABK                       cash_cb  4.831659e+10  4.919000e+10 8.734120e+08 1.807686e-02               NaN                 NaN no threshold; report EUR
    ISP        gains_hedge_accounting -1.375181e+07 -1.400000e+07 2.481910e+05 1.804788e-02               NaN                 NaN no threshold; report EUR
   RABO        total_operating_income  7.893829e+09  8.035000e+09 1.411707e+08 1.788368e-02               NaN                 NaN no threshold; report EUR
    NDA                  depreciation  2.947786e+08  3.000000e+08 5.221403e+06 1.771296e-02               NaN                 NaN no threshold; report EUR
   BAMI                      net_fees  1.141832e+09  1.122139e+09 1.969300e+07 1.724685e-02               NaN                 NaN no threshold; report EUR
    BNP                           pbt  8.648672e+09  8.797000e+09 1.483275e+08 1.715032e-02               NaN                 NaN no threshold; report EUR
    NDA                       cash_cb  4.162254e+10  4.090900e+10 7.135381e+08 1.714307e-02               NaN                 NaN no threshold; report EUR
   RABO                       cash_cb  6.964840e+10  6.845600e+10 1.192401e+09 1.712029e-02               NaN                 NaN no threshold; report EUR
    SAN              interest_expense  3.064791e+10  3.012700e+10 5.209060e+08 1.699646e-02               NaN                 NaN no threshold; report EUR
    DBK            deposits_customers  6.425805e+11  6.533670e+11 1.078651e+10 1.678624e-02               NaN                 NaN no threshold; report EUR
    UNI                trading_assets  1.307660e+09  1.329151e+09 2.149100e+07 1.643470e-02               NaN                 NaN no threshold; report EUR
    KBC              interest_expense  6.006013e+09  5.909000e+09 9.701307e+07 1.615266e-02               NaN                 NaN no threshold; report EUR
   INGA               at1_instruments  6.230496e+09  6.131751e+09 9.874519e+07 1.584869e-02               NaN                 NaN no threshold; report EUR
    GLE                  total_equity  7.625526e+10  7.746100e+10 1.205742e+09 1.581192e-02               NaN                 NaN no threshold; report EUR
    DNB               at1_instruments  1.834975e+09  1.806550e+09 2.842499e+07 1.549067e-02               NaN                 NaN no threshold; report NOK
    GLE               impairments_fin  6.885823e+08  6.990000e+08 1.041774e+07 1.512925e-02               NaN                 NaN no threshold; report EUR
   SWED                           pbt  1.814818e+09  1.842183e+09 2.736524e+07 1.507878e-02               NaN                 NaN no threshold; report SEK
    KBC               interest_income  8.711568e+09  8.839000e+09 1.274320e+08 1.462791e-02               NaN                 NaN no threshold; report EUR
    DNB               interest_income  8.207494e+09  8.091298e+09 1.161958e+08 1.415728e-02               NaN                 NaN no threshold; report NOK
    NDA                           pbt  3.162665e+09  3.206000e+09 4.333520e+07 1.370212e-02               NaN                 NaN no threshold; report EUR
    UCG                admin_expenses  4.731477e+09  4.796000e+09 6.452330e+07 1.363703e-02               NaN                 NaN no threshold; report EUR
    SAN          exchange_differences  1.155680e+08  1.140000e+08 1.568000e+06 1.356777e-02               NaN                 NaN no threshold; report EUR
    GLE                admin_expenses  8.278665e+09  8.167000e+09 1.116651e+08 1.348830e-02               NaN                 NaN no threshold; report EUR
    ISP               at1_instruments  7.667561e+09  7.768000e+09 1.004393e+08 1.309926e-02               NaN                 NaN no threshold; report EUR
    BNP              interest_expense  2.704164e+10  2.669400e+10 3.476432e+08 1.285585e-02               NaN                 NaN no threshold; report EUR
    BNP                  depreciation  1.130498e+09  1.145000e+09 1.450233e+07 1.282827e-02               NaN                 NaN no threshold; report EUR
    CBK               interest_income  9.630622e+09  9.751000e+09 1.203779e+08 1.249950e-02               NaN                 NaN no threshold; report EUR
    BNP               at1_instruments  1.691444e+10  1.670600e+10 2.084417e+08 1.232330e-02               NaN                 NaN no threshold; report EUR
    SAN               interest_income  5.197630e+10  5.133800e+10 6.382950e+08 1.228050e-02               NaN                 NaN no threshold; report EUR
    GLE                           pat  3.514048e+09  3.557000e+09 4.295200e+07 1.222294e-02               NaN                 NaN no threshold; report EUR
 DANSKE                trading_assets  7.089604e+10  7.005321e+10 8.428303e+08 1.188826e-02               NaN                 NaN no threshold; report DKK
    BNP               interest_income  3.700518e+10  3.657300e+10 4.321847e+08 1.167903e-02               NaN                 NaN no threshold; report EUR
 DANSKE                           pbt  1.985131e+09  2.007857e+09 2.272576e+07 1.144799e-02               NaN                 NaN no threshold; report DKK
    ISP                  depreciation  8.577514e+08  8.480000e+08 9.751428e+06 1.136859e-02               NaN                 NaN no threshold; report EUR
    DBK               at1_instruments  1.167096e+10  1.180100e+10 1.300399e+08 1.114217e-02               NaN                 NaN no threshold; report EUR
   BBVA                admin_expenses  5.971588e+09  6.038000e+09 6.641200e+07 1.112133e-02               NaN                 NaN no threshold; report EUR
    ISP              interest_expense  5.636708e+09  5.697000e+09 6.029175e+07 1.069627e-02               NaN                 NaN no threshold; report EUR
    SAN             total_liabilities  1.688959e+12  1.706903e+12 1.794401e+10 1.062430e-02               NaN                 NaN no threshold; report EUR
    DNB                       cash_cb  3.711572e+10  3.672466e+10 3.910637e+08 1.053633e-02               NaN                 NaN no threshold; report NOK
    SHB            deposits_customers  1.281195e+11  1.267782e+11 1.341292e+09 1.046907e-02               NaN                 NaN no threshold; report SEK
    SHB               dividend_income  1.783960e+05  1.802439e+05 1.847898e+03 1.035840e-02               NaN                 NaN no threshold; report SEK
    DNB                  total_equity  2.361017e+10  2.337386e+10 2.363016e+08 1.000847e-02               NaN                 NaN no threshold; report NOK
    SAN                  total_assets  1.797910e+12  1.815888e+12 1.797808e+10 9.999433e-03      1.797911e+12        6.006975e-07 no threshold; report EUR
   RABO               at1_instruments  4.899677e+09  4.948000e+09 4.832306e+07 9.862498e-03               NaN                 NaN no threshold; report EUR
    KBC                      net_fees  1.370212e+09  1.357000e+09 1.321225e+07 9.642483e-03               NaN                 NaN no threshold; report EUR
    DNB        total_operating_income  3.771589e+09  3.807887e+09 3.629768e+07 9.623976e-03               NaN                 NaN no threshold; report NOK
    SHB               interest_income  6.248918e+09  6.191109e+09 5.780895e+07 9.251034e-03               NaN                 NaN no threshold; report SEK
    ABN                admin_expenses  2.523776e+09  2.547000e+09 2.322379e+07 9.201999e-03               NaN                 NaN no threshold; report EUR
    SEB                           pbt  1.817702e+09  1.834252e+09 1.655009e+07 9.104950e-03               NaN                 NaN no threshold; report SEK
    GLE                  depreciation  7.748422e+08  7.680000e+08 6.842237e+06 8.830490e-03               NaN                 NaN no threshold; report EUR
    DBK               impairments_fin  9.019528e+08  8.940000e+08 7.952839e+06 8.817356e-03               NaN                 NaN no threshold; report EUR
   BBVA                  depreciation  7.424910e+08  7.490000e+08 6.509000e+06 8.766436e-03               NaN                 NaN no threshold; report EUR
    BPE              interest_expense  6.000206e+08  5.947880e+08 5.232637e+06 8.720762e-03               NaN                 NaN no threshold; report EUR
    GLE              interest_expense  1.766593e+10  1.781700e+10 1.510689e+08 8.551428e-03               NaN                 NaN no threshold; report EUR
   BAMI                  depreciation  1.539060e+08  1.551960e+08 1.290000e+06 8.381740e-03               NaN                 NaN no threshold; report EUR
   CABK                  depreciation  3.911950e+08  3.880000e+08 3.195000e+06 8.167282e-03               NaN                 NaN no threshold; report EUR
    DNB                admin_expenses  1.256818e+09  1.266980e+09 1.016178e+07 8.085323e-03               NaN                 NaN no threshold; report NOK
    UNI                      net_fees  2.643140e+08  2.621830e+08 2.131000e+06 8.062380e-03               NaN                 NaN no threshold; report EUR
    BKT                      net_fees  3.832180e+08  3.801440e+08 3.073973e+06 8.021474e-03               NaN                 NaN no threshold; report EUR
    CAG                  total_equity  1.510958e+11  1.522130e+11 1.117151e+09 7.393655e-03               NaN                 NaN no threshold; report EUR
   RABO        resolution_dgs_contrib  2.920980e+07  2.900000e+07 2.097950e+05 7.182351e-03               NaN                 NaN no threshold; report EUR
    DNB              interest_expense  5.336637e+09  5.298951e+09 3.768607e+07 7.061763e-03               NaN                 NaN no threshold; report NOK
   BBVA               dividend_income  7.547200e+07  7.600000e+07 5.280000e+05 6.995972e-03               NaN                 NaN no threshold; report EUR
   CABK               dividend_income  5.840600e+07  5.800000e+07 4.060000e+05 6.951341e-03               NaN                 NaN no threshold; report EUR
    SAN        gains_held_for_trading  6.961760e+08  7.010000e+08 4.824000e+06 6.929282e-03               NaN                 NaN no threshold; report EUR
   BAMI               impairments_fin  1.614800e+08  1.625440e+08 1.064000e+06 6.589051e-03               NaN                 NaN no threshold; report EUR
    SEB            deposits_customers  1.782612e+11  1.771053e+11 1.155959e+09 6.484636e-03               NaN                 NaN no threshold; report SEK
    DBK              interest_expense  1.512709e+10  1.502900e+10 9.809223e+07 6.484540e-03               NaN                 NaN no threshold; report EUR
    SAN        total_operating_income  2.899813e+10  2.918200e+10 1.838690e+08 6.340719e-03               NaN                 NaN no threshold; report EUR
    BKT               interest_income  1.981849e+09  1.969723e+09 1.212595e+07 6.118503e-03               NaN                 NaN no threshold; report EUR
   SWED                       cash_cb  2.932872e+10  2.915893e+10 1.697888e+08 5.789166e-03               NaN                 NaN no threshold; report SEK
   BBVA               impairments_fin  2.776280e+09  2.761000e+09 1.528000e+07 5.503768e-03               NaN                 NaN no threshold; report EUR
    UNI                           pbt  4.735160e+08  4.760370e+08 2.521000e+06 5.324002e-03               NaN                 NaN no threshold; report EUR
   INGA        total_operating_income  1.127898e+10  1.133900e+10 6.001500e+07 5.320958e-03               NaN                 NaN no threshold; report EUR
    ABN gains_derecognition_not_fvtpl -2.714019e+07 -2.700000e+07 1.401930e+05 5.165512e-03               NaN                 NaN no threshold; report EUR
    SAN                      net_fees  6.310215e+09  6.342000e+09 3.178500e+07 5.037071e-03               NaN                 NaN no threshold; report EUR
    UCG            deposits_customers  4.932116e+11  4.956840e+11 2.472363e+09 5.012782e-03               NaN                 NaN no threshold; report EUR
   BBVA                       cash_cb  4.021699e+10  4.001700e+10 1.999910e+08 4.972799e-03               NaN                 NaN no threshold; report EUR
   BAMI              interest_expense  1.293077e+09  1.286889e+09 6.188000e+06 4.785485e-03               NaN                 NaN no threshold; report EUR
    ABN               interest_income  7.198655e+09  7.233000e+09 3.434496e+07 4.771025e-03               NaN                 NaN no threshold; report EUR
   BAMI                    provisions -3.385000e+06 -3.401000e+06 1.600000e+04 4.726736e-03               NaN                 NaN no threshold; report EUR
    BPE                  depreciation  1.514781e+08  1.507760e+08 7.021410e+05 4.635263e-03               NaN                 NaN no threshold; report EUR
    UNI               interest_income  1.192879e+09  1.198407e+09 5.528000e+06 4.634167e-03               NaN                 NaN no threshold; report EUR
    UNI             total_liabilities  8.815711e+10  8.856531e+10 4.082040e+08 4.630415e-03               NaN                 NaN no threshold; report EUR
   SWED                 profit_owners  1.443297e+09  1.449972e+09 6.675179e+06 4.624951e-03               NaN                 NaN no threshold; report SEK
   SWED                           pat  1.442684e+09  1.449342e+09 6.657971e+06 4.614991e-03               NaN                 NaN no threshold; report SEK
    SEB                 profit_owners  1.442374e+09  1.448891e+09 6.517097e+06 4.518313e-03               NaN                 NaN no threshold; report SEK
    SEB                           pat  1.442374e+09  1.448891e+09 6.517097e+06 4.518313e-03               NaN                 NaN no threshold; report SEK
    UNI                  total_assets  9.515042e+10  9.555898e+10 4.085630e+08 4.293865e-03      9.515042e+10        1.603649e-16 no threshold; report EUR
    UCG                      net_fees  3.692442e+09  3.708000e+09 1.555848e+07 4.213603e-03               NaN                 NaN no threshold; report EUR
    ISP            deposits_customers  4.373961e+11  4.356380e+11 1.758082e+09 4.019427e-03               NaN                 NaN no threshold; report EUR
   BBVA                trading_assets  1.068193e+11  1.063960e+11 4.233130e+08 3.962888e-03               NaN                 NaN no threshold; report EUR
   BBVA                           pbt  8.391135e+09  8.424000e+09 3.286500e+07 3.916633e-03               NaN                 NaN no threshold; report EUR
    DBK                      net_fees  5.446687e+09  5.426000e+09 2.068660e+07 3.798015e-03               NaN                 NaN no threshold; report EUR
   BBVA                  total_equity  6.068382e+10  6.088700e+10 2.031850e+08 3.348257e-03               NaN                 NaN no threshold; report EUR
   BMPS               dividend_income  1.294226e+07  1.290000e+07 4.226000e+04 3.265272e-03               NaN                 NaN no threshold; report EUR
    SHB                       cash_cb  5.538848e+10  5.521096e+10 1.775169e+08 3.204943e-03               NaN                 NaN no threshold; report SEK
    SAN               impairments_fin  6.544163e+09  6.524000e+09 2.016300e+07 3.081066e-03               NaN                 NaN no threshold; report EUR
    BKT        total_operating_income  1.490153e+09  1.494420e+09 4.266949e+06 2.863430e-03               NaN                 NaN no threshold; report EUR
    DBK                           pbt  5.243544e+09  5.258000e+09 1.445615e+07 2.756943e-03               NaN                 NaN no threshold; report EUR
    BPE                admin_expenses  1.334900e+09  1.338481e+09 3.580961e+06 2.682569e-03               NaN                 NaN no threshold; report EUR
   BBVA                 profit_owners  5.433215e+09  5.447000e+09 1.378500e+07 2.537172e-03               NaN                 NaN no threshold; report EUR
    UCG               impairments_fin  2.154684e+08  2.160000e+08 5.316100e+05 2.467230e-03               NaN                 NaN no threshold; report EUR
    UCG        gains_hedge_accounting -6.415782e+07 -6.400000e+07 1.578240e+05 2.459934e-03               NaN                 NaN no threshold; report EUR
    DBK                 profit_owners  3.663940e+09  3.655000e+09 8.940202e+06 2.440051e-03               NaN                 NaN no threshold; report EUR
   SWED                  depreciation  9.493859e+07  9.516880e+07 2.302086e+05 2.424816e-03               NaN                 NaN no threshold; report SEK
    SAN            deposits_customers  1.005813e+12  1.008229e+12 2.416398e+09 2.402434e-03               NaN                 NaN no threshold; report EUR
    DBK                           pat  3.736635e+09  3.745000e+09 8.365387e+06 2.238749e-03               NaN                 NaN no threshold; report EUR
   BMPS                    provisions  3.046801e+07  3.040000e+07 6.800700e+04 2.232079e-03               NaN                 NaN no threshold; report EUR
    CAG                trading_assets  3.530318e+11  3.522570e+11 7.747624e+08 2.194597e-03               NaN                 NaN no threshold; report EUR
    CBK        gains_hedge_accounting  1.117568e+08  1.120000e+08 2.431794e+05 2.175970e-03               NaN                 NaN no threshold; report EUR
   BBVA                           pat  5.785426e+09  5.798000e+09 1.257400e+07 2.173392e-03               NaN                 NaN no threshold; report EUR
    ABN                  depreciation  7.883542e+07  7.900000e+07 1.645800e+05 2.087640e-03               NaN                 NaN no threshold; report EUR
   BMPS            deposits_customers  8.316393e+10  8.332840e+10 1.644712e+08 1.977674e-03               NaN                 NaN no threshold; report EUR
    SAN                  depreciation  1.622841e+09  1.626000e+09 3.159000e+06 1.946586e-03               NaN                 NaN no threshold; report EUR
   BAMI        gains_hedge_accounting  1.087900e+07  1.090000e+07 2.100000e+04 1.930324e-03               NaN                 NaN no threshold; report EUR
    SAN                    provisions  1.252417e+09  1.250000e+09 2.417000e+06 1.929868e-03               NaN                 NaN no threshold; report EUR
    BNP                  total_equity  1.313882e+11  1.316400e+11 2.518339e+08 1.916717e-03               NaN                 NaN no threshold; report EUR
    SAN                       cash_cb  1.758862e+11  1.755550e+11 3.311770e+08 1.882905e-03               NaN                 NaN no threshold; report EUR
    DBK        total_operating_income  1.629732e+10  1.632800e+10 3.068422e+07 1.882778e-03               NaN                 NaN no threshold; report EUR
    UNI                admin_expenses  4.254940e+08  4.262670e+08 7.730000e+05 1.816712e-03               NaN                 NaN no threshold; report EUR
    NDA               interest_income  9.014674e+09  8.999000e+09 1.567384e+07 1.738703e-03               NaN                 NaN no threshold; report EUR
    NDA                 profit_owners  2.459132e+09  2.455000e+09 4.131650e+06 1.680126e-03               NaN                 NaN no threshold; report EUR
    NDA                           pat  2.459132e+09  2.455000e+09 4.131650e+06 1.680126e-03               NaN                 NaN no threshold; report EUR
   BAMI                           pbt  1.653245e+09  1.650507e+09 2.738000e+06 1.656137e-03               NaN                 NaN no threshold; report EUR
    CBK                           pbt  1.859013e+09  1.862000e+09 2.986871e+06 1.606697e-03               NaN                 NaN no threshold; report EUR
    BNP                           pat  6.498768e+09  6.509000e+09 1.023165e+07 1.574398e-03               NaN                 NaN no threshold; report EUR
    SAN                           pbt  9.089942e+09  9.104000e+09 1.405800e+07 1.546545e-03               NaN                 NaN no threshold; report EUR
    NDA              interest_expense  5.380102e+09  5.372000e+09 8.101817e+06 1.505885e-03               NaN                 NaN no threshold; report EUR
    DBK             total_liabilities  1.318049e+12  1.319978e+12 1.929429e+09 1.463853e-03               NaN                 NaN no threshold; report EUR
   CABK          exchange_differences -2.083040e+08 -2.080000e+08 3.040000e+05 1.459405e-03               NaN                 NaN no threshold; report EUR
    SAN               dividend_income  4.703410e+08  4.710000e+08 6.590000e+05 1.401111e-03               NaN                 NaN no threshold; report EUR
    DBK                  total_assets  1.395880e+12  1.397830e+12 1.950133e+09 1.397064e-03      1.395880e+12        9.523034e-08 no threshold; report EUR
    ABN        total_operating_income  4.293763e+09  4.288000e+09 5.762614e+06 1.342090e-03               NaN                 NaN no threshold; report EUR
    SAB            impairments_nonfin  2.717800e+07  2.714200e+07 3.600000e+04 1.324601e-03               NaN                 NaN no threshold; report EUR
    CBK                       cash_cb  7.236730e+10  7.246300e+10 9.569712e+07 1.322381e-03               NaN                 NaN no threshold; report EUR
    UCG                    provisions  1.461879e+08  1.460000e+08 1.879280e+05 1.285523e-03               NaN                 NaN no threshold; report EUR
    ABN     loans_customers_allowance  1.265562e+09  1.264000e+09 1.561920e+06 1.234171e-03               NaN                 NaN no threshold; report EUR
    BPE         intangibles_deduction  4.405009e+08  4.410000e+08 4.991330e+05 1.133103e-03               NaN                 NaN no threshold; report EUR
    SAN                admin_expenses  1.072604e+10  1.073800e+10 1.196200e+07 1.115230e-03               NaN                 NaN no threshold; report EUR
    ABN               at1_instruments  4.220363e+09  4.225000e+09 4.637121e+06 1.098749e-03               NaN                 NaN no threshold; report EUR
 DANSKE                  total_equity  2.318181e+10  2.315686e+10 2.494870e+07 1.076219e-03               NaN                 NaN no threshold; report DKK
    ABN         intangibles_deduction  2.872920e+08  2.870000e+08 2.920110e+05 1.016426e-03               NaN                 NaN no threshold; report EUR
    CBK              interest_expense  5.623689e+09  5.618000e+09 5.689186e+06 1.011647e-03               NaN                 NaN no threshold; report EUR
    ABN             total_liabilities  3.868094e+11  3.864360e+11 3.734398e+08 9.654360e-04               NaN                 NaN no threshold; report EUR
   BAMI                admin_expenses  1.397331e+09  1.398628e+09 1.297000e+06 9.281981e-04               NaN                 NaN no threshold; report EUR
    ABN                  total_assets  4.142951e+11  4.139220e+11 3.731215e+08 9.006177e-04      4.142950e+11        2.933633e-07 no threshold; report EUR
   BMPS                admin_expenses  1.016912e+09  1.017800e+09 8.880510e+05 8.732821e-04               NaN                 NaN no threshold; report EUR
 DANSKE                 profit_owners  1.501455e+09  1.502676e+09 1.220398e+06 8.128097e-04               NaN                 NaN no threshold; report DKK
 DANSKE                           pat  1.501455e+09  1.502676e+09 1.220398e+06 8.128097e-04               NaN                 NaN no threshold; report DKK
    KBC                       cash_cb  3.600982e+10  3.603900e+10 2.918269e+07 8.104092e-04               NaN                 NaN no threshold; report EUR
   BMPS gains_derecognition_not_fvtpl  3.782958e+07  3.780000e+07 2.958100e+04 7.819542e-04               NaN                 NaN no threshold; report EUR
    CBK        resolution_dgs_contrib  1.621250e+08  1.620000e+08 1.249615e+05 7.707730e-04               NaN                 NaN no threshold; report EUR
    BKT        gains_hedge_accounting -3.712590e+05 -3.710000e+05 2.590000e+02 6.976262e-04               NaN                 NaN no threshold; report EUR
    BKT                    provisions  3.378388e+07  3.376200e+07 2.188100e+04 6.476757e-04               NaN                 NaN no threshold; report EUR
    SAN            impairments_nonfin  1.470920e+08  1.470000e+08 9.200000e+04 6.254589e-04               NaN                 NaN no threshold; report EUR
    ABN                           pbt  1.661985e+09  1.663000e+09 1.014633e+06 6.104945e-04               NaN                 NaN no threshold; report EUR
    CBK                      net_fees  2.016222e+09  2.015000e+09 1.222128e+06 6.061476e-04               NaN                 NaN no threshold; report EUR
    NDA                  total_equity  3.034872e+10  3.036700e+10 1.828324e+07 6.024387e-04               NaN                 NaN no threshold; report EUR
    UCG               interest_income  1.383276e+10  1.382500e+10 7.755725e+06 5.606782e-04               NaN                 NaN no threshold; report EUR
   RABO                admin_expenses  3.989217e+09  3.987000e+09 2.216619e+06 5.556527e-04               NaN                 NaN no threshold; report EUR
   RABO         intangibles_deduction  6.103314e+08  6.100000e+08 3.314204e+05 5.430172e-04               NaN                 NaN no threshold; report EUR
   BAMI     loans_customers_allowance  1.694894e+09  1.694000e+09 8.940000e+05 5.274666e-04               NaN                 NaN no threshold; report EUR
    UCG               dividend_income  5.487112e+08  5.490000e+08 2.888460e+05 5.264081e-04               NaN                 NaN no threshold; report EUR
   RABO                     npl_gross  9.183989e+09  9.180000e+09 3.988516e+06 4.342902e-04               NaN                 NaN no threshold; report EUR
    UCG                           pbt  8.202446e+09  8.206000e+09 3.553655e+06 4.332433e-04               NaN                 NaN no threshold; report EUR
    KBC                trading_assets  1.052856e+10  1.053300e+10 4.441578e+06 4.218600e-04               NaN                 NaN no threshold; report EUR
    BPE     loans_customers_allowance  1.907232e+09  1.908000e+09 7.678130e+05 4.025797e-04               NaN                 NaN no threshold; report EUR
   RABO                      net_fees  1.209518e+09  1.210000e+09 4.815290e+05 3.981163e-04               NaN                 NaN no threshold; report EUR
    ABN                 npl_allowance  9.413665e+08  9.410000e+08 3.665490e+05 3.893797e-04               NaN                 NaN no threshold; report EUR
    BPE            deposits_customers  1.074661e+11  1.074257e+11 4.043406e+07 3.762493e-04               NaN                 NaN no threshold; report EUR
    CBK                 profit_owners  1.296470e+09  1.296000e+09 4.704742e+05 3.628885e-04               NaN                 NaN no threshold; report EUR
    DBK               interest_income  2.252796e+10  2.253600e+10 8.040646e+06 3.569185e-04               NaN                 NaN no threshold; report EUR
    ISP                           pat  5.233742e+09  5.232000e+09 1.741745e+06 3.327915e-04               NaN                 NaN no threshold; report EUR
    SAN                  total_equity  1.089509e+11  1.089850e+11 3.406900e+07 3.127004e-04               NaN                 NaN no threshold; report EUR
    UCG               at1_instruments  4.959571e+09  4.961000e+09 1.429000e+06 2.881298e-04               NaN                 NaN no threshold; report EUR
    CBK                  total_equity  3.521888e+10  3.522900e+10 1.012346e+07 2.874440e-04               NaN                 NaN no threshold; report EUR
   CABK        gains_held_for_trading  3.119110e+08  3.120000e+08 8.900000e+04 2.853378e-04               NaN                 NaN no threshold; report EUR
   BAMI                 npl_allowance  1.248344e+09  1.248000e+09 3.440000e+05 2.755651e-04               NaN                 NaN no threshold; report EUR
    DBK                  total_equity  7.783130e+10  7.785200e+10 2.070409e+07 2.660124e-04               NaN                 NaN no threshold; report EUR
   CABK                           pat  2.955762e+09  2.955000e+09 7.620000e+05 2.578015e-04               NaN                 NaN no threshold; report EUR
    ISP                 npl_allowance  4.950265e+09  4.949000e+09 1.265279e+06 2.555982e-04               NaN                 NaN no threshold; report EUR
   RABO                 npl_allowance  1.540353e+09  1.540000e+09 3.534830e+05 2.294817e-04               NaN                 NaN no threshold; report EUR
    DNB                      net_fees  6.747561e+08  6.749109e+08 1.548381e+05 2.294726e-04               NaN                 NaN no threshold; report NOK
    SAN                trading_assets  2.347813e+11  2.348340e+11 5.274900e+07 2.246730e-04               NaN                 NaN no threshold; report EUR
    SAB                      net_fees  6.944950e+08  6.943490e+08 1.460000e+05 2.102247e-04               NaN                 NaN no threshold; report EUR
    SAB                           pbt  1.430798e+09  1.430502e+09 2.960000e+05 2.068776e-04               NaN                 NaN no threshold; report EUR
    SAB               interest_income  4.429154e+09  4.428241e+09 9.130000e+05 2.061342e-04               NaN                 NaN no threshold; report EUR
    ABN                      net_fees  9.992044e+08  9.990000e+08 2.044050e+05 2.045678e-04               NaN                 NaN no threshold; report EUR
   BMPS              interest_expense  8.894816e+08  8.893000e+08 1.815800e+05 2.041414e-04               NaN                 NaN no threshold; report EUR
    CAG                           pat  5.346940e+09  5.348000e+09 1.060075e+06 1.982582e-04               NaN                 NaN no threshold; report EUR
   BAMI                  total_equity  1.531282e+10  1.531575e+10 2.924000e+06 1.909510e-04               NaN                 NaN no threshold; report EUR
   RABO                 profit_owners  2.659510e+09  2.660000e+09 4.900220e+05 1.842527e-04               NaN                 NaN no threshold; report EUR
    NDA     loans_customers_allowance  1.506260e+09  1.506000e+09 2.598871e+05 1.725380e-04               NaN                 NaN no threshold; report EUR
    NDA               at1_instruments  2.983492e+09  2.984000e+09 5.077635e+05 1.701910e-04               NaN                 NaN no threshold; report EUR
    NDA         intangibles_deduction  2.739534e+09  2.740000e+09 4.657501e+05 1.700107e-04               NaN                 NaN no threshold; report EUR
   BAMI               at1_instruments  1.787273e+09  1.787000e+09 2.732900e+05 1.529089e-04               NaN                 NaN no threshold; report EUR
    BKT                           pbt  7.657583e+08  7.656430e+08 1.152720e+05 1.505331e-04               NaN                 NaN no threshold; report EUR
   CABK                 profit_owners  2.951443e+09  2.951000e+09 4.430000e+05 1.500961e-04               NaN                 NaN no threshold; report EUR
    ISP     loans_customers_allowance  6.986030e+09  6.985000e+09 1.029502e+06 1.473658e-04               NaN                 NaN no threshold; report EUR
   SWED                  total_equity  1.872623e+10  1.872355e+10 2.681021e+06 1.431693e-04               NaN                 NaN no threshold; report SEK
    BPE        gains_hedge_accounting -3.464490e+06 -3.464000e+06 4.900000e+02 1.414350e-04               NaN                 NaN no threshold; report EUR
    UCG                  total_equity  6.842761e+10  6.841800e+10 9.605307e+06 1.403718e-04               NaN                 NaN no threshold; report EUR
   CABK            deposits_customers  4.546126e+11  4.545490e+11 6.364500e+07 1.399983e-04               NaN                 NaN no threshold; report EUR
   INGA                 profit_owners  3.129602e+09  3.130000e+09 3.980000e+05 1.271727e-04               NaN                 NaN no threshold; report EUR
    ISP                trading_assets  4.615774e+10  4.615200e+10 5.740165e+06 1.243597e-04               NaN                 NaN no threshold; report EUR
    BPE                     npl_gross  2.381705e+09  2.382000e+09 2.954500e+05 1.240498e-04               NaN                 NaN no threshold; report EUR
    ISP                     npl_gross  9.902829e+09  9.904000e+09 1.171159e+06 1.182651e-04               NaN                 NaN no threshold; report EUR
    ABN                           pat  1.225144e+09  1.225000e+09 1.441350e+05 1.176474e-04               NaN                 NaN no threshold; report EUR
   INGA                           pat  3.256378e+09  3.256000e+09 3.780000e+05 1.160799e-04               NaN                 NaN no threshold; report EUR
    CAG                 profit_owners  4.802450e+09  4.803000e+09 5.497149e+05 1.144655e-04               NaN                 NaN no threshold; report EUR
   RABO                           pbt  3.737594e+09  3.738000e+09 4.062720e+05 1.086988e-04               NaN                 NaN no threshold; report EUR
    SAB                trading_assets  3.755218e+09  3.754816e+09 4.020000e+05 1.070510e-04               NaN                 NaN no threshold; report EUR
    DBK     loans_customers_allowance  5.975632e+09  5.975000e+09 6.317160e+05 1.057153e-04               NaN                 NaN no threshold; report EUR
   BBVA     loans_customers_allowance  1.166813e+10  1.166700e+10 1.133000e+06 9.710208e-05               NaN                 NaN no threshold; report EUR
    UNI              interest_expense  4.558900e+08  4.558460e+08 4.400000e+04 9.651451e-05               NaN                 NaN no threshold; report EUR
    UCG              interest_expense  6.810638e+09  6.810000e+09 6.379420e+05 9.366846e-05               NaN                 NaN no threshold; report EUR
   BAMI         intangibles_deduction  3.054739e+09  3.055000e+09 2.610960e+05 8.547244e-05               NaN                 NaN no threshold; report EUR
   SWED                 npl_allowance  3.378024e+08  3.377742e+08 2.825999e+04 8.365834e-05               NaN                 NaN no threshold; report SEK
   BMPS                  total_assets  1.255844e+11  1.255741e+11 1.026956e+07 8.177422e-05      1.255843e+11        1.876348e-07 no threshold; report EUR
   RABO     loans_customers_allowance  2.285185e+09  2.285000e+09 1.845380e+05 8.075409e-05               NaN                 NaN no threshold; report EUR
    SAB        gains_held_for_trading  6.708380e+08  6.707840e+08 5.400000e+04 8.049633e-05               NaN                 NaN no threshold; report EUR
    ISP                 profit_owners  5.216419e+09  5.216000e+09 4.190360e+05 8.033020e-05               NaN                 NaN no threshold; report EUR
    BNP                 profit_owners  6.208502e+09  6.209000e+09 4.981800e+05 8.024158e-05               NaN                 NaN no threshold; report EUR
    GLE                 profit_owners  3.060769e+09  3.061000e+09 2.309649e+05 7.545975e-05               NaN                 NaN no threshold; report EUR
   BMPS               impairments_fin  1.509114e+08  1.509000e+08 1.137100e+04 7.534886e-05               NaN                 NaN no threshold; report EUR
    UNI                       cash_cb  4.863443e+09  4.863806e+09 3.630000e+05 7.463848e-05               NaN                 NaN no threshold; report EUR
    SAN                 profit_owners  6.832517e+09  6.833000e+09 4.830000e+05 7.069137e-05               NaN                 NaN no threshold; report EUR
    ABN                     npl_gross  5.567388e+09  5.567000e+09 3.875230e+05 6.960590e-05               NaN                 NaN no threshold; report EUR
    SAN                 npl_allowance  1.424398e+10  1.424300e+10 9.800000e+05 6.880100e-05               NaN                 NaN no threshold; report EUR
   INGA                      net_fees  2.215848e+09  2.216000e+09 1.520000e+05 6.859676e-05               NaN                 NaN no threshold; report EUR
    GLE                 npl_allowance  6.156411e+09  6.156000e+09 4.112781e+05 6.680485e-05               NaN                 NaN no threshold; report EUR
    BNP         intangibles_deduction  7.535497e+09  7.535000e+09 4.965400e+05 6.589347e-05               NaN                 NaN no threshold; report EUR
    DBK                 npl_allowance  4.642695e+09  4.643000e+09 3.045642e+05 6.560072e-05               NaN                 NaN no threshold; report EUR
   BMPS                      net_fees  7.983480e+08  7.984000e+08 5.199300e+04 6.512573e-05               NaN                 NaN no threshold; report EUR
    CBK                           pat  1.405910e+09  1.406000e+09 9.044640e+04 6.433301e-05               NaN                 NaN no threshold; report EUR
    NDA                     npl_gross  3.666768e+09  3.667000e+09 2.321943e+05 6.332397e-05               NaN                 NaN no threshold; report EUR
    UNI               impairments_fin  6.383500e+07  6.383100e+07 4.000000e+03 6.266155e-05               NaN                 NaN no threshold; report EUR
   CABK               impairments_fin  4.830300e+08  4.830000e+08 3.000000e+04 6.210794e-05               NaN                 NaN no threshold; report EUR
    UCG                 npl_allowance  5.314322e+09  5.314000e+09 3.222460e+05 6.063727e-05               NaN                 NaN no threshold; report EUR
   SWED     loans_customers_allowance  6.967619e+08  6.967209e+08 4.099942e+04 5.884279e-05               NaN                 NaN no threshold; report SEK
    SAB                 profit_owners  9.753370e+08  9.752800e+08 5.700000e+04 5.844134e-05               NaN                 NaN no threshold; report EUR
    SAB                           pat  9.764200e+08  9.763630e+08 5.700000e+04 5.837652e-05               NaN                 NaN no threshold; report EUR
   SWED                     npl_gross  1.160160e+09  1.160095e+09 6.513255e+04 5.614100e-05               NaN                 NaN no threshold; report SEK
    CAG     loans_customers_allowance  2.167881e+10  2.168000e+10 1.194504e+06 5.510006e-05               NaN                 NaN no threshold; report EUR
    NDA                 npl_allowance  1.042056e+09  1.042000e+09 5.631355e+04 5.404079e-05               NaN                 NaN no threshold; report EUR
   BBVA                 npl_allowance  7.429600e+09  7.430000e+09 4.000000e+05 5.383870e-05               NaN                 NaN no threshold; report EUR
    BPE                 npl_allowance  1.324929e+09  1.325000e+09 7.096600e+04 5.356211e-05               NaN                 NaN no threshold; report EUR
    ABN                 profit_owners  1.224941e+09  1.225000e+09 5.856200e+04 4.780800e-05               NaN                 NaN no threshold; report EUR
    UNI                  depreciation  4.532000e+07  4.532200e+07 2.000000e+03 4.413063e-05               NaN                 NaN no threshold; report EUR
   BAMI                           pat  1.222843e+09  1.222790e+09 5.300000e+04 4.334162e-05               NaN                 NaN no threshold; report EUR
    DNB     loans_customers_allowance  6.218655e+08  6.218390e+08 2.656090e+04 4.271165e-05               NaN                 NaN no threshold; report NOK
   BMPS                           pat  8.923632e+08  8.924000e+08 3.681100e+04 4.125114e-05               NaN                 NaN no threshold; report EUR
    UCG                 profit_owners  6.114749e+09  6.115000e+09 2.513900e+05 4.111207e-05               NaN                 NaN no threshold; report EUR
   RABO                           pat  2.693893e+09  2.694000e+09 1.067970e+05 3.964411e-05               NaN                 NaN no threshold; report EUR
    UCG         intangibles_deduction  2.541900e+09  2.542000e+09 1.000000e+05 3.934065e-05               NaN                 NaN no threshold; report EUR
    GLE         intangibles_deduction  7.095270e+09  7.095000e+09 2.699746e+05 3.804994e-05               NaN                 NaN no threshold; report EUR
    BNP                 npl_allowance  1.303349e+10  1.303300e+10 4.899810e+05 3.759400e-05               NaN                 NaN no threshold; report EUR
    GLE     loans_customers_allowance  8.705682e+09  8.706000e+09 3.180925e+05 3.653850e-05               NaN                 NaN no threshold; report EUR
    SAB                admin_expenses  1.278416e+09  1.278462e+09 4.600000e+04 3.598203e-05               NaN                 NaN no threshold; report EUR
 DANSKE                      net_fees  9.471300e+08  9.470972e+08 3.280209e+04 3.463314e-05               NaN                 NaN no threshold; report DKK
   BMPS                 profit_owners  8.923695e+08  8.924000e+08 3.054000e+04 3.422349e-05               NaN                 NaN no threshold; report EUR
    DBK                     npl_gross  1.491451e+10  1.491500e+10 4.919155e+05 3.298235e-05               NaN                 NaN no threshold; report EUR
    BPE               at1_instruments  1.115964e+09  1.116000e+09 3.568600e+04 3.197773e-05               NaN                 NaN no threshold; report EUR
   BMPS                           pbt  8.571752e+08  8.572000e+08 2.484700e+04 2.898707e-05               NaN                 NaN no threshold; report EUR
    BNP     loans_customers_allowance  1.661053e+10  1.661100e+10 4.737710e+05 2.852234e-05               NaN                 NaN no threshold; report EUR
    SAB            deposits_customers  1.833893e+11  1.833841e+11 5.132000e+06 2.798419e-05               NaN                 NaN no threshold; report EUR
    BPE               debt_securities  2.981924e+10  2.982000e+10 7.587590e+05 2.544528e-05               NaN                 NaN no threshold; report EUR
    CAG                 npl_allowance  1.291530e+10  1.291500e+10 3.028850e+05 2.345163e-05               NaN                 NaN no threshold; report EUR
    SAN         intangibles_deduction  1.529664e+10  1.529700e+10 3.552480e+05 2.322392e-05               NaN                 NaN no threshold; report EUR
   BAMI                 profit_owners  1.214492e+09  1.214465e+09 2.700000e+04 2.223152e-05               NaN                 NaN no threshold; report EUR
    UCG                     npl_gross  1.172375e+10  1.172400e+10 2.524460e+05 2.153288e-05               NaN                 NaN no threshold; report EUR
   SWED               at1_instruments  1.401995e+09  1.401965e+09 3.005428e+04 2.143680e-05               NaN                 NaN no threshold; report SEK
    DBK         intangibles_deduction  4.996895e+09  4.997000e+09 1.045405e+05 2.092110e-05               NaN                 NaN no threshold; report EUR
   SWED         intangibles_deduction  1.660821e+09  1.660790e+09 3.032342e+04 1.825809e-05               NaN                 NaN no threshold; report SEK
   BBVA                     npl_gross  1.413625e+10  1.413600e+10 2.500000e+05 1.768503e-05               NaN                 NaN no threshold; report EUR
    SAB             total_liabilities  2.378860e+11  2.378821e+11 3.885000e+06 1.633135e-05               NaN                 NaN no threshold; report EUR
    BKT              interest_expense  8.686281e+08  8.686140e+08 1.405400e+04 1.617954e-05               NaN                 NaN no threshold; report EUR
   BAMI                     npl_gross  2.904953e+09  2.905000e+09 4.700000e+04 1.617926e-05               NaN                 NaN no threshold; report EUR
    SAB                  total_assets  2.523766e+11  2.523727e+11 3.885000e+06 1.539366e-05      2.523766e+11        4.754799e-10 no threshold; report EUR
    BNP                     npl_gross  2.687041e+10  2.687000e+10 4.132200e+05 1.537825e-05               NaN                 NaN no threshold; report EUR
    SAN                     npl_gross  3.592445e+10  3.592500e+10 5.460000e+05 1.519856e-05               NaN                 NaN no threshold; report EUR
    BPE        loans_households_gross  4.484940e+10  4.485000e+10 6.047020e+05 1.348295e-05               NaN                 NaN no threshold; report EUR
    CAG              interest_expense  2.130729e+10  2.130700e+10 2.870709e+05 1.347290e-05               NaN                 NaN no threshold; report EUR
   BAMI        loans_households_gross  3.268756e+10  3.268800e+10 4.380000e+05 1.339959e-05               NaN                 NaN no threshold; report EUR
   BAMI               debt_securities  4.675160e+10  4.675100e+10 6.050000e+05 1.294073e-05               NaN                 NaN no threshold; report EUR
    SAN     loans_customers_allowance  2.105627e+10  2.105600e+10 2.660000e+05 1.263282e-05               NaN                 NaN no threshold; report EUR
   BMPS                  total_equity  1.147047e+10  1.147060e+10 1.341540e+05 1.169560e-05               NaN                 NaN no threshold; report EUR
    ABN                  total_equity  2.748568e+10  2.748600e+10 3.182300e+05 1.157803e-05               NaN                 NaN no threshold; report EUR
    BKT          exchange_differences -2.131494e+08 -2.131470e+08 2.398000e+03 1.125032e-05               NaN                 NaN no threshold; report EUR
    BKT               dividend_income  1.808382e+07  1.808400e+07 1.840000e+02 1.017484e-05               NaN                 NaN no threshold; report EUR
    CAG                     npl_gross  2.643175e+10  2.643200e+10 2.508067e+05 9.488840e-06               NaN                 NaN no threshold; report EUR
    GLE                     npl_gross  1.400687e+10  1.400700e+10 1.313767e+05 9.379448e-06               NaN                 NaN no threshold; report EUR
   CABK                  total_equity  3.743465e+10  3.743500e+10 3.480000e+05 9.296200e-06               NaN                 NaN no threshold; report EUR
    DBK               debt_securities  7.662761e+10  7.662700e+10 6.143959e+05 8.017944e-06               NaN                 NaN no threshold; report EUR
    BPE         loans_customers_gross  9.477975e+10  9.477900e+10 7.493920e+05 7.906668e-06               NaN                 NaN no threshold; report EUR
   INGA                           pbt  4.493034e+09  4.493000e+09 3.400000e+04 7.567270e-06               NaN                 NaN no threshold; report EUR
   RABO                     loans_all  5.074487e+11  5.074450e+11 3.714918e+06 7.320775e-06               NaN                 NaN no threshold; report EUR
    UCG     loans_customers_allowance  8.949936e+09  8.950000e+09 6.442700e+04 7.198599e-06               NaN                 NaN no threshold; report EUR
    SAN                           pat  6.737048e+09  6.737000e+09 4.800000e+04 7.124782e-06               NaN                 NaN no threshold; report EUR
   BMPS               interest_income  1.971114e+09  1.971100e+09 1.400100e+04 7.103090e-06               NaN                 NaN no threshold; report EUR
   BAMI         loans_customers_gross  1.030993e+11  1.031000e+11 7.010000e+05 6.799270e-06               NaN                 NaN no threshold; report EUR
    ABN         loans_customers_gross  2.907298e+11  2.907280e+11 1.786733e+06 6.145683e-06               NaN                 NaN no threshold; report EUR
    SAN               debt_securities  1.675381e+11  1.675390e+11 9.380000e+05 5.598728e-06               NaN                 NaN no threshold; report EUR
    ISP               debt_securities  1.600758e+11  1.600750e+11 8.327190e+05 5.202028e-06               NaN                 NaN no threshold; report EUR
   RABO                  total_equity  5.476127e+10  5.476100e+10 2.717620e+05 4.962668e-06               NaN                 NaN no threshold; report EUR
    ABN        loans_households_gross  1.717758e+11  1.717750e+11 8.271010e+05 4.815002e-06               NaN                 NaN no threshold; report EUR
    ABN               debt_securities  4.917422e+10  4.917400e+10 2.246900e+05 4.569264e-06               NaN                 NaN no threshold; report EUR
    GLE               debt_securities  9.035834e+10  9.035800e+10 3.431136e+05 3.797254e-06               NaN                 NaN no threshold; report EUR
    UCG               debt_securities  1.734634e+11  1.734640e+11 6.480390e+05 3.735884e-06               NaN                 NaN no threshold; report EUR
    CAG               debt_securities  1.758304e+11  1.758310e+11 6.438480e+05 3.661757e-06               NaN                 NaN no threshold; report EUR
   BBVA               debt_securities  9.920336e+10  9.920300e+10 3.610000e+05 3.638990e-06               NaN                 NaN no threshold; report EUR
    ISP         intangibles_deduction  7.815974e+09  7.816000e+09 2.634200e+04 3.370277e-06               NaN                 NaN no threshold; report EUR
    ISP                  total_equity  6.665779e+10  6.665800e+10 2.147450e+05 3.221604e-06               NaN                 NaN no threshold; report EUR
    UNI                           pat  3.378480e+08  3.378470e+08 1.000000e+03 2.959911e-06               NaN                 NaN no threshold; report EUR
   BMPS         intangibles_deduction  1.048397e+08  1.048400e+08 2.990000e+02 2.851973e-06               NaN                 NaN no threshold; report EUR
   RABO         loans_customers_gross  4.768233e+11  4.768220e+11 1.348917e+06 2.828966e-06               NaN                 NaN no threshold; report EUR
    ISP        loans_households_gross  1.800385e+11  1.800390e+11 4.930120e+05 2.738370e-06               NaN                 NaN no threshold; report EUR
    BPE               impairments_fin  1.401674e+08  1.401670e+08 3.720000e+02 2.653970e-06               NaN                 NaN no threshold; report EUR
   BAMI                     loans_all  1.062453e+11  1.062450e+11 2.740000e+05 2.578938e-06               NaN                 NaN no threshold; report EUR
    SAB              interest_expense  2.003345e+09  2.003340e+09 5.000000e+03 2.495826e-06               NaN                 NaN no threshold; report EUR
    BNP               debt_securities  2.375784e+11  2.375790e+11 5.857360e+05 2.465443e-06               NaN                 NaN no threshold; report EUR
    BPE               dividend_income  4.302310e+07  4.302300e+07 1.010000e+02 2.347576e-06               NaN                 NaN no threshold; report EUR
    ABN                     loans_all  3.105067e+11  3.105060e+11 7.093510e+05 2.284495e-06               NaN                 NaN no threshold; report EUR
   BBVA         loans_customers_gross  4.384271e+11  4.384280e+11 9.360000e+05 2.134905e-06               NaN                 NaN no threshold; report EUR
    NDA               debt_securities  5.564889e+10  5.564900e+10 1.143781e+05 2.055354e-06               NaN                 NaN no threshold; report EUR
    NDA                     loans_all  3.431383e+11  3.431390e+11 6.691014e+05 1.949947e-06               NaN                 NaN no threshold; report EUR
    DBK        loans_households_gross  1.905007e+11  1.905010e+11 3.235481e+05 1.698409e-06               NaN                 NaN no threshold; report EUR
    UCG                           pat  6.149010e+09  6.149000e+09 9.783000e+03 1.590988e-06               NaN                 NaN no threshold; report EUR
    GLE         loans_customers_gross  4.731353e+11  4.731360e+11 6.679978e+05 1.411854e-06               NaN                 NaN no threshold; report EUR
    UCG                     loans_all  4.936763e+11  4.936770e+11 6.920710e+05 1.401872e-06               NaN                 NaN no threshold; report EUR
   BBVA         intangibles_deduction  1.596002e+09  1.596000e+09 2.000000e+03 1.253131e-06               NaN                 NaN no threshold; report EUR
    SEB                  total_equity  1.942980e+10  1.942978e+10 2.378747e+04 1.224277e-06               NaN                 NaN no threshold; report SEK
    NDA         loans_customers_gross  3.382034e+11  3.382030e+11 4.108329e+05 1.214751e-06               NaN                 NaN no threshold; report EUR
    ISP         loans_customers_gross  4.205255e+11  4.205260e+11 5.005370e+05 1.190266e-06               NaN                 NaN no threshold; report EUR
    DBK                     loans_all  7.327751e+11  7.327760e+11 8.631039e+05 1.177856e-06               NaN                 NaN no threshold; report EUR
   RABO               debt_securities  2.721697e+10  2.721700e+10 2.878800e+04 1.057722e-06               NaN                 NaN no threshold; report EUR
    GLE        loans_households_gross  1.812548e+11  1.812550e+11 1.764438e+05 9.734573e-07               NaN                 NaN no threshold; report EUR
   INGA                  total_equity  5.014605e+10  5.014600e+10 4.700000e+04 9.372623e-07               NaN                 NaN no threshold; report EUR
    UCG                trading_assets  6.037095e+10  6.037100e+10 5.445400e+04 9.019902e-07               NaN                 NaN no threshold; report EUR
    SAN        loans_households_gross  5.788165e+11  5.788160e+11 4.870000e+05 8.413720e-07               NaN                 NaN no threshold; report EUR
   BMPS                trading_assets  8.262107e+09  8.262100e+09 6.572000e+03 7.954388e-07               NaN                 NaN no threshold; report EUR
    ISP                     loans_all  4.495866e+11  4.495870e+11 3.550030e+05 7.896209e-07               NaN                 NaN no threshold; report EUR
    SAN                     loans_all  1.073587e+12  1.073588e+12 8.070000e+05 7.516856e-07               NaN                 NaN no threshold; report EUR
   SWED         loans_customers_gross  1.654226e+11  1.654225e+11 1.234468e+05 7.462511e-07               NaN                 NaN no threshold; report SEK
    BNP         loans_customers_gross  9.233787e+11  9.233780e+11 6.629890e+05 7.180034e-07               NaN                 NaN no threshold; report EUR
    UCG        loans_households_gross  1.408181e+11  1.408180e+11 8.777000e+04 6.232864e-07               NaN                 NaN no threshold; report EUR
   BMPS     loans_customers_allowance  1.929656e+09  1.929655e+09 1.166000e+03 6.042527e-07               NaN                 NaN no threshold; report EUR
    BKT                           pat  5.416927e+08  5.416930e+08 3.230000e+02 5.962791e-07               NaN                 NaN no threshold; report EUR
    BKT                 profit_owners  5.416927e+08  5.416930e+08 3.230000e+02 5.962791e-07               NaN                 NaN no threshold; report EUR
   BBVA        loans_households_gross  1.903381e+11  1.903380e+11 1.070000e+05 5.621575e-07               NaN                 NaN no threshold; report EUR
   SWED                     loans_all  1.695585e+11  1.695584e+11 8.540797e+04 5.037080e-07               NaN                 NaN no threshold; report SEK
   SWED               debt_securities  1.472659e+10  1.472660e+10 7.356569e+03 4.995434e-07               NaN                 NaN no threshold; report SEK
    GLE                     loans_all  5.065102e+11  5.065100e+11 2.356225e+05 4.651880e-07               NaN                 NaN no threshold; report EUR
    SAN         loans_customers_gross  1.000489e+12  1.000489e+12 4.260000e+05 4.257920e-07               NaN                 NaN no threshold; report EUR
    DBK         loans_customers_gross  6.820533e+11  6.820530e+11 2.508040e+05 3.677190e-07               NaN                 NaN no threshold; report EUR
    UCG         loans_customers_gross  4.427608e+11  4.427610e+11 1.597520e+05 3.608088e-07               NaN                 NaN no threshold; report EUR
   BBVA                     loans_all  4.715868e+11  4.715870e+11 1.570000e+05 3.329185e-07               NaN                 NaN no threshold; report EUR
   RABO        loans_households_gross  2.078971e+11  2.078970e+11 6.903200e+04 3.320489e-07               NaN                 NaN no threshold; report EUR
   RABO                  total_assets  6.358652e+11  6.358650e+11 2.061730e+05 3.242401e-07      6.358650e+11        3.242401e-07 no threshold; report EUR
    BPE                           pbt  1.368677e+09  1.368677e+09 4.360000e+02 3.185559e-07               NaN                 NaN no threshold; report EUR
   INGA             total_liabilities  1.036614e+12  1.036614e+12 2.910000e+05 2.807217e-07               NaN                 NaN no threshold; report EUR
    BKT        gains_held_for_trading  2.164591e+08  2.164590e+08 6.000000e+01 2.771887e-07               NaN                 NaN no threshold; report EUR
    CAG         loans_customers_gross  1.209189e+12  1.209189e+12 3.195124e+05 2.642370e-07               NaN                 NaN no threshold; report EUR
    CAG                     loans_all  1.345533e+12  1.345533e+12 3.474908e+05 2.582552e-07               NaN                 NaN no threshold; report EUR
    BPE                      net_fees  1.047525e+09  1.047525e+09 2.590000e+02 2.472495e-07               NaN                 NaN no threshold; report EUR
    BNP        loans_households_gross  3.387801e+11  3.387800e+11 8.085700e+04 2.386711e-07               NaN                 NaN no threshold; report EUR
   INGA                  total_assets  1.086760e+12  1.086760e+12 2.440000e+05 2.245206e-07      1.086760e+12        2.245206e-07 no threshold; report EUR
   BMPS                     npl_gross  3.064444e+09  3.064444e+09 4.950000e+02 1.615301e-07               NaN                 NaN no threshold; report EUR
   BMPS                 npl_allowance  1.408400e+09  1.408400e+09 2.010000e+02 1.427151e-07               NaN                 NaN no threshold; report EUR
   SWED        loans_households_gross  1.062151e+11  1.062150e+11 1.309828e+04 1.233185e-07               NaN                 NaN no threshold; report SEK
   RABO             total_liabilities  5.811039e+11  5.811040e+11 6.558000e+04 1.128542e-07               NaN                 NaN no threshold; report EUR
    BPE               interest_income  2.220806e+09  2.220806e+09 1.630000e+02 7.339677e-08               NaN                 NaN no threshold; report EUR
    NDA        loans_households_gross  1.936110e+11  1.936110e+11 1.410475e+04 7.285097e-08               NaN                 NaN no threshold; report EUR
    BNP                     loans_all  9.636181e+11  9.636180e+11 6.235000e+04 6.470406e-08               NaN                 NaN no threshold; report EUR
   CABK         intangibles_deduction  3.566832e+09  3.566832e+09 2.240000e+02 6.280083e-08               NaN                 NaN no threshold; report EUR
    BPE                  total_equity  1.163390e+10  1.163390e+10 7.270000e+02 6.248979e-08               NaN                 NaN no threshold; report EUR
    BPE                trading_assets  8.035200e+08  8.035200e+08 4.700000e+01 5.849263e-08               NaN                 NaN no threshold; report EUR
    BPE                 profit_owners  9.034690e+08  9.034690e+08 2.800000e+01 3.099166e-08               NaN                 NaN no threshold; report EUR
    CAG        loans_households_gross  6.441880e+11  6.441880e+11 1.946470e+04 3.021587e-08               NaN                 NaN no threshold; report EUR
    BPE                     loans_all  9.512500e+10  9.512500e+10 2.349000e+03 2.469382e-08               NaN                 NaN no threshold; report EUR
    BPE                           pat  9.200890e+08  9.200890e+08 2.000000e+01 2.173703e-08               NaN                 NaN no threshold; report EUR
    DNB         loans_customers_gross  1.964786e+11  1.964786e+11 4.224935e+03 2.150329e-08               NaN                 NaN no threshold; report NOK
   BMPS        loans_households_gross  3.662574e+10  3.662574e+10 5.060000e+02 1.381542e-08               NaN                 NaN no threshold; report EUR
   CABK               debt_securities  9.293359e+10  9.293359e+10 1.000000e+03 1.076037e-08               NaN                 NaN no threshold; report EUR
   BMPS         loans_customers_gross  8.216746e+10  8.216746e+10 8.070000e+02 9.821406e-09               NaN                 NaN no threshold; report EUR
   BMPS               debt_securities  1.253381e+10  1.253381e+10 6.900000e+01 5.505111e-09               NaN                 NaN no threshold; report EUR
   CABK        loans_households_gross  1.871196e+11  1.871196e+11 1.000000e+03 5.344175e-09               NaN                 NaN no threshold; report EUR
   BMPS                     loans_all  8.398345e+10  8.398345e+10 2.760000e+02 3.286362e-09               NaN                 NaN no threshold; report EUR
   CABK         loans_customers_gross  3.757346e+11  3.757346e+11 1.000000e+03 2.661453e-09               NaN                 NaN no threshold; report EUR
    BPE                  total_assets  1.445282e+11  1.445282e+11 1.470000e+02 1.017103e-09      1.445282e+11        1.017103e-09 no threshold; report EUR
    SEB                 npl_allowance  2.716394e+08  2.716394e+08 3.517574e-02 1.294943e-10               NaN                 NaN no threshold; report SEK
    SEB                     npl_gross  8.229919e+08  8.229919e+08 3.668559e-02 4.457588e-11               NaN                 NaN no threshold; report SEK
    SEB     loans_customers_allowance  5.635493e+08  5.635493e+08 2.225816e-02 3.949639e-11               NaN                 NaN no threshold; report SEK
    SEB               debt_securities  9.546436e+09  9.546436e+09 2.323532e-02 2.433926e-12               NaN                 NaN no threshold; report SEK
 DANSKE         intangibles_deduction  8.157030e+08  8.157030e+08 3.483295e-04 4.270299e-13               NaN                 NaN no threshold; report DKK
    SEB         loans_customers_gross  1.851348e+11  1.851348e+11 6.442261e-02 3.479768e-13               NaN                 NaN no threshold; report SEK
 DANSKE                 npl_allowance  1.086466e+09  1.086466e+09 9.775162e-06 8.997206e-15               NaN                 NaN no threshold; report DKK
 DANSKE                     loans_all  2.849431e+11  2.849431e+11 1.708984e-03 5.997633e-15               NaN                 NaN no threshold; report DKK
    SEB                     loans_all  1.935690e+11  1.935690e+11 9.765625e-04 5.045036e-15               NaN                 NaN no threshold; report SEK
    DNB                     npl_gross  2.229734e+09  2.229734e+09 8.583069e-06 3.849368e-15               NaN                 NaN no threshold; report NOK
    SHB        loans_households_gross  1.118921e+11  1.118921e+11 3.967285e-04 3.545634e-15               NaN                 NaN no threshold; report SEK
    DNB               debt_securities  2.771977e+10  2.771977e+10 8.010864e-05 2.889946e-15               NaN                 NaN no threshold; report NOK
    SHB         loans_customers_gross  2.076280e+11  2.076280e+11 4.882812e-04 2.351712e-15               NaN                 NaN no threshold; report SEK
 DANSKE        loans_households_gross  1.023596e+11  1.023596e+11 2.136230e-04 2.086986e-15               NaN                 NaN no threshold; report DKK
    SEB               at1_instruments  1.305090e+09  1.305090e+09 1.907349e-06 1.461469e-15               NaN                 NaN no threshold; report SEK
 DANSKE               debt_securities  3.789369e+10  3.789369e+10 5.340576e-05 1.409358e-15               NaN                 NaN no threshold; report DKK
 DANSKE     loans_customers_allowance  2.034125e+09  2.034125e+09 2.861023e-06 1.406513e-15               NaN                 NaN no threshold; report DKK
    SHB     loans_customers_allowance  8.670111e+07  8.670111e+07 1.192093e-07 1.374945e-15               NaN                 NaN no threshold; report SEK
    DNB         intangibles_deduction  1.952850e+09  1.952850e+09 2.622604e-06 1.342963e-15               NaN                 NaN no threshold; report NOK
    SEB         intangibles_deduction  5.490941e+08  5.490941e+08 5.960464e-07 1.085509e-15               NaN                 NaN no threshold; report SEK
    DNB                 npl_allowance  4.871248e+08  4.871248e+08 4.768372e-07 9.788809e-16               NaN                 NaN no threshold; report NOK
 DANSKE         loans_customers_gross  2.775934e+11  2.775934e+11 2.441406e-04 8.794899e-16               NaN                 NaN no threshold; report DKK
    SHB               at1_instruments  8.499013e+08  8.499013e+08 5.960464e-07 7.013125e-16               NaN                 NaN no threshold; report SEK
    SEB        loans_households_gross  6.640160e+10  6.640160e+10 4.577637e-05 6.893865e-16               NaN                 NaN no threshold; report SEK
    SHB                     npl_gross  6.519987e+08  6.519987e+08 3.576279e-07 5.485101e-16               NaN                 NaN no threshold; report SEK
    SHB               debt_securities  2.010437e+10  2.010437e+10 7.629395e-06 3.794894e-16               NaN                 NaN no threshold; report SEK
    DNB        loans_households_gross  9.410390e+10  9.410390e+10 1.525879e-05 1.621483e-16               NaN                 NaN no threshold; report NOK
    DNB                     loans_all  2.065960e+11  2.065960e+11 3.051758e-05 1.477162e-16               NaN                 NaN no threshold; report NOK
    SHB                     loans_all  2.124551e+11  2.124551e+11 3.051758e-05 1.436425e-16               NaN                 NaN no threshold; report SEK
 DANSKE                     npl_gross  4.055949e+09  4.055949e+09 4.768372e-07 1.175649e-16               NaN                 NaN no threshold; report DKK
   INGA                 npl_allowance  4.184136e+09  4.184136e+09 4.768372e-07 1.139631e-16               NaN                 NaN no threshold; report EUR
   CABK     loans_customers_allowance  6.520161e+09  6.520161e+09 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    UNI        loans_households_gross  3.505981e+10  3.505981e+10 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    UNI                 npl_allowance  5.196830e+08  5.196830e+08 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    UNI                     npl_gross  1.168229e+09  1.168229e+09 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    UNI                     loans_all  5.203985e+10  5.203985e+10 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
   CABK                     loans_all  3.926125e+11  3.926125e+11 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    UNI        gains_held_for_trading  1.242700e+07  1.242700e+07 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    UNI         intangibles_deduction  8.339626e+07  8.339626e+07 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    UNI        gains_hedge_accounting  5.000000e+04  5.000000e+04 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    UNI          exchange_differences  4.940000e+05  4.940000e+05 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    UNI               debt_securities  2.886004e+10  2.886004e+10 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    UNI               dividend_income  1.220600e+07  1.220600e+07 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    UNI                    provisions  4.590600e+07  4.590600e+07 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    UNI                 profit_owners  3.375170e+08  3.375170e+08 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    UNI               at1_instruments  5.473600e+08  5.473600e+08 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    UNI     loans_customers_allowance  8.191000e+08  8.191000e+08 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    UNI         loans_customers_gross  5.041351e+10  5.041351e+10 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
   CABK                     npl_gross  9.157315e+09  9.157315e+09 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    SAB                 npl_allowance  1.977613e+09  1.977613e+09 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    SAB                  total_equity  1.449060e+10  1.449060e+10 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    SHB                 npl_allowance  5.924765e+07  5.924765e+07 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report SEK
    SAB                       cash_cb  2.635894e+10  2.635894e+10 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    SAB               at1_instruments  2.750000e+09  2.750000e+09 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    SAB        loans_households_gross  9.345563e+10  9.345563e+10 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    SAB         intangibles_deduction  2.198089e+09  2.198089e+09 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    SAB               impairments_fin  2.177890e+08  2.177890e+08 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    SAB                     loans_all  1.766576e+11  1.766576e+11 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    SAB     loans_customers_allowance  2.599305e+09  2.599305e+09 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    SAB         loans_customers_gross  1.651622e+11  1.651622e+11 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
   CABK                 npl_allowance  4.919884e+09  4.919884e+09 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    SAB                     npl_gross  4.356326e+09  4.356326e+09 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    SAB               debt_securities  3.403300e+10  3.403300e+10 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    SAB                  depreciation  2.318810e+08  2.318810e+08 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    SAB               dividend_income  3.921000e+06  3.921000e+06 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    SAB          exchange_differences -6.352670e+08 -6.352670e+08 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    SAB        gains_hedge_accounting -3.617800e+07 -3.617800e+07 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    KBC         intangibles_deduction  1.829798e+09  1.829798e+09 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
   INGA        loans_households_gross  3.977157e+11  3.977157e+11 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
   INGA         loans_customers_gross  7.522638e+11  7.522638e+11 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
   INGA     loans_customers_allowance  5.773571e+09  5.773571e+09 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
   INGA                     loans_all  8.281321e+11  8.281321e+11 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
   INGA         intangibles_deduction  1.087606e+09  1.087606e+09 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
   INGA               debt_securities  1.034350e+11  1.034350e+11 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    KBC                     loans_all  2.416534e+11  2.416534e+11 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    KBC               debt_securities  6.157397e+10  6.157397e+10 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    KBC               at1_instruments  2.864000e+09  2.864000e+09 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    KBC                     npl_gross  3.731734e+09  3.731734e+09 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    KBC                 npl_allowance  1.960674e+09  1.960674e+09 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    KBC        loans_households_gross  9.657530e+10  9.657530e+10 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    KBC         loans_customers_gross  2.051790e+11  2.051790e+11 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
    KBC     loans_customers_allowance  2.470053e+09  2.470053e+09 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
   INGA                     npl_gross  1.232948e+10  1.232948e+10 0.000000e+00 0.000000e+00               NaN                 NaN no threshold; report EUR
   BMPS               at1_instruments  0.000000e+00  0.000000e+00 0.000000e+00          NaN               NaN                 NaN no threshold; report EUR
```

#### scope gate (check 8b, instruction 02b B.1): value_a eba total_assets EUR, value_b lr1 row 1 + row 2 in EUR

```
        check bank_id   ref_date        field      value_a      value_b     diff_abs     diff_rel  threshold  passed                   note
8b_scope_gate     ABN 2025-06-30 total_assets 4.142951e+11 4.142950e+11 1.215390e+05 2.933633e-07       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate    BAMI 2025-06-30 total_assets 1.942171e+11 1.942170e+11 1.120000e+05 5.766742e-07       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate    BBVA 2025-06-30 total_assets 7.469548e+11 7.469540e+11 7.690000e+05 1.029513e-06       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate    BMPS 2025-06-30 total_assets 1.255844e+11 1.255844e+11 5.640000e+02 4.491005e-09       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate     BNP 2025-06-30 total_assets 2.573934e+12 2.573934e+12 7.703300e+04 2.992812e-08       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate     BPE 2025-06-30 total_assets 1.445282e+11 1.445280e+11 1.701470e+05 1.177258e-06       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate    CABK 2025-06-30 total_assets 5.798973e+11 5.798973e+11 0.000000e+00 0.000000e+00       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate     CAG 2025-06-30 total_assets 2.187749e+12 2.187749e+12 1.112021e+05 5.082943e-08       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate  DANSKE 2025-06-30 total_assets 4.291889e+11 4.291889e+11 2.952332e+00 6.878863e-12       0.02    True lr1 row 1 + row 2, DKK
8b_scope_gate     DBK 2025-06-30 total_assets 1.395880e+12 1.395880e+12 1.329301e+05 9.523034e-08       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate     DNB 2025-06-30 total_assets 2.926278e+11 2.925535e+11 7.426466e+07 2.537854e-04       0.02    True lr1 row 1 + row 2, NOK
8b_scope_gate     GLE 2025-06-30 total_assets 1.380480e+12 1.380480e+12 1.686054e+04 1.221353e-08       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate    INGA 2025-06-30 total_assets 1.086760e+12 1.086760e+12 0.000000e+00 0.000000e+00       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate     ISP 2025-06-30 total_assets 7.705184e+11 7.705190e+11 6.063550e+05 7.869442e-07       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate     KBC 2025-06-30 total_assets 3.565054e+11 3.565054e+11 0.000000e+00 0.000000e+00       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate     NDA 2025-06-30 total_assets 5.469076e+11 5.469070e+11 5.917151e+05 1.081929e-06       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate    RABO 2025-06-30 total_assets 6.358652e+11 6.358650e+11 2.061730e+05 3.242401e-07       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate     SAB 2025-06-30 total_assets 2.523766e+11 2.523766e+11 0.000000e+00 0.000000e+00       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate     SAN 2025-06-30 total_assets 1.797910e+12 1.797910e+12 8.000000e+04 4.449611e-08       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate     SEB 2025-06-30 total_assets 3.258115e+11 3.258115e+11 1.971436e-02 6.050847e-14       0.02    True lr1 row 1 + row 2, SEK
8b_scope_gate     SHB 2025-06-30 total_assets 3.025829e+11 3.284230e+11 2.584004e+10 8.539821e-02       0.02   False lr1 row 1 + row 2, SEK
8b_scope_gate    SWED 2025-06-30 total_assets 2.433942e+11 2.433942e+11 3.157942e+04 1.297460e-07       0.02    True lr1 row 1 + row 2, SEK
8b_scope_gate     UCG 2025-06-30 total_assets 8.168161e+11 8.168170e+11 8.858800e+05 1.084553e-06       0.02    True lr1 row 1 + row 2, EUR
8b_scope_gate     UNI 2025-06-30 total_assets 9.515042e+10 9.515042e+10 1.525879e-05 1.603649e-16       0.02    True lr1 row 1 + row 2, EUR
```

#### scope table at 2025-06-30, 1 row per EU bank (EUR; scope_adj_diff_rel = |report total_assets + lr1_scope_adjustment - eba| / eba)

```
bank_id  eba_total_assets  report_total_assets  lr1_scope_adjustment  scope_adj_diff_rel
    NDA      5.469076e+11         6.368080e+11         -8.990100e+10        1.081929e-06
    DNB      2.926278e+11         3.241186e+11         -3.156509e+10        2.538954e-04
 DANSKE      4.291889e+11         5.012307e+11          0.000000e+00        1.678556e-01
    SEB      3.258115e+11         3.687682e+11         -4.295673e+10        6.856378e-08
    SHB      3.025829e+11         3.284230e+11          2.583989e+10        1.707961e-01
   SWED      2.433942e+11         2.810247e+11         -3.763056e+10        1.297460e-07
   INGA      1.086760e+12         1.086760e+12          0.000000e+00        2.245206e-07
    ABN      4.142951e+11         4.139220e+11          3.730000e+08        2.933633e-07
    KBC      3.565054e+11         3.906690e+11         -3.416393e+10        1.070242e-06
   RABO      6.358652e+11         6.358650e+11          0.000000e+00        3.242401e-07
    BNP      2.573934e+12         2.849376e+12         -2.754420e+11        2.992812e-08
    GLE      1.380480e+12         1.551491e+12         -1.710110e+11        1.221353e-08
    CAG      2.187749e+12         2.614010e+12         -4.262620e+11        5.079202e-07
    DBK      1.395880e+12         1.397830e+12         -1.950000e+09        9.523034e-08
    CBK      5.990921e+11         5.818180e+11                   NaN                 NaN
    SAN      1.797910e+12         1.815888e+12         -1.797700e+10        6.006975e-07
   BBVA      7.469548e+11         7.769740e+11         -3.002000e+10        1.029513e-06
   CABK      5.798973e+11         6.598220e+11         -7.992465e+10        1.379555e-07
    SAB      2.523766e+11         2.523727e+11          3.885120e+06        4.754799e-10
    BKT      1.317730e+11                  NaN                   NaN                 NaN
    UNI      9.515042e+10         9.555898e+10         -4.085630e+08        1.603649e-16
    UCG      8.168161e+11         8.603280e+11         -4.351100e+10        1.084553e-06
    ISP      7.705184e+11         9.434520e+11         -1.729330e+11        7.869442e-07
   BAMI      1.942171e+11         2.109483e+11         -1.673100e+10        7.929270e-07
    BPE      1.445282e+11         1.445282e+11          0.000000e+00        1.017103e-09
   BMPS      1.255844e+11         1.255741e+11          1.024600e+07        1.876348e-07
```

#### CAG total_assets line (seam 2 and the scope gate)

```
bank_id        field      value_a      value_b     diff_rel  report_scope_adj  diff_rel_scope_adj         check
    CAG total_assets 2.187749e+12 2.614010e+12 1.948399e-01      2.187748e+12        5.079202e-07     8_seam_pl
    CAG total_assets 2.187749e+12 2.187749e+12 5.082943e-08               NaN                 NaN 8b_scope_gate
```

#### checks 2 to 5 on entry rows: counts by check and passed (passed blank = no_liabilities_line, B.8)

```
          check passed  rows
2_balance_sheet   True    78
       3_income   True   104
         4_cet1   True    70
5_period_length   True  1573
```

#### checks 2 to 5 on entry rows that failed

```
none
```

#### check 2 rows with no total_liabilities line (B.8)

```
bank_id   ref_date                        note
   BAMI 2024-12-31 report; no_liabilities_line
   BAMI 2025-06-30 report; no_liabilities_line
   BAMI 2025-12-31 report; no_liabilities_line
   BAMI 2026-06-30 report; no_liabilities_line
   BMPS 2024-12-31 report; no_liabilities_line
   BMPS 2025-06-30 report; no_liabilities_line
   BMPS 2025-12-31 report; no_liabilities_line
   BMPS 2026-06-30 report; no_liabilities_line
    BPE 2024-12-31 report; no_liabilities_line
    BPE 2025-06-30 report; no_liabilities_line
    BPE 2025-12-31 report; no_liabilities_line
    BPE 2026-06-30 report; no_liabilities_line
    CBK 2024-12-31 report; no_liabilities_line
    CBK 2025-06-30 report; no_liabilities_line
    CBK 2025-12-31 report; no_liabilities_line
    CBK 2026-06-30 report; no_liabilities_line
    ISP 2024-12-31 report; no_liabilities_line
    ISP 2025-06-30 report; no_liabilities_line
    ISP 2025-12-31 report; no_liabilities_line
    ISP 2026-06-30 report; no_liabilities_line
    UCG 2024-12-31 report; no_liabilities_line
    UCG 2025-06-30 report; no_liabilities_line
    UCG 2025-12-31 report; no_liabilities_line
    UCG 2026-06-30 report; no_liabilities_line
```

#### outputs/tables/checks.csv: rows by check and passed

```
          check passed  rows
   1_provenance   True  5589
2_balance_sheet   True   577
       3_income   True   603
         4_cet1   True   572
5_period_length   True  6673
     6_currency   True    77
 7_seam_capital   True    72
      8_seam_pl   True   738
  8b_scope_gate  False     1
  8b_scope_gate   True    23
      9_outlier  False    14
      9_outlier   True 18588
```

### Step 2.5: KPIs to 2026-06-30

#### KPI table, ISP, 2025-06-30 (eba), 2025-12-31 and 2026-06-30 (reported basis; underlying identical while one_offs.csv is empty)

```
      date            kpi    value    numerator  denominator  unit    family             status
2025-06-30           rote      NaN          NaN          NaN   pct       NaN  pending_section_3
2025-06-30            roa 0.011872 9.117185e+09 7.679816e+11   bps       eba                 ok
2025-06-30     ppp_assets 0.017321 1.330186e+10 7.679816e+11   bps       eba                 ok
2025-06-30            nim 0.023196 1.522854e+10 6.565065e+11   bps       eba                 ok
2025-06-30      fee_share 0.357156 9.638949e+09 2.698804e+10   pct       eba                 ok
2025-06-30    cost_income 0.507120 1.368617e+10 2.698804e+10   pct       eba                 ok
2025-06-30    cost_assets 0.017821 1.368617e+10 7.679816e+11   bps       eba                 ok
2025-06-30   cost_of_risk 0.002779 1.176057e+09 4.231346e+11   bps       eba                 ok
2025-06-30      npl_ratio 0.022027 9.902829e+09 4.495866e+11   pct       eba                 ok
2025-06-30   npl_coverage 0.499884 4.950265e+09 9.902829e+09   pct       eba                 ok
2025-06-30     cet1_ratio 0.129715 4.001800e+10 3.085076e+11   pct       eba                 ok
2025-06-30 leverage_ratio 0.057888 4.768556e+10 8.237507e+11   pct       eba                 ok
2025-06-30    rwa_density 0.400390 3.085076e+11 7.705184e+11   pct       eba                 ok
2025-06-30   loan_deposit 0.945458 4.135395e+11 4.373961e+11   pct       eba                 ok
2025-06-30            lcr      NaN          NaN          NaN   pct       NaN  missing_input:lcr
2025-06-30           nsfr      NaN          NaN          NaN   pct       NaN missing_input:nsfr
2025-06-30     income_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2025-06-30       cost_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2025-06-30  cost_customer      NaN          NaN          NaN   eur       NaN  pending_section_3
2025-12-31           rote      NaN          NaN          NaN   pct       NaN  pending_section_3
2025-12-31            roa 0.009847 9.321000e+09 9.465860e+11   bps    report                 ok
2025-12-31     ppp_assets 0.018294 1.731700e+10 9.465860e+11   bps    report    levies_in_admin
2025-12-31            nim 0.026664 1.731000e+10 6.491845e+11   bps    report                 ok
2025-12-31      fee_share 0.295091 8.992000e+09 3.047200e+10   pct    report                 ok
2025-12-31    cost_income 0.431708 1.315500e+10 3.047200e+10   pct    report    levies_in_admin
2025-12-31    cost_assets 0.013897 1.315500e+10 9.465860e+11   bps    report    levies_in_admin
2025-12-31   cost_of_risk 0.004333 1.843000e+09 4.253120e+11   bps    report                 ok
2025-12-31      npl_ratio 0.016535 7.589000e+09 4.589720e+11   pct    report                 ok
2025-12-31   npl_coverage 0.484517 3.677000e+09 7.589000e+09   pct    report                 ok
2025-12-31     cet1_ratio 0.131702 4.085400e+10 3.102010e+11   pct        p3                 ok
2025-12-31 leverage_ratio 0.058325 4.852200e+10 8.319200e+11   pct        p3                 ok
2025-12-31    rwa_density 0.323164 3.102010e+11 9.598870e+11   pct p3+report                 ok
2025-12-31   loan_deposit 0.899277 4.194050e+11 4.663800e+11   pct    report                 ok
2025-12-31            lcr 1.396000 1.396000e+00 1.000000e+00   pct    report                 ok
2025-12-31           nsfr 1.220000 1.220000e+00 1.000000e+00   pct    report                 ok
2025-12-31     income_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2025-12-31       cost_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2025-12-31  cost_customer      NaN          NaN          NaN   eur       NaN  pending_section_3
2026-06-30           rote      NaN          NaN          NaN   pct       NaN  pending_section_3
2026-06-30            roa 0.009978 9.659000e+09 9.680605e+11   bps    report                 ok
2026-06-30     ppp_assets 0.021037 2.036500e+10 9.680605e+11   bps    report    levies_in_admin
2026-06-30            nim 0.025944 1.739200e+10 6.703705e+11   bps    report                 ok
2026-06-30      fee_share 0.273300 9.190000e+09 3.362600e+10   pct    report                 ok
2026-06-30    cost_income 0.394367 1.326100e+10 3.362600e+10   pct    report    levies_in_admin
2026-06-30    cost_assets 0.013699 1.326100e+10 9.680605e+11   bps    report    levies_in_admin
2026-06-30   cost_of_risk 0.004078 1.749000e+09 4.288525e+11   bps    report                 ok
2026-06-30      npl_ratio 0.016918 8.021000e+09 4.740990e+11   pct    report                 ok
2026-06-30   npl_coverage 0.500436 4.014000e+09 8.021000e+09   pct    report                 ok
2026-06-30     cet1_ratio 0.129772 4.132300e+10 3.184280e+11   pct        p3                 ok
2026-06-30 leverage_ratio 0.057366 5.024000e+10 8.757740e+11   pct        p3                 ok
2026-06-30    rwa_density 0.320780 3.184280e+11 9.926690e+11   pct p3+report                 ok
2026-06-30   loan_deposit 0.903615 4.312880e+11 4.772920e+11   pct    report                 ok
2026-06-30            lcr 1.376000 1.376000e+00 1.000000e+00   pct    report                 ok
2026-06-30           nsfr 1.198000 1.198000e+00 1.000000e+00   pct    report                 ok
2026-06-30     income_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2026-06-30       cost_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2026-06-30  cost_customer      NaN          NaN          NaN   eur       NaN  pending_section_3
```

#### KPI table, SWED, 2025-06-30 (eba), 2025-12-31 and 2026-06-30 (reported basis; underlying identical while one_offs.csv is empty)

```
      date            kpi     value     numerator  denominator  unit    family             status
2025-06-30           rote       NaN           NaN          NaN   pct       NaN  pending_section_3
2025-06-30            roa  0.012495  2.987766e+09 2.391236e+11   bps       eba                 ok
2025-06-30     ppp_assets  0.014941  3.572862e+09 2.391236e+11   bps       eba                 ok
2025-06-30            nim  0.020594  4.355012e+09 2.114737e+11   bps       eba                 ok
2025-06-30      fee_share  0.226032  1.405261e+09 6.217089e+09   pct       eba                 ok
2025-06-30    cost_income  0.425316  2.644226e+09 6.217089e+09   pct       eba                 ok
2025-06-30    cost_assets  0.011058  2.644226e+09 2.391236e+11   bps       eba                 ok
2025-06-30   cost_of_risk  0.000351  5.771199e+07 1.642643e+11   bps       eba                 ok
2025-06-30      npl_ratio  0.006842  1.160160e+09 1.695585e+11   pct       eba                 ok
2025-06-30   npl_coverage  0.291169  3.378024e+08 1.160160e+09   pct       eba                 ok
2025-06-30     cet1_ratio  0.197044  1.570728e+10 7.971472e+10   pct       eba                 ok
2025-06-30 leverage_ratio  0.066812  1.710479e+10 2.560123e+11   pct       eba                 ok
2025-06-30    rwa_density  0.327513  7.971472e+10 2.433942e+11   pct       eba                 ok
2025-06-30   loan_deposit  1.359582  1.647259e+11 1.211592e+11   pct       eba                 ok
2025-06-30            lcr       NaN           NaN          NaN   pct       NaN  missing_input:lcr
2025-06-30           nsfr       NaN           NaN          NaN   pct       NaN missing_input:nsfr
2025-06-30     income_fte       NaN           NaN          NaN eur_k       NaN  pending_section_3
2025-06-30       cost_fte       NaN           NaN          NaN eur_k       NaN  pending_section_3
2025-06-30  cost_customer       NaN           NaN          NaN   eur       NaN  pending_section_3
2025-12-31           rote       NaN           NaN          NaN   pct       NaN  pending_section_3
2025-12-31            roa  0.010790  3.276200e+10 3.036240e+12   bps    report                 ok
2025-12-31     ppp_assets  0.013577  4.122200e+10 3.036240e+12   bps    report                 ok
2025-12-31            nim  0.018823  4.400000e+10 2.337513e+12   bps    report                 ok
2025-12-31      fee_share  0.237430  1.632000e+10 6.873600e+10   pct    report                 ok
2025-12-31    cost_income  0.400285  2.751400e+10 6.873600e+10   pct    report                 ok
2025-12-31    cost_assets  0.009062  2.751400e+10 3.036240e+12   bps    report                 ok
2025-12-31   cost_of_risk -0.000018 -3.400000e+07 1.859907e+12   bps    report                 ok
2025-12-31      npl_ratio  0.005963  1.146600e+10 1.922977e+12   pct    report                 ok
2025-12-31   npl_coverage  0.178441  2.046000e+09 1.146600e+10   pct    report                 ok
2025-12-31     cet1_ratio  0.178201  1.660990e+11 9.320900e+11   pct        p3                 ok
2025-12-31 leverage_ratio  0.065632  1.812390e+11 2.761434e+12   pct        p3                 ok
2025-12-31    rwa_density  0.304328  9.320900e+11 3.062782e+12   pct p3+report                 ok
2025-12-31   loan_deposit  1.447789  1.886718e+12 1.303172e+12   pct    report                 ok
2025-12-31            lcr  1.651400  1.651400e+00 1.000000e+00   pct    report                 ok
2025-12-31           nsfr  1.239500  1.239500e+00 1.000000e+00   pct    report                 ok
2025-12-31     income_fte       NaN           NaN          NaN eur_k       NaN  pending_section_3
2025-12-31       cost_fte       NaN           NaN          NaN eur_k       NaN  pending_section_3
2025-12-31  cost_customer       NaN           NaN          NaN   eur       NaN  pending_section_3
2026-06-30           rote       NaN           NaN          NaN   pct       NaN  pending_section_3
2026-06-30            roa  0.009694  3.121200e+10 3.219568e+12   bps    report                 ok
2026-06-30     ppp_assets  0.012348  3.975600e+10 3.219568e+12   bps    report                 ok
2026-06-30            nim  0.018293  4.401700e+10 2.406188e+12   bps    report                 ok
2026-06-30      fee_share  0.244172  1.700000e+10 6.962300e+10   pct    report                 ok
2026-06-30    cost_income  0.428982  2.986700e+10 6.962300e+10   pct    report                 ok
2026-06-30    cost_assets  0.009277  2.986700e+10 3.219568e+12   bps    report                 ok
2026-06-30   cost_of_risk  0.000229  4.340000e+08 1.895227e+12   bps    report                 ok
2026-06-30      npl_ratio  0.004036  7.974000e+09 1.975801e+12   pct    report                 ok
2026-06-30   npl_coverage  0.219087  1.747000e+09 7.974000e+09   pct    report                 ok
2026-06-30     cet1_ratio  0.174024  1.698010e+11 9.757350e+11   pct        p3                 ok
2026-06-30 leverage_ratio  0.062459  1.855940e+11 2.971442e+12   pct        p3                 ok
2026-06-30    rwa_density  0.295079  9.757350e+11 3.306693e+12   pct p3+report                 ok
2026-06-30   loan_deposit  1.431414  1.940893e+12 1.355927e+12   pct    report                 ok
2026-06-30            lcr  1.616400  1.616400e+00 1.000000e+00   pct    report                 ok
2026-06-30           nsfr  1.216000  1.216000e+00 1.000000e+00   pct    report                 ok
2026-06-30     income_fte       NaN           NaN          NaN eur_k       NaN  pending_section_3
2026-06-30       cost_fte       NaN           NaN          NaN eur_k       NaN  pending_section_3
2026-06-30  cost_customer       NaN           NaN          NaN   eur       NaN  pending_section_3
```

#### KPI table, BBVA, 2025-06-30 (eba), 2025-12-31 and 2026-06-30 (reported basis; underlying identical while one_offs.csv is empty)

```
      date            kpi    value    numerator  denominator  unit    family             status
2025-06-30           rote      NaN          NaN          NaN   pct       NaN  pending_section_3
2025-06-30            roa 0.014182 1.048573e+10 7.393666e+11   bps       eba                 ok
2025-06-30     ppp_assets 0.027510 2.033993e+10 7.393666e+11   bps       eba                 ok
2025-06-30            nim 0.040764 2.422019e+10 5.941629e+11   bps       eba                 ok
2025-06-30      fee_share 0.242576 8.477726e+09 3.494871e+10   pct       eba                 ok
2025-06-30    cost_income 0.418006 1.460878e+10 3.494871e+10   pct       eba                 ok
2025-06-30    cost_assets 0.019759 1.460878e+10 7.393666e+11   bps       eba                 ok
2025-06-30   cost_of_risk 0.013494 5.694388e+09 4.219959e+11   bps       eba                 ok
2025-06-30      npl_ratio 0.029976 1.413625e+10 4.715868e+11   pct       eba                 ok
2025-06-30   npl_coverage 0.525571 7.429600e+09 1.413625e+10   pct       eba                 ok
2025-06-30     cet1_ratio 0.133403 5.163361e+10 3.870507e+11   pct       eba                 ok
2025-06-30 leverage_ratio 0.069259 5.712264e+10 8.247687e+11   pct       eba                 ok
2025-06-30    rwa_density 0.518172 3.870507e+11 7.469548e+11   pct       eba                 ok
2025-06-30   loan_deposit 0.923630 4.267589e+11 4.620453e+11   pct       eba                 ok
2025-06-30            lcr      NaN          NaN          NaN   pct       NaN  missing_input:lcr
2025-06-30           nsfr      NaN          NaN          NaN   pct       NaN missing_input:nsfr
2025-06-30     income_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2025-06-30       cost_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2025-06-30  cost_customer      NaN          NaN          NaN   eur       NaN  pending_section_3
2025-12-31           rote      NaN          NaN          NaN   pct       NaN  pending_section_3
2025-12-31            roa 0.012881 1.051100e+10 8.159890e+11   bps    report                 ok
2025-12-31     ppp_assets 0.027695 2.259900e+10 8.159890e+11   bps    report    levies_in_admin
2025-12-31            nim 0.041094 2.628000e+10 6.395075e+11   bps    report                 ok
2025-12-31      fee_share 0.222442 8.215000e+09 3.693100e+10   pct    report                 ok
2025-12-31    cost_income 0.388075 1.433200e+10 3.693100e+10   pct    report    levies_in_admin
2025-12-31    cost_assets 0.017564 1.433200e+10 8.159890e+11   bps    report    levies_in_admin
2025-12-31   cost_of_risk 0.013530 6.073000e+09 4.488575e+11   bps    report                 ok
2025-12-31      npl_ratio 0.028215 1.435400e+10 5.087380e+11   pct    report                 ok
2025-12-31   npl_coverage 0.556779 7.992000e+09 1.435400e+10   pct    report                 ok
2025-12-31     cet1_ratio 0.126991 5.044600e+10 3.972410e+11   pct        p3                 ok
2025-12-31 leverage_ratio 0.061542 5.593400e+10 9.088690e+11   pct        p3                 ok
2025-12-31    rwa_density 0.462136 3.972410e+11 8.595760e+11   pct p3+report                 ok
2025-12-31   loan_deposit 0.917479 4.610340e+11 5.025010e+11   pct    report                 ok
2025-12-31            lcr 1.400800 1.400800e+00 1.000000e+00   pct    report                 ok
2025-12-31           nsfr 1.263700 1.263700e+00 1.000000e+00   pct    report                 ok
2025-12-31     income_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2025-12-31       cost_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2025-12-31  cost_customer      NaN          NaN          NaN   eur       NaN  pending_section_3
2026-06-30           rote      NaN          NaN          NaN   pct       NaN  pending_section_3
2026-06-30            roa 0.012758 1.111500e+10 8.712000e+11   bps    report                 ok
2026-06-30     ppp_assets 0.028135 2.451100e+10 8.712000e+11   bps    report    levies_in_admin
2026-06-30            nim 0.042599 2.883700e+10 6.769405e+11   bps    report                 ok
2026-06-30      fee_share 0.219068 8.775000e+09 4.005600e+10   pct    report                 ok
2026-06-30    cost_income 0.388082 1.554500e+10 4.005600e+10   pct    report    levies_in_admin
2026-06-30    cost_assets 0.017843 1.554500e+10 8.712000e+11   bps    report    levies_in_admin
2026-06-30   cost_of_risk 0.014153 6.809000e+09 4.811060e+11   bps    report                 ok
2026-06-30      npl_ratio 0.027195 1.545600e+10 5.683370e+11   pct    report                 ok
2026-06-30   npl_coverage 0.553442 8.554000e+09 1.545600e+10   pct    report                 ok
2026-06-30     cet1_ratio 0.128988 5.462600e+10 4.234970e+11   pct        p3                 ok
2026-06-30 leverage_ratio 0.059974 6.111000e+10 1.018949e+12   pct        p3                 ok
2026-06-30    rwa_density 0.438663 4.234970e+11 9.654260e+11   pct p3+report                 ok
2026-06-30   loan_deposit 0.957862 5.105220e+11 5.329810e+11   pct    report                 ok
2026-06-30            lcr 1.420000 1.420000e+00 1.000000e+00   pct    report                 ok
2026-06-30           nsfr 1.250000 1.250000e+00 1.000000e+00   pct    report                 ok
2026-06-30     income_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2026-06-30       cost_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2026-06-30  cost_customer      NaN          NaN          NaN   eur       NaN  pending_section_3
```

#### KPI table, CAG, 2025-06-30 (eba), 2025-12-31 and 2026-06-30 (reported basis; underlying identical while one_offs.csv is empty)

```
      date            kpi    value    numerator  denominator  unit    family             status
2025-06-30           rote      NaN          NaN          NaN   pct       NaN  pending_section_3
2025-06-30            roa 0.004205 9.030012e+09 2.147700e+12   bps       eba                 ok
2025-06-30     ppp_assets 0.006460 1.387463e+10 2.147700e+12   bps       eba                 ok
2025-06-30            nim 0.009527 1.604565e+10 1.684178e+12   bps       eba                 ok
2025-06-30      fee_share 0.424838 1.776284e+10 4.181088e+10   pct       eba                 ok
2025-06-30    cost_income 0.668157 2.793625e+10 4.181088e+10   pct       eba                 ok
2025-06-30    cost_assets 0.013008 2.793625e+10 2.147700e+12   bps       eba                 ok
2025-06-30   cost_of_risk 0.002655 3.180364e+09 1.197774e+12   bps       eba                 ok
2025-06-30      npl_ratio 0.019644 2.643175e+10 1.345533e+12   pct       eba                 ok
2025-06-30   npl_coverage 0.488628 1.291530e+10 2.643175e+10   pct       eba                 ok
2025-06-30     cet1_ratio 0.175817 1.141072e+11 6.490132e+11   pct       eba                 ok
2025-06-30 leverage_ratio 0.055911 1.224859e+11 2.190715e+12   pct       eba                 ok
2025-06-30    rwa_density 0.296658 6.490132e+11 2.187749e+12   pct       eba                 ok
2025-06-30   loan_deposit 0.917467 1.187510e+12 1.294336e+12   pct       eba                 ok
2025-06-30            lcr      NaN          NaN          NaN   pct       NaN  missing_input:lcr
2025-06-30           nsfr      NaN          NaN          NaN   pct       NaN missing_input:nsfr
2025-06-30     income_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2025-06-30       cost_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2025-06-30  cost_customer      NaN          NaN          NaN   eur       NaN  pending_section_3
2025-12-31           rote      NaN          NaN          NaN   pct       NaN  pending_section_3
2025-12-31            roa 0.003314 8.754000e+09 2.641826e+12   bps    report                 ok
2025-12-31     ppp_assets 0.006053 1.599000e+10 2.641826e+12   bps    report    levies_in_admin
2025-12-31            nim 0.012376 2.104300e+10 1.700320e+12   bps    report                 ok
2025-12-31      fee_share 0.325042 1.285800e+10 3.955800e+10   pct    report                 ok
2025-12-31    cost_income 0.595783 2.356800e+10 3.955800e+10   pct    report    levies_in_admin
2025-12-31    cost_assets 0.008921 2.356800e+10 2.641826e+12   bps    report    levies_in_admin
2025-12-31   cost_of_risk 0.002836 3.452000e+09 1.217416e+12   bps    report                 ok
2025-12-31      npl_ratio 0.020166 2.765100e+10 1.371164e+12   pct    report                 ok
2025-12-31   npl_coverage 0.489566 1.353700e+10 2.765100e+10   pct    report                 ok
2025-12-31     cet1_ratio 0.172899 1.145810e+11 6.627030e+11   pct        p3                 ok
2025-12-31 leverage_ratio 0.055364 1.225790e+11 2.214046e+12   pct        p3                 ok
2025-12-31    rwa_density 0.247100 6.627030e+11 2.681925e+12   pct p3+report                 ok
2025-12-31   loan_deposit 1.006314 1.206999e+12 1.199426e+12   pct    report                 ok
2025-12-31            lcr 1.358000 1.358000e+00 1.000000e+00   pct    report                 ok
2025-12-31           nsfr 1.190900 1.190900e+00 1.000000e+00   pct    report                 ok
2025-12-31     income_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2025-12-31       cost_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2025-12-31  cost_customer      NaN          NaN          NaN   eur       NaN  pending_section_3
2026-06-30           rote      NaN          NaN          NaN   pct       NaN  pending_section_3
2026-06-30            roa 0.003272 8.826000e+09 2.697272e+12   bps    report                 ok
2026-06-30     ppp_assets 0.006192 1.670200e+10 2.697272e+12   bps    report    levies_in_admin
2026-06-30            nim 0.013149 2.262400e+10 1.720543e+12   bps    report                 ok
2026-06-30      fee_share 0.325415 1.320600e+10 4.058200e+10   pct    report                 ok
2026-06-30    cost_income 0.588438 2.388000e+10 4.058200e+10   pct    report    levies_in_admin
2026-06-30    cost_assets 0.008853 2.388000e+10 2.697272e+12   bps    report    levies_in_admin
2026-06-30   cost_of_risk 0.002992 3.699000e+09 1.236388e+12   bps    report                 ok
2026-06-30      npl_ratio 0.021102 2.961900e+10 1.403588e+12   pct    report                 ok
2026-06-30   npl_coverage 0.468753 1.388400e+10 2.961900e+10   pct    report                 ok
2026-06-30     cet1_ratio 0.172324 1.185290e+11 6.878280e+11   pct        p3                 ok
2026-06-30 leverage_ratio 0.055341 1.265850e+11 2.287370e+12   pct        p3                 ok
2026-06-30    rwa_density 0.247373 6.878280e+11 2.780535e+12   pct p3+report                 ok
2026-06-30   loan_deposit 1.021969 1.240756e+12 1.214084e+12   pct    report                 ok
2026-06-30            lcr 1.357500 1.357500e+00 1.000000e+00   pct    report                 ok
2026-06-30           nsfr 1.197000 1.197000e+00 1.000000e+00   pct    report                 ok
2026-06-30     income_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2026-06-30       cost_fte      NaN          NaN          NaN eur_k       NaN  pending_section_3
2026-06-30  cost_customer      NaN          NaN          NaN   eur       NaN  pending_section_3
```

#### coverage, non-blank KPIs per bank and date (reported basis, 19 KPIs per date)

```
bank_id  2021-12-31  2022-06-30  2022-12-31  2023-06-30  2023-12-31  2024-06-30  2024-12-31  2025-06-30  2025-12-31  2026-06-30
    ABN          13          13          13          13          13          13          13          13          15          15
   BAMI          13          13          13          13          13          13          13          13          15          15
   BBVA          13          13          13          13          13          13          13          13          15          15
    BKT          13          13          13          13          13          13          13          13           5          10
   BMPS          13          13          13          13          13          13          13          13          15          15
    BNP          13          13          13          13          13          13          13          13          15          15
    BPE           8           6          13          13          13          13          13          13          15          15
   CABK          13          13          13          13          13          13          13          13          15          15
    CAG          13          13          13          13          13          13          13          13          15          15
    CBK          13          13          13          13          13          13          13          13           5           5
 DANSKE          13          13          13          13          13          13          13          13          15          15
    DBK          13          13          13          13          13          13          13          13          15          15
    DNB           0           6           8          13          13          13          13          13          15           5
    GLE          13          13          13          13          13          13          13          13          15          15
   INGA          13          13          13          13          13          13          13          13          15          15
    ISP          13          13          13          13          13          13          13          13          15          15
    KBC          13          13          13          13          13          13          13          13          15          15
    NDA          13          13          13          13          13          13          13          13          15          15
   RABO          13          13          13          13          13          13          13          13          15          15
    SAB          13          13          13          13          13          13          13          13          15          15
    SAN          13          13          13          13          13          13          13          13          15          15
    SEB          13          13          13          13          13          13          13          13          15          15
    SHB          13          13          13          13          13          13          13          13           0           0
   SWED          13          13          13          13          13          13          13          13          15          15
    UCG          13          13          13          13          13          13          13          13          15           5
    UNI          13          13          13          13          13          13          13          13          14          14
```

#### KPI rows by status (both bases)

```
                                 status  rows
                                     ok  6458
                      pending_section_3  2080
                      missing_input:lcr   428
                     missing_input:nsfr   428
                        levies_in_admin   182
                      scope_gate_failed    44
           levies_in_admin;dep_in_admin    40
    missing_input:loans_customers_gross    14
                missing_input:npl_gross    14
            missing_input:npl_allowance    14
                     missing_input:cet1    14
                    missing_input:tier1    14
                      missing_input:rwa    14
      missing_input:loans_customers_net    14
                           mixed_family    12
             missing_input:total_assets    12
                     missing_input:opex    12
          missing_input:debt_securities    10
                dep_in_admin;toi_summed     8
                             toi_summed     8
levies_in_admin;dep_in_admin;toi_summed     8
                       from_comparative     6
       levies_in_admin;from_comparative     6
            missing_input:profit_owners     6
                      missing_input:ppp     6
                      missing_input:nii     6
                 missing_input:net_fees     6
          missing_input:impairments_fin     6
                      missing_input:iea     4
                           dep_in_admin     4
       missing_input:deposits_customers     2
```

#### blank KPIs after 2025-06-30, other than pending_section_3, lcr and nsfr (reported basis)

```
bank_id       date            kpi                           status
    BKT 2025-12-31            nim    missing_input:debt_securities
    BKT 2025-12-31      npl_ratio          missing_input:npl_gross
    BKT 2025-12-31   npl_coverage      missing_input:npl_allowance
    BKT 2025-12-31     cet1_ratio               missing_input:cet1
    BKT 2025-12-31 leverage_ratio              missing_input:tier1
    BKT 2025-12-31    rwa_density                missing_input:rwa
    BKT 2025-12-31           nsfr               missing_input:nsfr
    BKT 2026-06-30            roa                     mixed_family
    BKT 2026-06-30     ppp_assets                     mixed_family
    BKT 2026-06-30            nim                     mixed_family
    BKT 2026-06-30    cost_assets                     mixed_family
    BKT 2026-06-30   cost_of_risk                     mixed_family
    CBK 2025-12-31            nim    missing_input:debt_securities
    CBK 2025-12-31      npl_ratio          missing_input:npl_gross
    CBK 2025-12-31   npl_coverage      missing_input:npl_allowance
    CBK 2025-12-31     cet1_ratio               missing_input:cet1
    CBK 2025-12-31 leverage_ratio              missing_input:tier1
    CBK 2025-12-31    rwa_density                missing_input:rwa
    CBK 2025-12-31           nsfr               missing_input:nsfr
    CBK 2026-06-30            nim    missing_input:debt_securities
    CBK 2026-06-30      npl_ratio          missing_input:npl_gross
    CBK 2026-06-30   npl_coverage      missing_input:npl_allowance
    CBK 2026-06-30     cet1_ratio               missing_input:cet1
    CBK 2026-06-30 leverage_ratio              missing_input:tier1
    CBK 2026-06-30    rwa_density                missing_input:rwa
    CBK 2026-06-30           nsfr               missing_input:nsfr
    DNB 2026-06-30            nim    missing_input:debt_securities
    DNB 2026-06-30      npl_ratio          missing_input:npl_gross
    DNB 2026-06-30   npl_coverage      missing_input:npl_allowance
    DNB 2026-06-30     cet1_ratio               missing_input:cet1
    DNB 2026-06-30 leverage_ratio              missing_input:tier1
    DNB 2026-06-30    rwa_density                missing_input:rwa
    DNB 2026-06-30           nsfr               missing_input:nsfr
    SHB 2025-12-31            roa                scope_gate_failed
    SHB 2025-12-31     ppp_assets                scope_gate_failed
    SHB 2025-12-31            nim                scope_gate_failed
    SHB 2025-12-31      fee_share                scope_gate_failed
    SHB 2025-12-31    cost_income                scope_gate_failed
    SHB 2025-12-31    cost_assets                scope_gate_failed
    SHB 2025-12-31   cost_of_risk                scope_gate_failed
    SHB 2025-12-31      npl_ratio                scope_gate_failed
    SHB 2025-12-31   npl_coverage                scope_gate_failed
    SHB 2025-12-31     cet1_ratio                scope_gate_failed
    SHB 2025-12-31 leverage_ratio                scope_gate_failed
    SHB 2025-12-31    rwa_density                scope_gate_failed
    SHB 2025-12-31   loan_deposit                scope_gate_failed
    SHB 2025-12-31            lcr                scope_gate_failed
    SHB 2025-12-31           nsfr                scope_gate_failed
    SHB 2026-06-30            roa                scope_gate_failed
    SHB 2026-06-30     ppp_assets                scope_gate_failed
    SHB 2026-06-30            nim                scope_gate_failed
    SHB 2026-06-30      fee_share                scope_gate_failed
    SHB 2026-06-30    cost_income                scope_gate_failed
    SHB 2026-06-30    cost_assets                scope_gate_failed
    SHB 2026-06-30   cost_of_risk                scope_gate_failed
    SHB 2026-06-30      npl_ratio          missing_input:npl_gross
    SHB 2026-06-30   npl_coverage      missing_input:npl_allowance
    SHB 2026-06-30     cet1_ratio               missing_input:cet1
    SHB 2026-06-30 leverage_ratio              missing_input:tier1
    SHB 2026-06-30    rwa_density                missing_input:rwa
    SHB 2026-06-30           nsfr               missing_input:nsfr
    UCG 2026-06-30            nim    missing_input:debt_securities
    UCG 2026-06-30      npl_ratio          missing_input:npl_gross
    UCG 2026-06-30   npl_coverage      missing_input:npl_allowance
    UCG 2026-06-30     cet1_ratio               missing_input:cet1
    UCG 2026-06-30 leverage_ratio              missing_input:tier1
    UCG 2026-06-30    rwa_density                missing_input:rwa
    UCG 2026-06-30           nsfr               missing_input:nsfr
    UNI 2025-12-31            nim                     mixed_family
    UNI 2026-06-30   loan_deposit missing_input:deposits_customers
```

#### KPI families after 2025-06-30 (reported basis, non-blank)

```
   family  rows
   report   558
       p3    90
p3+report    45
```

### Step 2.5: hand check, ISP nim and cost_income at 2025-12-31

#### ISP entries used (value in EUR)

```
  ref_date                  field value_as_printed unit_scale        value doc_type page                                                                                           snippet
2024-12-31         admin_expenses           -7,422    1000000   7422000000   annual  388                                      component 1/2: a) personnel expenses -6,889 -7,422 -533 -7.2
2024-12-31         admin_expenses           -4,575    1000000   4575000000   annual  388                           component 2/2: b) other administrative expenses -4,475 -4,575 -100 -2.2
2025-12-31         admin_expenses           -6,889    1000000   6889000000   annual  388                                      component 1/2: a) personnel expenses -6,889 -7,422 -533 -7.2
2025-12-31         admin_expenses           -4,475    1000000   4475000000   annual  388                           component 2/2: b) other administrative expenses -4,475 -4,575 -100 -2.2
2024-12-31                cash_cb           40,533    1000000  40533000000   annual  386                                           10. Cash and cash equivalents 37,868 40,533 -2,665 -6.6
2025-12-31                cash_cb           37,868    1000000  37868000000   annual  386                                           10. Cash and cash equivalents 37,868 40,533 -2,665 -6.6
2024-12-31        debt_securities          143,027    1000000 143027000000  pillar3  117                                 component 1/2: 90 Debt securities 143,027 135,096 7,066 126 - 126
2024-12-31        debt_securities              126    1000000    126000000  pillar3  117                                 component 2/2: 90 Debt securities 143,027 135,096 7,066 126 - 126
2025-12-31        debt_securities          162,844    1000000 162844000000  pillar3  122                                 component 1/2: 90 Debt securities 162,844 158,456 3,441 855 - 852
2025-12-31        debt_securities              855    1000000    855000000  pillar3  122                                 component 2/2: 90 Debt securities 162,844 158,456 3,441 855 - 852
2024-12-31           depreciation             -647    1000000    647000000   annual  388 component 1/2: 210. Net adjustments to / recoveries on property and equipment -581 -647 -66 -10.2
2024-12-31           depreciation           -1,111    1000000   1111000000   annual  388     component 2/2: 220. Net adjustments to / recoveries on intangible assets -1,210 -1,111 99 8.9
2025-12-31           depreciation             -581    1000000    581000000   annual  388 component 1/2: 210. Net adjustments to / recoveries on property and equipment -581 -647 -66 -10.2
2025-12-31           depreciation           -1,210    1000000   1210000000   annual  388     component 2/2: 220. Net adjustments to / recoveries on intangible assets -1,210 -1,111 99 8.9
2024-12-31       interest_expense          -16,512    1000000  16512000000   annual  388                                     20. Interest and similar expense -10,448 -16,512 -6,064 -36.7
2025-12-31       interest_expense          -10,448    1000000  10448000000   annual  388                                     20. Interest and similar expense -10,448 -16,512 -6,064 -36.7
2024-12-31        interest_income           34,602    1000000  34602000000   annual  388                                        10. Interest and similar income 27,758 34,602 -6,844 -19.8
2025-12-31        interest_income           27,758    1000000  27758000000   annual  388                                        10. Interest and similar income 27,758 34,602 -6,844 -19.8
2024-12-31              loans_all          444,361    1000000 444361000000  pillar3  117                         component 1/2: 10 Loans and advances 444,361 407,228 36,218 9,783 - 9,532
2024-12-31              loans_all            9,783    1000000   9783000000  pillar3  117                         component 2/2: 10 Loans and advances 444,361 407,228 36,218 9,783 - 9,532
2025-12-31              loans_all          451,383    1000000 451383000000  pillar3  122                         component 1/2: 10 Loans and advances 451,383 416,984 33,257 7,589 - 7,482
2025-12-31              loans_all            7,589    1000000   7589000000  pillar3  122                         component 2/2: 10 Loans and advances 451,383 416,984 33,257 7,589 - 7,482
2024-12-31 total_operating_income           30,693    1000000  30693000000   annual  388                                120. Net interest and other banking income 30,472 30,693 -221 -0.7
2025-12-31 total_operating_income           30,472    1000000  30472000000   annual  388                                120. Net interest and other banking income 30,472 30,693 -221 -0.7
```

#### hand arithmetic (Decimal, from report_entries.csv values)

```
interest_income 2025-12-31 = 27,758,000,000
interest_expense 2025-12-31 = 10,448,000,000
nii = interest_income - |interest_expense| = 27,758,000,000 - 10,448,000,000 = 17,310,000,000
cash_cb 2024-12-31 = 40,533,000,000
debt_securities 2024-12-31 = 143,027,000,000 + 126,000,000 = 143,153,000,000
loans_all 2024-12-31 = 444,361,000,000 + 9,783,000,000 = 454,144,000,000
iea 2024-12-31 = cash_cb + debt_securities + loans_all = 40,533,000,000 + 143,153,000,000 + 454,144,000,000 = 637,830,000,000
cash_cb 2025-12-31 = 37,868,000,000
debt_securities 2025-12-31 = 162,844,000,000 + 855,000,000 = 163,699,000,000
loans_all 2025-12-31 = 451,383,000,000 + 7,589,000,000 = 458,972,000,000
iea 2025-12-31 = cash_cb + debt_securities + loans_all = 37,868,000,000 + 163,699,000,000 + 458,972,000,000 = 660,539,000,000
average iea = (637,830,000,000 + 660,539,000,000) / 2 = 649,184,500,000
nim = 17,310,000,000 / 649,184,500,000 = 0.026664
total_operating_income 2025-12-31 = 30,472,000,000
admin_expenses 2025-12-31 = 6,889,000,000 + 4,475,000,000 = 11,364,000,000
resolution_dgs_contrib 2025-12-31 = 0
depreciation 2025-12-31 = 581,000,000 + 1,210,000,000 = 1,791,000,000
opex = |admin_expenses| + |resolution_dgs_contrib| + |depreciation| = 11,364,000,000 + 0 + 1,791,000,000 = 13,155,000,000
cost_income = 13,155,000,000 / 30,472,000,000 = 0.431708
nim: hand 0.026664, kpi.csv 0.026664 (numerator 17,310,000,000, denominator 649,184,500,000, family report, status ok); |diff| 4.63e-12
cost_income: hand 0.431708, kpi.csv 0.431708 (numerator 13,155,000,000, denominator 30,472,000,000, family report, status levies_in_admin); |diff| 2.21e-11
```

### Step 2.3: per-bank changes, missing fields and judgement calls (session 2)

From the fix and entry work of session 2. These lines describe the committed entries. Session 1's per-bank notes (below) still hold where a line here does not replace them.

- BNP fix pass (213 entries)
- FY2024 P&L added (17 fields); LR1 p213: 2,849,376 and (275,442); scope gate passes (2.99e-08).
- admin_expenses now the income statement "Operating expenses" total (14,344 / 29,003 / 15,501; old note build 14,517 at 2025-06-30); depreciation as printed. profit_owners unchanged (attributable to equity holders, AT1 in equity). No zero cells needed.
- NDA fix pass (216 entries)
- debt_securities added at 4 dates (CR1 090 col d blank); FY2024 P&L 18 rows; LR1 p52: 636,808 and -89,901, gate 1e-06; profit_owners = shareholders + AT1 holders (2026-06-30 AT1 line "-": shareholders only = net profit, no NCI split). admin unchanged.
- CAG fix pass (218): FY2024 P&L 20 rows; LR1 2 614 011 / (426 262), gate 5e-08; admin = IS "Operating expenses 4.7" line (10,844 / 21,438 / 11,169), depreciation printed; impairments_nonfin FY2024 = goodwill change +4 (stored -4); CC1 not in PDFs.
- GLE fix pass (233): debt_securities 2025-12-31, 2026-06-30 with "-" zero cell; FY2024 P&L; LR1 p36 1,551,491 / (171,011), gate 1e-08; admin = IS single "Other operating expenses" line (personnel and other are only in note 5; IS line is already net of the 778 reclassified into insurance inside NBI).
- RABO fix pass (232): debt_securities 4 dates (col d blank); FY2024 P&L (+ impairments_nonfin 70 FY2024); LR1 p20 635,865 / row 2 blank = 0, gate 3e-07; profit_owners = Rabobank + Certificates + Capital Securities (FY2024 5,098; H1 2025 2,660; FY2025 4,906; H1 2026 2,668). gains_derecognition_not_fvtpl 2026-06-30 still missing ("4 4" line not unique).
- SWED fix pass (216): customer loans gross/allowance and debt_securities at 4 dates (030 d,j and 090 d blank); FY2024 P&L; LR1 p15 3 132 442 / -419 449, gate 1e-07; P3 2026-06-30 (PDF from Data Hub ZIP) KM1/CC1/CR1; admin keeps the printed "VAT Reimbursements G14 -1 539" line (IS line, in the statement's total).
- ABN fix pass (220): loans_customers_allowance (030 g, j blank) and debt_securities (090 d blank) at 4 dates; FY2024 P&L; LR1 p19 413,922 / 373 (positive), gate 3e-07.
- DANSKE fix pass (201): P3 workbooks (.xls) at 4 dates: KM1/CC1/CR1, LR1 3202135.5 / 0, gate 1e-10; admin = IS "Operating expenses" total at all P&L dates, no depreciation (dep_in_admin); profit_owners half years = net profit (no NCI/AT1 split printed); FY2024 P&L. One CR1 cell stored as 7.46e-06 (DKK m) re-entered as 0.00000746 x 1e6 after the sheet writer stopped using exponents.
- SHB fix pass (179): customer loans and debt_securities zero cells at 3 Pillar 3 dates; FY2024 P&L; P3 2025-06-30 workbook KM1/CC1 row 30/CR1; intangibles_deduction 2025-06-30 left out (the workbook's CC1 values are shifted one row up against their labels). SCOPE GATE FAILS: SHB's LR1 row 1 (3,372,742) is already the prudential total and row 2 is +288,024 (row 1 + row 2 = the published total 3,660,767); EBA total assets = row 1 alone. 8.5% > 2% -> rule 4 stop for SHB only: its report and p3 rows are kept with status scope_gate_failed and no KPI.
- SEB fix pass (202): debt_securities 2024-12-31, 2025-12-31 (col d blank); P3 workbooks 2025-06-30 and 2026-06-30 (KM1, CC1 rows 8 and 30, CR1); LR1 4110475.2 / -478817.2, gate 2e-12; FY2024 P&L (SEB restated this column: SEK 680m moved into NII).
- INGA fix pass (205): debt_securities zero cells at 3 PDF dates; P3 workbook 2025-06-30; LR1 1086759.8 / row 2 blank = 0, gate 0; admin = IS "Staff expenses" + "Other operating expenses" (includes depreciation and provisions): note-based depreciation and provisions removed (dep_in_admin); FY2024 P&L.
- Data Hub and CBK search: none fetchable by script (EDAP serves files only via Power BI; Commerzbank's IR links are built client-side by an authenticated EQS API). DNB, SHB, UCG at 2026-06-30 and CBK at all 4 dates stay missing.
- BBVA (253, first committed this session): FY2024 P&L 26 rows; LR1 p33 776,974 / (30,020), gate 1e-06; no zero cells needed; admin/profit_owners unchanged. Missing: resolution_dgs_contrib (inside other operating expense). Mandatorily-FVTPL line in other_operating_net; customer deposits at amortised cost only; CC1 annex 2024 headed "(12-31-2023)" but figures are 2024 (match KM1 2024).
- UCG (188, first committed this session): FY2024 P&L 19 rows; LR1 p98 860,328 / (43,511), gate 1e-06; total_liabilities not printed (check 2 rows no_liabilities_line); P3 2026-06-30 Data Hub only. 110b mandatorily-FV gains in other_operating_net; item 230 below item 120 not entered; intangibles 2025-12-31 3,607 as printed (CC1 row 8 with reference "(D)").
- SAN (261, first committed this session): FY2024 P&L 26 rows (2024A column re-presented for the Poland discontinued operation); LR1 p20 1,815,887 / -17,977, gate 4e-08; resolution_dgs_contrib missing (no line). Mapping as in session 2: net_fees = income + expense; gains_designated_fvtpl = non-trading mandatorily FVTPL + designated; other_operating_net 5 lines incl. equity method and insurance; pat continuing; deposits_customers 3 customer lines.
- CBK (128, first committed this session): no Pillar 3 (not fetchable) so no KM1/CC1/CR1/LR1 and no scope gate; total_operating_income = 10 printed income lines (toi_summed): 11,107 FY24, 6,092 H1 25, 12,171 FY25, 6,518 H1 26; admin_expenses = IS "Operating expenses" total (no depreciation line: dep_in_admin); total_liabilities not printed (no_liabilities_line); profit_owners = net profit minus NCI (includes AT1 investors); deposits_customers only at Dec dates (note 26, 4 sectors); restructuring expenses have no field.
- DBK (233, first committed this session): admin_expenses = compensation + G&A (B.5, dep_in_admin): 11,731+11,243 FY24, 5,935+4,245 H1 25, 11,813+8,860 FY25, 6,037+4,415 H1 26; total_operating_income = 7 printed income lines (toi_summed): 30,092 / 16,328 / 32,094 / 17,150; FY2024 P&L; LR1 p34 1,397,830 / (1,950), gate 1e-07. deposits_customers = single "Deposits" line (incl. banks); profit_owners includes additional equity components; resolution_dgs_contrib inside G&A.
- KBC (213): P3 workbooks at 4 dates (KM1, CC1 rows 8/30, CR1; sheets store EUR units except the 2Q2025 CR1 sheet in millions); LR1 390,669,381,547 / -34,163,934,566, gate 1e-10; admin_expenses = IS "Operating expenses (excluding opex allocated to insurance expenses)" total (2,518 / 4,706 / 2,727 / FY24 4,565), no depreciation line (dep_in_admin); bank and insurance tax is a sub-line inside that total, not entered; FY2024 P&L.
- BKT (143, first committed this session): H1 2025 P&L from the H1 2026 report's comparative column (B.9, status from_comparative), no 2025-06-30 balance sheet; FY2024 P&L; P3 2026-06-30 workbook (KM1, CC1, CR1; row 030 g and j "-" zero cells); no other Pillar 3, so no LR1 and no scope gate; the 2026 workbook's 2Q25/4Q25 KM1 columns not used (B.9: Bankinter Pillar 3 dates stay blank); gains_designated_fvtpl dash; resolution_dgs_contrib inside other operating expenses.
- DNB (188): P3 workbooks 2024-12-31, 2025-06-30, 2025-12-31 (KM1, CC1, CR1; zero cells 090 d, 030 d/g/j); LR1 3,835,781.4 / -373,557.0, gate 2.5e-04; profit_owners = shareholders + AT1 holders (p12 half years; statement of changes in equity p210 FY); FY admin = staff (salaries + restructuring as in the statement's staff line) + other expenses, from the clean management-report table p53 (the income statement page is garbled); FY2024 P&L from clean pages. P3 2026-06-30 missing (Data Hub).
- CABK (249, first committed this session): P3 workbooks 2025-06-30 and 2026-06-30 (KM1, CC1, CR1; 2026 allowances printed negative -> flip); LR1 659,821.92 / -79,924.649, gate 0; FY2024 P&L 25 rows; at1_instruments = CC1 row 30 before own holdings (EBA is after: 6.2% seam gap).
- ISP (221, first committed this session): FY2024 P&L; LR1 p118 943,452 / -172,933, gate 8e-07; total_liabilities not printed; impairments_nonfin dash; total_operating_income = item 120 (insurance items 160/170 below it, not entered); item 230 not entered; 110b in other_operating_net; cash_cb item 10 includes demand deposits with banks. Hand check inputs 2025-12-31: II 27,758 (p388 item 10), IE 10,448 (item 20), TOI 30,472 (item 120), admin 6,889 + 4,475, depreciation 581 + 1,210, cash_cb 37,868 (p386), loans_all 451,383 + 7,589, debt_securities 162,844 + 855 (P3 p122 CR1).
- SAB (241, first committed this session): P3 workbooks 2025-06-30, 2026-06-30 (KM1, CC1, CR1; 2026 CC1 row 30 matched on label, row number cell empty); LR1 252,372,724.88 / 3,885.12 (EUR thousands, positive), gate 8e-11; FY2024 P&L (TSB restated as discontinued); gains_designated_fvtpl dash; resolution_dgs_contrib no line.
- BPE (225, first committed this session): statements in EUR thousands, P3 in EUR millions; LR1 p34 144,528 / "-" (zero cell), gate 1e-06; total_liabilities not printed; total_equity = group equity + minorities (statement of changes in equity); item 230 left out (EBA TOI includes it: 2767.5 + 233.4 = 3000.9 vs EBA 2999.9); 110b in other_operating_net; impairments_nonfin no line; includes Sondrio from 2025-12-31.
- BMPS (221, first committed this session): FY2025 statements in EUR thousands, half years in EUR millions, P3 in EUR thousands; LR1 p20, gate 4.5e-09; total_liabilities not printed; total_equity from the statement of changes in equity; at1_instruments CC1 row 30 "-" at every date (zero cells); intangibles 2025-12-31 6,415.8m (as printed; includes goodwill in equity investments after Mediobanca); item 230/160/170/140 below item 120 not entered (EBA TOI includes 230); tier1 2025-12-31 cited from its number-only line; includes Mediobanca from 2025-12-31.
- BAMI (248, first committed this session): the 3 later Pillar 3 PDFs print 1,234.5 (decimal point), not a decimal comma: the step 2.2 scan's "," declaration was wrong and is blanked in report_urls.csv. LR1 210,948 / -16,731, gate 6e-07; total_liabilities not printed; total_equity = 8 balance sheet equity items (7 where item 155 is "-"; rotated statement of changes in equity unreadable); insurance 160/170 and item 230 below item 120 not entered; at1_instruments 2025-06-30 1,787 as printed (KM1 implies ~1,389).
- UNI (243, first committed this session): no decimal comma anywhere; P3 workbooks 2025-06-30, 2026-06-30; LR1 workbook -408.563 adjustment, gate 0; loans_all and debt_securities 2024-12-31 missing (CR1 col a split across 2 text lines in the 2024 PDF); deposits_customers missing at half years (only the amortised cost total printed); em-dash zero cells (030 g, 050 d/j); gains_designated_fvtpl dash; resolution_dgs_contrib no line; mandatorily-FVTPL in other_operating_net (SAN puts it in gains_designated_fvtpl).
- UNI total_equity 2025-06-30 removed before commit: Printed "6,993,667" on p.15 of the H1 2025 report is split by text extraction as "6,9 93,667"; provenance cannot match it. Left missing (not partially entered).

### Step 2.3: session 1 per-bank notes (entry counts as of session 1; superseded where a session 2 line differs: zero cells, FY2024 P&L, LR1, workbooks, admin_expenses (B.5, B.6), profit_owners (B.7))

Every field the documents show was entered; what is missing, and why, per bank (from the entry work):

#### NDA (186 entries)
- Missing: debt_securities all dates (CR1 row 090 non performing column blank); trading_assets (no held-for-trading line); dividend_income, gains_derecognition_not_fvtpl, gains_designated_fvtpl, gains_hedge_accounting, exchange_differences (inside "Net result from items at fair value"); provisions, impairments_nonfin (not printed).
- Judgement: resolution_dgs_contrib = "Regulatory fees" (resolution fees + bank tax); impairments_fin = "Net loan losses" (excludes "Net result on loans in hold portfolios mandatorily held at FV"); pbt = "Operating profit"; pat 2025-12-31 from a line merged with the comprehensive income column (same figure); CR1 2026-06-30 row 030 impairments printed "-0", stored 0; CR1 2025-12-31 columns chosen a, d, g, j.
#### DNB (74 entries; no Pillar 3 document)
- Missing: all Pillar 3 fields (Excel only / Data Hub); dividend_income (inside net gains at FV); trading_assets; resolution_dgs_contrib (inside interest expense); provisions, impairments_nonfin.
- Judgement: annual income statement page text is garbled (doubled characters), so FY2025 P&L taken from clean pages of the same report: notes G18 (interest), G19 (fees), financial highlights p8, segment note G3 p216 (depreciation, operating expenses 30 726 as one admin_expenses total excluding depreciation); pat entered as 2 components (pre-tax operating profit + tax) because operations held for sale are shown separately; gains_held_for_trading = whole "Net gains on financial instruments at fair value"; profit_owners FY from note G50 p292.
#### DANSKE (61 entries; no Pillar 3 document)
- Missing: all Pillar 3 fields (Excel only); admin_expenses and depreciation at 2025-06-30 and 2026-06-30 (half-year reports print only an operating expenses total, no group note); profit_owners at 2025-06-30 and 2026-06-30 (no attributable line printed); dividend_income, other income components, resolution_dgs_contrib, provisions, impairments_nonfin.
- Judgement: interest_income = 2 components (effective interest + other interest income); other_operating_net = net insurance result + other income; 2024-12-31 comparative column marked restated (allowed for 2024-12-31 balance sheet values); FY admin_expenses = staff costs + administrative expenses from note G9(a) (administrative expenses include resolution fund and bank tax); pat from the statement of capital (same figure as the income statement).
#### SEB (118 entries)
- Missing: Pillar 3 fields at 2025-06-30 and 2026-06-30 (Excel only); debt_securities (CR1 row 090 non performing blank); trading_assets; dividend_income, other gains lines, provisions; impairments_nonfin at half years (nothing printed).
- Judgement: half-year interest income/expense from Note 2 (statement shows only net interest income); resolution_dgs_contrib = "Imposed levies" (includes Swedish bank tax); impairments_nonfin FY = items affecting comparability -416 (goodwill impairment Card Norway, note G13); deposits_customers = "Deposits and borrowings from the public"; pat 2025-06-30 from key figures p3 and 2025-12-31 from a merged two-column line (same figure); CR1 2024-12-31 from the 2024 Pillar 3, not the restated 2025 comparative.
#### SHB (94 entries)
- Missing: Pillar 3 fields at 2025-06-30 and 2026-06-30 (Excel / Data Hub only); loans_customers_gross and loans_customers_allowance at both Pillar 3 dates (CR1 030 col d and j and 050 col j printed blank); debt_securities (090 col d blank); trading_assets, provisions, impairments_nonfin (not printed).
- Judgement: resolution_dgs_contrib = "Regulatory fees" (risk tax + resolution fee + deposit guarantee); pat = continuing operations at 2025-06-30 and 2025-12-31 (discontinued operations exist), profit for the period at 2026-06-30; profit_owners as printed (total operations); gains_held_for_trading = "Net gains/losses on financial transactions"; 2026-06-30 depreciation cited from the number line (label printed on a separate line).
#### ABN (161 entries)
- Missing: loans_customers_allowance all dates (CR1 030 allowance columns blank); debt_securities all dates (090 col d blank); dividend_income, gains_designated_fvtpl, gains_hedge_accounting, exchange_differences, resolution_dgs_contrib, provisions, impairments_nonfin (not printed).
- Judgement: other_operating_net = other operating activities + share of equity-accounted investments; deposits_customers 2025-06-30 = 4 components (current accounts, demand, time, other) since no total printed; impairments_fin 2025-06-30 printed -1 in an expense section where charges are positive (stored -1, a net release); KM1 regulatory basis (excludes interim profit).
#### SWED (109 entries)
- Missing: Pillar 3 fields at 2026-06-30 (Data Hub ZIP only); loans_customers_gross and loans_customers_allowance at all 3 Pillar 3 dates (CR1 030 col d and j blank); debt_securities (090 col d blank); dividend_income, trading_assets, provisions, other gains lines (one "Net gains and losses on financial items" line).
- Judgement: admin_expenses has a 3rd component "VAT reimbursements" (-1 539 at 2025-12-31, stored negative; 0 at 2026-06-30), as the statement nets it; resolution_dgs_contrib = "Bank taxes and resolution fees"; impairments_nonfin = impairment of tangible assets (0); profit_owners at half years from the EPS note; 2024 CR1 has no row numbers (matched on labels).
#### INGA (186 entries)
- Missing: Pillar 3 fields at 2025-06-30 (Excel only); debt_securities (CR1 090 col d blank); trading_assets at half years (only FVTPL total printed); dividend_income (inside "Investment income"); resolution_dgs_contrib (only in the opex note, left inside admin_expenses); impairments_nonfin.
- Judgement: admin_expenses = staff expenses + 10 lines of the operating expenses note (excludes depreciation and provisions, which are entered from the same note); provisions = "Additions and releases of provisions" from the opex note; other_operating_net = investment income + associates + impairment of associates + other net income (FY), investment income + other net income (half years); FY2025 and 2024 CC1 rows 8 and 30 cited from number lines identified by row number (rotated labels); AT1 classified as liability, so total_equity excludes it.
#### KBC (93 entries; no Pillar 3 document)
- Missing: all Pillar 3 fields (Excel only); provisions, gains_derecognition_not_fvtpl, gains_designated_fvtpl, gains_hedge_accounting, exchange_differences (not printed).
- Judgement / doubt: admin_expenses (staff + 5 general administrative lines) and depreciation from the "operating expenses by nature" note; that note includes opex allocated to insurance service expenses (559m FY2025, 280m H1 2025, 309m H1 2026), so it is wider than the income statement opex line (4 706 FY2025). resolution_dgs_contrib = "Bank and insurance tax" (own line, broader than resolution/DGS). deposits_customers from note 4.1 "Subtotal deposits from customers" (total column, not pro forma); trading_assets = "of which held for trading"; other_operating_net = insurance revenues before reinsurance + insurance finance income/expense + net other income; share of associates sits below total income (not entered).
#### RABO (194 entries)
- Missing: debt_securities all dates (CR1 090 col d blank); gains_derecognition_not_fvtpl at 2026-06-30 (the amortised-cost value prints on a line "4 4" that cannot be matched uniquely; the field dropped, income check gap 2m); impairments_nonfin 2025-12-31 (dash); provisions, dividend_income.
- Doubt (reviewer): profit_owners = "Of which attributed to Rabobank" (4,262 / 2,334 / 2,367), which excludes Rabobank Certificates (CET1) and Capital Securities (AT1) holders. EBA's figure (2,660 at 2025-06-30) equals the broader owners figure (Rabobank + Certificates + Capital Securities), printed only as a column of the statement of changes in equity.
- Judgement: resolution_dgs_contrib = "Regulatory levies"; cash_cb = "Cash and cash equivalents"; other_operating_net = other operating activities + associates/JVs + other income.
#### GLE (211 entries)
- Missing: debt_securities at 2025-12-31 and 2026-06-30 (CR1 090 col d printed "-"); trading_assets (only a combined FVTPL line); dividend_income, resolution_dgs_contrib (inside "Taxes and levies", note 5.2), provisions, impairments_nonfin.
- Judgement: admin_expenses = 3 components from note 5 Table 5.A (personnel, other operating expenses, and "other general operating expenses attributable to insurance contracts" stored negative, so the total equals what the income statement deducts); net gains on financial transactions split by "o/w" sub-lines (FVTPL -> gains_held_for_trading; FVOCI and amortised-cost derecognition -> gains_derecognition_not_fvtpl); other_operating_net = 8 components (insurance lines, cost of credit risk of insurance financial assets inside NBI, lease/mobility income and expense); net_fees = fee income + fee expense; CC1 2024 row 30 = 9,323.
#### BNP (197 entries)
- Missing: dividend_income (inside FVOCI gains line), resolution_dgs_contrib (inside taxes and contributions, note 2.f), provisions (the legal-risk cost line left out), impairments_nonfin (the "Goodwill" +48 line is a net gain, left out), trading_assets (no held-for-trading line).
- Judgement / doubt: admin_expenses = staff costs + "Other operating expenses for banking activities" (note 2.f), 29,291 FY2025 against the 29,003 opex total: the insurance non-attributable costs (877) and the reclassification to insurance contracts (+1,165) are left out. GLE instead includes its insurance reallocation line so its admin_expenses equals the income statement deduction: the 2 treatments differ. net_fees = commission income + expense; other_operating_net = insurance net income + income and expense of other activities; Pillar 3 from URD chapter 5 (doc_type pillar3).
#### BKT (64 entries; only the FY2025 annual and H1 2026 reports downloaded)
- Missing: every field at 2025-06-30 (H1 2025 report not downloadable: bot protection, 403); all Pillar 3 fields (not available); gains_designated_fvtpl (dash); resolution_dgs_contrib (inside other operating expenses).
- Judgement: amounts in EUR thousands; other_operating_net = equity-method share + non-trading mandatorily FVTPL gains + other operating income + other operating expenses; deposits_customers = customer deposits at amortised cost only (2024-12-31 excludes 1,672,108k held-for-trading customer deposits; 2026-06-30 from note 10); 2026-06-30 impairments_nonfin printed 6,046 without brackets but subtracted (stored positive); 2 half-year lines cited from number-only lines (labels split).
#### CBK (78 entries; no Pillar 3 document found)
- Missing: all Pillar 3 fields (direct PDFs not found); total_operating_income every date (no total income line printed; check 3 cannot run); total_liabilities (not printed); deposits_customers at half years (notes not split by counterparty); impairments_nonfin (dash / not printed); provisions (inside other net income).
- Judgement: deposits_customers at 2024-12-31 and 2025-12-31 = note 26 (p320) 4 counterparty components (corporates, private customers, other financial corporations, general governments), amortised cost only; profit_owners 2025-06-30 label includes investors in additional equity components (AT1); gains_derecognition_not_fvtpl = disposal at amortised cost + other sundry realised profit or loss; gains_held_for_trading = whole FVTPL line; resolution_dgs_contrib = "Compulsory contributions" (includes Polish bank tax); restructuring expenses (562 FY2025) have no field.
#### DBK (186 entries)
- Missing (reviewer question): admin_expenses and depreciation at every P&L date: "General and administrative expenses" includes depreciation and amortisation (note 23: "EUR 1.2 billion were included in general and administrative expenses") and no depreciation line is printed, so no split excluding depreciation exists; opex, cost_income, cost_assets and ppp_assets are therefore blank for DBK. Printed: compensation 11,813 / 5,935 / 6,037 and G&A 8,860 / 4,245 / 4,415 (FY2025 / H1 2025 / H1 2026). Also missing: resolution_dgs_contrib (inside G&A), provisions, impairments_nonfin (dash / 0), dividend_income.
- Judgement: total_operating_income = "Memo: Total net revenues" (FY, AR p44) and segment-results "Net revenues" (half years), each = NII + total noninterest income, since the IFRS statement has no total line; deposits_customers = the single balance sheet "Deposits" line (includes deposits from banks; not split); profit_owners = attributable to DB shareholders and additional equity components (includes AT1); other_operating_net = equity method + "Other income (loss)" (includes hedge-accounting results); CR1 rows unnumbered (matched on labels).
#### SAB (152 entries)
- Missing: Pillar 3 fields at 2025-06-30 and 2026-06-30 (Excel only); gains_designated_fvtpl (dash); resolution_dgs_contrib (no line).
- Judgement: EUR thousands; TSB is a discontinued operation from FY2025: pat = continuing operations at 2025-12-31 and 2026-06-30, profit_owners as printed (includes discontinued); H1 2025 from the original report (TSB still included); the 2025-12-31 balance sheet holds TSB as held for sale (assets 52,549,489k, liabilities 49,333,344k), so deposits and CR1 loans drop from 2024 to 2025 while total assets do not; other_operating_net = equity-method share + non-trading mandatorily FVTPL + other operating income and expenses; impairments_nonfin = non-financial assets line only; provisions FY2025 a net release (stored negative).
#### SAN (233 entries)
- Missing: resolution_dgs_contrib (no income statement line).
- Judgement: net_fees = commission income + expense; gains_designated_fvtpl = non-trading mandatorily FVTPL + designated FVTPL; other_operating_net = equity-method income + other operating income and expenses + insurance income and expenses (5); pat = continuing operations (discontinued operations exist: Poland sale); deposits_customers = 3 customer deposit lines (held for trading, designated, amortised cost), half years from the management report's condensed balance sheet (p19, p20); CC1 row 30 (EBA AT1 is close to rows 30 + 34).
#### CABK (158 entries)
- Missing: Pillar 3 fields at 2025-06-30 and 2026-06-30 (Excel only); resolution_dgs_contrib (inside other operating expenses).
- Judgement: other_operating_net = equity-method share + other operating income and expenses + insurance service result + reinsurance result (5); gains_designated_fvtpl = non-trading mandatorily FVTPL (no designated line printed); deposits_customers = amortised-cost "Customers" line (excludes 4,269 designated at FVTPL at 2025-12-31); at1_instruments = CC1 row 30 before own-holdings deduction; CR1 in the 17-column CRR3 layout (a, d, g, j); 2 hedge lines and the 2025-06-30 provisions line print a note number before the value (value taken after it); interest_expense includes insurance finance expense as printed.


## Tests run

Repo root at f8adbcb:

```
$ pytest -q
.....................                                                    [100%]
21 passed
$ ruff check .
All checks passed!
```

The 21 tests are the 20 from session 1 plus `test_provenance_styles` (step 2.4). The fresh-clone run below uses `-p socket --disable-socket`.

## Fresh-clone check

Clone path: `C:\Users\astha\AppData\Local\Temp\claude\...\scratchpad\fc3`, on Windows (no Linux machine was available). The check was run at f8adbcb, the last step commit, after it was pushed.

```
$ git clone https://github.com/uty101/Bank-Performance-Benchmarking.git fc3
$ git log --oneline -1
f8adbcb step 2.5: KPIs at 2025-12-31 and 2026-06-30 for EU banks
$ uv venv --python 3.12
$ uv pip install -r requirements-lock.txt
$ uv pip install -e . --no-deps
$ ruff check .
All checks passed!
$ pytest -p socket --disable-socket -q

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
21 passed, 1 warning in 48.04s
$ python scripts/run_all.py
facts 23438 rows, kpi 9880 rows, checks 33551 rows
$ git status --short
```

`run_all.py` rebuilt `outputs/tables/kpi.csv` and `outputs/tables/checks.csv` byte-identical to the committed files: `git status --short` is empty after the run.

## Runtime per step

Session 2. Times are approximate, taken from file and commit times.

- **2.0b:** about 1 h of edits: decisions, config, the workbook reader in `fetch_reports.py`, and the B.1, B.4, B.5 and B.8 code.
- **The ECB outage:**
  - The fx stage (RON) failed from about 13:00 to 14:25 UTC on 2026-11-03: data API read timeouts and 504s, retried every 5 minutes, 16 failed tries.
  - It then succeeded on a direct run (14:25 to 14:44).
  - The 2.0b commit waited for it, because RON is part of that step.
- **2.3, entries:** about 2 h 30 min.
  - Fix passes on the 13 committed banks and entry of the other 13, by parallel agents working from specs.
  - Workbook downloads for the new Pillar 3 documents.
  - Merging, caching and provenance took about 20 s per bank: 26 commits in 9 minutes.
- **2.4 and 2.5:** about 30 min. `run_all.py` takes 55 s.

## Deviations from PLAN.md

Session 1's deviations 1 to 9 stand. They are in the review at a5c5bc0 and are repeated briefly here:
1. the `decimal_mark` column in `report_urls.csv`;
2. merger sources fetched through `fetch_reports.py`, with doc_type `merger_target`;
3. fetch retries and a curl fallback that keeps TLS certificate checks on;
4. summed fields marked `component k/n`;
5. entry value and sign rules;
6. `levies_in_admin` as a usable status;
7. check 3 on report rows, summing only the lines the statement prints;
8. entries made through per-bank specs, with the snippet copied from the cited line;
9. 2 fix commits outside the one-commit-per-step rule.

New in session 2:

10. **Stop evidence: SHB scope gate (rule 4, SHB only).**
    - What SHB's LR1 at 2025-06-30 prints:
      - row 1, "Total assets as per published financial statements", is 3,372,742m SEK;
      - row 2 is +288,024m SEK;
      - their sum, 3,660,767m, is the balance sheet total;
      - EBA total assets (EUR 302.6bn) equal row 1 alone.
    - So SHB fills row 1 with the prudential total and row 2 with the add-back, the reverse of the template's intent. The B.1 formula therefore gives 8.54% > 2%.
    - The rows are under Evidence (scope gate and scope table).
    - Treatment, per B.1:
      - SHB's report and p3 FACTS keep their values with status `scope_gate_failed`, so the checks still see them;
      - `kpi.py` treats that status as unusable, so SHB's KPI rows after 2025-06-30 are blank (22 per basis, 44 in all);
      - every other bank was finished.
11. **xlsx and xls workbooks as sources (B.3).**
    - `fetch_reports.py` recognises xlsx, xls (OLE header) and a ZIP holding a PDF.
    - It writes each sheet as a tab-separated text page, with numbers formatted with `.15g` and never in exponent form.
    - Danske's workbooks are `.xls`, so `xlrd` was added to the dev extras and the lock (`xlrd==2.0.2`, the only lock change).
    - SWED's 2026-06-30 Pillar 3 came from a Data Hub ZIP that can be downloaded by script.
12. **KBC workbook units.** KBC's workbooks store EUR units under "EUR millions" headers. Exception: the 2Q2025 CR1 sheet, which is in millions. `unit_scale` follows the stored cell.
13. **BAMI decimal marks.**
    - The step 2.2 scan had declared `,` for BAMI's 3 later Pillar 3 PDFs, but they print `1,234.5`.
    - The declaration was blanked in `report_urls.csv`.
    - The only `,` documents left are BPE 2021-12-31, BPE 2024-12-31 and UNI 2020-12-31, all merger targets.
14. **Exact entry values.**
    - The scratchpad entry writer had formatted `value` with 10 significant digits. That broke provenance on about 120 workbook rows with long cell values.
    - It now computes |printed| × unit_scale in Decimal arithmetic, and all 26 banks' entries were regenerated before any commit.
15. **Zero rows in provenance (B.4).**
    - A zero row passes if its row label is on the cited page.
    - When the snippet line holds no words (UNI prints a bare em dash on its own line), the check falls back to an exact match of that line on the page.
    - 79 zero cells were entered.
16. **KPI statuses carried (step 2.5).**
    - `kpi.py` had reported `ok` for a KPI built from inputs with a usable status.
    - A KPI now carries those statuses, joined in USABLE order (for example `levies_in_admin;dep_in_admin`).
    - This makes B.5 (`dep_in_admin`), B.8 (`toi_summed`) and B.9 (`from_comparative`) visible in `kpi.csv`.
17. **p3 + report ratio pairs after 2025-06-30.**
    - A ratio may take its numerator from p3 and its denominator from report (or the reverse) at the same date. Family `p3+report`, 45 reported-basis rows; rwa_density is an example.
    - Averages and rolling sums still stay inside one family.
18. **`mixed_family` blanks.**
    - BKT at 2026-06-30: averages need 2025-06-30, where BKT has no report balance sheet (its H1 2025 report returned 403, see B.9). B.2 forbids an eba/report pair, so roa, ppp_assets, nim, cost_assets and cost_of_risk are blank.
    - UNI nim at 2025-12-31: the same cause, with the 2024-12-31 report-family loans_all and debt_securities missing.
19. **UNI total_equity at 2025-06-30 left out.** The printed 6,993,667 comes out of pdfplumber as `6,9 93,667`, so provenance cannot match it. The row was removed before UNI's commit rather than committed as a failure.
20. **The 2.0b commit carries the code for B.1, B.3, B.4, B.5, B.8 and B.9** (`bpb/ingest.py`, `bpb/checks.py`, `bpb/kpi.py` and `scripts/fetch_reports.py`). The decisions cannot be applied without it. B.11 put `tests/test_checks.py` and `scripts/run_all.py` under step 2.4, and they still matched instruction 02 unchanged.

#### Stop evidence

**CAG (session 1, instruction 02 B.3).**
- Report total_assets (2,614,010m) were 19.48% above EBA (2,187,749m).
- CAG's LR1 row 2, (426,262), bridges the gap exactly.
- Instruction 02b B.1 replaced that gate with the scope adjusted gate, which CAG passes.

**SHB (session 2, instruction 02b B.1).**
- Its LR1 rows and balance sheet total at 2025-06-30, from `report_entries.csv`, are printed below with the scope gate rows from `outputs/tables/checks.csv`.
- After them comes the count of SHB's KPI statuses after 2025-06-30 (both bases).

```
bank_id   ref_date                field value_as_printed unit_scale         value ccy  doc_type   page                                                                                                                                       snippet
    SHB 2025-06-30         total_assets        3,660,767    1000000 3660767000000 SEK half_year     25                                                                        Total assets Note 18 3,660,767 3,702,091 3,539,173 3,756,046 3,727,558
    SHB 2025-06-30     lr1_total_assets   3372742.222818    1000000 3372742222818 SEK   pillar3 LR1!D8                                                                         1\tTotal assets as per published financial statements\t3372742.222818
    SHB 2025-06-30 lr1_scope_adjustment     288024.36346    1000000  288024363460 SEK   pillar3 LR1!D9 2\tAdjustment for entities which are consolidated for accounting purposes but are outside the scope of prudential consolidation\t288024.36346
    CAG 2025-06-30         total_assets        2,614,010    1000000 2614010000000 EUR half_year     10                                                                                                              TOTAL ASSETS 2,614,010 2,601,727
    CAG 2025-06-30     lr1_total_assets        2 614 011    1000000 2614011000000 EUR   pillar3     11                                                                                1 Total assets as per published financial statements 2 614 011
    CAG 2025-06-30 lr1_scope_adjustment        (426 262)    1000000 -426262000000 EUR   pillar3     11                                                                                                                                   2 (426 262)
```

```
        check bank_id   ref_date        field      value_a      value_b     diff_abs     diff_rel  threshold passed                   note
8b_scope_gate     CAG 2025-06-30 total_assets 2.187749e+12 2.187749e+12 1.112021e+05 5.082943e-08       0.02   True lr1 row 1 + row 2, EUR
8b_scope_gate     SHB 2025-06-30 total_assets 3.025829e+11 3.284230e+11 2.584004e+10 8.539821e-02       0.02  False lr1 row 1 + row 2, SEK
```

```
                           status  rows
                scope_gate_failed    44
                pending_section_3    16
          missing_input:npl_gross     2
      missing_input:npl_allowance     2
               missing_input:cet1     2
              missing_input:tier1     2
                missing_input:rwa     2
missing_input:loans_customers_net     2
                missing_input:lcr     2
               missing_input:nsfr     2
```

## Not verified

- **Seam 2 explanations.**
  - Large P&L differences are reasoned from line definitions, not checked against EBA definitions. Examples are other_operating_net and the gains lines, where EBA FINREP and the income statement group lines differently.
  - Total assets are now explained for every bank with LR1, via the scope table.
- **DANSKE passes the gate with LR1 row 2 = 0.**
  - Its LR1 row 1 (3,202,135.5m DKK) is already the prudential total, so the gate compares prudential with prudential.
  - Report total assets are 16.8% above EBA (scope table).
  - SHB fails because its row 2 is non-zero. The two banks fill the template the same way, and only the sign of the formula's outcome differs.
- **Shares of KPIs from p3+report pairs.** These depend on the bank's KM1 and its income statement being on the same consolidation scope. This was not checked bank by bank.

## Open questions

1. **SHB (the stop):**
   - (a) Leave SHB out of report-family KPIs.
   - (b) Gate SHB on LR1 row 1 alone, since its row 1 already equals EBA.
   - (c) Gate every bank on report total_assets + row 2, as in the scope table. On that basis SHB is 17.1% and DANSKE 16.8% off, and both would fail.
2. **Documents not obtained** (listed under Evidence):
   - the Data Hub is the only source for DNB, SHB and UCG Pillar 3 at 2026-06-30. EDAP serves these files through Power BI only, with no per-bank file URL;
   - Commerzbank's Disclosure Report at all 4 dates: the links are built client-side by an authenticated EQS API;
   - Bankinter's H1 2025 report and its Pillar 3 reports for 2024-12-31, 2025-06-30 and 2025-12-31: 403 bot protection, not circumvented.
   - Under B.9 the Bankinter Pillar 3 dates stay blank. The KM1 comparative columns for 2Q25 and 4Q25 in the 2026 workbook were not used. Should they be?
3. **CBK and BKT have no LR1,** so there is no scope check for them.
4. **Outlier check 9:** 14 rows fail. These are the same 14 EBA rows with the same results as in Section 1.

## Files changed

Changes since the session 1 stop (57f4b68..f8adbcb):
- **Decisions and instructions:**
  - `decisions/section_2_stop_review.md` (new);
  - `CLAUDE.md`: amendments 16 to 25, plus the superseded note in amendment 13.
- **Config:**
  - `config.toml`: RON;
  - `config/fields.yaml`: lr1_total_assets, lr1_scope_adjustment;
  - `config/source_map.yaml`.
- **FX data:** `data/raw/fx/RON.csv` (new), `data/raw/MANIFEST.json`.
- **Manual data:**
  - `data/manual/mergers.csv`: UBI unit and AXA IM sized by consideration;
  - `data/manual/report_urls.csv`: new documents, the BAMI decimal marks, 2 merger targets;
  - `data/manual/report_entries.csv`: 5,589 rows across 26 banks.
- **Report data:** `data/raw/report_manifest.csv` (workbooks added); `data/raw/report_text/*.jsonl.gz` (cited pages and sheets only).
- **Scripts:**
  - `scripts/fetch_reports.py`: workbooks, the ZIP-held PDF, and sheet text;
  - `scripts/run_all.py`: KPIs to 2026-06-30, checks on every family.
- **Code:**
  - `bpb/ingest.py`: zero cells, from_comparative, toi_summed, the scope gate status;
  - `bpb/checks.py`: sheet pages, zero-row labels, no_liabilities_line, scope_gate;
  - `bpb/kpi.py`: USABLE statuses, IN_ADMIN, p3+report pairs, carried statuses.
- **Tests:** `tests/test_checks.py` (test_provenance_styles).
- **Dependencies:** `pyproject.toml` and `requirements-lock.txt` (xlrd).
- **Outputs:** `outputs/tables/kpi.csv`, `outputs/tables/checks.csv`.

## Reviewer reads

1. The outcome paragraph, then Deviation 10 (SHB) and the scope gate and scope table under Evidence.
2. Open question 1.
3. The provenance pass rate, and the counts by check in `checks.csv`.
4. Seam 1, and the head of seam 2.
5. The KPI tables for ISP, SWED, BBVA and CAG, then the hand check.
6. The coverage table, and the blank KPIs after 2025-06-30.
7. The per-bank notes for DBK, CBK, KBC and DANSKE: these carry the B.5 and B.8 statuses.
