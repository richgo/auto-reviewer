import tempfile
import unittest
from pathlib import Path

import yaml

from compose.validator import validate_manifest


class TestComposeValidator(unittest.TestCase):
    def test_validate_manifest_rejects_unknown_auto_reviewer_dependency(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            manifest = {
                "name": "repo",
                "dependencies": {
                    "apm": [
                        "richgo/auto-reviewer/skills/core/review-orchestrator#v1.0.0",
                        "richgo/auto-reviewer/skills/languages/not-a-real-skill#v1.0.0",
                    ]
                },
            }
            errors = validate_manifest(manifest, repo_root=root)
        self.assertTrue(any("not-a-real-skill" in error for error in errors))

    def test_validate_manifest_rejects_invalid_ref_format(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "skills" / "core").mkdir(parents=True)
            (root / "skills" / "core" / "review-orchestrator.md").write_text("skill", encoding="utf-8")
            manifest = {
                "name": "repo",
                "dependencies": {
                    "apm": [
                        "richgo/auto-reviewer/skills/core/review-orchestrator#",
                    ]
                },
            }
            errors = validate_manifest(manifest, repo_root=root)
        self.assertTrue(any("Invalid ref" in error for error in errors))

    def test_validate_manifest_rejects_missing_name_field(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            manifest = {"dependencies": {"apm": []}}
            errors = validate_manifest(manifest, repo_root=root)
        self.assertTrue(any("name" in error.lower() for error in errors))

    def test_validate_manifest_rejects_non_list_dependencies_shape(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            manifest = {
                "name": "repo",
                "dependencies": {"apm": "richgo/auto-reviewer/skills/core/review-orchestrator#v1.0.0"},
            }
            errors = validate_manifest(manifest, repo_root=root)

        self.assertTrue(any("must be a list" in error for error in errors))

    def test_validate_manifest_rejects_non_string_dependency_entries(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            manifest = {
                "name": "repo",
                "dependencies": {
                    "apm": [
                        123,
                    ]
                },
            }
            errors = validate_manifest(manifest, repo_root=root)

        self.assertTrue(any("must be a string" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
