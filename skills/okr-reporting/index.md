# OKR Reporting Skill — Index

> This directory contains the measurement SOPs and runbooks for Platform OKR
> reporting. KR-specific SOPs follow the naming convention
> `[feature]_[metric_type].md`. Quarterly KR references follow
> `[year]-[quarter]-kr-reference.md` and rotate each quarter.
>
> **All agents:** read `AGENTS.md` at the vault root before modifying any file here.

---

## 📋 Contents

| File | Description |
| :--- | :--- |
| `procedure.md` | Evergreen runbook — baseline/target establishment steps (no quarterly content) |
| `data_sources.md` | Data source inventory for all Platform KRs |
| `2026-q2-kr-reference.md` | Q2 2026 — per-KR baseline status, confirmed values, targets, next steps |
| `changelog.md` | Detail log for this skill — all structural changes |

---

## 📐 File Type Guide

| Type | Naming convention | Lifecycle |
| :--- | :--- | :--- |
| Evergreen runbook | `procedure.md` | Never contains quarterly content |
| Quarterly KR reference | `[year]-[quarter]-kr-reference.md` | Archived at quarter end; new file created |
| KR measurement SOP | `[feature]_[metric_type].md` | Evergreen; updated as instrumentation changes |
| Data inventory | `data_sources.md` | Evergreen; updated as new sources confirmed |

---

## 🔗 References

- Universal agent contract: `/Users/benbelanger/GitHub/ben-cp/AGENTS.md`
- Status logic: `/Users/benbelanger/GitHub/ben-cp/skills/skill-builder/mappings/status_mapping.md`
- Visual standards: `/Users/benbelanger/GitHub/ben-cp/skills/skill-builder/styles/emoji_key.md`
