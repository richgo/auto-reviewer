import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from llm.transport import CompletionRequest, CompletionResponse
from skill_machine.llm_client import LLMClient, _CopilotTransport


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

    def test_llm_client_routes_complete_through_transport_contract(self):
        captured = {}

        class FakeTransport:
            def complete(self, request):
                captured["request"] = request
                return CompletionResponse(
                    text="transport-result",
                    model=request.model,
                    provider="fake",
                    usage={},
                    raw=None,
                )

        client = LLMClient(model="gpt-5-mini", transport=FakeTransport())
        result = client.complete("hello", system="sys", max_tokens=77, temperature=0.1)

        self.assertEqual("transport-result", result)
        self.assertIsInstance(captured["request"], CompletionRequest)
        self.assertEqual("hello", captured["request"].prompt)
        self.assertEqual("sys", captured["request"].system)
        self.assertEqual("gpt-5-mini", captured["request"].model)
        self.assertEqual(77, captured["request"].max_tokens)
        self.assertEqual(0.1, captured["request"].temperature)

    def test_llm_client_forwards_response_format_to_transport_request(self):
        captured = {}

        class FakeTransport:
            def complete(self, request):
                captured["request"] = request
                return CompletionResponse(
                    text="ok",
                    model=request.model,
                    provider="fake",
                    usage={},
                    raw=None,
                )

        client = LLMClient(model="gpt-5-mini", transport=FakeTransport())
        client.complete("hello", response_format="json")

        self.assertEqual("json", captured["request"].response_format)

    def test_copilot_transport_maps_prompt_and_model_from_request(self):
        captured = {}

        class FakeCopilot:
            def complete(self, **kwargs):
                captured.update(kwargs)
                return "copilot-result"

        transport = _CopilotTransport(timeout=30)
        transport._copilot = FakeCopilot()
        response = transport.complete(
            CompletionRequest(
                prompt="check me",
                system="sys",
                model="gpt-5-mini",
                max_tokens=12,
                temperature=0.4,
            )
        )

        self.assertEqual("check me", captured["prompt"])
        self.assertEqual("sys", captured["system"])
        self.assertEqual("gpt-5-mini", captured["model"])
        self.assertEqual(12, captured["max_tokens"])
        self.assertEqual(0.4, captured["temperature"])
        self.assertEqual("copilot-result", response.text)
        self.assertEqual("copilot", response.provider)


if __name__ == "__main__":
    unittest.main()
