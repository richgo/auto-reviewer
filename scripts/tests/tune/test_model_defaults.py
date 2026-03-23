import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tune.llm_client import LLMClient
from tune.mutator import Mutator
from tune.scorer import Scorer


class TestTuneModelDefaults(unittest.TestCase):
    def test_llm_client_defaults_to_configured_model(self):
        client = LLMClient()
        self.assertIsNone(client.model)

    def test_scorer_defaults_to_configured_model(self):
        scorer = Scorer()
        self.assertIsNone(scorer.llm.model)

    def test_mutator_defaults_to_configured_model(self):
        mutator = Mutator()
        self.assertIsNone(mutator.llm.model)


if __name__ == "__main__":
    unittest.main()
