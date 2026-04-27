---
title: Claude Code Implementation Plan Consolidate Casebook into skillscasebook
type: handoff
domain: handoffs/complete
---

# Claude Code Implementation Plan: Consolidate Casebook into skills/casebook/

> **Prepared by:** Claude (Cowork session, 2026-04-08)
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **v1.0**
> **STATUS**: ✅ COMPLETE

All 9 files moved from `skills/casebook-reporting/` to `skills/casebook/reporting/` via `git mv`. Stubs created for `admin-mcp/` and `billing-mcp/`. `index.md` and `changelog.md` created at `skills/casebook/`. `AGENTS.md` vault tree and `skills/index.md` links updated. No unexpected findings in the external MCP repos — both are standard Node/TypeScript projects. `skills/index.md` had 5 direct links to `casebook-reporting/` paths, all updated.

**Changelog:** see root `changelog.md` (next version bump)

---

## Context

Casebook-related work is currently split across three separate locations:

| Location | Contents | Type |
| :--- | :--- | :--- |
| `skills/casebook-reporting/` | Reference docs (cases, intake, people, tenants, users, Reveal BI) + changelog | Documentation |
| `/Users/benbelanger/GitHub/casebook-admin-mcp` | Casebook Admin MCP server | External repo |
| `/Users/benbelanger/GitHub/casebook-billing-mcp` | Casebook Billing MCP server | External repo |

**Goal:** Consolidate everything under `skills/casebook/` so all Casebook skill
documentation, reference files, and MCP context lives in one place. The external
repos stay where they are (they are independent git repos) — but their documentation,
SOPs, and any reference material moves into `skills/casebook/`.

---

## Execution Order

1. **Task 1** — Audit all three source locations
2. **Task 2** — Create `skills/casebook/` directory structure
3. **Task 3** — Move `skills/casebook-reporting/` contents into `skills/casebook/reporting/`
4. **Task 4** — Create reference stubs for casebook-admin-mcp and casebook-billing-mcp
5. **Task 5** — Create `skills/casebook/index.md`
6. **Task 6** — Create `skills/casebook/changelog.md`
7. **Task 7** — Update `AGENTS.md` vault structure tree
8. **Task 8** — Update root `skills/index.md` if it references `casebook-reporting`
9. **Task 9** — Final audit and completion report

---

## Task 1: Audit All Source Locations

Read and list:
1. `list_directory` on `skills/casebook-reporting/` — note all files
2. `list_directory` on `/Users/benbelanger/GitHub/casebook-admin-mcp/` — note structure
3. `list_directory` on `/Users/benbelanger/GitHub/casebook-billing-mcp/` — note structure
4. `list_directory` on `skills/` — confirm `casebook/` does not yet exist

Report any unexpected files or structure before proceeding.

---

## Task 2: Create skills/casebook/ Directory Structure

Create the following directories:

```
skills/casebook/
skills/casebook/reporting/
skills/casebook/admin-mcp/
skills/casebook/billing-mcp/
```

Use `create_directory` for each. Confirm each exists before proceeding.

---

## Task 3: Move casebook-reporting/ Contents

Move all files from `skills/casebook-reporting/` into `skills/casebook/reporting/`:

| From | To |
| :--- | :--- |
| `skills/casebook-reporting/casebook-cases.md` | `skills/casebook/reporting/casebook-cases.md` |
| `skills/casebook-reporting/casebook-intake.md` | `skills/casebook/reporting/casebook-intake.md` |
| `skills/casebook-reporting/casebook-people.md` | `skills/casebook/reporting/casebook-people.md` |
| `skills/casebook-reporting/casebook-tenants.md` | `skills/casebook/reporting/casebook-tenants.md` |
| `skills/casebook-reporting/casebook-users.md` | `skills/casebook/reporting/casebook-users.md` |
| `skills/casebook-reporting/reveal_bi_syntax.md` | `skills/casebook/reporting/reveal_bi_syntax.md` |
| `skills/casebook-reporting/reveal_bi_visualizations.md` | `skills/casebook/reporting/reveal_bi_visualizations.md` |
| `skills/casebook-reporting/index.md` | `skills/casebook/reporting/index.md` |
| `skills/casebook-reporting/changelog.md` | `skills/casebook/reporting/changelog.md` |

**Use `git mv` for all moves** — preserves file history.

After confirming all files moved successfully, remove the now-empty
`skills/casebook-reporting/` directory:
```
git rm -r skills/casebook-reporting/
```

---

## Task 4: Create MCP Reference Stubs

These repos live outside the vault. Create a lightweight reference doc in each
subdirectory so agents know what they are and where to find them.

