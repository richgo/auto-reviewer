"""
Binary assertion scorer for code review evaluation.
Judges whether a review output satisfies specific assertions using LLM.
"""

import json
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from .llm_client import LLMClient


@dataclass
class AssertionResult:
    """Result of evaluating a single assertion."""
    name: str
    passed: bool
    reason: str


@dataclass
class EvalScore:
    """Overall evaluation score for a review."""
    total_assertions: int
    passed_assertions: int
    failed_assertions: int
    pass_rate: float
    assertion_results: List[AssertionResult]


class Scorer:
    """
    Binary assertion scorer that evaluates review quality using LLM.
    
    Assertion types:
    - detected_bug: Did the review catch the vulnerability/issue?
    - no_false_positive: Is the finding legitimate (not a false alarm)?
    - actionable_fix: Does the review suggest a concrete fix?
    - correct_severity: Is the severity rating appropriate?
    - evidence_cited: Does the review cite code evidence?
    """
    
    ASSERTION_TYPES = {
        "detected_bug": "The review must identify the specific bug or vulnerability present in the code.",
        "no_false_positive": "The review must not flag code that is actually safe/correct.",
        "actionable_fix": "The review must suggest a specific, implementable fix or remediation.",
        "correct_severity": "The review must assign an appropriate severity level for the issue.",
        "evidence_cited": "The review must cite specific code lines or patterns as evidence."
    }
    
    def __init__(self, model: Optional[str] = None):
        """
        Initialize scorer.
        
        Args:
            model: Optional LLM model to use for assertion evaluation
        """
        self.llm = LLMClient(model)
    
    def score_review(
        self,
        review_output: str,
        eval_case: Dict[str, Any]
    ) -> EvalScore:
        """
        Score a review against eval case assertions.
        
        Args:
            review_output: The review text produced by the skill
            eval_case: Eval case dict with code_snippet, expected_findings, assertions
            
        Returns:
            EvalScore with pass/fail results for each assertion
        """
        assertions = eval_case.get("assertions", {})
        results: List[AssertionResult] = []
        
        for assertion_name, expected_value in assertions.items():
            if assertion_name in self.ASSERTION_TYPES:
                passed, reason = self._evaluate_assertion(
                    assertion_name,
                    expected_value,
                    review_output,
                    eval_case
                )
                results.append(AssertionResult(
                    name=assertion_name,
                    passed=passed,
                    reason=reason
                ))
        
        passed_count = sum(1 for r in results if r.passed)
        failed_count = len(results) - passed_count
        pass_rate = passed_count / len(results) if results else 0.0
        
        return EvalScore(
            total_assertions=len(results),
            passed_assertions=passed_count,
            failed_assertions=failed_count,
            pass_rate=pass_rate,
            assertion_results=results
        )
    
    def _evaluate_assertion(
        self,
        assertion_name: str,
        expected_value: Any,
        review_output: str,
        eval_case: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """
        Evaluate a single assertion using LLM.
        
        Args:
            assertion_name: Type of assertion (e.g., "detected_bug")
            expected_value: Expected value (usually True for binary assertions)
            review_output: The review text
            eval_case: Full eval case for context
            
        Returns:
            (passed, reason) tuple
        """
        assertion_description = self.ASSERTION_TYPES[assertion_name]
        
        prompt = f"""You are evaluating the quality of a code review.

**Assertion to check:** {assertion_name}
**Definition:** {assertion_description}
**Expected:** {expected_value}

**Code being reviewed:**
```{eval_case.get('language', 'python')}
{eval_case.get('code_snippet', eval_case.get('prompt', ''))}
```

**Expected findings:**
{json.dumps(eval_case.get('expected_findings', []), indent=2)}

**Actual review output:**
{review_output}

Does the review satisfy the assertion "{assertion_name}"?

Respond with JSON:
{{
  "passed": true/false,
  "reason": "Brief explanation of why it passed or failed"
}}
"""
        
        try:
            response = self.llm.complete(prompt, temperature=0.1)
            # Extract JSON from response (handle markdown code blocks)
            response = response.strip()
            if response.startswith("```"):
                lines = response.split("\n")
                response = "\n".join(lines[1:-1])
            
            result = json.loads(response)
            return result["passed"], result["reason"]
        
        except Exception as e:
            return False, f"Scoring error: {str(e)}"
    
    def format_score_report(self, score: EvalScore) -> str:
        """
        Format score as human-readable report.
        
        Args:
            score: EvalScore to format
            
        Returns:
            Formatted report string
        """
        lines = [
            f"Pass Rate: {score.pass_rate:.1%} ({score.passed_assertions}/{score.total_assertions})",
            "",
            "Assertion Results:"
        ]
        
        for result in score.assertion_results:
            status = "✓" if result.passed else "✗"
            lines.append(f"  {status} {result.name}: {result.reason}")
        
        return "\n".join(lines)
