import unittest
from pathlib import Path


class TestComposerAgentEntry(unittest.TestCase):
    def test_composer_agent_entry_defines_compose_commands(self):
        repo_root = Path(__file__).resolve().parents[3]
        agent_path = repo_root / "agents" / "composer" / "agent.md"

        self.assertTrue(agent_path.exists())

        content = agent_path.read_text(encoding="utf-8")
        self.assertIn("compose", content)
        self.assertIn("compose-update", content)
        self.assertIn("apm.yml", content)
        self.assertIn("policy", content.lower())


if __name__ == "__main__":
    unittest.main()
