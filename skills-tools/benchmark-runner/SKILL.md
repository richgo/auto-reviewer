---
name: benchmark runner
description: >
  Auto-reviewer skill guidance for benchmark-runner.
---

# Benchmark Runner

## Purpose
Run SWE-bench-style benchmarks across all skills and models, producing a score matrix for comparison. Use this to evaluate model performance, identify skill difficulty, and recommend adversarial pairings.

## Running Benchmarks

### Basic Usage

```bash
MODELS="${MODELS:-gpt-4o-mini,gemini-2.0-flash}"

python scripts/benchmark/runner.py \
  --skills-dir skills/ \
  --evals-dir evals/ \
  --models "$MODELS" \
  --output benchmark-results/
```

This will:
1. Find all skill/eval pairs in `skills/*/SKILL.md` ↔ `evals/*.json`
2. Run each skill against its eval set using each model
3. Score results with binary assertions
4. Output `benchmark-results/model_scores.json`

### Automated Tuning Integration

Phase 3 workflows consume benchmark outputs during gated promotion:

- tune workflow screens candidates on failing subsets, then validates on full benchmark coverage.
- accepted results update `skills/model-scores.yml` snapshots.
- trajectory rows are appended to `tune-history/<skill>/<model>.jsonl` for auditability.

### Parameters

- **--skills-dir:** Directory containing skill markdown files (default: `skills/`)
- **--evals-dir:** Directory containing eval JSON files (default: `evals/`)
- **--models:** Comma-separated list of model identifiers
- **--output:** Output directory for results (default: `benchmark-results/`)

### Model Identifiers

Use model IDs available via Copilot SDK:

- Examples: `gpt-4.1`, `gpt-5-mini`, `gemini-2.0-flash`

Authenticate with GitHub so SDK calls can run:
- `gh auth login`
- or set `GITHUB_TOKEN`

## Output Format

### model_scores.json

```json
{
  "timestamp": "2025-03-21T12:00:00Z",
  "models": {
    "gpt-4o-mini": {
      "security-injection": {
        "pass_rate": 0.89,
        "f1": 0.89,
        "total_cases": 8,
        "last_run": "2025-03-21T12:05:00Z"
      },
      "security-auth": {
        "pass_rate": 0.92,
        "f1": 0.92,
        "total_cases": 6,
        "last_run": "2025-03-21T12:10:00Z"
      }
    },
    "gpt-4o": {
      "security-injection": {
        "pass_rate": 0.85,
        "f1": 0.85,
        "total_cases": 8,
        "last_run": "2025-03-21T12:15:00Z"
      }
    }
  },
  "skills": ["security-injection", "security-auth", ...]
}
```

### Metrics Explained

- **pass_rate:** Fraction of binary assertions that passed (0.0-1.0)
- **f1:** F1 score (approximated as pass_rate for balanced datasets)
- **total_cases:** Number of eval cases tested
- **last_run:** Timestamp of benchmark execution

## Generating Reports

After running the benchmark, generate a human-readable report:

```bash
python scripts/benchmark/reporter.py \
  benchmark-results/model_scores.json \
  --output benchmark-results/REPORT.md
```

### Report Sections

1. **Model Leaderboard** — Models ranked by average pass rate
2. **Skill Difficulty Ranking** — Skills ranked by average pass rate (hardest first)
3. **Detailed Scores** — Model × Skill matrix
4. **Adversarial Pairings** — Model combinations with complementary strengths
5. **Heatmap Data** — JSON for visualization

## Interpreting Results

### Model Comparison

**Use case: Choosing a production model**

1. Check overall leaderboard (average across all skills)
2. Prioritize skills critical to your use case (e.g., security for fintech)
3. Weigh cost vs. performance (e.g., GPT-4o may be cheaper than Claude Opus)

**Example:**
- Claude Sonnet: 87% avg, strong on security, weaker on performance
- GPT-4o: 84% avg, balanced across categories
- Gemini: 82% avg, strong on correctness, weaker on concurrency

**Decision:** Use Claude Sonnet for security-critical reviews, GPT-4o for general-purpose.

### Skill Difficulty

**Use case: Prioritizing skill improvements**

- **Very Hard (< 50%):** Skill needs redesign or more eval cases
- **Hard (50-70%):** Good candidate for autoresearch tuning
- **Medium (70-85%):** Acceptable, tune if production requires higher precision
- **Easy (> 85%):** Well-tuned, focus elsewhere

**Example:**
- `security-injection`: 89% avg → Easy (well-tuned)
- `concurrency`: 68% avg → Hard (needs tuning)
- `performance`: 52% avg → Very Hard (redesign or add evals)

### Adversarial Pairings

**Use case: Ensemble reviews for critical code**

The reporter identifies skills where models have different strengths. Use multiple models on these skills to catch different bug patterns.

**Example output:**
```
| Skill              | Variance | Best Model  | Worst Model |
|--------------------|----------|-------------|-------------|
| security-injection | 15%      | Claude      | Gemini      |
| concurrency        | 22%      | GPT-4o      | Claude      |
```

