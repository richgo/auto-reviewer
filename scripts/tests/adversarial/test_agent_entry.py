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

    def test_adversarial_agent_entry_defines_sqlite_persistence_contract(self):
        repo_root = Path(__file__).resolve().parents[3]
        agent_path = repo_root / "agents" / "adversarial" / "agent.md"
        content = agent_path.read_text(encoding="utf-8").lower()

        self.assertIn(".auto-reviewer/adversarial.db", content)
        self.assertIn("runs", content)
        self.assertIn("findings", content)
        self.assertIn("stances", content)
        self.assertIn("verdicts", content)
        self.assertIn("cleanup", content)
        self.assertIn("repo, pr, commit_sha", content)
        self.assertIn("transaction", content)

    def test_adversarial_agent_entry_defines_explicit_round_order(self):
        repo_root = Path(__file__).resolve().parents[3]
        agent_path = repo_root / "agents" / "adversarial" / "agent.md"
        content = agent_path.read_text(encoding="utf-8").lower()

        self.assertIn("round order", content)
        self.assertIn("detector -> challenger -> defender -> judge", content)


if __name__ == "__main__":
    unittest.main()
