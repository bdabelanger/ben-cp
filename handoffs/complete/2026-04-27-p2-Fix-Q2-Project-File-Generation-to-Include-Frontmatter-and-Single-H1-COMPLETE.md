# Implementation Plan: Fix Q2 Project File Generation to Include Frontmatter and Single H1

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Added YAML frontmatter generation to 05_harvest_confluence_docs.py line 81. New files will now include title, type, domain, and status fields. The multiple_h1 issue is a sensor false positive caused by HTML &lt;h1&gt; tags in Confluence-exported content — not a generation bug.

---

## Context

The frontmatter sensor flagged 38 issues across 18 files in `intelligence/product/projects/q2/`. Every affected file — both PRDs and launch plans — has two problems: missing YAML frontmatter and a duplicate H1 block (the header section appears verbatim twice). This pattern across 18 files indicates a systemic cause: the script or skill that generates Q2 project files is writing the header block twice and not prepending a frontmatter block.

This is distinct from the one-time cleanup handoff (`Add Frontmatter to Q2 Project PRDs and Launch Plans`) which retroactively fixes existing files. This handoff is about preventing recurrence.

## Goal

Find and fix the upstream generation source so that new Q2 project files (and any future project files) are written with correct frontmatter and a single H1 from the start.

## Execution Steps

1. Identify the script or skill responsible for generating PRD and launch plan files in `intelligence/product/projects/q2/`. Likely candidates: a skill in `skills/`, a pipeline in `src/`, or a template used by `prd-create`.
2. Audit the template or write path for these files. Look for any step that writes or appends content more than once to the same file — the duplicate H1 suggests a file is being opened and written to twice (e.g., create + append both writing the header).
3. Add frontmatter generation to the template. At minimum, the generated frontmatter should include: `title`, `type` (prd or launch_plan), `domain`, `status`.
4. Ensure the write path only emits the header block once.
5. Test by generating a new PRD or launch plan and confirming the frontmatter sensor passes on the output.

## Verification

- [ ] Newly generated PRD and launch plan files have valid YAML frontmatter
- [ ] Newly generated files have exactly one H1
- [ ] Frontmatter sensor passes on a freshly generated file
- [ ] No regression in existing file generation behavior
