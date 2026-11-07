# Section 6 review decisions

Written in step 6.6 from `instructions/06c_section_6_finish.md` Sections A and B, verbatim.

---

## A. Review of Section 6

Section 6 is approved once steps 6.6 to 6.8 are done. The build, the determinism test, CI and the fresh clone checks are accepted as reported.

The reviewer read the README and checked 3 things against the CSVs and the entries.

### A.1 Cost of risk is sized without the margin it buys

Q2's 4th and 7th rows size SAN's cost of risk at EUR 11.5bn and BBVA's at EUR 6.3bn. Both banks lead their cluster on NIM, so their NIM is not sized. Their high cost of risk is the price of lending in Brazil, Mexico and Turkey, and their high NIM is what that price buys. Sizing 1 side and not the other is the fee_share mistake of instruction 05 again.

The reviewer computed a risk adjusted margin, (NII − impairments_fin) / average IEA, from the numerators and denominators in `kpi.csv` at 2026-06-30, underlying basis. Targets are Harrell Davis p = 0.75, leave one out, over the 2025 clusters of `peers.csv`:

| bank | risk adjusted margin | target |
|---|---|---|
| SAN | 0.020965 | 0.019887 |
| BBVA | 0.032541 | 0.019569 |

Both banks sit above the target, so EUR 17.8bn of the Q2 table is not a gap.

### A.2 The headline leads with a bank the README says not to compare

The headline gap is CAG's, EUR 19.9bn. CAG is on the scope caveat list, its NIM denominator holds insurance assets, and its joint RoTE gap is blank because at1_instruments is missing at the bridge dates.

### A.3 The insurer note is right

For ISP at 2026-06-30, the 2 fair value lines inside item 120 (−3,254 and 6,157) are returns on policyholder assets. Their offset, the insurance finance result, sits below item 120. For KBC, insurance revenue is inside TOTAL INCOME and insurance service expenses sit below it. So the README note holds: other below the line is the insurance effect, and the cost to income ratio is flattered. No change.

### A.4 The 4 open questions

1. **The headline:** see B.2.
2. **spec_log `status` column:** accepted, as a reviewer schema change.
3. **League cluster files:** a cluster league must rank within the cluster. See B.3.
4. **README readings:** Q2 stays the 10 largest by joint EUR, with the B.2 columns. Q3, the largest gaps to the median either way, is accepted.

Also, the dashboard has no test, so B.4 adds one.

## B. Decisions

### B.1 Risk adjusted margin replaces separate NIM and cost of risk sizing

1. **Derived field `nii_net_llp`.** It is nii − impairments_fin, at the same bank, date, period and family. The status carries both inputs' statuses. A net release (negative impairments_fin) adds to it.

2. **New KPI `risk_adj_nim`.** In `config/kpis.yaml`: numerator `nii_net_llp`, denominator `iea`, average true, unit bps, direction higher. It is computed on both bases, ranked, benchmarked and given verdicts like every other ranked KPI. It is not a peer feature.

3. **What is sized.** `[gaps] sized` = `["cost_income", "risk_adj_nim"]`. This is a reviewer change to `config.toml`.

   nim and cost_of_risk stay benchmarked. They keep their verdicts and stay in the KPI table and the profiles, but they are not sized.

4. **Standalone gap.** ΔΠ = (target − value) × ĪEA. It uses the same lagging and outside noise rule as every sized gap.

5. **Joint gap.** The margin gap is closed through NII at the bank's current credit cost:
   - d = target_ram × IEA − (NII − LLP);
   - NII′ = NII + d;
   - LLP′ = LLP.

   The cost to income term stays as it is, on I + d. `joint_gap` takes the key `risk_adj_nim` in place of `nim` and `cost_of_risk`.

6. **Hand check workbook.** Rebuild it with the risk adjusted margin lines in place of the NIM and cost of risk lines. Its test must still pass.

7. **Rebuild** everything downstream: GAPS, GAPS_JOINT, gaps_range, VALUATION (the uplift uses joint_rote_pts), the profiles, the league tables, the README and answers.csv.

### B.2 README headline and Q2

1. **Headline sentence.** Name the bank with the largest joint RoTE gap in points among banks outside the scope list, with its points and its joint EUR. The valuation clause stays.

   The scope list is the one the README already generates in Q5: the amendment 26 banks, plus any bank with a total assets seam above 5%.

