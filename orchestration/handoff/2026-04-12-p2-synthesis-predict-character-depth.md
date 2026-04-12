# Implementation Plan: synthesis-predict-character-depth

> **Prepared by:** Antigravity (Gemini) (2026-04-12)
> **Assigned to:** Claude (Cowork)
> **Vault root:** /Users/benbelanger/GitHub/ben-cp
> **Priority:** P2
> **v1.0**
> **STATUS: 🔲 READY — pick up 2026-04-12**

---

# Implementation Plan: synthesis-predict-character-depth

> **Prepared by:** Antigravity (Gemini) (2026-04-12)
> **Assigned to:** Claude (Cowork)
> **Vault root:** /Users/benbelanger/GitHub/ben-cp
> **Priority:** P2

---

## Context
Robert (Synthesis) and Bryan (Predict) now have their structural scaffolding in place (`SKILL.md`, `report.md`, `index.md`, `report_spec.json`). The next step is to deeply flesh out their **character identities** and the **SKILL.md** for Robert — both require a richer understanding of who they are.

## Robert (Synthesis) — Character Context
Robert is based on:
- **human user's uncle** (specific voice and warmth — ask human user for more detail if needed)
- **Robert Frost** — spare, imagistic, precision of language, finding the profound in the ordinary
- **Robert Burns** — grounded, human-scale, a little rough around the edges, burns with feeling

His report output is explicitly **artistic**. He is not producing a structured bullet-point summary. He is writing prose that *means* something. Digest Editor will select from it editorially.

### What Claude needs to do:
1. Write `skills/synthesis/SKILL.md` — full behavioral procedure mirroring the same pattern as `predict/SKILL.md`, but tuned for Robert's literary, synthesis-focused role.
2. Deepen `skills/synthesis/character.md` with the Robert Frost/Burns/uncle trifecta voice. Give him mannerisms, tendencies, a writing style guide.

## Bryan (Predict) — Character Context
Bryan mirrors Robert's free-range philosophy but through a forecasting lens. His voice should be:
- Sharp and confident, not hedgy
- Data-informed but not robotic — he trusts his gut *and* the numbers
- Useful first, interesting second

### What Claude needs to do:
1. Deepen `skills/predict/character.md` to establish Bryan's voice fully.

## Approval Required
Both `character.md` updates and the new `synthesis/SKILL.md` must be reviewed by human user before being considered canonical.
