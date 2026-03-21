import json
from typing import Dict


class AssertionJudge:
    def __init__(self, llm_client, model: str = "gpt-4.1"):
        self.llm_client = llm_client
        self.model = model

    def evaluate(
        self,
        *,
        code_snippet: str,
        review_output: str,
        assertion_name: str,
        criteria: str,
    ) -> Dict[str, str]:
        prompt = (
            f"Code:\n{code_snippet}\n\n"
            f"Review:\n{review_output}\n\n"
            f"Assertion: {assertion_name}\n"
            f"Criteria: {criteria}\n"
            "Respond with exactly 'pass: <one-line justification>' or "
            "'fail: <one-line justification>'."
        )
        response = self.llm_client.complete(prompt, model=self.model, temperature=0.0).strip()
        parsed = self._parse_response(response)
        if parsed:
            parsed["model"] = self.model
            return parsed
        normalized = "fail"
        justification = "ambiguous judge response"
        return {
            "status": normalized,
            "justification": justification,
            "model": self.model,
        }

    def _parse_response(self, response: str):
        if response.startswith("{"):
            parsed = json.loads(response)
            status = str(parsed.get("status", "")).strip().lower()
            justification = str(parsed.get("justification", "")).strip()
            if status in {"pass", "fail"} and justification:
                return {
                    "status": status,
                    "justification": justification,
                }
            return None
        status, _, justification = response.partition(":")
        normalized = status.strip().lower()
        if normalized not in {"pass", "fail"}:
            return None
        return {
            "status": normalized,
            "justification": justification.strip(),
        }
