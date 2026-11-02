# Section 2

**Outcome: stopped at step 2.3, CAG (rule 4).** Instruction 02 B.3 sets a gate: "CAG total_assets at 2025-06-30 from report and from eba must agree within 2%. If not, stop under rule 4." CAG's entries are Crédit Agricole Group figures (pat and profit_owners agree with EBA within 0.02%, seam 1 agrees within 0.0003%), but report total_assets (2,614,010m) are 19.48% above EBA (2,187,749m). The Group's own EU LR1 (Pillar 3 30/06/2025, p11) bridges the two exactly: "1 Total assets as per published financial statements 2 614 011", "2 (426 262)" for entities "consolidated for accounting purposes but ... outside the scope of prudential consolidation" (insurance), leaving 2,187,749. The gap is a scope difference, not a CASA/Group mix-up, but the gate is fixed, so the section stops here. CAG's entries are committed as the evidence; no bank after CAG is committed, and steps 2.4 and 2.5 were not run.

## Steps completed

- 2.0 apply section 1 review decisions (6efb278)
- 2.1 load_p3 and load_report_entries (eb9aecc); fix: provenance reads ASCII digits only, provenance on mergers.csv rows (92cda21)
- 2.2 report URLs and fetch (71154d8); fix: ruff PLW1510 in fetch_reports.py (811eec3)
- 2.3 entries, universe order, 1 commit per bank: NDA (1e8959e), DNB (c0b5c60), DANSKE (da57e5b), SEB (982c977), SHB (0652103), SWED (f246388), INGA (efe4b74), ABN (23b15dc), KBC (8376a6c), RABO (26d7e4a), BNP (fd99099), GLE (642a65d), CAG (25ecc99), then stopped at the CAG gate
- 2.4, 2.5: not run (stop)

## Evidence

### Step 2.0: mergers

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
        ABN                                  Hauck Aufh�user Lampe Privatbank AG      2025-07-01         1.177700e+10        EUR 2025-06-30               4.142951e+11             1.177700e+10 0.028427 False                                                             
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

### Steps 2.2 and 2.3: documents, entries, provenance, seams

Every table below is printed by a script from the committed files (seams use the committed `bpb/checks.py`).

#### report_manifest.csv in full

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
   BMPS        annual 2025-12-31 e35390a41b09f45f0a21be538499dc6f49c12186f5765627bdde73dc749552fe 11359888  1216 2026-11-02T16:31:58Z                                                                                                                                                                https://www.gruppomps.it/static/upload/ann/annual-report-2025.pdf
   BMPS     half_year 2025-06-30 84d7df338b99cc5a8eb472d8cfeda7594b99547e5c55bd8af95c4e8fc7e9fb30  4375884   145 2026-11-02T16:32:22Z                                                                                                                                          https://www.gruppomps.it/static/upload/_con/consolidate-half_yearly-report-30062025.pdf
   BMPS     half_year 2026-06-30 6fb43542d89140102c4e3be283160172b1468e70b6dd4dbf2b434ca05f025e3e  5488936   220 2026-11-02T16:32:30Z                                                                                                                                             https://www.gruppomps.it/static/upload/_con/consolidated-half-yearly-report-2026.pdf
   BMPS merger_target 2024-12-31 0d1119ccb84dcd0bb91e9842b46ff3bf4b3e0621b0e68403bc6cbe78beafbf17   868150   210 2026-11-02T16:09:37Z                                                                                                                                      https://www.mediobanca.com/static/upload_new/med/0001/mediobanca-semestrale-2024-en_def.pdf
   BMPS       pillar3 2024-12-31 68708350cc063a0305f49f64f82ff08754dcff9d3125f18485f4386efb93b43b  6119614   233 2026-11-02T16:32:36Z                                                                                                                                                 https://www.gruppomps.it/static/upload/pil/pillar-iii-report---december-2024.pdf
   BMPS       pillar3 2025-06-30 77457ff941a4dc6c7c979aea39caeaff76d2a9c79c91aa007e4fcb64d5440c94  4223157   105 2026-11-02T16:32:49Z                                                                                                                                                     https://www.gruppomps.it/static/upload/pil/pillar-iii-report---june-2025.pdf
   BMPS       pillar3 2025-12-31 5bde7cd552b4d911e8889e1c3e4ce949b4ce448cccb3530d212e6299fc5231e8  6594363   262 2026-11-02T16:32:58Z                                                                                                                                                      https://www.gruppomps.it/static/upload/pil/pillar3-report-december-2025.pdf
   BMPS       pillar3 2026-06-30 11fa0beb2ad535cc0c0693d9fd3b24cf9c89f42be8b5697983a3aa6b43d6f8a5  3837650   111 2026-11-02T16:33:10Z                                                                                                                                                        https://www.gruppomps.it/static/upload/pil/pillar3-report---june-2026.pdf
    BNP        annual 2025-12-31 65822993e7ad299d84f16bd4b495391bb670800bb9a0f301ef72e97b6f62a2e2 12235510   936 2026-11-02T16:18:14Z                                                                                                                           https://invest.bnpparibas/en/document/universal-registration-document-annual-financial-report-2025-pdf
    BNP     half_year 2025-06-30 4a9e520c9d8224f9e914dd6fde8f09fc7e50df73d8c1464a5e519a3db8d9301e 12399951   332 2026-11-02T16:18:25Z                                                                                                      https://invest.bnpparibas/en/document/2nd-amendment-to-the-2024-universal-registration-document-and-annual-financial-report
    BNP     half_year 2026-06-30 213831e3a723521ec48a99b12e19ce009ce9c97933c3a53f85240be98cba3969 14725323   316 2026-11-02T16:18:33Z                                                                                                      https://invest.bnpparibas/en/document/2nd-amendment-to-the-2025-universal-registration-document-and-annual-financial-report
    BNP       pillar3 2024-12-31 8af8bcabde1d1822c7193b26dfb2f1c41a40a159f20ae38469960244f05b48e2 17225487   952 2026-11-02T16:18:43Z                                                                                                                           https://invest.bnpparibas/en/document/universal-registration-document-annual-financial-report-2024-pdf
    BNP       pillar3 2025-06-30 4a9e520c9d8224f9e914dd6fde8f09fc7e50df73d8c1464a5e519a3db8d9301e 12399951   332 2026-11-02T16:19:06Z                                                                                                      https://invest.bnpparibas/en/document/2nd-amendment-to-the-2024-universal-registration-document-and-annual-financial-report
    BNP       pillar3 2025-12-31 65822993e7ad299d84f16bd4b495391bb670800bb9a0f301ef72e97b6f62a2e2 12235510   936 2026-11-02T16:19:12Z                                                                                                                           https://invest.bnpparibas/en/document/universal-registration-document-annual-financial-report-2025-pdf
    BNP       pillar3 2026-06-30 213831e3a723521ec48a99b12e19ce009ce9c97933c3a53f85240be98cba3969 14725323   316 2026-11-02T16:19:25Z                                                                                                      https://invest.bnpparibas/en/document/2nd-amendment-to-the-2025-universal-registration-document-and-annual-financial-report
    BPE        annual 2025-12-31 a23880a8af1feffafda72049bdc7e8e69e06c378be7909d254bbb97578666c2a 11440137  1064 2026-11-02T16:31:29Z                                                                                                                https://group.bper.it/documents/133577364/2795795058/2025+Annual+Reports.pdf/d62fc4b8-e447-b337-c81b-d518cf6d25a0
    BPE     half_year 2025-06-30 7701e4e05218c4b4b096f106c731d090d52a6ea3596917d9702ad3d5ffd5b77b  4215086   192 2026-11-02T16:31:37Z                                                                                     https://group.bper.it/documents/133577364/2795795058/Consolidated+Half-Year+Report+as+at+30+06+2025.pdf/ee8e303c-519c-d986-4655-01592227dfab
    BPE     half_year 2026-06-30 866a31842a1deb2b6b9dc1ce1088e9f876623cfafa44612e54a715342aeaf2da  5108805   184 2026-11-02T16:31:40Z                                                                              https://group.bper.it/documents/133577364/2801082007/CONSOLIDATED+INTERIM+FINANCIAL+REPORT+AT+30+JUNE+2026.pdf/aff85517-7264-dc67-1748-8f695a06bdcf
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
   CABK       pillar3 2025-12-31 219948b6064e38a6d3317731980d6c75489c6e79cd34ebce4df05e1b00bfc6d7 13464323   521 2026-11-02T16:24:36Z                                                                             https://www.caixabank.com/deployedfiles/caixabank_com/Estaticos/PDFs/Accionistasinversores/Informacion_economico_financiera/Pillar_3_Report_2025.pdf
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
    SAB       pillar3 2025-12-31 271e5c6cf51af263719151a4b021303f8fd069f6a4a26d4d60f8f44fe55ee767 33440729   442 2026-11-02T16:25:07Z                                                                                                                               https://www.grupbancsabadell.com/corp/files/6000340525667/en_pillariiidisclosures_bsgroup_2025.pdf
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
    SEB       pillar3 2025-12-31 996ae1dfdbe484cfee27a496d26054b17c51b6689ab84f4e04125d92e2f1f26b  1579788   113 2026-11-02T16:15:45Z                                                                                                        https://webapp.sebgroup.com/mb/mblib.nsf/alldocsbyunid/823997216F4EE08EC1258DBD002B9B86/$FILE/Pillar_3_tables_2025_Q4.pdf
    SHB        annual 2025-12-31 3b757bc166dedc47211dcfd6ffdc4c1da60c3dc034613dc654fe7005b1b6c148  5504887   352 2026-11-02T16:15:47Z                                                                                                                                                                              https://mb.cision.com/Main/3555/4313527/3954484.pdf
    SHB     half_year 2025-06-30 db337294e89c8feb0d9b205bf01afe03a4b084a467d0b17487728f5c2ca500e1   919868    67 2026-11-02T16:15:53Z                                                                                                                                                                              https://mb.cision.com/Main/3555/4207558/3581803.pdf
    SHB     half_year 2026-06-30 7983c15f2ab05af94a1c50b7220a89eb0571294c60b2c05d2360fce395ae0b26   883076    65 2026-11-02T16:15:54Z                                                                                                                                                                              https://mb.cision.com/Main/3555/4374686/4192694.pdf
    SHB       pillar3 2024-12-31 dd21c17ebab547222bd26cc33cae07919a59aa8884dfd08233aa041bd6902f8f  3051488   111 2026-11-02T16:15:55Z                                                                                                             https://storage.mfn.se/a/handelsbanken/98f8d9b9-60ae-4a36-8be2-c34713842cda/pillar-3-disclosures-pdf-annual-2024.pdf
    SHB       pillar3 2025-12-31 1d3f71fab3c4e00373bbef549e7b335da3c5c5962f089eb65641b464746cece4 25634443   116 2026-11-02T16:16:00Z                                                                                                             https://storage.mfn.se/a/handelsbanken/ce9b5313-6d37-486c-89fc-582ae5ce34ad/pillar-3-disclosures-pdf-annual-2025.pdf
   SWED        annual 2025-12-31 d16afc74c782c77ccee2384423119d36d2687be5aa5ef33d56107740fe133dba 11234146   340 2026-11-02T16:16:17Z                                                                                                                                https://internetbank.swedbank.se/ConditionsEarchive/download?bankid=1111&id=WEBDOC-PRODE277903288
   SWED     half_year 2025-06-30 fd7458f5148948d722a6dc7f5faa15e18eae40b121e31fccb3ec744fb5f7d60a  5002284    58 2026-11-02T16:16:33Z                                                                                                                                https://internetbank.swedbank.se/ConditionsEarchive/download?bankid=1111&id=WEBDOC-PRODE234709540
   SWED     half_year 2026-06-30 8f41044f33a350646c2fd6c1da5cb52faaaa40fa20174caf178b40282f9b3904  5363968    62 2026-11-02T16:16:38Z                                                                                                                                https://internetbank.swedbank.se/ConditionsEarchive/download?bankid=1111&id=WEBDOC-PRODE307024995
   SWED       pillar3 2024-12-31 03f97ed60bfa8d7c84e47fd03aa19ae1e4d0a8fd12613240261dc4d29740156c  6760282   117 2026-11-02T16:16:44Z                                                                                                                                https://internetbank.swedbank.se/ConditionsEarchive/download?bankid=1111&id=WEBDOC-PRODE221684981
   SWED       pillar3 2025-06-30 614137b8f0e228b90e93ddb82ff1413ec4a9b343fb2d7fcf7a8d90328fcb9f4f  1455933    56 2026-11-02T16:16:51Z                                                                                                                                https://internetbank.swedbank.se/ConditionsEarchive/download?bankid=1111&id=WEBDOC-PRODE248869515
   SWED       pillar3 2025-12-31 f5657b3ebebe821efbd554cc3135f3b4f64a7dd4dc5e79e3733f20e7f559c2b3  1840378   120 2026-11-02T16:16:54Z                                                                                                                                https://internetbank.swedbank.se/ConditionsEarchive/download?bankid=1111&id=WEBDOC-PRODE278025941
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
    UNI       pillar3 2025-12-31 a18359e4f9bcdc2b8fe7435c694b04315631141f0960735bceb973846a31216b  2746865   245 2026-11-02T16:26:49Z                                                 https://www.unicajabanco.com/content/dam/unicaja/unicaja-corporacion/documentos-corporacion/inversores-y-accionistas/informacion-relevancia-prudencial/2025-informe-anual-en.pdf
