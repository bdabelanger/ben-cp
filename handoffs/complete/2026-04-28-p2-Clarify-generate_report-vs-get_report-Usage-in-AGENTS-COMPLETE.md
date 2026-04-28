# Clarify generate_report vs get_report + Fix Wired Skill Enums in ben-cp.ts

> **Prepared by:** Cowork (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-28

Removed phantom 'platform' enum from ben-cp.ts; wired 'status' and 'tasks'; updated schema description to list valid values; improved error message. AGENTS.md reordered to list_reports → get_report → generate_report with bold read-vs-write warnings. Build passed clean.

---

## Context

Two related issues found in `generate_report`:

**Issue 1 — `ben-cp.ts` has wrong/missing skill enums**
The source code at `src/ben-cp.ts` lines 982–990 only wires two skills:
- `"platform"` → maps to `skills/status/run.py` — but `"platform"` is not a real repo domain and confuses agents
- `"dream"` / `"reporting"` → maps to `skills/dream/run.py`
- Everything else throws: `Report generation not automated for skill: {skill}`

`"status"` and `"tasks"` both have `run.py` files but are not wired. `"platform"` should be removed entirely.

**Issue 2 — AGENTS.md doesn't distinguish generate_report from get_report**
Agents have been calling `generate_report` to *read* reports, when they should use `get_report`. The distinction needs to be explicit in the MCP Tools table.

---

## Execution Steps

### Step 1 — Edit `src/ben-cp.ts`

Read the file first, then locate the `generate_report` handler (around line 977). Replace the skill routing block:

**Old:**
```typescript
if (skill === "platform") {
  script = path.resolve(rootPath, "skills/status/run.py");
  cmdArgs = ["--force", "--team", "platform"];
} else if (skill === "dream" || skill === "reporting") {
  script = path.resolve(rootPath, "skills/dream/run.py");
} else {
  throw new Error(`Report generation not automated for skill: ${skill}`);
}
```

**New:**
```typescript
if (skill === "status") {
  script = path.resolve(rootPath, "skills/status/run.py");
  cmdArgs = ["--force", "--team", "platform"];
} else if (skill === "dream" || skill === "reporting") {
  script = path.resolve(rootPath, "skills/dream/run.py");
} else if (skill === "tasks") {
  script = path.resolve(rootPath, "skills/tasks/run.py");
} else {
  throw new Error(`Report generation not automated for skill: ${skill}. Valid options: status, dream, tasks.`);
}
```

Also update the tool description and schema at line ~440:

**Old:**
```typescript
skill: { type: "string", description: "The skill or domain (e.g. 'platform', 'dream')." },
```

**New:**
```typescript
skill: { type: "string", description: "The skill or domain to run. Valid values: 'status', 'dream', 'tasks'." },
```

### Step 2 — Rebuild ben-cp
```
cd "/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp" && npm run build
```

### Step 3 — Edit AGENTS.md MCP Tools table

Locate the three report rows and replace:

**Old:**
```
| `list_reports` | List available report domains. Always call this first if unsure which domain to use — do not guess or rely on examples in tool descriptions. |
| `generate_report` | Run a report pipeline for a domain. Use `list_reports` to confirm valid domains before calling. |
| `get_report` | Read a generated report. Path is relative to `reports/` — e.g. `get_report(path="status/report.md")`. Never prefix with `reports/` or `skills/`. |
```

**New:**
```
| `list_reports` | List available report domains. |
| `get_report` | **Default tool for reading any report.** Path is relative to `reports/` — e.g. `get_report(path="status/report.md")`. Never prefix with `reports/` or `skills/`. Use this to fetch the latest report. |
| `generate_report` | **Runs a pipeline to produce a new report — do NOT use this to read reports.** Valid skills: `status`, `dream`, `tasks`. Calling with any other value will fail. |
```

### Step 4 — Changelog
Root `changelog.md` entry only (Handoff Exemption applies).

---

## Acceptance Criteria

- [ ] `"platform"` enum removed from `ben-cp.ts`
- [ ] `"status"` and `"tasks"` wired in `ben-cp.ts`
- [ ] Error message lists valid options
- [ ] Tool schema description updated — no mention of `platform`
- [ ] `npm run build` succeeds
- [ ] AGENTS.md `get_report` marked as default read tool
- [ ] AGENTS.md `generate_report` explicitly warns against using it to read reports
- [ ] Root changelog entry written
