import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tune.autoresearch import build_tuning_policy


class TestTuningPolicy(unittest.TestCase):
    def test_build_tuning_policy_applies_cli_overrides(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "config.yaml"
            config_path.write_text(
                yaml.safe_dump(
                    {
                        "max_rounds": 10,
                        "convergence_rounds": 3,
                        "min_f1_delta": 0.05,
                        "max_fpr_regression": 0.02,
                        "dry_run": False,
                    }
                ),
                encoding="utf-8",
            )
            policy = build_tuning_policy(
                config_path=config_path,
                overrides={
                    "max_rounds": 4,
                    "convergence_rounds": 2,
                    "min_f1_delta": 0.01,
                    "max_fpr_regression": 0.01,
                    "dry_run": True,
                },
            )

        self.assertEqual(policy.max_rounds, 4)
        self.assertEqual(policy.convergence_rounds, 2)
        self.assertEqual(policy.min_f1_delta, 0.01)
        self.assertEqual(policy.max_fpr_regression, 0.01)
        self.assertTrue(policy.dry_run)


if __name__ == "__main__":
    unittest.main()
