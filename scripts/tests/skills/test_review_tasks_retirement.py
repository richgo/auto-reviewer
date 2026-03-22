import unittest
from pathlib import Path

import yaml


class TestReviewTasksRetirement(unittest.TestCase):
    def test_readme_documents_skill_first_primitives_without_review_tasks_runtime_dependency(self):
        repo_root = Path(__file__).resolve().parents[3]
        readme = (repo_root / "README.md").read_text(encoding="utf-8")
        lowered = readme.lower()

        self.assertIn("skills", lowered)
        self.assertIn("agents", lowered)
        self.assertNotIn("review tasks", lowered)
        self.assertNotIn("review-tasks/", lowered)

    def test_tuning_and_benchmark_workflows_do_not_reference_review_tasks_directory(self):
        repo_root = Path(__file__).resolve().parents[3]
        workflow_names = ["autoresearch-tuning.yml", "benchmark.yml"]
        for workflow_name in workflow_names:
            with self.subTest(workflow=workflow_name):
                workflow = yaml.safe_load(
                    (repo_root / ".github" / "workflows" / workflow_name).read_text(
                        encoding="utf-8"
                    )
                )
                dumped = yaml.safe_dump(workflow, sort_keys=False).lower()
                self.assertNotIn("review-tasks/", dumped)
                self.assertNotIn("review tasks", dumped)

    def test_tuning_readme_no_longer_uses_review_tasks_as_active_eval_or_skill_source(self):
        repo_root = Path(__file__).resolve().parents[3]
        tuning_readme = (repo_root / "scripts" / "TUNING_README.md").read_text(encoding="utf-8")
        lowered = tuning_readme.lower()
        self.assertNotIn("review-tasks/", lowered)
        self.assertNotIn("review tasks", lowered)


if __name__ == "__main__":
    unittest.main()

