# Tasks: Phase 2 - SWE-bench-Style Scoring

## Phase 1: Benchmark Harness & Copilot Sessions

- [ ] **1.1** Add benchmark dependencies and shared result schemas  
  Update `scripts/requirements.txt` and `scripts/benchmark/__init__.py` to support Copilot SDK integration, retry helpers, and shared structures for run metadata/raw result rows. (Specs: benchmark-harness Result Storage)

- [ ] **1.2** Implement Copilot SDK wrapper module  
  Create `scripts/benchmark/copilot_client.py` with model discovery, session creation, BYOK provider passthrough, prompt send/wait, and streaming hooks for TTFT/total latency capture. (Specs: benchmark-harness Copilot SDK Integration scenarios)

- [ ] **1.3** Implement content-hash cache module  
  Create `scripts/benchmark/cache.py` to compute `(skill, eval, model)` hashes, read/write cached runs, and report cache-hit reuse when hashes are unchanged. (Spec: benchmark-harness Cached Results)

- [ ] **1.4** Refactor runner CLI and discovery flow  
  Extend `scripts/benchmark/runner.py` to support full discovery, `--skill`, `--models`, `--all-models`, model availability validation, and output directory layout per run id. (Specs: benchmark-harness CLI Interface + Available Models Discovery)

- [ ] **1.5** Add batch execution engine with retries and fault isolation  
  In `scripts/benchmark/runner.py`, add configurable concurrency (default 4), exponential backoff (max 3 retries), and continue-on-failure behavior for individual combinations. (Spec: benchmark-harness Batch Execution Across Models)

- [ ] **1.6** Persist metadata and raw JSONL artifacts  
  Write `benchmark-results/<run-id>/metadata.json` and append required raw result fields to `benchmark-results/<run-id>/raw_results.jsonl` including hashes, latency, tokens, and timestamps. (Specs: benchmark-harness Result File Structure + Run Metadata + Single Run)

- [ ] **1.7** Implement dry-run planning and pricing bootstrap  
  Add `--dry-run` behavior in `scripts/benchmark/runner.py` and create `scripts/benchmark/pricing.json` so dry runs list combinations and estimate API calls/token cost without model requests. (Specs: benchmark-harness Dry Run, model-scoring Cost Estimation)

## Phase 2: Scoring, Aggregation, and Reporting

- [ ] **2.1** Build binary assertion judge module  
  Create `scripts/benchmark/judge.py` with strict pass/fail prompt templates, configurable judge model (default `gpt-4.1`), and robust response parsing. (Specs: model-scoring Assertion Types + LLM-as-Judge Scoring)

- [ ] **2.2** Add eval assertion migration utility  
  Create `scripts/benchmark/migrate_evals.py` and migrate `evals/*.json` from legacy assertion keys to binary assertion schema while preserving counter-example metadata. (Specs: model-scoring Binary Assertion Evaluation + Counter-Example Scoring)

- [ ] **2.3** Implement assertion scoring pipeline and JSONL output  
  Create `scripts/benchmark/scorer.py` and integrate with `runner.py` to evaluate each assertion, skip non-`no_false_positive` checks for counter examples, and write `assertion_results.jsonl`. (Specs: model-scoring Binary Assertion Evaluation scenarios)

- [ ] **2.4** Implement aggregate metric calculations with confidence rules  
  Add aggregation logic in `scripts/benchmark/scorer.py` for pass_rate, detection/false-positive/actionability rates, precision/recall/F1, mean latency/tokens, stddev outputs, and low-confidence flags for `N < 5`. (Specs: model-scoring Aggregate Metrics scenarios)

- [ ] **2.5** Generate model score matrix and best-model updates  
  Write `benchmark-results/<run-id>/model_scores.json` with required nested shape and update `skills/model-scores.yml` using F1 then pass_rate tie-breaks, including `needs tuning` flags when F1 <= 0.70. (Specs: model-scoring Matrix Generation + Best Model Selection)

- [ ] **2.6** Add per-run and per-skill cost rollups  
  Use token usage plus `scripts/benchmark/pricing.json` to compute estimated cost per `(skill, model)` and total run cost, and expose values in score outputs. (Spec: model-scoring Per-Run Cost Tracking)

- [ ] **2.7** Extend reporter CLI formats and baseline comparison  
  Update `scripts/benchmark/reporter.py` to support `--format markdown|json|github` and `--compare-to` baseline inputs with shared report data assembly. (Specs: reporting JSON Export + GitHub Actions Output + Cross-Run Comparison)

- [ ] **2.8** Implement markdown leaderboard, difficulty, and pairing sections  
  Generate overall/per-category F1 leaderboard, hardest-to-easiest skill ranking with unsolved/trivial flags, and `recommended_pairings` based on complementary miss patterns. (Specs: reporting Model Leaderboard, Skill Difficulty Ranking, Adversarial Pairings)

- [ ] **2.9** Implement heatmap export and regression reporting  
  Export `benchmark-results/<run-id>/heatmap.csv`, add emoji color bands in markdown, and produce `regressions` section for F1 drop > 0.05 and latency increase > 50%. (Specs: reporting Heatmap Data Export + Regression Detection)

- [ ] **2.10** Implement GitHub summary outputs and failure signaling  
  For `--format github`, emit step-summary markdown, set outputs for overall pass rate and regression count, and return exit code 1 when regression thresholds are exceeded. (Spec: reporting GitHub Actions Output)

## Phase 3: Testing & Verification

- [ ] **3.1** Write unit tests for harness/scoring modules  
  Add tests for `scripts/benchmark/copilot_client.py`, `cache.py`, `judge.py`, and `scorer.py` using mocked model responses to cover model discovery, retry paths, counter-example handling, and strict pass/fail parsing. (Covers benchmark-harness + model-scoring scenarios)

- [ ] **3.2** Write integration tests for end-to-end benchmark/report flows  
  Add integration coverage for single-skill runs, dry-run behavior, cache reuse, model score matrix generation, heatmap export, regression comparison, and JSON/GitHub formatter outputs. (Covers benchmark-harness CLI + model-scoring matrix + reporting scenarios)

- [ ] **3.3** Manual verification checklist  
  Run a small multi-model benchmark plus single-skill and dry-run modes, then verify all expected artifacts (`metadata.json`, `raw_results.jsonl`, `assertion_results.jsonl`, `model_scores.json`, `heatmap.csv`, `report.md`) and GitHub regression exit behavior align with spec thresholds.
