#!/usr/bin/env python3
"""
transcripts/scripts/run.py — Parse Gemini transcript/email → Cowork handoff

Parses the "Suggested next steps" section of a Gemini transcript or email,
classifies each action item, and writes a handoff for Cowork to run
the task-capture skill with Ben in an interactive session.

Usage:
    python3 run.py --email /path/to/notes.txt [--date "Apr 27, 2026"] [--mode rich|standup]
"""
import os, sys, re, json, argparse, textwrap
from datetime import datetime

SCRIPT_DIR     = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT     = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
PEOPLE_PATH    = os.path.join(SCRIPT_DIR, "..", "schemas", "people.json")
HANDOFFS_DIR   = os.path.join(REPO_ROOT, "handoffs")

BEN_NAME = "Ben"

# ---------------------------------------------------------------------------
# People cache
# ---------------------------------------------------------------------------

def load_people():
    with open(PEOPLE_PATH) as f:
        return json.load(f)

# ---------------------------------------------------------------------------
# Email parsing
# ---------------------------------------------------------------------------

NEXT_STEPS_PATTERN = re.compile(
    r'(?:Suggested next steps|Next steps)[:\s]*\n(.*?)(?:\n\s*\n[A-Z\[]|\Z)',
    re.IGNORECASE | re.DOTALL
)
ITEM_PATTERN = re.compile(
    r'^\s*[-•]?\s*\[([^\]]+)\]\s+([^:]+):\s+(.+)',
    re.MULTILINE
)
JIRA_KEY_PATTERN = re.compile(r'\b(?:ticket|PR|issue|CBP-)?(\d{4,})\b', re.IGNORECASE)
CBP_KEY_PATTERN  = re.compile(r'\bCBP-(\d+)\b', re.IGNORECASE)

def parse_transcript(text, mode="standup"):
    """Extract action items and context from Gemini transcript/email."""
    match = NEXT_STEPS_PATTERN.search(text)
    section = match.group(1) if match else text

    items = []
    for m in ITEM_PATTERN.finditer(section):
        raw_assignees = m.group(1)
        action_label  = m.group(2).strip()
        description   = m.group(3).strip()
        assignees     = [a.strip() for a in raw_assignees.split(",")]

        # Extract bare ticket numbers as CBP references
        bare_numbers = JIRA_KEY_PATTERN.findall(description + " " + action_label)
        explicit_keys = CBP_KEY_PATTERN.findall(description + " " + action_label)
        jira_refs = list({f"CBP-{n}" for n in bare_numbers + explicit_keys})

        context = ""
        if mode == "rich":
            try:
                search_term = description[:50]
                idx = text.find(search_term)
                if idx != -1:
                    start_ctx = max(0, text.rfind('\n', 0, idx - 1))
                    end_ctx = text.find('\n', idx + len(description) + 100)
                    if end_ctx == -1: end_ctx = len(text)
                    context = text[start_ctx:end_ctx].strip()
                    context = "\n".join([line.strip() for line in context.split('\n') if line.strip()][:10])
            except:
                pass

        items.append({
            "assignees":    assignees,
            "action_label": action_label,
            "description":  description,
            "jira_refs":    sorted(jira_refs),
            "context":      context
        })

    return items

# ---------------------------------------------------------------------------
# Classification (for routing hints in the handoff)
# ---------------------------------------------------------------------------

BUG_SIGNALS  = re.compile(r'\b(bug|regression|broken|error|fix|issue|broken)\b', re.I)
PR_SIGNALS   = re.compile(r'\b(pr|merge|implement|deploy|build)\b', re.I)
PM_SIGNALS   = re.compile(r'\b(review|clarif|coordinat|notify|check|demo|send|file|initiat|request|confirm|verify|tiebreak|decision)\b', re.I)

def classify_hint(item, people):
    """Return a routing hint string for the handoff."""
    assignees    = item["assignees"]
    description  = item["description"] + " " + item["action_label"]
    is_group     = len(assignees) == 1 and assignees[0].lower() in ("the group", "group")

    if is_group:
        return "Asana → Ben (group item, triage)"

    roles = []
    for name in assignees:
        name_lower = name.lower()
        for cached_name, info in people.items():
            if cached_name.lower() == name_lower or name_lower.startswith(cached_name.lower()):
                roles.append(info.get("role", ""))
                break

    any_dev = any("dev" in r for r in roles if r)

    if BUG_SIGNALS.search(description):
        dest = "Jira Bug"
        if any_dev and len(assignees) == 1:
            dest += f" → {assignees[0]}"
        return dest

    if any_dev and PR_SIGNALS.search(description):
        dest = "Jira Task"
        if len(assignees) == 1:
            dest += f" → {assignees[0]}"
        return dest

    if PM_SIGNALS.search(description) or not any_dev:
        if "note" in description.lower(): return "Asana → Ben (Notes)"
        if "enroll" in description.lower(): return "Asana → Ben (Service Plan)"
        return f"Asana → Ben"

    return "Asana → Ben (default)"