```

#### documents not downloaded (34), with the URL tried and the URL agent's note

```
bank_id  doc_type     period                                                                                                                                                                                          url                                                                                                                                                                note
    DNB   pillar3 2024-12-31                                                                           https://www.ir.dnb.no/sites/default/files/pr/Risk_and_capital_management_Pillar_3_attachment_%28Excel%29_4Q24.xlsx Excel - Pillar 3 attachment 4Q24 (templates); narrative PDF report 2024 at https://www.ir.dnb.no/sites/default/files/pr/202503192798-3.pdf lacks KM1/CC1/CR1 tables
    DNB   pillar3 2025-06-30                                                                                 https://www.ir.dnb.no/sites/default/files/pr/Risk-and-capital-management-Pillar-3-attachment-Excel-2Q25.xlsx                                                                                                   Excel only - Risk and capital management Pillar 3 attachment 2Q25
    DNB   pillar3 2025-12-31                                                                           https://www.ir.dnb.no/sites/default/files/pr/Risk_and_capital_management_Pillar_3_attachment_%28Excel%29_4Q25.xlsx Excel - Pillar 3 attachment 4Q25 (templates); narrative PDF report 2025 at https://www.ir.dnb.no/sites/default/files/pr/202603113411-3.pdf lacks KM1/CC1/CR1 tables
    DNB   pillar3 2026-06-30                                                                                                     https://edap-public.eba.europa.eu/ExternalLinks/index?id=Mg==&rhversion=20260423085052-2                                                                                     No bank-hosted file; DNB states 2Q26 Pillar 3 is only via EBA Pillar 3 Data Hub
 DANSKE   pillar3 2024-12-31                                                                                https://danskebank.com/-/media/danske-bank-com/file-cloud/2025/2/additional-pillar-3-disclosures-q4-2024.xlsx            Excel - Additional Pillar 3 disclosures Q4 2024 (legacy XLS/OLE header despite .xlsx name; holds templates - Risk Management 2024 PDF lacks KM1/CC1/CR1)
 DANSKE   pillar3 2025-06-30                                                                                https://danskebank.com/-/media/danske-bank-com/file-cloud/2025/7/additional-pillar-3-disclosures-q2-2025.xlsx                                                                     Excel only - Additional Pillar 3 disclosures Q2 2025 (legacy XLS/OLE header despite .xlsx name)
 DANSKE   pillar3 2025-12-31                                                                                https://danskebank.com/-/media/danske-bank-com/file-cloud/2026/2/additional-pillar-3-disclosures-q4-2025.xlsx            Excel - Additional Pillar 3 disclosures Q4 2025 (legacy XLS/OLE header despite .xlsx name; holds templates - Risk Management 2025 PDF lacks KM1/CC1/CR1)
 DANSKE   pillar3 2026-06-30                                                                                https://danskebank.com/-/media/danske-bank-com/file-cloud/2026/7/additional-pillar-3-disclosures-q2-2026.xlsx                                                                     Excel only - Additional Pillar 3 disclosures Q2 2026 (legacy XLS/OLE header despite .xlsx name)
    SEB   pillar3 2025-06-30                                                                   https://webapp.sebgroup.com/mb/mblib.nsf/alldocsbyunid/251456EC17C911C6C1258CC800373A83/$FILE/Pillar_3_tables_2025_Q2.xlsx                                                                                                                                Excel only - Pillar 3 Tables Q2 2025
    SEB   pillar3 2026-06-30                                                                https://webapp.sebgroup.com/mb/mblib.nsf/alldocsbyunid/81EB34F3D6595730C1258E3700396BE2/$FILE/Pillar_3_SEB_Group_Q2_2026.xlsx                                                                                                                                Excel only - Pillar 3 Tables Q2 2026
    SHB   pillar3 2025-06-30                                                                https://storage.mfn.se/a/handelsbanken/1423ee80-cb8b-4be7-9d9f-91a179653520/pillar-203-20-xlsx-20-20interim-20-2025-20q2.xlsx                                                                                                                               Excel only - Pillar 3 interim Q2 2025
    SHB   pillar3 2026-06-30                                                                                                               https://edap-public.eba.europa.eu/Report/index/MTE1?rhversion=20260706134722-2                                                                                  No bank-hosted file for Q2 2026; handelsbanken.com points to EBA Pillar 3 Data Hub
   SWED   pillar3 2026-06-30                                 https://errp.eba.europa.eu/public-documents/P3NONREMDISDOCS/input/M312WZV08Y7LYUC71685.CON_SE_PILLAR3010000_P3NONREMDISDOCS_2026-06-30_20260831092202363.zip                                           ZIP on EBA server (linked from swedbank.com risk-reports page) containing the Q2 2026 Pillar 3 PDF; no PDF on bank domain
   INGA   pillar3 2025-06-30                                                                                      https://www.ing.com/binaries/content/assets/documents/files/2q2025-ing-group-pillar-iii-disclosures.xls                                                                      Excel only - 2Q2025 ING Group Pillar III disclosures (OOXML/PK content despite .xls extension)
    KBC   pillar3 2024-12-31                                                                                   https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/3-Reports/20251020-pillar-3-4q2024.xlsx                                            Excel only: Pillar 3 templates (KM1/CC1/CR1 sheets confirmed); Risk Report 2024 PDF is narrative and refers to this file
    KBC   pillar3 2025-06-30                                                                                 https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/3-Reports/20251020-pillar-3-2q2025-2.xlsx                                                                                                                           Excel only (KM1/CC1/CR1 sheets confirmed)
    KBC   pillar3 2025-12-31                                                                                   https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/3-Reports/20261030-pillar-3-4q2025.xlsx                                                     Excel only (KM1/CC1/CR1 confirmed); narrative Risk Report 2025 PDF at .../Results/jvs-2025/risk-report-2025.pdf
    KBC   pillar3 2026-06-30                                                                                   https://wcmassets.kbc.be/content/dam/kbccom/doc/investor-relations/3-Reports/20260904-pillar-3-2q2026.xlsx                                                                                                                           Excel only (KM1/CC1/CR1 sheets confirmed)
    CBK   pillar3 2024-12-31                                                                                                                                https://investor-relations.commerzbank.com/disclosure-report/                                                                                                  IR site is JS-rendered (EQS API); direct PDF link not discoverable
    CBK   pillar3 2025-06-30                                                                                                                                https://investor-relations.commerzbank.com/disclosure-report/                                                                                                  IR site is JS-rendered (EQS API); direct PDF link not discoverable
    CBK   pillar3 2025-12-31                                                                                                                                https://investor-relations.commerzbank.com/disclosure-report/                                             Main PDF not found; only ESG annex found (media/document/be38c909-f7cd-41bb-89cd-200eb7cd619c/assets/Annex_4_-_ESG.pdf)
    CBK   pillar3 2026-06-30                                                                                                                                https://investor-relations.commerzbank.com/disclosure-report/                                                                                            Listed on IR reports page (11 Sep 2026) but direct link not discoverable
   CABK   pillar3 2025-06-30                                           https://www.caixabank.com/deployedfiles/caixabank_com/Estaticos/PDFs/Accionistasinversores/Informacion_economico_financiera/Pillar3DataJun-25.xlsx                                                                                                                        Excel only (quarterly Pillar 3 data); no PDF
   CABK   pillar3 2026-06-30                                           https://www.caixabank.com/deployedfiles/caixabank_com/Estaticos/PDFs/Accionistasinversores/Informacion_economico_financiera/Pillar3DataJun-26.xlsx                                                                                                                        Excel only (quarterly Pillar 3 data); no PDF
    SAB   pillar3 2025-06-30                                                                                                         https://www.grupbancsabadell.com/corp/files/6000293693221/bs_irp_-_2025_2t_-_en.xlsx                                                                                                            Excel only for templates; the 2Q25 PDF is ESG risks only
    SAB   pillar3 2026-06-30                                                                                                               https://www.grupbancsabadell.com/corp/files/6000375089198/gbs_p3r_2026_q2.xlsx                                                                                                            Excel only for templates; the 2Q26 PDF is ESG risks only
    BKT half_year 2025-06-30  https://www.bankinter.com/file_source2/webcorporativa/estaticos/pdf/accionistas-e-inversores/informacion-financiera/info-publica-periodica/2025/en_gb-informe-financiero-semestral-2025.pdf                                                                                             Guessed from 2026 naming pattern; unconfirmed; site returns 403 to curl
    BKT   pillar3 2024-12-31                                                                                https://www.bankinter.com/webcorporativa/en/shareholders-investors/financial-information/pillar-3-disclosures                                                                                          File link is on the page's 2024 year tab; not retrievable (bot protection)
    BKT   pillar3 2025-06-30                                                                                https://www.bankinter.com/webcorporativa/en/shareholders-investors/financial-information/pillar-3-disclosures                                                                            File link is on the page's 2025 year tab; not retrievable (bot protection); likely Excel
    BKT   pillar3 2025-12-31                                                                                https://www.bankinter.com/webcorporativa/en/shareholders-investors/financial-information/pillar-3-disclosures                                                                       2025 Prudential Relevance Report published 26 Mar 2026; link not retrievable (bot protection)
    BKT   pillar3 2026-06-30 https://www.bankinter.com/file_source2/webcorporativa/estaticos/pdf/accionistas-e-inversores/informacion-financiera/info-relevancia-prudencial/2026/pillar-3-disclosures-q2-2026-tables.xlsx                                                                                     Excel only (Q2 2026 tables) linked from Pillar 3 page; site returns 403 to curl
    UNI   pillar3 2025-06-30           https://www.unicajabanco.com/content/dam/unicaja/unicaja-corporacion/documentos-corporacion/inversores-y-accionistas/informacion-relevancia-prudencial/2025-segundo-trimestre.xlsx                                                                                                            Excel only (Q2 2025 templates incl. KM1/CC1/CR1); no PDF
    UNI   pillar3 2026-06-30           https://www.unicajabanco.com/content/dam/unicaja/unicaja-corporacion/documentos-corporacion/inversores-y-accionistas/informacion-relevancia-prudencial/2026-segundo-trimestre.xlsx                                                                                                            Excel only (Q2 2026 templates incl. KM1/CC1/CR1); no PDF
    UCG   pillar3 2026-06-30                                                                                                                                https://edap-public.eba.europa.eu/ExternalLinks/index?id=Mg==                                                      Not on bank site: from 31-Mar-2026 UCG publishes Pillar 3 only on EBA Pillar 3 Data Hub (EDAP) per CRR art.434
