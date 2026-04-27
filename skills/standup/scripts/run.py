#!/usr/bin/env python3
"""
standup/scripts/run.py — Parse Gemini standup email → Cowork handoff

Parses the "Suggested next steps" section of a Gemini standup email,
classifies each action item, and writes a handoff for Cowork to run
the task-capture skill with Ben in an interactive session.

Usage:
    python3 run.py --email /path/to/email.txt [--date "Apr 27, 2026"]
"""
import os, sys, re, json, argparse
from datetime import datetime

SCRIPT_DIR     = os.path.dirname(os.path.abspath(__file__))
VAULT_ROOT     = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
PEOPLE_PATH    = os.path.join(SCRIPT_DIR, "..", "schemas", "people.json")
HANDOFFS_DIR   = os.path.join(VAULT_ROOT, "handoffs")
HANDOFFS_INDEX = os.path.join(HANDOFFS_DIR, "index.md")

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

def parse_email(text):
    """Extract action items from Gemini standup email body."""
    match = NEXT_STEPS_PATTERN.search(text)
    section = match.group(1) if match else text

    items = []
    for m in ITEM_PATTERN.finditer(section):
        raw_assignees = m.group(1)
        action_label  = m.group(2).strip()
        description   = m.group(3).strip()

        assignees = [a.strip() for a in raw_assignees.split(",")]

        # Extract bare ticket numbers as CBP references
        bare_numbers = JIRA_KEY_PATTERN.findall(description + " " + action_label)
        explicit_keys = CBP_KEY_PATTERN.findall(description + " " + action_label)
        jira_refs = list({f"CBP-{n}" for n in bare_numbers + explicit_keys})

        items.append({
            "assignees":    assignees,
            "action_label": action_label,
            "description":  description,
            "jira_refs":    sorted(jira_refs),
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
            if cached_name.lower() == name_lower or cached_name.lower().startswith(name_lower):
                roles.append(info.get("role", ""))
                break

    all_devs = all("dev" in r for r in roles if r)
    any_dev  = any("dev" in r for r in roles if r)

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
        return f"Asana → Ben"

    return "Asana → Ben (default)"

# ---------------------------------------------------------------------------
# Handoff generation
# ---------------------------------------------------------------------------

def write_handoff(items, meeting_date, people):
    today = datetime.now().strftime("%Y-%m-%d")
    date_slug = today

    # Filename: 2026-04-27-p2-Standup-Harvest-Apr-27.md
    month_day = datetime.now().strftime("%b-%-d").replace(" ", "-")
    filename = f"{date_slug}-p2-Standup-Harvest-{month_day}.md"
    filepath = os.path.join(HANDOFFS_DIR, filename)

    lines = [
        "---",
        f"title: Standup Harvest — {meeting_date}",
        "priority: P2",
        "assigned_to: Cowork (Sonnet 4.6)",
        "status: READY",
        f"date: {today}",
        "---",
        "",
        f"# Standup Harvest — {meeting_date}",
        "",
        f"> **Prepared by:** Code (standup) ({today})",
        f"> **Assigned to:** Cowork (Sonnet 4.6)",
        f"> **Priority:** P2",
        f"> **STATUS**: 🔲 READY — pick up {today}",
        "",
        "---",
        "",
        "## Context",
        "",
        f"Gemini standup notes from {meeting_date} have been parsed. The action items below need to be captured as tasks. Work through them with Ben using the **task-capture skill** — present each item, confirm routing, and fire off creation.",
        "",
        "---",
        "",
        "## Action Items",
        "",
        "| # | Assignee(s) | Action | Description | Jira Refs | Suggested Route |",
        "|---|---|---|---|---|---|",
    ]

    for i, item in enumerate(items, 1):
        assignees_str = ", ".join(item["assignees"])
        action        = item["action_label"]
        description   = item["description"].replace("|", "\\|")[:80]
        jira_refs     = ", ".join(item["jira_refs"]) if item["jira_refs"] else "—"
        hint          = classify_hint(item, people)
        lines.append(f"| {i} | {assignees_str} | {action} | {description} | {jira_refs} | {hint} |")

    lines += [
        "",
        "---",
        "",
        "## Execution Steps",
        "",
        "1. Read each action item above.",
        "2. For each item, present it to Ben with the suggested route.",
        "3. Confirm or adjust with Ben, then use the **task-capture skill** to create it.",
        "4. Work through all items in order. Do not skip — Ben can defer or dismiss individually.",
        "5. Confirm concisely after each creation (key/GID + title).",
        "",
        "## Verification",
        "",
        "- [ ] All action items reviewed with Ben",
        f"- [ ] Tasks/issues created for all {len(items)} items (or explicitly deferred)",
        "",
    ]

    with open(filepath, "w") as f:
        f.write("\n".join(lines))

    return filename, filepath

def update_index(filename):
    today = datetime.now().strftime("%Y-%m-%d")
    new_row = f"| [{filename}]({filename}) | P2 | Cowork (Sonnet 4.6) | {today} |"

    with open(HANDOFFS_INDEX) as f:
        content = f.read()

    # Insert after the last row in the Active Handoffs table
    insert_marker = "| Cowork (Sonnet 4.6) |"
    last_idx = content.rfind(insert_marker)
    if last_idx != -1:
        end_of_line = content.find("\n", last_idx)
        content = content[:end_of_line + 1] + new_row + "\n" + content[end_of_line + 1:]
    else:
        # Fallback: append after the table header
        content = content.replace(
            "| File | Priority | Assigned To | Date |\n|------|----------|-------------|------|",
            f"| File | Priority | Assigned To | Date |\n|------|----------|-------------|------|\n{new_row}"
        )

    with open(HANDOFFS_INDEX, "w") as f:
        f.write(content)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Standup note harvester → handoff")
    parser.add_argument("--email", required=True, help="Path to email text file")
    parser.add_argument("--date",  help='Meeting date string, e.g. "Apr 27, 2026"')
    args = parser.parse_args()

    with open(args.email) as f:
        email_text = f.read()

    meeting_date = args.date or datetime.now().strftime("%b %-d, %Y")
    people = load_people()

    items = parse_email(email_text)
    if not items:
        print("❌ No action items found. Check that the email contains a '[Name] Action: Description' format.")
        sys.exit(1)

    print(f"📋 Parsed {len(items)} action items from {meeting_date} standup\n")

    for i, item in enumerate(items, 1):
        hint = classify_hint(item, people)
        assignees = ", ".join(item["assignees"])
        print(f"  {i}. [{assignees}] {item['action_label']}: {item['description'][:60]} → {hint}")

    filename, filepath = write_handoff(items, meeting_date, people)
    update_index(filename)

    print(f"\n✅ Handoff written: handoffs/{filename}")
    print(f"   Cowork will work through these with Ben using task-capture.")

if __name__ == "__main__":
    main()

