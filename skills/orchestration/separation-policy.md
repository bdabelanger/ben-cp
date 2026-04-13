# Vault Separation Policy

> Effective: 2026-04-12
> Authority: AGENTS.md § Directory Boundaries

---

## The Five Layers

| Layer | Lives in | Contents |
| :--- | :--- | :--- |
| Skill logic | `skills/` | `SKILL.md`, `character.md`, `index.md`, `changelog.md`, templates, report specs — anything defining *how* a skill works |
| Execution tooling | `tools/` | Scripts, pipeline runners, and automation harnesses that *execute* a skill's procedure |
| Live data / WIP | `inputs/` | Raw API responses, processed JSON, `manifest.json` — anything produced *during* a run |
| Outputs | `outputs/` | Final reports, HTML, archives — anything *produced by* a run |
| Vault source of truth | `intelligence/` | Logic stubs, status rules, domain knowledge, schema reference — gitignored optional |

---

## What Belongs in `skills/`

- `SKILL.md` — skill contract and execution instructions
- `character.md` — voice, persona, and output structure (user-customization surface)
- `index.md` — structural directory index
- `changelog.md` — skill revision history
- `report.md`, `report_spec.json` — output format definitions
- `audit.md` — static audit criteria or checklists
- `data_sources.md` — reference doc for data source inventory
- `procedure.md` — evergreen runbooks
- Templates and static reference markdown

---

## What Does Not Belong in `skills/`

| File type | Rationale | Correct location |
| :--- | :--- | :--- |
| `*.py`, `*.sh` scripts | Execution tooling, not skill definition | `tools/` |
| `manifest.json` | Pipeline state (live data) | `inputs/` |
| Raw or processed JSON data files | Live run data | `inputs/` |
| Archived reports (`.html`, `.md` run outputs) | Run artifacts | `outputs/` |
| Execution logs | Run artifacts | `outputs/` |
| Ephemeral `notes.md` session files | Transient WIP — must be deleted after changelog | Delete post-session |

`skills/` must be a version-controlled toolset that can be iterated independently of any particular run's data. Files that change with every execution pollute the skill layer and make diffs noisy and meaningless.

---

## The `character.md` Contract

`character.md` is the user-customization surface for a skill: it controls voice, output structure, and persona. It belongs exclusively inside its skill directory.

`SKILL.md` invokes `character.md` by reference only — it never embeds character content inline. `character.md` never embeds `SKILL.md` content. Neither file owns the other's domain.

---

## Known Migration Debt

> Last updated: 2026-04-12. Items marked ✅ are resolved.

### Scripts and Executables in `skills/`

- ✅ `skills/product/status-reports/scripts/` — migrated to `tools/status-reports/scripts/` (2026-04-12)
- ✅ `skills/product/status-reports/run_pipeline.sh` — migrated to `tools/status-reports/` (2026-04-12)
- ✅ `skills/product/status-reports/tests/` — migrated to `tools/status-reports/tests/` (2026-04-12)
- `skills/intelligence/report/run.py` — execution script (→ `tools/intelligence-report/`)

### Live Data in `skills/`

- ✅ `skills/product/status-reports/inputs/` — migrated to `inputs/status-reports/` (2026-04-12)
- ✅ `skills/product/status-reports/manifest.json` — migrated to `inputs/status-reports/manifest.json` (2026-04-12)
- ✅ `skills/product/status-reports/logs/` — migrated to `outputs/status-reports/logs/` (2026-04-12)

### Structural Bugs

- `skills/product/shared/shared/vault.css` — double-nesting artifact; `product/shared/shared/` is a spurious extra directory layer (→ remove duplicate; `vault.css` canonical copy lives at `skills/styles/vault.css`)

### Stale Ephemeral Session Files

Per AGENTS.md §notes.md Write Policy, session `notes.md` files must be deleted after changelog is written. The following are still present:

- `skills/product/notes.md`
- `skills/orchestration/communication/notes.md`
- `skills/orchestration/changelog/notes.md`
- `skills/orchestration/access/notes.md`
- `skills/intelligence/analysis/synthesize/notes.md`
- `skills/intelligence/analysis/predict/notes.md`
- `skills/intelligence/memory/notes.md`
