#!/usr/bin/env python3
"""
Dream Cycle — Daily Report Orchestrator

Execution model:
  Phase 1 (Draft)    — each skill produces an independent report envelope
  Phase 2 (Revision) — each skill receives the full draft pool and may revise
  Phase 3 (Editorial)— the orchestrator edits final envelopes: selects key
                       details, preserves agent voice via quotes, writes lede
  Phase 4 (Assembly) — compiles edited excerpts into the daily report

Display framing (titles, bylines, section names, output filenames) is loaded
from character.md at runtime so this script stays persona-agnostic.

Skills in this version are MOCKED. Real invocation happens once the
agent-python-wrappers layer is built (see handoff: p1-agent-python-wrappers).
"""
import json
import os
import re
import glob
import argparse
import subprocess
from datetime import datetime

SKILLS_DIR   = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "intelligence", "core", "skills"))
REPO_ROOT    = os.path.abspath(os.path.join(SKILLS_DIR, "..", "..", ".."))
VAULT_ROOT   = os.path.abspath(os.path.join(REPO_ROOT, "..", ".."))
OUTPUTS_DIR  = os.path.join(REPO_ROOT, "orchestration", "pipelines", "outputs", "dream")
REPORT_MD    = os.path.join(os.path.dirname(__file__), "report.md")
VAULT_CSS    = os.path.join(SKILLS_DIR, "styles", "vault.css")


def load_vault_css():
    """Load shared vault.css for inlining into HTML reports."""
    if os.path.exists(VAULT_CSS):
        with open(VAULT_CSS, "r") as f:
            return f.read()
    print("[WARN] styles/vault.css not found — falling back to minimal inline styles.")
    return "body { font-family: Georgia, serif; max-width: 820px; margin: 2rem auto; padding: 0 1rem; }"


# ---------------------------------------------------------------------------
# Character loading — all display strings come from character.md
# ---------------------------------------------------------------------------

def load_character():
    """
    Parse character.md for display config used in report assembly.
    Looks for a fenced ```json block under a ## Report Config header.
    Falls back to safe generic defaults if the block is absent or malformed.
    """
    defaults = {
        "report_title":      "Daily Report",
        "byline":            "Orchestrator",
        "editor_label":      "Editor",
        "lede_section":      "Summary",
        "columns_section":   "Skill Reports",
        "output_prefix":     "daily-report",
        "footer":            "End of report.",
        "editorial_note":    "Columns are editorial excerpts from each skill's full report.",
    }
    if not os.path.exists(REPORT_MD):
        print("[WARN] report.md not found — using generic display defaults.")
        return defaults

    with open(REPORT_MD, "r") as f:
        content = f.read()

    match = re.search(r"## Report Config\s+```json\s+(\{.*?\})\s+```", content, re.DOTALL)
    if not match:
        print("[WARN] No '## Report Config' JSON block in character.md — using generic defaults.")
        return defaults

    try:
        overrides = json.loads(match.group(1))
        return {**defaults, **overrides}
    except json.JSONDecodeError as e:
        print(f"[WARN] character.md Report Config JSON malformed: {e} — using generic defaults.")
        return defaults


# ---------------------------------------------------------------------------
# Spec discovery
# ---------------------------------------------------------------------------

def get_report_specs():
    """
    Discovers all report_spec.json files in the skills tree and returns
    them sorted by run_order. Any spec missing run_order sorts to the end.
    Ensures each skill is unique (handles symlink overlaps).
    """
    specs_by_name = {}
    for filepath in glob.glob(os.path.join(SKILLS_DIR, "**", "report_spec.json"), recursive=True):
        with open(filepath, "r") as f:
            try:
                spec = json.load(f)
                name = spec.get("skill_name")
                if name:
                    # If duplicate, keep the one with shorter path (likely the real one)
                    if name not in specs_by_name or len(filepath) < len(specs_by_name[name]["_path"]):
                        spec["_path"] = filepath
                        specs_by_name[name] = spec
            except json.JSONDecodeError as e:
                print(f"[WARN] Malformed report_spec at {filepath}: {e}")
    
    unique_specs = list(specs_by_name.values())
    return sorted(unique_specs, key=lambda x: x.get("run_order", 99))


