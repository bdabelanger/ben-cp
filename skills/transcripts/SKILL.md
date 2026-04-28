---
title: Transcript Note Harvester — Gemini Notes → Cowork Handoff
type: skill
domain: skills/transcripts
---

# Transcript Note Harvester

> **Trigger:** "Harvest tasks from this transcript", "Process my notes from [date]", "Pull action items from the Discovery Review transcript", "Run transcript harvester in rich mode"
> **Agent:** Code (Claude)
> **Output:** A handoff in `handoffs/` for Cowork to run task-capture with Ben

---

## What it does

Reads a Gemini meeting transcript or standup email, parses the "Suggested next steps" section, classifies each action item with a routing hint, and writes a structured handoff. 

**Modes:**
- **standup** (default): Optimized for short standup emails.
- **rich**: Optimized for long meeting transcripts. Extracts surrounding discussion context for each action item to ensure high-fidelity task creation.

Cowork then picks up the handoff and works through each item interactively with Ben using the task-capture skill.

---

## Step 1 — Get the email

**Option A — Google MCP (preferred when available):**
Use the Gmail MCP to find the most recent email from `gemini-notes@google.com` with subject matching `"🧍 CBP - Standup"`. Extract the plain-text body.

**Option B — Ben pastes it:**
Ask Ben to paste the email body (or forward it). Save it to a temp file, e.g. `/tmp/standup-email.txt`.

---

## Step 2 — Run the harvester

```bash
python3 "skills/transcripts/scripts/run.py" \
  --email /tmp/transcript.txt \
  --date "Apr 27, 2026" \
  --mode rich
```

All paths relative to repo root:
`/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`

The `--date` flag is optional — defaults to today.
The `--mode` flag is optional — defaults to `standup`. Use `rich` for narrative transcripts.

---

## Step 3 — Confirm to Ben

The script will print a summary of parsed items and the handoff filename. Show Ben the list and confirm:

```
✅ Transcript harvested — Apr 27, 2026 (8 action items)
   Handoff ready for Cowork: handoffs/2026-04-27-p2-Transcript-Harvest-Apr-27.md
```

Cowork will pick it up and work through the items with Ben using task-capture.

---

## Email format reference

Gemini sends a consistent email after each standup. The section that matters:

```
Suggested next steps

[Ben] Review Ticket: Review ticket 2990 issues. Provide tiebreaker decision.
[Russell] Implement Deletable: Implement 'deletable' prop on compact attachment.
[The group] File Bug: File bug report regarding the link styling regression.
```

- Assignees in `[Square Brackets]` — comma-separated for multi-assignee
- `[The group]` = unassigned/team-wide → Asana task for Ben
- Action label before the colon is short verb phrase
- Bare ticket numbers (e.g. "ticket 2990") are extracted as CBP references

---

## People cache

`skills/transcripts/schemas/people.json` maps first names to roles. Used for routing hints only — no Jira/Asana lookups at harvest time.

---

## Troubleshooting

- **"No action items found"** — Check that the email has `[Name] Action: Description` lines. Paste the raw text to verify.
- **Wrong routing hint** — Hints are suggestions only; Cowork confirms with Ben before creating.
