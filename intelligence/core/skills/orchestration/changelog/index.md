# Skill: Changelog Procedure

> **PURPOSE:** End-of-session documentation for all agents. Uses a multi-level
> changelog system — write from the deepest relevant level outward. Each outer
> level summarizes and points back to the level below for full detail.

---

## The Multi-Level Changelog System

| Level | File | Granularity |
| :--- | :--- | :--- |
| Deepest | `intelligence/core/skills/[name]/changelog.md` | Every file touch, exact values, KR-level detail |
| Root | `changelog.md` | Version-tagged milestones, one-liner per skill, pointer down |

Start at the deepest level. The root entry should be readable as a summary;
the subdirectory entry should be complete enough to reconstruct what happened.

---

## When to Run

- At the natural end of a work session **if writes, edits, or structural changes occurred**
- When context window is approaching limit (to preserve state of work-in-progress)
- When handing off to a different agent (to bridge the context gap)
- After any significant structural change to the vault
- **Optional:** Read-only sessions that produce a significant new insight or blocker

---

## Procedure

### Stage 1 — Identify Active Skills

List which `intelligence/core/skills/` subdirectories were touched this session. Each active
subdirectory gets its own changelog entry before the root entry is written.

### Stage 2 — Write Subdirectory Changelog Entries (Deepest First)

**Handoff Exemption:** If the work performed in a subdirectory is already fully detailed in a newly created READY handoff file, you SHOULD skip Stage 2 for that subdirectory. Instead, ensure the root entry in Stage 3 points directly to the handoff.
 
 For each active subdirectory (e.g., `intelligence/core/skills/okr-reporting/`):

1. Check if `intelligence/core/skills/[name]/changelog.md` exists
   - If yes: read it first, then use `edit_file` to prepend a new entry
   - If no: create it with the starter format from `intelligence/core/skills/orchestration/changelog/entry_template.md`
2. Write with full granularity — exact paths, exact values, specific blockers
3. Include a **Next** line: what to do in this subdirectory next session

**Rule:** Always `read_text_file` before `edit_file`. Never `write_file` on an
existing changelog.

### Stage 3 — Write Root Changelog Entry

Read `changelog.md` at vault root. Find the highest `[X.Y.Z]` version and
determine the bump:

- **Patch** (`[X.Y.Z+1]`): routine work within existing skills
- **Minor** (`[X.Y+1.0]`): new skills, renamed files, structural changes
- **Major** (`[X+1.0.0]`): vault-wide rearchitecture

Prepend a new entry to root `changelog.md`:
- One-line summary per subdirectory touched
- Pointer to each subdirectory changelog: `See intelligence/core/skills/[name]/changelog.md`
- If this session was triggered by a handoff, include: `**Handoff:** handoff/[filename]-COMPLETE.md`
- Blockers and next tasks at vault level only — not granular KR detail

**Rule:** Use `edit_file` — never `write_file` on `changelog.md`.

### Stage 4 — Confirm and Report

State clearly:
- Subdirectory changelog(s) written (paths)
- Root `changelog.md` version and date
- Any blockers that prevented completion

---

## Creating a New Subdirectory Changelog

If `intelligence/core/skills/[name]/changelog.md` does not exist, create it with:

```markdown
# [Skill Name] Changelog

> Detail log for `intelligence/core/skills/[name]/`. See root `changelog.md` for version history.

---

## [Unreleased]
```

Then prepend the first entry immediately below `## [Unreleased]`.

---

## Entry Templates

Prepend below `## [Unreleased]` in the relevant subdirectory changelog. Full granularity.

### Subdirectory Entry (`intelligence/core/skills/[name]/changelog.md`)
Prepend below `## [Unreleased]` in the relevant subdirectory changelog. Full granularity.

```markdown
## [YYYY-MM-DD] — [Short Title]

**Files changed:**
- `intelligence/core/skills/[name]/file.md` — [what changed, one line]

**Blockers:**
- [description] — [what's needed to unblock]

**Next:** [what to do next]
```

### Root Entry (`changelog.md`)
Prepend below `## [Unreleased]`. High-level summary with directory pointers.

```markdown
## [X.Y.Z] — [Short Title] ([YYYY-MM-DD])

**Changes:**
- `intelligence/core/skills/[name]/` — [one-line summary] (see `intelligence/core/skills/[name]/changelog.md`)

**Handoff:** `handoff/[filename]-COMPLETE.md`
**Blockers:** [if any]

**Next Tasks:**
1. [vault-level task]
```

---

## Nightly Meta-Audit (Changelog Auditor)

> **Purpose:** Changelog auditing — accuracy, completeness, and cross-reference checks.
> Companion to Knowledge (structure) and Changelog (procedure).

### What Changelog Auditor Does
Knowledge checks vault structure. Changelog Auditor checks the logs.
Runs after sessions with significant work to verify changelogs accurately reflect what happened.

### Checks
See `audit_procedure.md` for full execution steps.
| Check | What it catches |
| :--- | :--- |
| 1 — Missing entries | Work done this session with no changelog entry |
| 2 — Phantom entries | Entries describing things that don't exist (dirs, files, tools) |
| 3 — Stale Next Tasks | Next Tasks already completed in a later entry — not removed |
| 4 — Inaccurate counts or names | Wrong numbers, wrong paths, superseded tool names |
| 5 — Subdir ↔ root alignment | Subdirectory entries without a root pointer, or vice versa |
| 6 — Handoff cross-reference | COMPLETE handoffs without a changelog entry; entries missing Handoff field |
| 7 — Version sequence | Gaps or duplicates in `[X.Y.Z]` version numbering |
| 9 — Permission & Access Scan | Scan the git log for the past 24 hours. Compare active agents against `AGENTS.md`. <br> - **Permission Gap**: Did an agent edit a file outside their defined scope? <br> - **Policy Bypass**: Did an agent invoke shell or build commands directly if they are a pure "Planner" or "Synthesizer"? <br> - **Config Viability**: Scan the local model config proxy paths `intelligence/core/skills/orchestration/access/agent-roots/*`. Check file permissions on token files (must be 600 or stricter) and note active JSON configurations (`allowedTools` or active paths). <br><br> **Format:** Output the raw flags and findings. Roz will synthesize them into "Violation!" and "Oops!" summaries based on the Artifact-First logic checks. |

### Output
A structured report (not a fix — flag only):
`intelligence/core/skills/orchestration/changelog/reports/changelog-report-YYYY-MM-DD.md`
