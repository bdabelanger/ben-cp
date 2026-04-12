# Product Skills — Shared Data Sources

> **Scope:** Data sources shared across `status-reports/` and `okr-reporting/`.
> **Note:** Skill-specific data source configurations remain in each sub-skill's own files. This document covers sources used by both.

---

## Primary Shared Sources

| Source | Used By | Purpose |
| :--- | :--- | :--- |
| **Google Analytics (GA4)** | OKR Reporting, Status Reports | User behavior, event tracking, adoption metrics |
| **Casebook Admin / Reveal BI** | OKR Reporting | Transactional data: Service Notes, Enrollments, Denominators |
| **Asana** | Status Reports | Project and task tracking for weekly status generation |
| **ChurnZero / SQL** | OKR Reporting | Tenant segmentation and external validation |

---

## Data Integrity Notes

- **Event names** for all shortcut metrics must be confirmed via DevTools before final implementation.
- **Portal KRs** are currently blocked pending data model confirmation.
- **Jira** integration has been deprecated from Status Reports as of 2026-04 — Asana is now the sole source.

---

## Skill-Specific References

- OKR data source detail: `okr-reporting/data_sources.md`
- Status report inputs: `status-reports/inputs/`
