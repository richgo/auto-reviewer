# Reporting Specification Delta

## ADDED Requirements

### Requirement: Markdown Report Generation

The system SHALL generate human-readable markdown reports from benchmark results.

#### Scenario: Model Leaderboard

- GIVEN a completed model score matrix
- WHEN the reporter generates a leaderboard
- THEN it SHALL produce a markdown table ranking models by overall F1 score
- AND it SHALL include per-category breakdowns (security, concurrency, correctness, etc.)
- AND it SHALL highlight the best model per category in bold

#### Scenario: Skill Difficulty Ranking

- GIVEN aggregate metrics across all models for each skill
- WHEN the reporter generates a difficulty ranking
- THEN it SHALL rank skills from hardest (lowest average F1 across models) to easiest
- AND it SHALL identify "unsolved" skills where no model achieves F1 > 0.70
- AND it SHALL identify "trivial" skills where all models achieve F1 > 0.95

#### Scenario: Adversarial Pairing Recommendations

- GIVEN per-model assertion-level results for each skill
- WHEN the reporter analyzes complementarity
- THEN it SHALL identify model pairs where each model catches bugs the other misses
- AND it SHALL recommend adversarial pairings per skill based on complementary detection patterns
- AND it SHALL output this as a `recommended_pairings` section in the report

### Requirement: Heatmap Data Export

The system SHALL export data suitable for heatmap visualization.

#### Scenario: Model × Skill Heatmap

- GIVEN a completed model score matrix
- WHEN heatmap data is exported
- THEN it SHALL produce a CSV file at `benchmark-results/<run-id>/heatmap.csv`
- AND each row SHALL be a model, each column a skill, and cell values SHALL be F1 scores
- AND cells SHALL be color-coded in the markdown report using emoji: 🟢 (F1 ≥ 0.90), 🟡 (0.70-0.89), 🔴 (< 0.70)

### Requirement: Regression Detection

The system SHALL detect performance regressions between benchmark runs.

#### Scenario: Cross-Run Comparison

- GIVEN a current benchmark run and a previous benchmark run
- WHEN the reporter compares results
- THEN it SHALL flag any (skill, model) combination where F1 dropped by more than 0.05
- AND it SHALL flag any combination where latency increased by more than 50%
- AND it SHALL produce a `regressions` section in the report

### Requirement: CI Integration

The system SHALL support integration with CI/CD pipelines.

#### Scenario: GitHub Actions Output

- GIVEN the reporter runs with `--format github`
- WHEN the report is generated
- THEN it SHALL output results as GitHub Actions step summary markdown
- AND it SHALL set output variables for overall pass rate and regression count
- AND it SHALL exit with code 1 if any regression exceeds threshold

#### Scenario: JSON Export

- GIVEN the reporter runs with `--format json`
- WHEN the report is generated
- THEN it SHALL output the full model score matrix, leaderboard, and recommendations as a single JSON document
- AND it SHALL be suitable for consumption by downstream tools (e.g., the Composer Agent for model selection)