# ---------------------------------------------------------------------------
# Skill execution
# ---------------------------------------------------------------------------

def execute_skill(spec, phase="draft", draft_pool=None):
    """
    Executes a skill's automated report.py script.
    If the script is missing, falls back to a mock envelope.
    """
    skill_name = spec.get("skill_name", "unknown")
    spec_path  = spec.get("_path")
    skill_dir  = os.path.dirname(spec_path)
    # Try to find the script in the tools/ mirror path first
    rel_path = os.path.relpath(skill_dir, SKILLS_DIR)
    script_path = os.path.join(REPO_ROOT, "tools", rel_path, "report.py")

    if not os.path.exists(script_path):
        # Fallback to the legacy skill-dir report.py (usually for migration/testing)
        script_path = os.path.join(skill_dir, "report.py")

    if not os.path.exists(script_path):
        # Fallback to mock for v1 rollout
        return {
            "skill":          skill_name,
            "preferred_agent": spec.get("preferred_agent", "unknown"),
            "run_at":         datetime.utcnow().isoformat() + "Z",
            "status":         "ok",
            "phase":          phase,
            "summary":        f"[MOCK] {skill_name}: draft assessment complete.",
            "findings":       ["[MOCK] Live report.py not found — using placeholder."],
            "flags":          [],
        }

    try:
        # Pass the draft pool as JSON if in revision phase
        env = os.environ.copy()
        if draft_pool:
            env["DREAM_DRAFTS"] = json.dumps(draft_pool)
        
        result = subprocess.run(
            ["python3", script_path, "--phase", phase],
            capture_output=True, text=True, check=True, env=env
        )
        return json.loads(result.stdout)
    except Exception as e:
        print(f"  [ERROR] {skill_name} failed: {e}")
        return {
            "skill":          skill_name,
            "preferred_agent": spec.get("preferred_agent", "unknown"),
            "run_at":         datetime.utcnow().isoformat() + "Z",
            "status":         "error",
            "phase":          phase,
            "summary":        f"Audit failed to execute for {skill_name}.",
            "findings":       [],
            "flags":          [f"Execution Error: {str(e)}"],
        }


def editorialize(envelope):
    """
    Editorial pass: reduces a full skill envelope to a brief excerpt.
    Preserves the skill agent's voice via direct quotes where available.
    Adds no padding.

    In the real system this calls an LLM with character.md + the full envelope.
    For now, uses mock excerpts.
    """
    skill = envelope["skill"]
    # context, quote = MOCK_EDITORIAL_EXCERPTS.get(skill, (envelope["summary"], None))
    context = envelope["summary"]
    quote = None

    excerpt = ""
    if context:
        excerpt += context
    if quote:
        excerpt = f"{excerpt} {quote}".strip() if excerpt else quote

    return {
        **envelope,
        "excerpt":   excerpt or envelope["summary"],
        "has_flags": bool(envelope.get("flags")),
    }


# ---------------------------------------------------------------------------
# Pipeline phases
# ---------------------------------------------------------------------------

def process_draft_phase(specs):
    print("\n[PHASE 1] Draft — skills producing independent reports...")
    drafts = []
    for spec in specs:
        print(f"  → {spec.get('skill_name')} (agent: {spec.get('preferred_agent')})")
        drafts.append(execute_skill(spec, phase="draft"))
    return drafts


def process_revision_phase(specs, draft_pool):
    print(f"\n[PHASE 2] Revision — skills reviewing {len(draft_pool)} peer drafts...")
    finals = []
    for spec in specs:
        print(f"  → {spec.get('skill_name')}")
        finals.append(execute_skill(spec, phase="final", draft_pool=draft_pool))
    return finals


def process_editorial_phase(envelopes):
    """
    Editorial pass — selects key details, preserves agent voice,
    reduces full reports to sharp excerpts for the daily report.
    """
    print(f"\n[PHASE 3] Editorial — reducing {len(envelopes)} skill reports to excerpts...")
    edited = []
    for env in envelopes:
        edited.append(editorialize(env))
        print(f"  → {env['skill']}")
    return edited


# ---------------------------------------------------------------------------
# Report assembly — display strings loaded from character
# ---------------------------------------------------------------------------

