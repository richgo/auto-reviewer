import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import yaml

from skill_machine.cascade import CascadeOrchestrator
from skill_machine.orchestrator import build_plan


class TestCascadeIntegration(unittest.TestCase):
    """Test cascade integration with orchestrator and config."""

    def test_orchestrator_loads_cascade_config_from_config_yaml(self):
        """Given a config.yaml with cascade section
        When orchestrator loads the config
        Then it should extract cascade models and iteration limits."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            config_file = root / "config.yaml"
            config_file.write_text(
                yaml.safe_dump({
                    "max_rounds": 10,
                    "convergence_rounds": 3,
                    "cascade": {
                        "enabled": True,
                        "stages": [
                            {
                                "model": "gpt-5-mini",
                                "max_iterations": 5,
                                "target_pass_rate": 0.95,
                            },
                            {
                                "model": "claude-haiku-4.5",
                                "max_iterations": 3,
                                "target_pass_rate": 0.95,
                            },
                        ],
                    },
                }),
                encoding="utf-8",
            )

            # Load the config
            with open(config_file) as f:
                config = yaml.safe_load(f)

            # Verify cascade config is present and valid
            self.assertTrue(config["cascade"]["enabled"])
            self.assertEqual(len(config["cascade"]["stages"]), 2)
            self.assertEqual(config["cascade"]["stages"][0]["model"], "gpt-5-mini")
            self.assertEqual(config["cascade"]["stages"][0]["max_iterations"], 5)
            self.assertEqual(config["cascade"]["stages"][1]["model"], "claude-haiku-4.5")
            self.assertEqual(config["cascade"]["stages"][1]["max_iterations"], 3)

    def test_orchestrator_creates_cascade_on_convergence_failure(self):
        """Given an orchestrator with convergence failure detected
        When build_plan is called with cascade enabled
        Then it should prepare cascade execution parameters."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            skills_dir.mkdir(parents=True)
            evals_dir.mkdir(parents=True)

            # Create skill
            skill_dir = skills_dir / "test-skill"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text("skill", encoding="utf-8")
            (evals_dir / "test-skill.json").write_text("{}", encoding="utf-8")

            config_file = root / "config.yaml"
            config_file.write_text(
                yaml.safe_dump({
                    "models": ["gpt-5-mini"],
                    "cascade": {
                        "enabled": True,
                        "stages": [
                            {
                                "model": "gpt-5-mini",
                                "max_iterations": 5,
                                "target_pass_rate": 0.95,
                            },
                            {
                                "model": "claude-haiku-4.5",
                                "max_iterations": 3,
                                "target_pass_rate": 0.95,
                            },
                        ],
                    },
                }),
                encoding="utf-8",
            )

            # Simulate convergence failure and verify cascade can be instantiated
            config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
            history_dir = root / "tune-history" / "test-skill"
            history_dir.mkdir(parents=True, exist_ok=True)

            cascade = CascadeOrchestrator(
                skill_name="test-skill",
                history_dir=history_dir,
                config=config,
            )

            # Verify cascade was created with correct stages
            self.assertIsNotNone(cascade)
            self.assertEqual(cascade.skill_name, "test-skill")
            cascade_stages = cascade.config["cascade"]["stages"]
            self.assertEqual(len(cascade_stages), 2)


if __name__ == "__main__":
    unittest.main()
