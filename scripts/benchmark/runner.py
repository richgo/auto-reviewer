#!/usr/bin/env python3
"""
SWE-bench-style benchmark harness for code review skills.

Runs all skills against their eval sets and produces a model × skill score matrix.
Supports multiple models for comparison.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Import from tune module
sys.path.insert(0, str(Path(__file__).parent.parent))
from tune.llm_client import CopilotLLMClient
from tune.scorer import Scorer


console = Console()


class BenchmarkRunner:
    """
    Benchmark harness that runs skills against eval sets and tracks scores.
    """
    
    def __init__(
        self,
        skills_dir: Path,
        evals_dir: Path,
        models: List[str],
        output_dir: Path
    ):
        """
        Initialize benchmark runner.
        
        Args:
            skills_dir: Directory containing skill markdown files
            evals_dir: Directory containing eval JSON files
            models: List of model identifiers to benchmark
            output_dir: Where to save results
        """
        self.skills_dir = skills_dir
        self.evals_dir = evals_dir
        self.models = models
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def find_skill_eval_pairs(self) -> List[tuple]:
        """
        Find matching skill/eval pairs.
        
        Returns:
            List of (skill_path, eval_path, skill_name) tuples
        """
        pairs = []
        
        # Look in skills/concerns/ for concern skills
        concerns_dir = self.skills_dir / "concerns"
        if concerns_dir.exists():
            for skill_file in concerns_dir.glob("*.md"):
                skill_name = skill_file.stem
                eval_file = self.evals_dir / f"{skill_name}.json"
                
                if eval_file.exists():
                    pairs.append((skill_file, eval_file, skill_name))
        
        return pairs
    
    def run_skill_on_eval(
        self,
        skill_content: str,
        eval_case: Dict[str, Any],
        model: str
    ) -> str:
        """
        Run a skill on a single eval case using specified model.
        
        Args:
            skill_content: Skill markdown content
            eval_case: Eval case dict
            model: Model identifier
            
        Returns:
            Review output text
        """
        llm = CopilotLLMClient(model)
        
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
            review = llm.complete(user_prompt, system=system_prompt, temperature=0.3)
            return review
        except Exception as e:
            return f"Error running skill: {str(e)}"
    
    def benchmark_skill(
        self,
        skill_path: Path,
        eval_path: Path,
        skill_name: str,
        model: str
    ) -> Dict[str, Any]:
        """
        Benchmark a single skill with a model.
        
        Args:
            skill_path: Path to skill file
            eval_path: Path to eval file
            skill_name: Skill identifier
            model: Model identifier
            
        Returns:
            Results dict with scores
        """
        # Load skill
        with open(skill_path) as f:
            skill_content = f.read()
        
        # Load evals
        with open(eval_path) as f:
            eval_data = json.load(f)
            eval_cases = eval_data.get("cases", eval_data.get("evals", []))
        
        if not eval_cases:
            return {
                "skill": skill_name,
                "model": model,
                "pass_rate": 0.0,
                "f1": 0.0,
                "total_cases": 0,
                "error": "No eval cases found"
            }
        
        scorer = Scorer(model)
        pass_rates = []
        
        for eval_case in eval_cases:
            review = self.run_skill_on_eval(skill_content, eval_case, model)
            score = scorer.score_review(review, eval_case)
            pass_rates.append(score.pass_rate)
        
        avg_pass_rate = sum(pass_rates) / len(pass_rates)
        
        # Calculate F1 (approximation: F1 ≈ pass_rate for balanced datasets)
        f1 = avg_pass_rate
        
        return {
            "skill": skill_name,
            "model": model,
            "pass_rate": avg_pass_rate,
            "f1": f1,
            "total_cases": len(eval_cases),
            "last_run": datetime.now().isoformat()
        }
    
    def run(self) -> Dict[str, Any]:
        """
        Run full benchmark across all skills and models.
        
        Returns:
            Results dict with model × skill scores
        """
        console.print("\n[bold cyan]Benchmark Runner[/bold cyan]\n")
        
        # Find skill/eval pairs
        pairs = self.find_skill_eval_pairs()
        console.print(f"Found {len(pairs)} skill/eval pairs")
        console.print(f"Testing {len(self.models)} models\n")
        
        # Results storage
        results = {
            "timestamp": datetime.now().isoformat(),
            "models": {},
            "skills": [pair[2] for pair in pairs]
        }
        assertion_results_path = self.output_dir / "assertion_results.jsonl"
        assertion_results_path.write_text("", encoding="utf-8")
        
        for model in self.models:
            results["models"][model] = {}
        
        # Run benchmarks
        total_runs = len(pairs) * len(self.models)
        current = 0
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Benchmarking...", total=total_runs)
            
            for skill_path, eval_path, skill_name in pairs:
                for model in self.models:
                    current += 1
                    progress.update(
                        task,
                        description=f"[{current}/{total_runs}] {skill_name} × {model}"
                    )
                    
                    result = self.benchmark_skill(
                        skill_path,
                        eval_path,
                        skill_name,
                        model
                    )
                    
                    results["models"][model][skill_name] = {
                        "pass_rate": result["pass_rate"],
                        "f1": result["f1"],
                        "total_cases": result["total_cases"],
                        "last_run": result["last_run"]
                    }
                    self._append_assertion_stub(
                        assertion_results_path,
                        skill_name=skill_name,
                        model=model,
                        pass_rate=result["pass_rate"],
                        timestamp=result["last_run"],
                    )
                    
                    progress.advance(task)
        
        # Save results
        output_file = self.output_dir / "model_scores.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        
        console.print(f"\n[green]✓ Benchmark complete[/green]")
        console.print(f"Results saved to: {output_file}\n")
        
        # Print summary table
        self._print_summary(results)
        
        return results
    
    def _print_summary(self, results: Dict[str, Any]) -> None:
        """Print summary table of results."""
        table = Table(title="Benchmark Results (Pass Rates)")
        
        table.add_column("Skill", style="cyan")
        for model in results["models"].keys():
            table.add_column(model, justify="right")
        
        for skill in results["skills"]:
            row = [skill]
            for model in results["models"].keys():
                score_data = results["models"][model].get(skill, {})
                pass_rate = score_data.get("pass_rate", 0.0)
                row.append(f"{pass_rate:.1%}")
            table.add_row(*row)
        
        console.print(table)

    @staticmethod
    def _append_assertion_stub(
        output_path: Path,
        *,
        skill_name: str,
        model: str,
        pass_rate: float,
        timestamp: str,
    ) -> None:
        with output_path.open("a", encoding="utf-8") as assertion_handle:
            assertion_handle.write(
                json.dumps(
                    {
                        "skill_name": skill_name,
                        "model_id": model,
                        "pass_rate": pass_rate,
                        "timestamp": timestamp,
                    }
                )
                + "\n"
            )


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Benchmark code review skills across models"
    )
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=Path("skills"),
        help="Directory containing skills"
    )
    parser.add_argument(
        "--evals-dir",
        type=Path,
        default=Path("evals"),
        help="Directory containing eval JSON files"
    )
    parser.add_argument(
        "--models",
        default="claude-sonnet-4-20250514",
        help="Comma-separated list of models to test"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("benchmark-results"),
        help="Output directory for results"
    )
    
    args = parser.parse_args()
    
    models = [m.strip() for m in args.models.split(",")]
    
    runner = BenchmarkRunner(
        skills_dir=args.skills_dir,
        evals_dir=args.evals_dir,
        models=models,
        output_dir=args.output
    )
    
    runner.run()


if __name__ == "__main__":
    main()
