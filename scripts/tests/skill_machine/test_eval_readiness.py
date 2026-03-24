import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from skill_machine.eval_readiness import validate_eval_readiness


class TestEvalReadiness(unittest.TestCase):
    def test_eval_readiness_rejects_empty_cases(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            eval_path = Path(tmp_dir) / "security-injection.json"
            eval_path.write_text('{"skill":"security-injection","cases":[]}', encoding="utf-8")

            result = validate_eval_readiness(eval_path=eval_path)

        self.assertFalse(result["ready"])
        self.assertIn("at least one case", result["reasons"][0].lower())

    def test_eval_readiness_rejects_when_all_cases_are_positive(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            eval_path = Path(tmp_dir) / "security-injection.json"
            eval_path.write_text(
                """
                {
                  "skill":"security-injection",
                  "cases":[
                    {"id":"p1","assertions":{"must_detect":true}},
                    {"id":"p2","assertions":{"must_detect":true}}
                  ]
                }
                """.strip(),
                encoding="utf-8",
            )

            result = validate_eval_readiness(eval_path=eval_path)

        self.assertFalse(result["ready"])
        self.assertTrue(any("negative" in reason.lower() for reason in result["reasons"]))

    def test_eval_readiness_rejects_when_all_cases_are_negative(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            eval_path = Path(tmp_dir) / "security-injection.json"
            eval_path.write_text(
                """
                {
                  "skill":"security-injection",
                  "cases":[
                    {"id":"n1","assertions":{"must_not_detect":true}},
                    {"id":"n2","assertions":{"must_not_detect":true}}
                  ]
                }
                """.strip(),
                encoding="utf-8",
            )

            result = validate_eval_readiness(eval_path=eval_path)

        self.assertFalse(result["ready"])
        self.assertTrue(any("positive" in reason.lower() for reason in result["reasons"]))


if __name__ == "__main__":
    unittest.main()
