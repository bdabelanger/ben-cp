# Claude Code Implementation Plan: Fix data_sources.md Portal Gaps + AGENTS.md SKILL.md Exemption

> **Prepared by:** Claude (Cowork session, 2026-04-08)
> **Source:** Vault Auditor report `reports/knowledge-report-2026-04-08.md` flags 6.1, 6.2, 7.1 naming note
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **v1.0**
> **STATUS: ✅ COMPLETE — 2026-04-09**

`skills/okr-reporting/data_sources.md` updated: added "Database (Direct) — Portal KRs" section after SQL via Data team, and added `/portal` page view proxy row to the GA table with an engineering confirmation note. `AGENTS.md` updated with SKILL.md/AGENTS.md naming exemption in the File Naming section.

**Changelog:** 1.6.0 — 2026-04-09 (see root `changelog.md`)

---

## Context

Two small gaps flagged by Vault Auditor:

1. `skills/okr-reporting/data_sources.md` is missing two Portal-related sources
   referenced in `2026-q2-kr-reference.md`. These KRs are currently blocked but
   sources should be inventoried now.

2. `AGENTS.md` naming convention rules don't address `SKILL.md` files, which use
   all-caps rather than underscores. This should be documented as an explicit
   exemption to avoid future false positives in Vault Auditor Check 7.

---

## Execution Order

1. **Task 1** — Add Portal sources to `data_sources.md`
2. **Task 2** — Add SKILL.md naming exemption to `AGENTS.md`
3. **Task 3** — Final audit and completion report

---

## Task 1: Update data_sources.md

**Read first:** `skills/okr-reporting/data_sources.md`

Add a new **Database (Direct)** section after the existing SQL via Data team section:

```markdown
### Database (Direct) — Portal KRs
Delegated query via Data team. All three Portal KRs share the same architectural
blocker — they unblock together once the data model is confirmed.

| Table / Source | Used For | KR | Status |
| :--- | :--- | :--- | :--- |
| `external_user_invitations` | Invitation sent/accepted counts | Portal — Invitations Sent, Invitation Acceptance | 🛑 Blocked — data model unstable |
| Session data (TBD) | Person login confirmation | Portal — Invitation Acceptance | 🛑 Blocked |
```

Also add one row to the existing Google Analytics table:

```
| `/portal` page view (proxy) | Proxy — portal login confirmation (URL-based, not a formal GA event) | Portal — Invitation Acceptance |
```

Add a note after that row:
```
> ⚠️ Confirm with Engineering whether this is a trackable GA event or URL-only signal before using as a formal metric.
```

---

## Task 2: Update AGENTS.md — SKILL.md Naming Exemption

**Read first:** `AGENTS.md`

In the **File Naming** section, add one line after the existing naming rules:

```markdown
- `SKILL.md` and `AGENTS.md` are exempt from the underscore convention — all-caps
  filenames are valid for vault contracts and Cowork skill descriptors
```

---

## Task 3: Final Audit and Completion Report

1. Read `skills/okr-reporting/data_sources.md` — confirm Portal section and GA row added
2. Read `AGENTS.md` — confirm exemption line present in File Naming section
3. Write changelog entry using `write_changelog_entry`

```
## Completion Report

**Files modified:**
- skills/okr-reporting/data_sources.md — added Portal DB sources and /portal GA proxy
- AGENTS.md — added SKILL.md/AGENTS.md naming exemption to File Naming section

**Flags for Ben:** [anything unexpected]
```
