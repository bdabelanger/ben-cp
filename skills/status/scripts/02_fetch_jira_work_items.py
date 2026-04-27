import os
import sys
import json
import time
import random
try:
    import requests
    from requests.auth import HTTPBasicAuth
except ImportError:
    print("❌ Error: 'requests' library not installed. Run: pip3 install requests", file=sys.stderr)
    sys.exit(1)
from datetime import datetime

# Manifest path resolution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../.."))
MANIFEST_PATH = os.path.join(VAULT_ROOT, "reports/status/data/manifest.json")
REPO_ROOT = VAULT_ROOT

def _load_dotenv():
    env_path = os.path.join(VAULT_ROOT, ".env")
    if not os.path.exists(env_path): return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line: continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

def hardened_get(url, auth, headers, params=None, max_retries=3):
    """Execution wrapper with exponential backoff and rate-limit awareness."""
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, headers=headers, params=params, auth=auth, timeout=30)
            
            if resp.status_code == 200:
                return resp
            
            if resp.status_code == 429:
                wait = (2 ** attempt) + random.random()
                retry_after = resp.headers.get("Retry-After")
                if retry_after:
                    try:
                        wait = int(retry_after) + 0.5
                    except:
                        pass
                print(f"\n⚠️  Rate limited (429). Waiting {wait:.1f}s... ", end="", file=sys.stderr)
                time.sleep(wait)
                continue

            if resp.status_code in (500, 502, 503, 504):
                wait = (2 ** attempt) + random.random()
                print(f"\n⚠️  Server error ({resp.status_code}). Retrying in {wait:.1f}s... ", end="", file=sys.stderr)
                time.sleep(wait)
                continue

            # Non-retryable errors (401, 404, etc.)
            return resp

        except requests.exceptions.RequestException as e:
            wait = (2 ** attempt) + random.random()
            print(f"\n⚠️  Connection error: {e}. Retrying in {wait:.1f}s... ", end="", file=sys.stderr)
            time.sleep(wait)
            
    return None

def get_path_from_manifest(data, step_id):
    try:
        relative_path = next(s['file'] for s in data['steps'] if s['id'] == step_id)
        return os.path.join(REPO_ROOT, relative_path)
    except StopIteration:
        print(f"❌ Error: Step ID '{step_id}' not found in manifest.", file=sys.stderr)
        sys.exit(1)

def build_epic_keys_from_asana(asana_path):
    if not os.path.exists(asana_path):
        print(f"⚠️  Asana input not found: {asana_path}")
        return []
    with open(asana_path, 'r') as f:
        projects = json.load(f)
    keys = []
    for p in projects:
        if '_metadata' in p: continue
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
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] fetch_jira_work_items.py (Hardened)")
    _load_dotenv()
    
    email = os.environ.get("ATLASSIAN_USER_EMAIL")
    token = os.environ.get("ATLASSIAN_API_TOKEN")
    
    if not email or not token:
        print("❌ Error: Missing credentials (ATLASSIAN_USER_EMAIL/TOKEN).", file=sys.stderr)
        sys.exit(1)
        
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}
    base_url = "https://casecommons.atlassian.net"

    if not os.path.exists(MANIFEST_PATH):
        print(f"❌ Error: Manifest missing at {MANIFEST_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(MANIFEST_PATH, 'r') as f:
        manifest = json.load(f)

    ASANA_FILTERED = get_path_from_manifest(manifest, "1_asana_ingest")
    JIRA_RAW_DIR = get_path_from_manifest(manifest, "2_atlassian_fetch")
    os.makedirs(JIRA_RAW_DIR, exist_ok=True)

    keys_to_fetch = build_epic_keys_from_asana(ASANA_FILTERED)

    if not keys_to_fetch:
        print("✅ step_2_atlassian_fetch Complete: No epics found.")
        return

    print(f"📥 Fetching Atlassian data for {len(keys_to_fetch)} epics...")
    failed_keys = []

    for key in keys_to_fetch:
        save_path = os.path.join(JIRA_RAW_DIR, f"{key}.json")
        project = key.split('-')[0] if '-' in key else "CBP"
        jql = f'project = {project} AND parent = {key} ORDER BY created ASC'
        
        all_issues = []
        start_at = 0
        max_results = 100
        
        print(f"  Fetching -> {key} ... ", end="")
        harvest_success = True
        while True:
            params = {
                "jql": jql,
                "fields": "summary,status,assignee,priority,issuetype,parent,timeoriginalestimate,timespent,fixVersions,created,updated",
                "maxResults": max_results,
                "startAt": start_at
            }
            
            resp = hardened_get(f"{base_url}/rest/api/3/search/jql", auth, headers, params)
            
            if not resp or resp.status_code != 200:
                code = resp.status_code if resp else "TIMEOUT"
                print(f"\n❌ Error: Failed fetching children for {key} (HTTP {code}).", file=sys.stderr)
                harvest_success = False
                break
                
            data = resp.json()
            issues_batch = data.get("issues", [])
            all_issues.extend(issues_batch)
            
            total = data.get("total", 0)
            start_at += len(issues_batch)
            if start_at >= total or len(issues_batch) == 0:
                break
        
        if harvest_success:
            with open(save_path, 'w') as f:
                json.dump(all_issues, f, indent=2)

            epic_path = os.path.join(JIRA_RAW_DIR, f"{key}_epic.json")
            epic_resp = hardened_get(f"{base_url}/rest/api/3/issue/{key}", auth, headers, {"fields": "summary,timeoriginalestimate,timespent,status,issuetype"})
            
            if epic_resp and epic_resp.status_code == 200:
                with open(epic_path, 'w') as f:
                    json.dump(epic_resp.json(), f, indent=2)
            else:
                code = epic_resp.status_code if epic_resp else "TIMEOUT"
                print(f"  ⚠️  Could not fetch epic {key} details (HTTP {code})")

            print(f"OK ({len(all_issues)} issues)")
        else:
            failed_keys.append(key)
            
    if failed_keys:
        print(f"\n❌ step_2_atlassian_fetch Failed for keys: {', '.join(failed_keys)}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ step_2_atlassian_fetch Complete: Successfully harvested {len(keys_to_fetch)} epics.")

if __name__ == "__main__":
    fetch_missing_atlassian_data()
