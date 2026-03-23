---
name: skill-optimizer
description: >
  Auto-reviewer skill guidance for skill-optimizer.
---

# Skill Optimizer

## Purpose
Guide for using the autoresearch tuning loop to optimize code review skills. This skill explains when to tune, what to look for, and how to interpret results.

## When to Tune a Skill

**Trigger conditions:**
- New skill created (baseline optimization before deployment)
- Eval pass rate below 85% (indicates detection gaps or false positives)
- Production false positive reports (real-world misfire)
- New vulnerability patterns discovered (need to expand detection)
- Major framework/language updates (patterns may have changed)

**Don't tune if:**
- Pass rate already above 95% (diminishing returns)
- Less than 5 eval cases (insufficient signal)
- Skill is platform-specific but evals are generic (fix evals first)

## Running the Autoresearch Loop

### Basic Usage

```bash
python scripts/tune/autoresearch.py \
  --skill skills/security-injection/SKILL.md \
  --evals evals/security-injection.json \
  --model claude-sonnet-4-20250514 \
  --max-iterations 30 \
  --target-pass-rate 0.95 \
  --output skills/security-injection/SKILL.md \
  --log tune-logs/security-injection.jsonl
```

### Scheduled Automation (Phase 3)

Autoresearch runs are now expected to execute via GitHub workflows:

- `.github/workflows/autoresearch-tuning.yml` handles weekly + dispatch + path-triggered runs.
- `.github/workflows/autoresearch-promote.yml` handles branch-first promotion PR creation.
- `tune-history/<skill>/<model>.jsonl` stores append-only decision history per pair.

Promotion is gate-driven. Candidates must satisfy minimum F1 improvement and maximum FPR regression constraints from `scripts/tune/config.yaml`.
Large diffs are labeled for manual review before merge.

### Parameters Explained

- **--skill:** Path to skill markdown file to optimize
- **--evals:** Path to eval JSON with test cases and assertions
- **--model:** LLM model to use for skill execution and mutation (use same model as production)
- **--max-iterations:** Maximum optimization cycles (30-50 recommended)
- **--target-pass-rate:** Stop when this pass rate is reached (0.90-0.95 recommended)
- **--output:** Where to save optimized skill (can overwrite input)
- **--log:** JSONL log of each iteration (for analysis)
- **--history-file:** Append-only trajectory file for accepted/rejected decisions
- **--dry-run:** Build/score the plan without persisting skill changes

### Typical Workflow

1. **Baseline evaluation:** Run with `--max-iterations 1` to see current pass rate
2. **Quick tune:** Run 10-15 iterations to catch low-hanging fruit
3. **Full optimization:** Run 30-50 iterations for target pass rate
4. **Review changes:** Diff the optimized skill against original
5. **Test in production:** Deploy and monitor false positive rate
6. **Iterate:** Add new eval cases for production failures, re-tune

## Interpreting Results

### Tuning Log Analysis

The JSONL log contains one entry per iteration:

```json
{
  "iteration": 5,
  "timestamp": "2025-03-21T10:30:00Z",
  "pass_rate": 0.78,
  "mutation_strategy": "add_detection_heuristic",
  "mutation_description": "Added heuristic to catch 3 missed bugs",
  "accepted": true,
  "failure_patterns": {
    "total_cases": 8,
    "failed_cases": 2,
    "common_failures": {
      "detected_bug": 2,
      "actionable_fix": 1
    },
    "false_negative_count": 2,
    "false_positive_count": 0
  }
}
```

**Key metrics:**
- **pass_rate:** Fraction of assertions passing (0.0-1.0)
- **accepted:** Was this mutation kept? (true if improved score)
- **false_negative_count:** Bugs missed by skill (priority fix)
- **false_positive_count:** Safe code flagged as buggy (critical fix)
- **common_failures:** Which assertions fail most

### Mutation Strategies

The tuner uses these strategies based on failure patterns:

1. **add_detection_heuristic** — Adds new pattern to catch missed bugs (false negatives)
2. **add_counter_example** — Adds example of safe code to avoid false positives
3. **refine_instruction** — Clarifies confusing wording that leads to errors
4. **add_platform_guidance** — Adds platform-specific detection rules
5. **remove_noise** — Removes verbose/unhelpful instructions

**Strategy selection priority:**
- False negatives → add_detection_heuristic
- False positives → add_counter_example
- Missing fix suggestions → refine_instruction
- Otherwise → rotate through platform_guidance and remove_noise

### Warning Signs

**Optimization stalling:**
- Pass rate stuck below target for 10+ iterations
- **Cause:** Eval cases may be too hard, or skill approach is fundamentally wrong
- **Fix:** Review failed cases manually, consider redesigning skill

**Overfitting:**
- Pass rate jumps to 100% quickly, but production has high false positives
- **Cause:** Skill memorizing eval patterns without generalizing
- **Fix:** Add diverse eval cases, add counter-examples

**Regression:**
- Pass rate drops after accepted mutation
- **Cause:** Mutation added noise or conflicting guidance
- **Fix:** Revert to last good version, try different strategy

## Best Practices

### Eval Case Design
- **5-8 cases minimum:** Enough signal to detect patterns
- **Balance true/false positives:** Include counter-examples
- **Diverse patterns:** Cover different languages, frameworks, edge cases
- **Real-world bugs:** Pull from actual CVEs, production incidents

### Tuning Hygiene
- **Version control:** Commit before tuning, diff after
- **A/B test:** Keep old skill version, compare production metrics
- **Incremental:** Tune one concern at a time, don't batch
- **Log retention:** Keep tuning logs for analysis

### Model Selection
- **Production parity:** Tune with the same model used in production
- **Multiple models:** If using ensemble, tune separately for each
- **Temperature:** Use temperature=0.3 for deterministic review (configured in autoresearch.py)

## Example Session

```bash
# 1. Check current skill performance
python scripts/tune/autoresearch.py \
  --skill skills/security-injection/SKILL.md \
  --evals evals/security-injection.json \
  --max-iterations 1
# Output: Initial pass rate: 72.5%

# 2. Run optimization
python scripts/tune/autoresearch.py \
  --skill skills/security-injection/SKILL.md \
  --evals evals/security-injection.json \
  --max-iterations 30 \
  --target-pass-rate 0.90

# Output after 18 iterations:
# Target 90.0% reached!
# Best pass rate: 91.2%

# 3. Review changes
git diff skills/security-injection/SKILL.md

# 4. Analyze log
cat tune-logs/security-injection.jsonl | jq '.mutation_strategy' | sort | uniq -c
# 8 add_detection_heuristic
# 6 add_counter_example
# 4 refine_instruction

# 5. Commit optimized skill
git add skills/security-injection/SKILL.md
git commit -m "Tune security-injection skill to 91% pass rate"
```

## Troubleshooting

### "Pass rate not improving"
- Check if eval cases are realistic (not too obscure)
- Add more eval cases for better signal
- Try different mutation strategies manually
- Consider rewriting skill from scratch

### "Too many false positives in production"
- Add counter-examples to evals for known false positives
- Re-tune with `--target-pass-rate 0.95` (stricter)
- Review production logs, add failing cases to evals

### "Skill keeps flip-flopping"
- Lower temperature in llm_client.py (more deterministic)
- Reduce max-iterations (may be overtuning)
- Check for conflicting guidance in skill

## Related
- `skills-tools/benchmark-runner/SKILL.md` — Compare skills across models
- `skills-tools/local-calibration/SKILL.md` — Adapt skills to repo-specific conventions
