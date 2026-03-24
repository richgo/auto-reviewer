# Tuning & Eval Infrastructure

Autoresearch-based skill optimization and SWE-bench-style benchmarking for code review skills.

## Overview

This infrastructure implements an autoresearch loop (inspired by [Claude Code autoresearch](https://www.mindstudio.ai/blog/claude-code-autoresearch-self-improving-skills) and [Karpathy's autoresearch](https://github.com/karpathy/autoresearch)) for self-tuning code review skills.

**Core concept:**
1. Run a skill against eval cases (code samples with expected findings)
2. Score results with binary assertions (detected_bug, no_false_positive, etc.)
3. Analyze failure patterns
4. Mutate the skill to address failures (add heuristics, refine instructions, etc.)
5. Re-evaluate and keep improvements
6. Repeat 30-50 cycles

## Quick Start

### Prerequisites

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Authenticate GitHub CLI so Copilot SDK can select models
gh auth login
# Optional override:
# export GITHUB_TOKEN=ghp_...
```

### Tune a Single Skill

```bash
python scripts/tune/autoresearch.py \
  --skill skills/security-injection/SKILL.md \
  --evals evals/security-injection.json \
  --model gpt-4o-mini \
  --max-iterations 30 \
  --target-pass-rate 0.95 \
  --output skills/security-injection/SKILL.md \
  --log tune-logs/security-injection.jsonl
```

### Run Full Benchmark

```bash
python scripts/benchmark/runner.py \
  --skills-dir skills/ \
  --evals-dir evals/ \
  --models gpt-4o-mini,gemini-2.0-flash \
  --output benchmark-results/
```

### Benchmark One Skill Across Multiple Models

```bash
SKILL=security-injection
MODELS=gpt-4o-mini,gemini-2.0-flash
RUN_DIR=".tmp-benchmark-${SKILL}"

mkdir -p "$RUN_DIR/skills/${SKILL}" "$RUN_DIR/evals" "$RUN_DIR/output"
cp "skills/${SKILL}/SKILL.md" "$RUN_DIR/skills/${SKILL}/SKILL.md"
cp "evals/${SKILL}.json" "$RUN_DIR/evals/${SKILL}.json"

python scripts/benchmark/runner.py \
  --skills-dir "$RUN_DIR/skills" \
  --evals-dir "$RUN_DIR/evals" \
  --models "$MODELS" \
  --output "$RUN_DIR/output"

python scripts/benchmark/reporter.py \
  "$RUN_DIR/output/model_scores.json" \
  --output "$RUN_DIR/output/REPORT.md"

cat "$RUN_DIR/output/REPORT.md"
# optional cleanup: rm -rf "$RUN_DIR"
```

For a more detailed walkthrough, see `skills-tools/benchmark-runner/SKILL.md` (Workflow 4).

### Generate Report

```bash
python scripts/benchmark/reporter.py \
  benchmark-results/model_scores.json \
  --output benchmark-results/REPORT.md
```

## Directory Structure

```
scripts/
├── tune/
│   ├── __init__.py
│   ├── llm_client.py          # LLM interface backed by Copilot SDK
│   ├── scorer.py              # Binary assertion evaluator
│   ├── mutator.py             # Skill mutation strategies
│   └── autoresearch.py        # Main optimization loop (CLI)
├── benchmark/
│   ├── __init__.py
│   ├── copilot_client.py      # Copilot SDK wrapper
│   ├── runner.py              # SWE-bench-style benchmark harness (CLI)
│   └── reporter.py            # Markdown report generator (CLI)
└── requirements.txt           # httpx, pyyaml, rich, github-copilot-sdk

evals/
├── security-injection.json    # Eval cases for SQL injection, XSS, command injection
├── security-auth.json         # Auth bypass, CSRF, password storage
├── security-data-protection.json
├── security-network.json      # SSRF, open redirect, CORS
├── concurrency.json           # Race conditions, deadlocks, async misuse
├── correctness.json           # Null deref, off-by-one, logic errors
└── performance.json           # N+1 queries, memory leaks, algorithmic complexity

skills/
├── security-injection/
│   └── SKILL.md
├── security-auth/
│   └── SKILL.md
└── benchmark-runner/
    └── SKILL.md

tune-logs/                     # JSONL logs from autoresearch runs
benchmark-results/             # Benchmark outputs (model_scores.json, REPORT.md)
```

## Modules

### `tune/llm_client.py`

Unified LLM client backed by the **GitHub Copilot SDK**.
Model selection happens via `--model`/`--models` strings passed to the SDK.

**Usage:**
```python
from tune.llm_client import LLMClient

llm = LLMClient()
response = llm.complete("Review this code...", system="You are a reviewer.")
```

### `tune/scorer.py`

Binary assertion scorer that evaluates review quality using LLM.

**Assertion types:**
- `detected_bug`: Did the review catch the vulnerability?
- `no_false_positive`: Is the finding legitimate (not a false alarm)?
- `actionable_fix`: Does the review suggest a concrete fix?
- `correct_severity`: Is the severity rating appropriate?
- `evidence_cited`: Does the review cite code evidence?

**Usage:**
```python
from tune.scorer import Scorer

scorer = Scorer()
score = scorer.score_review(review_output, eval_case)
print(score.pass_rate)  # 0.0-1.0
```

### `tune/mutator.py`

Skill mutation strategies:
1. **add_detection_heuristic** — Add pattern to catch missed bugs
2. **add_counter_example** — Add safe code example to avoid false positives
3. **refine_instruction** — Clarify confusing wording
4. **add_platform_guidance** — Add platform-specific rules
5. **remove_noise** — Remove unhelpful instructions

**Usage:**
```python
from tune.mutator import Mutator

mutator = Mutator()
patterns = mutator.analyze_failures([(eval_case, score), ...])
mutation = mutator.generate_mutation(skill_content, patterns, "add_detection_heuristic")
```

### `tune/autoresearch.py`

Main optimization loop. CLI tool.

**Flow:**
1. Load skill and evals
2. Evaluate current skill (run against eval cases, score with assertions)
3. For N iterations:
   - Analyze failure patterns
   - Select mutation strategy (priority: false negatives → false positives → fixes)
   - Generate mutation
   - Evaluate mutated skill
   - Accept if improved, reject otherwise
4. Save best skill + log

**CLI:**
```bash
python scripts/tune/autoresearch.py --help
```

### `benchmark/runner.py`

SWE-bench-style benchmark harness. Runs all skills against their eval sets, produces model × skill score matrix.

**Output:** `model_scores.json`

**CLI:**
```bash
python scripts/benchmark/runner.py --help
```

### `benchmark/reporter.py`

Generates human-readable markdown report from benchmark results.

**Sections:**
- Model leaderboard
- Skill difficulty ranking
- Detailed scores (matrix)
- Adversarial pairing recommendations
- Heatmap data (JSON)

**CLI:**
```bash
python scripts/benchmark/reporter.py benchmark-results/model_scores.json
```

## Eval Format

Eval JSON structure:

```json
{
  "description": "Eval cases for ...",
  "skill": "security-injection",
  "cases": [
    {
      "id": "sql-injection-001",
      "name": "Python f-string SQL injection",
      "description": "SQL query built with f-string interpolation",
      "code_snippet": "def get_user(username):\n    query = f\"SELECT * FROM users WHERE username = '{username}'\"\n    cursor.execute(query)",
      "language": "python",
      "expected_findings": [
        {
          "type": "sql-injection",
          "line": 2,
          "description_contains": ["SQL injection", "f-string", "parameterized"]
        }
      ],
      "assertions": {
        "detected_bug": true,
        "correct_severity": true,
        "actionable_fix": true,
        "evidence_cited": true
      }
    },
    {
      "id": "safe-sql-001",
      "name": "Safe parameterized query",
      "description": "Should NOT be flagged",
      "code_snippet": "cursor.execute('SELECT * FROM users WHERE username = %s', (username,))",
      "language": "python",
      "expected_findings": [],
      "assertions": {
        "no_false_positive": true
      }
    }
  ]
}
```

**Guidelines:**
- 5-8 cases per skill (enough signal for tuning)
- Mix true positives (buggy code) and counter-examples (safe code)
- Use `assertions` to define pass/fail criteria
- Pull real-world examples from CVEs, production incidents, and skill-linked eval archives

## Typical Workflows

### Workflow 1: Optimize a New Skill

```bash
# 1. Create skill markdown
vi skills/my-new-skill/SKILL.md

# 2. Create eval cases
vi evals/my-new-skill.json  # 5-8 cases

# 3. Baseline evaluation
python scripts/tune/autoresearch.py \
  --skill skills/my-new-skill/SKILL.md \
  --evals evals/my-new-skill.json \
  --max-iterations 1
# Output: Initial pass rate: 65%

# 4. Optimize
python scripts/tune/autoresearch.py \
  --skill skills/my-new-skill/SKILL.md \
  --evals evals/my-new-skill.json \
  --max-iterations 30 \
  --target-pass-rate 0.90
# Output: Target 90% reached! (iteration 22)

# 5. Review changes
git diff skills/my-new-skill/SKILL.md

# 6. Commit
git add skills/my-new-skill/SKILL.md evals/my-new-skill.json
git commit -m "Add my-new-skill (90% pass rate)"
```

### Workflow 2: Compare Models

```bash
# Run benchmark
python scripts/benchmark/runner.py \
  --models gpt-4o-mini,gemini-2.0-flash

# Generate report
python scripts/benchmark/reporter.py \
  benchmark-results/model_scores.json \
  --output REPORT.md

# Review leaderboard
cat REPORT.md

# Decision: Use Claude for security, GPT-4o for general-purpose
```

### Workflow 3: Fix Production False Positives

```bash
# 1. Extract false positive from production logs
grep "FALSE_POSITIVE" logs/*.json | jq -r '.code_snippet' > fp.txt

# 2. Add to local eval set
cat > .skill-machine/local-evals.json <<EOF
{
  "cases": [
    {
      "id": "local-fp-001",
      "code_snippet": "$(cat fp.txt)",
      "expected_findings": [],
      "assertions": {"no_false_positive": true}
    }
  ]
}
EOF

# 3. Merge with global evals
jq -s '.[0].cases + .[1].cases | {cases: .}' \
  evals/security-injection.json \
  .skill-machine/local-evals.json > merged.json

# 4. Re-tune
python scripts/tune/autoresearch.py \
  --skill skills/security-injection/SKILL.md \
  --evals merged.json \
  --max-iterations 10 \
  --output .skill-machine/security-injection-local.md

# 5. Deploy local skill
# (configure skill-machine to use .skill-machine/security-injection-local.md)
```

## Best Practices

### Eval Design
- **Real-world bugs:** Pull from CVEs, production incidents
- **Diversity:** Cover different languages, frameworks, edge cases
- **Balance:** Mix true positives and counter-examples
- **Clarity:** Make expected findings unambiguous

### Tuning
- **Version control:** Commit before tuning, diff after
- **Incremental:** Tune one skill at a time
- **A/B test:** Compare old vs. new in production
- **Target:** 85-95% pass rate (higher = overfitting risk)

### Model Selection
- **Production parity:** Tune with the model you'll use in production
- **Cost:** GPT-4o cheaper than Claude Opus, balance vs. performance
- **Ensemble:** Use multiple models on high-variance skills

### Maintenance
- **Re-tune periodically:** When new patterns emerge or models update
- **Monitor production:** Track false positive/negative rates
- **Contribute back:** Add generalizable patterns to global evals

## Troubleshooting

### "Pass rate not improving"
- Check if eval cases are realistic (not too obscure)
- Add more eval cases (need 5+ for signal)
- Review skill manually (may need redesign)

### "Too many false positives in production"
- Add counter-examples to evals
- Re-tune with stricter target (0.95+)
- Use local calibration for repo-specific patterns

### "API rate limit exceeded"
- Add delays in runner.py (manual throttling for now)
- Run on fewer models/skills initially
- Spread benchmark across multiple runs

## References

- [Claude Code Autoresearch](https://www.mindstudio.ai/blog/claude-code-autoresearch-self-improving-skills)
- [Karpathy Autoresearch](https://github.com/karpathy/autoresearch)
- SWE-bench benchmark methodology
- OWASP Code Review Guide

## Contributing

### Adding New Eval Cases

1. Add cases to existing eval JSON (e.g., `evals/security-injection.json`)
2. Follow format: `id`, `code_snippet`, `expected_findings`, `assertions`
3. Run benchmark to establish baseline
4. Re-tune skill if pass rate drops

### Adding New Skills

1. Create `skills/<skill>/SKILL.md`
2. Create eval JSON in `evals/` (matching filename)
3. Run baseline benchmark
4. Tune to 85%+ pass rate
5. Document in the corresponding `skills/<skill>/SKILL.md` and relevant skill-linked eval metadata

### Improving Infrastructure

Open to contributions:
- Additional mutation strategies
- Better failure pattern analysis
- Cost optimization (caching, batching)
- Visualization tools for heatmaps
- Integration with CI/CD

## License

(Match repo license)
