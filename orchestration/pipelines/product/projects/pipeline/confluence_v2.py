#!/usr/bin/env python3
import os
import sys
import json
from atlassian import Confluence

# Standard Vault Paths
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))

def load_env():
    env_path = os.path.join(REPO_ROOT, ".env")
    env = {}
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line: continue
                key, _, val = line.partition("=")
                env[key.strip()] = val.strip().strip('"').strip("'")
    return env

def get_confluence_client():
    env = load_env()
    email = env.get("ATLASSIAN_USER_EMAIL")
    token = env.get("ATLASSIAN_API_TOKEN")
    url = "https://casecommons.atlassian.net" # Default for this vault
    
    if not email or not token:
        print("Error: Missing credentials in .env", file=sys.stderr)
        return None

    return Confluence(
        url=url,
        username=email,
        password=token,
        cloud=True
    )

def fetch_page_v2(url_or_id):
    confluence = get_confluence_client()
    if not confluence: return None

    # Resolve Tiny Link or Page ID
    page_id = None
    if "/pages/" in url_or_id:
        import re
        match = re.search(r'pages/(\d+)', url_or_id)
        if match: page_id = match.group(1)
    elif "/x/" in url_or_id:
        # The wrapper doesn't directly resolve tiny links via URL parsing, 
        # but we can resolve it via a simple request or use the page title if known.
        # For now, we'll use our previous redirect logic if it's a tiny link.
        import requests
        resp = requests.get(url_or_id, auth=(confluence.username, confluence.password), allow_redirects=True)
        import re
        match = re.search(r'pages/(\d+)', resp.url)
        if match: page_id = match.group(1)
    else:
        page_id = url_or_id # Assume it's a raw ID

    if not page_id:
        print(f"Error: Could not determine Page ID for {url_or_id}", file=sys.stderr)
        return None

    print(f"Fetching Page {page_id}...", file=sys.stderr)
    page = confluence.get_page_by_id(page_id, expand='body.storage,metadata.labels')
    
    # NEW: Also list attachments automatically!
    print(f"Checking for attachments...", file=sys.stderr)
    attachments = confluence.get_attachments_from_content(page_id)
    page['attachments'] = attachments.get('results', [])
    
    return page

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_confluence_v2.py <url_or_id>")
        sys.exit(1)
    
    data = fetch_page_v2(sys.argv[1])
    if data:
        print(json.dumps(data, indent=2))
    else:
        sys.exit(1)
