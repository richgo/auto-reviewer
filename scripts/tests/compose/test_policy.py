import unittest
from pathlib import Path

import yaml


class TestComposePolicy(unittest.TestCase):
    def test_policy_contains_signal_mappings_and_fallback_core(self):
        repo_root = Path(__file__).resolve().parents[3]
        policy_path = repo_root / "scripts" / "compose" / "policy.yaml"
        self.assertTrue(policy_path.exists())

        policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
        self.assertIn("core", policy)
        self.assertIn("fallback", policy)
        self.assertIn("signals", policy)
        self.assertIn("python", policy["signals"])
        self.assertIn("ci_github_actions", policy["signals"])
        self.assertIn("review-orchestrator", " ".join(policy["core"]))


if __name__ == "__main__":
    unittest.main()
