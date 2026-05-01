#!/usr/bin/env python3
import os
import sys

# Standard Repo Paths
# skills/intelligence/02_parse.py -> ../.. -> ben-cp/
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SCHEMA_PATH = os.path.join(REPO_ROOT, "skills/intelligence/schemas/source-to-intelligence-prompt.md")

def parse_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return

    print(f"--- Pipeline: Parser Phase ---")
    print(f"Target: {os.path.basename(file_path)}")
    print(f"Schema: {SCHEMA_PATH}")
    print(f"\n--- INSTRUCTIONS FOR AGENT ---")
    print(f"1. Read the content of: {file_path}")
    print(f"2. Apply the extraction logic defined in the schema above.")
    print(f"3. Use 'add_intelligence' to create the record in the parent directory.")
    print(f"4. Once created, run '03_scan_orphans.py' to verify completion.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 02_parse.py <file_path>")
        sys.exit(1)
    parse_file(sys.argv[1])
