import tempfile
import unittest
from pathlib import Path

import yaml

from compose.selector import select_dependencies


class TestComposeSelector(unittest.TestCase):
    def test_select_dependencies_includes_core_and_sorts_deduped_results(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            policy_path = Path(tmp_dir) / "policy.yaml"
            policy_path.write_text(
                yaml.safe_dump(
                    {
                        "core": [
                            "richgo/auto-reviewer/skills/core/review-orchestrator",
                            "richgo/auto-reviewer/skills/core/diff-analysis",
                        ],
                        "fallback": ["richgo/auto-reviewer/skills/concerns/correctness"],
                        "signals": {
                            "python": {
                                "dependencies": [
                                    "richgo/auto-reviewer/skills/languages/python",
                                    "richgo/auto-reviewer/skills/core/review-orchestrator",
                                ]
                            },
                            "ci_github_actions": {
                                "dependencies": [
                                    "richgo/auto-reviewer/skills/outputs/inline-comments"
                                ]
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )

            selected = select_dependencies(
                policy_path=policy_path,
                detected_signals={"ci_github_actions", "python"},
            )

        self.assertEqual(
            selected,
            [
                "richgo/auto-reviewer/skills/core/diff-analysis",
                "richgo/auto-reviewer/skills/core/review-orchestrator",
                "richgo/auto-reviewer/skills/languages/python",
                "richgo/auto-reviewer/skills/outputs/inline-comments",
            ],
        )

    def test_select_dependencies_uses_fallback_when_no_signals_detected(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            policy_path = Path(tmp_dir) / "policy.yaml"
            policy_path.write_text(
                yaml.safe_dump(
                    {
                        "core": [
                            "richgo/auto-reviewer/skills/core/review-orchestrator",
                        ],
                        "fallback": [
                            "richgo/auto-reviewer/skills/concerns/correctness",
                        ],
                        "signals": {},
                    }
                ),
                encoding="utf-8",
            )
            selected = select_dependencies(
                policy_path=policy_path,
                detected_signals=set(),
            )

        self.assertEqual(
            selected,
            [
                "richgo/auto-reviewer/skills/concerns/correctness",
                "richgo/auto-reviewer/skills/core/review-orchestrator",
            ],
        )


if __name__ == "__main__":
    unittest.main()
