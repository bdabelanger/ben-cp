#!/usr/bin/env python3
"""
01_harvest.py — Intelligence Harvest Script
Refreshes stale intelligence sources nightly.
"""
import os
import sys
import json
import yaml
import requests
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth

# Path Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT  = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
INTEL_DIR  = os.path.join(REPO_ROOT, "intelligence")
ASANA_CACHE = os.path.join(REPO_ROOT, "reports", "asana", "raw", "all_projects.json")

def _load_dotenv():
    env_path = os.path.join(REPO_ROOT, ".env")
    if not os.path.exists(env_path): return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line: continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

def get_atlassian_auth():
    _load_dotenv()
    email = os.environ.get("ATLASSIAN_USER_EMAIL")
    token = os.environ.get("ATLASSIAN_API_TOKEN")
    if not email or not token:
        return None
    return HTTPBasicAuth(email, token)

def is_stale(last_fetched_str, days=7):
    if not last_fetched_str:
        return True
    try:
        last_fetched = datetime.strptime(str(last_fetched_str), "%Y-%m-%d")
        return datetime.now() - last_fetched > timedelta(days=days)
    except ValueError:
        return True

def harvest_asana(source, record_dir):
    gid = source.get("gid")
    if not gid: return False
    
    if not os.path.exists(ASANA_CACHE):
        print(f"  ⚠️  Asana cache missing: {ASANA_CACHE}")
        return False
        
    with open(ASANA_CACHE, 'r') as f:
        projects = json.load(f)
        
    project_data = next((p for p in projects if str(p.get("gid")) == str(gid)), None)
    if not project_data:
        print(f"  ⚠️  Project {gid} not found in Asana cache.")
        return False
        
    source_dir = os.path.join(record_dir, "source")
    os.makedirs(source_dir, exist_ok=True)
    save_path = os.path.join(source_dir, f"asana-{gid}.json")
    
    with open(save_path, 'w') as f:
        json.dump(project_data, f, indent=2)
    return True

def harvest_jira(source, record_dir, auth):
    key = source.get("key")
    if not key or not auth: return False
    
    headers = {"Accept": "application/json"}
    base_url = "https://casecommons.atlassian.net"
    
    print(f"  📥 Fetching Jira {key}...", end="", flush=True)
    
    # Fetch Epic
    epic_url = f"{base_url}/rest/api/3/issue/{key}"
    resp = requests.get(epic_url, auth=auth, headers=headers)
    if resp.status_code != 200:
        print(f" FAILED (HTTP {resp.status_code})")
        return False
        
    source_dir = os.path.join(record_dir, "source")
    os.makedirs(source_dir, exist_ok=True)
    
    data = {"epic": resp.json(), "children": []}
    
    # Fetch Children
    jql = f'parent = {key}'
    search_url = f"{base_url}/rest/api/3/search"
    search_resp = requests.get(search_url, auth=auth, headers=headers, params={"jql": jql, "maxResults": 100})
    if search_resp.status_code == 200:
        data["children"] = search_resp.json().get("issues", [])
        
    save_path = os.path.join(source_dir, f"jira-{key}.json")
    with open(save_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(" OK")
    return True

def update_frontmatter(file_path, source_type, index, date_str):
    with open(file_path, 'r') as f:
        content = f.read()
    
    parts = content.split('---', 2)
    if len(parts) < 3: return
    
    try:
        data = yaml.safe_load(parts[1])
        if "sources" in data and source_type in data["sources"]:
            data["sources"][source_type][index]["last_fetched"] = date_str
            new_fm = yaml.dump(data, sort_keys=False, default_flow_style=False)
            new_content = f"--- \n{new_fm}---{parts[2]}"
            with open(file_path, 'w') as f:
                f.write(new_content)
    except Exception as e:
        print(f"  ❌ Failed to update frontmatter in {file_path}: {e}")

def main():
    force = "--force" in sys.argv
    auth = get_atlassian_auth()
    today = datetime.now().strftime("%Y-%m-%d")
    
    stats = {"checked": 0, "refreshed": 0, "failed": 0, "skipped": 0}
    
    print(f"--- Intelligence Harvest ---")
    print(f"Vault: {REPO_ROOT}")
    
    for root, dirs, files in os.walk(INTEL_DIR):
        # Skip source/ directories
        if "source" in dirs:
            dirs.remove("source")
            
        for file in files:
            if not file.endswith(".md") or file in ("changelog.md"):
                continue
                
            file_path = os.path.join(root, file)
            stats["checked"] += 1
            
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                if not content.startswith("---"): continue
                
                # Split and take the first block
                parts = content.split('---')
                if len(parts) < 3: continue
                
                fm_text = parts[1]
                data = yaml.safe_load(fm_text)
                
                if not isinstance(data, dict): continue
                
                sources = data.get("sources")
                if not sources:
                    continue
                
                print(f"Checking {os.path.relpath(file_path, INTEL_DIR)}...")
                record_changed = False
                
                # Asana
                for i, s in enumerate(sources.get("asana", [])):
                    if force or is_stale(s.get("last_fetched")):
                        if harvest_asana(s, root):
                            update_frontmatter(file_path, "asana", i, today)
                            stats["refreshed"] += 1
                            record_changed = True
                        else:
                            stats["failed"] += 1
                
                # Jira
                for i, s in enumerate(sources.get("jira", [])):
                    if force or is_stale(s.get("last_fetched")):
                        if harvest_jira(s, root, auth):
                            update_frontmatter(file_path, "jira", i, today)
                            stats["refreshed"] += 1
                            record_changed = True
                        else:
                            stats["failed"] += 1
                
                if not record_changed:
                    stats["skipped"] += 1
                    
            except Exception as e:
                print(f"  ❌ Error processing {file}: {e}")
                stats["failed"] += 1

    print(f"\n✅ Harvest complete.")
    print(f"   Checked:   {stats['checked']}")
    print(f"   Refreshed: {stats['refreshed']}")
    print(f"   Failed:    {stats['failed']}")
    print(f"   Skipped:   {stats['skipped']}")

if __name__ == "__main__":
    main()
