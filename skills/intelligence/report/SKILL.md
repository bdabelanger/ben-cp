---
name: dream
description: Nightly report orchestrator. Runs all skill agents in sequence (draft, revision, editorial, assembly) and compiles a curated daily report. Display framing is loaded from character.md at runtime — the skill itself is persona-agnostic.
preferred_agent: kucera
cadence: daily
report: no
---

# Skill: Dream (Orchestrator)

> **Purpose:** Orchestrate the nightly skill cycle — invoke each skill's preferred agent, collect structured output envelopes, apply an editorial pass, and publish a curated daily report.
> **Preferred Agent:** Digest Editor (see `character.md`)
> **Does not produce its own skill report** — it assembles the reports of all other skills.
> Last updated: 2026-04-12

---

## How It Works

The dream skill runs `run.py` nightly. It has four phases:

| Phase | What happens |
| :--- | :--- |
| **Draft** | Each skill's preferred agent produces an independent report envelope |
| **Revision** | Each agent receives the full draft pool and may revise its envelope |
| **Editorial** | The orchestrator reduces each envelope to a brief excerpt, preserving the agent's voice via direct quotes |
| **Assembly** | Excerpts are compiled into the daily report (MD + HTML) and published to `outputs/` |

---

## Display Framing

All report titles, bylines, section names, output filenames, and footer text are loaded from `character.md` at runtime via the `## Report Config` JSON block. The script `run.py` contains no hardcoded display strings. To change the report's look, feel, or naming — edit `character.md`, not `run.py`.

---

## Skill Discovery

The dream skill discovers which skills to run by reading all `report_spec.json` files in the `skills/` tree. Each skill that wants to participate in the nightly cycle must have a `report_spec.json` declaring:
- `skill_name` — identifier
- `preferred_agent` — which agent runs this skill
- `cadence` — `daily` or `weekly`
- `run_order` — integer sort order for the cycle

---

## Output

Daily reports are written to `skills/dream/outputs/` as both `.md` and `.html`. Filename prefix is set by `character.md`. Existing files are automatically archived to `outputs/archive/` before overwriting.

---

## Running

```bash
# Normal nightly run
python skills/dream/run.py

# Dry run — prints to stdout, no files written
python skills/dream/run.py --dry-run

# Override date
python skills/dream/run.py --date 2026-04-11
```

---

## Constraints

- `run.py` must remain persona-agnostic — no hardcoded character names, report titles, or framing
- All display strings come from `character.md` Report Config block
- Character names are not used outside of `character.md`
- Never auto-fixes vault issues — flags only, via handoffs
