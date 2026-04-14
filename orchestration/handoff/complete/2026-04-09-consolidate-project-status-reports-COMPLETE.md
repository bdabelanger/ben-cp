# Claude Code Implementation Plan: Consolidate Project Status Reports Pipeline into skills/

> **Prepared by:** Claude (Cowork session, 2026-04-08)
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **v1.0**
> **STATUS: ✅ COMPLETE — 2026-04-09**

---

## Context

The project-status-reports pipeline currently lives in two places:

| Location | Contents | Type |
| :--- | :--- | :--- |
| `project-status-reports/` (vault root) | Python scripts, manifest.json, inputs/, outputs/, logs/, run_pipeline.sh | **Executable pipeline** |
| `skills/project-status-reports/` | index.md (runbook SOP), changelog.md, empty scripts/ and outputs/ dirs | **Documentation layer** |

These are one system — the SOP documents the pipeline, the pipeline executes it.
The goal is to consolidate everything under `skills/project-status-reports/`
so the skill is self-contained: runbook + code + changelog all in one place.

---

## Execution Order

Run tasks in sequence. Read before every write — no exceptions.

1. **Task 1** — Audit both directories in full
2. **Task 2** — Move pipeline files into `skills/project-status-reports/`
3. **Task 3** — Update run paths in `skills/project-status-reports/index.md`
4. **Task 4** — Remove empty root directory and stale scaffolding
5. **Task 5** — Update `AGENTS.md` vault structure tree
6. **Task 6** — Update `skills/project-status-reports/changelog.md`
7. **Task 7** — Final audit and completion report

---

## Task 1: Audit Both Directories

Read and list the full contents of both:
1. `list_directory` on `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/project-status-reports/`
2. `list_directory` on `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/project-status-reports/scripts/`
3. `list_directory` on `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/project-status-reports/`
4. `list_directory` on `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/project-status-reports/scripts/` (confirm empty)
5. `list_directory` on `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/project-status-reports/outputs/` (confirm empty)

Report any unexpected files before proceeding.

---

## Task 2: Move Pipeline Files

Move the following from `project-status-reports/` to `skills/project-status-reports/`:

| From | To |
| :--- | :--- |
| `project-status-reports/scripts/` (all .py files) | `skills/project-status-reports/scripts/` |
| `project-status-reports/manifest.json` | `skills/project-status-reports/manifest.json` |
| `project-status-reports/run_pipeline.sh` | `skills/project-status-reports/run_pipeline.sh` |
| `project-status-reports/inputs/` | `skills/project-status-reports/inputs/` |
| `project-status-reports/outputs/` | `skills/project-status-reports/outputs/` |
| `project-status-reports/logs/` | `skills/project-status-reports/logs/` |
| `project-status-reports/tests/` | `skills/project-status-reports/tests/` |

**Use `git mv` for all moves** — this preserves git history on the scripts.
Do not copy-and-delete; use git mv only.

---

## Task 3: Update Run Paths in index.md

**Read first:** `skills/project-status-reports/index.md`

The runbook references paths like:
```
python3 project-status-reports/scripts/full_run.py --force
```

These must be updated to reflect the new location. Replace all occurrences of:
```
project-status-reports/scripts/
```
with:
```
skills/project-status-reports/scripts/
```

Also update any other absolute or relative paths in the runbook that reference
the old `project-status-reports/` root location.

---

## Task 4: Remove Root Directory Scaffolding

After confirming all files have moved successfully:

1. Confirm `project-status-reports/` at vault root is now empty (or only contains
   `.DS_Store` / git artifacts)
2. Remove the empty root directory:
   ```
   git rm -r project-status-reports/
   ```
3. Also remove the now-redundant empty dirs from `skills/project-status-reports/`
   if they were pre-existing stubs with no content:
   - `skills/project-status-reports/scripts/` — only remove if it was empty before Task 2
   - `skills/project-status-reports/outputs/` — same

---

## Task 5: Update AGENTS.md Vault Structure Tree

**Read first:** `AGENTS.md`

Update the vault structure tree to remove `project-status-reports/` from the
root level and ensure `skills/project-status-reports/` reflects its full contents:

```
skills/
    ├── project-status-reports/
    │   ├── index.md              ← runbook SOP
    │   ├── changelog.md
    │   ├── manifest.json
    │   ├── run_pipeline.sh
    │   ├── scripts/              ← pipeline Python scripts
    │   ├── inputs/
    │   ├── outputs/
    │   ├── logs/
    │   └── tests/
```

---

## Task 6: Update skills/project-status-reports/changelog.md

**Read first:** `skills/project-status-reports/changelog.md`

Append a new entry documenting this consolidation:

```markdown
## [1.1.0] - Pipeline Consolidation (2026-04-09)

**Changes:**
- Pipeline moved from `project-status-reports/` (vault root) into this directory
- `scripts/`, `inputs/`, `outputs/`, `logs/`, `tests/`, `manifest.json`,
  `run_pipeline.sh` all now live under `skills/project-status-reports/`
- Run path updated in `index.md`: `skills/project-status-reports/scripts/full_run.py`
- Root `project-status-reports/` directory removed

**Rationale:** Skill is now self-contained — runbook, code, and changelog in one place.
```

---

## Task 7: Final Audit and Completion Report

1. `list_directory` on `skills/project-status-reports/` — confirm all files present
2. Confirm `project-status-reports/` no longer exists at vault root
3. Read `skills/project-status-reports/index.md` — confirm run paths updated
4. Read `AGENTS.md` — confirm vault tree updated

Output:

```
## Completion Report — Consolidate Project Status Reports v1.0

**Files moved (git mv):**
- [from] → [to]

**Files modified:**
- [full path] — [what changed]

**Flags for Ben:**
- [anything unexpected]

**Not completed / blockers:**
- [anything that could not be done and why]
```

---

## Notes for This Agent

- Use `git mv` for all file moves — never copy-delete, history must be preserved
- Read before every write — no exceptions
- Do not modify any `.py` script contents — move only
- If any script has a hardcoded path to `project-status-reports/` internally,
  flag it for human user rather than editing script logic
- Follow all Read → Write rules from `AGENTS.md`
