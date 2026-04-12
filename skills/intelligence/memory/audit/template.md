# Audit Requirements: [Skill Name]

> **Owner:** [Agent Name]
> **Domain:** [Skill Path]
> **Instruction:** The Vault Auditor reads this file to understand the specific "known details" and quality standards required for this skill.

---

## 📋 Security & Compliance
- [ ] List specific file permissions or access rules.
- [ ] List sensitive data markers to watch for.

## 🏗️ Structural Integrity
- [ ] Define mandatory file naming conventions.
- [ ] Define required directory structure.
- [ ] Check for linked presence in parent `index.md`.

## 🧠 Logic & Mappings
- [ ] Reference specific `mapping/` files that must be valid.
- [ ] Define expected output invariants for reports.

## ⏱️ Freshness
- [ ] Define expiration logic for stale stats or data.

---

## 🛠️ Audit Procedure
Describe how the Vault Auditor should validate these requirements (e.g., "Check all files in q2-2026/ for the presence of a target_value").
