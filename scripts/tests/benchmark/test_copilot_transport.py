import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from benchmark.copilot_client import CopilotTransport
from llm.transport import CompletionRequest


class TestCopilotTransport(unittest.TestCase):
    def test_complete_returns_provider_neutral_response(self):
        captured = {}

        class FakeCopilotClient:
            def complete(self, **kwargs):
                captured.update(kwargs)
                return "copilot-output"

        transport = CopilotTransport(client=FakeCopilotClient())
        response = transport.complete(
            CompletionRequest(
                prompt="find bug",
                system="sys",
                model="gpt-5-mini",
                max_tokens=42,
                temperature=0.3,
            )
        )

        self.assertEqual("find bug", captured["prompt"])
        self.assertEqual("sys", captured["system"])
        self.assertEqual("gpt-5-mini", captured["model"])
        self.assertEqual(42, captured["max_tokens"])
        self.assertEqual(0.3, captured["temperature"])
        self.assertEqual("copilot-output", response.text)
        self.assertEqual("copilot", response.provider)


if __name__ == "__main__":
    unittest.main()
