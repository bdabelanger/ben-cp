"""
Converts the platform report markdown into a self-contained, styled HTML file.
No external dependencies — uses only stdlib + a regex-based md→html pass.
"""

import re
from datetime import datetime

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg:        #f9f9fb;
    --surface:   #ffffff;
    --border:    #e2e2e8;
    --text:      #1a1a2e;
    --muted:     #6b6b80;
    --accent:    #4f6ef7;
    --done:      #22c55e;
    --progress:  #4f6ef7;
    --todo:      #e2e2e8;
    --radius:    10px;
    --shadow:    0 2px 8px rgba(0,0,0,0.07);
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg:      #0f0f17;
        --surface: #1a1a26;
        --border:  #2e2e42;
        --text:    #e8e8f0;
        --muted:   #8888a8;
        --todo:    #2e2e42;
        --shadow:  0 2px 8px rgba(0,0,0,0.4);
    }
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    padding: 2rem 1rem;
}

.container {
    max-width: 860px;
    margin: 0 auto;
}

/* ---------- typography ---------- */
h1 { font-size: 1.75rem; font-weight: 700; margin-bottom: 0.25rem; }
h2 { font-size: 1.2rem;  font-weight: 700; margin: 2rem 0 0.75rem;
     padding-bottom: 0.4rem; border-bottom: 2px solid var(--border); }
h3 { font-size: 1rem;    font-weight: 600; margin: 1.25rem 0 0.4rem; }
p  { margin: 0.4rem 0; }
a  { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
ul { padding-left: 1.4rem; margin: 0.3rem 0; }
li { margin: 0.15rem 0; }
strong { font-weight: 600; }
table { border-collapse: collapse; width: 100%; margin: 0.5rem 0 1rem; font-size: 0.88rem; }
th { text-align: left; padding: 0.3rem 0.75rem; font-weight: 600; color: var(--muted); font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.04em; border-bottom: 2px solid var(--border); }
td { text-align: left; padding: 0.35rem 0.75rem; border-bottom: 1px solid var(--border); }
tr:last-child td { border-bottom: none; }

/* ---------- header card ---------- */
.report-header {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow);
}
.report-header .subtitle {
    font-size: 0.82rem;
    color: var(--muted);
    margin-top: 0.2rem;
}

/* ---------- project cards ---------- */
.project-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.1rem 1.3rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow);
}
.project-card h3 { margin-top: 0; font-size: 1rem; }

/* ---------- progress bar ---------- */
.progress-wrap {
    display: flex;
    height: 10px;
    border-radius: 6px;
    overflow: hidden;
    background: var(--todo);
    margin: 0.5rem 0;
    gap: 1px;
}
.prog-done     { background: var(--done); }
.prog-progress { background: var(--progress); }
.prog-todo     { background: var(--todo); }

