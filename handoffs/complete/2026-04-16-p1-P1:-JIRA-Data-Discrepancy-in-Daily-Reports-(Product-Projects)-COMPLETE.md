The daily report for Product Projects is not accurately reflecting the data from JIRA.

**Observed Issue:**
- The HTML report (`file:///Users/benbelanger/My%20Drive%20(ben.belanger@casebook.net)/ben-cp/reports/dream/reports/product-projects.html#CBP-2736`) shows only one outstanding Jira user story for project CBP-2736.
- However, I manually counted 13 outstanding stories within the JIRA epic for this project.
- The count of 'Done' stories is also wildly inaccurate across all projects and statuses.

**Request:** Please investigate the pipeline responsible for fetching and processing JIRA data to determine why it is not retrieving the complete set of user stories and accurate status counts. This seems to be a systemic issue across multiple projects/statuses.

---

## 🛠️ Code Implementation Plan (Proposed Solution)

**Issue Root Cause:** The pipeline intentionally short-circuits recursive HTTPS requests if a matching `.json` file already exists locally in `inputs/status-reports/raw/jira`. This causes stories to be permanently orphaned and cached to their state on the day the project was first introduced.

**Proposed Changes:**
### `orchestration/pipelines/product/projects/pipeline/`
#### [MODIFY] [step_2_atlassian_fetch.py](file:///Users/benbelanger/My%20Drive%20(ben.belanger@casebook.net)/ben-cp/orchestration/pipelines/product/projects/pipeline/step_2_atlassian_fetch.py)
* Refactor `missing_keys` logic to trigger API interactions for *all* `epic_keys` generated from Asana state, overriding the locally saved files with the newest structural payload. This ensures daily execution returns daily statuses.

**Open Questions:**
- None; this behaves as a conventional, self-contained fix.

**Verification Plan:**
### Automated Tests
- Run `cd orchestration/pipelines/product/projects/pipeline && python3 full_run.py` to initiate a clean flush.
- Read `./inputs/status-reports/raw/jira/CBP-2736.json` directly to verify data represents current-state stories (expecting an increase from 1 left outstanding on 04/14 to ~13 instances today).
- Verify the generated `daily-report.html` correctly displays the true status breakdown.