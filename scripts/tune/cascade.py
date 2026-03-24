"""Multi-model tuning cascade orchestrator.

Coordinates automatic escalation of difficult skills through a sequence of
models, attempting each until reaching the target pass rate or exhausting stages.
"""


class CascadeOrchestrator:
    """Orchestrates multi-model tuning cascade for a skill."""

    def __init__(self, skill_name, history_dir, config):
        """Initialize cascade orchestrator.

        Args:
            skill_name: Name of the skill to tune.
            history_dir: Path to skill's tuning history directory.
            config: Configuration dict with cascade settings.
        """
        self.skill_name = skill_name
        self.history_dir = history_dir
        self.config = config

    def _run_single_stage(self, model, max_iterations, target_pass_rate):
        """Run a single tuning stage with the given model.

        Args:
            model: Model identifier (e.g., "gpt-5-mini").
            max_iterations: Maximum iterations for this stage.
            target_pass_rate: Target pass rate (e.g., 0.95 for 95%).

        Returns:
            Dict with tuning results including pass_rate and model.
        """
        raise NotImplementedError("Subclass must implement _run_single_stage")

    def run(self):
        """Run cascade through stages until convergence or exhaustion.

        Returns:
            Dict with cascade results:
            - pass_rate: Best achieved pass rate
            - needs_review: True if all stages failed to reach target
            - best_model: Model that achieved best result
            - best_pass_rate: Best pass rate achieved
            - stage: Stage number that succeeded (0 if none)
        """
        stages = self.config.get("cascade", {}).get("stages", [])
        best_result = None
        best_pass_rate = 0.0
        best_model = None

        for stage_idx, stage_config in enumerate(stages, 1):
            model = stage_config["model"]
            max_iterations = stage_config["max_iterations"]
            target_pass_rate = stage_config["target_pass_rate"]

            # Run this stage
            result = self._run_single_stage(model, max_iterations, target_pass_rate)

            # Track best result
            if result["pass_rate"] > best_pass_rate:
                best_pass_rate = result["pass_rate"]
                best_model = model
                best_result = result

            # Check if we've reached the target
            if result["pass_rate"] >= target_pass_rate:
                result["stage"] = stage_idx
                return result

        # All stages exhausted - mark for review
        # Use the last attempted model (most capable) as the one that "failed"
        last_model = stages[-1]["model"] if stages else None
        return {
            "pass_rate": best_pass_rate,
            "needs_review": True,
            "best_model": last_model or best_model,
            "best_pass_rate": best_pass_rate,
            "stage": 0,
            "model": last_model or best_model,
        }
