import os
import sys
import json
try:
    import requests
    from requests.auth import HTTPBasicAuth
except ImportError:
    print("❌ Error: 'requests' library not installed. Run: pip3 install requests", file=sys.stderr)
    sys.exit(1)
from datetime import datetime

# Manifest path resolution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../.."))
MANIFEST_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "../inputs/status-reports/manifest.json"))
REPO_ROOT = VAULT_ROOT

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
    return list(dict.fromkeys(keys))

def fetch_missing_atlassian_data():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] step_2_atlassian_fetch.py")
    
    # 1. Check for required credentials
    atlassian_email = os.environ.get("ATLASSIAN_USER_EMAIL")
    atlassian_token = os.environ.get("ATLASSIAN_API_TOKEN")
    
    if not atlassian_email or not atlassian_token:
        print("❌ Error: Missing credentials. Please set ATLASSIAN_USER_EMAIL and ATLASSIAN_API_TOKEN environment variables.", file=sys.stderr)
        sys.exit(1)
        
    auth = HTTPBasicAuth(atlassian_email, atlassian_token)
    headers = {"Accept": "application/json"}
    atlassian_base_url = "https://casecommons.atlassian.net"

    # 2. Setup dynamic paths
    with open(MANIFEST_PATH, 'r') as f:
        manifest = json.load(f)

    ASANA_FILTERED = get_path_from_manifest(manifest, "1_asana_ingest")
    JIRA_RAW_DIR = get_path_from_manifest(manifest, "2_atlassian_fetch")
    
    os.makedirs(JIRA_RAW_DIR, exist_ok=True)

    epic_keys = build_epic_keys_from_asana(ASANA_FILTERED) if os.path.exists(ASANA_FILTERED) else []
    keys_to_fetch = epic_keys

    if not keys_to_fetch:
        print("✅ step_2_atlassian_fetch Complete: No epics to fetch.")
        return

    print(f"📥 Fetching Atlassian data for {len(keys_to_fetch)} epics...")

    # 3. Iteratively fetch each epic
    for key in keys_to_fetch:
        save_path = os.path.join(JIRA_RAW_DIR, f"{key}.json")
        # Use parent in (...) — this workspace uses "Project" as the top-level type,
        # not Epic. Child stories have parent.key set directly. "Epic Link" is the
        # old Jira Epic field and does not apply here.
        # QAFE exclusion is done in step_3_jira_harvest.py (Python), not in JQL.
        jql = f'project = CBP AND parent in ({key}) ORDER BY parent ASC, status ASC'
        
        all_issues = []
        start_at = 0
        max_results = 100
        
        print(f"  Fetching -> {key} ... ", end="")
        while True:
            params = {
                "jql": jql,
                "fields": "summary,status,assignee,priority,issuetype,parent,timeoriginalestimate,timespent,fixVersions,created,updated",
                "maxResults": max_results,
                "startAt": start_at
            }
            
            resp = requests.get(
                f"{atlassian_base_url}/rest/api/3/search/jql",
                headers=headers,
                params=params,
                auth=auth
            )
            
            if resp.status_code in (401, 403):
                print(f"\n❌ Error: Authentication failed (HTTP {resp.status_code}). Please verify your ATLASSIAN_USER_EMAIL and ATLASSIAN_API_TOKEN.", file=sys.stderr)
                sys.exit(1)
            elif resp.status_code != 200:
                print(f"\n❌ Error: Atlassian API returned HTTP {resp.status_code} - {resp.text}", file=sys.stderr)
                sys.exit(1)
                
            data = resp.json()
            issues_batch = data.get("issues", [])
            all_issues.extend(issues_batch)
            
            # Support both old (total) and new (isLast) pagination
            is_last = data.get("isLast", False)
            total = data.get("total")
            
            if is_last:
                break
            
            if total is not None:
                start_at += len(issues_batch)
                if start_at >= total:
                    break
            
            if len(issues_batch) == 0:
                break
                
            # For new pagination, we might need to use nextPageToken
            next_token = data.get("nextPageToken")
            if next_token:
                params["nextPageToken"] = next_token
            else:
                params["startAt"] = start_at + len(issues_batch)
        
        if not all_issues:
            print(f"⚠️  0 child issues found for {key} — saving empty file and continuing.")

        print(f"OK ({len(all_issues)} issues)")

        # 4. Save child issues to disk
        with open(save_path, 'w') as f:
            json.dump(all_issues, f, indent=2)

        # 5. Also fetch the epic itself for timeoriginalestimate
        epic_path = os.path.join(JIRA_RAW_DIR, f"{key}_epic.json")
        epic_resp = requests.get(
            f"{atlassian_base_url}/rest/api/3/issue/{key}",
            headers=headers,
            params={"fields": "summary,timeoriginalestimate,timespent,status,issuetype"},
            auth=auth
        )
        if epic_resp.status_code == 200:
            with open(epic_path, 'w') as f:
                json.dump(epic_resp.json(), f, indent=2)
        else:
            print(f"  ⚠️  Could not fetch epic {key} ({epic_resp.status_code})")
            
    print(f"✅ step_2_atlassian_fetch Complete: Successfully fetched {len(keys_to_fetch)} epics.")

if __name__ == "__main__":
    fetch_missing_atlassian_data()
