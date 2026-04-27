#!/usr/bin/env python3
"""
dream/run.py — Nightly audit cycle.
Runs data pipelines, then 13 vault health sensors, and consolidates
everything into the daily report.
Output: reports/dream/report.md
"""
import os, sys, json, re, subprocess, importlib.util
from datetime import datetime

VAULT_ROOT   = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SENSORS_DIR  = os.path.join(os.path.dirname(__file__), 'scripts')
OUTPUTS_DIR  = os.path.join(VAULT_ROOT, 'reports', 'dream', 'data', 'raw')
REPORT_DIR   = os.path.join(VAULT_ROOT, 'reports', 'dream')
REPORT_MD    = os.path.join(REPORT_DIR, 'report.md')

SENSORS = [
    'pulse', 'links', 'frontmatter', 'drift',
    'handoffs', 'index', 'agents',
    'tasks', 'changelog', 'context', 'access',
    'paths', 'scripts',
]

PIPELINES = [
    {
        'name': 'status',
        'script': os.path.join(VAULT_ROOT, 'skills', 'status', 'scripts', 'run.py'),
        'report': 'reports/status/report.md',
        'label': 'Platform Status',
    },
    {
        'name': 'tasks',
        'script': os.path.join(VAULT_ROOT, 'skills', 'tasks', 'run.py'),
        'report': 'reports/tasks/report.md',
        'label': 'My Tasks',
    },
    {
        'name': 'intelligence-harvest',
        'script': os.path.join(VAULT_ROOT, 'skills', 'intelligence', 'run.py'),
        'args': ['--harvest'],
        'report': None,
        'label': 'Intelligence Harvest',
    },
    {
        'name': 'intelligence-scan',
        'script': os.path.join(VAULT_ROOT, 'skills', 'intelligence', 'run.py'),
        'args': ['--scan'],
        'report': None,
        'label': 'Intelligence Scan',
    },
]

# ---------------------------------------------------------------------------
# Pipelines
# ---------------------------------------------------------------------------

def run_pipelines():
    results = {}
    for p in PIPELINES:
        name = p['name']
        print(f'  ⚙️  {name} pipeline…', end=' ', flush=True)
        try:
            cmd = ['python3', p['script']] + p.get('args', [])
            proc = subprocess.run(
                cmd,
                capture_output=True, text=True, timeout=180,
                cwd=VAULT_ROOT,
            )
            ok = proc.returncode == 0
            results[name] = {'ok': ok, 'stdout': proc.stdout, 'error': None if ok else proc.stderr[-300:]}
            print('✅' if ok else '⚠️  failed')
        except subprocess.TimeoutExpired:
            results[name] = {'ok': False, 'error': 'timeout'}
            print('⏱️  timeout')
        except Exception as e:
            results[name] = {'ok': False, 'error': str(e)}
            print(f'❌ {e}')
    return results


def _read_report(rel_path):
    path = os.path.join(VAULT_ROOT, rel_path)
    if not os.path.exists(path):
        return None
    with open(path, errors='replace') as f:
        return f.read()


def _summarise_status(content):
    """Extract the numbered project list from ## 📋 Summary."""
    lines = []
    in_section = False
    for line in content.splitlines():
        if re.match(r'^##\s+.*Summary', line):
            in_section = True
            continue
        if in_section:
            if line.startswith('##'):
                break
            if re.match(r'^\d+\.', line):
                # Strip inline Jira/stage markup for brevity
                clean = re.sub(r'\|\|.*', '', line).strip()
                clean = re.sub(r'\[stage:([^\]]+)\]', r'(\1)', clean)
                lines.append(clean)
    return lines


def _summarise_tasks(content):
    """Extract sync line and overdue count."""
    sync_line = ''
    overdue_count = 0
    for line in content.splitlines():
        if line.startswith('_Last synced'):
            sync_line = line.strip('_').strip()
        if line.startswith('- ') and 'due 20' in line:
            overdue_count += 1
    return sync_line, overdue_count


def build_pipeline_section(pipeline_results):
    lines = ['', '## Pipeline Reports', '']
    for p in PIPELINES:
        name = p['name']
        result = pipeline_results.get(name, {})
        icon = '✅' if result.get('ok') else '⚠️'
        lines.append(f'### {icon} {p["label"]}')
        lines.append('')

        if not p.get('report'):
            # Pipeline with no report file — show stdout summary
            stdout = pipeline_results[name].get('stdout', '').strip()
            if stdout:
                for line in stdout.splitlines()[-5:]:
                    lines.append(f'`{line}`')
            lines.append('')
            continue

        content = _read_report(p['report'])
        if content:
            lines.append(f'[Full report]({p["report"]})')
        else:
            lines.append('_Report not found._')
        lines.append('')

        if not content:
            continue

        if name == 'status':
            projects = _summarise_status(content)
            if projects:
                for proj in projects:
                    lines.append(proj)
            else:
                lines.append('_No summary available._')

        elif name == 'tasks':
            sync_line, overdue = _summarise_tasks(content)
            if sync_line:
                lines.append(f'_{sync_line}_')
            if overdue:
                lines.append(f'**{overdue} overdue tasks** — see full report for details.')
            else:
                lines.append('No overdue tasks.')

        lines.append('')
    return lines


# ---------------------------------------------------------------------------
# Sensors
# ---------------------------------------------------------------------------

