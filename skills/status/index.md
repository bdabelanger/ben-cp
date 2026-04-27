# Skill: Task Capture

> **Purpose:** Captures work items from raw notes and routes them into Asana or Jira with correct metadata, issue types, and templates.
> **Preferred Agent:** Claude (Cowork)
> **Cadence:** On-demand

---

## Overview

Task Capture classifies work items by type and destination, applies the correct template and metadata, creates the item in Asana and/or Jira, and confirms concisely. It encodes Ben's classification system, issue type mapping, Asana custom field GIDs, and Jira project conventions.

---

## Contents

| File | Description |
| :--- | :--- |
| `index.md` | This file — purpose, scope, usage |
| `SKILL.md` | Full routing logic, classification rules, metadata, confirmation steps |
| `schemas/` | Mappings and logic schemas (status_mapping.md) |
| `changelog.md` | Change history |

---

## Intelligence & Mapping

Reference data for this skill has been consolidated into the `intelligence/` domain:

| Item | Location |
| :--- | :--- |
| Data Sources Map | `intelligence/product/projects/data_sources.md` |
| Asana/Jira Templates | `intelligence/product/projects/source/` |

---

---

## Source of Truth Note

> **Cowork plugin:** This skill is mirrored in the Cowork runtime plugin (`task-capture/SKILL.md`). Update this vault version first; keep the plugin in sync manually until auto-sync is in place. The vault version is the canonical reference and edit target.