### skills/casebook/admin-mcp/index.md

```markdown
# Casebook Admin MCP

> **Repo:** `/Users/benbelanger/GitHub/casebook-admin-mcp`
> This directory is the skills/documentation layer for the Casebook Admin MCP server.

---

## What It Does

[To be populated — describe the admin MCP's purpose and tools]

## Key Files (in repo)

[To be populated — list main entry points, config, tool definitions]

## SOPs

[To be populated — add procedure files here as the skill is documented]
```

### skills/casebook/billing-mcp/index.md

```markdown
# Casebook Billing MCP

> **Repo:** `/Users/benbelanger/GitHub/casebook-billing-mcp`
> This directory is the skills/documentation layer for the Casebook Billing MCP server.

---

## What It Does

[To be populated — describe the billing MCP's purpose and tools]

## Key Files (in repo)

[To be populated — list main entry points, config, tool definitions]

## SOPs

[To be populated — add procedure files here as the skill is documented]
```

---

## Task 5: Create skills/casebook/index.md

```markdown
# Skill: Casebook

> All Casebook-related skills, reference documentation, and MCP context.
> Last updated: [YYYY-MM-DD]

---

## Subdirectories

| Directory | Contents |
| :--- | :--- |
| `reporting/` | Reveal BI reference docs, entity schemas (cases, intake, people, tenants, users) |
| `admin-mcp/` | Casebook Admin MCP — skill docs and SOPs |
| `billing-mcp/` | Casebook Billing MCP — skill docs and SOPs |

---

## MCP Repos (external)

| Skill | Repo path |
| :--- | :--- |
| Admin MCP | `/Users/benbelanger/GitHub/casebook-admin-mcp` |
| Billing MCP | `/Users/benbelanger/GitHub/casebook-billing-mcp` |
```

---

## Task 6: Create skills/casebook/changelog.md

```markdown
# Casebook Changelog

> Detail log for `skills/casebook/`. See root `changelog.md` for version history.
> Use `write_changelog_entry` to append — never overwrite this file.

---

## [Unreleased]

---

## [1.0.0] - Casebook Skill Consolidated (YYYY-MM-DD)

**Changes:**
- `skills/casebook-reporting/` moved to `skills/casebook/reporting/`
- `skills/casebook/admin-mcp/` created — stub for casebook-admin-mcp docs
- `skills/casebook/billing-mcp/` created — stub for casebook-billing-mcp docs
- `skills/casebook/index.md` created — TOC for all Casebook skill content

**TODOs:**
1. Populate `admin-mcp/index.md` with tool descriptions and SOPs
2. Populate `billing-mcp/index.md` with tool descriptions and SOPs
```

---

## Task 7: Update AGENTS.md Vault Structure Tree

**Read first:** `AGENTS.md`

Replace `casebook-reporting/` in the skills tree with the new structure:

```
skills/
    ├── casebook/
    │   ├── index.md
    │   ├── changelog.md
    │   ├── reporting/       ← Reveal BI + entity reference docs
    │   ├── admin-mcp/       ← Casebook Admin MCP skill docs
    │   └── billing-mcp/     ← Casebook Billing MCP skill docs
```

---

## Task 8: Update skills/index.md

**Read first:** `skills/index.md`

If it references `casebook-reporting/`, update to `casebook/`. If it doesn't
reference it at all, no change needed.

---

## Task 9: Final Audit and Completion Report

1. `list_directory` on `skills/casebook/` — confirm structure
2. `list_directory` on `skills/casebook/reporting/` — confirm all 9 files present
3. Confirm `skills/casebook-reporting/` no longer exists
4. Read `AGENTS.md` — confirm vault tree updated
5. Read `skills/casebook/index.md` — confirm TOC accurate

Output:

```
## Completion Report — Consolidate Casebook v1.0

**Files moved (git mv):**
- [from] → [to]

**Files created:**
- [full path] — [description]

**Files modified:**
- [full path] — [what changed]

**Flags for Ben:**
- [anything unexpected found in casebook-admin-mcp or casebook-billing-mcp]

**Not completed / blockers:**
- [anything that could not be done and why]
```

---

## Notes for This Agent

- Use `git mv` for all moves — never copy-delete, history must be preserved
- The two MCP repos (`casebook-admin-mcp`, `casebook-billing-mcp`) are
  independent git repos — do not move their code, only create documentation
  stubs inside `skills/casebook/`
- Read before every write — no exceptions
- Follow all Read → Write rules from `AGENTS.md`
- Use the `write_changelog_entry` tool for the final changelog entry
