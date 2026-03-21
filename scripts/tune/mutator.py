"""
Skill mutation strategies for autoresearch tuning.
Analyzes failure patterns and generates skill improvements.
"""

import json
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from .llm_client import LLMClient
from .scorer import EvalScore


@dataclass
class Mutation:
    """A proposed change to a skill."""
    strategy: str
    description: str
    modified_skill: str


class Mutator:
    """
    Generates skill mutations based on failure patterns.
    
    Strategies:
    - add_detection_heuristic: Add new detection pattern for missed bugs
    - add_counter_example: Add false-positive avoidance example
    - refine_instruction: Reword confusing instruction
    - add_platform_guidance: Add platform-specific guidance
    - remove_noise: Remove unhelpful instructions
    """
    
    STRATEGIES = [
        "add_detection_heuristic",
        "add_counter_example",
        "refine_instruction",
        "add_platform_guidance",
        "remove_noise"
    ]
    
    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize mutator.
        
        Args:
            model: LLM model to use for mutation generation
        """
        self.llm = LLMClient(model)
    
    def analyze_failures(
        self,
        scores: List[Tuple[Dict[str, Any], EvalScore]]
    ) -> Dict[str, Any]:
        """
        Analyze failure patterns across multiple eval cases.
        
        Args:
            scores: List of (eval_case, score) tuples
            
        Returns:
            Failure pattern analysis dict
        """
        patterns = {
            "total_cases": len(scores),
            "failed_cases": 0,
            "common_failures": {},
            "false_negatives": [],  # Bugs not detected
            "false_positives": [],  # Safe code flagged as buggy
            "missing_fixes": [],    # No actionable fix suggested
            "severity_errors": [],  # Wrong severity assigned
        }
        
        for eval_case, score in scores:
            if score.pass_rate < 1.0:
                patterns["failed_cases"] += 1
            
            for assertion_result in score.assertion_results:
                if not assertion_result.passed:
                    # Track which assertions fail most
                    assertion_name = assertion_result.name
                    patterns["common_failures"][assertion_name] = \
                        patterns["common_failures"].get(assertion_name, 0) + 1
                    
                    # Categorize failures
                    if assertion_name == "detected_bug":
                        patterns["false_negatives"].append({
                            "case_id": eval_case.get("id"),
                            "code": eval_case.get("code_snippet", eval_case.get("prompt")),
                            "reason": assertion_result.reason
                        })
                    elif assertion_name == "no_false_positive":
                        patterns["false_positives"].append({
                            "case_id": eval_case.get("id"),
                            "reason": assertion_result.reason
                        })
                    elif assertion_name == "actionable_fix":
                        patterns["missing_fixes"].append({
                            "case_id": eval_case.get("id"),
                            "reason": assertion_result.reason
                        })
                    elif assertion_name == "correct_severity":
                        patterns["severity_errors"].append({
                            "case_id": eval_case.get("id"),
                            "reason": assertion_result.reason
                        })
        
        return patterns
    
    def generate_mutation(
        self,
        skill_content: str,
        failure_patterns: Dict[str, Any],
        strategy: str
    ) -> Mutation:
        """
        Generate a skill mutation using specified strategy.
        
        Args:
            skill_content: Current skill markdown content
            failure_patterns: Analysis from analyze_failures()
            strategy: Mutation strategy to apply
            
        Returns:
            Mutation with modified skill content
        """
        if strategy == "add_detection_heuristic":
            return self._add_detection_heuristic(skill_content, failure_patterns)
        elif strategy == "add_counter_example":
            return self._add_counter_example(skill_content, failure_patterns)
        elif strategy == "refine_instruction":
            return self._refine_instruction(skill_content, failure_patterns)
        elif strategy == "add_platform_guidance":
            return self._add_platform_guidance(skill_content, failure_patterns)
        elif strategy == "remove_noise":
            return self._remove_noise(skill_content, failure_patterns)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
    
    def _add_detection_heuristic(
        self,
        skill_content: str,
        patterns: Dict[str, Any]
    ) -> Mutation:
        """Add a new detection heuristic for missed bugs."""
        false_negatives = patterns.get("false_negatives", [])
        
        if not false_negatives:
            return Mutation(
                strategy="add_detection_heuristic",
                description="No false negatives to address",
                modified_skill=skill_content
            )
        
        prompt = f"""You are improving a code review skill that missed detecting bugs.

**Current skill:**
{skill_content}

**Missed bugs (false negatives):**
{json.dumps(false_negatives[:3], indent=2)}

Add a new detection heuristic to the "Detection Strategy" section that would catch these missed bugs.
The heuristic should be specific, pattern-based, and actionable.

