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
            (repo / "skills" / "core" / "review-orchestrator").mkdir()
            (repo / "skills" / "core" / "diff-analysis").mkdir()
            (repo / "skills" / "languages" / "python").mkdir()
            (repo / "skills" / "languages" / "typescript").mkdir()
            (repo / "skills" / "outputs" / "inline-comments").mkdir()
            (repo / "skills" / "core" / "review-orchestrator" / "SKILL.md").write_text("skill", encoding="utf-8")
            (repo / "skills" / "core" / "diff-analysis" / "SKILL.md").write_text("skill", encoding="utf-8")
            (repo / "skills" / "languages" / "python" / "SKILL.md").write_text("skill", encoding="utf-8")
            (repo / "skills" / "languages" / "typescript" / "SKILL.md").write_text("skill", encoding="utf-8")
            (repo / "skills" / "outputs" / "inline-comments" / "SKILL.md").write_text("skill", encoding="utf-8")

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

    def test_compose_manifest_update_preserves_non_managed_and_applies_fallback(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Path(tmp_dir) / "repo"
            repo.mkdir()
            (repo / "skills" / "core").mkdir(parents=True)
            (repo / "skills" / "concerns").mkdir(parents=True)
            (repo / "skills" / "core" / "review-orchestrator").mkdir()
            (repo / "skills" / "concerns" / "correctness").mkdir()
            (repo / "skills" / "core" / "review-orchestrator" / "SKILL.md").write_text("skill", encoding="utf-8")
            (repo / "skills" / "concerns" / "correctness" / "SKILL.md").write_text("skill", encoding="utf-8")

            policy = repo / "policy.yaml"
            policy.write_text(
                yaml.safe_dump(
                    {
                        "core": ["richgo/auto-reviewer/skills/core/review-orchestrator"],
                        "fallback": ["richgo/auto-reviewer/skills/concerns/correctness"],
                        "signals": {},
                    }
                ),
                encoding="utf-8",
            )
            apm = repo / "apm.yml"
            apm.write_text(
                yaml.safe_dump(
                    {
                        "name": "repo-review",
                        "dependencies": {"apm": ["external-org/custom-skill#v2"]},
                        "config": {"severity_threshold": "high"},
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )

            result = compose_manifest(
                repo_root=repo,
                policy_path=policy,
                output_path=apm,
                ref_strategy="none",
                ref_value=None,
                update=True,
            )

            written = yaml.safe_load(apm.read_text(encoding="utf-8"))

        self.assertEqual(result["composer"]["detection_confidence"], "low")
        self.assertIn("external-org/custom-skill#v2", written["dependencies"]["apm"])
        self.assertIn("richgo/auto-reviewer/skills/core/review-orchestrator", written["dependencies"]["apm"])
        self.assertIn("richgo/auto-reviewer/skills/concerns/correctness", written["dependencies"]["apm"])
        self.assertEqual(written["config"]["severity_threshold"], "high")

    def test_compose_manifest_default_tag_is_stable_and_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Path(tmp_dir) / "repo"
            repo.mkdir()
            (repo / "requirements.txt").write_text("pyyaml", encoding="utf-8")
            (repo / "skills" / "core").mkdir(parents=True)
            (repo / "skills" / "languages").mkdir(parents=True)
            (repo / "skills" / "core" / "review-orchestrator").mkdir()
            (repo / "skills" / "languages" / "python").mkdir()
            (repo / "skills" / "core" / "review-orchestrator" / "SKILL.md").write_text("skill", encoding="utf-8")
            (repo / "skills" / "languages" / "python" / "SKILL.md").write_text("skill", encoding="utf-8")
            policy = repo / "policy.yaml"
            policy.write_text(
                yaml.safe_dump(
                    {
                        "core": ["richgo/auto-reviewer/skills/core/review-orchestrator"],
                        "fallback": [],
                        "signals": {"python": {"dependencies": ["richgo/auto-reviewer/skills/languages/python"]}},
                    }
                ),
                encoding="utf-8",
            )
            output = repo / "apm.yml"

            first = compose_manifest(repo_root=repo, policy_path=policy, output_path=output)
            second = compose_manifest(repo_root=repo, policy_path=policy, output_path=output)

        self.assertEqual(first["dependencies"]["apm"], second["dependencies"]["apm"])
        self.assertTrue(all(dep.endswith("#v1.0.0") for dep in first["dependencies"]["apm"]))


if __name__ == "__main__":
    unittest.main()