def write_lede(envelopes, char):
    """
    Writes the lede (front page / summary) as an editorial read.
    Not a summary of summaries — surfaces what matters across skills.
    In the real system an LLM writes this from character.md + all envelopes.
    """
    errors  = [e for e in envelopes if e["status"] == "error"]
    flagged = [e for e in envelopes if e.get("has_flags")]
    warnings = [e for e in envelopes if e["status"] == "warn"]

    if errors:
        return (
            f"🔴 **{len(errors)} skill(s) failed to report.** "
            "Review the columns below and check logged handoffs before proceeding."
        )
    elif flagged:
        flag_skills = ", ".join(e["skill"] for e in flagged)
        return (
            f"🟡 Clean run with items to watch. Flags from: {flag_skills}. "
            "Review flagged columns — no action required unless noted."
        )
    elif warnings:
        return f"🟡 **{len(warnings)} warning(s).** Clean run with items to watch."
    else:
        return "🟢 All skills reporting clean. Nothing to flag."


def build_report_markdown(envelopes, date_str, run_ts, char):
    lede = write_lede(envelopes, char)

    md  = f"# {char['report_title']} — {date_str}\n\n"
    md += f"> **{char['editor_label']}:** {char['byline']}  \n"
    md += f"> **Published:** {run_ts}  \n"
    md += f"> **Skills:** {len(envelopes)} active  \n\n"
    md += "---\n\n"
    md += f"## {char['lede_section']}\n\n{lede}\n\n"
    md += "---\n\n"
    md += f"## {char['columns_section']}\n\n"

    for env in envelopes:
        icon = {"ok": "🟢", "warn": "🟡", "error": "🔴"}.get(env["status"], "⚪")
        md += f"### {icon} {env['skill']}\n\n"
        md += f"{env['excerpt']}\n\n"
        if env.get("flags"):
            md += "**Flags:**\n"
            for flag in env["flags"]:
                md += f"- {flag}\n"
            md += "\n"

        if env.get("findings"):
            for find in env["findings"]:
                md += f"- {find}\n"
            md += "\n"

    md += f"---\n\n*{char['footer']}*\n"
    return md


def build_report_html(envelopes, date_str, run_ts, char):
    status_colors = {"ok": "#22c55e", "warn": "#f59e0b", "error": "#ef4444"}
    lede = write_lede(envelopes, char)
    css  = load_vault_css()

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{char['report_title']} — {date_str}</title>
  <style>
{css}
  </style>
</head>
<body class="gazette-body">
<div class="container">
  <h1>{char['report_title']} — {date_str}</h1>
  <div class="gazette-meta">{char['editor_label']}: {char['byline']} &nbsp;|&nbsp; Published: {run_ts} &nbsp;|&nbsp; {len(envelopes)} skills</div>
  <p class="gazette-editorial-note">{char['editorial_note']}</p>
"""
    html += f'  <div class="lede">{lede}</div>\n'

    for env in envelopes:
        color   = status_colors.get(env["status"], "#94a3b8")
        excerpt = env["excerpt"]
        content = (
            f'<blockquote>{excerpt}</blockquote>'
            if excerpt.startswith('"') and excerpt.endswith('"')
            else f'<p>{excerpt}</p>'
        )
        html += f'  <div class="column" style="border-left-color:{color};">\n'
        html += f'    <h3>{env["skill"]}</h3>\n'
        html += f'    {content}\n'
        if env.get("findings"):
            html += '<div class="findings-list"><ul>'
            for find in env["findings"]:
                # Convert markdown links [text](url.md) to HTML <a> and swap to .html for humans
                rendered_find = re.sub(r'\[([^\]]+)\]\(([^\)]+)\.md\)', r'<a href="\2.html" target="_blank">\1</a>', find)
                # Also handle non-md links
                rendered_find = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', rendered_find)
                html += f"<li>{rendered_find}</li>"
            html += '</ul></div>\n'

        if env.get("flags"):
            for flag in env["flags"]:
                # Handle both string flags (Gazette v1) and legacy object flags
                msg = flag.get("message", flag) if isinstance(flag, dict) else flag
                sev = flag.get("severity", "flag").lower() if isinstance(flag, dict) else "flag"
                html += f'    <div class="flag-card flag-{sev}">{msg}</div>\n'
        html += "  </div>\n"

    html += f'  <footer class="vault-footer">{char["footer"]}</footer>\n'
    html += "</div>\n</body>\n</html>\n"
    return html


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def should_run(spec, date):
    """Cadence gating: skip weekly skills unless it's Monday."""
    cadence = spec.get("cadence", "daily")
    if cadence == "weekly" and date.weekday() != 0:
        return False
    return True


