# Section 3 review decisions

Written in step 3.8 from `instructions/04_section_4.md` Sections A and A.1, verbatim.

---

## A. Approval of Section 3

Section 3 is approved once step 3.8 is done.

What the reviewer checked:
- rote at reported basis across banks and dates. It is plausible where filled: NWG 19.2% and HSBA 14.5%, against their published figures.
- The 3 hand checks (LLOY, BBVA, SEB) match `kpi.csv`.
- The BAMI and BMPS gaps to their published RoTE trace to the banks' own definitions, not to entry errors, and are accepted.
- Deviations 22 and 23 are accepted.

You may delete the fresh clone folders on the owner's machine (`C:\bpbs3`, `C:\bpbs3b`, `C:\bpbs3c`) if your safety check allows it. If it does not, leave them.

### A.1 Decisions on OPEN-34 and OPEN-35

1. **OPEN-34.** at1_coupons is 0 with status `no_at1_coupon` when the bank had no AT1 in equity during the period, or when the period's coupon line is printed as a dash or as nil. Cite the page that says so:
   - BMPS: the "no equity instruments" statement, with CC1 row 30 a dash;
   - NDA H1 2026: the cash flow line.

   That gap was the reviewer's, left open in the 03c rule.
2. **OPEN-35.**
   - **Comparative columns.** A comparative column in a later document counts as a printed amount for its date, with status `from_comparative`. This applies to SANUK, DANSKE and ABN.
   - **Dash-only lines.** A balance sheet non controlling interests line printed only as dashes is 0 with status `no_nci_line`, the same as no line. This applies to BKT.