Return the FULL modified skill content with the new heuristic added.
"""
        
        try:
            modified = self.llm.complete(prompt, temperature=0.7)
            return Mutation(
                strategy="add_detection_heuristic",
                description=f"Added heuristic to catch {len(false_negatives)} missed bugs",
                modified_skill=modified
            )
        except Exception as e:
            return Mutation(
                strategy="add_detection_heuristic",
                description=f"Failed: {str(e)}",
                modified_skill=skill_content
            )
    
    def _add_counter_example(
        self,
        skill_content: str,
        patterns: Dict[str, Any]
    ) -> Mutation:
        """Add a counter-example to avoid false positives."""
        false_positives = patterns.get("false_positives", [])
        
        if not false_positives:
            return Mutation(
                strategy="add_counter_example",
                description="No false positives to address",
                modified_skill=skill_content
            )
        
        prompt = f"""You are improving a code review skill that produced false positives.

**Current skill:**
{skill_content}

**False positives:**
{json.dumps(false_positives[:3], indent=2)}

Add a counter-example to the "Examples" section showing safe code that should NOT be flagged.
This will help avoid similar false positives in the future.

Return the FULL modified skill content with the new counter-example added.
"""
        
        try:
            modified = self.llm.complete(prompt, temperature=0.7)
            return Mutation(
                strategy="add_counter_example",
                description=f"Added counter-example to avoid {len(false_positives)} false positives",
                modified_skill=modified
            )
        except Exception as e:
            return Mutation(
                strategy="add_counter_example",
                description=f"Failed: {str(e)}",
                modified_skill=skill_content
            )
    
    def _refine_instruction(
        self,
        skill_content: str,
        patterns: Dict[str, Any]
    ) -> Mutation:
        """Reword an instruction that's being misinterpreted."""
        common_failures = patterns.get("common_failures", {})
        
        if not common_failures:
            return Mutation(
                strategy="refine_instruction",
                description="No clear instruction issues",
                modified_skill=skill_content
            )
        
        most_common = max(common_failures.items(), key=lambda x: x[1])
        
        prompt = f"""You are improving a code review skill that has instruction clarity issues.

**Current skill:**
{skill_content}

**Most common failure:** {most_common[0]} (failed {most_common[1]} times)

Refine the instructions in the "Review Instructions" section to be clearer and more specific.
Focus on making the guidance unambiguous and actionable.

Return the FULL modified skill content with refined instructions.
"""
        
        try:
            modified = self.llm.complete(prompt, temperature=0.7)
            return Mutation(
                strategy="refine_instruction",
                description=f"Refined instructions for {most_common[0]}",
                modified_skill=modified
            )
        except Exception as e:
            return Mutation(
                strategy="refine_instruction",
                description=f"Failed: {str(e)}",
                modified_skill=skill_content
            )
    
    def _add_platform_guidance(
        self,
        skill_content: str,
        patterns: Dict[str, Any]
    ) -> Mutation:
        """Add platform-specific guidance for platform-specific failures."""
        # This is a simpler mutation that doesn't require failure analysis
        prompt = f"""You are improving a code review skill with platform-specific guidance.

**Current skill:**
{skill_content}

Enhance the "Platform-Specific Guidance" section with more detailed, actionable advice
for each platform (Web/API, Android, iOS, Microservices).

Return the FULL modified skill content with enhanced platform guidance.
"""
        
        try:
            modified = self.llm.complete(prompt, temperature=0.7)
            return Mutation(
                strategy="add_platform_guidance",
                description="Enhanced platform-specific guidance",
                modified_skill=modified
            )
        except Exception as e:
            return Mutation(
                strategy="add_platform_guidance",
                description=f"Failed: {str(e)}",
                modified_skill=skill_content
            )
    
    def _remove_noise(
        self,
        skill_content: str,
        patterns: Dict[str, Any]
    ) -> Mutation:
        """Remove instructions that aren't helping."""
        # This requires correlation analysis - for now, we'll just trim verbose sections
        prompt = f"""You are streamlining a code review skill by removing unhelpful content.

**Current skill:**
{skill_content}

Remove redundant or overly verbose instructions that don't add value.
Keep the skill concise and focused on actionable detection strategies.

Return the FULL modified skill content with noise removed.
"""
        
        try:
            modified = self.llm.complete(prompt, temperature=0.7)
            return Mutation(
                strategy="remove_noise",
                description="Removed redundant instructions",
                modified_skill=modified
            )
        except Exception as e:
            return Mutation(
                strategy="remove_noise",
                description=f"Failed: {str(e)}",
                modified_skill=skill_content
            )
