import os
import sys
import json
try:
    import requests
except ImportError:
    print("❌ Error: 'requests' library not installed. Run: pip3 install requests", file=sys.stderr)
    sys.exit(1)
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../.."))
OUTPUT_PATH = os.path.join(REPO_ROOT, "reports/asana/raw/all_projects.json")

def _load_dotenv():
    env_path = os.path.join(REPO_ROOT, ".env")
    if not os.path.exists(env_path): return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line: continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

ASANA_API_URL = (
    "https://app.asana.com/api/1.0/teams/1208693459152259/projects"
    "?completed=false"
    "&opt_fields=name,gid,permalink_url"
    ",current_status_update,current_status_update.status_type,current_status_update.title,current_status_update.text"
    ",custom_fields,custom_fields.gid,custom_fields.name"
    ",custom_fields.enum_value,custom_fields.enum_value.gid"
    ",custom_fields.date_value,custom_fields.text_value,custom_fields.display_value"
)


def fetch_asana_projects():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] fetch_asana_projects.py")
    _load_dotenv()

    token = os.environ.get("ASANA_API_TOKEN")
    if not token:
        print("❌ Error: ASANA_API_TOKEN environment variable not set.", file=sys.stderr)
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    all_projects = []
    url = ASANA_API_URL

    while url:
        print(f"  Fetching: {url[:80]}...")
        resp = requests.get(url, headers=headers)

        if resp.status_code == 401:
            print("❌ Error: Authentication failed (HTTP 401). Check your ASANA_API_TOKEN.", file=sys.stderr)
            sys.exit(1)
        elif resp.status_code != 200:
            print(f"❌ Error: Asana API returned HTTP {resp.status_code} — {resp.text}", file=sys.stderr)
            sys.exit(1)

        body = resp.json()
        batch = body.get("data", [])
        
        # MINIFICATION: Only keep fields required for status reporting and intelligence
        WHITELIST_GIDS = {
            "1208820967756795", "1208822149019495", "1211631943113717",
            "1210467277124544", "1208818118032458", "1210909549820601",
            "1208818124273418", "1208818005809198", "1211632504010030",
            "1211632748689814"
        }
        
        minified_batch = []
        for p in batch:
            mini_p = {
                "gid": p.get("gid"),
                "name": p.get("name"),
                "permalink_url": p.get("permalink_url"),
                "current_status_update": p.get("current_status_update")
            }
            # Filter custom fields
            custom_fields = p.get("custom_fields", [])
            mini_p["custom_fields"] = [
                f for f in custom_fields if f.get("gid") in WHITELIST_GIDS
            ]
            minified_batch.append(mini_p)

        all_projects.extend(minified_batch)
        print(f"  → {len(batch)} projects received (minified total: {len(all_projects)})")

        # Pagination: follow next_page.uri if present
        next_page = body.get("next_page")
        url = next_page.get("uri") if next_page else None

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(all_projects, f)

    print(f"✅ 01_fetch_projects Complete: {len(all_projects)} projects written to {OUTPUT_PATH}")


if __name__ == "__main__":
    fetch_asana_projects()
