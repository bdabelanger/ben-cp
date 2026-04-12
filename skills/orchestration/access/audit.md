# Audit Requirements: Access Domain

> **Owner:** Roz (Access Auditor)

## Requirements
- [ ] No credential patterns (keys, tokens) in session logs.
- [ ] Check `outputs/access/` for report consistency.
- [ ] Flag any multi-agent session where a PII-scrub was not verified.
- [ ] **Supply Chain Audit:** Scan `node_modules/` for extraneous packages (not in `package.json`).
- [ ] **Resource Audit:** Flag any file >1MB that is not a database.

## Audit Procedure
1. Scan `outputs/` for accidental git-tracked secrets.
2. Read `package.json` vs `node_modules/` to identify unlisted dependencies.
3. Read `skills/access/SKILL.md` to ensure procedure hasn't drifted.
