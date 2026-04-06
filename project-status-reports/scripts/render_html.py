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
    --progress:  #f59e0b;
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
    height: 8px;
    border-radius: 6px;
    overflow: hidden;
    background: var(--todo);
    margin: 0.3rem 0;
    max-width: 260px;
}
.time-filled   { background: var(--accent); }
.time-over     { background: #ef4444; }

/* ---------- badge / pill ---------- */
.badge {
    display: inline-block;
    padding: 0.1rem 0.55rem;
    border-radius: 999px;
    font-size: 0.73rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.badge-stage   { background: #dbeafe; color: #1d4ed8; }
.badge-ga      { background: #dcfce7; color: #15803d; }
.badge-beta    { background: #fef9c3; color: #854d0e; }
.badge-qa      { background: #fce7f3; color: #9d174d; }
.badge-dev     { background: #f3f4f6; color: #374151; }
.stat-row      { font-size: 0.85rem; color: var(--muted); margin: 0.2rem 0; }

@media (prefers-color-scheme: dark) {
    .badge-stage { background: #1e3a8a; color: #93c5fd; }
    .badge-ga    { background: #14532d; color: #86efac; }
    .badge-beta  { background: #713f12; color: #fde68a; }
    .badge-qa    { background: #831843; color: #fbcfe8; }
    .badge-dev   { background: #1f2937; color: #d1d5db; }
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

/* ---------- section callout ---------- */
.data-quality {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.3rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow);
}
.data-quality p { font-size: 0.88rem; }

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
        "GA": "badge-ga",
        "Beta": "badge-beta",
        "In QA": "badge-qa",
        "In UAT": "badge-qa",
    }.get(stage, "badge-dev")
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
    Parse `█████░░░░░ 3.5d act / 7.0d est (50%)` into an HTML bar + label.
    """
    m = re.search(r'([\d.]+)d\s+act\s*/\s*([\d.]+)d\s+est\s*\((\d+)%\)', bar_text)
    if not m:
        return f"<p><code>{bar_text}</code></p>"
    act, est, pct = float(m.group(1)), float(m.group(2)), int(m.group(3))
    over = pct > 100
    fill_cls = "time-over" if over else "time-filled"
    fill_pct = min(100, pct)
    prefix = "⚠️ " if over else ""
    bar = (f'<div class="time-bar-wrap">'
           f'<div class="{fill_cls}" style="width:{fill_pct}%"></div>'
           f'</div>')
    label = f'<span class="stat-row">{prefix}{act:.1f}d act / {est:.1f}d est ({pct}%)</span>'
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
    in_project = False

    def close_ul():
        nonlocal in_ul
        if in_ul:
            html_parts.append("</ul>")
            in_ul = False

    def close_project():
        nonlocal in_project
        if in_project:
            html_parts.append("</div>")  # .project-card
            in_project = False

    while i < len(lines):
        line = lines[i]

        # H1 — report title → header card
        if line.startswith("# "):
            close_ul(); close_project()
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
            close_ul(); close_project()
            heading = _md_inline(line[3:])
            html_parts.append(f'<h2>{heading}</h2>')
            i += 1; continue

        # H3 — project card header
        if line.startswith("### "):
            close_ul(); close_project()
            heading = _md_inline(line[4:])
            # Extract stage badge if present — e.g. "### Name · KEY · Stage"
            stage_m = re.search(r'·\s+([^··]+)\s*$', line)
            stage_html = _stage_badge(stage_m.group(1).strip()) if stage_m else ""
            html_parts.append(
                f'<div class="project-card">'
                f'<h3>{heading} {stage_html}</h3>'
            )
            in_project = True
            i += 1; continue

        # Progress bar line (backtick-wrapped containing ▓/▒/░)
        if line.startswith("`") and any(c in line for c in "▓▒░"):
            close_ul()
            inner = line.strip("`").strip()
            html_parts.append(_progress_bar_html(inner))
            i += 1; continue

        # Time bar line (backtick-wrapped containing █/░ and 'd act')
        if line.startswith("`") and ("d act" in line or "d logged" in line or "no time" in line):
            close_ul()
            inner = line.strip("`").strip()
            html_parts.append(_time_bar_html(inner))
            i += 1; continue

        # Generic backtick code line
        if line.startswith("`") and line.endswith("`"):
            close_ul()
            inner = line[1:-1]
            html_parts.append(f'<p><code>{inner}</code></p>')
            i += 1; continue

        # Bullet list item
        if re.match(r'^[\*\-] ', line) or re.match(r'^\* ', line):
            if not in_ul:
                html_parts.append('<ul>')
                in_ul = True
            content = _md_inline(line[2:])
            html_parts.append(f'<li>{content}</li>')
            i += 1; continue

        # Blank line
        if line.strip() == "":
            close_ul()
            i += 1; continue

        # Bold line (standalone **…**)
        if line.startswith("**") and line.endswith("**") and line.count("**") == 2:
            close_ul()
            html_parts.append(f'<p><strong>{line[2:-2]}</strong></p>')
            i += 1; continue

        # Fallback: paragraph
        close_ul()
        if line.strip():
            html_parts.append(f'<p>{_md_inline(line)}</p>')
        i += 1

    close_ul()
    close_project()
    return "\n".join(html_parts)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def render_html(report_md: str) -> str:
    """Return a complete self-contained HTML document for the platform report."""
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
