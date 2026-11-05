# instructions/06d_section_6_finish.md: finish Section 6

Resume at step 6.6. Build steps 6.6 to 6.8 as written in `instructions/06c_section_6_finish.md`, with the decisions below. Precedence (rule 13): this file beats instruction 06c.

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

## C. Steps

### Step 6.6

Finish step 6.6 as in instruction 06c, with B.1, B.2 and B.4. Commit it as `step 6.6b: hand check bank and CAG AT1`.

**Review evidence:**
- the 3 hand check sheets' totals against the pipeline;
- CAG's at1_instruments rows and their pages;
- CAG's joint RoTE gap at 2026-06-30;
- `test_hand_check` output.

### Steps 6.7 and 6.8

As in instruction 06c, with B.3 in step 6.7.

**Headline check.** If CAG's joint RoTE gap is now filled, the 06c B.2 headline rule still applies. CAG is on the scope list, so it cannot be the headline bank.

## D. End

1. Run the fresh clone check.
2. Append the steps to `review/section_6.md`.
3. Push.
4. Write `instructions/06d_section_6_finish.status.md`, commit it, push it and stop.

The partial rule applies.
