#!/usr/bin/env python3
import os
import glob

# Standard Vault Paths
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
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
            
            source_files = os.listdir(source_dir)
            
            # Check for matches
            available_mds = [f.replace('.md', '').lower() for f in os.listdir(parent_dir) if f.endswith('.md')]
            
            for s_file in source_files:
                if s_file.startswith('.') or s_file == "index.md":
                    continue
                
                # Try to find a match in the parent
                # We check if the basename (without extension) of the source file 
                # matches any of the MD files in the parent.
                basename = os.path.splitext(s_file)[0].lower()
                
                # Loose matching: if basename is IN an MD filename or vice versa
                matched = False
                for md in available_mds:
                    if basename in md or md in basename:
                        matched = True
                        break
                
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
