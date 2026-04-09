# Procedure: Robert Diff Checker

This procedure enables Robert to identify structural or philosophical drift in `AGENTS.md`.

## Prerequisites

- Shell access with `git` available.
- Read access to `AGENTS.md`.

## Steps

1. **Identify Recent History:**
   Run `git log --oneline -10 -- AGENTS.md` to see the most recent changes.

2. **Extract Diffs:**
   Run `git diff HEAD~5 -- AGENTS.md` to see changes across the last five commits (adjust number as needed to cover the recent un-audited history).

3. **Read Current State:**
   Perform a full read of `AGENTS.md`. Focus specifically on:
   - The **Agent's Creed** (Section 1).
   - **Universal Rules** (Section 5/6).
   - **Agent Dispatch** (Section 3).

4. **Compare and Formulate Report:**
   Look for the following "Drift Markers":
   - Modifications to the poem/mission statement in the Creek section.
   - Deletions of Universal Rules (especially Read → Write).
   - Changes to the Agent Table without a corresponding changelog entry.
   - Major structural shifting of files without Ben's recorded approval.

5. **Report Result:**
   Output a factual report in the current session.

## Report Format

```markdown
# Robert: Mission Integrity Audit (YYYY-MM-DD)

- **Audit Target:** AGENTS.md
- **Drift Detected:** [YES/NO]
- **Confidence:** [HIGH/MEDIUM/LOW]

## Observations
- [Factual point 1]
- [Factual point 2]

## Recommendation
- [None / Flag for Ben / Escalate]
```
