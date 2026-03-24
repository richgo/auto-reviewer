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

    def test_creating_skills_doc_includes_transition_guidance_for_legacy_entrypoints(self):
        doc_path = (
            Path(__file__).resolve().parents[3]
            / "skills-tools"
            / "creating-skills.md"
        )
        text = doc_path.read_text(encoding="utf-8")

        self.assertIn("Transition guidance", text)
        self.assertIn("scripts/skill_machine/pipeline.py", text)
        self.assertIn("legacy entrypoints", text)
        self.assertIn("supported as internal building blocks", text)


if __name__ == "__main__":
    unittest.main()
