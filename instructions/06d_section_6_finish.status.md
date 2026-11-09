# Status: instructions/06d_section_6_finish.md

## Outcome

**Done.** Steps 6.6b, 6.7 and 6.8 are built, committed and pushed. CI on the final commit, 1588a2a, gives `success`, 65 passed, and so does the fresh clone at that commit. A second `bpb build` leaves `git status --porcelain` empty. The review is the 06d part of `review/section_6.md`.

## Last step reached

Step 6.8, then the fresh clone check, the review and this file. Commits this session:

- **6.6b:** 125e3e8
- **6.7:** 51f3f45
- **6.8:** 1588a2a
- **Review:** 6231b0f

## Results

- **Hand check:** LLOY, INGA and SWED all match the pipeline to within EUR 0.50. INGA's sheet tests the joint formula on 2 gaps.
- **CAG AT1:** the 4 printed values are entered, 7,218, 8,612, 8,143 and 8,020 (EUR m), status `at1_from_reconciliation`, and all pass provenance.
- **CAG's joint RoTE gap is still blank.** RoTE now lacks intangibles_deduction, which CAG has not got in the report family at any date (OPEN-47).
- **Headline:** INGA, 10.20 points of RoTE or EUR 6,926m a year, the largest joint RoTE gap outside the scope list.
- **README:** 14,844 bytes. It went to 15,051 with the B.2 and B.3 changes, so Q5 lists only the 29 fields that at least 15 banks report, leaving out 6.
- **League tables:** the cluster CSVs rank within each cluster, and the HTML pages show 1 table per cluster.
- **Dashboard:** `test_dashboard_runs` and `test_dashboard_no_external` pass on Windows and on CI's Linux.

## Questions for the reviewer

1. **OPEN-47 (not blocking):** CAG's Pillar 3 pages print "Goodwills and intangible assets" in the same table as the AT1 line: 19,143, 19,309, 19,604 and 20,747 (EUR m). At the 2 EBA dates it agrees with the EBA value. Enter it as intangibles_deduction, which would fill CAG's RoTE, or leave CAG's RoTE blank?

## Notes

- **The page text cache** for the 4 cited CAG documents was rebuilt with `scripts/fetch_reports.py --cache-pages`, with no network. Otherwise the new entries fail provenance.
- **The venv left the lock once.** An early `uv run` updated 9 packages. I reinstalled from `requirements-lock.txt` and rebuilt, and nothing built on the newer versions was committed. From then on I called the venv's Python directly.
- **Housekeeping:** `C:\bpbs6e` joins `C:\bpbs6d` and the other `C:\bpbs*` folders for the owner to delete.

## git log origin/main --oneline -5

```
6231b0f section 6: review of steps 6.6b to 6.8
1588a2a step 6.8: build check
51f3f45 step 6.7: readme, league tables and dashboard test
125e3e8 step 6.6b: hand check bank and CAG AT1
b09fddc instruction 06d: decisions on OPEN-45 and OPEN-46, finish section 6
```
