# Status: instructions/01b_section_1_completion.md (session 1b)

## Outcome

Completed. Section 1 is finished, and the review is `review/section_1.md` (00ecea3).

## Last step reached

Step 1.7, mergers and materiality (0f8971c). The steps of this session:

- 1.2b (e43a65d)
- 1.3 (f7fc13f)
- 1.4 (6d9980b)
- 1.5 (31de065)
- 1.6 (30ce5b6)
- 1.7 (0f8971c)

## Stop reason

None.

## Questions and blockers for the reviewer

1. **BPER–Carige (completed 2022-06-03).** Carige's total assets were not found on a BPER or Carige page, so materiality is blank. BPER's EBA total assets at 2022-03-31 are EUR 135.8bn, so Carige is a break if its total assets exceed EUR 13.6bn.
2. **Non-bank acquisitions.** BNP–AXA IM, Société Générale (Ayvens)–LeasePlan and Deutsche Bank–Numis are in `mergers.csv` with blank target total assets. Banco BPM–Anima is left out, since no acquirer page was found. Should non-bank targets stay in the file?
3. **Blank target total assets.** These deals have none, so their materiality is blank:
   - UniCredit–Alpha Bank Romania;
   - BPER–UBI branch unit (no total published);
   - Nordea–Danske Norway (a business transfer; lending of EUR 9bn is the only size given);
   - Barclays–Tesco Bank and NatWest–Sainsbury's Bank (not looked up).
4. **UK acquirers.** SANUK–TSB, HSBA–SVB UK, BARC–Tesco Bank and NWG–Sainsbury's Bank wait for Section 3 total assets.
5. **REYL (Intesa, 2021).** It is in CHF, which is not in `[fx] currencies`, so its ratio is blank. It is clearly immaterial.
6. **Material breaks found:**
   - CaixaBank–Bankia, 2021-03-26, ratio 0.545;
   - Unicaja–Liberbank, 2021-07-30, 0.723;
   - BPER–Banca Popolare di Sondrio, 2025-07-18, 0.392;
   - Monte dei Paschi–Mediobanca, 2025-09-15, 0.796.

Other notes:

- **Merger research.** The list and figures were gathered by research subagents that fetched each source page. They were not re-fetched in the main session, and the review lists every document and page.
- **Fields and source map.** `fields.yaml` keeps the P&L or balance sheet split in a new `period` key, because `kind` is now `amount` or `ratio`. `source_map.yaml` gained `bank_groups` (the UK list), because `apply_source_map` receives no universe.
- **Check results.** Checks 2 to 6 pass on every EBA row. Check 9 flags 14 of 18,602 moves, including the quarters of the Bankia and Liberbank acquisitions. Check 3's largest relative miss is 2.6e-6.
- **KPI coverage.** Every EU bank has 13 of 19 KPIs at every date. The exceptions are BPER at 2021-12-31 and 2022-06-30, and DNB before 2023-06-30. The other 6 KPIs are rote, income_fte, cost_fte and cost_customer (`pending_section_3`) and lcr and nsfr (`missing_input`).
- **Fresh clone.** A clone from GitHub at 0f8971c passed: ruff clean, `17 passed`, clean `git status`.
- **Pushes.** There were 3: the steps, the review, then this file.

## git log origin/main --oneline -3

```
00ecea3 section 1: review (complete)
0f8971c step 1.7: mergers and materiality
30ce5b6 step 1.6: checks 2 to 6 and 9 on EBA rows
```
