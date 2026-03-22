import json
import tempfile
import unittest
from pathlib import Path

from tune.orchestrator import build_plan


class TestEvalResolution(unittest.TestCase):
    def test_build_plan_uses_skill_mapped_eval_inputs_without_review_task_identifiers(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills" / "concerns"
            evals_dir = root / "evals"
            skills_dir.mkdir(parents=True)
            evals_dir.mkdir(parents=True)

            (skills_dir / "security-auth.md").write_text("skill", encoding="utf-8")
            (evals_dir / "security-auth.json").write_text(
                json.dumps(
                    {
                        "source_of_truth": "skill-eval",
                        "skill": "security-auth",
                        "review_task": "security/auth-bypass",
                        "cases": [],
                    }
                ),
                encoding="utf-8",
            )
            (root / "config.yaml").write_text('models: ["gpt-4.1"]\n', encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "review_task"):
                build_plan(
                    skills_dir=root / "skills",
                    evals_dir=evals_dir,
                    config_path=root / "config.yaml",
                    skills_filter=None,
                    models_filter=None,
                )


if __name__ == "__main__":
    unittest.main()

