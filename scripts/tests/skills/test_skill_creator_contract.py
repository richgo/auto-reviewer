import unittest
from pathlib import Path


class TestSkillCreatorContract(unittest.TestCase):
    @staticmethod
    def _skill_root() -> Path:
        repo_root = Path(__file__).resolve().parents[3]
        return repo_root / "skills" / "skill-creator"

    def test_skill_creator_exists_with_required_frontmatter_and_copilot_sdk_guidance(self):
        skill_path = self._skill_root() / "SKILL.md"

        self.assertTrue(
            skill_path.exists(),
            "skills/skill-creator/SKILL.md must exist.",
        )

        content = skill_path.read_text(encoding="utf-8")
        self.assertIn("name: skill-creator", content)
        self.assertIn("description:", content)
        self.assertIn("Copilot SDK", content)
        self.assertIn("GITHUB_TOKEN", content)

    def test_skill_creator_includes_upstream_license_file(self):
        license_path = self._skill_root() / "LICENSE.txt"

        self.assertTrue(
            license_path.exists(),
            "skills/skill-creator/LICENSE.txt must exist when importing from upstream.",
        )

        license_text = license_path.read_text(encoding="utf-8")
        self.assertIn("Apache License", license_text)


if __name__ == "__main__":
    unittest.main()
