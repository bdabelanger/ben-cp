import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

SKIP_DIRS = {'.git', '__pycache__', 'node_modules', 'dist', 'src', 'reports',
             'art', 'complete', 'archive', 'archived'}

def collect_md_files(root=None, skip_dirs=None):
    root = root or REPO_ROOT
    skip = skip_dirs or SKIP_DIRS
    files = []
    for dirpath, dirs, fs in os.walk(root):
        dirs[:] = [d for d in dirs if d not in skip and not d.startswith('.')]
        for f in fs:
            if f.endswith('.md'):
                files.append(os.path.join(dirpath, f))
    return files

def get_manifest():
    path = os.path.join(REPO_ROOT, 'reports', 'dream', 'data', 'raw', 'reindex_report.json')
    if os.path.exists(path):
        import json
        try:
            with open(path) as f:
                return json.load(f).get('manifest', {})
        except:
            return {}
    return {}

def get_manifest_files():
    manifest = get_manifest()
    if manifest:
        return [os.path.join(REPO_ROOT, f) for f in manifest.get('files', {}).keys() if f.endswith('.md')]
    return collect_md_files()

def get_manifest_all_files():
    manifest = get_manifest()
    if manifest:
        return [os.path.join(REPO_ROOT, f) for f in manifest.get('files', {}).keys()]
    # Fallback to walk
    all_files = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for f in files:
            all_files.append(os.path.join(root, f))
    return all_files
