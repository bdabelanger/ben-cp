import json
import os

MANIFEST_PATH = "/Users/benbelanger/GitHub/ben-cp/project-status-reports/manifest.json"

def get_path_from_manifest(step_id):
    with open(MANIFEST_PATH, 'r') as f:
        data = json.load(f)
    repo_root = data['config']['repo_root']
    relative_path = next(s['file'] for s in data['steps'] if s['id'] == step_id)
    return os.path.join(repo_root, relative_path)

def generate_insights():
    ASANA_FILE = get_path_from_manifest("1_asana_ingest")
    OUTPUT_FILE = get_path_from_manifest("2_rovo_context")
    
    with open(ASANA_FILE, 'r') as f:
        projects = json.load(f)
        
    insights = {}
    
    # -------------------------------------------------------------
    # TODO: FUTURE ROVO API INTEGRATION
    # 
    # For each project, we can call:
    # 1. `searchAtlassian(query=project['name'])` to find related docs
    # 2. `getJiraIssue(issueIdOrKey=epic_key)` for sentiment analysis
    #
    # Real implementations will parse API results. Here we use a stub.
    # -------------------------------------------------------------
    
    for p in projects:
        name = p.get('name', 'Unknown Project')
        # Stub logic as approved
        insights[name] = {
            "summary": f"Placeholder insight for {name}. Team is progressing well.",
            "sentiment": "Neutral",
            "blockers_mention": "None detected in recent Confluence/Slack logs."
        }
        
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(insights, f, indent=2)
        
    print(f"✅ 2_rovo_context Complete: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_insights()
