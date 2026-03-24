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
                            "richgo/skill-machine/skills/review-orchestrator",
                            "richgo/skill-machine/skills/diff-analysis",
                        ],
                        "fallback": ["richgo/skill-machine/skills/correctness"],
                        "signals": {
                            "python": {
                                "dependencies": [
                                    "richgo/skill-machine/skills/lang-python",
                                    "richgo/skill-machine/skills/review-orchestrator",
                                ]
                            },
                            "ci_github_actions": {
                                "dependencies": [
                                    "richgo/skill-machine/skills/inline-comments"
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
                "richgo/skill-machine/skills/diff-analysis",
                "richgo/skill-machine/skills/inline-comments",
                "richgo/skill-machine/skills/lang-python",
                "richgo/skill-machine/skills/review-orchestrator",
            ],
        )

    def test_select_dependencies_uses_fallback_when_no_signals_detected(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            policy_path = Path(tmp_dir) / "policy.yaml"
            policy_path.write_text(
                yaml.safe_dump(
                    {
                        "core": [
                            "richgo/skill-machine/skills/review-orchestrator",
                        ],
                        "fallback": [
                            "richgo/skill-machine/skills/correctness",
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
                "richgo/skill-machine/skills/correctness",
                "richgo/skill-machine/skills/review-orchestrator",
            ],
        )

    def test_select_dependencies_is_stable_across_repeated_calls(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            policy_path = Path(tmp_dir) / "policy.yaml"
            policy_path.write_text(
                yaml.safe_dump(
                    {
                        "core": [
                            "richgo/skill-machine/skills/review-orchestrator",
                        ],
                        "fallback": [],
                        "signals": {
                            "python": {
                                "dependencies": [
                                    "richgo/skill-machine/skills/lang-python",
                                ]
                            },
                            "ci_github_actions": {
                                "dependencies": [
                                    "richgo/skill-machine/skills/inline-comments",
                                ]
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )

            first = select_dependencies(
                policy_path=policy_path,
                detected_signals={"python", "ci_github_actions"},
            )
            second = select_dependencies(
                policy_path=policy_path,
                detected_signals={"ci_github_actions", "python"},
            )

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
