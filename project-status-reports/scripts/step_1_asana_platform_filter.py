import json

def filter_platform_projects(input_file, output_file):
    PLATFORM_TEAM_GID = "1208820967756799"
    TEAM_FIELD_GID = "1208820967756795"
    
    with open(input_file, 'r') as f:
        data = json.load(f)
        
    filtered = []
    for p in data:
        # Check custom fields for Platform Team GID
        team_field = next((f for f in p.get('custom_fields', []) if f['gid'] == TEAM_FIELD_GID), None)
        if team_field and team_field.get('enum_value', {}).get('gid') == PLATFORM_TEAM_GID:
            if p.get('current_status_update', {}).get('status_type') != "complete":
                filtered.append(p)
                
    with open(output_file, 'w') as f:
        json.dump(filtered, f, indent=2)

# Gemma/Claude will execute this via the shell/python MCP