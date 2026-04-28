# Implementation Plan: Refine Releasinator Leak Detection & PR Query

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-28

undefined

---

# Context
The current `releasinator` logic for "leaks" and "repos to bump" relies on finding open `qa→master` PRs. However, the operational reality is that anything merged into the staging branch (`develop`) since the last production push (`master`) is "riding" with the next release. 

We need to shift the logic from "open PRs" to "branch comparison" to capture everything in flight, specifically looking for merged PRs in the staging branch that contain Jira keys not in the current release.

# Logic & Strategy

### 1. Staging Branch & Repo Discovery
- Use `develop` as the default staging branch (configurable via `STAGING_BRANCH` constant).
- Instead of searching for open PRs, the script will:
  - Identify the set of repos involved in the release (from Jira issues).
  - For each repo, check if `develop` is ahead of `master` using the GitHub Compare API (`/repos/{owner}/{repo}/compare/master...develop`).
  - If `ahead_by > 0`, the repo is added to the "Repos to Bump" list.

### 2. Deep Leak Detection via Merged PRs
- For each "ahead" repo:
  - Find the timestamp of the most recent commit on `master`.
  - Query GitHub for PRs merged into `develop` *after* that timestamp:
    - `is:pr is:merged base:develop merged:>{last_master_timestamp}`
  - Parse these PR titles and bodies for Jira keys (`CBP-XXXX`, `DATA-XXXX`).
  - Accumulate all unique keys found this way.

### 3. Jira Validation & Filtering
- For all discovered "candidate" leak keys:
  - Fetch their current status from Jira.
  - **Filter out** any issue where:
    - The key is already in the current release's "Release Issues" list.
    - The Jira `statusCategory` is "Done" or "Complete".
  - This ensures the "Leaks" report only contains active work that is moving to production unplanned.

### 4. Reporting Adjustments
- Update the "Repos to Bump" section to reflect all repos with pending `develop` changes.
- Update "Potential Leaks" to display the specific PRs where the leak was found for easier investigation.

# Execution Steps

1.  **Read & Baseline**:
    - Read `skills/releasinator/scripts/run.py` to identify all GitHub/Jira API call points.
    - Confirm the `STAGING_BRANCH` name is consistent across the org (default `develop`).

2.  **Update GitHub Helpers**:
    - Implement `get_last_master_commit_date(repo_path)`.
    - Implement `get_merged_prs_since(repo_path, date, base_branch)`.
    - Refactor `get_in_flight_jira_keys` to accept a list of PRs and parse their metadata.

3.  **Refactor Pipeline Logic**:
    - Update `run_project_pipeline` to use the new "ahead/behind" check instead of `get_qa_to_master_prs`.
    - Update the leak detection loop to use the PR-based discovery logic.

4.  **Integrate Jira Filtering**:
    - Enhance the Jira issue fetcher to check the `statusCategory` of candidate leaks.
    - Update the leak list construction to exclude Done items.

5.  **Verify & Document**:
    - Run `generate_report(skill='releasinator', date='2026-4-2')`.
    - Compare findings with the previous run to ensure no regressions in "known" issues.
    - Update `SKILL.md` with the new logic description.

# Verification
- [ ] `drift` sensor or manual check confirms `reports/releasinator/report.md` is generated correctly.
- [ ] Leaks section shows issues that are in `develop` but not in the release.
- [ ] "Done" issues in Jira are NOT shown as leaks even if they have commits in the diff.
- [ ] All repos with pending `develop` changes are listed in "Repos to Bump".
