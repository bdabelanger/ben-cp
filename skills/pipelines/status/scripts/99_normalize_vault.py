#!/usr/bin/env python3
import os
import shutil
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
INTEL_DIR = os.path.join(REPO_ROOT, "intelligence/product/projects/q2")

def slugify(text):
    # Match the filename format: lowercase, hyphens, no special chars
    s = text.lower()
    s = re.sub(r' - ', '-', s)
    s = re.sub(r' ', '-', s)
    s = re.sub(r'[^a-z0-9\-]', '', s)
    return s.strip('-')

def normalize():
    # 1. Clean up the messy directories created by mass_harvest.py
    for d in os.listdir(INTEL_DIR):
        d_path = os.path.join(INTEL_DIR, d)
        if not os.path.isdir(d_path) or d == "archive" or d == "backlog" or d == "source":
            continue
        
        # Detect messy slug (multiple hyphens)
        if "---" in d or "--" in d:
            new_name = re.sub(r'-+', '-', d).strip('-')
            new_path = os.path.join(INTEL_DIR, new_name)
            if d_path != new_path:
                print(f"Renaming {d} -> {new_name}")
                if os.path.exists(new_path):
                    # Merge content
                    for f in os.listdir(d_path):
                        shutil.move(os.path.join(d_path, f), os.path.join(new_path, f))
                    os.rmdir(d_path)
                else:
                    os.rename(d_path, new_path)

    # 2. Match .md files to directories and move them as index.md
    md_files = [f for f in os.listdir(INTEL_DIR) if f.endswith(".md") and f != "index.md" and f != "changelog.md"]
    
    for f in md_files:
        # Extract base name before GID: "project-name-(GID).md"
        match = re.search(r'^(.*?)-\(\d+\)\.md$', f)
        if not match:
            continue
        
        base_name = match.group(1).strip('-')
        target_dir = os.path.join(INTEL_DIR, base_name)
        
        if os.path.exists(target_dir):
            print(f"Moving {f} -> {base_name}/index.md")
            shutil.move(os.path.join(INTEL_DIR, f), os.path.join(target_dir, "index.md"))
            
            # 3. Add links to documentation in the new index.md
            index_path = os.path.join(target_dir, "index.md")
            with open(index_path, "r") as idx:
                content = idx.read()
            
            links_block = "\n## 📚 Internal Documentation\n"
            if os.path.exists(os.path.join(target_dir, "prd.md")):
                links_block += "- [**Product Requirements Document (PRD)**](prd.md)\n"
            if os.path.exists(os.path.join(target_dir, "launch_plan.md")):
                links_block += "- [**Launch Plan**](launch_plan.md)\n"
            
            if "## 📚 Internal Documentation" not in content:
                # Add before "Related:" or at end
                if "Related:" in content:
                    content = content.replace("Related:", links_block + "\nRelated:")
                else:
                    content += "\n" + links_block
                
                with open(index_path, "w") as idx:
                    idx.write(content)

if __name__ == "__main__":
    normalize()
