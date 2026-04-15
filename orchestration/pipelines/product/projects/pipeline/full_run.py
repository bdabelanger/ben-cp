import os
import sys
import json
import shutil
import subprocess
import webbrowser
from datetime import datetime

# Ensure sibling scripts are importable when run from any working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from platform_report import PlatformStatusReport
from render_html import render_html

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../.."))
MANIFEST_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "../inputs/status-reports/manifest.json"))
REPO_ROOT = VAULT_ROOT

def _load_dotenv():
    """Load .env from vault root (ben-cp/.env)."""
    env_path = os.path.join(VAULT_ROOT, ".env")
    if not os.path.exists(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            os.environ.setdefault(key, val)

_load_dotenv()

def get_path_from_manifest(data, step_id):
    relative_path = next(s['file'] for s in data['steps'] if s['id'] == step_id)
    return os.path.join(REPO_ROOT, relative_path)

def build_epic_keys_from_asana(asana_path):
    """Extract epic CBP-XXXX keys from the filtered Asana output."""
    with open(asana_path, 'r') as f:
        projects = json.load(f)
    keys = []
    for p in projects:
        if '_metadata' in p:
            continue
        link = p.get('jira_link') or ''
        if 'CBP-' in link:
            keys.append(link.split('/')[-1].strip())
        for cf in p.get('custom_fields', []):
            if cf.get('gid') == '1208818005809198':
                val = cf.get('text_value') or cf.get('display_value') or ''
                if 'CBP-' in val:
                    keys.append(val.split('/')[-1].strip())
    return list(dict.fromkeys(keys))  # dedupe, preserve order

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] full_run.py")
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Parse flags
    args = sys.argv[1:]
    force = "--force" in args
    open_report = "--open" in args
    team_arg = args[args.index("--team") + 1].lower() if "--team" in args else None
    plain_args = [a for a in args if not a.startswith("--")]
    target_arg = plain_args[0] if plain_args else None

    if force:
        print("🔄 --force: wiping inputs/raw/jira/ and processed outputs for a clean run...")
        jira_raw_dir = os.path.join(VAULT_ROOT, "inputs/status-reports/raw/jira")
        if os.path.isdir(jira_raw_dir):
            shutil.rmtree(jira_raw_dir)
        subprocess.run(["python3", os.path.join(script_dir, "update_manifest.py"), "reset"], check=True)

    with open(MANIFEST_PATH, 'r') as f:
        manifest = json.load(f)

    ASANA_RAW      = os.path.abspath(os.path.join(SCRIPT_DIR, "../inputs/status-reports/raw/asana_all_projects.json"))
    JIRA_RAW_DIR   = os.path.abspath(os.path.join(SCRIPT_DIR, "../inputs/status-reports/raw/jira"))
    ASANA_FILTERED = get_path_from_manifest(manifest, "1_asana_ingest")
    JIRA_HARVESTED = get_path_from_manifest(manifest, "4_jira_harvest")
    OUTPUT_PATH    = get_path_from_manifest(manifest, "5_report_generation")

    print("🚀 Triggering Pipeline Components...")

    # Step 0: Asana API refresh
    result = subprocess.run(["python3", os.path.join(script_dir, "step_0_asana_refresh.py")])
    if result.returncode != 0:
        if not os.path.exists(ASANA_RAW):
            print(f"❌ Asana refresh failed and no cached data at {ASANA_RAW}. Aborting.")
            sys.exit(1)
        print("⚠️  Asana refresh failed — continuing with existing cached data.")

    # Step 1: Asana filter
    cmd = ["python3", os.path.join(script_dir, "step_1_asana_ingest.py")]
    if target_arg:
        cmd.append(target_arg)
    if team_arg:
        cmd += ["--team", team_arg]
    subprocess.run(cmd)

    # Step 2 (Agent-side): per-epic Jira fetch via searchJiraIssuesUsingJql
    if not os.path.exists(JIRA_HARVESTED):
        epic_keys = build_epic_keys_from_asana(ASANA_FILTERED) if os.path.exists(ASANA_FILTERED) else []
        missing_keys = [k for k in epic_keys if not os.path.exists(os.path.join(JIRA_RAW_DIR, f"{k}.json"))]

        if not epic_keys:
            print("ℹ️  No Jira epic keys found — skipping Jira fetch and harvest.")
            # Write an empty harvest file so the report generator has something to read
            os.makedirs(os.path.dirname(JIRA_HARVESTED), exist_ok=True)
            with open(JIRA_HARVESTED, "w") as f:
                json.dump([], f)
        else:
            if missing_keys:
                print(f"\n📥 Fetching raw Jira data for {len(missing_keys)} epic(s)...")
                result = subprocess.run(["python3", os.path.join(script_dir, "step_2_atlassian_fetch.py")])
                if result.returncode != 0:
                    print("❌ Jira fetch failed. Check step_2_atlassian_fetch.py output above.")
                    sys.exit(1)

            # Raw files present — run harvest automatically
            print("📥 Raw Jira files found for all epics. Running harvest...")
            result = subprocess.run(["python3", os.path.join(script_dir, "step_3_jira_harvest.py")])
            if result.returncode != 0 or not os.path.exists(JIRA_HARVESTED):
                print("❌ Harvest failed. Check step_3_jira_harvest.py output above.")
                sys.exit(1)

    # 📊 Final Synthesis
    print("📊 Synthesizing Platform Weekly Status...")

    reporter = PlatformStatusReport(ASANA_FILTERED, JIRA_HARVESTED, JIRA_RAW_DIR)
    report_md = reporter.render()

    html_path = OUTPUT_PATH.replace(".md", ".html")
    os.makedirs(os.path.dirname(html_path), exist_ok=True)
    with open(html_path, "w") as f:
        f.write(render_html(report_md))

    print(f"✅ Report generated: {html_path}")
    if open_report:
        webbrowser.open(f"file://{os.path.abspath(html_path)}")
    print(f"\n--- PREVIEW ---\n")
    print(report_md)

if __name__ == "__main__":
    main()
