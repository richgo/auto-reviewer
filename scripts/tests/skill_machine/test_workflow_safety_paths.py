import sys
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


class TestWorkflowSafetyPaths(unittest.TestCase):
    def _workflow(self, name: str):
        repo_root = Path(__file__).resolve().parents[3]
        path = repo_root / ".github" / "workflows" / name
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_tuning_workflow_invokes_promote_workflow(self):
        workflow = self._workflow("autoresearch-tuning.yml")
        jobs = workflow["jobs"]
        self.assertIn("promote", jobs)
        promote_job = jobs["promote"]
        self.assertEqual(promote_job["uses"], "./.github/workflows/autoresearch-promote.yml")


if __name__ == "__main__":
    unittest.main()