**Recommendation:** For concurrency reviews, run both GPT-4o and Claude, take union of findings.

## Typical Workflows

### Workflow 1: Model Selection

**Goal:** Pick the best model for production.

```bash
# Run benchmark on candidate models
MODELS="${MODELS:-gpt-4o-mini,gemini-2.0-flash,gpt-4.1}"

python scripts/benchmark/runner.py \
  --models "$MODELS"

# Generate report
python scripts/benchmark/reporter.py \
  benchmark-results/model_scores.json \
  --output REPORT.md

# Review leaderboard and cost tradeoffs
cat REPORT.md
```

### Workflow 2: Skill Health Check

**Goal:** Find weak skills that need improvement.

```bash
# Run benchmark with your production model
MODEL="${MODEL:-gpt-4o-mini}"

python scripts/benchmark/runner.py \
  --models "$MODEL"

# Generate report
python scripts/benchmark/reporter.py \
  benchmark-results/model_scores.json

# Identify skills below 85% pass rate
cat REPORT.md | grep "Hard\|Very Hard"

# Tune weak skills
python scripts/skill_machine/autoresearch.py \
  --skill skills/concurrency/SKILL.md \
  --evals evals/concurrency.json \
  --max-iterations 30
```

### Workflow 3: Ensemble Strategy

**Goal:** Use multiple models to maximize coverage.

```bash
# Run benchmark on all available models
MODELS="${MODELS:-gpt-4o-mini,gemini-2.0-flash,gpt-4.1}"

python scripts/benchmark/runner.py \
  --models "$MODELS"

# Generate report
python scripts/benchmark/reporter.py \
  benchmark-results/model_scores.json

# Review adversarial pairings section
# Identify high-variance skills

# Configure production to use ensemble on those skills:
# - security-injection → gpt-4.1 + gpt-4o
# - concurrency → gpt-4o + Gemini
```

### Workflow 4: Benchmark One Skill Across Multiple Models

**Goal:** Compare model performance for a single skill without running the full matrix.

```bash
# 1) Choose skill + model list
SKILL=security-injection
MODELS="${MODELS:-gpt-4o-mini,gemini-2.0-flash,gpt-4.1}"

# 2) Create an isolated benchmark workspace
RUN_DIR=".tmp-benchmark-${SKILL}"
mkdir -p "$RUN_DIR/skills/${SKILL}" "$RUN_DIR/evals" "$RUN_DIR/output"

# 3) Copy only the target skill and matching eval set
cp "skills/${SKILL}/SKILL.md" "$RUN_DIR/skills/${SKILL}/SKILL.md"
cp "evals/${SKILL}.json" "$RUN_DIR/evals/${SKILL}.json"

# 4) Run benchmark (single skill x multiple models)
python scripts/benchmark/runner.py \
  --skills-dir "$RUN_DIR/skills" \
  --evals-dir "$RUN_DIR/evals" \
  --models "$MODELS" \
  --output "$RUN_DIR/output"

# 5) Generate report
python scripts/benchmark/reporter.py \
  "$RUN_DIR/output/model_scores.json" \
  --output "$RUN_DIR/output/REPORT.md"

# 6) Review results
cat "$RUN_DIR/output/REPORT.md"
```

Expected result:
- `model_scores.json` contains exactly one skill in `skills[]`.
- Each model has one score entry for that skill under `models.<model>.<skill>`.
- `REPORT.md` ranks models by average pass rate for that single skill (effectively a direct per-skill comparison).

Optional cleanup:

```bash
rm -rf "$RUN_DIR"
```

## Best Practices

### Benchmark Frequency
- **Daily:** If actively tuning skills (to track improvements)
- **Weekly:** For stable production (to catch model drift)
- **On-demand:** Before major releases or model upgrades

### Versioning
- Commit `model_scores.json` to version control
- Tag with model versions and skill commit hashes
- Track score trends over time

### Cost Management
- Benchmarking is expensive (N skills × M models × K eval cases × 2 LLM calls each)
- Start with 1 model to validate, expand to multi-model later
- Use cheaper models (GPT-4o-mini, Gemini Flash) for rapid iteration

### Adding New Skills
- Create eval JSON with at least 5 cases
- Add to `evals/` directory matching skill name
- Re-run benchmark to establish baseline
- Tune if pass rate < 85%

## Troubleshooting

### "No skill/eval pairs found"
- Check that eval JSON filename matches skill filename (e.g., `security-injection.md` ↔ `security-injection.json`)
- Ensure skills are in `skills/` subdirectory
- Verify JSON is valid with `cat evals/security-injection.json | jq`

### "API rate limit exceeded"
- Add delays between calls in `runner.py` (not implemented yet, manual throttling)
- Use fewer models or skills initially
- Spread benchmark across multiple runs

### "Scores don't match production"
- Check that benchmark uses same model as production
- Verify eval cases match production failure patterns
- Add more diverse eval cases

## Related
- `skills-tools/skill-optimizer/SKILL.md` — Tune individual skills
- `skills-tools/local-calibration/SKILL.md` — Adapt skills to repo conventions