```

#### NDA: entries per field and date

```
                    field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
           admin_expenses           0           2           2           2
          at1_instruments           1           1           1           1
                  cash_cb           1           1           1           1
                     cet1           0           1           1           1
      cet1_ratio_reported           0           1           1           1
       deposits_customers           1           1           1           1
             depreciation           0           1           1           1
   gains_held_for_trading           0           1           1           1
          impairments_fin           0           1           1           1
    intangibles_deduction           1           1           1           1
         interest_expense           0           1           1           1
          interest_income           0           2           2           2
                      lcr           0           0           1           1
        leverage_exposure           0           1           1           1
                loans_all           2           2           2           2
loans_customers_allowance           8           8           8           8
    loans_customers_gross           8           8           8           8
   loans_households_gross           2           2           2           2
                 net_fees           0           1           1           1
            npl_allowance           1           1           1           1
                npl_gross           1           1           1           1
                     nsfr           0           0           1           1
      other_operating_net           0           3           3           3
                      pat           0           1           1           1
                      pbt           0           1           1           1
            profit_owners           0           1           1           1
   resolution_dgs_contrib           0           1           1           1
                      rwa           0           1           1           1
                    tier1           0           1           1           1
             total_assets           1           1           1           1
             total_equity           1           1           1           1
        total_liabilities           1           1           1           1
   total_operating_income           0           1           1           1
```

#### DNB: entries per field and date

```
                 field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
        admin_expenses           0           2           1           2
               cash_cb           1           1           1           1
    deposits_customers           1           1           1           1
          depreciation           0           1           1           1
gains_held_for_trading           0           1           1           1
       impairments_fin           0           1           1           1
      interest_expense           0           2           1           2
       interest_income           0           2           1           2
              net_fees           0           2           1           2
   other_operating_net           0           4           2           4
                   pat           0           2           2           2
                   pbt           0           1           1           1
         profit_owners           0           1           1           1
          total_assets           1           1           1           1
          total_equity           1           1           1           1
     total_liabilities           1           1           1           1
total_operating_income           0           1           1           1
```

#### DANSKE: entries per field and date

```
                 field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
        admin_expenses           0           0           2           0
               cash_cb           1           1           1           1
    deposits_customers           1           1           1           1
          depreciation           0           0           1           0
gains_held_for_trading           0           1           1           1
       impairments_fin           0           1           1           1
      interest_expense           0           1           1           1
       interest_income           0           2           2           2
              net_fees           0           1           1           1
   other_operating_net           0           2           2           2
                   pat           0           1           1           1
                   pbt           0           1           1           1
         profit_owners           0           0           1           0
          total_assets           1           1           1           1
          total_equity           1           1           1           1
     total_liabilities           1           1           1           1
total_operating_income           0           1           1           1
        trading_assets           1           1           1           1
```

#### SEB: entries per field and date

```
                    field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
           admin_expenses           0           2           2           2
          at1_instruments           1           0           1           0
                  cash_cb           1           1           1           1
                     cet1           0           0           1           0
      cet1_ratio_reported           0           0           1           0
       deposits_customers           1           1           1           1
             depreciation           0           1           1           1
   gains_held_for_trading           0           1           1           1
          impairments_fin           0           1           1           1
       impairments_nonfin           0           0           1           0
    intangibles_deduction           1           0           1           0
         interest_expense           0           1           1           1
          interest_income           0           1           1           1
                      lcr           0           0           1           0
        leverage_exposure           0           0           1           0
                loans_all           2           0           2           0
loans_customers_allowance           8           0           8           0
    loans_customers_gross           8           0           8           0
   loans_households_gross           2           0           2           0
                 net_fees           0           1           1           1
            npl_allowance           1           0           1           0
                npl_gross           1           0           1           0
                     nsfr           0           0           1           0
      other_operating_net           0           1           1           1
                      pat           0           1           1           1
                      pbt           0           1           1           1
            profit_owners           0           1           1           1
   resolution_dgs_contrib           0           1           1           1
                      rwa           0           0           1           0
                    tier1           0           0           1           0
             total_assets           1           1           1           1
             total_equity           1           1           1           1
        total_liabilities           1           1           1           1
   total_operating_income           0           1           1           1
```

#### SHB: entries per field and date

```
                 field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
        admin_expenses           0           2           2           2
       at1_instruments           1           0           1           0
               cash_cb           1           1           1           1
                  cet1           0           0           1           0
   cet1_ratio_reported           0           0           1           0
    deposits_customers           1           1           1           1
          depreciation           0           1           1           1
       dividend_income           0           1           1           1
gains_held_for_trading           0           1           1           1
       impairments_fin           0           1           1           1
 intangibles_deduction           1           0           1           0
      interest_expense           0           1           1           1
       interest_income           0           1           1           1
                   lcr           0           0           1           0
     leverage_exposure           0           0           1           0
             loans_all           2           0           2           0
loans_households_gross           2           0           2           0
              net_fees           0           1           1           1
         npl_allowance           1           0           1           0
             npl_gross           1           0           1           0
                  nsfr           0           0           1           0
   other_operating_net           0           3           3           3
                   pat           0           1           1           1
                   pbt           0           1           1           1
         profit_owners           0           1           1           1
resolution_dgs_contrib           0           1           1           1
                   rwa           0           0           1           0
                 tier1           0           0           1           0
          total_assets           1           1           1           1
          total_equity           1           1           1           1
     total_liabilities           1           1           1           1
total_operating_income           0           1           1           1
```

#### SWED: entries per field and date

```
                 field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
        admin_expenses           0           2           3           3
       at1_instruments           1           1           1           0
               cash_cb           1           1           1           1
                  cet1           0           1           1           0
   cet1_ratio_reported           0           1           1           0
    deposits_customers           1           1           1           1
          depreciation           0           1           1           1
gains_held_for_trading           0           1           1           1
       impairments_fin           0           1           1           1
    impairments_nonfin           0           1           1           1
 intangibles_deduction           1           1           1           0
      interest_expense           0           1           1           1
       interest_income           0           1           1           1
                   lcr           0           0           1           0
     leverage_exposure           0           1           1           0
             loans_all           2           2           2           0
loans_households_gross           2           2           2           0
              net_fees           0           1           1           1
         npl_allowance           1           1           1           0
             npl_gross           1           1           1           0
                  nsfr           0           0           1           0
   other_operating_net           0           3           3           3
                   pat           0           1           1           1
                   pbt           0           1           1           1
         profit_owners           0           1           1           1
resolution_dgs_contrib           0           1           1           1
                   rwa           0           1           1           0
                 tier1           0           1           1           0
          total_assets           1           1           1           1
          total_equity           1           1           1           1
     total_liabilities           1           1           1           1
total_operating_income           0           1           1           1
```

#### INGA: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           0          11          11          11
              at1_instruments           1           0           1           1
                      cash_cb           1           1           1           1
                         cet1           0           0           1           1
          cet1_ratio_reported           0           0           1           1
           deposits_customers           1           1           1           1
                 depreciation           0           2           2           2
gains_derecognition_not_fvtpl           0           0           1           0
       gains_held_for_trading           0           1           1           1
              impairments_fin           0           1           1           1
        intangibles_deduction           1           0           1           1
             interest_expense           0           1           1           1
              interest_income           0           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           0           1           1
                    loans_all           2           0           2           2
    loans_customers_allowance           8           0           8           8
        loans_customers_gross           8           0           8           8
       loans_households_gross           2           0           2           2
                     net_fees           0           1           1           1
                npl_allowance           1           0           1           1
                    npl_gross           1           0           1           1
                         nsfr           0           0           1           1
          other_operating_net           0           2           4           2
                          pat           0           1           1           1
                          pbt           0           1           1           1
                profit_owners           0           1           1           1
                   provisions           0           1           1           1
                          rwa           0           0           1           1
                        tier1           0           0           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
            total_liabilities           1           1           1           1
       total_operating_income           0           1           1           1
               trading_assets           1           0           1           0
```

#### ABN: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           0           2           2           2
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
           deposits_customers           1           4           1           1
                 depreciation           0           1           1           1
gains_derecognition_not_fvtpl           0           1           1           1
       gains_held_for_trading           0           1           1           1
              impairments_fin           0           1           1           1
        intangibles_deduction           1           1           1           1
             interest_expense           0           2           2           2
              interest_income           0           2           2           2
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
                     net_fees           0           1           1           1
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           0           2           2           2
                          pat           0           1           1           1
                          pbt           0           1           1           1
                profit_owners           0           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
            total_liabilities           1           1           1           1
       total_operating_income           0           1           1           1
               trading_assets           1           1           1           1
```

#### KBC: entries per field and date

```
                 field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
        admin_expenses           0           6           6           6
               cash_cb           1           1           1           1
    deposits_customers           1           1           1           1
          depreciation           0           1           1           1
       dividend_income           0           1           1           1
gains_held_for_trading           0           1           1           1
       impairments_fin           0           1           1           1
    impairments_nonfin           0           2           2           2
      interest_expense           0           1           1           1
       interest_income           0           1           1           1
              net_fees           0           1           1           1
   other_operating_net           0           3           3           3
                   pat           0           1           1           1
                   pbt           0           1           1           1
         profit_owners           0           1           1           1
resolution_dgs_contrib           0           1           1           1
          total_assets           1           1           1           1
          total_equity           1           1           1           1
     total_liabilities           1           1           1           1
total_operating_income           0           1           1           1
        trading_assets           1           1           1           1
```

#### RABO: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           0           2           2           2
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
           deposits_customers           1           1           1           1
                 depreciation           0           1           1           1
gains_derecognition_not_fvtpl           0           2           2           0
       gains_held_for_trading           0           1           1           1
              impairments_fin           0           1           1           1
        intangibles_deduction           1           1           1           1
             interest_expense           0           1           1           1
              interest_income           0           2           2           2
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
                     net_fees           0           1           1           1
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           0           3           3           3
                          pat           0           1           1           1
                          pbt           0           1           1           1
                profit_owners           0           1           1           1
       resolution_dgs_contrib           0           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
            total_liabilities           1           1           1           1
       total_operating_income           0           1           1           1
               trading_assets           1           1           1           1
```

#### BNP: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           0           2           2           2
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           2           2
           deposits_customers           1           1           1           1
                 depreciation           0           1           1           1
gains_derecognition_not_fvtpl           0           2           2           2
       gains_held_for_trading           0           1           1           1
              impairments_fin           0           1           1           1
        intangibles_deduction           1           1           1           1
             interest_expense           0           1           1           1
              interest_income           0           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
                     net_fees           0           2           2           2
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           0           3           3           3
                          pat           0           1           1           1
                          pbt           0           1           1           1
                profit_owners           0           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
            total_liabilities           1           1           1           1
       total_operating_income           0           1           1           1
```

#### GLE: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           0           3           3           3
              at1_instruments           1           1           1           1
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           0           0
           deposits_customers           1           1           1           1
                 depreciation           0           1           1           1
gains_derecognition_not_fvtpl           0           2           2           2
       gains_held_for_trading           0           1           1           1
              impairments_fin           0           1           1           1
        intangibles_deduction           1           1           1           1
             interest_expense           0           1           1           1
              interest_income           0           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
                     net_fees           0           2           2           2
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           0           8           8           8
                          pat           0           1           1           1
                          pbt           0           1           1           1
                profit_owners           0           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
            total_liabilities           1           1           1           1
       total_operating_income           0           1           1           1
```

#### CAG: entries per field and date

```
                        field  2024-12-31  2025-06-30  2025-12-31  2026-06-30
               admin_expenses           0           4           4           4
                      cash_cb           1           1           1           1
                         cet1           0           1           1           1
          cet1_ratio_reported           0           1           1           1
              debt_securities           2           2           2           2
           deposits_customers           1           1           1           1
                 depreciation           0           1           1           1
              dividend_income           0           1           1           1
gains_derecognition_not_fvtpl           0           2           2           2
       gains_designated_fvtpl           0           1           1           1
       gains_held_for_trading           0           1           1           1
              impairments_fin           0           1           1           1
             interest_expense           0           1           1           1
              interest_income           0           1           1           1
                          lcr           0           0           1           1
            leverage_exposure           0           1           1           1
                    loans_all           2           2           2           2
    loans_customers_allowance           8           8           8           8
        loans_customers_gross           8           8           8           8
       loans_households_gross           2           2           2           2
                     net_fees           0           2           2           2
                npl_allowance           1           1           1           1
                    npl_gross           1           1           1           1
                         nsfr           0           0           1           1
          other_operating_net           0           3           3           3
                          pat           0           1           1           1
                          pbt           0           1           1           1
                profit_owners           0           1           1           1
                          rwa           0           1           1           1
                        tier1           0           1           1           1
                 total_assets           1           1           1           1
                 total_equity           1           1           1           1
            total_liabilities           1           1           1           1
       total_operating_income           0           1           1           1
               trading_assets           1           1           1           1
```

