#!/usr/bin/env python3
import os
import glob

# Standard Vault Paths
# skills/intelligence/03_scan_orphans.py -> ../.. -> ben-cp/
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INTEL_DIR = os.path.join(REPO_ROOT, "intelligence")

def scan_orphans():
    print(f"--- Intelligence Source Scan ---")
    print(f"Scanning: {INTEL_DIR}")

    orphans = []

    # Walk all directories looking for 'source' folders
    for root, dirs, files in os.walk(INTEL_DIR):
        if 'source' in dirs:
            source_dir = os.path.join(root, 'source')
            parent_dir = root

            # Exclude known template files from orphans
            IGNORE_KEYWORDS = ['template', 'test', 'example', '.DS_Store']

            source_files = os.listdir(source_dir)
            available_mds = [f.replace('.md', '').lower() for f in os.listdir(parent_dir) if f.endswith('.md')]

            for s_file in source_files:
                if s_file.startswith('.') or s_file == "index.md":
                    continue

                # Check for ignore keywords
                if any(keyword in s_file.lower() for keyword in IGNORE_KEYWORDS):
                    continue

                # Try to find a match in the parent
                basename = os.path.splitext(s_file)[0].lower()

                # 1. Filename match (Loose)
                matched = False
                for md in available_mds:
                    if basename == md or basename in md or md in basename:
                        matched = True
                        break

                # 2. Frontmatter 'sources' match
                if not matched:
                    for f in os.listdir(parent_dir):
                        if f.endswith('.md'):
                            md_path = os.path.join(parent_dir, f)
                            try:
                                with open(md_path, 'r', errors='ignore') as mdf:
                                    content = mdf.read()
                                    # Check for source path in content (simple grep-like check)
                                    # This handles 'source/filename' in the frontmatter
                                    if f"source/{s_file}" in content:
                                        matched = True
                                        break
                            except:
                                continue

                if not matched:
                    orphans.append(os.path.join(source_dir, s_file))

    if not orphans:
        print("✅ No orphaned source files found.")
    else:
        print(f"⚠️ Found {len(orphans)} orphaned source file(s):")
        for o in orphans:
            rel = os.path.relpath(o, REPO_ROOT)
            print(f"  - {rel}")

if __name__ == "__main__":
    scan_orphans()
