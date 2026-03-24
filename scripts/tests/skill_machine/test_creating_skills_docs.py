import unittest
from pathlib import Path


class TestCreatingSkillsDocs(unittest.TestCase):
    def test_creating_skills_doc_references_pipeline_entrypoint_and_stages(self):
        doc_path = (
            Path(__file__).resolve().parents[3]
            / "skills-tools"
            / "creating-skills.md"
        )
        text = doc_path.read_text(encoding="utf-8")

        self.assertIn("scripts/skill_machine/pipeline.py", text)
        self.assertIn("`create`", text)
        self.assertIn("`tune`", text)
        self.assertIn("unified lifecycle", text)


if __name__ == "__main__":
    unittest.main()
