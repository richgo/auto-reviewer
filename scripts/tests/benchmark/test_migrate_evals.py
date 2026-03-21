import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from benchmark.migrate_evals import migrate_eval_payload


class TestMigrateEvals(unittest.TestCase):
    def test_migrate_maps_legacy_assertions_to_binary_schema(self):
        payload = {
            "skill": "security-injection",
            "cases": [
                {
                    "id": "legacy-1",
                    "assertions": {
                        "must_detect": True,
                        "severity": "critical",
                        "suggest_parameterized_query": True,
                    },
                }
            ],
        }

        migrated = migrate_eval_payload(payload)

        self.assertEqual(
            migrated["cases"][0]["assertions"],
            {
                "detected_bug": True,
                "correct_severity": True,
                "actionable_fix": True,
                "evidence_cited": True,
            },
        )
        self.assertFalse(migrated["cases"][0]["counter_example"])


if __name__ == "__main__":
    unittest.main()
