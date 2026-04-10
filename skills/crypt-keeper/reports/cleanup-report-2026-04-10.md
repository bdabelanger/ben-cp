# Crypt-Keeper Report — 2026-04-10

| Check | Result |
| :--- | :--- |
| 1 — Orphaned Files | ⚠️ 1 flag |
| 2 — Misplaced Files | ✅ Clean |
| 3 — Missing index.md | ✅ Clean |
| 4 — Duplicate Files | ⚠️ 1 flag |
| 5 — Stale Status Flags | ✅ 5 monitored (none stale) |
| 6 — data_sources.md Sync | ⚠️ 2 flags |
| 7 — AGENTS.md Compliance | ⚠️ 1 flag (Convention) |

---

## Flags

### 1 — Orphaned Files
- **File:** `skills/okr-reporting/q2-2026/planning-services-at-scale/notes_quick_entry.md`
- **Issue:** File exists but is not listed in `skills/okr-reporting/q2-2026/planning-services-at-scale/index.md`.
- **Recommendation:** Add to the contents table in the local index.

### 4 — Duplicate / Near-Duplicate Files
- **Files:** `skills/crypt-keeper/SKILL.md` vs `skills/crypt-keeper/procedure.md`
- **Issue:** High redundancy. `SKILL.md` is the MCP entry point but duplicates much of the SOP text.
- **Recommendation:** Consolidate `procedure.md` content into `SKILL.md` or have one point to the other.

### 6 — data_sources.md Sync
- **Flag A:** `TrackServiceNoteNew` event mentioned in `notes_quick_entry.md` is missing from the `data_sources.md` inventory.
- **Flag B:** `Notes Datagrid Shortcuts` SOP (`planning-services-at-scale/notes_datagrid_shortcuts.md`) is entirely missing from the master indicator list in `data_sources.md`.

### 7 — AGENTS.md Compliance (Spot-Check)
- **Violation:** `handoff/` filenames use hyphens (e.g., `2026-04-10-p2-quartermaster-convention.md`).
- **Context:** `AGENTS.md` Section 4 prescribes underscores for word separation.
- **Recommendation:** Clarify if `handoff/` is exempt or migrate to underscores.

---

## Suggested Actions
- [ ] Create P1 handoff for orphaned index entry.
- [ ] Create P3 handoff for `data_sources.md` sync gaps.
- [ ] Create P2 handoff for structural convention alignment (hyphens in handoffs).
