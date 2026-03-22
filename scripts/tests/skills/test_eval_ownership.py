import json
import unittest
from pathlib import Path


class TestEvalOwnership(unittest.TestCase):
    def test_eval_payloads_explicitly_identify_skill_as_source_of_truth(self):
        repo_root = Path(__file__).resolve().parents[3]
        eval_paths = sorted((repo_root / "evals").glob("*.json"))

        self.assertGreater(len(eval_paths), 0)
        for eval_path in eval_paths:
            payload = json.loads(eval_path.read_text(encoding="utf-8"))
            if "cases" not in payload:
                continue

            with self.subTest(eval_file=eval_path.name):
                self.assertIn(
                    "source_of_truth",
                    payload,
                    msg="eval payload must declare skill ownership explicitly",
                )
                self.assertEqual(payload["source_of_truth"], "skill-eval")
                self.assertIn("skill", payload)
                self.assertNotIn("review_task", payload)
                self.assertNotIn("task_local_eval", payload)


if __name__ == "__main__":
    unittest.main()

