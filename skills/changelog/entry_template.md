# Changelog Entry Templates

Two templates — one per level. Start with the subdirectory entry, then write
the root entry. The root entry summarizes and points back to the subdirectory.

---

## Subdirectory Entry (`skills/[name]/changelog.md`)

Prepend below `## [Unreleased]` in the relevant subdirectory changelog.
Full granularity — exact paths, exact values, specific blockers.

```markdown
## [YYYY-MM-DD] — [Short Title]

**Files changed:**
- `skills/[name]/file.md` — [what changed, one line]
- `skills/[name]/file.md` — [what changed, one line]

**KR State:** _(okr-reporting only — omit otherwise)_
- [KR name]: [old status] → [new status] ([exact value if applicable])

**Blockers:**
- [description] — [what's needed to unblock]
_(omit if none)_

**Next:** [what to do in this subdirectory next session — specific enough to act without asking]
```

---

## Root Entry (`changelog.md`)

Prepend below `## [Unreleased]` in root `changelog.md`.
High-level summary only — readers go to subdirectory changelogs for detail.

```markdown
## [X.Y.Z] — [Short Title] ([YYYY-MM-DD])

**Changes:**
- `skills/[name]/` — [one-line summary] (see `skills/[name]/changelog.md`)
- `skills/[name]/` — [one-line summary] (see `skills/[name]/changelog.md`)
_(structural changes at vault level, if any)_

**Blockers:**
- [description] — [what's needed to unblock]
_(omit if none)_

**Next Tasks:**
1. [vault-level task — enough context to act]
2. [vault-level task]
```