2. **Q2 table.**
   - Keep the 10 largest by joint EUR.
   - Add 2 columns after Joint: `Joint RoTE pts`, and `Scope`, which reads `yes` for a bank on the scope list and is blank otherwise.
   - The callout adds 1 sentence: NIM and cost of risk are sized together as a risk adjusted margin, because a high cost of risk is the price of a high margin.

3. **Q4 wording.** Write "β rose from X in Y to Z in W", using the first and last years with a significant β. Do not write "every year".

4. **Percentages** follow Convention 4.7: 2 decimals. Q5's "0.0000%" becomes "0.00%".

5. **Size.** README.md must stay under 15 KB. If it goes over, the Q5 table lists only fields that at least 15 banks report, and its callout says how many fields were left out.

### B.3 League tables by cluster

1. **Cluster league CSVs.** These are the cluster group files. Add a column `cluster` after `rank`. The rank restarts at 1 within each cluster.
2. **League HTML.** It shows 1 table per cluster.
3. **README Q1.** Q1 ranks all banks, as now. Add a `Cluster` column on each side, so each verdict can be read against its group.

### B.4 Dashboard test

1. **Root path.** `bpb/dashboard.py` reads `outputs/` under the path in the environment variable `BPB_ROOT`. If the variable is not set, it uses the current directory.

2. **Test `tests/test_dashboard.py::test_dashboard_runs`.**
   - Build into `tmp_path`. A session scoped fixture in `tests/conftest.py` may share 1 build with `test_build`.
   - Load the app with `streamlit.testing.v1.AppTest.from_file`.
   - Select LLOY, ISP and SWED in turn, and run.
   - Assert that `at.exception` is empty each time.

### B.5 CAG at1_instruments

Enter CAG's at1_instruments from CC1 row 30 of the Crédit Agricole Group Pillar 3 report at 2024-12-31, 2025-06-30, 2025-12-31 and 2026-06-30, wherever it is printed. Rule 16 applies.

If a date's Group Pillar 3 report is not among the hashed documents, or the row is not printed, leave that date out and list it.

---

# Instruction 06d decisions

Written in step 6.6 from `instructions/06d_section_6_finish.md` Sections A and B, verbatim.

## A. Review

The stop was correct. B.1 of instruction 06c removed ISP's only sized gaps, and the reviewer did not check the hand check banks against it.

The reviewer confirmed from `gaps.csv` at 2025-12-31 that ISP is `not_sized` in all 12 rows. INGA has both gaps sized in the cluster and universe groups on both bases.

The A.1 result holds. risk_adj_nim matches the reviewer's figures to within 1e-6, and the EUR 17.8bn for SAN and BBVA is gone.

## B. Decisions

1. **OPEN-46: (a).** `[gaps] hand_check_banks` = `["LLOY", "INGA", "SWED"]`. This is a reviewer change to `config.toml`.

   INGA has both sized gaps, so the workbook now exercises the joint formula on 2 gaps. INGA is also outside the scope list. `test_hand_check` itself is unchanged.

2. **OPEN-45: use the printed line.** "(-) AT1 instruments accounted as equity" is the AT1 held in accounting equity. That is the amount the tangible equity deduction needs, and it is closer to it than CC1 row 30's regulatory amount.

   - Enter it as at1_instruments for CAG at the 4 dates, from the cited pages, with status `at1_from_reconciliation`. Rule 16 applies.
   - The 2024-12-31 value of 7,218 also appears in the equity statement cited for at1_in_equity. Print both pages in the review.
   - Do not fetch the website's CC1 tables.
   - This applies to CAG only.

3. **Rule 7 and B.4: the marker is accepted.** `@pytest.mark.allow_hosts(["127.0.0.1"])` is allowed on `test_dashboard_runs` only. Rule 7 exists to keep the suite off the network, and a loopback socket does not break that.

   Add to the same test file `test_dashboard_no_external`. Under the same marker, a connect to `example.com:80` must raise.

4. **`joint_gap` branches: confirmed.** Keep the `nim` and `cost_of_risk` branches. Add a comment that the pipeline does not use them since instruction 06c B.1.

5. **CI.** `main` is red until step 6.6 is committed again. That is expected. Step 6.8 confirms that it is green.

6. **Housekeeping.** `C:\bpbs6d` joins the other folders the owner will delete.
