# Transcripts Changelog

## [Unreleased]

## 2026-04-28 — Improve Transcripts Skill — Rich Meeting Support + capture_task Clarification

**Files changed:**
- `skills/tasks/SKILL.md` — Created SKILL.md to document the capture_task MCP tool and its routing logic. done
- `src/ben-cp.ts` — Updated capture_task schema to support optional fields (ACs, Figma, project override) and updated getPopulatedTemplate to make fields conditional. done
- `skills/transcripts/scripts/run.py` — Added --mode rich flag, heuristic context extraction, and improved routing hints based on description content. done
- `skills/transcripts/SKILL.md` — Updated to reflect rich mode and context extraction capabilities. done

**Next:** Run harvester on a real meeting transcript to verify context extraction quality.

