# Implementation Plan: kucera-orchestrator-scaffold

> **Prepared by:** Antigravity (Gemini) (2026-04-12)
> **Assigned to:** Claude Code
> **Vault root:** /Users/benbelanger/GitHub/ben-cp
> **Priority:** P1
> **v1.2**
> **STATUS: ✅ COMPLETE — 2026-04-12**

Successfully deployed structured `report_spec.json` definitions uniformly across the vault enabling decentralized routing requests by agent cadence. Engineered `skills/dream/run.py` to seamlessly execute a `glob` loop ingesting all specs natively, sequencing agents via an explicit numerical constraints mapping, logging mock terminal outputs internally via character logic envelopes, and compiling both `.md` and `.html` datestamped output versions of Daily Progress Digest cleanly into the target outputs directory.

**Changelog:** (see root changelog.md)


---

## Context
The architecture for `Daily Progress Digest` (Dream Cycles v1) has been approved. We need to build the orchestrator script that runs the agents in sequence and formats their outputs into a daily newspaper layout (HTML/MD).

## Architectural Vision (expanded 2026-04-12)
> **Contributed by:** Claude (Cowork) (2026-04-12)

The core principle: **every skill is independently runnable by any LLM**, but each skill declares a preferred agent for its daily report. Digest Editor reads those declarations dynamically — the agent roster is not hardcoded in `run.py`.

Character names (e.g. Changelog Auditor, Robert, Baton) belong exclusively in `character.md` files. All orchestration logic, routing tables, and skill references use the generic skill name only.

### Agent-to-Skill Routing
Each skill should ship with a `report_spec.json` (or equivalent frontmatter in `SKILL.md`) that declares:
- `preferred_agent`: which agent ideally picks this up
- `output_schema`: the envelope shape Digest Editor expects back
- `cadence`: daily / weekly / on-change

**Rough routing intent:**
| Skill | Preferred Agent |
|---|---|
| synthesis | Claude (Cowork) |
| knowledge | Gemini (Antigravity) |
| changelog | Gemma |
| dream | Digest Editor — orchestration only, no content generation |

Digest Editor's job is to: read each skill's `report_spec.json` → invoke the preferred agent → collect outputs → compile the Digest → publish for the next day's agents to learn from.

### The Daily Cycle
```
[Each skill's run.py] → structured JSON output
        ↓
[dream / Digest Editor] reads report_specs, invokes agents in order
        ↓
Compiles Digest (HTML + MD)
        ↓
Publishes to vault as tomorrow's context artifact
        ↓
Next day's agents read yesterday's Digest on startup
```

### Output Envelope (shared contract)
All agent `run.py` outputs should conform to:
```json
{
  "agent": "<agent name>",
  "skill": "<skill name>",
  "run_at": "<iso8601>",
  "status": "ok | warn | error",
  "summary": "<character-voiced summary — this is what hits the Digest>",
  "findings": [],
  "flags": []
}
```
Character voice lives in `summary` only. Machine-readable data stays in `findings`/`flags`.

## Execution Order
1. **Define `report_spec.json` schema** — establish the shared spec format all skills will use to declare preferred agent, output schema, and cadence.
2. **Scaffold `skills/dream/run.py`**: Create the Python script. Digest Editor reads all skill `report_spec.json` files to build the run order dynamically.
3. **Digest Editor Logic**: Implement orchestration. Run order driven by `report_spec.json` declarations, not hardcoded skill or character names.
4. **Format**: Compile returned envelopes into valid HTML and Markdown — "Front Page" (summary of summaries) + per-skill subsections.
5. **Publish**: Write Digest output to a datestamped vault artifact that agents can read on next startup.
6. **Mock Execution**: For v1, since individual skills lack full Python wrappers, `run.py` should `print` mock outputs per skill to test `launchd` and Digest formatting end-to-end.
