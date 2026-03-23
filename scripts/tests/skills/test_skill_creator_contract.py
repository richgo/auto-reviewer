import unittest
from pathlib import Path
import re


class TestSkillCreatorContract(unittest.TestCase):
    EXPECTED_PYTHON_APP_FILES = [
        "eval-viewer/generate_review.py",
        "scripts/__init__.py",
        "scripts/aggregate_benchmark.py",
        "scripts/copilot_sdk.py",
        "scripts/generate_report.py",
        "scripts/improve_description.py",
        "scripts/package_skill.py",
        "scripts/quick_validate.py",
        "scripts/run_eval.py",
        "scripts/run_loop.py",
        "scripts/utils.py",
    ]

    @staticmethod
    def _skill_root() -> Path:
        repo_root = Path(__file__).resolve().parents[3]
        return repo_root / "skills-tools" / "skill-creator"

    def _assert_skill_file_exists(self, relative_path: str, *, message: str) -> None:
        self.assertTrue(
            (self._skill_root() / relative_path).exists(),
            message,
        )

    def test_skill_creator_exists_with_required_frontmatter_and_copilot_sdk_guidance(self):
        skill_path = self._skill_root() / "SKILL.md"
        self._assert_skill_file_exists(
            "SKILL.md",
            message="skills-tools/skill-creator/SKILL.md must exist.",
        )

        content = skill_path.read_text(encoding="utf-8")
        self.assertIn("name: skill-creator", content)
        self.assertIn("description:", content)
        self.assertIn("Copilot SDK", content)
        self.assertIn("GITHUB_TOKEN", content)

    def test_skill_creator_includes_upstream_license_file(self):
        license_path = self._skill_root() / "LICENSE.txt"
        self._assert_skill_file_exists(
            "LICENSE.txt",
            message="skills-tools/skill-creator/LICENSE.txt must exist when importing from upstream.",
        )

        license_text = license_path.read_text(encoding="utf-8")
        self.assertIn("Apache License", license_text)

    def test_skill_creator_includes_upstream_python_app_files(self):
        missing_files = []
        for relative_path in self.EXPECTED_PYTHON_APP_FILES:
            if not (self._skill_root() / relative_path).exists():
                missing_files.append(relative_path)

        self.assertEqual(
            missing_files,
            [],
            "All upstream skill-creator Python app files should be copied locally.",
        )

    def test_skill_creator_python_app_removes_claude_references_and_uses_copilot_sdk(self):
        python_files = sorted(self._skill_root().rglob("*.py"))
        forbidden_pattern = re.compile(r"claude|\.claude", re.IGNORECASE)
        offenders = []
        copilot_mentions = 0

        for path in python_files:
            text = path.read_text(encoding="utf-8")
            if forbidden_pattern.search(text):
                offenders.append(str(path.relative_to(self._skill_root())))
            if re.search(r"copilot|github_token|github token", text, re.IGNORECASE):
                copilot_mentions += 1

        self.assertEqual(
            offenders,
            [],
            "Skill-creator Python app should not contain Claude-specific references.",
        )
        self.assertGreater(
            copilot_mentions,
            0,
            "Skill-creator Python app should include Copilot SDK runtime references.",
        )


if __name__ == "__main__":
    unittest.main()
