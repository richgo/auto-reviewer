import unittest
from pathlib import Path

import yaml


class TestAdversarialRuntimeConfig(unittest.TestCase):
    def test_apm_config_includes_adversarial_runtime_defaults(self):
        repo_root = Path(__file__).resolve().parents[3]
        apm_path = repo_root / "apm.yml"
        payload = yaml.safe_load(apm_path.read_text(encoding="utf-8"))
        adversarial = payload["config"]["adversarial"]

        self.assertIn("panel_size", adversarial)
        self.assertIn("max_rounds", adversarial)
        self.assertIn("db_path", adversarial)
        self.assertIn("retention_days", adversarial)


if __name__ == "__main__":
    unittest.main()
