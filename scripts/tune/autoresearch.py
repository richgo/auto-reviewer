#!/usr/bin/env python3
"""
Autoresearch tuning loop for code review skills.

Inspired by:
- https://www.mindstudio.ai/blog/claude-code-autoresearch-self-improving-skills
- https://github.com/karpathy/autoresearch

Core loop:
1. Run skill against eval cases
2. Score results with binary assertions
3. Identify failure patterns
4. Mutate skill to address failures
5. Re-evaluate
6. Keep mutation if score improves, discard if not
7. Repeat 30-50 cycles
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
from datetime import datetime

from rich.console import Console
from rich.progress import track

from .llm_client import LLMClient
from .scorer import Scorer, EvalScore
from .mutator import Mutator


console = Console()


class AutoResearcher:
    """
    Main autoresearch tuning loop.
    
    Iteratively improves a skill by:
    1. Running it against eval cases
    2. Scoring with binary assertions
    3. Analyzing failures
    4. Generating mutations
    5. Keeping improvements
    """
    
    def __init__(
        self,
        skill_path: Path,
        evals_path: Path,
        model: str,
        max_iterations: int,
        target_pass_rate: float,
        output_path: Path,
        log_path: Path
    ):
        """
        Initialize AutoResearcher.
        
        Args:
            skill_path: Path to skill markdown file
            evals_path: Path to evals JSON file
            model: LLM model to use
            max_iterations: Maximum optimization iterations
            target_pass_rate: Target pass rate to achieve (0.0-1.0)
            output_path: Where to save optimized skill
            log_path: Where to save tuning log (JSONL)
        """
        self.skill_path = skill_path
        self.evals_path = evals_path
        self.model = model
        self.max_iterations = max_iterations
        self.target_pass_rate = target_pass_rate
        self.output_path = output_path
        self.log_path = log_path
        
        self.llm = LLMClient(model)
        self.scorer = Scorer(model)
        self.mutator = Mutator(model)
        
        self.current_skill = self._load_skill()
        self.eval_cases = self._load_evals()
        self.best_skill = self.current_skill
        self.best_score = 0.0
        
    def _load_skill(self) -> str:
        """Load skill markdown content."""
        with open(self.skill_path) as f:
            return f.read()
    
    def _load_evals(self) -> List[Dict[str, Any]]:
        """Load eval cases from JSON file."""
        with open(self.evals_path) as f:
            data = json.load(f)
            # Handle both formats: {"evals": [...]} and direct array
            if isinstance(data, dict):
                return data.get("cases", data.get("evals", []))
            return data
    
    def _run_skill_on_case(
        self,
        skill_content: str,
        eval_case: Dict[str, Any]
    ) -> str:
        """
        Simulate running the skill on an eval case.
        Uses LLM to generate a code review based on the skill.
        
        Args:
            skill_content: The skill markdown content
            eval_case: Eval case with code to review
            
        Returns:
            Review output text
        """
        code_snippet = eval_case.get("code_snippet", eval_case.get("prompt", ""))
        language = eval_case.get("language", "python")
        
        system_prompt = f"""You are a code reviewer using this skill:

{skill_content}

