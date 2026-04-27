#!/usr/bin/env python3
"""
dream/run.py — Nightly audit cycle.
Runs all 11 sensors and consolidates results into the daily report.
Output: reports/dream/report.md
"""
import os, sys, json, importlib.util
from datetime import datetime

VAULT_ROOT   = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SENSORS_DIR  = os.path.join(os.path.dirname(__file__), 'sensors')
OUTPUTS_DIR  = os.path.join(VAULT_ROOT, 'reports', 'dream', 'data', 'raw')
REPORT_DIR   = os.path.join(VAULT_ROOT, 'reports', 'dream')
REPORT_MD    = os.path.join(REPORT_DIR, 'report.md')

SENSORS = [
    'pulse', 'links', 'frontmatter', 'drift',
    'handoffs', 'index', 'agents',
    'tasks', 'changelog', 'context', 'access',
    'paths', 'scripts',
]

STATUS_ICON = {'OK': '🟢', 'WARN': '🟡', 'FAILED': '🔴'}

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
    # Build a short summary string from whatever keys exist
    parts = []
    for k, v in summary.items():
        if isinstance(v, int) and v > 0:
            parts.append(f'{v} {k.replace("_", " ")}')
        elif isinstance(v, str) and v not in ('OK',):
            parts.append(f'{k}: {v}')
    detail = ', '.join(parts) if parts else 'clean'
    # Icon logic: only yellow if there are actual issues/findings in the parts
    issue_parts = [p for p in parts if 'scanned' not in p.lower() and 'total' not in p.lower()]
    icon = '🟢' if not issue_parts else '🟡'
    # Override to red if sensor explicitly flagged failures
    failure_keys = {'ghost_links', 'issues', 'findings', 'red_flags', 'version_issues'}
    for key in failure_keys:
        if r.get(key):
            icon = '🔴'
            break
    return f'| {name} | {icon} | {detail} |'

def build_highlights(results):
    lines = []
    for name, data in results.items():
        if data['status'] == 'FAILED':
            continue
        r = data['report']
        # pulse
        if name == 'pulse':
            v = r.get('boundary_violations', [])
            if v:
                lines.append(f'- **{len(v)} boundary violations** detected (code/data files in wrong layer)')
            missing = r.get('dirs_missing_index', [])
            if missing:
                lines.append(f'- **{len(missing)} directories** missing `index.md`')
        # links
        if name == 'links' and r.get('ghost_links'):
            lines.append(f'- **{len(r["ghost_links"])} ghost links** — broken internal references')
        # context
        if name == 'context':
            if r.get('red_flags'):
                lines.append(f'- **{len(r["red_flags"])} files over 750KB** — token economy risk')
            elif r.get('yellow_flags'):
                lines.append(f'- {len(r["yellow_flags"])} files over 250KB (watch list)')
        # handoffs
        if name == 'handoffs' and r.get('issues'):
            lines.append(f'- **{len(r["issues"])} handoff issues** — missing sections or stale READY files')
        # drift
        if name == 'drift' and r.get('findings'):
            lines.append(f'- **{len(r["findings"])} drift findings** — unsanctioned directories')
    return lines or ['- No critical issues detected']

def build_report(results, failures, start, elapsed):
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

    # Append top red-flag files from context sensor
    ctx = results.get('context', {}).get('report', {})
    if ctx.get('red_flags'):
        lines += ['', '## Large Files (>750KB)', '']
        for f in ctx['red_flags'][:5]:
            lines.append(f'- `{f["file"]}` — {f["size_kb"]}KB')

    # Append ghost links sample
    lnk = results.get('links', {}).get('report', {})
    if lnk.get('ghost_links'):
        lines += ['', '## Ghost Links (sample)', '']
        for g in lnk['ghost_links'][:10]:
            lines.append(f'- `{g["source"]}` → `{g["link"]}`')

    return '\n'.join(lines)

def main():
    start = datetime.now()
    print(f'[{start.strftime("%Y-%m-%d %H:%M:%S")}] dream/run.py')

    results, failures = run_sensors()
    elapsed = (datetime.now() - start).total_seconds()

    md = build_report(results, failures, start, elapsed)

    os.makedirs(REPORT_DIR, exist_ok=True)
    with open(REPORT_MD, 'w') as f:
        f.write(md)

    # Write run log
    with open(os.path.join(OUTPUTS_DIR, 'dream_run.json'), 'w') as f:
        json.dump({
            'run_date': start.strftime('%Y-%m-%d'),
            'started': start.isoformat(),
            'elapsed_s': round(elapsed, 2),
            'sensors_ok': len(SENSORS) - len(failures),
            'failures': failures,
        }, f, indent=2)

    status = '✅' if not failures else '⚠️ '
    print(f'\n{status} dream complete — {len(SENSORS)-len(failures)}/{len(SENSORS)} sensors OK in {elapsed:.1f}s')
    print(f'   Report: {REPORT_MD}')

if __name__ == '__main__':
    main()
