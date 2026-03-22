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

    def test_composer_agent_entry_declares_skill_group_contract(self):
        repo_root = Path(__file__).resolve().parents[3]
        agent_path = repo_root / "agents" / "composer" / "agent.md"
        content = agent_path.read_text(encoding="utf-8").lower()

        self.assertIn("skills", content)
        self.assertIn("skill-group", content)
        self.assertIn("delegate", content)
        self.assertNotIn("review tasks", content)
        self.assertNotIn("review-task", content)

    def test_composer_agent_entry_requires_skill_attribution_for_outputs(self):
        repo_root = Path(__file__).resolve().parents[3]
        agent_path = repo_root / "agents" / "composer" / "agent.md"
        content = agent_path.read_text(encoding="utf-8").lower()

        self.assertIn("output", content)
        self.assertIn("attribution", content)
        self.assertIn("skill", content)


if __name__ == "__main__":
    unittest.main()