def load_sensor(name):
    path = os.path.join(SENSORS_DIR, f'{name}.py')
    spec = importlib.util.spec_from_file_location(name, path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def run_sensors():
    results = {}
    failures = []
    for name in SENSORS:
        try:
            mod = load_sensor(name)
            report = mod.run()
            results[name] = {'status': 'OK', 'report': report}
        except Exception as e:
            results[name] = {'status': 'FAILED', 'error': str(e)}
            failures.append(name)
            print(f'  ❌ {name} failed: {e}')
    return results, failures

def sensor_status_line(name, data):
    if data['status'] == 'FAILED':
        return f'| {name} | 🔴 FAILED | {data.get("error", "")} |'
    r = data['report']
    summary = r.get('summary', {})
    parts = []
    for k, v in summary.items():
        if isinstance(v, int) and v > 0:
            parts.append(f'{v} {k.replace("_", " ")}')
        elif isinstance(v, str) and v not in ('OK',):
            parts.append(f'{k}: {v}')
    detail = ', '.join(parts) if parts else 'clean'

    # subdirectory_changelogs is informational — per-skill changelogs are expected
    issue_parts = [p for p in parts if 'scanned' not in p.lower() and 'total' not in p.lower() and 'subdirectory changelogs' not in p.lower()]
    scanned_count = summary.get('files_scanned', summary.get('skills_checked', 1))

    finding_count = 0
    failure_keys = {'ghost_links', 'issues', 'findings', 'red_flags', 'version_issues', 'drift_findings', 'boundary_violations'}
    for key in failure_keys:
        val = r.get(key)
        if isinstance(val, list):
            finding_count += len(val)
        elif isinstance(val, int):
            finding_count += val

    if not issue_parts and finding_count == 0:
        icon = '🟢'
    elif scanned_count > 0 and (finding_count / scanned_count) > 0.20:
        icon = '🔴'
    else:
        icon = '🟡'

    return f'| {name} | {icon} | {detail} |'

def build_highlights(results):
    lines = []
    for name, data in results.items():
        if data['status'] == 'FAILED':
            continue
        r = data['report']
        if name == 'pulse':
            v = r.get('boundary_violations', [])
            if v:
                lines.append(f'- **{len(v)} boundary violations** detected (code/data files in wrong layer)')
            missing = r.get('dirs_missing_index', [])
            if missing:
                lines.append(f'- **{len(missing)} directories** missing `index.md`')
        if name == 'links' and r.get('ghost_links'):
            lines.append(f'- **{len(r["ghost_links"])} ghost links** — broken internal references')
        if name == 'context':
            if r.get('red_flags'):
                lines.append(f'- **{len(r["red_flags"])} files over 750KB** — token economy risk')
            elif r.get('yellow_flags'):
                lines.append(f'- {len(r["yellow_flags"])} files over 250KB (watch list)')
        if name == 'handoffs' and r.get('issues'):
            lines.append(f'- **{len(r["issues"])} handoff issues** — missing sections or stale READY files')
        if name == 'drift' and r.get('findings'):
            lines.append(f'- **{len(r["findings"])} drift findings** — unsanctioned directories')
    return lines or ['- No critical issues detected']


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------

def build_report(results, failures, pipeline_results, start, elapsed):
    today = start.strftime('%Y-%m-%d')
    time_str = start.strftime('%H:%M')
    ok_count = len(SENSORS) - len(failures)

    lines = [
        f'# Dream Report — {today}',
        f'',
        f'**Run:** {time_str} · **Sensors:** {ok_count}/{len(SENSORS)} OK · **Duration:** {elapsed:.1f}s',
        f'',
        f'## Sensor Summary',
        f'',
        f'| Sensor | Status | Detail |',
        f'|--------|--------|--------|',
    ]
    for name in SENSORS:
        lines.append(sensor_status_line(name, results[name]))

    lines += ['', '## Highlights', '']
    lines += build_highlights(results)

    if results.get('context', {}).get('report', {}).get('red_flags'):
        ctx = results['context']['report']
        lines += ['', '## Large Files (>750KB)', '']
        for f in ctx['red_flags'][:5]:
            lines.append(f'- `{f["file"]}` — {f["size_kb"]}KB')

    if results.get('links', {}).get('report', {}).get('ghost_links'):
        lnk = results['links']['report']
        lines += ['', '## Ghost Links (sample)', '']
        for g in lnk['ghost_links'][:10]:
            lines.append(f'- `{g["source"]}` → `{g["link"]}`')

    lines += build_pipeline_section(pipeline_results)

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    start = datetime.now()
    print(f'[{start.strftime("%Y-%m-%d %H:%M:%S")}] dream/run.py')

    print('\n⚙️  Running pipelines…')
    pipeline_results = run_pipelines()

    print('\n🔍 Running sensors…')
    results, failures = run_sensors()
    elapsed = (datetime.now() - start).total_seconds()

    md = build_report(results, failures, pipeline_results, start, elapsed)

    os.makedirs(REPORT_DIR, exist_ok=True)
    with open(REPORT_MD, 'w') as f:
        f.write(md)

    with open(os.path.join(OUTPUTS_DIR, 'dream_run.json'), 'w') as f:
        json.dump({
            'run_date': start.strftime('%Y-%m-%d'),
            'started': start.isoformat(),
            'elapsed_s': round(elapsed, 2),
            'sensors_ok': len(SENSORS) - len(failures),
            'failures': failures,
            'pipelines': {name: r['ok'] for name, r in pipeline_results.items()},
        }, f, indent=2)

    status = '✅' if not failures else '⚠️ '
    print(f'\n{status} dream complete — {len(SENSORS)-len(failures)}/{len(SENSORS)} sensors OK in {elapsed:.1f}s')
    print(f'   Report: {REPORT_MD}')

if __name__ == '__main__':
    main()
