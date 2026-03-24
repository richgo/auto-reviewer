import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from llm.transport import CompletionRequest, CompletionResponse


class TestLLMTransportTypes(unittest.TestCase):
    def test_completion_request_and_response_capture_provider_neutral_fields(self):
        request = CompletionRequest(
            prompt="review this code",
            system="system prompt",
            model="gpt-5-mini",
            max_tokens=512,
            temperature=0.2,
            response_format="text",
        )
        response = CompletionResponse(
            text="looks good",
            model="gpt-5-mini",
            provider="copilot",
            usage={"input_tokens": 10, "output_tokens": 20},
            raw={"event_id": "evt_123"},
        )

        self.assertEqual("review this code", request.prompt)
        self.assertEqual("gpt-5-mini", request.model)
        self.assertEqual("looks good", response.text)
        self.assertEqual("copilot", response.provider)


if __name__ == "__main__":
    unittest.main()