Follow the skill's detection strategies and review instructions exactly."""

        user_prompt = f"""Review this {language} code:

```{language}
{code_snippet}
```

Provide a code review following the skill's guidelines. Include:
- Whether there are security/quality issues
- Severity level if issues found
- Specific line numbers
- Concrete fix suggestions
- Evidence from the code"""

        try:
            review = self.llm.complete(user_prompt, system=system_prompt, temperature=0.3)
            return review
        except Exception as e:
            return f"Error running skill: {str(e)}"
    
    def _evaluate_current_skill(self) -> Tuple[float, List[Tuple[Dict, EvalScore]]]:
        """
        Evaluate current skill against all eval cases.
        
        Returns:
            (average_pass_rate, list of (eval_case, score) tuples)
        """
        results: List[Tuple[Dict, EvalScore]] = []
        
        for eval_case in track(self.eval_cases, description="Evaluating skill..."):
            review_output = self._run_skill_on_case(self.current_skill, eval_case)
            score = self.scorer.score_review(review_output, eval_case)
            results.append((eval_case, score))
        
        avg_pass_rate = sum(score.pass_rate for _, score in results) / len(results)
        return avg_pass_rate, results
    
    def _log_iteration(
        self,
        iteration: int,
        pass_rate: float,
        mutation_strategy: str,
        mutation_desc: str,
        accepted: bool,
        failure_patterns: Dict[str, Any]
    ) -> None:
        """Log iteration results to JSONL file."""
        log_entry = {
            "iteration": iteration,
            "timestamp": datetime.now().isoformat(),
            "pass_rate": pass_rate,
            "mutation_strategy": mutation_strategy,
            "mutation_description": mutation_desc,
            "accepted": accepted,
            "failure_patterns": {
                "total_cases": failure_patterns.get("total_cases", 0),
                "failed_cases": failure_patterns.get("failed_cases", 0),
                "common_failures": failure_patterns.get("common_failures", {}),
                "false_negative_count": len(failure_patterns.get("false_negatives", [])),
                "false_positive_count": len(failure_patterns.get("false_positives", [])),
            }
        }
        
        with open(self.log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def run(self) -> None:
        """Run the autoresearch optimization loop."""
        console.print(f"\n[bold cyan]Autoresearch Tuning Loop[/bold cyan]")
        console.print(f"Skill: {self.skill_path}")
        console.print(f"Evals: {self.evals_path} ({len(self.eval_cases)} cases)")
        console.print(f"Model: {self.model}")
        console.print(f"Target: {self.target_pass_rate:.1%} pass rate\n")
        
        # Initial evaluation
        console.print("[yellow]Initial evaluation...[/yellow]")
        initial_pass_rate, initial_results = self._evaluate_current_skill()
        self.best_score = initial_pass_rate
        
        console.print(f"[bold]Initial pass rate: {initial_pass_rate:.1%}[/bold]\n")
        
        self._log_iteration(
            0,
            initial_pass_rate,
            "baseline",
            "Initial skill evaluation",
            True,
            self.mutator.analyze_failures(initial_results)
        )
        
        # Optimization loop
        for iteration in range(1, self.max_iterations + 1):
            console.print(f"\n[bold]Iteration {iteration}/{self.max_iterations}[/bold]")
            
            # Analyze failures from current skill
            _, current_results = self._evaluate_current_skill()
            failure_patterns = self.mutator.analyze_failures(current_results)
            
            # Pick a mutation strategy based on failure patterns
            strategy = self._select_strategy(failure_patterns)
            console.print(f"Strategy: {strategy}")
            
            # Generate mutation
            mutation = self.mutator.generate_mutation(
                self.current_skill,
                failure_patterns,
                strategy
            )
            console.print(f"Mutation: {mutation.description}")
            
            # Evaluate mutated skill
            mutated_skill_backup = self.current_skill
            self.current_skill = mutation.modified_skill
            
            pass_rate, results = self._evaluate_current_skill()
            console.print(f"Pass rate: {pass_rate:.1%} (was {self.best_score:.1%})")
            
            # Accept or reject mutation
            if pass_rate > self.best_score:
                console.print("[green]✓ Accepted (improvement)[/green]")
                self.best_score = pass_rate
                self.best_skill = mutation.modified_skill
                accepted = True
            else:
                console.print("[red]✗ Rejected (no improvement)[/red]")
                self.current_skill = mutated_skill_backup
                accepted = False
            
            self._log_iteration(
                iteration,
                pass_rate,
                strategy,
                mutation.description,
                accepted,
                failure_patterns
            )
            
            # Check if target reached
            if self.best_score >= self.target_pass_rate:
                console.print(f"\n[bold green]Target {self.target_pass_rate:.1%} reached![/bold green]")
                break
        
        # Save optimized skill
        console.print(f"\n[bold]Optimization complete[/bold]")
        console.print(f"Best pass rate: {self.best_score:.1%}")
        console.print(f"Saving to: {self.output_path}")
        
        with open(self.output_path, "w") as f:
            f.write(self.best_skill)
        
        console.print(f"Log saved to: {self.log_path}\n")
    
    def _select_strategy(self, failure_patterns: Dict[str, Any]) -> str:
        """
        Select mutation strategy based on failure patterns.
        
        Args:
            failure_patterns: Failure analysis from mutator
            
        Returns:
            Strategy name
        """
        # Priority-based selection
        false_negatives = len(failure_patterns.get("false_negatives", []))
        false_positives = len(failure_patterns.get("false_positives", []))
        missing_fixes = len(failure_patterns.get("missing_fixes", []))
        
        if false_negatives > 0:
            return "add_detection_heuristic"
        elif false_positives > 0:
            return "add_counter_example"
        elif missing_fixes > 0:
            return "refine_instruction"
        else:
            # Rotate through other strategies
            import random
            return random.choice(["add_platform_guidance", "remove_noise"])


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Autoresearch tuning loop for code review skills"
    )
    parser.add_argument(
        "--skill",
        type=Path,
        required=True,
        help="Path to skill markdown file"
    )
    parser.add_argument(
        "--evals",
        type=Path,
        required=True,
        help="Path to evals JSON file"
    )
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-20250514",
        help="LLM model to use"
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=30,
        help="Maximum optimization iterations"
    )
    parser.add_argument(
        "--target-pass-rate",
        type=float,
        default=0.95,
        help="Target pass rate (0.0-1.0)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output path for optimized skill (default: overwrites input)"
    )
    parser.add_argument(
        "--log",
        type=Path,
        help="Path for tuning log JSONL (default: tune-logs/<skill-name>.jsonl)"
    )
    
    args = parser.parse_args()
    
    # Set defaults
    if args.output is None:
        args.output = args.skill
    
    if args.log is None:
        log_dir = Path("tune-logs")
        log_dir.mkdir(exist_ok=True)
        args.log = log_dir / f"{args.skill.stem}.jsonl"
    
    # Run tuning
    researcher = AutoResearcher(
        skill_path=args.skill,
        evals_path=args.evals,
        model=args.model,
        max_iterations=args.max_iterations,
        target_pass_rate=args.target_pass_rate,
        output_path=args.output,
        log_path=args.log
    )
    
    researcher.run()


if __name__ == "__main__":
    main()