def archive_if_exists(path):
    """Move an existing output file to outputs/archive/ before overwriting."""
    if os.path.exists(path):
        archive_dir = os.path.join(OUTPUTS_DIR, "archive")
        os.makedirs(archive_dir, exist_ok=True)
        name, ext = os.path.splitext(os.path.basename(path))
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        ts = datetime.utcnow().strftime("%H%M%S")
        dest = os.path.join(archive_dir, f"{name}-{date_str}-{ts}{ext}")
        os.rename(path, dest)
        print(f"  [ARCHIVE] Previous report moved → {dest}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="Dream Cycle — Daily Report Orchestrator")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Run the full pipeline but print to stdout instead of writing files."
    )
    parser.add_argument(
        "--date", default=None, metavar="YYYY-MM-DD",
        help="Override the target date (default: today)."
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    args    = parse_args()
    run_ts  = datetime.utcnow().isoformat() + "Z"
    char    = load_character()

    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print(f"[ERROR] Invalid --date format '{args.date}'. Expected YYYY-MM-DD.")
            return
    else:
        target_date = datetime.now().date()

    date_str = target_date.strftime("%Y-%m-%d")
    mode     = " [DRY-RUN]" if args.dry_run else ""
    print(f"[{run_ts}] Dream Cycle initializing — {char['report_title']} ({date_str}){mode}")

    all_specs = get_report_specs()
    if not all_specs:
        print("[ERROR] No report_spec.json files found in skills tree. Aborting.")
        return

    specs   = [s for s in all_specs if should_run(s, target_date)]
    # Sort by run_order (ascending). Skills with no run_order default to 100.
    specs.sort(key=lambda s: s.get("run_order", 100))

    skipped = [s.get("skill_name") for s in all_specs if not should_run(s, target_date)]
    if skipped:
        print(f"[INFO] Skipping (cadence): {skipped}")
    print(f"[INFO] Running {len(specs)} skill(s): {[s.get('skill_name') for s in specs]}")

    drafts = process_draft_phase(specs)
    finals = process_revision_phase(specs, drafts)
    edited = process_editorial_phase(finals)

    md_content   = build_report_markdown(edited, date_str, run_ts, char)
    html_content = build_report_html(edited, date_str, run_ts, char)

    if args.dry_run:
        print("\n" + "─" * 60)
        print(md_content)
        print("─" * 60)
        print("[DRY-RUN] Pipeline complete. No files written.")
        return

    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    prefix   = char["output_prefix"]
    md_path  = os.path.join(OUTPUTS_DIR, f"{prefix}.md")
    html_path = os.path.join(OUTPUTS_DIR, f"{prefix}.html")

    # [HOUSEKEEPING] Archive any legacy reports from previous dates to keep root clean
    print(f"[INFO] Cleaning root output directory...")
    all_reports = glob.glob(os.path.join(OUTPUTS_DIR, f"{prefix}-*.md")) + \
                  glob.glob(os.path.join(OUTPUTS_DIR, f"{prefix}-*.html"))
    for rpath in all_reports:
        # Move everything that isn't the CURRENT path (handles both same-day overwrites and past-day cleanup)
        if rpath != md_path and rpath != html_path:
            archive_if_exists(rpath)

    # Re-verify today's paths just in case they existed and weren't caught in glob (edge case)
    archive_if_exists(md_path)
    archive_if_exists(html_path)

    with open(md_path, "w") as f:
        f.write(md_content)
    with open(html_path, "w") as f:
        f.write(html_content)

    print(f"\n[SUCCESS] Report published.")
    print(f"  → {md_path}")
    print(f"  → {html_path}")


if __name__ == "__main__":
    main()