#### provenance (check 1) on report_entries.csv: 1889 of 1889 passed

```
bank_id  sum  count
    NDA  186    186
    DNB   74     74
 DANSKE   61     61
    SEB  118    118
    SHB   94     94
   SWED  109    109
   INGA  186    186
    ABN  161    161
    KBC   93     93
   RABO  194    194
    BNP  197    197
    GLE  211    211
    CAG  205    205
```

#### provenance rows that failed

```
none
```

#### provenance on mergers.csv rows sized from a hashed PDF

```
bank_id   ref_date      value_a  passed                                                                                 note
   CABK 2021-03-26 2.098419e+11    True                                  Bankia S.A.; 89d03b3cfde9@15; printed at scale 1000
    UNI 2021-07-30 4.751010e+10    True                               Liberbank S.A.; 2a3b0df0f556@33; printed at scale 1000
    BPE 2022-06-03 2.230982e+10    True                          Banca Carige S.p.A.; 1e30783de2e9@76; printed at scale 1000
    GLE 2023-05-22 3.452025e+10    True LeasePlan Corporation N.V. (via ALD/Ayvens); 65c0a58690b2@118; printed at scale 1000
    DBK 2023-10-13 6.227960e+08    True                       Numis Corporation plc; 43e693fd5a14@121; printed at scale 1000
    UCG 2024-11-04 2.357102e+10    True                      Alpha Bank Romania S.A.; bacb44c8e0a5@11; printed at scale 1000
   BAMI 2025-04-11 2.689939e+09    True    Anima Holding S.p.A. (via Banco BPM Vita); 049915f5f8b2@38; printed at scale 1000
    BPE 2025-07-18 5.662858e+10    True             Banca Popolare di Sondrio S.p.A.; 766c124b2182@40; printed at scale 1000
   BMPS 2025-09-15 9.991165e+10    True                            Mediobanca S.p.A.; 0d1119ccb84d@58; printed at scale 1000
```

#### entry FACTS rejected by the source map

```
none
```

#### seam 1 (check 7) at 2025-06-30, banks entered so far (value_a eba EUR, value_b p3 in EUR)

```
         check bank_id   ref_date             field      value_a      value_b      diff_abs     diff_rel  threshold  passed                note
7_seam_capital     ABN 2025-06-30              cet1 2.032130e+10 2.032100e+10 299382.529999 1.473245e-05      0.001    True   p3 EUR 2.0321e+10
7_seam_capital     ABN 2025-06-30 leverage_exposure 4.489414e+11 4.489410e+11 370416.614014 8.250891e-07      0.001    True  p3 EUR 4.48941e+11
7_seam_capital     ABN 2025-06-30               rwa 1.397895e+11 1.397890e+11 476483.890015 3.408582e-06      0.001    True  p3 EUR 1.39789e+11
7_seam_capital     BNP 2025-06-30              cet1 9.828056e+10 9.828100e+10 435571.000000 4.431914e-06      0.001    True   p3 EUR 9.8281e+10
7_seam_capital     BNP 2025-06-30 leverage_exposure 2.604850e+12 2.604850e+12 230790.299805 8.860023e-08      0.001    True  p3 EUR 2.60485e+12
7_seam_capital     BNP 2025-06-30               rwa 7.888496e+11 7.888500e+11 444562.650024 5.635582e-07      0.001    True   p3 EUR 7.8885e+11
7_seam_capital     CAG 2025-06-30              cet1 1.141072e+11 1.141070e+11 248902.859009 2.181306e-06      0.001    True  p3 EUR 1.14107e+11
7_seam_capital     CAG 2025-06-30 leverage_exposure 2.190715e+12 2.190715e+12  34587.530029 1.578824e-08      0.001    True p3 EUR 2.190715e+12
7_seam_capital     CAG 2025-06-30               rwa 6.490132e+11 6.490130e+11 182309.419922 2.809025e-07      0.001    True  p3 EUR 6.49013e+11
7_seam_capital     GLE 2025-06-30              cet1 5.253584e+10 5.253600e+10 155006.620003 2.950493e-06      0.001    True   p3 EUR 5.2536e+10
7_seam_capital     GLE 2025-06-30 leverage_exposure 1.405566e+12 1.405566e+12 339582.389893 2.415984e-07      0.001    True p3 EUR 1.405566e+12
7_seam_capital     GLE 2025-06-30               rwa 3.880294e+11 3.880290e+11 411005.128967 1.059211e-06      0.001    True  p3 EUR 3.88029e+11
7_seam_capital     NDA 2025-06-30              cet1 2.396494e+10 2.396500e+10  55167.924599 2.302026e-06      0.001    True   p3 EUR 2.3965e+10
7_seam_capital     NDA 2025-06-30 leverage_exposure 5.613919e+11 5.613920e+11  53466.521973 9.523920e-08      0.001    True  p3 EUR 5.61392e+11
7_seam_capital     NDA 2025-06-30               rwa 1.585755e+11 1.585760e+11 475934.206024 3.001309e-06      0.001    True  p3 EUR 1.58576e+11
7_seam_capital    RABO 2025-06-30              cet1 4.602747e+10 4.602700e+10 469081.139999 1.019133e-05      0.001    True   p3 EUR 4.6027e+10
7_seam_capital    RABO 2025-06-30 leverage_exposure 6.746864e+11 6.746860e+11 441330.580078 6.541269e-07      0.001    True  p3 EUR 6.74686e+11
7_seam_capital    RABO 2025-06-30               rwa 2.315758e+11 2.315760e+11 160644.309998 6.937006e-07      0.001    True  p3 EUR 2.31576e+11
7_seam_capital    SWED 2025-06-30              cet1 1.570728e+10 1.570726e+10  13636.567490 8.681688e-07      0.001    True  p3 SEK 1.75081e+11
7_seam_capital    SWED 2025-06-30 leverage_exposure 2.560123e+11 2.560123e+11   8253.711792 3.223951e-08      0.001    True p3 SEK 2.853641e+12
7_seam_capital    SWED 2025-06-30               rwa 7.971472e+10 7.971471e+10  15456.869812 1.939023e-07      0.001    True   p3 SEK 8.8854e+11
```

#### seam 2 (check 8) at 2025-06-30, banks entered so far, sorted by |diff_rel| (value_a eba EUR, value_b report in EUR)

