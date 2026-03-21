import tempfile
import unittest
from pathlib import Path

import yaml

from tune.orchestrator import build_plan, build_run_plan


class TestOrchestrator(unittest.TestCase):
    def test_build_plan_generates_skill_model_pairs_from_config(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills" / "concerns"
            evals_dir = root / "evals"
            skills_dir.mkdir(parents=True)
            evals_dir.mkdir(parents=True)
            (skills_dir / "security-injection.md").write_text("skill", encoding="utf-8")
            (skills_dir / "correctness.md").write_text("skill", encoding="utf-8")
            (evals_dir / "security-injection.json").write_text("{}", encoding="utf-8")
            (evals_dir / "correctness.json").write_text("{}", encoding="utf-8")

            config = root / "config.yaml"
            config.write_text(
                yaml.safe_dump({"models": ["gpt-4.1", "claude-sonnet-4-20250514"]}),
                encoding="utf-8",
            )

            pairs = build_plan(
                skills_dir=root / "skills",
                evals_dir=evals_dir,
                config_path=config,
                skills_filter=None,
                models_filter=None,
            )

        self.assertEqual(
            pairs,
            [
                ("correctness", "claude-sonnet-4-20250514"),
                ("correctness", "gpt-4.1"),
                ("security-injection", "claude-sonnet-4-20250514"),
                ("security-injection", "gpt-4.1"),
            ],
        )

    def test_build_run_plan_applies_filters_trigger_and_run_id(self):
        pairs = [
            ("correctness", "claude-sonnet-4-20250514"),
            ("correctness", "gpt-4.1"),
            ("security-injection", "claude-sonnet-4-20250514"),
            ("security-injection", "gpt-4.1"),
        ]
        run_plan = build_run_plan(
            pairs=pairs,
            skills_filter=["security-injection"],
            models_filter=["gpt-4.1"],
            trigger="schedule",
            run_id="run-123",
        )
        self.assertEqual(
            run_plan,
            [
                {
                    "run_id": "run-123",
                    "trigger": "schedule",
                    "skill": "security-injection",
                    "model": "gpt-4.1",
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
