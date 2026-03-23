import unittest
from pathlib import Path


class TestSkillLayoutContract(unittest.TestCase):
    def test_all_skills_use_flat_folder_contract(self):
        repo_root = Path(__file__).resolve().parents[3]
        skills_dir = repo_root / "skills"
        markdown_paths = sorted(skills_dir.rglob("*.md"))

        self.assertGreater(len(markdown_paths), 0)

        invalid_paths = []
        for path in markdown_paths:
            rel = path.relative_to(skills_dir)
            if len(rel.parts) != 2 or rel.name != "SKILL.md":
                invalid_paths.append(rel.as_posix())

        self.assertEqual(invalid_paths, [])

    def test_language_skills_follow_lang_prefix_naming_convention(self):
        repo_root = Path(__file__).resolve().parents[3]
        skills_dir = repo_root / "skills"
        language_skills = {
            "cpp",
            "csharp",
            "go",
            "java",
            "kotlin",
            "php",
            "python",
            "ruby",
            "rust",
            "swift",
            "typescript",
        }

        for language in sorted(language_skills):
            with self.subTest(language=language):
                self.assertTrue((skills_dir / f"lang-{language}" / "SKILL.md").exists())
                self.assertFalse((skills_dir / language / "SKILL.md").exists())

    def test_tool_skills_live_under_skills_tools(self):
        repo_root = Path(__file__).resolve().parents[3]
        skill_tools = {
            "benchmark-runner",
            "local-calibration",
            "skill-creator",
            "skill-optimizer",
        }

        for skill in sorted(skill_tools):
            with self.subTest(skill=skill):
                self.assertTrue((repo_root / "skills-tools" / skill / "SKILL.md").exists())
                self.assertFalse((repo_root / "skills" / skill / "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
