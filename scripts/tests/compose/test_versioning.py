import unittest

from compose.versioning import apply_refs


class TestComposeVersioning(unittest.TestCase):
    def test_apply_refs_uses_default_tag_strategy(self):
        deps = [
            "richgo/auto-reviewer/skills/core/review-orchestrator",
            "richgo/auto-reviewer/skills/languages/python",
        ]
        resolved = apply_refs(deps, strategy="tag", ref_value="v1.0.0")
        self.assertEqual(
            resolved,
            [
                "richgo/auto-reviewer/skills/core/review-orchestrator#v1.0.0",
                "richgo/auto-reviewer/skills/languages/python#v1.0.0",
            ],
        )

    def test_apply_refs_supports_none_strategy_without_suffix(self):
        deps = ["richgo/auto-reviewer/skills/core/review-orchestrator"]
        resolved = apply_refs(deps, strategy="none", ref_value=None)
        self.assertEqual(resolved, deps)

    def test_apply_refs_rejects_unknown_strategy(self):
        with self.assertRaises(ValueError):
            apply_refs(
                ["richgo/auto-reviewer/skills/core/review-orchestrator"],
                strategy="invalid",
                ref_value="v1.0.0",
            )


if __name__ == "__main__":
    unittest.main()
