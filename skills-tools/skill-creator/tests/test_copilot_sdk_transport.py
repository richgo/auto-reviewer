import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_DIR = REPO_ROOT / "skills-tools" / "skill-creator" / "scripts"
SCRIPTS_ROOT = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPTS_ROOT))

from copilot_sdk import CopilotSDKClient
from llm.transport import CompletionResponse


class TestSkillCreatorCopilotSDKClient(unittest.TestCase):
    def test_complete_routes_through_transport_contract(self):
        captured = {}

        class FakeTransport:
            def complete(self, request):
                captured["request"] = request
                return CompletionResponse(
                    text="from-transport",
                    model=request.model,
                    provider="fake",
                    usage={},
                    raw=None,
                )

        client = CopilotSDKClient(timeout=45, transport=FakeTransport())
        text = client.complete(prompt="hello", model="gpt-5-mini", system="sys")

        self.assertEqual("from-transport", text)
        self.assertEqual("hello", captured["request"].prompt)
        self.assertEqual("sys", captured["request"].system)
        self.assertEqual("gpt-5-mini", captured["request"].model)

    def test_complete_uses_legacy_async_path_when_transport_not_injected(self):
        client = CopilotSDKClient(timeout=45)

        async def fake_complete_async(*, prompt, model, system):
            self.assertEqual("hello", prompt)
            self.assertEqual("gpt-5-mini", model)
            self.assertEqual("sys", system)
            return "legacy-path"

        client._complete_async = fake_complete_async  # type: ignore[method-assign]

        text = client.complete(prompt="hello", model="gpt-5-mini", system="sys")
        self.assertEqual("legacy-path", text)


if __name__ == "__main__":
    unittest.main()
