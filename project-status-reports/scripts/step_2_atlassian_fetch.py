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
MANIFEST_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../manifest.json")
REPO_ROOT = os.path.dirname(os.path.abspath(MANIFEST_PATH))

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
    missing_keys = [k for k in epic_keys if not os.path.exists(os.path.join(JIRA_RAW_DIR, f"{k}.json"))]

    if not missing_keys:
        print("✅ step_2_atlassian_fetch Complete: No missing keys to fetch.")
        return

    print(f"📥 Fetchin Atlassian data for {len(missing_keys)} missing epics...")

    # 3. Iteratively fetch each missing epic
    for key in missing_keys:
        save_path = os.path.join(JIRA_RAW_DIR, f"{key}.json")
        jql = f'project = CBP AND issuetype != QAFE AND (issuekey = {key} OR "Epic Link" = {key} OR parent = {key}) ORDER BY updated DESC'
        
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
                f"{atlassian_base_url}/rest/api/3/search",
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
            
            total = data.get("total", 0)
            start_at += len(issues_batch)
            
            if start_at >= total or len(issues_batch) == 0:
                break
        
        if not all_issues:
            print("❌ Error: 0 issues returned for this Epic. Fatal pipeline error.", file=sys.stderr)
            sys.exit(1)
            
        print(f"OK ({len(all_issues)} issues)")
        
        # 4. Save to disk
        with open(save_path, 'w') as f:
            json.dump(all_issues, f, indent=2)
            
    print(f"✅ step_2_atlassian_fetch Complete: Successfully fetched {len(missing_keys)} epics.")

if __name__ == "__main__":
    fetch_missing_atlassian_data()
