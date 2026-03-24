import unittest
from pathlib import Path


class TestLocalCalibrationDocs(unittest.TestCase):
    def test_creating_skills_documents_local_calibration_as_separate_from_create_tune(self):
        doc_path = (
            Path(__file__).resolve().parents[3]
            / "skills-tools"
            / "creating-skills.md"
        )
        text = doc_path.read_text(encoding="utf-8")

        self.assertIn("local-calibration", text)
        self.assertIn("separate", text)
        self.assertIn("outside canonical create/tune promotion flow", text)


if __name__ == "__main__":
    unittest.main()