```
bank_id                         field       value_a       value_b     diff_abs     diff_rel  threshold  passed                     note
    BNP gains_derecognition_not_fvtpl -3.609968e+06  1.670000e+08 1.706100e+08 4.726080e+01        NaN    True no threshold; report EUR
    KBC           other_operating_net  7.917970e+07  1.563000e+09 1.483820e+09 1.873991e+01        NaN    True no threshold; report EUR
   INGA           other_operating_net -8.962000e+06  1.250000e+08 1.339620e+08 1.494778e+01        NaN    True no threshold; report EUR
    DNB           other_operating_net  2.446616e+07  1.938118e+08 1.693456e+08 6.921626e+00        NaN    True no threshold; report NOK
    NDA           other_operating_net  2.122900e+07  1.300000e+08 1.087710e+08 5.123700e+00        NaN    True no threshold; report EUR
   SWED        gains_held_for_trading -3.674553e+07  1.259905e+08 1.627360e+08 4.428731e+00        NaN    True no threshold; report SEK
    CAG           other_operating_net  1.270601e+09 -3.638000e+09 4.908601e+09 3.863212e+00        NaN    True no threshold; report EUR
    SEB        gains_held_for_trading  1.069246e+08  4.697157e+08 3.627911e+08 3.392961e+00        NaN    True no threshold; report SEK
 DANSKE           other_operating_net  3.390927e+07  1.380569e+08 1.041476e+08 3.071362e+00        NaN    True no threshold; report DKK
    DNB        gains_held_for_trading  3.956233e+07  1.468167e+08 1.072544e+08 2.711022e+00        NaN    True no threshold; report NOK
    CAG        gains_designated_fvtpl -1.404525e+09  2.293000e+09 3.697525e+09 2.632580e+00        NaN    True no threshold; report EUR
    KBC        resolution_dgs_contrib  1.793641e+08  5.660000e+08 3.866359e+08 2.155592e+00        NaN    True no threshold; report EUR
    KBC            impairments_nonfin  2.538184e+06  8.000000e+06 5.461816e+06 2.151860e+00        NaN    True no threshold; report EUR
    CAG gains_derecognition_not_fvtpl  3.729456e+08 -3.430000e+08 7.159456e+08 1.919705e+00        NaN    True no threshold; report EUR
    SHB        gains_held_for_trading -1.105219e+08  3.983391e+07 1.503559e+08 1.360416e+00        NaN    True no threshold; report SEK
    ABN           other_operating_net  4.903068e+07  1.140000e+08 6.496932e+07 1.325075e+00        NaN    True no threshold; report EUR
   RABO gains_derecognition_not_fvtpl  4.497332e+07 -7.000000e+06 5.197332e+07 1.155648e+00        NaN    True no threshold; report EUR
   SWED        resolution_dgs_contrib  6.806235e+07  1.447359e+08 7.667353e+07 1.126519e+00        NaN    True no threshold; report SEK
    SEB           other_operating_net  6.812394e+07 -2.883903e+06 7.100784e+07 1.042333e+00        NaN    True no threshold; report SEK
    ABN               impairments_fin  3.604281e+07 -1.000000e+06 3.704281e+07 1.027745e+00        NaN    True no threshold; report EUR
   SWED            impairments_nonfin  1.704571e+04  0.000000e+00 1.704571e+04 1.000000e+00        NaN    True no threshold; report SEK
    SEB        resolution_dgs_contrib  8.386577e+07  1.663652e+08 8.249939e+07 9.837076e-01        NaN    True no threshold; report SEK
   SWED               impairments_fin  3.985987e+07  8.110977e+05 3.904877e+07 9.796513e-01        NaN    True no threshold; report SEK
    NDA               impairments_fin  1.877929e+07  2.000000e+06 1.677929e+07 8.934997e-01        NaN    True no threshold; report EUR
   SWED           other_operating_net  1.212445e+08  2.282789e+08 1.070344e+08 8.827981e-01        NaN    True no threshold; report SEK
    BNP        gains_held_for_trading  3.616000e+09  6.797000e+09 3.181000e+09 8.797015e-01        NaN    True no threshold; report EUR
 DANSKE               impairments_fin  2.388016e+08  3.565353e+07 2.031480e+08 8.506981e-01        NaN    True no threshold; report DKK
   RABO                trading_assets  2.476672e+10  3.773000e+09 2.099372e+10 8.476584e-01        NaN    True no threshold; report EUR
    KBC               dividend_income  2.431761e+07  4.200000e+07 1.768239e+07 7.271435e-01        NaN    True no threshold; report EUR
    SHB           other_operating_net  9.109882e+06  1.514049e+07 6.030609e+06 6.619855e-01        NaN    True no threshold; report SEK
    ABN        gains_held_for_trading  3.052811e+08  1.110000e+08 1.942811e+08 6.364007e-01        NaN    True no threshold; report EUR
   RABO           other_operating_net  3.254081e+08  5.250000e+08 1.995919e+08 6.133588e-01        NaN    True no threshold; report EUR
    ABN                trading_assets  7.140887e+09  2.961000e+09 4.179887e+09 5.853457e-01        NaN    True no threshold; report EUR
    BNP           other_operating_net  2.116985e+09  3.349000e+09 1.232015e+09 5.819669e-01        NaN    True no threshold; report EUR
    KBC        gains_held_for_trading  1.431433e+08  6.200000e+07 8.114326e+07 5.668675e-01        NaN    True no threshold; report EUR
   RABO        gains_held_for_trading  2.906590e+08  4.350000e+08 1.443410e+08 4.965992e-01        NaN    True no threshold; report EUR
    CAG               dividend_income  1.675043e+08  2.450000e+08 7.749572e+07 4.626492e-01        NaN    True no threshold; report EUR
    GLE gains_derecognition_not_fvtpl  2.935694e+08  1.650000e+08 1.285694e+08 4.379522e-01        NaN    True no threshold; report EUR
   INGA              interest_expense  3.300594e+10  1.855300e+10 1.445294e+10 4.378891e-01        NaN    True no threshold; report EUR
    GLE           other_operating_net  2.086930e+09  1.205000e+09 8.819304e+08 4.225969e-01        NaN    True no threshold; report EUR
    KBC        total_operating_income  4.256054e+09  5.955000e+09 1.698946e+09 3.991833e-01        NaN    True no threshold; report EUR
   INGA               interest_income  4.011180e+10  2.571200e+10 1.439980e+10 3.589917e-01        NaN    True no threshold; report EUR
    CAG        gains_held_for_trading  3.595140e+09  4.845000e+09 1.249860e+09 3.476528e-01        NaN    True no threshold; report EUR
    CAG                  depreciation  1.528801e+09  1.020000e+09 5.088011e+08 3.328105e-01        NaN    True no threshold; report EUR
    SHB               impairments_fin -1.909033e+07 -2.460330e+07 5.512969e+06 2.887833e-01        NaN    True no threshold; report SEK
    CAG                      net_fees  8.882527e+09  6.398000e+09 2.484527e+09 2.797094e-01        NaN    True no threshold; report EUR
    SHB        resolution_dgs_contrib  1.651768e+08  1.214844e+08 4.369237e+07 2.645188e-01        NaN    True no threshold; report SEK
 DANSKE        gains_held_for_trading  1.857398e+08  2.326862e+08 4.694643e+07 2.527538e-01        NaN    True no threshold; report DKK
   SWED              interest_expense  2.520164e+09  1.919958e+09 6.002058e+08 2.381614e-01        NaN    True no threshold; report SEK
 DANSKE              interest_expense  3.536313e+09  2.728568e+09 8.077457e+08 2.284146e-01        NaN    True no threshold; report DKK
    GLE                       cash_cb  1.922134e+11  1.487820e+11 4.343144e+10 2.259542e-01        NaN    True no threshold; report EUR
   INGA        gains_held_for_trading  1.512130e+09  1.839000e+09 3.268700e+08 2.161653e-01        NaN    True no threshold; report EUR
   INGA                    provisions  1.233880e+08  1.500000e+08 2.661200e+07 2.156774e-01        NaN    True no threshold; report EUR
    BNP            deposits_customers  1.297581e+12  1.024734e+12 2.728469e+11 2.102735e-01        NaN    True no threshold; report EUR
    CAG             total_liabilities  2.036653e+12  2.461797e+12 4.251437e+11 2.087463e-01        NaN    True no threshold; report EUR
    CAG                  total_assets  2.187749e+12  2.614010e+12 4.262609e+11 1.948399e-01       0.02   False               report EUR
    KBC                           pbt  1.697203e+09  2.022000e+09 3.247967e+08 1.913717e-01        NaN    True no threshold; report EUR
    GLE            deposits_customers  6.320626e+11  5.183970e+11 1.136656e+11 1.798328e-01        NaN    True no threshold; report EUR
   RABO               impairments_fin  1.655401e+08  1.360000e+08 2.954014e+07 1.784470e-01        NaN    True no threshold; report EUR
 DANSKE             total_liabilities  4.060071e+11  4.780740e+11 7.206686e+10 1.775015e-01        NaN    True no threshold; report DKK
    SHB                      net_fees  4.415778e+08  5.196433e+08 7.806550e+07 1.767877e-01        NaN    True no threshold; report SEK
    GLE                      net_fees  3.142583e+09  2.594000e+09 5.485830e+08 1.745644e-01        NaN    True no threshold; report EUR
    NDA             total_liabilities  5.165589e+11  6.064410e+11 8.988213e+10 1.740017e-01        NaN    True no threshold; report EUR
    KBC                 profit_owners  1.334524e+09  1.564000e+09 2.294758e+08 1.719533e-01        NaN    True no threshold; report EUR
    KBC                           pat  1.334656e+09  1.564000e+09 2.293437e+08 1.718373e-01        NaN    True no threshold; report EUR
 DANSKE                  total_assets  4.291889e+11  5.012307e+11 7.204178e+10 1.678556e-01        NaN    True no threshold; report DKK
   SWED             total_liabilities  2.246680e+11  2.623012e+11 3.763321e+10 1.675059e-01        NaN    True no threshold; report SEK
    NDA                  total_assets  5.469076e+11  6.368080e+11 8.990041e+10 1.643795e-01        NaN    True no threshold; report EUR
    GLE        gains_held_for_trading  4.145146e+09  4.818000e+09 6.728541e+08 1.623234e-01        NaN    True no threshold; report EUR
   SWED               interest_income  4.693603e+09  3.939231e+09 7.543719e+08 1.607234e-01        NaN    True no threshold; report SEK
   SWED                  total_assets  2.433942e+11  2.810247e+11 3.763053e+10 1.546073e-01        NaN    True no threshold; report SEK
    SEB             total_liabilities  3.063817e+11  3.493384e+11 4.295673e+10 1.402066e-01        NaN    True no threshold; report SEK
   SWED                admin_expenses  1.166686e+09  1.007383e+09 1.593022e+08 1.365426e-01        NaN    True no threshold; report SEK
 DANSKE               interest_income  5.960038e+09  5.152338e+09 8.077004e+08 1.355193e-01        NaN    True no threshold; report DKK
    DNB               impairments_fin  1.077933e+08  9.321832e+07 1.457498e+07 1.352123e-01        NaN    True no threshold; report NOK
    SEB                  total_assets  3.258115e+11  3.687682e+11 4.295671e+10 1.318453e-01        NaN    True no threshold; report SEK
    GLE             total_liabilities  1.304225e+12  1.474030e+12 1.698052e+11 1.301963e-01        NaN    True no threshold; report EUR
    CAG                admin_expenses  1.239419e+10  1.084400e+10 1.550188e+09 1.250738e-01        NaN    True no threshold; report EUR
    NDA        gains_held_for_trading  4.826859e+08  5.430000e+08 6.031406e+07 1.249551e-01        NaN    True no threshold; report EUR
    GLE                  total_assets  1.380480e+12  1.551491e+12 1.710110e+11 1.238779e-01        NaN    True no threshold; report EUR
   RABO                 profit_owners  2.659510e+09  2.334000e+09 3.255100e+08 1.223947e-01        NaN    True no threshold; report EUR
    DNB             total_liabilities  2.690176e+11  3.007447e+11 3.172709e+10 1.179369e-01        NaN    True no threshold; report NOK
    SEB                      net_fees  1.083625e+09  1.206733e+09 1.231077e+08 1.136073e-01        NaN    True no threshold; report SEK
    BNP             total_liabilities  2.442546e+12  2.717736e+12 2.751902e+11 1.126653e-01        NaN    True no threshold; report EUR
    NDA                      net_fees  1.425609e+09  1.585000e+09 1.593908e+08 1.118054e-01        NaN    True no threshold; report EUR
    DNB                  total_assets  2.926278e+11  3.241186e+11 3.149079e+10 1.076138e-01        NaN    True no threshold; report NOK
    BNP                  total_assets  2.573934e+12  2.849376e+12 2.754421e+11 1.070121e-01        NaN    True no threshold; report EUR
    SEB                       cash_cb  4.828169e+10  4.314592e+10 5.135772e+09 1.063710e-01        NaN    True no threshold; report SEK
    BNP                      net_fees  5.967017e+09  5.349000e+09 6.180172e+08 1.035722e-01        NaN    True no threshold; report EUR
    CAG               impairments_fin  1.751049e+09  1.575000e+09 1.760493e+08 1.005393e-01        NaN    True no threshold; report EUR
    KBC             total_liabilities  3.316397e+11  3.644400e+11 3.280027e+10 9.890333e-02        NaN    True no threshold; report EUR
    CAG            deposits_customers  1.294336e+12  1.167898e+12 1.264379e+11 9.768552e-02        NaN    True no threshold; report EUR
    KBC                  total_assets  3.565054e+11  3.906690e+11 3.416355e+10 9.582898e-02        NaN    True no threshold; report EUR
    SEB              interest_expense  4.010133e+09  3.647867e+09 3.622656e+08 9.033756e-02        NaN    True no threshold; report SEK
    SHB             total_liabilities  2.860223e+11  3.115075e+11 2.548513e+10 8.910189e-02        NaN    True no threshold; report SEK
    SHB                  total_assets  3.025829e+11  3.284230e+11 2.584008e+10 8.539833e-02        NaN    True no threshold; report SEK
    DNB                  depreciation  1.740762e+08  1.593373e+08 1.473896e+07 8.466956e-02        NaN    True no threshold; report NOK
    SHB                 profit_owners  9.889273e+08  1.064250e+09 7.532306e+07 7.616643e-02        NaN    True no threshold; report SEK
    SHB                           pat  9.946130e+08  1.070289e+09 7.567552e+07 7.608540e-02        NaN    True no threshold; report SEK
    BNP               impairments_fin  1.535170e+09  1.650000e+09 1.148305e+08 7.479986e-02        NaN    True no threshold; report EUR
   INGA               impairments_fin  6.573060e+08  6.120000e+08 4.530600e+07 6.892680e-02        NaN    True no threshold; report EUR
    CAG               interest_income  2.936989e+10  3.136300e+10 1.993108e+09 6.786228e-02        NaN    True no threshold; report EUR
   RABO              interest_expense  7.074570e+09  6.615000e+09 4.595699e+08 6.496083e-02        NaN    True no threshold; report EUR
   RABO                  depreciation  1.548322e+08  1.450000e+08 9.832244e+06 6.350256e-02        NaN    True no threshold; report EUR
    CAG        total_operating_income  2.118275e+10  1.985600e+10 1.326752e+09 6.263362e-02        NaN    True no threshold; report EUR
    SEB               interest_income  5.891588e+09  5.523485e+09 3.681028e+08 6.247938e-02        NaN    True no threshold; report SEK
    SHB                           pbt  1.299384e+09  1.378866e+09 7.948262e+07 6.116948e-02        NaN    True no threshold; report SEK
    CAG                       cash_cb  1.825775e+11  1.720850e+11 1.049250e+10 5.746875e-02        NaN    True no threshold; report EUR
    KBC                  total_equity  2.486572e+10  2.622900e+10 1.363279e+09 5.482562e-02        NaN    True no threshold; report EUR
    ABN            deposits_customers  2.833446e+11  2.683230e+11 1.502156e+10 5.301518e-02        NaN    True no threshold; report EUR
    NDA        resolution_dgs_contrib  7.708224e+07  7.300000e+07 4.082240e+06 5.295954e-02        NaN    True no threshold; report EUR
    BNP                       cash_cb  2.080043e+11  1.974190e+11 1.058528e+10 5.088971e-02        NaN    True no threshold; report EUR
    CAG                           pbt  6.666819e+09  7.004000e+09 3.371811e+08 5.057601e-02        NaN    True no threshold; report EUR
   INGA                       cash_cb  7.950929e+10  7.556500e+10 3.944293e+09 4.960795e-02        NaN    True no threshold; report EUR
    ABN                       cash_cb  4.923372e+10  4.681100e+10 2.422719e+09 4.920852e-02        NaN    True no threshold; report EUR
    DNB                           pbt  2.188099e+09  2.290152e+09 1.020534e+08 4.664020e-02        NaN    True no threshold; report NOK
    NDA        total_operating_income  5.627151e+09  5.885000e+09 2.578489e+08 4.582228e-02        NaN    True no threshold; report EUR
   INGA            deposits_customers  7.734177e+11  7.380790e+11 3.533874e+10 4.569167e-02        NaN    True no threshold; report EUR
    NDA                admin_expenses  2.216054e+09  2.314000e+09 9.794576e+07 4.419827e-02        NaN    True no threshold; report EUR
    DNB                           pat  1.755016e+09  1.832122e+09 7.710597e+07 4.393463e-02        NaN    True no threshold; report NOK
    KBC                admin_expenses  2.124480e+09  2.035000e+09 8.948010e+07 4.211859e-02        NaN    True no threshold; report EUR
    GLE               at1_instruments  8.896372e+09  8.524000e+09 3.723716e+08 4.185657e-02        NaN    True no threshold; report EUR
    GLE                           pbt  4.353937e+09  4.524000e+09 1.700627e+08 3.905951e-02        NaN    True no threshold; report EUR
    ABN              interest_expense  4.305666e+09  4.141000e+09 1.646660e+08 3.824404e-02        NaN    True no threshold; report EUR
   SWED                      net_fees  6.908508e+08  7.168301e+08 2.597938e+07 3.760491e-02        NaN    True no threshold; report SEK
    KBC                  depreciation  1.908367e+08  1.980000e+08 7.163285e+06 3.753620e-02        NaN    True no threshold; report EUR
    SHB        total_operating_income  2.469968e+09  2.560636e+09 9.066775e+07 3.670807e-02        NaN    True no threshold; report SEK
    GLE               interest_income  2.210313e+10  2.290900e+10 8.058713e+08 3.645960e-02        NaN    True no threshold; report EUR
    SHB                  depreciation  8.919570e+07  9.237502e+07 3.179322e+06 3.564435e-02        NaN    True no threshold; report SEK
    SEB               impairments_fin  8.345891e+07  8.642697e+07 2.968058e+06 3.556310e-02        NaN    True no threshold; report SEK
   RABO               interest_income  1.293989e+10  1.248700e+10 4.528851e+08 3.499916e-02        NaN    True no threshold; report EUR
    BNP                admin_expenses  1.402934e+10  1.451700e+10 4.876589e+08 3.475993e-02        NaN    True no threshold; report EUR
    SEB                  depreciation  1.039170e+08  1.075155e+08 3.598531e+06 3.462891e-02        NaN    True no threshold; report SEK
   INGA                admin_expenses  5.577254e+09  5.756000e+09 1.787460e+08 3.204911e-02        NaN    True no threshold; report EUR
    KBC               impairments_fin  1.502970e+08  1.550000e+08 4.702961e+06 3.129111e-02        NaN    True no threshold; report EUR
    GLE        total_operating_income  1.345502e+10  1.387400e+10 4.189841e+08 3.113962e-02        NaN    True no threshold; report EUR
 DANSKE            deposits_customers  1.583335e+11  1.629994e+11 4.665831e+09 2.946837e-02        NaN    True no threshold; report DKK
 DANSKE                       cash_cb  2.219819e+10  2.154485e+10 6.533328e+08 2.943181e-02        NaN    True no threshold; report DKK
    SHB                admin_expenses  9.660963e+08  9.929639e+08 2.686751e+07 2.781038e-02        NaN    True no threshold; report SEK
   RABO            deposits_customers  4.115790e+11  4.223910e+11 1.081199e+10 2.626953e-02        NaN    True no threshold; report EUR
    KBC            deposits_customers  2.429599e+11  2.366260e+11 6.333948e+09 2.606993e-02        NaN    True no threshold; report EUR
    BNP        total_operating_income  2.490607e+10  2.554100e+10 6.349328e+08 2.549310e-02        NaN    True no threshold; report EUR
 DANSKE        total_operating_income  3.655121e+09  3.741879e+09 8.675786e+07 2.373598e-02        NaN    True no threshold; report DKK
    SHB              interest_expense  4.301442e+09  4.205181e+09 9.626127e+07 2.237883e-02        NaN    True no threshold; report SEK
    NDA            deposits_customers  2.425217e+11  2.372060e+11 5.315658e+09 2.191828e-02        NaN    True no threshold; report EUR
    SHB                  total_equity  1.656059e+10  1.691544e+10 3.548559e+08 2.142773e-02        NaN    True no threshold; report SEK
    SEB        total_operating_income  3.474778e+09  3.549093e+09 7.431482e+07 2.138692e-02        NaN    True no threshold; report SEK
   SWED        total_operating_income  3.026413e+09  3.090372e+09 6.395939e+07 2.113373e-02        NaN    True no threshold; report SEK
    DNB            deposits_customers  1.339311e+11  1.311932e+11 2.737880e+09 2.044245e-02        NaN    True no threshold; report NOK
   SWED            deposits_customers  1.211592e+11  1.188620e+11 2.297239e+09 1.896050e-02        NaN    True no threshold; report SEK
    SEB                admin_expenses  1.379816e+09  1.354623e+09 2.519223e+07 1.825768e-02        NaN    True no threshold; report SEK
   RABO        total_operating_income  7.893829e+09  8.035000e+09 1.411707e+08 1.788368e-02        NaN    True no threshold; report EUR
    NDA                  depreciation  2.947786e+08  3.000000e+08 5.221403e+06 1.771296e-02        NaN    True no threshold; report EUR
    BNP                           pbt  8.648672e+09  8.797000e+09 1.483275e+08 1.715032e-02        NaN    True no threshold; report EUR
    NDA                       cash_cb  4.162254e+10  4.090900e+10 7.135381e+08 1.714307e-02        NaN    True no threshold; report EUR
   RABO                       cash_cb  6.964840e+10  6.845600e+10 1.192401e+09 1.712029e-02        NaN    True no threshold; report EUR
    KBC              interest_expense  6.006013e+09  5.909000e+09 9.701307e+07 1.615266e-02        NaN    True no threshold; report EUR
    GLE                  total_equity  7.625526e+10  7.746100e+10 1.205742e+09 1.581192e-02        NaN    True no threshold; report EUR
    GLE               impairments_fin  6.885823e+08  6.990000e+08 1.041774e+07 1.512925e-02        NaN    True no threshold; report EUR
   SWED                           pbt  1.814818e+09  1.842183e+09 2.736524e+07 1.507878e-02        NaN    True no threshold; report SEK
    KBC               interest_income  8.711568e+09  8.839000e+09 1.274320e+08 1.462791e-02        NaN    True no threshold; report EUR
    DNB               interest_income  8.207494e+09  8.091298e+09 1.161958e+08 1.415728e-02        NaN    True no threshold; report NOK
    NDA                           pbt  3.162665e+09  3.206000e+09 4.333520e+07 1.370212e-02        NaN    True no threshold; report EUR
    GLE                admin_expenses  8.278665e+09  8.167000e+09 1.116651e+08 1.348830e-02        NaN    True no threshold; report EUR
    BNP              interest_expense  2.704164e+10  2.669400e+10 3.476432e+08 1.285585e-02        NaN    True no threshold; report EUR
    BNP                  depreciation  1.130498e+09  1.145000e+09 1.450233e+07 1.282827e-02        NaN    True no threshold; report EUR
    BNP               at1_instruments  1.691444e+10  1.670600e+10 2.084417e+08 1.232330e-02        NaN    True no threshold; report EUR
    NDA                 profit_owners  2.459132e+09  2.429000e+09 3.013165e+07 1.225296e-02        NaN    True no threshold; report EUR
    GLE                           pat  3.514048e+09  3.557000e+09 4.295200e+07 1.222294e-02        NaN    True no threshold; report EUR
 DANSKE                trading_assets  7.089604e+10  7.005321e+10 8.428303e+08 1.188826e-02        NaN    True no threshold; report DKK
    BNP               interest_income  3.700518e+10  3.657300e+10 4.321847e+08 1.167903e-02        NaN    True no threshold; report EUR
 DANSKE                           pbt  1.985131e+09  2.007857e+09 2.272576e+07 1.144799e-02        NaN    True no threshold; report DKK
    DNB                       cash_cb  3.711572e+10  3.672466e+10 3.910637e+08 1.053633e-02        NaN    True no threshold; report NOK
    SHB            deposits_customers  1.281195e+11  1.267782e+11 1.341292e+09 1.046907e-02        NaN    True no threshold; report SEK
    SHB               dividend_income  1.783960e+05  1.802439e+05 1.847898e+03 1.035840e-02        NaN    True no threshold; report SEK
    DNB                  total_equity  2.361017e+10  2.337386e+10 2.363016e+08 1.000847e-02        NaN    True no threshold; report NOK
   RABO               at1_instruments  4.899677e+09  4.948000e+09 4.832306e+07 9.862498e-03        NaN    True no threshold; report EUR
    KBC                      net_fees  1.370212e+09  1.357000e+09 1.321225e+07 9.642483e-03        NaN    True no threshold; report EUR
    DNB        total_operating_income  3.771589e+09  3.807887e+09 3.629768e+07 9.623976e-03        NaN    True no threshold; report NOK
    SHB               interest_income  6.248918e+09  6.191109e+09 5.780895e+07 9.251034e-03        NaN    True no threshold; report SEK
    ABN                admin_expenses  2.523776e+09  2.547000e+09 2.322379e+07 9.201999e-03        NaN    True no threshold; report EUR
    SEB                           pbt  1.817702e+09  1.834252e+09 1.655009e+07 9.104950e-03        NaN    True no threshold; report SEK
    GLE                  depreciation  7.748422e+08  7.680000e+08 6.842237e+06 8.830490e-03        NaN    True no threshold; report EUR
    GLE              interest_expense  1.766593e+10  1.781700e+10 1.510689e+08 8.551428e-03        NaN    True no threshold; report EUR
    DNB                admin_expenses  1.256818e+09  1.266980e+09 1.016178e+07 8.085323e-03        NaN    True no threshold; report NOK
    CAG                  total_equity  1.510958e+11  1.522130e+11 1.117151e+09 7.393655e-03        NaN    True no threshold; report EUR
   RABO        resolution_dgs_contrib  2.920980e+07  2.900000e+07 2.097950e+05 7.182351e-03        NaN    True no threshold; report EUR
    DNB              interest_expense  5.336637e+09  5.298951e+09 3.768607e+07 7.061763e-03        NaN    True no threshold; report NOK
    SEB            deposits_customers  1.782612e+11  1.771053e+11 1.155959e+09 6.484636e-03        NaN    True no threshold; report SEK
   SWED                       cash_cb  2.932872e+10  2.915893e+10 1.697888e+08 5.789166e-03        NaN    True no threshold; report SEK
   INGA        total_operating_income  1.127898e+10  1.133900e+10 6.001500e+07 5.320958e-03        NaN    True no threshold; report EUR
    ABN gains_derecognition_not_fvtpl -2.714019e+07 -2.700000e+07 1.401930e+05 5.165512e-03        NaN    True no threshold; report EUR
    ABN               interest_income  7.198655e+09  7.233000e+09 3.434496e+07 4.771025e-03        NaN    True no threshold; report EUR
   SWED                 profit_owners  1.443297e+09  1.449972e+09 6.675179e+06 4.624951e-03        NaN    True no threshold; report SEK
   SWED                           pat  1.442684e+09  1.449342e+09 6.657971e+06 4.614991e-03        NaN    True no threshold; report SEK
    SEB                           pat  1.442374e+09  1.448891e+09 6.517097e+06 4.518313e-03        NaN    True no threshold; report SEK
    SEB                 profit_owners  1.442374e+09  1.448891e+09 6.517097e+06 4.518313e-03        NaN    True no threshold; report SEK
   INGA                  depreciation  3.301970e+08  3.290000e+08 1.197000e+06 3.625109e-03        NaN    True no threshold; report EUR
    SHB                       cash_cb  5.538848e+10  5.521096e+10 1.775169e+08 3.204943e-03        NaN    True no threshold; report SEK
   SWED                  depreciation  9.493859e+07  9.516880e+07 2.302086e+05 2.424816e-03        NaN    True no threshold; report SEK
    CAG                trading_assets  3.530318e+11  3.522570e+11 7.747624e+08 2.194597e-03        NaN    True no threshold; report EUR
    ABN                  depreciation  7.883542e+07  7.900000e+07 1.645800e+05 2.087640e-03        NaN    True no threshold; report EUR
    BNP                  total_equity  1.313882e+11  1.316400e+11 2.518339e+08 1.916717e-03        NaN    True no threshold; report EUR
    NDA               interest_income  9.014674e+09  8.999000e+09 1.567384e+07 1.738703e-03        NaN    True no threshold; report EUR
    NDA                           pat  2.459132e+09  2.455000e+09 4.131650e+06 1.680126e-03        NaN    True no threshold; report EUR
    DNB                 profit_owners  1.753667e+09  1.756569e+09 2.902195e+06 1.654930e-03        NaN    True no threshold; report NOK
    BNP                           pat  6.498768e+09  6.509000e+09 1.023165e+07 1.574398e-03        NaN    True no threshold; report EUR
    NDA              interest_expense  5.380102e+09  5.372000e+09 8.101817e+06 1.505885e-03        NaN    True no threshold; report EUR
    ABN        total_operating_income  4.293763e+09  4.288000e+09 5.762614e+06 1.342090e-03        NaN    True no threshold; report EUR
    ABN               at1_instruments  4.220363e+09  4.225000e+09 4.637121e+06 1.098749e-03        NaN    True no threshold; report EUR
 DANSKE                  total_equity  2.318181e+10  2.315686e+10 2.494870e+07 1.076219e-03        NaN    True no threshold; report DKK
    ABN         intangibles_deduction  2.872920e+08  2.870000e+08 2.920110e+05 1.016426e-03        NaN    True no threshold; report EUR
    ABN             total_liabilities  3.868094e+11  3.864360e+11 3.734398e+08 9.654360e-04        NaN    True no threshold; report EUR
    ABN                  total_assets  4.142951e+11  4.139220e+11 3.731215e+08 9.006177e-04        NaN    True no threshold; report EUR
 DANSKE                           pat  1.501455e+09  1.502676e+09 1.220398e+06 8.128097e-04        NaN    True no threshold; report DKK
    KBC                       cash_cb  3.600982e+10  3.603900e+10 2.918269e+07 8.104092e-04        NaN    True no threshold; report EUR
    ABN                           pbt  1.661985e+09  1.663000e+09 1.014633e+06 6.104945e-04        NaN    True no threshold; report EUR
    NDA                  total_equity  3.034872e+10  3.036700e+10 1.828324e+07 6.024387e-04        NaN    True no threshold; report EUR
   RABO                admin_expenses  3.989217e+09  3.987000e+09 2.216619e+06 5.556527e-04        NaN    True no threshold; report EUR
   RABO         intangibles_deduction  6.103314e+08  6.100000e+08 3.314204e+05 5.430172e-04        NaN    True no threshold; report EUR
   RABO                     npl_gross  9.183989e+09  9.180000e+09 3.988516e+06 4.342902e-04        NaN    True no threshold; report EUR
    KBC                trading_assets  1.052856e+10  1.053300e+10 4.441578e+06 4.218600e-04        NaN    True no threshold; report EUR
   RABO                      net_fees  1.209518e+09  1.210000e+09 4.815290e+05 3.981163e-04        NaN    True no threshold; report EUR
    ABN                 npl_allowance  9.413665e+08  9.410000e+08 3.665490e+05 3.893797e-04        NaN    True no threshold; report EUR
   RABO                 npl_allowance  1.540353e+09  1.540000e+09 3.534830e+05 2.294817e-04        NaN    True no threshold; report EUR
    DNB                      net_fees  6.747561e+08  6.749109e+08 1.548381e+05 2.294726e-04        NaN    True no threshold; report NOK
    ABN                      net_fees  9.992044e+08  9.990000e+08 2.044050e+05 2.045678e-04        NaN    True no threshold; report EUR
    CAG                           pat  5.346940e+09  5.348000e+09 1.060075e+06 1.982582e-04        NaN    True no threshold; report EUR
    NDA     loans_customers_allowance  1.506260e+09  1.506000e+09 2.598871e+05 1.725380e-04        NaN    True no threshold; report EUR
    NDA               at1_instruments  2.983492e+09  2.984000e+09 5.077635e+05 1.701910e-04        NaN    True no threshold; report EUR
    NDA         intangibles_deduction  2.739534e+09  2.740000e+09 4.657501e+05 1.700107e-04        NaN    True no threshold; report EUR
   SWED                  total_equity  1.872623e+10  1.872355e+10 2.681021e+06 1.431693e-04        NaN    True no threshold; report SEK
   INGA                 profit_owners  3.129602e+09  3.130000e+09 3.980000e+05 1.271727e-04        NaN    True no threshold; report EUR
    ABN                           pat  1.225144e+09  1.225000e+09 1.441350e+05 1.176474e-04        NaN    True no threshold; report EUR
   INGA                           pat  3.256378e+09  3.256000e+09 3.780000e+05 1.160799e-04        NaN    True no threshold; report EUR
    CAG                 profit_owners  4.802450e+09  4.803000e+09 5.497149e+05 1.144655e-04        NaN    True no threshold; report EUR
   RABO                           pbt  3.737594e+09  3.738000e+09 4.062720e+05 1.086988e-04        NaN    True no threshold; report EUR
   SWED                 npl_allowance  3.378024e+08  3.377742e+08 2.825999e+04 8.365834e-05        NaN    True no threshold; report SEK
   RABO     loans_customers_allowance  2.285185e+09  2.285000e+09 1.845380e+05 8.075409e-05        NaN    True no threshold; report EUR
    BNP                 profit_owners  6.208502e+09  6.209000e+09 4.981800e+05 8.024158e-05        NaN    True no threshold; report EUR
    GLE                 profit_owners  3.060769e+09  3.061000e+09 2.309649e+05 7.545975e-05        NaN    True no threshold; report EUR
    ABN                     npl_gross  5.567388e+09  5.567000e+09 3.875230e+05 6.960590e-05        NaN    True no threshold; report EUR
   INGA                      net_fees  2.215848e+09  2.216000e+09 1.520000e+05 6.859676e-05        NaN    True no threshold; report EUR
    GLE                 npl_allowance  6.156411e+09  6.156000e+09 4.112781e+05 6.680485e-05        NaN    True no threshold; report EUR
    BNP         intangibles_deduction  7.535497e+09  7.535000e+09 4.965400e+05 6.589347e-05        NaN    True no threshold; report EUR
    NDA                     npl_gross  3.666768e+09  3.667000e+09 2.321943e+05 6.332397e-05        NaN    True no threshold; report EUR
   SWED                     npl_gross  1.160160e+09  1.160095e+09 6.513255e+04 5.614100e-05        NaN    True no threshold; report SEK
    CAG     loans_customers_allowance  2.167881e+10  2.168000e+10 1.194504e+06 5.510006e-05        NaN    True no threshold; report EUR
    NDA                 npl_allowance  1.042056e+09  1.042000e+09 5.631355e+04 5.404079e-05        NaN    True no threshold; report EUR
    ABN                 profit_owners  1.224941e+09  1.225000e+09 5.856200e+04 4.780800e-05        NaN    True no threshold; report EUR
   RABO                           pat  2.693893e+09  2.694000e+09 1.067970e+05 3.964411e-05        NaN    True no threshold; report EUR
    GLE         intangibles_deduction  7.095270e+09  7.095000e+09 2.699746e+05 3.804994e-05        NaN    True no threshold; report EUR
    BNP                 npl_allowance  1.303349e+10  1.303300e+10 4.899810e+05 3.759400e-05        NaN    True no threshold; report EUR
    GLE     loans_customers_allowance  8.705682e+09  8.706000e+09 3.180925e+05 3.653850e-05        NaN    True no threshold; report EUR
 DANSKE                      net_fees  9.471300e+08  9.470972e+08 3.280209e+04 3.463314e-05        NaN    True no threshold; report DKK
    BNP     loans_customers_allowance  1.661053e+10  1.661100e+10 4.737710e+05 2.852234e-05        NaN    True no threshold; report EUR
    CAG                 npl_allowance  1.291530e+10  1.291500e+10 3.028850e+05 2.345163e-05        NaN    True no threshold; report EUR
   SWED               at1_instruments  1.401995e+09  1.401965e+09 3.005428e+04 2.143680e-05        NaN    True no threshold; report SEK
   SWED         intangibles_deduction  1.660821e+09  1.660790e+09 3.032342e+04 1.825809e-05        NaN    True no threshold; report SEK
    BNP                     npl_gross  2.687041e+10  2.687000e+10 4.132200e+05 1.537825e-05        NaN    True no threshold; report EUR
    CAG              interest_expense  2.130729e+10  2.130700e+10 2.870709e+05 1.347290e-05        NaN    True no threshold; report EUR
    ABN                  total_equity  2.748568e+10  2.748600e+10 3.182300e+05 1.157803e-05        NaN    True no threshold; report EUR
    CAG                     npl_gross  2.643175e+10  2.643200e+10 2.508067e+05 9.488840e-06        NaN    True no threshold; report EUR
    GLE                     npl_gross  1.400687e+10  1.400700e+10 1.313767e+05 9.379448e-06        NaN    True no threshold; report EUR
   INGA                           pbt  4.493034e+09  4.493000e+09 3.400000e+04 7.567270e-06        NaN    True no threshold; report EUR
   RABO                     loans_all  5.074487e+11  5.074450e+11 3.714918e+06 7.320775e-06        NaN    True no threshold; report EUR
    ABN         loans_customers_gross  2.907298e+11  2.907280e+11 1.786733e+06 6.145683e-06        NaN    True no threshold; report EUR
   RABO                  total_equity  5.476127e+10  5.476100e+10 2.717620e+05 4.962668e-06        NaN    True no threshold; report EUR
    ABN        loans_households_gross  1.717758e+11  1.717750e+11 8.271010e+05 4.815002e-06        NaN    True no threshold; report EUR
    GLE               debt_securities  9.035834e+10  9.035800e+10 3.431136e+05 3.797254e-06        NaN    True no threshold; report EUR
    CAG               debt_securities  1.758304e+11  1.758310e+11 6.438480e+05 3.661757e-06        NaN    True no threshold; report EUR
   RABO         loans_customers_gross  4.768233e+11  4.768220e+11 1.348917e+06 2.828966e-06        NaN    True no threshold; report EUR
    BNP               debt_securities  2.375784e+11  2.375790e+11 5.857360e+05 2.465443e-06        NaN    True no threshold; report EUR
    ABN                     loans_all  3.105067e+11  3.105060e+11 7.093510e+05 2.284495e-06        NaN    True no threshold; report EUR
    NDA                     loans_all  3.431383e+11  3.431390e+11 6.691014e+05 1.949947e-06        NaN    True no threshold; report EUR
    GLE         loans_customers_gross  4.731353e+11  4.731360e+11 6.679978e+05 1.411854e-06        NaN    True no threshold; report EUR
    SEB                  total_equity  1.942980e+10  1.942978e+10 2.378747e+04 1.224277e-06        NaN    True no threshold; report SEK
    NDA         loans_customers_gross  3.382034e+11  3.382030e+11 4.108329e+05 1.214751e-06        NaN    True no threshold; report EUR
    GLE        loans_households_gross  1.812548e+11  1.812550e+11 1.764438e+05 9.734573e-07        NaN    True no threshold; report EUR
   INGA                  total_equity  5.014605e+10  5.014600e+10 4.700000e+04 9.372623e-07        NaN    True no threshold; report EUR
    BNP         loans_customers_gross  9.233787e+11  9.233780e+11 6.629890e+05 7.180034e-07        NaN    True no threshold; report EUR
   SWED                     loans_all  1.695585e+11  1.695584e+11 8.540797e+04 5.037080e-07        NaN    True no threshold; report SEK
    GLE                     loans_all  5.065102e+11  5.065100e+11 2.356225e+05 4.651880e-07        NaN    True no threshold; report EUR
   RABO        loans_households_gross  2.078971e+11  2.078970e+11 6.903200e+04 3.320489e-07        NaN    True no threshold; report EUR
   RABO                  total_assets  6.358652e+11  6.358650e+11 2.061730e+05 3.242401e-07        NaN    True no threshold; report EUR
   INGA             total_liabilities  1.036614e+12  1.036614e+12 2.910000e+05 2.807217e-07        NaN    True no threshold; report EUR
    CAG         loans_customers_gross  1.209189e+12  1.209189e+12 3.195124e+05 2.642370e-07        NaN    True no threshold; report EUR
    CAG                     loans_all  1.345533e+12  1.345533e+12 3.474908e+05 2.582552e-07        NaN    True no threshold; report EUR
    BNP        loans_households_gross  3.387801e+11  3.387800e+11 8.085700e+04 2.386711e-07        NaN    True no threshold; report EUR
   INGA                  total_assets  1.086760e+12  1.086760e+12 2.440000e+05 2.245206e-07        NaN    True no threshold; report EUR
   SWED        loans_households_gross  1.062151e+11  1.062150e+11 1.309828e+04 1.233185e-07        NaN    True no threshold; report SEK
   RABO             total_liabilities  5.811039e+11  5.811040e+11 6.558000e+04 1.128542e-07        NaN    True no threshold; report EUR
    NDA        loans_households_gross  1.936110e+11  1.936110e+11 1.410475e+04 7.285097e-08        NaN    True no threshold; report EUR
    BNP                     loans_all  9.636181e+11  9.636180e+11 6.235000e+04 6.470406e-08        NaN    True no threshold; report EUR
    CAG        loans_households_gross  6.441880e+11  6.441880e+11 1.946470e+04 3.021587e-08        NaN    True no threshold; report EUR
```

