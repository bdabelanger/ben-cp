# Dream Changelog

> Detail log for `skills/dream/`. See root `changelog.md` for version history.

---

## [Unreleased]

## 2026-04-12 — Vault Path Normalization: Unified Intelligence Domain

**Files changed:**
- `skills/intelligence/report/run.py` — Updated skill discovery logic to deduplicate symlink overlaps and filter out redundant execution paths. ✅ Complete
- `skills/intelligence/report/SKILL.md` — Updated domain references to point to the new **intelligence/** stem. ✅ Complete

## 2026-04-12 — Strip all Digest/Digest Editor framing from run.py — move all display strings to character.md Report Config block, run.py is now fully persona-agnostic.

**Files changed:**
- `/Users/benbelanger/GitHub/ben-cp/skills/dream/run.py` — Full rewrite — removed all hardcoded character names, report titles, section headers, output filenames, and print strings. All display strings now loaded from character.md at runtime via load_character(). Mock data keyed on skill names not character names. Functions renamed to generic equivalents (build_report_markdown, write_lede, process_editorial_phase, etc). ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/dream/character.md` — Added ## Report Config JSON block with all display strings: report_title, byline, editor_label, lede_section, columns_section, output_prefix, footer, editorial_note. These are the single source of truth for all Digest framing. ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/dream/SKILL.md` — Created — fully generic skill descriptor. Documents display framing contract, skill discovery via report_spec.json, output format, and run instructions. Constraint: run.py must remain persona-agnostic. ✅ Complete

**Next:** Execute P2 handoff: add missing index.md to predict/, changelog/lumberjack/ and archive agents/roz.md (dream/ now has SKILL.md)


## 2026-04-12 — Establish Digest Editor as editorial editor-in-chief — Digest is curated excerpts with agent voice, not full report aggregation.

**Files changed:**
- `/Users/benbelanger/GitHub/ben-cp/skills/dream/character.md` — Rewrote to establish Digest Editor's editorial principles: selects key details, quotes agents in their own voice, writes Front Page as original editorial read, brevity is a virtue ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/dream/run.py` — Added editorial phase between revision and assembly: editorialize() reduces full envelopes to sharp excerpts, preserves agent voice via direct quotes, write_front_page() produces original editorial read not a summary of summaries, HTML renders quotes as blockquotes ✅ Complete

**Next:** Execute P2 handoff: add missing index.md to dream/, predict/, changelog/lumberjack/ and archive agents/roz.md

