import json
import os

MANIFEST_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../manifest.json")
REPO_ROOT = os.path.dirname(os.path.abspath(MANIFEST_PATH))

def get_path_from_manifest(step_id):
    with open(MANIFEST_PATH, 'r') as f:
        data = json.load(f)
    relative_path = next(s['file'] for s in data['steps'] if s['id'] == step_id)
    return os.path.join(REPO_ROOT, relative_path)

def generate_insights():
    ASANA_FILE = get_path_from_manifest("1_asana_ingest")
    OUTPUT_FILE = get_path_from_manifest("3_rovo_context")
    
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
    import datetime
    insights["_metadata"] = {"generated_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(insights, f, indent=2)
        
    print(f"✅ 3_rovo_context Complete: {OUTPUT_FILE}")

if __name__ == "__main__":
    import datetime
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Started step_2_rovo_context.py")
    generate_insights()
