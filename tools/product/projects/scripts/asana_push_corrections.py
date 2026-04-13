#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
from datetime import datetime

# Asana Field GIDs
GA_FIELD = "1208818124273418"          # date field
BETA_START_FIELD = "1208818118032458"  # date field
GA_MONTH_FIELD = "1210909549820601"    # multi_enum field

# GA Month enum option GIDs (looked up from live Asana data)
GA_MONTH_MAY_26 = "1211441356703319"
GA_MONTH_JUN_26 = "1211441356703320"

def date_val(d):
    """Wrap a date string in the Asana date_value object format."""
    return {"date": d}

# Mapping: Project GID -> { 'name': str, 'fields': { Field GID: Value } }
# Date fields use {"date": "YYYY-MM-DD"} format.
# Multi-enum fields use the enum option GID as the value.
# NOTE: Notes - Tabbed design (1213002343224284) returned 404 — GID needs verification. Skipped.
CORRECTIONS = {
    "1211838817183809": { "name": 'Notes - Bulk "General Notes"',  "fields": { BETA_START_FIELD: date_val("2026-04-23"), GA_FIELD: date_val("2026-05-14") } },
    "1211786365522017": { "name": "Notes - Locked Notes",           "fields": { BETA_START_FIELD: date_val("2026-04-28"), GA_FIELD: date_val("2026-05-14") } },
    "1211757637943244": { "name": "Notes - Bulk Service Notes",     "fields": { BETA_START_FIELD: date_val("2026-04-28"), GA_FIELD: date_val("2026-05-28") } },
    "1211631360190563": { "name": "Service plan datagrid",          "fields": { GA_FIELD: date_val("2026-05-28"), GA_MONTH_FIELD: GA_MONTH_MAY_26 } },
    "1211733450555414": { "name": "Services WLV - Bulk actions",    "fields": { GA_FIELD: date_val("2026-05-28") } },
    "1213496879668016": { "name": "Zapier improvements",            "fields": { GA_FIELD: date_val("2026-06-11") } },
    "1213564552809143": { "name": "VPAT audit",                     "fields": { GA_FIELD: date_val("2026-06-11") } },
    "1210368097846960": { "name": "Notes - Global Notes WLV",       "fields": { GA_FIELD: date_val("2026-07-09") } },
    "1212560621975480": { "name": "Schema migration",               "fields": { GA_FIELD: date_val("2026-07-23") } },
    "1213685097670626": { "name": "Notes - Signing",                "fields": { GA_FIELD: date_val("2026-07-23") } },
    "1213506659163435": { "name": "Portal Client Dashboard",        "fields": { BETA_START_FIELD: date_val("2026-06-11") } },
}

def update_project(project_gid, data_bundle, dry_run=True, token=None):
    name = data_bundle["name"]
    field_map = data_bundle["fields"]
    url = f"https://app.asana.com/api/1.0/projects/{project_gid}"

    custom_fields = dict(field_map)
    payload = {"data": {"custom_fields": custom_fields}}
    data = json.dumps(payload).encode("utf-8")

    if dry_run:
        print(f"[DRY-RUN] {name} ({project_gid}): {json.dumps(custom_fields)}")
        return True

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    req = urllib.request.Request(url, data=data, headers=headers, method="PUT")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Updating {name} ({project_gid})...")
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status in [200, 201]:
                print(f"  ✅ SUCCESS")
                return True
            else:
                print(f"  ❌ FAILED: {resp.status}")
                return False
    except urllib.error.HTTPError as e:
        print(f"  ❌ HTTP ERROR {e.code}: {e.read().decode()}")
        return False
    except Exception as e:
        print(f"  ❌ ERROR: {str(e)}")
        return False

def main():
    dry_run = "--execute" not in sys.argv
    token = os.environ.get("ASANA_API_TOKEN")

    if not dry_run and not token:
        print("❌ Error: ASANA_API_TOKEN not found in environment. Switching to dry-run.")
        dry_run = True

    print(f"--- Asana Project Correction Sync ({'EXECUTE' if not dry_run else 'DRY-RUN'}) ---")
    print(f"⚠️  Skipped: Notes - Tabbed design (GID 1213002343224284 returned 404 — needs verification)\n")

    success_count = 0
    total = len(CORRECTIONS)

    for gid, bundle in CORRECTIONS.items():
        if update_project(gid, bundle, dry_run=dry_run, token=token):
            success_count += 1

    print(f"\nSummary: {success_count}/{total} projects processed successfully.")
    if dry_run:
        print("Run with --execute to commit changes.")

if __name__ == "__main__":
    main()
