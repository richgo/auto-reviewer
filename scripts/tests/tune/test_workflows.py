import sys
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


class TestAutoResearchWorkflows(unittest.TestCase):
    def _load_workflow(self, name: str):
        repo_root = Path(__file__).resolve().parents[3]
        workflow_path = repo_root / ".github" / "workflows" / name
        return yaml.safe_load(workflow_path.read_text(encoding="utf-8"))

    def test_autoresearch_tuning_workflow_has_schedule_dispatch_and_path_triggers(self):
        workflow = self._load_workflow("autoresearch-tuning.yml")
        self.assertIn("on", workflow)
        self.assertIn("schedule", workflow["on"])
        self.assertIn("workflow_dispatch", workflow["on"])
        self.assertIn("push", workflow["on"])
        self.assertEqual(workflow["on"]["push"]["paths"], ["evals/**", "skills/**"])

    def test_autoresearch_tuning_workflow_serializes_runs_per_skill_model(self):
        workflow = self._load_workflow("autoresearch-tuning.yml")
        jobs = workflow["jobs"]
        self.assertIn("tune_pair", jobs)
        self.assertIn("concurrency", jobs["tune_pair"])
        self.assertEqual(
            jobs["tune_pair"]["concurrency"]["group"],
            "autoresearch-${{ matrix.skill }}-${{ matrix.model }}",
        )

    def test_autoresearch_promote_workflow_enforces_branch_first_and_pr_permissions(self):
        workflow = self._load_workflow("autoresearch-promote.yml")
        self.assertEqual(workflow["permissions"]["contents"], "write")
        self.assertEqual(workflow["permissions"]["pull-requests"], "write")
        self.assertIn("workflow_call", workflow["on"])
        jobs = workflow["jobs"]
        self.assertIn("promote", jobs)
        promote_steps = jobs["promote"]["steps"]
        step_names = [step.get("name", "") for step in promote_steps]
        self.assertIn("Create promotion branch", step_names)
        self.assertIn("Open promotion PR", step_names)

    def test_autoresearch_promote_workflow_includes_regression_revert_job(self):
        workflow = self._load_workflow("autoresearch-promote.yml")
        jobs = workflow["jobs"]
        self.assertIn("revert_on_regression", jobs)
        revert_steps = jobs["revert_on_regression"]["steps"]
        step_names = [step.get("name", "") for step in revert_steps]
        self.assertIn("Detect post-merge regression", step_names)
        self.assertIn("Open revert PR", step_names)
        detect_step = next(step for step in revert_steps if step.get("name") == "Detect post-merge regression")
        open_revert_step = next(step for step in revert_steps if step.get("name") == "Open revert PR")
        self.assertEqual(detect_step.get("id"), "detect")
        self.assertEqual(open_revert_step.get("if"), "${{ steps.detect.outputs.regressed == 'true' }}")


if __name__ == "__main__":
    unittest.main()
