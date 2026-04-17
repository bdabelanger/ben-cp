<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Platform Weekly Status</title>
<style>

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
    --warn:      #f59e0b;
    --danger:    #ef4444;
    --unmapped:  #9ca3af;
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
h4 { font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em;
     color: var(--muted); margin: 1.75rem 0 0.5rem; }
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
.prog-todo     { background: var(--todo); }

/* ---------- readiness bar ---------- */
.readiness-wrap {
    display: flex;
    height: 10px;
    border-radius: 6px;
    overflow: hidden;
    background: var(--todo);
    margin: 0.5rem 0;
    gap: 1px;
}
.readiness-done     { background: var(--done); }
.readiness-aligned  { background: var(--progress); }
.readiness-stalled  { background: var(--warn); }
.readiness-lagging  { background: var(--danger); }
.readiness-unmapped { background: var(--unmapped); }

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
.time-remaining        { background: #8b5cf6; }
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

/* ---------- asana status body (rich html) ---------- */
.status-body { font-size: 0.82rem; margin: 0.35rem 0 0.5rem; color: var(--text); }
.status-body h1, .status-body h2 { font-size: 0.82rem; font-weight: 700; margin: 0.5rem 0 0.15rem; }
.status-body p { margin: 0.15rem 0; }
.status-body ul, .status-body ol { padding-left: 1.2rem; margin: 0.15rem 0; }
.status-body a { color: var(--accent); }

/* ---------- tumbleweed / not-set pill ---------- */
.tw {
    display: inline-block;
    font-size: 0.73rem;
    font-style: italic;
    color: var(--muted);
    background: var(--bg);
    border: 1px dashed var(--border);
    border-radius: 4px;
    padding: 0.05rem 0.4rem;
}

/* ---------- asana status tag ---------- */
.asana-status { display: inline-block; padding: 0.1rem 0.55rem; border-radius: 999px;
    font-size: 0.72rem; font-weight: 600; margin: 0.25rem 0 0.15rem; }
.status-on-track    { background: #d1fae5; color: #065f46; }
.status-at-risk     { background: #fef3c7; color: #92400e; }
.status-off-track   { background: #fee2e2; color: #991b1b; }
.status-on-hold     { background: #dbeafe; color: #1e40af; }
.status-complete    { background: #dcfce7; color: #166534; }

/* ---------- jira link row in card ---------- */
.card-jira-row { display: flex; align-items: center; font-size: 0.82rem; font-weight: 600;
    margin: 0.6rem 0 0.2rem; padding-top: 0.5rem; border-top: 1px solid var(--border); }

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

</style>
</head>
<body>
<div class="container">
<div class="report-layout"><div class="report-main"><div class="report-header"><h1>Platform Weekly Status — April 17, 2026</h1><div class="subtitle">Generated April 17, 2026 at 00:14</div></div>
<h2>📋 Summary</h2>
<ol>
<li><a href="#CBP-2736">Notes - Notes datagrid</a> <span class="badge badge-ga">GA</span><div class="issue-meta-row">6 P2, 4 P3, 1 P4 left</div></li>
<li><a href="#CBP-2917">Web applications - Material UI upgrade (all components)</a> <span class="badge badge-ga">GA</span><div class="issue-meta-row">1 P2 left</div></li>
<li><a href="#CBP-2992">Enrollment dialog - Bulk Services section</a> <span class="badge badge-beta">Beta</span><div class="issue-meta-row">2 P2 left</div></li>
<li><a href="#CBP-2752">Notes - Bulk "General Notes"</a> <span class="badge badge-beta">Beta</span><div class="issue-meta-row">1 P3 left</div></li>
<li><a href="#CBP-2923">Notes - Locked Notes</a> <span class="badge badge-qa">In QA</span><div class="issue-meta-row">3 P2 left</div></li>
<li><a href="#CBP-3066">Services - Service plan datagrid with bulk actions</a> <span class="badge badge-dev">Development</span><div class="issue-meta-row">8 P2 left</div></li>
<li><a href="#CBP-3121">Services WLV - Bulk actions</a> <span class="badge badge-dev">Development</span><div class="issue-meta-row">5 P2 left</div></li>
<li><a href="#CBP-2924">Notes - Bulk Service Notes</a> <span class="badge badge-dev">Development</span><div class="issue-meta-row">👀 2 P1, 8 P2, 7 P3, 1 P4 left</div></li>
<li><a href="#CBP-3158">Integrations - Zapier improvements</a> <span class="badge badge-dev">Development</span><div class="issue-meta-row">1 P2 left</div></li>
</ol>
<h2>📋 Detailed Status</h2>
<h4>GA</h4>
<div class="project-card" id="CBP-2736"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1209963394727039" target="_blank">Notes - Notes datagrid</a> <span class="badge badge-ga">GA</span></h3>
<span class="asana-status status-on-track">On Track</span>
<div class='status-body'><i><strong>4-2 release</strong>: Rows per page performance issue needs resolution ahead of next GA wave. Not a release-blocker, but should be addressed ASAP.</i> <p><strong>Summary</strong></p>Locked notes are no longer returned to any user without permission in the grid or search However new reports of lagging experience may require a hotfix or 4-2 release before we want to release to GA <ul><li>🗓️ <strong>Shifting GA target to 4-2 release, we can move up if hotfixed beforehand</strong></li><li><em>Note - estimate/actual data quality has been relatively poor for this project, will share with engineers</em></li></ul> <p><strong>Next steps</strong></p><ol><li>First step in addressing lagging performance has been pushed to QA</li><li>Notes/Service interactions synchronization work continues ahead of Notes v2 release in 4-2 release</li><li>Some outstanding FE cleanup for Locked notes continues</li></ol></div>
<p>PRD: https://casecommons.atlassian.net/wiki/spaces/PROD/pages/3812753669</p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>QA Start <span class="tw">not set</span></li>
<li>UAT Start <span class="tw">not set</span></li>
<li>✅ Beta Start - Apr 1</li>
<li>🎯 GA - Apr 27</li>
<div class="card-jira-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><polyline points="3,5 10,12 3,19" stroke="#0052CC"/><polyline points="8,5 15,12 8,19" stroke="#2684FF"/><polyline points="13,5 20,12 13,19" stroke="#579DFF"/></svg><a href="https://casecommons.atlassian.net/browse/CBP-2736" target="_blank">CBP-2736</a></div>
</ul>
<p><strong>Status</strong> (Grain: Stories)</p>
<div class="progress-wrap"><div class="prog-done" style="width:66.7%"></div><div class="prog-progress" style="width:15.2%"></div><div class="prog-todo" style="width:18.2%"></div></div><span class="stat-row">22 done &nbsp;·&nbsp; 5 in progress &nbsp;·&nbsp; 6 to do</span>
<p><strong>Readiness</strong> (Grain: Stories)</p>
<div class="readiness-wrap"><div class="readiness-done" style="width:66.7%"></div><div class="readiness-aligned" style="width:3.0%"></div><div class="readiness-stalled" style="width:0.0%"></div><div class="readiness-lagging" style="width:0.0%"></div><div class="readiness-unmapped" style="width:30.3%"></div></div><span class="stat-row">22 Done &nbsp;·&nbsp; 1 Aligned &nbsp;·&nbsp; 10 Unmapped</span>
<p><strong>Estimate</strong> (Grain: Days)</p>
<div class="time-bar-wrap"><div class="time-actual" style="width:51.9%"></div><div class="time-remaining" style="width:11.4%"></div></div><span class="stat-row">35.1d estimated &nbsp;·&nbsp; 18.2d actual &nbsp;·&nbsp; 4.0d remaining (63%)</span>
<p><strong>Readiness Details</strong></p>
<table><thead><tr><th>🎯 Aligned</th><th>⚠️ Stalled</th><th>🛑 Lagging</th><th>👀 Unmapped</th></tr></thead><tbody>
<tr><td>1</td><td>0</td><td>0</td><td>10</td></tr>
</tbody></table>
<p><strong>Done:</strong> 22 issues</p>
<p class="stat-row">31.1d estimated · 18.2d actual</p>
<p><strong>In Progress:</strong> 5 issues · ~4.0d est remaining</p>
<ul>
<li><a href="https://casecommons.atlassian.net/browse/CBP-3183" target="_blank">CBP-3183</a> — Notes - Lagging Case Details page when page size = 50<div class="issue-meta-row">Russell · Merged to QA · 👀 Unestimated · 👀 No actual · P2 · Release: 2026-4-2</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3150" target="_blank">CBP-3150</a> — Notes - Synchronize note_people and service_interaction_people attributes<div class="issue-meta-row">Tuan · Merged to QA · 2.0d estimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3107" target="_blank">CBP-3107</a> — Notes - Rename date fields for Services section<div class="issue-meta-row">Bisoye · Merged to QA · 👀 Unestimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3105" target="_blank">CBP-3105</a> — Notes - Migrate Start/End dates from service interactions to service notes<div class="issue-meta-row">Tuan · Merged to QA · 1.0d estimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3059" target="_blank">CBP-3059</a> — Notes datagrid - Display Services data in Note preview as structured list<div class="issue-meta-row">Blessing · Merged to QA · 1.0d estimated · 👀 No actual · P4 · 👀 No release</div></li>
</ul>
<p><strong>To Do:</strong> 6 issues</p>
<ul>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3191" target="_blank">CBP-3191</a> — Notes - Synchronize note_resources and service_interaction_people_resources attributes<div class="issue-meta-row">Feyi · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3055" target="_blank">CBP-3055</a> — Notes - Enable row pinning in Notes Datagrid<div class="issue-meta-row">Bisoye · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3186" target="_blank">CBP-3186</a> — Notes - Clean up "Locked Note" FE handling<div class="issue-meta-row">Bisoye · To do · 👀 Unestimated · 👀 No actual · P3 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3062" target="_blank">CBP-3062</a> — Notes - Enhance Service(s) column display in Notes Datagrid collapsed state<div class="issue-meta-row">Pierre · To do · 👀 Unestimated · 👀 No actual · P3 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3060" target="_blank">CBP-3060</a> — Notes - Evaluate nested DataGrid approach for Services data in Note preview<div class="issue-meta-row">Pierre · To do · 👀 Unestimated · 👀 No actual · P3 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3054" target="_blank">CBP-3054</a> — Notes - Enable multi-filter stacking in Notes Datagrid<div class="issue-meta-row">Bisoye · To do · 👀 Unestimated · 👀 No actual · P3 · 👀 No release</div></li>
</ul>
</div>
<div class="project-card" id="CBP-2917"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1212552174642233" target="_blank">Web applications - Material UI upgrade (all components)</a> <span class="badge badge-ga">GA</span></h3>
<span class="asana-status status-on-track">On Track</span>
<div class='status-body'><i><strong>4-2 release</strong>: Home web is next up for GA release, would be a release-blocker since we cannot easily revert and there are no feature flags. <strong>5-1 release</strong>: Sodiq can begin merging the next wave next Monday after 4-2 release.</i> <p><strong>Summary</strong></p><ol><li>✅ Auth, Intake, and Reporting shipped in 4-1 release 🎉</li><li>🔄 Home has now been updated in QA for 4-2 release</li><li>Engage, Track, and People for 5-1 release</li><li>Admin, Internal, Portal (Access), Workflows for 5-2 release (may be separated further)</li></ol> <p><strong>Next steps</strong></p><ol><li>Engage, Track, and People will be updated in QA after 4-2 release UAT merge</li></ol></div>
<p><strong>Launch Plan</strong></p>
<ul>
<li>✅ QA Start - Mar 16</li>
<li>✅ UAT Start - Apr 3</li>
<li>🎯 GA - Jun 1</li>
<div class="card-jira-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><polyline points="3,5 10,12 3,19" stroke="#0052CC"/><polyline points="8,5 15,12 8,19" stroke="#2684FF"/><polyline points="13,5 20,12 13,19" stroke="#579DFF"/></svg><a href="https://casecommons.atlassian.net/browse/CBP-2917" target="_blank">CBP-2917</a></div>
</ul>
<p><strong>Status</strong> (Grain: Stories)</p>
<div class="progress-wrap"><div class="prog-done" style="width:90.0%"></div><div class="prog-progress" style="width:0.0%"></div><div class="prog-todo" style="width:10.0%"></div></div><span class="stat-row">9 done &nbsp;·&nbsp; 0 in progress &nbsp;·&nbsp; 1 to do</span>
<p><strong>Readiness</strong> (Grain: Stories)</p>
<div class="readiness-wrap"><div class="readiness-done" style="width:90.0%"></div><div class="readiness-aligned" style="width:0.0%"></div><div class="readiness-stalled" style="width:0.0%"></div><div class="readiness-lagging" style="width:0.0%"></div><div class="readiness-unmapped" style="width:10.0%"></div></div><span class="stat-row">9 Done &nbsp;·&nbsp; 1 Unmapped</span>
<p><strong>Estimate</strong> (Grain: Days)</p>
<div class="time-bar-wrap"><div class="time-actual" style="width:58.3%"></div><div class="time-remaining" style="width:0.0%"></div></div><span class="stat-row">6.0d estimated &nbsp;·&nbsp; 3.5d actual &nbsp;·&nbsp; 0.0d remaining (58%)</span>
<p><strong>Readiness Details</strong></p>
<table><thead><tr><th>🎯 Aligned</th><th>⚠️ Stalled</th><th>🛑 Lagging</th><th>👀 Unmapped</th></tr></thead><tbody>
<tr><td>0</td><td>0</td><td>0</td><td>1</td></tr>
</tbody></table>
<p><strong>Done:</strong> 9 issues</p>
<p class="stat-row">6.0d estimated · 3.5d actual</p>
<p><strong>To Do:</strong> 1 issues</p>
<ul>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3221" target="_blank">CBP-3221</a> — SWW occurs on clicking add service note option via new service plan grid<div class="issue-meta-row">Blessing · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release</div></li>
</ul>
</div>
<h4>Beta</h4>
<div class="project-card" id="CBP-2992"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1211631356870657" target="_blank">Enrollment dialog - Bulk Services section</a> <span class="badge badge-beta">Beta</span></h3>
<span class="asana-status status-on-track">On Track</span>
<div class='status-body'><i><strong>5-1 release</strong>: Single-click editing is required before we wrap up full GA rollout.</i> <p><strong>Summary</strong></p>Looking good - we're awaiting &quot;single-click edits&quot; before shipping to GA in 4-2 release <p><strong>Next steps</strong></p><ol><li>Single-click edits are in progress by Russell, which will be applied to all editable datagrids at once including Enrollments + Notes + Funds</li></ol></div>
<p>PRD: https://casecommons.atlassian.net/wiki/x/BQBN2w</p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>✅ QA Start - Feb 26</li>
<li>✅ UAT Start - Mar 12</li>
<li>✅ Beta Start - Mar 18</li>
<li>🎯 GA - May 29</li>
<div class="card-jira-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><polyline points="3,5 10,12 3,19" stroke="#0052CC"/><polyline points="8,5 15,12 8,19" stroke="#2684FF"/><polyline points="13,5 20,12 13,19" stroke="#579DFF"/></svg><a href="https://casecommons.atlassian.net/browse/CBP-2992" target="_blank">CBP-2992</a></div>
</ul>
<p><strong>Status</strong> (Grain: Stories)</p>
<div class="progress-wrap"><div class="prog-done" style="width:90.5%"></div><div class="prog-progress" style="width:0.0%"></div><div class="prog-todo" style="width:9.5%"></div></div><span class="stat-row">19 done &nbsp;·&nbsp; 0 in progress &nbsp;·&nbsp; 2 to do</span>
<p><strong>Readiness</strong> (Grain: Stories)</p>
<div class="readiness-wrap"><div class="readiness-done" style="width:90.5%"></div><div class="readiness-aligned" style="width:0.0%"></div><div class="readiness-stalled" style="width:0.0%"></div><div class="readiness-lagging" style="width:0.0%"></div><div class="readiness-unmapped" style="width:9.5%"></div></div><span class="stat-row">19 Done &nbsp;·&nbsp; 2 Unmapped</span>
<p><strong>Estimate</strong> (Grain: Days)</p>
<div class="time-bar-wrap"><div class="time-actual-over" style="width:75.0%"></div><div class="time-remaining-over" style="width:25.0%"></div></div><span class="stat-row">❌ 1.0d estimated &nbsp;·&nbsp; 3.0d actual &nbsp;·&nbsp; 1.0d remaining (400%)</span>
<p><strong>Readiness Details</strong></p>
<table><thead><tr><th>🎯 Aligned</th><th>⚠️ Stalled</th><th>🛑 Lagging</th><th>👀 Unmapped</th></tr></thead><tbody>
<tr><td>0</td><td>0</td><td>0</td><td>2</td></tr>
</tbody></table>
<p><strong>Done:</strong> 19 issues</p>
<p class="stat-row">33.0d estimated · 3.0d actual</p>
<p><strong>To Do:</strong> 2 issues</p>
<ul>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3095" target="_blank">CBP-3095</a> — FE - Service Enrollment - Service Type changed is not reflected in the View Service Enrollment<div class="issue-meta-row">Tuan · To do · 1.0d estimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3094" target="_blank">CBP-3094</a> — FE - Service Enrollment - Default value is not reflected in the Add Service enrollment (For ex: Method of delivery)<div class="issue-meta-row">Ben · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release</div></li>
</ul>
</div>
<div class="project-card" id="CBP-2752"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1211838817183809" target="_blank">Notes - Bulk "General Notes"</a> <span class="badge badge-beta">Beta</span></h3>
<span class="asana-status status-on-track">On Track</span>
<div class='status-body'><i><strong>5-1 release</strong>: Single-click editing is required before we expand to more customers in beta rollout. We also get attendance toggle + long text handling in Notes.</i> <strong><p><strong>Summary</strong></p></strong> No update - all remains well. Copy/pasting last week's update: Remains released to 4 tenants. No feedback thus far. <strong><p><strong>Next steps</strong></p></strong> No other work planned for General Notes currently. This will get a much more significant text once Service Notes/Locked Notes roll out in 4/23 release <ol><li>Task: Before Service Notes phase I will aim to bring us up to ~10 beta tenants with CSM approval</li></ol></div>
<p>PRD: https://casecommons.atlassian.net/wiki/x/TYD0BwE</p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>✅ QA Start - Apr 6</li>
<li>✅ UAT Start - Apr 16</li>
<li>✅ Beta Start - Apr 1</li>
<li>🎯 GA - Jun 1</li>
<div class="card-jira-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><polyline points="3,5 10,12 3,19" stroke="#0052CC"/><polyline points="8,5 15,12 8,19" stroke="#2684FF"/><polyline points="13,5 20,12 13,19" stroke="#579DFF"/></svg><a href="https://casecommons.atlassian.net/browse/CBP-2752" target="_blank">CBP-2752</a></div>
</ul>
<p><strong>Status</strong> (Grain: Stories)</p>
<div class="progress-wrap"><div class="prog-done" style="width:91.7%"></div><div class="prog-progress" style="width:0.0%"></div><div class="prog-todo" style="width:8.3%"></div></div><span class="stat-row">11 done &nbsp;·&nbsp; 0 in progress &nbsp;·&nbsp; 1 to do</span>
<p><strong>Readiness</strong> (Grain: Stories)</p>
<div class="readiness-wrap"><div class="readiness-done" style="width:91.7%"></div><div class="readiness-aligned" style="width:0.0%"></div><div class="readiness-stalled" style="width:0.0%"></div><div class="readiness-lagging" style="width:0.0%"></div><div class="readiness-unmapped" style="width:8.3%"></div></div><span class="stat-row">11 Done &nbsp;·&nbsp; 1 Unmapped</span>
<p><strong>Estimate</strong> (Grain: Days)</p>
<div class="time-bar-wrap"><div class="time-actual" style="width:55.3%"></div><div class="time-remaining" style="width:0.0%"></div></div><span class="stat-row">15.9d estimated &nbsp;·&nbsp; 8.8d actual &nbsp;·&nbsp; 0.0d remaining (55%)</span>
<p><strong>Readiness Details</strong></p>
<table><thead><tr><th>🎯 Aligned</th><th>⚠️ Stalled</th><th>🛑 Lagging</th><th>👀 Unmapped</th></tr></thead><tbody>
<tr><td>0</td><td>0</td><td>0</td><td>1</td></tr>
</tbody></table>
<p><strong>Done:</strong> 11 issues</p>
<p class="stat-row">15.9d estimated · 8.8d actual</p>
<p><strong>To Do:</strong> 1 issues</p>
<ul>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-2862" target="_blank">CBP-2862</a> — Columns on people grid of New note modal doesn't support scroll unless few people are added<div class="issue-meta-row">Sindhu · To do · 👀 Unestimated · 👀 No actual · P3 · 👀 No release</div></li>
</ul>
</div>
<h4>In QA</h4>
<div class="project-card" id="CBP-2923"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1211786365522017" target="_blank">Notes - Locked Notes</a> <span class="badge badge-qa">In QA</span></h3>
<span class="asana-status status-on-track">On Track</span>
<div class='status-body'><i><strong>4-2 release</strong>: Ben will roll out after returning from PTO - QA approval is required for GA release. This should not be a release blocker if we cannot get it done, we have a feature flag and it can move out if necessary.</i> <p><strong>Summary</strong></p>New note dialog is looking GREAT All AC implemented and up-leveled by Russell, entering QA after 4-1 release <p><strong>Next steps</strong></p>QA noticed a gap: <ol><li><a href="https://casecommons.atlassian.net/browse/CBP-3186">CBP-3186</a> will clean up mismatched (UOW+People Role/Assignment permissions) x (Note permissions)... always taking the <em>minimum</em> that the user has available</li><li><em>Note: Feyi has thoughts here - wants to combine access permissions in BE so as to not handle things like this in FE.</em></li></ol></div>
<p>PRD: https://casecommons.atlassian.net/wiki/x/TYD0BwE</p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>✅ QA Start - Apr 6</li>
<li>❌ UAT Start - Apr 16</li>
<li>⚠️ Beta Start - Apr 28</li>
<li>⚠️ GA - May 14</li>
<div class="card-jira-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><polyline points="3,5 10,12 3,19" stroke="#0052CC"/><polyline points="8,5 15,12 8,19" stroke="#2684FF"/><polyline points="13,5 20,12 13,19" stroke="#579DFF"/></svg><a href="https://casecommons.atlassian.net/browse/CBP-2923" target="_blank">CBP-2923</a></div>
</ul>
<p><strong>Status</strong> (Grain: Stories)</p>
<div class="progress-wrap"><div class="prog-done" style="width:0.0%"></div><div class="prog-progress" style="width:100.0%"></div><div class="prog-todo" style="width:0.0%"></div></div><span class="stat-row">0 done &nbsp;·&nbsp; 3 in progress &nbsp;·&nbsp; 0 to do</span>
<p><strong>Readiness</strong> (Grain: Stories)</p>
<div class="readiness-wrap"><div class="readiness-done" style="width:0.0%"></div><div class="readiness-aligned" style="width:100.0%"></div><div class="readiness-stalled" style="width:0.0%"></div><div class="readiness-lagging" style="width:0.0%"></div><div class="readiness-unmapped" style="width:0.0%"></div></div><span class="stat-row">3 Aligned</span>
<p><strong>Estimate</strong> (Grain: Days)</p>
<div class="time-bar-wrap"><div class="time-actual" style="width:0.0%"></div><div class="time-remaining" style="width:100.0%"></div></div><span class="stat-row">👀 6.0d estimated &nbsp;·&nbsp; 0.0d actual &nbsp;·&nbsp; 6.0d remaining (100%)</span>
<p><strong>Readiness Details</strong></p>
<table><thead><tr><th>🎯 Aligned</th><th>⚠️ Stalled</th><th>🛑 Lagging</th><th>👀 Unmapped</th></tr></thead><tbody>
<tr><td>3</td><td>0</td><td>0</td><td>0</td></tr>
</tbody></table>
<p><strong>In Progress:</strong> 3 issues · ~2.4d est remaining</p>
<ul>
<li><a href="https://casecommons.atlassian.net/browse/CBP-3125" target="_blank">CBP-3125</a> — FE - Issues found on the Note v2 access(locking note)<div class="issue-meta-row">Russell · Merged to QA · 2.0d estimated · 👀 No actual · P2 · Release: 2026-4-2</div></li>
<li><a href="https://casecommons.atlassian.net/browse/CBP-2756" target="_blank">CBP-2756</a> — Notes - Show "Access" section for all note types<div class="issue-meta-row">Russell · Merged to QA · 4.0d estimated · 3.6d actual · P2 · Release: 2026-4-2</div></li>
<li><a href="https://casecommons.atlassian.net/browse/CBP-2990" target="_blank">CBP-2990</a> — Notes - Search and populate the "Access" section<div class="issue-meta-row">Russell · QA revise · 👀 Unestimated · 👀 No actual · P2 · Release: 2026-4-2</div></li>
</ul>
</div>
<h4>Development</h4>
<div class="project-card" id="CBP-3066"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1211631360190563" target="_blank">Services - Service plan datagrid with bulk actions</a> <span class="badge badge-dev">Development</span></h3>
<span class="asana-status status-on-track">On Track</span>
<div class='status-body'><p><strong>Summary</strong></p>Blessing has completed work on the SP datagrid - ready for testing, but behind Notes in 4-2 release... will drop in May <ul><li>All the bells and whistles including bulk actions - more than we had in Notes even</li><li><em>Note: Blessing had great data quality for this showing dev work coming in under estimate </em>🙂 </li></ul> <p><strong>Next steps</strong></p><ol><li>I will give this an &quot;epic-level&quot; review before QA so that Blessing can tidy up anything obvious that I notice ahead of testing</li><li>In the meantime, Blessing's moving on to Services WLV bulk actions on Monday</li></ol></div>
<p><strong>Launch Plan</strong></p>
<ul>
<li>🎯 QA Start - May 4</li>
<li>🎯 UAT Start - May 7</li>
<li>🎯 Beta Start - May 18</li>
<li>🎯 GA - May 28</li>
<div class="card-jira-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><polyline points="3,5 10,12 3,19" stroke="#0052CC"/><polyline points="8,5 15,12 8,19" stroke="#2684FF"/><polyline points="13,5 20,12 13,19" stroke="#579DFF"/></svg><a href="https://casecommons.atlassian.net/browse/CBP-3066" target="_blank">CBP-3066</a></div>
</ul>
<p><strong>Status</strong> (Grain: Stories)</p>
<div class="progress-wrap"><div class="prog-done" style="width:0.0%"></div><div class="prog-progress" style="width:100.0%"></div><div class="prog-todo" style="width:0.0%"></div></div><span class="stat-row">0 done &nbsp;·&nbsp; 8 in progress &nbsp;·&nbsp; 0 to do</span>
<p><strong>Readiness</strong> (Grain: Stories)</p>
<div class="readiness-wrap"><div class="readiness-done" style="width:0.0%"></div><div class="readiness-aligned" style="width:0.0%"></div><div class="readiness-stalled" style="width:0.0%"></div><div class="readiness-lagging" style="width:0.0%"></div><div class="readiness-unmapped" style="width:100.0%"></div></div><span class="stat-row">8 Unmapped</span>
<p><strong>Estimate</strong> (Grain: Days)</p>
<div class="time-bar-wrap"><div class="time-actual" style="width:0.0%"></div><div class="time-remaining" style="width:100.0%"></div></div><span class="stat-row">👀 8.1d estimated &nbsp;·&nbsp; 0.0d actual &nbsp;·&nbsp; 8.1d remaining (100%)</span>
<p><strong>Readiness Details</strong></p>
<table><thead><tr><th>🎯 Aligned</th><th>⚠️ Stalled</th><th>🛑 Lagging</th><th>👀 Unmapped</th></tr></thead><tbody>
<tr><td>0</td><td>0</td><td>0</td><td>8</td></tr>
</tbody></table>
<p><strong>In Progress:</strong> 8 issues · ~8.1d est remaining</p>
<ul>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3144" target="_blank">CBP-3144</a> — Service plan - Bulk row selection, bulk actions menu UI, and bulk action implementations<div class="issue-meta-row">Blessing · In development · 👀 Unestimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3069" target="_blank">CBP-3069</a> — Service plan - Stacking filters<div class="issue-meta-row">Blessing · Merged to QA · 2.0d estimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3100" target="_blank">CBP-3100</a> — Add service plan datagrid feature flag for Engage, Intake and People<div class="issue-meta-row">Blessing · In QA · 0.1d estimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3099" target="_blank">CBP-3099</a> — GQL Service plan - Implement filter logic for service offerings <div class="issue-meta-row">Blessing · In QA · 2.0d estimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3076" target="_blank">CBP-3076</a> — Service plan - Quick filter<div class="issue-meta-row">Blessing · In QA · 👀 Unestimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3073" target="_blank">CBP-3073</a> — Service plan - Row pinning<div class="issue-meta-row">Blessing · In QA · 👀 Unestimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3072" target="_blank">CBP-3072</a> — Service plan - Cache user preferences<div class="issue-meta-row">Blessing · In QA · 1.0d estimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3067" target="_blank">CBP-3067</a> — Service plan - Display enrollments as a datagrid with sorting and toolbar<div class="issue-meta-row">Blessing · In QA · 3.0d estimated · 👀 No actual · P2 · 👀 No release</div></li>
</ul>
</div>
<div class="project-card" id="CBP-3121"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1211733450555414" target="_blank">Services WLV - Bulk actions</a> <span class="badge badge-dev">Development</span></h3>
<span class="asana-status status-on-track">On Track</span>
<div class='status-body'><p><strong>Summary</strong></p>Re-baselined <p><strong>Next steps</strong></p>Blessing will move on to this work after wrapping Service Plan datagrid</div>
<p><strong>Launch Plan</strong></p>
<ul>
<li>🎯 QA Start - Apr 20</li>
<li>🎯 UAT Start - Apr 30</li>
<li>🎯 GA - May 28</li>
<div class="card-jira-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><polyline points="3,5 10,12 3,19" stroke="#0052CC"/><polyline points="8,5 15,12 8,19" stroke="#2684FF"/><polyline points="13,5 20,12 13,19" stroke="#579DFF"/></svg><a href="https://casecommons.atlassian.net/browse/CBP-3121" target="_blank">CBP-3121</a></div>
</ul>
<p><strong>Status</strong> (Grain: Stories)</p>
<div class="progress-wrap"><div class="prog-done" style="width:0.0%"></div><div class="prog-progress" style="width:0.0%"></div><div class="prog-todo" style="width:100.0%"></div></div><span class="stat-row">0 done &nbsp;·&nbsp; 0 in progress &nbsp;·&nbsp; 5 to do</span>
<p><strong>Readiness</strong> (Grain: Stories)</p>
<div class="readiness-wrap"><div class="readiness-done" style="width:0.0%"></div><div class="readiness-aligned" style="width:0.0%"></div><div class="readiness-stalled" style="width:0.0%"></div><div class="readiness-lagging" style="width:0.0%"></div><div class="readiness-unmapped" style="width:100.0%"></div></div><span class="stat-row">5 Unmapped</span>
<p><strong>Estimate</strong> (Grain: Days)</p>
<p><code>not set</code></p>
<p><strong>Readiness Details</strong></p>
<table><thead><tr><th>🎯 Aligned</th><th>⚠️ Stalled</th><th>🛑 Lagging</th><th>👀 Unmapped</th></tr></thead><tbody>
<tr><td>0</td><td>0</td><td>0</td><td>5</td></tr>
</tbody></table>
<p><strong>To Do:</strong> 5 issues</p>
<ul>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3155" target="_blank">CBP-3155</a> — Services WLV - "Delete services" bulk action<div class="issue-meta-row">Blessing · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3154" target="_blank">CBP-3154</a> — Services WLV - "End all enrollments" bulk action<div class="issue-meta-row">Blessing · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3153" target="_blank">CBP-3153</a> — Services WLV - "Add service note" bulk action<div class="issue-meta-row">Blessing · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3152" target="_blank">CBP-3152</a> — Services WLV - "Add service enrollment" bulk action<div class="issue-meta-row">Blessing · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3151" target="_blank">CBP-3151</a> — Services WLV - Implement bulk actions menu<div class="issue-meta-row">Blessing · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release</div></li>
</ul>
</div>
<div class="project-card" id="CBP-2924"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1211757637943244" target="_blank">Notes - Bulk Service Notes</a> <span class="badge badge-dev">Development</span></h3>
<span class="asana-status status-on-track">On Track</span>
<div class='status-body'><i><strong>5-1 release</strong>: Service types are currently still loading into Service offering field (BE fix required). Afterwards, QA testing + single-click editing is required before we give access to any tenants in beta rollout.</i> <p><strong>Summary</strong></p>New note dialog is looking GREAT All AC implemented and up-leveled by Bisoye + Russell, entering QA after 4-1 release <ul><li>Rosters!</li><li>Resource linking!</li><li>🐻 Bears! Oh my!</li><li><em>Note: exceptionally poor data quality on actuals/estimates, can't come close to an accurate burndown</em></li></ul> <p><strong>Next steps</strong></p>QA may find issues, this is a ton of new work to test</div>
<p>PRD: https://casecommons.atlassian.net/wiki/x/TYD0BwE</p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>❌ QA Start - Apr 6</li>
<li>❌ UAT Start - Apr 16</li>
<li>⚠️ Beta Start - May 18</li>
<li>⚠️ GA - Jun 1</li>
<div class="card-jira-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><polyline points="3,5 10,12 3,19" stroke="#0052CC"/><polyline points="8,5 15,12 8,19" stroke="#2684FF"/><polyline points="13,5 20,12 13,19" stroke="#579DFF"/></svg><a href="https://casecommons.atlassian.net/browse/CBP-2924" target="_blank">CBP-2924</a></div>
</ul>
<p><strong>Status</strong> (Grain: Stories)</p>
<div class="progress-wrap"><div class="prog-done" style="width:5.3%"></div><div class="prog-progress" style="width:78.9%"></div><div class="prog-todo" style="width:15.8%"></div></div><span class="stat-row">1 done &nbsp;·&nbsp; 15 in progress &nbsp;·&nbsp; 3 to do</span>
<p><strong>Readiness</strong> (Grain: Stories)</p>
<div class="readiness-wrap"><div class="readiness-done" style="width:5.3%"></div><div class="readiness-aligned" style="width:42.1%"></div><div class="readiness-stalled" style="width:0.0%"></div><div class="readiness-lagging" style="width:0.0%"></div><div class="readiness-unmapped" style="width:52.6%"></div></div><span class="stat-row">1 Done &nbsp;·&nbsp; 8 Aligned &nbsp;·&nbsp; 10 Unmapped</span>
<p><strong>Estimate</strong> (Grain: Days)</p>
<div class="time-bar-wrap"><div class="time-actual" style="width:0.0%"></div><div class="time-remaining" style="width:100.0%"></div></div><span class="stat-row">👀 30.1d estimated &nbsp;·&nbsp; 0.0d actual &nbsp;·&nbsp; 30.1d remaining (100%)</span>
<p><strong>Readiness Details</strong></p>
<table><thead><tr><th>🎯 Aligned</th><th>⚠️ Stalled</th><th>🛑 Lagging</th><th>👀 Unmapped</th></tr></thead><tbody>
<tr><td>8</td><td>0</td><td>0</td><td>10</td></tr>
</tbody></table>
<p>⚠️ QA Start was 11d ago but 18 stories still open — worth a check?</p>
<p><strong>Done:</strong> 1 issues</p>
<p><strong>In Progress:</strong> 15 issues · ~4.0d est remaining</p>
<ul>
<li><a href="https://casecommons.atlassian.net/browse/CBP-3075" target="_blank">CBP-3075</a> — Service Note UI/UX Issues and Bugs as the initial testing<div class="issue-meta-row">Bisoye · Merged to QA · 4.0d estimated · 👀 No actual · P1 · Release: 2026-4-2</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3174" target="_blank">CBP-3174</a> — [Data Grid] - Single-click editable mode for MUI DataGridPro<div class="issue-meta-row">Russell · In development · 👀 Unestimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3146" target="_blank">CBP-3146</a> — Notes - Tabbed UI in new Note dialog<div class="issue-meta-row">Russell · In development · 3.0d estimated · 5.0d actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3145" target="_blank">CBP-3145</a> — Notes - Service note datagrid UX improvements<div class="issue-meta-row">Russell · In development · 3.0d estimated · 3.0d actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3141" target="_blank">CBP-3141</a> — Service Notes - "Link" action for service interaction people<div class="issue-meta-row">Bisoye · In QA · 👀 Unestimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3113" target="_blank">CBP-3113</a> — Service Notes - Rostering in new Note dialog<div class="issue-meta-row">Bisoye · In QA · 👀 Unestimated · 👀 No actual · P2 · 👀 No release</div></li>
<li><a href="https://casecommons.atlassian.net/browse/CBP-2952" target="_blank">CBP-2952</a> — Notes - Show "Services" and hide "People" sections for Service Notes<div class="issue-meta-row">Bisoye · In QA · 3.0d estimated · 3.0d actual · P2 · Release: 2026-4-2</div></li>
<li><a href="https://casecommons.atlassian.net/browse/CBP-2985" target="_blank">CBP-2985</a> — Notes - Search and populate the "Services" section<div class="issue-meta-row">Bisoye · QA revise · 10.0d estimated · 8.0d actual · P2 · Release: 2026-4-2</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3110" target="_blank">CBP-3110</a> — Service Note - Clicking provider name in add-services flow adds service instead of opening provider<div class="issue-meta-row">Tuan · Merged to QA · 1.0d estimated · 1.0d actual · P3 · 👀 No release</div></li>
<li><a href="https://casecommons.atlassian.net/browse/CBP-3042" target="_blank">CBP-3042</a> — FE - Notes V2 - Service Note - "Add Service" option appears as mandatory, but no validation message is displayed<div class="issue-meta-row">Bisoye · Merged to QA · 👀 Unestimated · 👀 No actual · P3 · Release: 2026-4-2</div></li>
<li><a href="https://casecommons.atlassian.net/browse/CBP-3112" target="_blank">CBP-3112</a> — FE - Service Note - Trash icon on service interaction row shows incorrect tooltip "Delete enrollment"<div class="issue-meta-row">Bisoye · In QA · 0.1d estimated · 0.1d actual · P3 · Release: 2026-4-2</div></li>
<li><a href="https://casecommons.atlassian.net/browse/CBP-3111" target="_blank">CBP-3111</a> — Service Note - Note type switch confirmation dialog repeats identical text in header and body<div class="issue-meta-row">Bisoye · In QA · 👀 Unestimated · 👀 No actual · P3 · Release: 2026-4-2 / 2026-5-1</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3108" target="_blank">CBP-3108</a> — Service Note - Autocompleter freeze causes same person to be added multiple times<div class="issue-meta-row">Bisoye · In QA · 👀 Unestimated · 👀 No actual · P3 · 👀 No release</div></li>
<li><a href="https://casecommons.atlassian.net/browse/CBP-3063" target="_blank">CBP-3063</a> — Notes - Show and save Service Group column in Service Notes<div class="issue-meta-row">Bisoye · In QA · 👀 Unestimated · 👀 No actual · P3 · Release: 2026-4-2</div></li>
<li><a href="https://casecommons.atlassian.net/browse/CBP-2831" target="_blank">CBP-2831</a> — Issue with End Date Validation in Service Notes<div class="issue-meta-row">Uday · Product approved · 👀 Unestimated · 👀 No actual · P4 · Release: 2026-4-2</div></li>
</ul>
<p><strong>To Do:</strong> 3 issues</p>
<ul>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-2803" target="_blank">CBP-2803</a> — BE - Inconsistent Service Notes Display Between Case/Intake and Provider Notebooks<div class="issue-meta-row">Tuan · To do · 1.5d estimated · 👀 No actual · P1 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-2573" target="_blank">CBP-2573</a> — Duplicate Service interactions when adding multiple services on a note (intermittently)<div class="issue-meta-row">Yi · To do · 2.5d estimated · 👀 No actual · P2 · 👀 No release</div></li>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-1503" target="_blank">CBP-1503</a> — raisethebarr - Rostered people are not populated on service note of Notebook page navigated via enrollment with rostered service<div class="issue-meta-row">👀 Unassigned · Blocked - Needs Review · 2.0d estimated · 👀 No actual · P3 · 👀 No release</div></li>
</ul>
</div>
<div class="project-card" id="CBP-3158"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1213496879668016" target="_blank">Integrations - Zapier improvements</a> <span class="badge badge-dev">Development</span></h3>
<span class="asana-status status-on-track">On Track</span>
<div class='status-body'><p><strong>Summary</strong></p>Eric has not committed any code and he scheduled a demo out next Thursday. This week's report was again high level so I hope he has not filed any new hours for the week. I've set an expectation that he and I will meet with Yi before Thursday and I gather that he's again going to take on his work during the weekend. <p><strong>Next steps</strong></p><ol><li>Demo scheduled for Thursday where expectations have been set that Eric will be showing a working approach for dynamic schema rendering</li></ol></div>
<p>PRD: https://casecommons.atlassian.net/wiki/x/AoCwBQE</p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>🎯 QA Start - May 11</li>
<li>🎯 UAT Start - May 28</li>
<li>🎯 GA - Jun 11</li>
<div class="card-jira-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><polyline points="3,5 10,12 3,19" stroke="#0052CC"/><polyline points="8,5 15,12 8,19" stroke="#2684FF"/><polyline points="13,5 20,12 13,19" stroke="#579DFF"/></svg><a href="https://casecommons.atlassian.net/browse/CBP-3158" target="_blank">CBP-3158</a></div>
</ul>
<p><strong>Status</strong> (Grain: Stories)</p>
<div class="progress-wrap"><div class="prog-done" style="width:0.0%"></div><div class="prog-progress" style="width:0.0%"></div><div class="prog-todo" style="width:100.0%"></div></div><span class="stat-row">0 done &nbsp;·&nbsp; 0 in progress &nbsp;·&nbsp; 1 to do</span>
<p><strong>Readiness</strong> (Grain: Stories)</p>
<div class="readiness-wrap"><div class="readiness-done" style="width:0.0%"></div><div class="readiness-aligned" style="width:0.0%"></div><div class="readiness-stalled" style="width:0.0%"></div><div class="readiness-lagging" style="width:0.0%"></div><div class="readiness-unmapped" style="width:100.0%"></div></div><span class="stat-row">1 Unmapped</span>
<p><strong>Estimate</strong> (Grain: Days)</p>
<p><code>not set</code></p>
<p><strong>Readiness Details</strong></p>
<table><thead><tr><th>🎯 Aligned</th><th>⚠️ Stalled</th><th>🛑 Lagging</th><th>👀 Unmapped</th></tr></thead><tbody>
<tr><td>0</td><td>0</td><td>0</td><td>1</td></tr>
</tbody></table>
<p><strong>To Do:</strong> 1 issues</p>
<ul>
<li>👀 <a href="https://casecommons.atlassian.net/browse/CBP-3159" target="_blank">CBP-3159</a> — Zapier - Create/Update a Person Write Action<div class="issue-meta-row">eric.engoron · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release</div></li>
</ul>
</div>
<h4>Discovery</h4>
<div class="project-card" id="CBP-3085"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1213564552809143" target="_blank">Accessibility - 2026 VPAT accessibility audit</a> <span class="badge badge-discovery">Discovery</span></h3>
<span class="asana-status status-on-track">On Track</span>
<div class='status-body'><p><strong>Summary</strong></p>Nothin' doin' at the moment but will be prioritized later this quarter, likely with Sodiq and Russell to lead through <p><strong>Next steps</strong></p>None yet</div>
<p><strong>Launch Plan</strong></p>
<ul>
<li>🎯 QA Start - May 18</li>
<li>🎯 UAT Start - Jun 11</li>
<li>🎯 GA - Jun 11</li>
<div class="card-jira-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><polyline points="3,5 10,12 3,19" stroke="#0052CC"/><polyline points="8,5 15,12 8,19" stroke="#2684FF"/><polyline points="13,5 20,12 13,19" stroke="#579DFF"/></svg><a href="https://casecommons.atlassian.net/browse/CBP-3085" target="_blank">CBP-3085</a></div>
</ul>
</div>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1210368097846960" target="_blank">Notes - Global Notes WLV</a> <span class="badge badge-discovery">Discovery</span></h3>
<span class="asana-status status-on-track">On Track</span>
<div class='status-body'><p><strong>Summary</strong></p>Nothin' doin' at the moment but will be prioritized later this quarter, likely with Bisoye to lead through <strong><p><strong>Next steps</strong></p></strong> None yet</div>
<p><strong>Launch Plan</strong></p>
<ul>
<li>🎯 QA Start - Jun 1</li>
<li>🎯 UAT Start - Jun 18</li>
<li>🎯 Beta Start - Jun 25</li>
<li>🎯 GA - Jul 9</li>
</ul>
</div>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1212560621975480" target="_blank">Dynamic pages - Schema migration and duplicate prevention</a> <span class="badge badge-discovery">Discovery</span></h3>
<span class="asana-status status-on-track">On Track</span>
<div class='status-body'><p><strong>Summary</strong></p>Added AC for removing inline &quot;access&quot; section for People While reviewing Potts Family Foundation schemas, I found a number of real concerns <p><strong>Next steps</strong></p><ol><li>Planning with Russell, Bisoye, Feyi, and Yi</li></ol></div>
<p><strong>Launch Plan</strong></p>
<ul>
<li>🎯 QA Start - Jun 29</li>
<li>🎯 UAT Start - Jul 16</li>
<li>🎯 GA - Jul 23</li>
</ul>
</div>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1213506659163435" target="_blank">Portal - Client Dashboard</a> <span class="badge badge-discovery">Discovery</span></h3>
<p><span class="tw">not set</span></p>
<p>PRD: https://casecommons.atlassian.net/wiki/x/AgCrBQE</p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>🎯 QA Start - May 11</li>
<li>🎯 UAT Start - Jun 11</li>
<li>🎯 Beta Start - Jun 11</li>
<li>GA <span class="tw">not set</span></li>
</ul>
</div>
<h4>Study</h4>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1209189001499701" target="_blank">Assignment-based task notifications study</a> <span class="badge badge-study">Study</span></h3>
<p><span class="tw">not set</span></p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>QA Start <span class="tw">not set</span></li>
<li>UAT Start <span class="tw">not set</span></li>
<li>GA <span class="tw">not set</span></li>
</ul>
</div>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1208822133040792" target="_blank">Nylas Upgrade - UX Improvements</a> <span class="badge badge-study">Study</span></h3>
<span class="asana-status status-on-hold">On Hold</span>
<div class='status-body'>Completed a review of v3 diff and existing Nylas features that we have not leveraged <a href="https://developer.nylas.com/docs/v2/upgrade-to-v3/diff-view/#terminology-changes-in-v3">https://developer.nylas.com/docs/v2/upgrade-to-v3/diff-view/#terminology-changes-in-v3</a> A few interesting new features which would require additional dev: <strong>Email</strong> <ul><li>New webhook event for emails message.opened could be used to indicate that an internal user had seen a message</li></ul> <strong>Calendars</strong> <ul><li>Check a calendar for free/busy status</li><li>Each grant can now have up to 10 virtual calendars + Added the option to specify a primary calendar</li><li>”You can now send drafts” - save?</li><li>You can schedule a send time for a message, and edit or delete scheduled send times. - The new message.send_success and message.send_failed notifications allow you to track the results of a scheduled send</li><li>The new message.bounce_detected notification is available to check for message bounces from Google, Microsoft Graph, iCloud, and Yahoo.</li><li>You can now soft-delete messages and threads</li></ul> Also discussed Nylas’ scheduling tools which could address some user requests - after chatting with @Jordan Jan and Allie, it seems that this integration would be a heavy lift and wouldn’t qualify for low-hanging fruit <ul><li><a href="https://developer.nylas.com/docs/v3/calendar/group-booking/">https://developer.nylas.com/docs/v3/calendar/group-booking/</a></li></ul></div>
<p><strong>Launch Plan</strong></p>
<ul>
<li>QA Start <span class="tw">not set</span></li>
<li>UAT Start <span class="tw">not set</span></li>
<li>GA <span class="tw">not set</span></li>
</ul>
</div>
<h4>Backlog</h4>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1210860550580423" target="_blank">Data import - Bulk import for Notes</a> <span class="badge badge-backlog">Backlog</span></h3>
<span class="asana-status status-on-track">On Track</span>
<div class='status-body'><p><strong>Summary</strong></p>Nothin' doin' at the moment but will be prioritized later this quarter, likely with Duc and Tuan to lead through <p><strong>Next steps</strong></p>None yet</div>
<p>PRD: https://casecommons.atlassian.net/wiki/x/CgBGZ</p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>🎯 QA Start - Jun 11</li>
<li>🎯 UAT Start - Jul 2</li>
<li>🎯 GA - Jul 13</li>
</ul>
</div>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1210860550580376" target="_blank">Data import - Clearer IDs</a> <span class="badge badge-backlog">Backlog</span></h3>
<span class="asana-status status-on-hold">On Hold</span>
<div class='status-body'><p><strong>Summary</strong></p>Sorting out next steps re: Tuan's priorities</div>
<p>PRD: https://casecommons.atlassian.net/wiki/spaces/PROD/pages/1682309130</p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>QA Start <span class="tw">not set</span></li>
<li>UAT Start <span class="tw">not set</span></li>
<li>GA <span class="tw">not set</span></li>
</ul>
</div>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1209067717586483" target="_blank">Forms - Long-term strategy</a> <span class="badge badge-backlog">Backlog</span></h3>
<span class="asana-status status-on-hold">On Hold</span>
<div class='status-body'><strong>Temporarily de-prioritized based on 2025 planning</strong></div>
<p><strong>Launch Plan</strong></p>
<ul>
<li>QA Start <span class="tw">not set</span></li>
<li>UAT Start <span class="tw">not set</span></li>
<li>GA <span class="tw">not set</span></li>
</ul>
</div>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1210615331914095" target="_blank">Internal Admin - Activate/inactivate tenants from Chargebee</a> <span class="badge badge-backlog">Backlog</span></h3>
<span class="asana-status status-on-hold">On Hold</span>
<div class='status-body'><p><strong>Summary</strong></p>On hold; not in Q4 scope as of now.</div>
<p><strong>Launch Plan</strong></p>
<ul>
<li>QA Start <span class="tw">not set</span></li>
<li>UAT Start <span class="tw">not set</span></li>
<li>GA <span class="tw">not set</span></li>
</ul>
</div>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1213685097670612" target="_blank">Notes - Optional People in Service Notes</a> <span class="badge badge-backlog">Backlog</span></h3>
<p><span class="tw">not set</span></p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>QA Start <span class="tw">not set</span></li>
<li>UAT Start <span class="tw">not set</span></li>
<li>GA <span class="tw">not set</span></li>
</ul>
</div>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1210452458408269" target="_blank">Services - Multiple rosters for enrollments and notes</a> <span class="badge badge-backlog">Backlog</span></h3>
<span class="asana-status status-at-risk">At Risk</span>
<div class='status-body'><p><strong>Summary</strong></p>Currently showing risk for completion within Q1, will re-evaluate as other blocking work is completed</div>
<p>PRD: https://casecommons.atlassian.net/wiki/x/BQBN2w</p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>QA Start <span class="tw">not set</span></li>
<li>UAT Start <span class="tw">not set</span></li>
<li>GA <span class="tw">not set</span></li>
</ul>
</div>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1210874981107020" target="_blank">Test Automation Suite for Endpoint Security</a> <span class="badge badge-backlog">Backlog</span></h3>
<p><span class="tw">not set</span></p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>QA Start <span class="tw">not set</span></li>
<li>UAT Start <span class="tw">not set</span></li>
<li>GA <span class="tw">not set</span></li>
</ul>
</div>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1210615331914089" target="_blank">Text messaging - Phone number selection/onboarding</a> <span class="badge badge-backlog">Backlog</span></h3>
<p><span class="tw">not set</span></p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>QA Start <span class="tw">not set</span></li>
<li>UAT Start <span class="tw">not set</span></li>
<li>GA <span class="tw">not set</span></li>
</ul>
</div>
<h4>N/A</h4>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1211796849380964" target="_blank">Automation & Deflection 2026</a> <span class="badge badge-backlog">None</span></h3>
<p><span class="tw">not set</span></p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>QA Start <span class="tw">not set</span></li>
<li>UAT Start <span class="tw">not set</span></li>
<li>GA <span class="tw">not set</span></li>
</ul>
</div>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1211002139187115" target="_blank">MDM Upgrade & Implementation</a> <span class="badge badge-backlog">None</span></h3>
<p><span class="tw">not set</span></p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>QA Start <span class="tw">not set</span></li>
<li>UAT Start <span class="tw">not set</span></li>
<li>GA <span class="tw">not set</span></li>
</ul>
</div>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1213022940723417" target="_blank">Notes - Anonymous service notes</a> <span class="badge badge-backlog">None</span></h3>
<p><span class="tw">not set</span></p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>QA Start <span class="tw">not set</span></li>
<li>UAT Start <span class="tw">not set</span></li>
<li>GA <span class="tw">not set</span></li>
</ul>
</div>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1211708145580080" target="_blank">Services - Service groups for notes</a> <span class="badge badge-backlog">None</span></h3>
<p><span class="tw">not set</span></p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>QA Start <span class="tw">not set</span></li>
<li>UAT Start <span class="tw">not set</span></li>
<li>GA <span class="tw">not set</span></li>
</ul>
</div>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1210154179999344" target="_blank">Services - Service note resource linking</a> <span class="badge badge-backlog">None</span></h3>
<p><span class="tw">not set</span></p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>QA Start <span class="tw">not set</span></li>
<li>UAT Start <span class="tw">not set</span></li>
<li>GA <span class="tw">not set</span></li>
</ul>
</div>
<div class="project-card"><h3><svg width="13" height="13" viewBox="0 0 100 100" style="vertical-align:middle;margin-right:3px;flex-shrink:0"><circle cx="50" cy="22" r="22" fill="#F06A6A"/><circle cx="22" cy="73" r="22" fill="#F06A6A"/><circle cx="78" cy="73" r="22" fill="#F06A6A"/></svg><a href="https://app.asana.com/1/1123317448830974/project/1209742093504572" target="_blank">Small wins - May</a> <span class="badge badge-backlog">None</span></h3>
<p><span class="tw">not set</span></p>
<p><strong>Launch Plan</strong></p>
<ul>
<li>QA Start <span class="tw">not set</span></li>
<li>UAT Start <span class="tw">not set</span></li>
<li>GA <span class="tw">not set</span></li>
</ul>
</div></div><aside class="report-sidebar"><h2>⚙️ Data Quality</h2>
<p><strong>Estimates:</strong> 17/31 in-progress (54%)</p>
<p><strong>Actuals:</strong> 4/24 in QA (16%)</p>
<table><thead><tr><th>Engineer</th><th>Estimates</th><th>Actuals</th></tr></thead><tbody>
<tr><td>Bisoye</td><td>4/11 (36%)</td><td>2/10 (20%)</td></tr>
<tr><td>Blessing</td><td>6/9 (66%)</td><td>👀 0/8 (0%)</td></tr>
<tr><td>Russell</td><td>4/7 (57%)</td><td>👏 1/3 (33%)</td></tr>
<tr><td>Tuan</td><td>3/3 (100%)</td><td>1/3 (33%)</td></tr>
<tr><td>Uday</td><td>👀 0/1 (0%)</td><td>—</td></tr>
</tbody></table>
<p><strong>Unprioritized:</strong> 5 of 31 in-progress issues have no fix version set (16%)</p>
<table><thead><tr><th>Project</th><th>Unprioritized</th></tr></thead><tbody>
<tr><td>Notes - Bulk Service Notes</td><td>3/15 (20%)</td></tr>
<tr><td>Notes - Notes datagrid</td><td>2/5 (40%)</td></tr>
</tbody></table></aside></div>
<div class="footer">Platform Status Pipeline · 2026-04-17 00:14</div>
</div>
</body>
</html>