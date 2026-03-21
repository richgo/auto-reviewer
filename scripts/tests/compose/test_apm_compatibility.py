import tempfile
import unittest
from pathlib import Path

import yaml

from compose.composer import compose_manifest


class TestComposeApmCompatibility(unittest.TestCase):
    def _prepare_repo_with_skills(self, root: Path) -> Path:
        (root / "skills" / "core").mkdir(parents=True)
        (root / "skills" / "languages").mkdir(parents=True)
        (root / "skills" / "outputs").mkdir(parents=True)
        (root / "skills" / "core" / "review-orchestrator.md").write_text("skill", encoding="utf-8")
        (root / "skills" / "core" / "diff-analysis.md").write_text("skill", encoding="utf-8")
        (root / "skills" / "languages" / "python.md").write_text("skill", encoding="utf-8")
        (root / "skills" / "languages" / "typescript.md").write_text("skill", encoding="utf-8")
        (root / "skills" / "outputs" / "inline-comments.md").write_text("skill", encoding="utf-8")
        policy = root / "policy.yaml"
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
        return policy

    def test_generated_dependencies_use_parseable_apm_notation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Path(tmp_dir) / "repo"
            repo.mkdir()
            (repo / "requirements.txt").write_text("pyyaml", encoding="utf-8")
            policy = self._prepare_repo_with_skills(repo)
            output = repo / "apm.yml"

            manifest = compose_manifest(
                repo_root=repo,
                policy_path=policy,
                output_path=output,
                ref_strategy="tag",
                ref_value="v1.0.0",
            )

        for dep in manifest["dependencies"]["apm"]:
            self.assertIn("#", dep)
            dep_path, ref = dep.split("#", 1)
            self.assertTrue(dep_path)
            self.assertTrue(ref)

    def test_multi_runtime_manifest_sets_distributed_compilation_defaults(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Path(tmp_dir) / "repo"
            repo.mkdir()
            (repo / "requirements.txt").write_text("pyyaml", encoding="utf-8")
            (repo / "app.py").write_text("print('x')", encoding="utf-8")
            (repo / "package.json").write_text('{"name":"web"}', encoding="utf-8")
            (repo / "ui.ts").write_text("export const x = 1;", encoding="utf-8")
            policy = self._prepare_repo_with_skills(repo)
            output = repo / "apm.yml"

            manifest = compose_manifest(
                repo_root=repo,
                policy_path=policy,
                output_path=output,
            )

        self.assertEqual(manifest["compilation"]["target"], "all")
        self.assertEqual(manifest["compilation"]["strategy"], "distributed")

    def test_repeated_compose_preserves_dependency_intent(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Path(tmp_dir) / "repo"
            repo.mkdir()
            (repo / "requirements.txt").write_text("pyyaml", encoding="utf-8")
            policy = self._prepare_repo_with_skills(repo)
            output = repo / "apm.yml"

            first = compose_manifest(
                repo_root=repo,
                policy_path=policy,
                output_path=output,
                ref_strategy="tag",
                ref_value="v1.0.0",
            )
            second = compose_manifest(
                repo_root=repo,
                policy_path=policy,
                output_path=output,
                ref_strategy="tag",
                ref_value="v1.0.0",
            )
            persisted = yaml.safe_load(output.read_text(encoding="utf-8"))

        self.assertEqual(first["dependencies"]["apm"], second["dependencies"]["apm"])
        self.assertEqual(first["dependencies"]["apm"], persisted["dependencies"]["apm"])


if __name__ == "__main__":
    unittest.main()
