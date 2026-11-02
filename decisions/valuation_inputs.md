# Valuation inputs (kickoff Section 2, corrections 4, 5 and 7)

- RoTE waits for Section 3: EBA carries no AT1 coupons or share counts, so RoTE and every valuation input are computed once Section 3 enters them from reports. Section 1 computes every other KPI.
- Shares outstanding come from reports, not yfinance, whose share count history is unreliable; yfinance supplies the share price only.
- LSE prices are quoted in pence in yfinance (`GBp`) and are divided by 100 before any use.
