import os
import sys
import json
try:
    import requests
except ImportError:
    print("❌ Error: 'requests' library not installed. Run: pip3 install requests", file=sys.stderr)
    sys.exit(1)
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "../manifest.json")))
OUTPUT_PATH = os.path.join(REPO_ROOT, "inputs/raw/asana_all_projects.json")

ASANA_API_URL = (
    "https://app.asana.com/api/1.0/teams/1208693459152259/projects"
    "?completed=false"
    "&opt_fields=name,gid,permalink_url"
    ",current_status_update,current_status_update.status_type"
    ",custom_fields,custom_fields.gid,custom_fields.name"
    ",custom_fields.enum_value,custom_fields.enum_value.gid"
    ",custom_fields.date_value,custom_fields.text_value,custom_fields.display_value"
)


def fetch_asana_projects():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] step_0_asana_refresh.py")

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
        all_projects.extend(batch)
        print(f"  → {len(batch)} projects received (total so far: {len(all_projects)})")

        # Pagination: follow next_page.uri if present
        next_page = body.get("next_page")
        url = next_page.get("uri") if next_page else None

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(all_projects, f, indent=2)

    print(f"✅ step_0_asana_refresh Complete: {len(all_projects)} projects written to {OUTPUT_PATH}")


if __name__ == "__main__":
    fetch_asana_projects()
