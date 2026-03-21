import tempfile
import unittest
from pathlib import Path

import yaml

from compose.composer import compose_manifest


class TestComposer(unittest.TestCase):
    def test_compose_manifest_runs_pipeline_and_sets_distributed_for_multi_runtime(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Path(tmp_dir) / "repo"
            repo.mkdir()
            (repo / "requirements.txt").write_text("pyyaml", encoding="utf-8")
            (repo / "app.py").write_text("print('x')", encoding="utf-8")
            (repo / "package.json").write_text('{"name":"web"}', encoding="utf-8")
            (repo / "ui.ts").write_text("export const x = 1;", encoding="utf-8")
            (repo / "skills" / "core").mkdir(parents=True)
            (repo / "skills" / "languages").mkdir(parents=True)
            (repo / "skills" / "outputs").mkdir(parents=True)
            (repo / "skills" / "core" / "review-orchestrator.md").write_text("skill", encoding="utf-8")
            (repo / "skills" / "core" / "diff-analysis.md").write_text("skill", encoding="utf-8")
            (repo / "skills" / "languages" / "python.md").write_text("skill", encoding="utf-8")
            (repo / "skills" / "languages" / "typescript.md").write_text("skill", encoding="utf-8")
            (repo / "skills" / "outputs" / "inline-comments.md").write_text("skill", encoding="utf-8")

            policy = repo / "policy.yaml"
            policy.write_text(
                yaml.safe_dump(
                    {
                        "core": [
                            "richgo/auto-reviewer/skills/core/review-orchestrator",
                            "richgo/auto-reviewer/skills/core/diff-analysis",
                        ],
                        "fallback": [],
                        "signals": {
                            "python": {"dependencies": ["richgo/auto-reviewer/skills/languages/python"]},
                            "typescript": {"dependencies": ["richgo/auto-reviewer/skills/languages/typescript"]},
                            "ci_github_actions": {"dependencies": ["richgo/auto-reviewer/skills/outputs/inline-comments"]},
                        },
                    }
                ),
                encoding="utf-8",
            )

            result = compose_manifest(
                repo_root=repo,
                policy_path=policy,
                output_path=repo / "apm.yml",
                ref_strategy="tag",
                ref_value="v1.0.0",
            )

        self.assertIn("dependencies", result)
        self.assertEqual(result["compilation"]["strategy"], "distributed")
        self.assertIn(
            "richgo/auto-reviewer/skills/languages/python#v1.0.0",
            result["dependencies"]["apm"],
        )


if __name__ == "__main__":
    unittest.main()
