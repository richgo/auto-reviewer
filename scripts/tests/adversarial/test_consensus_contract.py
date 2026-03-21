import unittest
from pathlib import Path


class TestAdversarialConsensusContract(unittest.TestCase):
    def test_adversarial_agent_defines_canonical_fingerprint_and_sql_routing(self):
        repo_root = Path(__file__).resolve().parents[3]
        agent_path = repo_root / "agents" / "adversarial" / "agent.md"
        content = agent_path.read_text(encoding="utf-8").lower()

        self.assertIn("canonical", content)
        self.assertIn("fingerprint", content)
        self.assertIn("sql", content)
        self.assertIn("high-confidence", content)
        self.assertIn("contested", content)
        self.assertIn("debunked", content)


if __name__ == "__main__":
    unittest.main()
