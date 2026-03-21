import unittest
from pathlib import Path


class TestAdversarialAgentEntry(unittest.TestCase):
    def test_adversarial_agent_entry_defines_commands_roles_and_confidence_buckets(self):
        repo_root = Path(__file__).resolve().parents[3]
        agent_path = repo_root / "agents" / "adversarial" / "agent.md"

        self.assertTrue(agent_path.exists())

        content = agent_path.read_text(encoding="utf-8")
        self.assertIn("adversarial-review", content)
        self.assertIn("adversarial-resume", content)
        self.assertIn("adversarial-cleanup", content)
        self.assertIn("detector", content.lower())
        self.assertIn("challenger", content.lower())
        self.assertIn("defender", content.lower())
        self.assertIn("judge", content.lower())
        self.assertIn("high-confidence", content.lower())
        self.assertIn("contested", content.lower())
        self.assertIn("debunked", content.lower())


if __name__ == "__main__":
    unittest.main()