#### CAG total_assets line (the instruction 02 B.3 gate)

```
    check bank_id   ref_date        field      value_a      value_b     diff_abs  diff_rel  threshold  passed       note
8_seam_pl     CAG 2025-06-30 total_assets 2.187749e+12 2.614010e+12 4.262609e+11   0.19484       0.02   False report EUR
```

#### checks 2 to 5 on entry rows: counts by check and passed

```
          check  passed  rows
2_balance_sheet    True    52
       3_income    True    39
         4_cet1    True    24
5_period_length    True   517
```

#### checks 2 to 5 on entry rows that failed

```
none
```

### Step 2.3: missing fields and judgement calls, per bank

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

The committed suite, run in the fresh clone below: `ruff check .` clean, and `pytest -p socket --disable-socket -q` gives 20 passed. That is the 17 Section 1 tests plus `test_family_from_source_map`, `test_component_sum` and `test_scale_and_sign`. The step 2.4 test `test_provenance_styles` is written but not committed, because step 2.4 was not reached; it passed locally with the rest of the suite (21 passed before the stop).

## Fresh-clone check

Clone path `C:\Users\astha\AppData\Local\Temp\claude\...\scratchpad\fc2` (Windows; no Linux machine was available), at 92cda21:

```
$ git clone https://github.com/uty101/Bank-Performance-Benchmarking.git fc2
$ git log --oneline -1
92cda21 step 2.1: provenance reads ASCII digits only; provenance on mergers.csv rows
$ uv venv --python 3.12
$ uv pip install -r requirements-lock.txt
$ uv pip install -e . --no-deps
$ ruff check .
All checks passed!
$ pytest -p socket --disable-socket -q
....................                                                     [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\_pytest\config\__init__.py:894
  C:\Users\astha\AppData\Local\Temp\claude\c--Utkarsh-10--Quant-Projects-15--Bank-Benchmarking-Project\747fb65d-5706-4676-9116-d74cc77dfa3f\scratchpad\fc2\.venv\Lib\site-packages\_pytest\config\__init__.py:894: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; socket
    self.import_plugin(arg, consider_entry_points=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
20 passed, 1 warning in 53.57s
$ git status --short
```

