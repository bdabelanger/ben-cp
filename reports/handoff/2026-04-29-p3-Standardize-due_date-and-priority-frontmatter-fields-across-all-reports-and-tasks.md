# Implementation Plan: Standardize due_date and priority frontmatter fields across all reports and tasks

> **Prepared by:** Code (Gemini) (2026-04-29)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P3
> **STATUS**: 🔲 READY — pick up 2026-04-29

---

## Context
Local (Gemma) sorts and presents report items by urgency using `due_date` and `priority` fields. These fields are not consistently present or named across all reports and task outputs, requiring judgment calls that cause drift and inconsistency.

## Goal
Define and enforce a standard frontmatter schema for `due_date` and `priority` across all report types and task outputs so Local can sort and present items programmatically without interpretation.

## Scope
- Audit all current report templates under `reports/` and `skills/` for existing frontmatter patterns
- Propose a canonical field spec (field names, value formats, required vs optional)
- Update report templates and generation scripts to emit compliant frontmatter
- Document the standard in `governance/policies.md` or a new `governance/report-schema.md`

## Suggested field spec (starting point for Code to validate)
```yaml
priority: P1 | P2 | P3 | P4       # required
due_date: YYYY-MM-DD               # required where applicable
status: overdue | active | done    # optional, can be derived
```

## Done criteria
- [ ] Audit complete — all report types inventoried for current frontmatter usage
- [ ] Canonical field spec proposed and approved by human
- [ ] Report generation scripts updated to emit compliant fields
- [ ] Schema documented in governance

## Source
Conversation with Claude — 2026-04-28
