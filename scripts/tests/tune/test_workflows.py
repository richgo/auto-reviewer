import sys
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


class TestAutoResearchWorkflows(unittest.TestCase):
    def _load_workflow(self, name: str):
        repo_root = Path(__file__).resolve().parents[3]
        workflow_path = repo_root / ".github" / "workflows" / name
        return yaml.safe_load(workflow_path.read_text(encoding="utf-8"))

    def test_autoresearch_tuning_workflow_has_schedule_dispatch_and_path_triggers(self):
        workflow = self._load_workflow("autoresearch-tuning.yml")
        self.assertIn("on", workflow)
        self.assertIn("schedule", workflow["on"])
        self.assertIn("workflow_dispatch", workflow["on"])
        self.assertIn("push", workflow["on"])
        self.assertEqual(workflow["on"]["push"]["paths"], ["evals/**", "skills/**"])

    def test_autoresearch_tuning_workflow_runs_nightly(self):
        workflow = self._load_workflow("autoresearch-tuning.yml")
        schedules = workflow["on"]["schedule"]
        cron_expressions = [s["cron"] for s in schedules]
        # Should include a daily cron (runs every day, not just weekly)
        self.assertTrue(
            any(expr.endswith("* * *") for expr in cron_expressions),
            msg=f"Expected a nightly (daily) cron schedule but got: {cron_expressions}",
        )

    def test_autoresearch_tuning_workflow_plan_job_outputs_matrix(self):
        workflow = self._load_workflow("autoresearch-tuning.yml")
        plan_job = workflow["jobs"]["plan"]
        self.assertIn("outputs", plan_job)
        self.assertIn("matrix", plan_job["outputs"])

    def test_autoresearch_tuning_workflow_tune_pair_uses_dynamic_matrix(self):
        workflow = self._load_workflow("autoresearch-tuning.yml")
        tune_pair_job = workflow["jobs"]["tune_pair"]
        matrix_expr = tune_pair_job["strategy"]["matrix"]
        self.assertIn("fromJSON", matrix_expr)
        self.assertIn("needs.plan.outputs.matrix", matrix_expr)

    def test_autoresearch_tuning_workflow_generate_step_passes_skills_prefix_on_schedule(self):
        workflow = self._load_workflow("autoresearch-tuning.yml")
        plan_job = workflow["jobs"]["plan"]
        generate_step = next(
            step for step in plan_job["steps"] if step.get("id") == "generate"
        )
        run_script = generate_step["run"]
        self.assertIn("--skills-prefix security-", run_script)
        self.assertIn("schedule", run_script)

    def test_autoresearch_tuning_workflow_serializes_runs_per_skill_model(self):
        workflow = self._load_workflow("autoresearch-tuning.yml")
        jobs = workflow["jobs"]
        self.assertIn("tune_pair", jobs)
        self.assertIn("concurrency", jobs["tune_pair"])
        self.assertEqual(
            jobs["tune_pair"]["concurrency"]["group"],
            "autoresearch-${{ matrix.skill }}-${{ matrix.model }}",
        )

    def test_autoresearch_promote_workflow_enforces_branch_first_and_pr_permissions(self):
        workflow = self._load_workflow("autoresearch-promote.yml")
        self.assertEqual(workflow["permissions"]["contents"], "write")
        self.assertEqual(workflow["permissions"]["pull-requests"], "write")
        self.assertIn("workflow_call", workflow["on"])
        jobs = workflow["jobs"]
        self.assertIn("promote", jobs)
        promote_steps = jobs["promote"]["steps"]
        step_names = [step.get("name", "") for step in promote_steps]
        self.assertIn("Create promotion branch", step_names)
        self.assertIn("Open promotion PR", step_names)

    def test_autoresearch_promote_workflow_includes_regression_revert_job(self):
        workflow = self._load_workflow("autoresearch-promote.yml")
        jobs = workflow["jobs"]
        self.assertIn("revert_on_regression", jobs)
        revert_steps = jobs["revert_on_regression"]["steps"]
        step_names = [step.get("name", "") for step in revert_steps]
        self.assertIn("Detect post-merge regression", step_names)
        self.assertIn("Open revert PR", step_names)
        detect_step = next(step for step in revert_steps if step.get("name") == "Detect post-merge regression")
        open_revert_step = next(step for step in revert_steps if step.get("name") == "Open revert PR")
        self.assertEqual(detect_step.get("id"), "detect")
        self.assertEqual(open_revert_step.get("if"), "${{ steps.detect.outputs.regressed == 'true' }}")

    def test_benchmark_workflow_has_schedule_and_dispatch_triggers(self):
        workflow = self._load_workflow("benchmark.yml")
        self.assertIn("on", workflow)
        self.assertIn("schedule", workflow["on"])
        self.assertIn("workflow_dispatch", workflow["on"])

    def test_benchmark_workflow_defaults_to_free_models(self):
        workflow = self._load_workflow("benchmark.yml")
        jobs = workflow["jobs"]
        self.assertIn("run", jobs)
        run_steps = jobs["run"]["steps"]
        benchmark_step = next(
            step for step in run_steps if step.get("name") == "Run benchmark"
        )
        run_cmd = benchmark_step["run"]
        self.assertIn("gpt-4o-mini", run_cmd)
        self.assertIn("gemini-2.0-flash", run_cmd)

    def test_benchmark_workflow_runs_runner_and_reporter(self):
        workflow = self._load_workflow("benchmark.yml")
        jobs = workflow["jobs"]
        run_steps = jobs["run"]["steps"]
        step_names = [step.get("name", "") for step in run_steps]
        self.assertIn("Run benchmark", step_names)
        self.assertIn("Generate report", step_names)
        self.assertIn("Upload results", step_names)

    def test_benchmark_workflow_uses_copilot_sdk_not_provider_api_keys(self):
        workflow = self._load_workflow("benchmark.yml")
        jobs = workflow["jobs"]
        run_steps = jobs["run"]["steps"]
        benchmark_step = next(
            step for step in run_steps if step.get("name") == "Run benchmark"
        )
        env = benchmark_step.get("env") or {}
        self.assertNotIn("OPENAI_API_KEY", env)
        self.assertNotIn("GOOGLE_API_KEY", env)
        self.assertNotIn("ANTHROPIC_API_KEY", env)


if __name__ == "__main__":
    unittest.main()
