import os
import sys
import json

# Standard Vault Paths
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
INTEL_DIR = os.path.join(REPO_ROOT, "intelligence")

# Paths to Project Pipeline Outputs
PROJECTS_PIPELINE_JSON = os.path.join(REPO_ROOT, "inputs/status-reports/processed/asana_active.json")

def harvest_links():
    """
    Scans the processed Asana data from the Projects pipeline
    to identify documentation links for harvesting.
    """
    if not os.path.exists(PROJECTS_PIPELINE_JSON):
        print(f"Error: Projects Pipeline data not found at {PROJECTS_PIPELINE_JSON}")
        return

    with open(PROJECTS_PIPELINE_JSON, 'r') as f:
        projects = json.load(f)

    print(f"--- Pipeline: Link-Driven Harvester ---")
    print(f"Scanning {len(projects)} projects for documentation seeds...")
    
    docs_to_fetch = []

    for p in projects:
        name = p.get('name')
        prd = p.get('prd_link')
        lp = p.get('launch_plan_link')

        if prd or lp:
            print(f"  [+] Project: {name}")
            if prd:
                print(f"      Found PRD: {prd}")
                docs_to_fetch.append({"project": name, "url": prd, "type": "PRD"})
            if lp:
                print(f"      Found Launch Plan: {lp}")
                docs_to_fetch.append({"project": name, "url": lp, "type": "Launch Plan"})
                    
    print(f"\n--- RESULTS: Found {len(docs_to_fetch)} document(s) for harvesting. ---")
    if docs_to_fetch:
        print("NEXT: Execute 'fetch_confluence_pages' based on this seed list.")

if __name__ == "__main__":
    harvest_links()