# ---------------------------------------------------------------------------
# Handoff generation
# ---------------------------------------------------------------------------

def write_handoff(items, meeting_date, people, meeting_mode="standup"):
    today = datetime.now().strftime("%Y-%m-%d")
    month_day = datetime.now().strftime("%b-%-d").replace(" ", "-")
    filename = f"{today}-p2-Transcript-Harvest-{month_day}.md"
    filepath = os.path.join(HANDOFFS_DIR, filename)

    lines = [
        "---",
        f"title: Transcript Harvest — {meeting_date}",
        "priority: P2",
        "assigned_to: Cowork",
        "status: READY",
        f"date: {today}",
        "---",
        "",
        f"# Transcript Harvest — {meeting_date}",
        "",
        f"> **Prepared by:** Code (transcript) ({today})",
        f"> **Assigned to:** Cowork (Sonnet 4.6)",
        f"> **Priority:** P2",
        f"> **STATUS**: 🔲 READY — pick up {today}",
        "",
        "---",
        "",
        "## Context",
        "",
        f"Gemini notes from {meeting_date} have been parsed in **{meeting_mode}** mode.",
        "The action items below need to be captured as tasks. Work through them with Ben — present each item, confirm routing, and fire off creation.",
        "",
        "---",
        "",
        "## Action Items",
        "",
    ]

    for i, item in enumerate(items, 1):
        assignees_str = ", ".join(item["assignees"])
        action        = item["action_label"]
        description   = item["description"]
        jira_refs     = ", ".join(item["jira_refs"]) if item["jira_refs"] else "—"
        hint          = classify_hint(item, people)

        lines += [
            f"### {i}. {action}: {description}",
            f"- **Assignee(s)**: {assignees_str}",
            f"- **Suggested Route**: {hint}",
            f"- **Jira Refs**: {jira_refs}",
        ]

        if item.get("context"):
            ctx_block = textwrap.indent(item["context"], "  > ")
            lines.append(f"- **Meeting Context**:\n{ctx_block}")

        lines.append("")

    lines += [
        "---",
        "",
        "## Execution Steps",
        "",
        "1. Read each action item above.",
        "2. For each item, present it to Ben with the suggested route.",
        "3. Confirm or adjust with Ben, then use the **task-capture skill** to create it.",
        "4. Work through all items in order. Ben can skip, defer, or adjust any item.",
        "5. Confirm concisely after each creation (key/GID + title).",
        "",
        "## Verification",
        "",
        "- [ ] All action items reviewed with Ben",
        f"- [ ] Tasks/issues created for all {len(items)} items (or explicitly deferred/skipped)",
        "",
    ]

    with open(filepath, "w") as f:
        f.write("\n".join(lines))

    return filename, filepath

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Transcript note harvester → handoff")
    parser.add_argument("--email", required=True, help="Path to email/transcript text file")
    parser.add_argument("--date",  help='Meeting date string, e.g. "Apr 27, 2026"')
    parser.add_argument("--mode",  choices=["standup", "rich"], default="standup", help="Processing mode")
    args = parser.parse_args()

    with open(args.email) as f:
        email_text = f.read()

    meeting_date = args.date or datetime.now().strftime("%b %-d, %Y")
    people = load_people()

    items = parse_transcript(email_text, args.mode)
    if not items:
        print("❌ No action items found. Check that the source text contains a '[Name] Action: Description' format.")
        sys.exit(1)

    print(f"📋 Parsed {len(items)} action items from {meeting_date} notes\n")
    for i, item in enumerate(items, 1):
        hint = classify_hint(item, people)
        assignees = ", ".join(item["assignees"])
        print(f"  {i}. [{assignees}] {item['action_label']}: {item['description'][:60]} → {hint}")

    filename, filepath = write_handoff(items, meeting_date, people, args.mode)

    print(f"\n✅ Handoff written: handoffs/{filename}")
    print(f"   Cowork will work through these with Ben using task-capture.")

if __name__ == "__main__":
    main()
