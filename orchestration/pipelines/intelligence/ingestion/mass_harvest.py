#!/usr/bin/env python3
import os
import sys
import json
import subprocess

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
PROJECTS_PIPELINE_JSON = os.path.join(REPO_ROOT, "inputs/status-reports/processed/asana_active.json")
FETCH_SCRIPT = os.path.join(REPO_ROOT, "orchestration/pipelines/intelligence/ingestion/fetch_confluence.py")
INTEL_DIR = os.path.join(REPO_ROOT, "intelligence/product/roadmap/projects/q2")

def slugify(text):
    import re
    return re.sub(r'[^\w\-]', '-', text.lower()).strip('-')

def run_mass_harvest():
    if not os.path.exists(PROJECTS_PIPELINE_JSON):
        print("Error: Input data not found.")
        return

    with open(PROJECTS_PIPELINE_JSON, 'r') as f:
        projects = json.load(f)

    for p in projects:
        name = p.get('name')
        gid = p.get('gid')
        prd = p.get('prd_link')
        lp = p.get('launch_plan_link')

        if not (prd or lp):
            continue

        # Create project directory
        slug = slugify(name)
        project_dir = os.path.join(INTEL_DIR, f"{slug}")
        os.makedirs(project_dir, exist_ok=True)
        os.makedirs(os.path.join(project_dir, "source"), exist_ok=True)

        print(f"[*] Processing Project: {name}")

        targets = [("PRD", prd, "prd.md"), ("Launch Plan", lp, "launch_plan.md")]
        
        for type_name, url, filename in targets:
            if not url:
                continue
            
            print(f"    Fetching {type_name}: {url}")
            try:
                # Run fetcher
                result = subprocess.run(["python3", FETCH_SCRIPT, url], capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"    Error fetching {type_name}: {result.stderr}")
                    continue
                
                # Parse JSON and get content
                data = json.loads(result.stdout)
                content = data.get('body', {}).get('storage', {}).get('value', '')
                
                # Save as source
                source_path = os.path.join(project_dir, "source", f"{filename.replace('.md', '.txt')}")
                with open(source_path, "w") as sf:
                    sf.write(content)
                
                # Save as codified record (simplified for now, eventually run parser)
                target_path = os.path.join(project_dir, filename)
                with open(target_path, "w") as tf:
                    tf.write(f"# {type_name}: {name}\n\n{content}")
                    
            except Exception as e:
                print(f"    Exception: {str(e)}")

if __name__ == "__main__":
    run_mass_harvest()