## Runtime per step

- 2.0: about 1 h. Five background searches for URLs and merger sources ran alongside it.
- 2.1: about 30 min.
- 2.2: about 25 min of fetching: 143 bank documents and 9 merger sources.
- 2.3: about 2 h 30 min for the 13 committed banks. Parallel agents entered them and they were merged in universe order. Merging, caching and provenance took about 1 min per bank.

## Deviations from PLAN.md

1. **Decimal mark declaration.** The provenance test needs "a declared decimal comma", but nothing says where it is declared.
   - `data/manual/report_urls.csv` gained a last column, `decimal_mark` (blank means `.`).
   - It was set per document by scanning each document's text. `,` applies to only 3 later Banco BPM Pillar 3 reports and 3 Italian and Spanish merger sources.
   - `provenance()` reads it from an optional `decimal_mark` column in the entries.
2. **Merger sources go through `fetch_reports.py`.**
   - Each is a `report_urls.csv` row with doc_type `merger_target`, bank_id the acquirer, and period the target's balance sheet date.
   - The 4 material deals were hashed too, so `source_sha256` and `source_page` are filled for 9 rows.
   - `mergers.csv` records no unit, so `merger_provenance()` (check `1_provenance_merger`) accepts the value at scale 1, 1e3 or 1e6. All 9 pass at 1e3.
