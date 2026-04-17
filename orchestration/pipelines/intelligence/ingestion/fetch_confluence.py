#!/usr/bin/env python3
import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth
import re

# Standard Vault Paths
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

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

def fetch_confluence_page(url):
    env = load_env()
    email = env.get("ATLASSIAN_USER_EMAIL")
    token = env.get("ATLASSIAN_API_TOKEN")
    
    if not email or not token:
        print("Error: Missing ATLASSIAN_USER_EMAIL or ATLASSIAN_API_TOKEN in .env")
        return None

    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}
    
    # Handle tiny links vs full URLs
    if "/wiki/x/" in url:
        # Resolving Tiny Link
        print(f"Resolving Tiny Link: {url}", file=sys.stderr)
        resp = requests.get(url, auth=auth, allow_redirects=True)
        url = resp.url
        print(f"Resolved to: {url}", file=sys.stderr)

    # Extract Page ID or Title from URL
    match = re.search(r'pages/(\d+)', url)
    if not match:
        print(f"Error: Could not extract Page ID from {url}", file=sys.stderr)
        return None
    
    page_id = match.group(1)
    # ...
    # Wait, I'll just change all print statements to stderr.
    api_url = f"https://casecommons.atlassian.net/wiki/api/v2/pages/{page_id}?body-format=storage"

    print(f"Fetching API: {api_url}", file=sys.stderr)
    resp = requests.get(api_url, auth=auth, headers=headers)
    
    if resp.status_code != 200:
        print(f"Error: Confluence API returned {resp.status_code}", file=sys.stderr)
        return None
        
    return resp.json()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_confluence.py <url>")
        sys.exit(1)
    
    page_data = fetch_confluence_page(sys.argv[1])
    if page_data:
        # Output to stdout for the next step in the pipeline
        print(json.dumps(page_data, indent=2))
