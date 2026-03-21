import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from benchmark.judge import AssertionJudge


class _FakeLLM:
    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = []

    def complete(self, prompt, model, temperature=0.0):
        self.calls.append({"prompt": prompt, "model": model, "temperature": temperature})
        return self._responses.pop(0)


class TestAssertionJudge(unittest.TestCase):
    def test_evaluate_returns_pass_when_judge_response_is_pass(self):
        llm = _FakeLLM(["pass: clear evidence in lines 2-3"])
        judge = AssertionJudge(llm_client=llm)

        result = judge.evaluate(
            code_snippet="query = f\"SELECT ... {username}\"",
            review_output="SQL injection risk from string interpolation on line 1.",
            assertion_name="detected_bug",
            criteria="Bug is explicitly identified.",
        )

        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["justification"], "clear evidence in lines 2-3")
        self.assertEqual(result["model"], "gpt-4.1")

    def test_evaluate_parses_json_status_response(self):
        llm = _FakeLLM(['{"status":"fail","justification":"missing concrete fix"}'])
        judge = AssertionJudge(llm_client=llm, model="custom-judge")

        result = judge.evaluate(
            code_snippet="do_not_escape(query)",
            review_output="Potential issue but no fix details.",
            assertion_name="actionable_fix",
            criteria="Review includes a concrete fix.",
        )

        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["justification"], "missing concrete fix")
        self.assertEqual(result["model"], "custom-judge")


if __name__ == "__main__":
    unittest.main()
