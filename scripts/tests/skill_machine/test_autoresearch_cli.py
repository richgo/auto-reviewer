import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from skill_machine.autoresearch import parse_args


class TestAutoResearchCLI(unittest.TestCase):
    def test_parse_args_reads_new_policy_flags(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skill = root / "skill.md"
            evals = root / "evals.json"
            config = root / "config.yaml"
            skill.write_text("skill", encoding="utf-8")
            evals.write_text('{"cases":[]}', encoding="utf-8")
            config.write_text(yaml.safe_dump({"max_rounds": 9}), encoding="utf-8")

            args = parse_args(
                [
                    "--skill",
                    str(skill),
                    "--evals",
                    str(evals),
                    "--config",
                    str(config),
                    "--max-rounds",
                    "4",
                    "--convergence-rounds",
                    "2",
                    "--min-f1-delta",
                    "0.02",
                    "--max-fpr-regression",
                    "0.01",
                    "--history-file",
                    str(root / "history.jsonl"),
                    "--dry-run",
                ]
            )

        self.assertEqual(args.max_rounds, 4)
        self.assertEqual(args.convergence_rounds, 2)
        self.assertEqual(args.min_f1_delta, 0.02)
        self.assertEqual(args.max_fpr_regression, 0.01)
        self.assertTrue(args.dry_run)
        self.assertEqual(args.config, config)
        self.assertEqual(args.history_file, root / "history.jsonl")

    def test_parse_args_uses_default_config_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skill = root / "skill.md"
            evals = root / "evals.json"
            skill.write_text("skill", encoding="utf-8")
            evals.write_text('{"cases":[]}', encoding="utf-8")

            args = parse_args(
                [
                    "--skill",
                    str(skill),
                    "--evals",
                    str(evals),
                ]
            )

        self.assertTrue(str(args.config).endswith("scripts/skill_machine/config.yaml"))

    def test_parse_args_leaves_model_unset_when_not_provided(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skill = root / "skill.md"
            evals = root / "evals.json"
            skill.write_text("skill", encoding="utf-8")
            evals.write_text('{"cases":[]}', encoding="utf-8")

            args = parse_args(
                [
                    "--skill",
                    str(skill),
                    "--evals",
                    str(evals),
                ]
            )

        self.assertIsNone(args.model)


if __name__ == "__main__":
    unittest.main()
