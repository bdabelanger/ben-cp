# Implementation Plan: Restructure releasinator with auto mode and three-section report

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-28

---

## Context

Releasinator needs: `--auto` flag for dream pipeline, three-section report (next release primary + upcoming list + recent list), no sidecars.

**File:** `skills/releasinator/scripts/run.py`

## Change 1 — fetch_jira_versions()

```python
def fetch_jira_versions(project_key="CBP"):
    resp = requests.get(f"{JIRA_BASE}/project/{project_key}/versions", auth=jira_auth(), ...)
    today = datetime.now().date().isoformat()
    released, unreleased_future = [], []
    for v in resp.json():
        if not v.get("releaseDate"): continue
        entry = {"name": v["name"], "releaseDate": v["releaseDate"], "released": v.get("released", False)}
        if v.get("released"): released.append(entry)
        elif v["releaseDate"] >= today: unreleased_future.append(entry)
    unreleased_future.sort(key=lambda x: x["releaseDate"])
    released.sort(key=lambda x: x["releaseDate"], reverse=True)
    return unreleased_future[0] if unreleased_future else None, unreleased_future[1:], released[:5]
```

## Change 2 — --auto flag

```python
parser.add_argument("--auto", action="store_true")
# In main():
next_release, upcoming, recent = fetch_jira_versions()
if args.auto:
    if not next_release:
        print("⚠️  --auto: no upcoming release — skipping"); sys.exit(0)
    release_name = next_release["name"]
else:
    release_name = args.release
```

Always fetch version context regardless of mode.

## Change 3 — Three-section write_report()

**Section 1 — Primary (existing content, already works)**
Full readiness: repos, issues, leaks, flags, migrations — under `# Release Readiness — {release_name}`

**Section 2 — Upcoming Releases**
```markdown
---

## Upcoming Releases

| Release | Date | Days away |
|---------|------|-----------|
| Platform-2026-5-28 | 2026-05-28 | 30 days |
```
Compute days away from today. Empty: `_No additional releases scheduled._`

**Section 3 — Recent Releases**
```markdown
---

## Recent Releases

| Release | Date |
|---------|------|
| Platform-2026-4-23 | 2026-04-23 |
```
Last 5. Empty: `_No recent releases found._`

Pass `next_release`, `upcoming`, `recent` into `write_report()`.

## Verification
- [ ] `python3 run.py --auto` detects next release and runs
- [ ] `--auto` exits cleanly (code 0) if no upcoming release
- [ ] report.md has three sections
- [ ] `--release "2026-5-1"` still works
- [ ] Upcoming shows correct days-away
