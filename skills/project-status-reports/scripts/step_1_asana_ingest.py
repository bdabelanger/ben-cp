import json
import os
import sys
import re
from datetime import datetime
try:
    import requests
except ImportError:
    requests = None

MANIFEST_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../manifest.json")
REPO_ROOT = os.path.dirname(os.path.abspath(MANIFEST_PATH))

# GIDs from the Official Specification
TEAM_FIELD_GID = "1208820967756795"

# Custom Team field enum GIDs (the overarching Asana "Product" team never changes)
TEAM_GIDS = {
    "platform":  "1208820967756799",
    "reporting": "1208820967756798",
    "devops":    "1209860073668304",
    "indiana":   "1209860073668305",
    "specialty": "1209101939195843",
}
PLATFORM_TEAM_GID = TEAM_GIDS["platform"]  # kept for backwards compatibility
STAGE_FIELD_GID = "1208822149019495"
MILESTONE_GIDS = {
    "qa_start": "1211631943113717",
    "uat_start": "1210467277124544",
    "beta_start": "1208818118032458",
    "ga_date": "1210909549820601",   # GA Month fallback
    "ga_target": "1208818124273418"  # Primary GA target
}

def get_path_from_manifest(step_id):
    with open(MANIFEST_PATH, 'r') as f:
        data = json.load(f)
    relative_path = next(s['file'] for s in data['steps'] if s['id'] == step_id)
    return os.path.join(REPO_ROOT, relative_path)

def extract_gid_from_url(url):
    match = re.search(r'/0/(\d+)', url)
    return match.group(1) if match else None

def filter_platform_projects(input_path, output_path, target_gid=None, team_gid=None):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] step_1_asana_ingest.py")
    print(f"Reading from: {input_path}")

    try:
        with open(input_path, 'r') as f:
            data = json.load(f)

        filtered = []
        for p in data:
            # Single project mode: match GID
            if target_gid and p['gid'] != target_gid:
                continue

            custom_fields = p.get('custom_fields', [])

            jira_link = p.get('jira_link')
            stage = p.get('stage')

            # Extract stage from custom fields if not already set (new format)
            if not stage:
                stage_field = next((f for f in custom_fields if f['gid'] == STAGE_FIELD_GID), None)
                if stage_field:
                    stage = (stage_field.get('enum_value') or {}).get('name') or stage_field.get('display_value')

            # Extract status from current_status_update if not already set (new format)
            if not p.get('status'):
                csu = p.get('current_status_update') or {}
                if csu.get('status_type'):
                    p['status'] = csu['status_type']

            target_team_gid = team_gid or PLATFORM_TEAM_GID
            team_field = next((f for f in custom_fields if f['gid'] == TEAM_FIELD_GID), None)
            is_platform = (team_field and (team_field.get('enum_value') or {}).get('gid') == target_team_gid)

            if is_platform or not custom_fields:
                # Exclude completed projects
                if (p.get('current_status_update') or {}).get('status_type') == "complete" or p.get('status') == "complete":
                    continue

                # Extract milestones
                milestones = p.get('milestones', {})
                for key, gid in MILESTONE_GIDS.items():
                    field = next((f for f in custom_fields if f['gid'] == gid), None)
                    if field:
                        milestones[key] = (field.get('date_value') or {}).get('date') or (field.get('enum_value') or {}).get('name')

                p['milestones'] = milestones
                p['stage'] = stage

                # Ensure jira_link is present for the harvester
                if not jira_link:
                    link_field = next((f for f in custom_fields if f['gid'] == "1208818005809198"), None)
                    jira_link = link_field.get('text_value') or link_field.get('display_value') if link_field else "N/A"

                p['jira_link'] = jira_link
                filtered.append(p)

        # Enrich filtered projects with Asana status update HTML (separate API call per project)
        token = os.environ.get("ASANA_API_TOKEN")
        if token and requests:
            headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
            enriched = 0
            for p in filtered:
                csu = p.get("current_status_update") or {}
                gid = csu.get("gid")
                if not gid:
                    continue
                url = f"https://app.asana.com/api/1.0/status_updates/{gid}?opt_fields=html_text,text,title,status_type"
                resp = requests.get(url, headers=headers)
                if resp.status_code == 200:
                    su = resp.json().get("data", {})
                    csu["html_text"] = su.get("html_text", "")
                    csu["text"] = su.get("text", "")
                    csu["title"] = su.get("title", "")
                    p["current_status_update"] = csu
                    enriched += 1
            if enriched:
                print(f"  Fetched status update HTML for {enriched} projects.")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(filtered, f, indent=2)

        print(f"✅ step_1_asana_ingest Complete: {len(filtered)} projects filtered.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    INPUT_FILE = os.path.join(REPO_ROOT, "inputs/raw/asana_all_projects.json")
    OUTPUT_FILE = get_path_from_manifest("1_asana_ingest")

    target_gid = None
    team_gid = None

    plain_args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flag_args  = sys.argv[1:]

    # --team <name>  e.g. --team reporting
    if "--team" in flag_args:
        team_name = flag_args[flag_args.index("--team") + 1].lower()
        team_gid = TEAM_GIDS.get(team_name)
        if not team_gid:
            print(f"❌ Unknown team '{team_name}'. Options: {', '.join(TEAM_GIDS)}", file=sys.stderr)
            sys.exit(1)
        print(f"🏷️  Team filter: {team_name} ({team_gid})")

    if plain_args and "asana.com" in plain_args[0]:
        target_gid = extract_gid_from_url(plain_args[0])
        print(f"🎯 Single-project mode detected for GID: {target_gid}")

    filter_platform_projects(INPUT_FILE, OUTPUT_FILE, target_gid, team_gid)
