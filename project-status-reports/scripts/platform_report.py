import json
import os
import re
from datetime import datetime, date

JIRA_BASE = "https://casecommons.atlassian.net/browse"
ASANA_BASE = "https://app.asana.com/1/1123317448830974/project"

# Status name overrides — take precedence over Jira's native statusCategory
STATUS_OVERRIDES = {
    "Blocked - Needs Review": "To Do",
    "Blocked - Third-Party": "To Do",
    "QA Revise": "In Progress",
}

# statusCategory.key → name fallback (real API includes name, but guard against test data)
STATUS_CATEGORY_KEY_MAP = {
    "new": "To Do",
    "indeterminate": "In Progress",
    "inprogress": "In Progress",
    "done": "Done",
}

STAGE_RANKS = {
    "Development": 1,
    "In QA": 2,
    "In UAT": 3,
    "Beta": 4,
    "GA": 5,
}

# Required stage rank to count a milestone as "hit"
MILESTONE_REQUIREMENTS = {
    "qa_start": 2,
    "uat_start": 3,
    "beta_start": 4,
    "ga_target": 5,
}

# GA Month enum name → month number
GA_MONTH_MAP = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}


class PlatformStatusReport:

    def __init__(self, asana_data_path, jira_data_path, jira_raw_dir=None):
        self.asana_data = self._load_json(asana_data_path)
        self.jira_issues = self._load_json(jira_data_path)

        # Load epic-level data (timeoriginalestimate) keyed by CBP-XXXX
        self.epic_data = {}
        if jira_raw_dir and os.path.isdir(jira_raw_dir):
            for fname in os.listdir(jira_raw_dir):
                if fname.endswith("_epic.json"):
                    with open(os.path.join(jira_raw_dir, fname)) as f:
                        data = json.load(f)
                    key = data.get("key")
                    if key:
                        self.epic_data[key] = data
        self.jira_issues = [i for i in self.jira_issues if "key" in i]
        self.today = datetime.now().date()

        # Apply status category overrides and ensure effective_category is set
        for issue in self.jira_issues:
            status_name = (issue.get("fields", {}).get("status", {}).get("name") or "")
            if status_name in STATUS_OVERRIDES:
                issue["effective_category"] = STATUS_OVERRIDES[status_name]
            elif not issue.get("effective_category"):
                sc = issue.get("fields", {}).get("status", {}).get("statusCategory", {}) or {}
                native = sc.get("name") or STATUS_CATEGORY_KEY_MAP.get(sc.get("key", ""), "To Do")
                issue["effective_category"] = native

        # Build epic_key → [child issues] map
        issue_map = {i["key"]: i for i in self.jira_issues}
        self.project_issues = {}
        for issue in self.jira_issues:
            pkey = self._resolve_top_level_epic(issue, issue_map)
            if pkey:
                self.project_issues.setdefault(pkey, []).append(issue)

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _load_json(self, path):
        if not os.path.exists(path):
            return []
        with open(path) as f:
            return json.load(f)

    def _resolve_top_level_epic(self, issue, issue_map):
        curr = issue
        for _ in range(3):
            parent_key = ((curr.get("fields", {}).get("parent") or {}).get("key"))
            if not parent_key:
                parent_key = curr.get("fields", {}).get("customfield_10001")
            if not parent_key:
                return curr["key"]
            curr = issue_map.get(parent_key)
            if not curr:
                return parent_key
        return curr["key"]

    def _jira_url(self, key):
        return f"{JIRA_BASE}/{key}"

    def _asana_url(self, project):
        """Return Asana project URL, constructing from GID if permalink_url absent."""
        url = project.get("permalink_url")
        if url:
            return url
        gid = project.get("gid", "")
        return f"{ASANA_BASE}/{gid}" if gid else "#"

    def _get_pkey(self, project):
        """Extract CBP-XXXX key from project's jira_link field."""
        raw = (project.get("jira_link", "") or "").strip()
        if not raw or raw == "N/A":
            return None
        # Full URL: take last path segment
        key = raw.split("/")[-1].strip()
        # Must look like a CBP key
        if re.match(r"^CBP-\d+$", key):
            return key
        return None

    def _priority_rank(self, issue):
        p = ((issue.get("fields", {}).get("priority") or {}).get("name") or "")
        return {"P1": 1, "P2": 2, "P3": 3, "P4": 4}.get(p, 99)

    def _fmt_day(self, d):
        """Format date as 'Apr 3' (no leading zero)."""
        return d.strftime("%b %-d")

    # -------------------------------------------------------------------------
    # Sort
    # -------------------------------------------------------------------------

    def _parse_ga_sort_key(self, project):
        """Soonest GA first (ascending date), Stage rank descending as tiebreaker."""
        m = project.get("milestones", {})
        stage_rank = STAGE_RANKS.get(project.get("stage", ""), 0)

        # Try ga_target (YYYY-MM-DD)
        for field in ("ga_target", "ga_date"):
            raw = m.get(field)
            if not raw:
                continue
            # Try ISO date
            try:
                d = datetime.strptime(raw, "%Y-%m-%d").date()
                return (0, d, -stage_rank)
            except ValueError:
                pass
            # Try GA Month enum like "Apr 26"
            try:
                parts = raw.split()
                if len(parts) == 2:
                    month_num = GA_MONTH_MAP.get(parts[0][:3], 0)
                    yr_raw = parts[1]
                    year = 2000 + int(yr_raw) if len(yr_raw) <= 2 else int(yr_raw)
                    if month_num:
                        return (0, date(year, month_num, 1), -stage_rank)
            except (ValueError, TypeError):
                pass

        return (1, date.max, -stage_rank)

    # -------------------------------------------------------------------------
    # Progress / time bars
    # -------------------------------------------------------------------------

    def _progress_bar(self, issues):
        if not issues:
            return ""
        bar = ""
        done = inp = todo = 0
        for i in issues:
            cat = i.get("effective_category")
            if cat == "Done":
                bar += "▓"; done += 1
            elif cat == "In Progress":
                bar += "▒"; inp += 1
            else:
                bar += "░"; todo += 1
        return f"`{bar} {done} done · {inp} in progress · {todo} to do`"

    def _time_bar(self, issues, pkey=None):
        # Epic-level original estimate (if available)
        epic = self.epic_data.get(pkey) if pkey else None
        orig_est = ((epic or {}).get("fields", {}).get("timeoriginalestimate") or 0) / 28800

        # Actual = timespent on Done tickets; remaining = orig estimates on open tickets
        done_issues = [i for i in issues if i.get("effective_category") == "Done"]
        open_issues = [i for i in issues if i.get("effective_category") != "Done"]
        act = sum((i.get("fields", {}).get("timespent") or 0) for i in done_issues) / 28800
        rem = sum((i.get("fields", {}).get("timeoriginalestimate") or 0) for i in open_issues) / 28800

        if orig_est == 0:
            # Fallback: no epic estimate — use sum of child estimates as the budget
            child_est = sum((i.get("fields", {}).get("timeoriginalestimate") or 0) for i in issues) / 28800
            if child_est == 0 and act == 0:
                return "`👀 no time data`"
            if child_est == 0:
                return f"`👀 {act:.1f}d logged / no estimates`"
            orig_est = child_est  # treat child sum as the budget and fall through

        pct = int((act + rem) / orig_est * 100)
        actual_over   = act > orig_est
        combined_over = (act + rem) > orig_est
        prefix = "❌ " if actual_over else ("⚠️ " if combined_over else ("👀 " if pct >= 90 else ""))
        return f"`{prefix}{orig_est:.1f}d estimated · {act:.1f}d actual · {rem:.1f}d remaining ({pct}%)`"

    # -------------------------------------------------------------------------
    # Milestone bullets
    # -------------------------------------------------------------------------

    def _milestone_bullet(self, label, key, date_str, stage, prev_missed):
        """Returns (bullet_text, missed_bool)."""
        if not date_str:
            return f"* ❓ {label} - not set", False
        try:
            m_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return f"* ❓ {label} - {date_str}", False

        curr_rank = STAGE_RANKS.get(stage, 0)
        req_rank = MILESTONE_REQUIREMENTS.get(key, 0)
        is_hit = curr_rank >= req_rank
        passed = m_date < self.today

        missed = False
        if passed:
            emoji = "✅" if is_hit else "❌"
            missed = not is_hit
        elif prev_missed:
            emoji = "⚠️"
        else:
            emoji = "🎯"

        return f"* {emoji} {label} - {self._fmt_day(m_date)}", missed

    # -------------------------------------------------------------------------
    # Issue bullets
    # -------------------------------------------------------------------------

    def _format_versions(self, fields):
        versions = fields.get("fixVersions") or []
        if not versions:
            return "👀 Unprioritized"
        names = [re.sub(r"^Platform-", "", v.get("name", "")) for v in versions]
        return " / ".join(n for n in names if n)

    def _issue_bullet(self, issue):
        key = issue["key"]
        f = issue.get("fields", {})
        summary = (f.get("summary") or "")
        assignee = (((f.get("assignee") or {}).get("displayName") or "Unassigned")).split(" ")[0]
        status_name = ((f.get("status") or {}).get("name") or "")
        est = (f.get("timeoriginalestimate") or 0) / 28800
        act = (f.get("timespent") or 0) / 28800

        est_str = f"{est:.1f}d estimated" if est > 0 else "Unestimated 👀"
        act_str = f"{act:.1f}d actual" if act > 0 else "No actual 👀"

        priority = ((f.get("priority") or {}).get("name") or "")
        version = self._format_versions(f)

        main = f"[{key}]({self._jira_url(key)}) — {summary} — {assignee}"
        meta_parts = [status_name, est_str, act_str]
        if priority:
            meta_parts.append(priority)
        meta_parts.append(version)
        meta = " · ".join(meta_parts)

        return f"- {main}||{meta}"

    # -------------------------------------------------------------------------
    # Flag logic
    # -------------------------------------------------------------------------

    def _get_next_milestone(self, stage, milestones):
        """Return (label, date_or_None) for the next relevant milestone."""
        stage_map = {
            "Development": ("QA Start", "qa_start"),
            "In QA": ("UAT Start", "uat_start"),
            "In UAT": ("Beta Start", "beta_start"),
            "Beta": ("GA", "ga_target"),
        }
        label, key = stage_map.get(stage, ("GA", "ga_target"))
        date_str = milestones.get(key)

        # Fallback chains
        if not date_str and key in ("uat_start", "beta_start"):
            label, key = "GA", "ga_target"
            date_str = milestones.get(key)
        if not date_str:
            label, key = "GA", "ga_target"
            date_str = milestones.get("ga_target") or milestones.get("ga_date")

        if date_str:
            try:
                return label, datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                pass
        return label, None

    def _compute_flags(self, project, issues):
        flags = []
        stage = project.get("stage", "")
        m = project.get("milestones", {})
        status = project.get("status") or project.get("last_status_type", "")

        open_issues = [i for i in issues if i.get("effective_category") != "Done"]
        unassigned = [
            i for i in open_issues
            if not ((i.get("fields", {}).get("assignee") or {}).get("displayName"))
        ]

        next_label, next_date = self._get_next_milestone(stage, m)

        # Unassigned near milestone
        if unassigned and next_date:
            days = (next_date - self.today).days
            if -7 <= days <= 7:
                date_fmt = self._fmt_day(next_date)
                if days >= 0:
                    flags.append(
                        f"⚠️ {len(unassigned)} unassigned stories with {next_label} in {days}d ({date_fmt}) — assign soon"
                    )
                else:
                    flags.append(
                        f"⚠️ {len(unassigned)} unassigned stories with {next_label} {abs(days)}d ago ({date_fmt}) — assign soon"
                    )

        # Pipeline slip
        if next_date and open_issues:
            days_past = (self.today - next_date).days
            if days_past > 7:
                flags.append(
                    f"⚠️ {next_label} was {days_past}d ago but {len(open_issues)} stories still open — worth a check?"
                )

        # Last status
        if status in ("at_risk", "off_track"):
            flags.append(f"⚠️ Last status was `{status.replace('_', ' ')}` — checking in")

        return flags

    # -------------------------------------------------------------------------
    # Card renderer
    # -------------------------------------------------------------------------

    def _render_active_card(self, project, issues):
        pkey = self._get_pkey(project)
        name = project.get("name", "Unknown")
        asana_url = self._asana_url(project)
        stage = project.get("stage", "")
        prd = project.get("prd_link") or project.get("prd")

        # Header line
        if pkey:
            header = f"### [{name}]({asana_url}) · [{pkey}]({self._jira_url(pkey)}) · {stage}"
        else:
            header = f"### [{name}]({asana_url}) · {stage}"
        md = header + "\n"
        if prd:
            md += f"PRD: {prd}\n"

        # Minimal card: no Jira link
        if not pkey:
            md += "\n`👀 no time data`\n\n"
            md += "⚠️ No Jira link set — Jira stories needed to track progress\n\n"
            return md

        # Minimal card: Jira link set but no stories
        if not issues:
            md += "\n`👀 no time data`\n\n"
            md += (
                f"⚠️ Jira link set but no child stories found — "
                f"stories need to be created in [{pkey}]({self._jira_url(pkey)})\n\n"
            )
            return md

        # Progress bar
        md += "\n" + self._progress_bar(issues) + "\n"
        # Time bar
        md += "\n" + self._time_bar(issues, pkey) + "\n"

        # Milestone bullets
        m = project.get("milestones", {})
        prev_missed = False
        md += "\n"
        for label, key in [
            ("QA Start", "qa_start"),
            ("UAT Start", "uat_start"),
            ("Beta Start", "beta_start"),
            ("GA", "ga_target"),
        ]:
            if label == "Beta Start" and not m.get(key):
                continue  # Beta is optional — omit if not set
            bullet, missed = self._milestone_bullet(label, key, m.get(key), stage, prev_missed)
            md += bullet + "\n"
            if missed:
                prev_missed = True

        # Flags
        flags = self._compute_flags(project, issues)
        if flags:
            md += "\n"
            for f in flags:
                md += f + "\n"

        # Done section
        done_issues = [i for i in issues if i.get("effective_category") == "Done"]
        if done_issues:
            d_est = sum((i.get("fields", {}).get("timeoriginalestimate") or 0) for i in done_issues) / 28800
            d_act = sum((i.get("fields", {}).get("timespent") or 0) for i in done_issues) / 28800
            est_str = f"{d_est:.1f}d estimated" if d_est > 0 else "Unestimated 👀"
            act_str = f"{d_act:.1f}d actual" if d_act > 0 else "No actual 👀"
            md += f"\n**Done:** {len(done_issues)} issues\n~~{est_str} · {act_str}\n"

        # In Progress section
        inp = sorted(
            [i for i in issues if i.get("effective_category") == "In Progress"],
            key=self._priority_rank,
        )
        if inp:
            inp_est = sum((i.get("fields", {}).get("timeoriginalestimate") or 0) for i in inp) / 28800
            inp_act = sum((i.get("fields", {}).get("timespent") or 0) for i in inp) / 28800
            remaining = inp_est - inp_act
            h = f"**In Progress:** {len(inp)} issues"
            if remaining > 0:
                h += f" · ~{remaining:.1f}d est remaining"
            md += f"\n{h}\n"
            for i in inp:
                md += self._issue_bullet(i) + "\n"

        # To Do section
        todo = sorted(
            [i for i in issues if i.get("effective_category") == "To Do"],
            key=self._priority_rank,
        )
        if todo:
            md += f"\n**To Do:** {len(todo)} issues\n"
            for i in todo:
                md += self._issue_bullet(i) + "\n"

        return md + "\n"

    # -------------------------------------------------------------------------
    # Data Quality section
    # -------------------------------------------------------------------------

    def _render_data_quality(self, issues_by_name):
        """issues_by_name: {project_name: [issues]} for active projects only."""
        all_issues = [i for issues in issues_by_name.values() for i in issues]
        in_progress = [i for i in all_issues if i.get("effective_category") == "In Progress"]

        md = "## ⚙️ Data Quality\n"

        if not in_progress:
            md += "No in-progress issues found.\n\n"
            return md

        # --- Estimates (in-progress) ---
        with_est = [i for i in in_progress if (i.get("fields", {}).get("timeoriginalestimate") or 0) > 0]
        pct = int(len(with_est) / len(in_progress) * 100)

        eng_est = {}
        for i in in_progress:
            name = (((i.get("fields", {}).get("assignee") or {}).get("displayName")) or "Unassigned")
            if name == "Unassigned":
                continue
            first = name.split(" ")[0]
            eng_est.setdefault(first, {"total": 0, "estimated": 0})
            eng_est[first]["total"] += 1
            if (i.get("fields", {}).get("timeoriginalestimate") or 0) > 0:
                eng_est[first]["estimated"] += 1

        # --- Actuals (QA-stage issues only) ---
        qa_statuses = {"Merged to QA", "In QA", "QA Revise"}
        qa_issues = [
            i for i in all_issues
            if (i.get("fields", {}).get("status", {}).get("name", "")) in qa_statuses
        ]

        eng_act = {}
        pct_act = 0
        best_name = None
        if qa_issues:
            with_act = [i for i in qa_issues if (i.get("fields", {}).get("timespent") or 0) > 0]
            pct_act = int(len(with_act) / len(qa_issues) * 100)
            for i in qa_issues:
                name = (((i.get("fields", {}).get("assignee") or {}).get("displayName")) or "Unassigned")
                if name == "Unassigned":
                    continue
                first = name.split(" ")[0]
                eng_act.setdefault(first, {"total": 0, "logged": 0})
                eng_act[first]["total"] += 1
                if (i.get("fields", {}).get("timespent") or 0) > 0:
                    eng_act[first]["logged"] += 1
            for c in eng_act.values():
                c["pct"] = int(c["logged"] / c["total"] * 100) if c["total"] else 0
            if eng_act:
                best_name = max(eng_act, key=lambda k: (eng_act[k]["pct"], eng_act[k]["logged"]))

        # --- Combined Estimates + Actuals table ---
        md += f"**Estimates:** {len(with_est)}/{len(in_progress)} in-progress ({pct}%)\n"
        if qa_issues:
            md += f"**Actuals:** {len(with_act)}/{len(qa_issues)} in QA ({pct_act}%)\n"
        md += "\n"

        all_engs = sorted(set(list(eng_est.keys()) + list(eng_act.keys())))
        if all_engs:
            md += "| Engineer | Estimates | Actuals |\n|---|---|---|\n"
            for eng in all_engs:
                est_c = eng_est.get(eng)
                if est_c:
                    ep = int(est_c["estimated"] / est_c["total"] * 100) if est_c["total"] else 0
                    eflag = " 👀" if est_c["estimated"] == 0 or (ep < 20 and est_c["total"] >= 3) else ""
                    est_cell = f"{est_c['estimated']}/{est_c['total']} ({ep}%){eflag}"
                else:
                    est_cell = "—"

                act_c = eng_act.get(eng)
                if act_c:
                    ap = act_c["pct"]
                    if eng == best_name and act_c["logged"] > 0:
                        aflag = " 👏"
                    elif act_c["logged"] == 0 or (ap < 20 and act_c["total"] >= 3):
                        aflag = " 👀"
                    else:
                        aflag = ""
                    act_cell = f"{act_c['logged']}/{act_c['total']} ({ap}%){aflag}"
                else:
                    act_cell = "—"

                md += f"| {eng} | {est_cell} | {act_cell} |\n"
            md += "\n"

        # --- Unprioritized ---
        unprio = [i for i in in_progress if not (i.get("fields", {}).get("fixVersions") or [])]
        pct_unprio = int(len(unprio) / len(in_progress) * 100)
        md += f"**Unprioritized:** {len(unprio)} of {len(in_progress)} in-progress issues have no fix version set ({pct_unprio}%)\n\n"

        proj_unprio = {}
        for proj_name, issues in issues_by_name.items():
            proj_inp = [i for i in issues if i.get("effective_category") == "In Progress"]
            proj_unprio_count = sum(1 for i in proj_inp if not (i.get("fields", {}).get("fixVersions") or []))
            if proj_unprio_count > 0:
                proj_unprio[proj_name] = {"unprio": proj_unprio_count, "total": len(proj_inp)}

        if proj_unprio:
            md += "| Project | Unprioritized |\n|---|---|\n"
            for proj_name, counts in sorted(proj_unprio.items(), key=lambda x: -x[1]["unprio"]):
                p = int(counts["unprio"] / counts["total"] * 100) if counts["total"] else 0
                flag = " 👀" if p == 100 else ""
                md += f"| {proj_name} | {counts['unprio']}/{counts['total']} ({p}%){flag} |\n"

        return md + "\n"

    # -------------------------------------------------------------------------
    # Summary section
    # -------------------------------------------------------------------------

    def _render_summary(self, active_projects, issues_by_pkey):
        md = "## 📋 Summary\n"
        next_steps = []

        for idx, project in enumerate(active_projects, start=1):
            pkey = self._get_pkey(project)
            name = project.get("name", "Unknown")
            asana_url = self._asana_url(project)
            stage = project.get("stage", "")
            status = project.get("status") or ""

            issues = issues_by_pkey.get(pkey, []) if pkey else []
            done = sum(1 for i in issues if i.get("effective_category") == "Done")
            inp = sum(1 for i in issues if i.get("effective_category") == "In Progress")
            todo = sum(1 for i in issues if i.get("effective_category") == "To Do")
            open_issues = [i for i in issues if i.get("effective_category") != "Done"]

            if pkey:
                proj_link = f"[{name}]({asana_url}) ([{pkey}]({self._jira_url(pkey)}))"
            else:
                proj_link = f"[{name}]({asana_url})"

            line = f"{proj_link} is in **{stage}** — {done} done · {inp} in progress · {todo} to do."

            if not pkey:
                line += " 🎯 No Jira link set"
                next_steps.append((1, f"🎯 [{name}]({asana_url}): Add Jira link — no stories can be tracked without it"))
            else:
                # Priority breakdown of open work
                p_counts = {}
                for i in open_issues:
                    p = ((i.get("fields", {}).get("priority") or {}).get("name") or "")
                    if p:
                        p_counts[p] = p_counts.get(p, 0) + 1
                if p_counts:
                    parts = []
                    for p in ("P1", "P2", "P3", "P4"):
                        if p in p_counts:
                            prefix = "👀 " if p == "P1" else ""
                            parts.append(f"{prefix}{p_counts[p]} {p}")
                    if parts:
                        line += f" Open work: {', '.join(parts)}."

            if status == "off_track":
                line += f" 🎯 Last status was `{status}` — checking in"
                next_steps.append((2, f"🎯 {proj_link}: Last status was `{status}` — checking in"))
            elif status == "at_risk":
                line += f" Last status was `{status}`"

            md += f"{idx}. {line}\n"

        if next_steps:
            md += "\n**Next Steps**\n"
            for _, step in sorted(next_steps, key=lambda x: x[0]):
                md += f"- {step}\n"

        return md + "\n"

    # -------------------------------------------------------------------------
    # Top-level render
    # -------------------------------------------------------------------------

    def render(self):
        today_str = datetime.now().strftime("%B %-d, %Y")

        active_stages = {"Development", "In QA", "In UAT", "Beta", "GA"}
        discovery_stages = {"Discovery", "Study"}
        backlog_stages = {"On hold", "Backlog"}

        active = [p for p in self.asana_data if p.get("stage") in active_stages]
        discovery = [p for p in self.asana_data if p.get("stage") in discovery_stages]
        backlog = [p for p in self.asana_data if p.get("stage") in backlog_stages]

        # Sort active: soonest GA first, then stage rank descending
        active.sort(key=self._parse_ga_sort_key)

        # Build lookup maps
        issues_by_pkey = {}
        issues_by_name = {}
        for p in active:
            pkey = self._get_pkey(p)
            name = p.get("name", pkey or "Unknown")
            if pkey:
                issues = self.project_issues.get(pkey, [])
                issues_by_pkey[pkey] = issues
                issues_by_name[name] = issues

        md = f"# Platform Weekly Status — {today_str}\n\n"

        # 1. Summary
        md += self._render_summary(active, issues_by_pkey)

        # 3. Active Projects
        md += "---\n## 🟢 Active Projects\n\n"
        for p in active:
            pkey = self._get_pkey(p)
            issues = issues_by_pkey.get(pkey, []) if pkey else []
            md += self._render_active_card(p, issues)

        # 4. Discovery
        if discovery:
            md += "---\n## 🟣 Discovery\n\n"
            for p in discovery:
                name = p.get("name", "Unknown")
                asana_url = self._asana_url(p)
                pkey = self._get_pkey(p)
                stage = p.get("stage", "")
                if pkey:
                    md += f"- [{name}]({asana_url}) · [{pkey}]({self._jira_url(pkey)}) · {stage}\n"
                else:
                    md += f"- [{name}]({asana_url}) · {stage}\n"
            md += "\n"

        # 5. Backlog
        if backlog:
            md += "---\n## ⚪ Backlog\n\n"
            for p in backlog:
                name = p.get("name", "Unknown")
                asana_url = self._asana_url(p)
                stage = p.get("stage", "")
                status = p.get("status") or ""
                line = f"- [{name}]({asana_url}) · {stage}"
                if status in ("at_risk", "off_track"):
                    line += f" ⚠️ Last status: {status.replace('_', ' ')}"
                md += line + "\n"
            md += "\n"

        # 6. Data Quality (sidebar)
        md += self._render_data_quality(issues_by_name)

        return md
