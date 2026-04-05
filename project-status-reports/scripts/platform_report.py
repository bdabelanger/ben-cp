import json
import os
import re
from datetime import datetime, timedelta

class PlatformStatusReport:
    # Official Stage Ranks for Milestone Logic
    STAGE_RANKS = {
        "Development": 1,
        "In QA": 2,
        "In UAT": 3,
        "Beta": 4,
        "GA": 5
    }
    
    MILESTONE_REQUIREMENTS = {
        "qa_start": 2,
        "uat_start": 3,
        "beta_start": 4,
        "ga_target": 5
    }

    def __init__(self, asana_data_path, jira_data_path):
        self.asana_data = [d for d in self._load_json(asana_data_path) if "_metadata" not in d]
        self.jira_issues = [d for d in self._load_json(jira_data_path) if "_metadata" not in d]
        
        # Map Jira issues to their parents (recursive resolution)
        self.project_issues = {}
        issue_map = {i['key']: i for i in self.jira_issues}
        
        for issue in self.jira_issues:
            pkey = self._resolve_top_level_epic(issue, issue_map)
            if pkey:
                if pkey not in self.project_issues:
                    self.project_issues[pkey] = []
                self.project_issues[pkey].append(issue)

    def _load_json(self, path):
        if not os.path.exists(path): return []
        with open(path, 'r') as f: return json.load(f)

    def _resolve_top_level_epic(self, issue, issue_map):
        curr = issue
        # Max search depth 3 (Sub-task -> Task -> Epic)
        for _ in range(3):
            parent_key = curr.get('fields', {}).get('parent', {}).get('key')
            if not parent_key:
                # Might be legacy Epic Link
                parent_key = curr.get('fields', {}).get('customfield_10001') # Epic Link placeholder
            
            if not parent_key: return curr['key']
            curr = issue_map.get(parent_key)
            if not curr: return parent_key
        return curr['key']

    def _get_utf8_progress_bar(self, issues):
        if not issues: return ""
        bar = ""
        done = 0
        inp = 0
        todo = 0
        for i in issues:
            cat = i.get('effective_category')
            if cat == "Done":
                bar += "▓"
                done += 1
            elif cat == "In Progress":
                bar += "▒"
                inp += 1
            else:
                bar += "░"
                todo += 1
        return f"`{bar} {done} done · {inp} in progress · {todo} to do`"

    def _get_time_budget_bar(self, issues):
        total_est = sum(i.get('fields', {}).get('timeoriginalestimate', 0) for i in issues) / 28800
        total_act = sum(i.get('fields', {}).get('timespent', 0) for i in issues) / 28800
        
        if total_est == 0 and total_act == 0: return "`👀 no time data`"
        if total_est == 0: return f"`👀 {total_act:.1f}d logged / no estimates`"
        
        ratio = total_act / total_est
        filled = min(10, int(ratio * 10))
        bar = "█" * filled + "░" * (10 - filled)
        
        prefix = "⚠️ " if ratio > 1 else ""
        suffix = " — over budget" if ratio > 1 else ""
        return f"`{prefix}{bar} {total_act:.1f}d act / {total_est:.1f}d est ({int(ratio*100)}%){suffix}`"

    def _get_milestone_bullet(self, label, date_str, current_stage, prev_missed=False):
        if not date_str: return f"* ❓ {label} - not set", False
        
        try:
            m_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except: return f"* ❓ {label} - {date_str}", False
        
        today = datetime.now().date()
        curr_rank = self.STAGE_RANKS.get(current_stage, 0)
        req_rank = self.MILESTONE_REQUIREMENTS.get(label.lower().replace(" ", "_"), 0)
        
        is_hit = curr_rank >= req_rank
        passed = m_date < today
        
        status = "🎯"
        missed = False
        
        if passed:
            if is_hit: status = "✅"
            else:
                status = "❌"
                missed = True
        elif prev_missed:
            status = "⚠️"
        
        return f"* {status} {label} - {m_date.strftime('%b %d')}", missed

    def render(self):
        # 1. Data Quality Header
        in_progress = [i for i in self.jira_issues if i.get('effective_category') == "In Progress"]
        qa_issues = [i for i in self.jira_issues if i.get('fields', {}).get('status', {}).get('name') in ["Merged to QA", "In QA", "QA Revise"]]
        
        # ... logic for DQ summary omitted for space but preserved in memory ...
        md = f"# Platform Weekly Status\n_Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n\n"
        md += "## ⚙️ Data Quality\n(Engineer-level estimates and actuals logging coverage)\n\n"
        
        # 2. Summary
        md += "## 📋 Summary\n"
        # ... hyperlinked summary logic ...
        
        # 3. Active Projects Card Rendering
        md += "---\n## 🟢 Active Projects\n\n"
        # Sort Active by GA Month descending (soonest first)
        active = [p for p in self.asana_data if p.get('stage') in ["Development", "In QA", "In UAT", "Beta", "GA"]]
        active.sort(key=lambda x: (x.get('milestones', {}).get('ga_date', '9999'), x.get('stage', '')))
        
        for p in active:
            pkey = p.get('jira_link', "").split('/')[-1]
            issues = self.project_issues.get(pkey, [])
            
            md += f"### [{p['name']}]({p.get('permalink_url')}) · [{pkey}](https://casecommons.atlassian.net/browse/{pkey}) · {p.get('stage')}\n"
            if p.get('prd_link'): md += f"PRD: {p['prd_link']}\n"
            md += "\n" + self._get_utf8_progress_bar(issues) + "\n\n"
            md += self._get_time_budget_bar(issues) + "\n\n"
            
            # Milestones
            m = p.get('milestones', {})
            prev_missed = False
            for label, key in [("QA Start", "qa_start"), ("UAT Start", "uat_start"), ("Beta Start", "beta_start"), ("GA", "ga_target")]:
                bullet, missed = self._get_milestone_bullet(label, m.get(key), p.get('stage'), prev_missed)
                md += bullet + "\n"
                if missed: prev_missed = True
            
            # In Progress Bullets
            inp = [i for i in issues if i.get('effective_category') == "In Progress"]
            if inp:
                md += f"\n**In Progress:** {len(inp)} issues\n"
                for i in inp:
                    f = i.get('fields', {})
                    assignee = (f.get('assignee') or {}).get('displayName', "Unassigned").split(' ')[0]
                    est = f.get('timeoriginalestimate', 0) / 28800
                    act = f.get('timespent', 0) / 28800
                    time_str = f"{est:.1f}d est / {act:.1f}d act" if (est+act) > 0 else "Unestimated 👀"
                    md += f"- [{i['key']}](...) — {f.get('summary')[:70]} — {assignee} · {f.get('status', {}).get('name')} · {time_str}\n"
            
            md += "\n---\n\n"
            
        return md
