#!/usr/bin/env python3
"""
Generate markdown reports from benchmark results.

Produces:
- Model leaderboard per skill
- Skill difficulty ranking
- Heatmap data
- Adversarial pairing recommendations
"""

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional


class BenchmarkReporter:
    """Generate reports from benchmark results."""
    
    def __init__(self, results_path: Path, compare_to: Optional[Path] = None):
        """
        Initialize reporter.
        
        Args:
            results_path: Path to model_scores.json
        """
        self.results_path = results_path
        with open(results_path) as f:
            self.results = json.load(f)
        self.baseline = None
        if compare_to and compare_to.exists():
            with open(compare_to) as f:
                self.baseline = json.load(f)
    
    def generate_report(self) -> str:
        """
        Generate full markdown report.
        
        Returns:
            Markdown report string
        """
        lines = [
            "# Code Review Skills Benchmark Report",
            "",
            f"**Generated:** {self.results['timestamp']}",
            f"**Models tested:** {', '.join(self.results['models'].keys())}",
            f"**Skills evaluated:** {len(self.results['skills'])}",
            "",
            "---",
            ""
        ]
        
        # Model leaderboard
        lines.extend(self._model_leaderboard())
        lines.append("")
        
        # Skill difficulty ranking
        lines.extend(self._skill_difficulty_ranking())
        lines.append("")
        
        # Detailed scores
        lines.extend(self._detailed_scores())
        lines.append("")
        
        # Adversarial pairings
        lines.extend(self._adversarial_pairings())
        lines.append("")
        
        # Heatmap data
        lines.extend(self._heatmap_data())
        
        return "\n".join(lines)

    def generate_json_report(self) -> Dict[str, Any]:
        """Generate structured JSON report payload."""
        return {
            "timestamp": self.results.get("timestamp"),
            "leaderboard": self._leaderboard_payload(),
            "regressions": self._regressions(),
            "model_scores": self.results.get("models", {}),
        }

    def generate_github_output(self) -> Dict[str, Any]:
        json_payload = self.generate_json_report()
        regressions = json_payload.get("regressions", [])
        overall_pass_rates = self._collect_pass_rates()
        overall_pass_rate = (
            sum(overall_pass_rates) / len(overall_pass_rates)
            if overall_pass_rates
            else 0.0
        )
        summary_lines = [
            "## Benchmark Summary",
            "",
            f"- Overall pass rate: {overall_pass_rate:.1%}",
            f"- Regressions: {len(regressions)}",
        ]
        return {
            "summary_markdown": "\n".join(summary_lines),
            "outputs": {
                "overall_pass_rate": round(overall_pass_rate, 6),
                "regression_count": len(regressions),
            },
            "exit_code": 1 if regressions else 0,
        }

    def _collect_pass_rates(self) -> List[float]:
        pass_rates: List[float] = []
        for model_scores in self.results.get("models", {}).values():
            pass_rates.extend(score.get("pass_rate", 0.0) for score in model_scores.values())
        return pass_rates
    
    def _model_leaderboard(self) -> List[str]:
        """Generate model leaderboard section."""
        lines = [
            "## Model Leaderboard",
            "",
            "Average pass rate across all skills:",
            ""
        ]
        
        # Calculate average for each model
        model_avgs: List[Tuple[str, float]] = []
        
        for model, skills in self.results["models"].items():
            pass_rates = [data["pass_rate"] for data in skills.values()]
            avg = sum(pass_rates) / len(pass_rates) if pass_rates else 0.0
            model_avgs.append((model, avg))
        
        # Sort by average descending
        model_avgs.sort(key=lambda x: x[1], reverse=True)
        
        lines.append("| Rank | Model | Avg Pass Rate |")
        lines.append("|------|-------|---------------|")
        
        for rank, (model, avg) in enumerate(model_avgs, 1):
            medal = "🥇" if rank == 1 else ("🥈" if rank == 2 else ("🥉" if rank == 3 else ""))
            lines.append(f"| {rank} {medal} | {model} | {avg:.1%} |")
        
        return lines

    def _leaderboard_payload(self) -> List[Dict[str, Any]]:
        model_avgs: List[Tuple[str, float]] = []
        for model, skills in self.results.get("models", {}).items():
            f1_scores = [data.get("f1", 0.0) for data in skills.values()]
            avg = sum(f1_scores) / len(f1_scores) if f1_scores else 0.0
            model_avgs.append((model, avg))
        model_avgs.sort(key=lambda x: x[1], reverse=True)
        payload = [
            {"rank": idx, "model": model, "avg_f1": avg}
            for idx, (model, avg) in enumerate(model_avgs, start=1)
        ]
        return payload

    def _regressions(self) -> List[Dict[str, Any]]:
        if not self.baseline:
            return []
        regressions: List[Dict[str, Any]] = []
        for model_id, skill_scores in self.results.get("models", {}).items():
            baseline_model = self.baseline.get("models", {}).get(model_id, {})
            for skill, current in skill_scores.items():
                previous = baseline_model.get(skill)
                if not previous:
                    continue
                current_f1 = float(current.get("f1", 0.0))
                previous_f1 = float(previous.get("f1", 0.0))
                current_latency = float(current.get("mean_latency_ms", 0.0))
                previous_latency = float(previous.get("mean_latency_ms", 0.0))
                f1_drop = previous_f1 - current_f1
                latency_increase = (
                    (current_latency - previous_latency) / previous_latency
                    if previous_latency > 0
                    else 0.0
                )
                if f1_drop > 0.05 or latency_increase > 0.5:
                    regressions.append(
                        {
                            "model": model_id,
                            "skill": skill,
                            "f1_drop": f1_drop,
                            "latency_increase_pct": latency_increase * 100.0,
                        }
                    )
        return regressions
    
    def _skill_difficulty_ranking(self) -> List[str]:
        """Generate skill difficulty ranking section."""
        lines = [
            "## Skill Difficulty Ranking",
            "",
            "Skills ranked by average pass rate (lower = harder):",
            ""
        ]
        
        # Calculate average for each skill
        skill_avgs: List[Tuple[str, float]] = []
        
        for skill in self.results["skills"]:
            pass_rates = []
            for model_data in self.results["models"].values():
                if skill in model_data:
                    pass_rates.append(model_data[skill]["pass_rate"])
            
            avg = sum(pass_rates) / len(pass_rates) if pass_rates else 0.0
            skill_avgs.append((skill, avg))
        
        # Sort by average ascending (hardest first)
        skill_avgs.sort(key=lambda x: x[1])
        
        lines.append("| Rank | Skill | Avg Pass Rate | Difficulty |")
        lines.append("|------|-------|---------------|------------|")
        unsolved_skills: List[str] = []
        trivial_skills: List[str] = []
        
        for rank, (skill, avg) in enumerate(skill_avgs, 1):
            if avg < 0.5:
                difficulty = "🔴 Very Hard"
            elif avg < 0.7:
                difficulty = "🟠 Hard"
            elif avg < 0.85:
                difficulty = "🟡 Medium"
            else:
                difficulty = "🟢 Easy"
            
            lines.append(f"| {rank} | {skill} | {avg:.1%} | {difficulty} |")
            if avg < 0.70:
                unsolved_skills.append(skill)
            if avg > 0.95:
                trivial_skills.append(skill)

        lines.append("")
        lines.extend(self._difficulty_labels(unsolved_skills, trivial_skills))
        
        return lines
    
    def _detailed_scores(self) -> List[str]:
        """Generate detailed scores section."""
        lines = [
            "## Detailed Scores",
            "",
            "Model performance per skill:",
            ""
        ]
        
        # Build table header
        header = ["Skill"] + list(self.results["models"].keys())
        lines.append("| " + " | ".join(header) + " |")
        lines.append("|" + "|".join(["---"] * len(header)) + "|")
        
        # Build rows
        for skill in sorted(self.results["skills"]):
            row = [skill]
            for model in self.results["models"].keys():
                score_data = self.results["models"][model].get(skill, {})
                pass_rate = score_data.get("pass_rate", 0.0)
                row.append(f"{pass_rate:.1%}")
            
            lines.append("| " + " | ".join(row) + " |")
        
        return lines
    
    def _adversarial_pairings(self) -> List[str]:
        """Generate adversarial pairing recommendations."""
        lines = [
            "## Adversarial Pairing Recommendations",
            "",
            "Model combinations that complement each other (different strengths):",
            "",
            "recommended_pairings",
            ""
        ]
        
        models = list(self.results["models"].keys())
        
        if len(models) < 2:
            lines.append("*(Requires at least 2 models for comparison)*")
            return lines
        
        # Find skills where models differ most
        max_variance_skills: List[Tuple[str, float, str, str]] = []
        
        for skill in self.results["skills"]:
            scores = {}
            for model in models:
                scores[model] = self.results["models"][model].get(skill, {}).get("pass_rate", 0.0)
            
            if len(scores) >= 2:
                sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                best_model = sorted_scores[0][0]
                worst_model = sorted_scores[-1][0]
                variance = sorted_scores[0][1] - sorted_scores[-1][1]
                
                if variance > 0.1:  # Only significant differences
                    max_variance_skills.append((skill, variance, best_model, worst_model))
        
        # Sort by variance
        max_variance_skills.sort(key=lambda x: x[1], reverse=True)
        
        if max_variance_skills:
            lines.append("| Skill | Variance | Best Model | Worst Model |")
            lines.append("|-------|----------|------------|-------------|")
            
            for skill, variance, best, worst in max_variance_skills[:10]:
                lines.append(f"| {skill} | {variance:.1%} | {best} | {worst} |")
            
            lines.append("")
            lines.append("**Recommendation:** Use multiple models on high-variance skills to catch different bug patterns.")
        else:
            lines.append("*(All models perform similarly)*")
        
        return lines

    @staticmethod
    def _difficulty_labels(unsolved_skills: List[str], trivial_skills: List[str]) -> List[str]:
        return [
            f"unsolved: {', '.join(unsolved_skills) if unsolved_skills else '(none)'}",
            f"trivial: {', '.join(trivial_skills) if trivial_skills else '(none)'}",
        ]
    
    def _heatmap_data(self) -> List[str]:
        """Generate heatmap data section."""
        lines = [
            "## Heatmap Data",
            "",
            "Model × Skill pass rate matrix (for visualization):",
            "",
            "```json"
        ]
        
        heatmap = {
            "models": list(self.results["models"].keys()),
            "skills": self.results["skills"],
            "data": []
        }
        
        for skill in self.results["skills"]:
            row = []
            for model in heatmap["models"]:
                score = self.results["models"][model].get(skill, {}).get("pass_rate", 0.0)
                row.append(round(score, 3))
            heatmap["data"].append(row)
        
        lines.append(json.dumps(heatmap, indent=2))
        lines.append("```")
        
        return lines

    def write_heatmap_csv(self, output_path: Path) -> None:
        models = list(self.results.get("models", {}).keys())
        skills = self.results.get("skills", [])
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["model", *skills])
            for model in models:
                row = [model, *self._heatmap_f1_values(model, skills)]
                writer.writerow(row)

    def _heatmap_f1_values(self, model: str, skills: List[str]) -> List[float]:
        return [
            self.results["models"].get(model, {}).get(skill, {}).get("f1", 0.0)
            for skill in skills
        ]


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate markdown report from benchmark results"
    )
    parser.add_argument(
        "results",
        type=Path,
        help="Path to model_scores.json"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output markdown file (default: print to stdout)"
    )
    
    args = parser.parse_args()
    
    reporter = BenchmarkReporter(args.results)
    report = reporter.generate_report()
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"Report saved to: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
