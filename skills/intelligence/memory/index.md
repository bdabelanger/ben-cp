# Memory Domain Index

> **Purpose:** Long-term storage, mapping logic, and active vault intelligence.
> **Last updated:** 2026-04-12

---

## 🏛️ Contents

| Sub-skill | Agent | Purpose |
| :--- | :--- | :--- |
| [`learn/`](learn/SKILL.md) | Vault Auditor | Tool for writing to long-term memory (indexing Digest/notes) |
| [`recall/`](recall/SKILL.md) | Vault Auditor | Tool for context retrieval and pattern matching |
| [`mapping/`](mapping/status_mapping.md) | Vault Auditor | Store for structural logic and health rulebaselines |
| [`watchdog/`](watchdog/SKILL.md) | Vault Auditor | Weekly structural hygiene and drift audit (legacy Vault Auditor) |

---

## 🔗 Architecture

The Memory Store is the vault's central repository of truth. 
- **Mapping** defines how data is interpreted.
- **Learn** ensures recent context becomes permanent intelligence.
- **Recall** provides a single point of entry for past information.
- **Watchdog** ensures the file structure remains valid.

All agents MUST respect the Memory Store as the final source of structural and logical truth.
