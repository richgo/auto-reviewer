import tempfile
import unittest
from pathlib import Path

import yaml

from compose.merge import merge_managed_dependencies


class TestComposeMerge(unittest.TestCase):
    def test_merge_managed_dependencies_preserves_non_managed_sections(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            manifest_path = Path(tmp_dir) / "apm.yml"
            manifest_path.write_text(
                yaml.safe_dump(
                    {
                        "name": "repo",
                        "dependencies": {
                            "apm": [
                                "other-org/other-package#v2",
                                "richgo/skill-machine/skills/review-orchestrator#v0.9.0",
                            ]
                        },
                        "config": {"severity_threshold": "high"},
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )
            merged = merge_managed_dependencies(
                manifest_path=manifest_path,
                managed_dependencies=[
                    "richgo/skill-machine/skills/review-orchestrator#v1.0.0",
                    "richgo/skill-machine/skills/diff-analysis#v1.0.0",
                ],
            )

        self.assertIn("other-org/other-package#v2", merged["dependencies"]["apm"])
        self.assertIn("richgo/skill-machine/skills/diff-analysis#v1.0.0", merged["dependencies"]["apm"])
        self.assertEqual(merged["config"]["severity_threshold"], "high")

    def test_merge_managed_dependencies_creates_manifest_dependencies_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            manifest_path = Path(tmp_dir) / "apm.yml"
            manifest_path.write_text(yaml.safe_dump({"name": "repo"}), encoding="utf-8")
            merged = merge_managed_dependencies(
                manifest_path=manifest_path,
                managed_dependencies=[
                    "richgo/skill-machine/skills/review-orchestrator#v1.0.0",
                ],
            )
        self.assertEqual(
            merged["dependencies"]["apm"],
            ["richgo/skill-machine/skills/review-orchestrator#v1.0.0"],
        )


if __name__ == "__main__":
    unittest.main()
