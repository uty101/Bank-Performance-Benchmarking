# Status: instructions/06c_section_6_finish.md

## Outcome

**Stopped** under rules 4 and 5 at step 6.6. `test_hand_check` fails because ISP no longer has a sized gap (OPEN-46). Steps 6.7 and 6.8 were not run, so Section 6 is not yet approved.

The fresh clone at 7e055ed gives 61 passed and 1 failed, and ruff is clean. CI on that commit fails on the same test, so `main` is red until OPEN-46 is decided. The review is the 06c part of `review/section_6.md`.

## Last step reached

Step 6.6, with B.1 and B.5 applied and everything rebuilt. Commits this session:

- **6.6:** 7e055ed
- **Review:** the commit after it

## Results

- **risk_adj_nim:** matches A.1 to within 1e-6: SAN 0.020965 against a target of 0.019887, BBVA 0.032541 against 0.019569. Neither has a margin gap, so the EUR 17.8bn is gone.
- **Largest joint gap at 2026-06-30:** still CAG, now EUR 16.7bn, down from EUR 19.9bn. INGA is next at EUR 6.9bn.
- **GAPS:** 3,720 rows, down from 5,580, with 2 sized gaps in place of 3.
- **B.5:** no entries. CC1 is not printed in any of the 4 hashed CAG documents, so all 4 dates are left out, and CAG's joint RoTE gap stays blank.

## Stop reason

Under B.1, ISP at 2025-12-31 is `leading` on risk_adj_nim in every group. On cost_income it is inside noise in the cluster and universe groups and `leading` in the market group. So it has no sized gap in any group on either basis.

`test_hand_check` asserts a sized gap on every sheet, so it fails at ISP. B.1 item 6 says the test must still pass, step 6.7 says existing tests pass unchanged, rule 5 forbids rewriting it, and rule 6 fixes `hand_check_banks`. Every way out is a reviewer decision.

The method itself is doing what it should for a bank with a strong risk adjusted margin. The LLOY and SWED sheets match the pipeline.

## Questions and blockers for the reviewer

1. **OPEN-46 (blocking):** (a) replace ISP in `[gaps] hand_check_banks`, or (b) keep ISP and change the test? LLOY and SWED have 1 sized gap each, so neither exercises the joint formula on 2 gaps. 11 banks have both at that date: ABN, BMPS, DANSKE, GLE, INGA, NDA, RABO, SAB, SANUK, SEB and SHB.
2. **OPEN-45 (not blocking):** CAG's Group AT1 is printed as "(-) AT1 instruments accounted as equity", not as CC1 row 30. Use that line, or fetch the website's CC1 tables? Either should fill CAG's joint RoTE gap.
3. **Rule 7 and B.4:** `test_dashboard_runs` cannot run under `--disable-socket` without `@pytest.mark.allow_hosts(["127.0.0.1"])`, because `AppTest` needs a loopback socket. In a trial on Windows it passed, and an external connect was still refused. Is that marker acceptable?
4. **`joint_gap` keeps its `nim` and `cost_of_risk` branches,** because `test_joint_single_synthetic` uses them and existing tests must pass unchanged. The pipeline does not use them. Please confirm.

## Housekeeping

C:\bpbs6d joins the other `C:\bpbs*` folders for the owner to delete. Heavy jobs ran one at a time this session, and no memory failure occurred.

## git log origin/main --oneline -3

```
736c760 section 6: review of step 6.6 (stopped: ISP has no sized gap, OPEN-46)
7e055ed step 6.6: section 6 review decisions (stopped: ISP has no sized gap, OPEN-46)
ebd7afd instruction 06c: section 6 review and finish
```
