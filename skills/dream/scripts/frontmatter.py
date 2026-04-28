#!/usr/bin/env python3
"""frontmatter.py — Enforce metadata schema and readability standards."""
import os, json, re, yaml
from datetime import datetime
from utils import get_manifest_files

REPO_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(REPO_ROOT, 'reports', 'dream', 'data', 'raw')

SKIP_DIRS  = {'.git', '__pycache__', 'node_modules', 'dist', 'src', 'reports', 'complete', 'archive', 'archived'}
REQUIRED_KEYS = {'title', 'type', 'domain'}
VALID_TYPES = {'index', 'skill', 'intelligence', 'handoff', 'changelog', 'release', 'prd', 'agent', 'task', 'report', 'log', 'session', 'launch_plan', 'run_log', 'shareout', 'source', 'reference', 'governance', 'art', 'design'}

def load_taxonomy_terms():
    """Return set of valid taxonomy labels from intelligence/casebook/taxonomy.md."""
    path = os.path.join(REPO_ROOT, 'intelligence', 'casebook', 'taxonomy.md')
    try:
        with open(path, errors='replace') as f:
            content = f.read()
    except OSError:
        return set()
    terms = set()
    for section in ('## Products', '## Features'):
        m = re.search(rf'{re.escape(section)}\n\n([\s\S]*?)\n---', content)
        if m:
            for row in m.group(1).splitlines():
                if row.startswith('|') and '---' not in row and ('| Product |' not in row) and ('| Feature |' not in row):
                    label = row.split('|')[1].strip()
                    if label:
                        terms.add(label.lower())
    # Also add combined labels like "Cases - Notes", "Admin - Audit Log"
    # These appear in the inference map — extract `backtick` values
    for m in re.finditer(r'`([^`]+)`', content):
        val = m.group(1)
        if ' — ' not in val and val != '*(omit label; do not guess)*':
            terms.add(val.lower())
    return terms

# Removed local collect_md_files, using utils.collect_md_files

def parse_frontmatter(content):
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not m:
        return None, content
    try:
        data = yaml.safe_load(m.group(1))
        return data, content[m.end():]
    except:
        return "MALFORMED", content

def word_count(text):
    return len(re.findall(r'\S+', text))

def run():
    issues = []
    scanned = 0
    taxonomy_terms = load_taxonomy_terms()

    for path in get_manifest_files():
        scanned += 1
        rel = os.path.relpath(path, REPO_ROOT)
        try:
            with open(path, errors='replace') as f:
                content = f.read()
        except OSError:
            continue

        fm_data, body = parse_frontmatter(content)

        if fm_data is None:
            issues.append({"file": rel, "issue": "missing_frontmatter"})
        elif fm_data == "MALFORMED":
            issues.append({"file": rel, "issue": "malformed_frontmatter"})
        else:
            # Field Presence
            missing_keys = REQUIRED_KEYS - set(fm_data.keys() if isinstance(fm_data, dict) else [])
            if missing_keys:
                issues.append({"file": rel, "issue": "missing_keys", "keys": sorted(missing_keys)})
            
            # Type Validation
            if isinstance(fm_data, dict) and 'type' in fm_data and fm_data['type'] not in VALID_TYPES:
                issues.append({"file": rel, "issue": "invalid_type", "value": fm_data['type']})

            # Taxonomy check — intelligence files only
            if rel.startswith('intelligence/') and os.path.basename(path) not in {'index.md', 'changelog.md', 'taxonomy.md'}:
                taxonomy_val = fm_data.get('taxonomy') if isinstance(fm_data, dict) else None
                if taxonomy_val is None:
                    issues.append({"file": rel, "issue": "missing_taxonomy"})
                elif str(taxonomy_val).strip().lower() != 'none':
                    terms = [t.strip() for t in str(taxonomy_val).split(',')]
                    unknown = [t for t in terms if t.lower() not in taxonomy_terms and not any(t.lower() in combo for combo in taxonomy_terms)]
                    if unknown:
                        issues.append({"file": rel, "issue": "unknown_taxonomy_term", "terms": unknown})

        # H1 check: strip code blocks first
        clean_content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        h1_md = re.findall(r'^#\s+(.+)$', clean_content, re.MULTILINE)
        h1_html = re.findall(r'<h1[^>]*>(.*?)</h1>', clean_content, re.DOTALL | re.IGNORECASE)
        h1_count = len(h1_md) + len(h1_html)
        
        if h1_count == 0:
            issues.append({"file": rel, "issue": "no_h1"})
        elif h1_count > 1:
            issues.append({"file": rel, "issue": "multiple_h1", "count": h1_count})

        # Readability: >500 words without H2
        wc = word_count(body if fm_data is not None and fm_data != "MALFORMED" else content)
        if wc > 500:
            h2_md = re.findall(r'^## .+$', content, re.MULTILINE)
            h2_html = re.findall(r'<h2[^>]*>', content, re.IGNORECASE)
            if not h2_md and not h2_html:
                issues.append({"file": rel, "issue": "long_file_no_h2", "words": wc})

    report = {
        "sensor": "frontmatter",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "files_scanned": scanned,
            "issues_found": len(issues),
        },
        "issues": issues,
    }
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'frontmatter_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ frontmatter → {out}")
    return report

if __name__ == '__main__':
    run()
