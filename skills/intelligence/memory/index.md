# Memory Domain Index

> **Purpose:** Long-term storage, mapping logic, and active vault intelligence.
> **Last updated:** 2026-04-12

---

## 🏛️ Contents

| Sub-skill | Agent | Purpose |
| :--- | :--- | :--- |
| [`intake/`](intake/index.md) | Vault Auditor | Tool for writing to long-term memory (indexing findings) |
| [`retrieval/`](retrieval/index.md) | Vault Auditor | Tool for context retrieval and pattern matching |
| [`audit/`](audit/index.md) | Vault Auditor | Weekly structural hygiene and drift audit |

---

## 🗺️ Logic & Mapping
Structural logic and health rulebaselines are stored centrally in the intelligence domain:
- [**Status Mapping**](../../../intelligence/mapping/status_mapping.md)


---

## 🔗 Architecture

The Memory Store is the vault's central repository of truth. 
- **Mapping** defines how data is interpreted.
- **Learn** ensures recent context becomes permanent intelligence.
- **Recall** provides a single point of entry for past information.
- **Watchdog** ensures the file structure remains valid.

All agents MUST respect the Memory Store as the final source of structural and logical truth.
