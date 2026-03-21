# Model Scoring Specification Delta

## ADDED Requirements

### Requirement: Binary Assertion Evaluation

The system SHALL evaluate each benchmark result against the eval case's binary assertions using an LLM-as-judge approach.

#### Scenario: Assertion Types

- GIVEN a benchmark result (the model's review output) and an eval case with assertions
- WHEN the scorer evaluates the result
- THEN it SHALL check each of these assertion types:
  - `detected_bug`: Did the review identify the specific bug described in the eval case?
  - `no_false_positive`: Did the review avoid flagging the counter-example as a bug?
  - `actionable_fix`: Did the review suggest a concrete, correct fix?
  - `correct_severity`: Did the review assign the correct severity level (critical/high/medium/low)?
  - `evidence_cited`: Did the review cite specific code lines or patterns as evidence?
- AND each assertion SHALL produce exactly one of: `pass` or `fail` (no partial credit)

#### Scenario: LLM-as-Judge Scoring

- GIVEN a review output and an assertion to evaluate
- WHEN the scorer judges the assertion
- THEN it SHALL send a structured prompt to a judge model containing: the original code snippet, the review output, the assertion criteria, and instructions to respond with pass/fail and a one-line justification
- AND it SHALL use a cheaper/faster model for judging (configurable, default: `claude-sonnet-4-20250514`)
- AND the judge prompt SHALL instruct strict binary evaluation with no subjective interpretation

#### Scenario: Counter-Example Scoring

- GIVEN an eval case marked as `counter_example: true` (safe code that should NOT be flagged)
- WHEN the scorer evaluates the result
- THEN the `no_false_positive` assertion SHALL pass only if the review does NOT flag the code as having the target vulnerability
- AND any other assertions (detected_bug, actionable_fix) SHALL be skipped for counter-examples

### Requirement: Aggregate Metrics

The system SHALL compute aggregate metrics from individual assertion results.

#### Scenario: Per-Skill × Model Metrics

- GIVEN all assertion results for a specific (skill, model) combination
- WHEN metrics are aggregated
- THEN the system SHALL compute:
  - `pass_rate`: proportion of assertions that passed (total passes / total assertions)
  - `detection_rate`: proportion of `detected_bug` assertions that passed
  - `false_positive_rate`: proportion of `no_false_positive` assertions that failed
  - `actionability_rate`: proportion of `actionable_fix` assertions that passed
  - `precision`: true positives / (true positives + false positives)
  - `recall`: true positives / (true positives + false negatives)
  - `f1`: harmonic mean of precision and recall
  - `mean_latency_ms`: average wall-clock time per eval case
  - `mean_tokens`: average total tokens (input + output) per eval case

#### Scenario: Confidence Intervals

- GIVEN a (skill, model) combination with N eval cases where N >= 5
- WHEN metrics are computed
- THEN the system SHALL report mean ± standard deviation for pass_rate, latency, and token counts
- AND it SHALL flag results with fewer than 5 eval cases as "low confidence"

### Requirement: Model Score Matrix

The system SHALL produce a model × skill score matrix.

#### Scenario: Matrix Generation

- GIVEN benchmark results for multiple (skill, model) combinations
- WHEN the matrix is generated
- THEN it SHALL be stored as `benchmark-results/<run-id>/model_scores.json`
- AND it SHALL contain a nested structure: `{model_id: {skill_name: {pass_rate, f1, detection_rate, false_positive_rate, mean_latency_ms, mean_tokens, eval_count}}}`

#### Scenario: Best Model Selection

- GIVEN a completed model score matrix
- WHEN best models are selected
- THEN the system SHALL identify the best model per skill based on F1 score (primary) with pass_rate as tiebreaker
- AND it SHALL update `skills/model-scores.yml` with the results
- AND it SHALL flag any skill where no model achieves F1 > 0.70 as "needs tuning"

### Requirement: Cost Estimation

The system SHALL estimate and track API costs.

#### Scenario: Per-Run Cost Tracking

- GIVEN token counts for each API call and a pricing table
- WHEN a benchmark run completes
- THEN the system SHALL compute estimated cost per (skill, model) combination
- AND it SHALL report total estimated cost for the entire run
- AND the pricing table SHALL be configurable via `scripts/benchmark/pricing.json`