/* ---------- time bar ---------- */
.time-bar-wrap {
    display: flex;
    height: 10px;
    border-radius: 6px;
    overflow: hidden;
    background: var(--todo);
    margin: 0.3rem 0;
}
.time-actual           { background: var(--accent); }
.time-actual-over      { background: #ef4444; }
.time-remaining        { background: #1a237e; }
.time-remaining-over   { background: #ef4444; }

/* ---------- badge / pill ---------- */
.badge {
    display: inline-block;
    padding: 0.1rem 0.55rem;
    border-radius: 999px;
    font-size: 0.73rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.badge-backlog    { background: #f3f4f6; color: #4b5563; }
.badge-discovery  { background: #ede9fe; color: #6d28d9; }
.badge-dev        { background: #cffafe; color: #0e7490; }
.badge-qa         { background: #fef3c7; color: #b45309; }
.badge-uat        { background: #fefce8; color: #854d0e; }
.badge-beta       { background: #d1fae5; color: #065f46; }
.badge-ga         { background: #dcfce7; color: #166534; }
.badge-study      { background: #ffedd5; color: #9a3412; }
.badge-onhold     { background: #dbeafe; color: #1e40af; }
.stat-row      { font-size: 0.85rem; color: var(--muted); margin: 0.2rem 0; }

@media (prefers-color-scheme: dark) {
    .badge-backlog   { background: #1f2937; color: #9ca3af; }
    .badge-discovery { background: #2e1065; color: #c4b5fd; }
    .badge-dev       { background: #164e63; color: #67e8f9; }
    .badge-qa        { background: #451a03; color: #fcd34d; }
    .badge-uat       { background: #422006; color: #fde68a; }
    .badge-beta      { background: #064e3b; color: #6ee7b7; }
    .badge-ga        { background: #14532d; color: #86efac; }
    .badge-study     { background: #431407; color: #fdba74; }
    .badge-onhold    { background: #1e3a8a; color: #93c5fd; }
}

/* ---------- milestone list ---------- */
.milestones { list-style: none; padding: 0; margin: 0.4rem 0; }
.milestones li { font-size: 0.85rem; margin: 0.15rem 0; }

/* ---------- issue list ---------- */
.issue-list { list-style: none; padding: 0; margin: 0.4rem 0 0; }
.issue-list li {
    font-size: 0.82rem;
    padding: 0.25rem 0;
    border-top: 1px solid var(--border);
    display: flex;
    gap: 0.5rem;
    align-items: baseline;
    flex-wrap: wrap;
}
.issue-list li:first-child { border-top: none; }
.issue-key { font-weight: 600; white-space: nowrap; }
.issue-meta { color: var(--muted); font-size: 0.78rem; white-space: nowrap; }
.issue-meta-row { font-size: 0.78rem; color: var(--muted); margin-top: 0.15rem; }

/* ---------- sidebar layout ---------- */
.report-layout {
    display: flex;
    gap: 1.5rem;
    align-items: flex-start;
}
.report-main { flex: 1; min-width: 0; }
.report-sidebar {
    width: 240px;
    flex-shrink: 0;
    position: sticky;
    top: 1.5rem;
}
.report-sidebar h2 {
    font-size: 0.95rem;
    margin-top: 0;
    border-bottom-width: 1px;
}
.report-sidebar p,
.report-sidebar table { font-size: 0.82rem; }
.report-sidebar th { font-size: 0.72rem; }
.report-sidebar td,
.report-sidebar th { padding: 0.25rem 0.5rem; }

@media (max-width: 800px) {
    .report-layout { flex-direction: column; }
    .report-sidebar { width: 100%; position: static; }
}

/* ---------- footer ---------- */
.footer { margin-top: 2.5rem; font-size: 0.78rem; color: var(--muted); text-align: right; }

/* ---------- code / mono ---------- */
code {
    font-family: "SF Mono", "Fira Code", Menlo, Consolas, monospace;
    font-size: 0.82rem;
    background: var(--border);
    padding: 0.1rem 0.35rem;
    border-radius: 4px;
}
"""

# ---------------------------------------------------------------------------
# Markdown → HTML (lightweight, purpose-built for this report's output)
# ---------------------------------------------------------------------------

def _md_inline(text):
    """Convert inline markdown (links, bold, code, emoji-safe) to HTML."""
    # [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # **bold**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # `code`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text


def _stage_badge(stage):
    cls = {
        "GA":        "badge-ga",
        "Beta":      "badge-beta",
        "In QA":     "badge-qa",
        "In UAT":    "badge-uat",
        "Development": "badge-dev",
        "Discovery": "badge-discovery",
        "Study":     "badge-study",
        "On hold":   "badge-onhold",
        "Backlog":   "badge-backlog",
    }.get(stage, "badge-backlog")
    return f'<span class="badge {cls}">{stage}</span>'


def _progress_bar_html(bar_text):
    """
    Parse `▓▓▒▒░░ 3 done · 2 in progress · 1 to do` into an HTML bar + label.
    Falls back to plain text if pattern not matched.
    """
    m = re.search(r'(\d+)\s+done[^·]*·\s*(\d+)\s+in progress[^·]*·\s*(\d+)\s+to do', bar_text)
    if not m:
        return f"<p><code>{bar_text}</code></p>"
    done, inp, todo = int(m.group(1)), int(m.group(2)), int(m.group(3))
    total = done + inp + todo or 1
    dp = done / total * 100
    ip = inp / total * 100
    tp = todo / total * 100
    bar = (f'<div class="progress-wrap">'
           f'<div class="prog-done" style="width:{dp:.1f}%"></div>'
           f'<div class="prog-progress" style="width:{ip:.1f}%"></div>'
           f'<div class="prog-todo" style="width:{tp:.1f}%"></div>'
           f'</div>')
    label = f'<span class="stat-row">{done} done &nbsp;·&nbsp; {inp} in progress &nbsp;·&nbsp; {todo} to do</span>'
    return bar + label


def _time_bar_html(bar_text):
    """
    Parse `60.0d estimated · 10.0d actual · 25.0d remaining (42%)` into a 3-segment HTML bar + label.
    Segments: actual (blue/red) | remaining (light-blue/red) | slack (gray background).
    Bar width = max(estimated, actual + remaining) so it always tells the full story.
    """
    # Strip leading emoji prefix before parsing numbers
    clean = re.sub(r'^[⚠️👀❌\s]+', '', bar_text).strip()

    m = re.search(
        r'([\d.]+)d\s+estimated\s*·\s*([\d.]+)d\s+actual\s*·\s*([\d.]+)d\s+remaining\s*\((\d+)%\)',
        clean
    )
    if not m:
        return f"<p><code>{bar_text}</code></p>"

    est, act, rem, pct = float(m.group(1)), float(m.group(2)), float(m.group(3)), int(m.group(4))

    actual_over    = act > est                  # actual alone blew the budget → ❌
    combined_over  = (act + rem) > est          # on track to blow the budget  → ⚠️

    # Symbol: ❌ wins if actual is already over, otherwise ⚠️ for projected overage
    if actual_over:
        symbol = "❌ "
    elif combined_over:
        symbol = "⚠️ "
    elif pct >= 90:
        symbol = "👀 "
    else:
        symbol = ""

    # Bar total = max(est, act+rem) so overages extend naturally
    total = max(est, act + rem) or 1
    actual_pct    = act / total * 100
    remaining_pct = rem / total * 100

    actual_cls    = "time-actual-over" if actual_over    else "time-actual"
    remaining_cls = "time-remaining-over" if combined_over else "time-remaining"

    bar = (f'<div class="time-bar-wrap">'
           f'<div class="{actual_cls}" style="width:{actual_pct:.1f}%"></div>'
           f'<div class="{remaining_cls}" style="width:{remaining_pct:.1f}%"></div>'
           f'</div>')
    label = (f'<span class="stat-row">{symbol}'
             f'{est:.1f}d estimated &nbsp;·&nbsp; {act:.1f}d actual &nbsp;·&nbsp; {rem:.1f}d remaining ({pct}%)'
             f'</span>')
    return bar + label


def md_to_html(md: str) -> str:
    """
    Convert the platform report markdown to structured HTML.
    Handles the specific patterns this report generates; falls back to
    simple paragraph rendering for anything unrecognised.
    """
    lines = md.splitlines()
    html_parts = []
    i = 0
    in_ul = False
    in_ol = False
    in_table = False
    in_project = False

    def close_ul():
        nonlocal in_ul
        if in_ul:
            html_parts.append("</ul>")
            in_ul = False

    def close_ol():
        nonlocal in_ol
        if in_ol:
            html_parts.append("</ol>")
            in_ol = False

    def close_table():
        nonlocal in_table
        if in_table:
            html_parts.append("</tbody></table>")
            in_table = False

    def close_project():
        nonlocal in_project
        if in_project:
            html_parts.append("</div>")  # .project-card
            in_project = False

    def close_all():
        close_ul(); close_ol(); close_table()

    while i < len(lines):
        line = lines[i]

        # H1 — report title → header card
        if line.startswith("# "):
            close_ul(); close_ol(); close_project()
            title = _md_inline(line[2:])
            subtitle = f'Generated {datetime.now().strftime("%B %d, %Y at %H:%M")}'
            html_parts.append(
                f'<div class="report-header">'
                f'<h1>{title}</h1>'
                f'<div class="subtitle">{subtitle}</div>'
                f'</div>'
            )
            i += 1; continue

        # H2 — section heading
        if line.startswith("## "):
            close_ul(); close_ol(); close_project()
            heading = _md_inline(line[3:])
            html_parts.append(f'<h2>{heading}</h2>')
            i += 1; continue

        # H3 — project card header
        if line.startswith("### "):
            close_ul(); close_ol(); close_project()
            # Extract stage badge from last · segment, then strip it from heading text
            stage_m = re.search(r'·\s+([^··]+)\s*$', line)
            stage_html = _stage_badge(stage_m.group(1).strip()) if stage_m else ""
            heading_text = re.sub(r'\s*·\s*[^··]+\s*$', '', line[4:]) if stage_m else line[4:]
            heading = _md_inline(heading_text)
            html_parts.append(
                f'<div class="project-card">'
                f'<h3>{heading} {stage_html}</h3>'
            )
            in_project = True
            i += 1; continue

        # Time bar line (backtick-wrapped containing time data) — check BEFORE progress bar
        if line.startswith("`") and ("d actual" in line or "d estimated" in line or "d logged" in line or "no time" in line):
            close_ul()
            inner = line.strip("`").strip()
            html_parts.append(_time_bar_html(inner))
            i += 1; continue

        # Progress bar line (backtick-wrapped containing ▓/▒/░)
        if line.startswith("`") and any(c in line for c in "▓▒░"):
            close_ul()
            inner = line.strip("`").strip()
            html_parts.append(_progress_bar_html(inner))
            i += 1; continue

        # Generic backtick code line
        if line.startswith("`") and line.endswith("`"):
            close_ul()
            inner = line[1:-1]
            html_parts.append(f'<p><code>{inner}</code></p>')
            i += 1; continue

        # Stat-row line (~~text)
        if line.startswith("~~"):
            close_ul(); close_ol()
            html_parts.append(f'<p class="stat-row">{_md_inline(line[2:])}</p>')
            i += 1; continue

        # Ordered list item (1. 2. etc.)
        if re.match(r'^\d+\. ', line):
            close_ul()
            if not in_ol:
                html_parts.append('<ol>')
                in_ol = True
            content = _md_inline(re.sub(r'^\d+\. ', '', line))
            html_parts.append(f'<li>{content}</li>')
            i += 1; continue

        # Table separator row (|---|---| etc.) — skip, just marks thead boundary
        if line.startswith('|') and re.match(r'^[\|\-\s:]+$', line):
            i += 1; continue

        # Table data/header row
        if line.startswith('|'):
            close_ul(); close_ol()
            cells = [c.strip() for c in line.strip('|').split('|')]
            next_line = lines[i + 1] if i + 1 < len(lines) else ""
            is_header = bool(re.match(r'^[\|\-\s:]+$', next_line))
            if is_header:
                close_table()
                html_parts.append(
                    '<table><thead><tr>'
                    + ''.join(f'<th>{_md_inline(c)}</th>' for c in cells)
                    + '</tr></thead><tbody>'
                )
                in_table = True
            else:
                if not in_table:
                    html_parts.append('<table><tbody>')
                    in_table = True
                html_parts.append(
                    '<tr>' + ''.join(f'<td>{_md_inline(c)}</td>' for c in cells) + '</tr>'
                )
            i += 1; continue

        # Bullet list item
        if re.match(r'^[\*\-] ', line) or re.match(r'^\* ', line):
            close_ol(); close_table()
            if not in_ul:
                html_parts.append('<ul>')
                in_ul = True
            body = line[2:]
            if '||' in body:
                main, meta = body.split('||', 1)
                html_parts.append(
                    f'<li>{_md_inline(main)}'
                    f'<div class="issue-meta-row">{_md_inline(meta)}</div></li>'
                )
            else:
                html_parts.append(f'<li>{_md_inline(body)}</li>')
            i += 1; continue

        # Blank line or horizontal rule (--- section dividers)
        if line.strip() == "" or line.strip() == "---":
            close_ul(); close_ol(); close_table()
            i += 1; continue

        # Bold line (standalone **…**)
        if line.startswith("**") and line.endswith("**") and line.count("**") == 2:
            close_ul(); close_ol(); close_table()
            html_parts.append(f'<p><strong>{line[2:-2]}</strong></p>')
            i += 1; continue

        # Fallback: paragraph
        close_ul(); close_ol(); close_table()
        if line.strip():
            html_parts.append(f'<p>{_md_inline(line)}</p>')
        i += 1

    close_ul()
    close_ol()
    close_table()
    close_project()
    return "\n".join(html_parts)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def render_html(report_md: str) -> str:
    """Return a complete self-contained HTML document for the platform report."""
    dq_marker = "\n## ⚙️ Data Quality\n"
    if dq_marker in report_md:
        main_md, dq_md = report_md.split(dq_marker, 1)
        main_html = md_to_html(main_md)
        sidebar_html = md_to_html("## ⚙️ Data Quality\n" + dq_md)
        body = (
            f'<div class="report-layout">'
            f'<div class="report-main">{main_html}</div>'
            f'<aside class="report-sidebar">{sidebar_html}</aside>'
            f'</div>'
        )
    else:
        body = md_to_html(report_md)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Platform Weekly Status</title>
<style>
{CSS}
</style>
</head>
<body>
<div class="container">
{body}
<div class="footer">Platform Status Pipeline · {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
</div>
</body>
</html>"""