3. **Retries in `fetch_reports.py`.**
   - After an HTTP error, the last attempt drops the browser headers, because Alpha Bank Romania's host refuses them.
   - On a TLS certificate error, it falls back to the system curl, which verifies against the Windows certificate store (needed for Commerzbank's host). Certificate checking is never turned off.
   - A download that is not a PDF is listed, not treated as a stop: instruction 02 step 2.2 overrides PLAN's stop rule.
4. **Summed fields.** Each component row starts its snippet with `component k/n`. `load_report_entries` sums the field when all n components are present and drops it otherwise.
5. **Entry value and sign.**
   - `value` is entered with its sign set by Convention 4.2.
   - The loader checks that |value| equals |value_as_printed| × unit_scale; a mismatch gets status `value_mismatch`.
   - A blank `value` is derived, positive for expense, allowance and deduction fields.
6. **`levies_in_admin`.** `derived()` handles report rows that have no resolution_dgs_contrib line (B.2). The KPI engine treats `fx_combined` and `levies_in_admin` as usable statuses.
7. **Check 3 on report rows.** It sums only the components the income statement shows (kickoff 5.3 item 3). Interest income and expense are still required.
8. **How entries were made.**
   - For each bank, an agent wrote a spec of entries. Each gives the date, field, document, physical page, a substring that identifies the pdfplumber line, the number as printed, unit_scale, sign rule and component.
   - A script checked the number is on the cited line and copied the whole line as the snippet. No figure was typed from memory.
   - Each bank was run through checks 2 to 5 and both seams before it was merged.
9. **Extra commits.** Two fixes fall outside the one-commit-per-step rule: 811eec3 (step 2.2, ruff) and 92cda21 (step 2.1, provenance digits and merger provenance).

## Not verified

- **Seam 2 explanations.** The per-bank notes put most differences down to prudential scope excluding insurance, or to FINREP line definitions. These are reasoned from the numbers and the documents' own reconciliations, not checked against EBA definitions. CAG is the exception: it is checked through the LR1 bridge above.
- **Banks entered but not committed because of the stop.**
  - DBK, CBK, SAN, BBVA, CABK, SAB, BKT and UCG passed checks 2 to 5 in the scratchpad, plus seam 1 where a Pillar 3 report exists. They are not in the repo.
  - UNI, ISP, BAMI, BPE and BMPS were stopped partway through entry.
  - The next session enters them again, starting from DBK.
- **KPIs and the ISP hand check.** No KPI at 2025-12-31 or 2026-06-30 has been computed, and the ISP hand check (step 2.5) was not done.

## Open questions

1. **The CAG gate (the stop reason).**
   - The 2% gate compares accounting-scope report total_assets with prudential-scope EBA total_assets. For a bank-insurer these differ by the insurance entities: EUR 426bn, or 19.5%, for CAG.
   - The same scope gap shows for other bank-insurers in seam 2: NDA 16%, DANSKE 17%, SWED 15%, SEB 13%, KBC 10%, BNP 11%, GLE 12%.
   - (a) Keep report total_assets as printed, and drop or widen the gate.
   - (b) Gate on report total_assets less LR1 row 2, i.e. the prudential scope. For CAG this agrees with EBA exactly.
2. **OPEN-26 (new): Pillar 3 published only as Excel or only on the EBA Data Hub.** Some bank/date pairs were not fetched for this reason; they are in the not-downloaded table. The options are in `decisions/OPEN.md`.
3. **Blank cells in CR1.** Many CR1 tables print a blank or `-` where an amount is nil. The usual cases are row 090 debt securities, non-performing (col d), and row 030 general governments, non-performing (cols d and j).
   - Decision B.1 allows no partial sums, so these fields are missing:
     - debt_securities for NDA, SEB, SHB, SWED, INGA, ABN and RABO at every Pillar 3 date, and for GLE at 2 dates;
     - loans_customers_gross and loans_customers_allowance for SHB and SWED;
     - loans_customers_allowance for ABN.
   - As a result, nim (through iea) and cost_of_risk will be blank for these banks.
   - Should a blank cell in an EU template count as 0?
4. **DBK admin_expenses and depreciation.** G&A includes depreciation (EUR 1.2bn, per note 23), and no depreciation line is printed. Both fields are missing, so DBK's opex-based KPIs will be blank.
   - (a) Leave them blank.
   - (b) Allow admin_expenses = compensation + G&A (including depreciation), with depreciation set to 0 and a status.
5. **Insurance-related lines in admin_expenses.** Three banks treat them differently. Which treatment is wanted?
   - GLE includes its reallocation line to insurance contracts, so its admin_expenses equals the income statement deduction.
   - BNP leaves its equivalent lines out.
   - KBC's figure comes from a note and includes opex allocated to insurance service expenses.
6. **RABO profit_owners.** It is entered as "attributed to Rabobank". That excludes the holders of Rabobank Certificates (CET1) and Capital Securities (AT1); EBA's figure includes them.
7. **Banks with no total operating income or total liabilities line.**
   - CBK prints neither. It has no total income line because credit risk sits between NII and fees, so its cost_income and fee_share will be blank.
   - UCG prints no total liabilities.
8. **Documents not obtained.** All are listed in the not-downloaded table.
   - Bankinter's H1 2025 report and all its Pillar 3 reports: the site returns 403 bot protection, which was not circumvented.
   - Commerzbank's Pillar 3 PDFs: no direct link was found.
9. **Mergers.**
   - BPER–UBI branch unit and BNP–AXA IM stay unsized. The proxy figures are listed above but not used.
   - Alpha Bank Romania needs RON in `[fx]` before its ratio can be computed.

## Files changed

- **Decisions:** `decisions/section_1_completion_review.md` (new), `decisions/data_sources.md`, `decisions/OPEN.md` (OPEN-26).
- **Instructions and config:** `CLAUDE.md` (amendments 11 to 15, staged per step 2.0), `config.toml` (CHF), `config/source_map.yaml` (comments).
- **FX data:** `data/raw/fx/CHF.csv` (new), `data/raw/MANIFEST.json`.
- **Manual data:**
  - `data/manual/mergers.csv`: 3 new columns, sizes, and the Anima row.
  - `data/manual/report_urls.csv`.
  - `data/manual/report_entries.csv`: 1,889 rows across 13 banks.
- **Report data:** `data/raw/report_manifest.csv` (new), `data/raw/report_text/*.jsonl.gz` (cited pages only).
- **Scripts:** `scripts/fetch_reports.py` (new).
- **Code:**
  - `bpb/ingest.py`: `load_report_entries`, `load_p3`, `entries_facts` and `parse_printed`, plus `build_facts` now taking report and p3 rows.
  - `bpb/checks.py`: `provenance`, `merger_provenance`, `seam_capital`, `seam_pl`, and check 3 on report rows.
  - `bpb/kpi.py`: `levies_in_admin`.
- **Tests:** `tests/test_report_entries.py` (new).
- **Uncommitted in the working tree** (steps 2.4 and 2.5, not reached):
  - `tests/test_checks.py`: `test_provenance_styles`.
  - `scripts/run_all.py`: KPIs to 2026-06-30, and checks on every family.

## Reviewer reads

1. The outcome paragraph at the top, and the CAG total_assets line under Evidence.
2. Open questions 1 to 5.
3. The provenance pass rate, and the counts for checks 2 to 5.
4. The seam 1 and seam 2 tables.
5. The not-downloaded table, and OPEN-26 in `decisions/OPEN.md`.
6. The step 2.0 merger tables.
7. The missing fields for each bank.
