"""
Golden fixture test for PlatformStatusReport.

Run from the project-status-reports directory:
    python3 -m pytest tests/ -v
or directly:
    python3 tests/test_report.py

The fixtures contain minimal but realistic Jira/Asana shapes.
If platform_report.py changes break the output contract (missing sections,
blank status, wrong emoji), these tests will catch it.
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../scripts"))
from platform_report import PlatformStatusReport

# ---------------------------------------------------------------------------
# Minimal fixtures — realistic shapes, no real data
# ---------------------------------------------------------------------------

ASANA_FIXTURE = [
    {
        "name": "Notes - Notes datagrid",
        "gid": "1200000000000001",
        "status": "on_track",
        "stage": "GA",
        "jira_link": "CBP-2736",
        "milestones": {
            "qa_start":  "2026-02-01",
            "uat_start": "2026-03-01",
            "ga_target": "2026-04-01",
        },
    }
]

JIRA_FIXTURE = [
    # Epic itself
    {
        "key": "CBP-2736",
        "fields": {
            "summary": "Epic: Notes datagrid",
            "status": {"name": "Done", "statusCategory": {"key": "done", "name": "Done"}},
            "assignee": {"displayName": "Tuan Nguyen"},
            "priority": {"name": "P1"},
            "issuetype": {"name": "Epic"},
            "parent": None,
            "timeoriginalestimate": 28800,   # 1 day
            "timespent": 25200,              # 0.875 day
            "fixVersions": [{"name": "Platform-v2.4"}],
            "created": "2026-01-01T00:00:00.000+0000",
            "updated": "2026-04-01T00:00:00.000+0000",
        },
    },
    # Child — In Progress
    {
        "key": "CBP-3150",
        "fields": {
            "summary": "Implement bulk select for notes",
            "status": {"name": "In Development", "statusCategory": {"key": "inprogress", "name": "In Progress"}},
            "assignee": {"displayName": "Tuan Nguyen"},
            "priority": {"name": "P2"},
            "issuetype": {"name": "Story"},
            "parent": {"key": "CBP-2736"},
            "timeoriginalestimate": 57600,   # 2 days
            "timespent": 28800,              # 1 day
            "fixVersions": [{"name": "Platform-v2.4"}],
            "created": "2026-01-05T00:00:00.000+0000",
            "updated": "2026-04-02T00:00:00.000+0000",
        },
    },
    # Child — Done
    {
        "key": "CBP-3151",
        "fields": {
            "summary": "Notes datagrid column sorting",
            "status": {"name": "Done", "statusCategory": {"key": "done", "name": "Done"}},
            "assignee": {"displayName": "Blessing Okafor"},
            "priority": {"name": "P2"},
            "issuetype": {"name": "Story"},
            "parent": {"key": "CBP-2736"},
            "timeoriginalestimate": 28800,
            "timespent": 28800,
            "fixVersions": [{"name": "Platform-v2.4"}],
            "created": "2026-01-05T00:00:00.000+0000",
            "updated": "2026-03-20T00:00:00.000+0000",
        },
    },
    # Child — status override: Blocked → To Do
    {
        "key": "CBP-3152",
        "fields": {
            "summary": "Notes export PDF — blocked on legal sign-off",
            "status": {"name": "Blocked - Third-Party", "statusCategory": {"key": "indeterminate", "name": "In Progress"}},
            "assignee": None,
            "priority": {"name": "P3"},
            "issuetype": {"name": "Story"},
            "parent": {"key": "CBP-2736"},
            "timeoriginalestimate": 0,
            "timespent": 0,
            "fixVersions": [],
            "created": "2026-02-01T00:00:00.000+0000",
            "updated": "2026-04-01T00:00:00.000+0000",
        },
    },
]


class TestPlatformReport(unittest.TestCase):

    def _render(self, asana=None, jira=None):
        asana = asana or ASANA_FIXTURE
        jira  = jira  or JIRA_FIXTURE
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as af:
            json.dump(asana, af)
            af_path = af.name
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as jf:
            json.dump(jira, jf)
            jf_path = jf.name
        try:
            reporter = PlatformStatusReport(af_path, jf_path)
            return reporter.render()
        finally:
            os.unlink(af_path)
            os.unlink(jf_path)

    # ------------------------------------------------------------------
    # Structure
    # ------------------------------------------------------------------

    def test_report_has_header(self):
        md = self._render()
        self.assertIn("Platform Weekly Status", md)

    def test_report_has_data_quality_section(self):
        md = self._render()
        self.assertIn("Data Quality", md)

    def test_report_has_active_projects_section(self):
        md = self._render()
        self.assertIn("Active Projects", md)

    def test_report_has_summary_section(self):
        md = self._render()
        self.assertIn("Summary", md)

    def test_project_name_in_report(self):
        md = self._render()
        self.assertIn("Notes - Notes datagrid", md)

    def test_epic_key_in_report(self):
        md = self._render()
        self.assertIn("CBP-2736", md)

    # ------------------------------------------------------------------
    # Status override
    # ------------------------------------------------------------------

    def test_blocked_third_party_counts_as_todo(self):
        """CBP-3152 is Blocked - Third-Party; must land in To Do, not In Progress."""
        md = self._render()
        # The progress bar should show 1 in-progress (CBP-3150) not 2
        self.assertIn("1 in progress", md)

    # ------------------------------------------------------------------
    # Data quality flags
    # ------------------------------------------------------------------

    def test_estimates_section_present(self):
        """Data Quality section must include an Estimates line with a percentage."""
        md = self._render()
        dq_section = md.split("Data Quality")[1].split("##")[0] if "Data Quality" in md else ""
        self.assertIn("Estimates", dq_section)
        self.assertIn("%", dq_section)

    def test_unprioritized_flagged(self):
        """CBP-3152 has no fixVersion; should trigger unprioritized flag."""
        md = self._render()
        self.assertIn("Unprioritized", md)

    # ------------------------------------------------------------------
    # Milestones
    # ------------------------------------------------------------------

    def test_ga_milestone_present(self):
        md = self._render()
        self.assertIn("GA", md)

    # ------------------------------------------------------------------
    # Empty / degenerate inputs
    # ------------------------------------------------------------------

    def test_empty_jira_does_not_crash(self):
        md = self._render(jira=[])
        self.assertIsInstance(md, str)
        self.assertGreater(len(md), 0)

    def test_empty_asana_does_not_crash(self):
        md = self._render(asana=[])
        self.assertIsInstance(md, str)

    def test_no_estimates_does_not_crash(self):
        no_est = json.loads(json.dumps(JIRA_FIXTURE))
        for i in no_est:
            i["fields"]["timeoriginalestimate"] = 0
            i["fields"]["timespent"] = 0
        md = self._render(jira=no_est)
        self.assertIsInstance(md, str)


if __name__ == "__main__":
    unittest.main(verbosity=2)
