# Crypt-Keeper — Vault Quality Watchdog

> **Purpose:** Crypt-Keeper is the scheduled vault hygiene agent for the ben-cp
> SOP vault. It runs weekly, catches structural drift introduced by any agent
> (Gemma, Gemini, Claude Code), and produces a flagged report for Ben's review.
> It never auto-fixes — it only flags.
>
> **All agents:** Read `AGENTS.md` at the vault root before modifying any file here.

---

## 📋 Contents

| File | Description |
| :--- | :--- |
| `index.md` | This file — overview and table of contents |
| `SKILL.md` | Cowork/scheduled task skill descriptor — entry point for automated runs |
| `procedure.md` | Full check spec — what Crypt-Keeper runs each session |
| `report-template.md` | Output template for cleanup reports |
| `changelog.md` | Detail log for this skill — all structural changes |
| `reports/` | Generated cleanup reports — current run + archive/ |

---

## 🔗 References

- Universal agent contract: `/Users/benbelanger/GitHub/ben-cp/AGENTS.md`
- Reports output directory: `/Users/benbelanger/GitHub/ben-cp/skills/crypt-keeper/reports/`
- Vault structure reference: `AGENTS.md` Section 1
