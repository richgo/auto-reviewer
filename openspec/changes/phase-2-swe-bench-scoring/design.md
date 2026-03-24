# Design: Phase 2 — SWE-bench-Style Scoring

## Overview

This design implements a comprehensive benchmark harness to evaluate model × skill performance on real-world code review scenarios, inspired by SWE-bench's approach. The system uses the **GitHub Copilot SDK** as a unified LLM client, providing access to all models through a single interface. The harness runs skills against eval datasets, scores outputs using an LLM-as-judge approach with binary assertions, and generates performance matrices comparing models across skills. This enables data-driven model selection per skill and category.

## Architecture

### Components Affected

- **`scripts/benchmark/runner.py`** — Extend existing runner to use Copilot SDK instead of direct API calls; add caching, retry logic, streaming latency measurement
- **`scripts/benchmark/scorer.py`** — New module for LLM-as-judge evaluation of binary assertions
- **`scripts/benchmark/reporter.py`** — Extend existing reporter with heatmap generation, regression detection, adversarial pairing recommendations
- **`scripts/benchmark/__init__.py`** — Shared utilities (content hashing, result schemas)
- **`evals/*.json`** — Update assertion format to match new binary evaluation schema (detected_bug, no_false_positive, actionable_fix, correct_severity, evidence_cited)
- **`skills/model-scores.yml`** — Update schema to store best model per skill with confidence metrics

### New Components

- **`scripts/benchmark/copilot_client.py`** — Thin wrapper around `github-copilot-sdk` for session management, model discovery, and streaming events
- **`scripts/benchmark/judge.py`** — LLM-as-judge prompts and evaluation logic for assertion scoring
- **`scripts/benchmark/cache.py`** — Content-addressable cache for benchmark results (keyed by skill hash + eval hash + model)
- **`scripts/benchmark/pricing.json`** — Configurable pricing table for cost estimation per model
- **`benchmark-results/<run-id>/`** — Output directory structure:
  - `metadata.json` — Run configuration, git commit, timestamp, models list
  - `raw_results.jsonl` — One line per (skill × model × eval case) with raw output, latency, tokens
  - `assertion_results.jsonl` — One line per assertion evaluation with pass/fail and justification
  - `model_scores.json` — Aggregated metrics per (model × skill) combination
  - `heatmap.csv` — Model × skill matrix with F1 scores
  - `report.md` — Human-readable report with leaderboard, difficulty ranking, adversarial pairings

## Technical Decisions

### Decision: Use GitHub Copilot SDK as Unified LLM Client

**Chosen:** Integrate `github-copilot-sdk` Python package via thin wrapper

**Alternatives considered:**
- Build separate HTTP clients for each provider (OpenAI, Anthropic, Google) — rejected because it requires maintaining multiple API integrations, handling auth/retries separately, and managing rate limits per-provider
- Use LangChain or LiteLLM — rejected because they add heavy dependencies and abstractions when we need low-level control over streaming, custom tools, and session management

**Rationale:** The Copilot SDK provides a single interface to all major models (Claude, GPT, Gemini, DeepSeek, etc.) with built-in authentication, streaming events for latency measurement, and custom tool support for structured output. It also supports BYOK for high-volume benchmarking. The SDK is in technical preview, so we wrap it in a thin abstraction layer (`copilot_client.py`) to isolate API changes.

### Decision: LLM-as-Judge for Assertion Evaluation

**Chosen:** Use a cheaper/faster judge model (default `gpt-4o-mini`) to evaluate binary assertions on review outputs

**Alternatives considered:**
- String matching/regex on review output — rejected because reviews are natural language and patterns vary widely (e.g., "SQL injection" vs "injectable query" vs "parameterization missing")
- Embedding similarity to expected findings — rejected because it doesn't handle negation well (false positives) and requires maintaining embeddings for all findings
- Human annotation — rejected because it doesn't scale to 40+ skills × 10+ models × 200+ eval cases per run

**Rationale:** LLM-as-judge provides flexible, semantic evaluation while keeping costs low by using a fast model. We structure judge prompts to demand binary pass/fail with a one-line justification, avoiding subjective scoring. Judge results are cached alongside raw outputs for reproducibility.

### Decision: Content-Addressable Caching with Skip Logic

**Chosen:** Cache results keyed by `sha256(skill_content + eval_content + model_id)`, skip execution if hash matches and result exists

**Alternatives considered:**
- No caching, re-run everything — rejected because benchmark runs are expensive (~$50-100 per full run) and time-consuming (2-3 hours)
- Cache by filename only — rejected because skills and evals evolve; cache must invalidate when content changes
- Timestamp-based cache invalidation — rejected because it's not deterministic and breaks reproducibility

**Rationale:** Content-addressable caching ensures reproducibility while avoiding redundant API calls. If a skill or eval changes, the hash changes and the result is re-executed. This supports incremental benchmarking (e.g., adding one new model to an existing run).

### Decision: JSONL for Append-Friendly Result Storage

**Chosen:** Store raw results and assertion results as JSONL (one JSON object per line)

**Alternatives considered:**
- Single JSON array — rejected because it requires loading/rewriting the entire file for each result, risking corruption on crash
- SQLite database — rejected because it adds complexity and isn't as portable for version control/diffing
- CSV — rejected because it doesn't handle nested structures (findings, assertions) well

**Rationale:** JSONL is append-only, crash-safe, and easy to stream/parse. Each line is self-contained, so partial results are still usable. It's also git-friendly for tracking historical runs.

### Decision: Separate Counter-Example Handling

**Chosen:** Eval cases can be marked `counter_example: true` (safe code); only `no_false_positive` assertion is evaluated

**Alternatives considered:**
- Treat counter-examples as regular cases with inverted assertions — rejected because it complicates scoring logic and makes reports confusing
- Separate counter-example files — rejected because it doubles the number of eval files and makes pairing harder

**Rationale:** Explicit `counter_example` flag keeps data in one place and makes scoring logic clear: if `counter_example == true`, check that the model does NOT flag the code. If it does, `no_false_positive` fails.

### Decision: Streaming for Time-to-First-Token (TTFT) Measurement

**Chosen:** Enable streaming on Copilot SDK sessions, capture `assistant.message_delta` events for TTFT, `session.idle` for total latency

**Alternatives considered:**
- Measure total latency only — rejected because TTFT is critical for perceived responsiveness in interactive review workflows
- Poll for partial responses — rejected because it adds latency overhead and isn't supported by all providers

**Rationale:** TTFT is a key UX metric. Streaming is natively supported by the Copilot SDK, so we get accurate measurements without overhead.

## Data Flow

### High-Level Pipeline

```
┌─────────────────┐
│  Skill Discovery│
│  (skills/*.md)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│ Eval Matching   │────▶│ Copilot SDK     │
│ (evals/*.json)  │     │ Session Create  │
└─────────────────┘     └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ Execute Review  │
                        │ (skill + code)  │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ Raw Result      │
                        │ (output +       │
                        │  latency +      │
                        │  tokens)        │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ LLM-as-Judge    │
                        │ (assertions)    │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ Aggregator      │
                        │ (model scores)  │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ Reporter        │
                        │ (markdown +     │
                        │  heatmap)       │
                        └─────────────────┘
```

### Detailed Execution Flow

1. **Discovery Phase**
   - Scan `skills/concerns/` for SKILL.md files
   - Match each skill to its eval file in `evals/<skill-name>.json`
   - Load target models from CLI args or discover via `client.list_models()`

2. **Cache Check Phase**
   - For each (skill × model × eval case) combination:
     - Compute `content_hash = sha256(skill_body + eval_code + model_id)`
     - Check if `benchmark-results/.cache/<content_hash>.json` exists
     - If exists and not stale (< 7 days), skip execution and load cached result
     - If not, queue for execution

3. **Execution Phase** (parallelized with configurable concurrency)
   - Create Copilot SDK session: `session = client.create_session(model=model_id, system_message=skill_body)`
   - Send eval code snippet: `response = await session.send_and_wait({"prompt": code_snippet})`
   - Capture streaming events:
     - `assistant.message_start` → start timer
     - `assistant.message_delta` → record TTFT on first delta
     - `session.idle` → record total latency
   - Extract token counts from `response.usage`
   - Store raw result to `benchmark-results/<run-id>/raw_results.jsonl`
   - Write to cache: `benchmark-results/.cache/<content_hash>.json`

4. **Scoring Phase**
   - For each raw result, load corresponding eval case's assertions
   - For each assertion (detected_bug, no_false_positive, actionable_fix, correct_severity, evidence_cited):
     - Send judge prompt to `gpt-4o-mini` (or configured judge model)
     - Parse judge response for pass/fail + justification
     - Store to `benchmark-results/<run-id>/assertion_results.jsonl`

5. **Aggregation Phase**
   - Group assertion results by (model × skill)
   - Compute metrics:
     - `pass_rate = total_passes / total_assertions`
     - `detection_rate = detected_bug_passes / detected_bug_total`
     - `false_positive_rate = no_false_positive_fails / no_false_positive_total`
     - `actionability_rate = actionable_fix_passes / actionable_fix_total`
     - `precision = true_positives / (true_positives + false_positives)`
     - `recall = true_positives / (true_positives + false_negatives)`
     - `f1 = 2 * (precision * recall) / (precision + recall)`
     - `mean_latency_ms`, `mean_tokens`, `confidence_interval` (if N >= 5)
   - Write to `benchmark-results/<run-id>/model_scores.json`

6. **Reporting Phase**
   - Load `model_scores.json`
   - Generate leaderboard (models ranked by F1, grouped by category)
   - Generate difficulty ranking (skills ranked by average F1 across models)
   - Generate heatmap CSV (model × skill matrix with F1 values)
   - Detect regressions (if previous run exists, compare F1/latency)
   - Recommend adversarial pairings (models with complementary detection patterns)
   - Write to `benchmark-results/<run-id>/report.md`

## API Changes

**No breaking API changes to existing review pipeline.** This is a new scoring/benchmarking capability.

### New CLI Interface

```bash
# Full benchmark run
python scripts/benchmark/runner.py \
  --models claude-sonnet-4-20250514,gpt-4o,gemini-2.5-pro \
  --output benchmark-results/

# Single skill benchmark
python scripts/benchmark/runner.py \
  --skill skills/concerns/security-injection \
  --models claude-sonnet-4-20250514

# Discover and run all available Copilot models
python scripts/benchmark/runner.py --all-models

# Dry run (no API calls, just planning)
python scripts/benchmark/runner.py --dry-run --models gpt-4o

# Use custom judge model
python scripts/benchmark/runner.py \
  --models claude-sonnet-4-20250514 \
  --judge-model gpt-4o-mini

# Skip cache (force re-execution)
python scripts/benchmark/runner.py --no-cache

# Generate report from existing run
python scripts/benchmark/reporter.py \
  --results benchmark-results/run-20250201-143022/model_scores.json \
  --format markdown

# Generate report for CI
python scripts/benchmark/reporter.py \
  --results benchmark-results/latest/model_scores.json \
  --format github \
  --compare-to benchmark-results/baseline/model_scores.json
```

## Dependencies

### New Python Packages

```
github-copilot-sdk>=0.2.0  # Unified LLM client
pydantic>=2.0             # Data validation for result schemas
rich>=13.0                # Terminal UI for progress bars
tenacity>=8.0             # Retry logic with exponential backoff
```

### Existing Dependencies (No Changes)

- Python 3.10+ (already required)
- Standard library: `json`, `hashlib`, `pathlib`, `asyncio`, `datetime`

### External Services

- **GitHub Copilot subscription** (for Copilot SDK auth) OR BYOK config for OpenAI/Anthropic/Azure
- No new external dependencies

## Migration / Backwards Compatibility

### Eval File Schema Migration

**Current schema** (from `evals/evals.json` and `evals/*.json`):
```json
{
  "assertions": {
    "must_detect": true,
    "severity": "critical",
    "suggest_parameterized_query": true
  }
}
```

**New schema** (binary assertions):
```json
{
  "assertions": {
    "detected_bug": true,
    "correct_severity": true,
    "actionable_fix": true,
    "evidence_cited": true
  },
  "counter_example": false
}
```

**Migration strategy:**
1. Create migration script `scripts/benchmark/migrate_evals.py` that:
   - Reads old eval files
   - Maps old assertion keys to new schema:
     - `must_detect` → `detected_bug`
     - `suggest_*` → `actionable_fix`
     - `severity` → `correct_severity`
   - Adds `counter_example: false` to all non-counter-example cases
   - Adds `evidence_cited: true` to all cases (new requirement)
   - Writes updated files
2. Support both schemas during transition (check for `must_detect` vs `detected_bug`)
3. Deprecate old schema after Phase 2 completion

### Backwards Compatibility

- **Existing `runner.py` and `reporter.py`** — will be extended, not replaced; old functionality preserved
- **`skills/model-scores.yml`** — schema extended with new fields (mean_latency_ms, mean_tokens, confidence_interval); old fields remain
- **No breaking changes to skill format** — skills continue to be plain markdown files

## Testing Strategy

### Unit Tests

**`tests/benchmark/test_copilot_client.py`**
- Mock Copilot SDK responses
- Test session creation with different models
- Test streaming event capture (TTFT, total latency)
- Test error handling (model unavailable, rate limit)

**`tests/benchmark/test_judge.py`**
- Test judge prompt generation for each assertion type
- Test parsing of judge responses (pass/fail/justification)
- Test handling of ambiguous judge responses (retry logic)

**`tests/benchmark/test_cache.py`**
- Test content hash generation (stability across runs)
- Test cache hit/miss logic
- Test stale cache invalidation (> 7 days)

**`tests/benchmark/test_scorer.py`**
- Test metric aggregation (pass_rate, F1, precision, recall)
- Test counter-example handling
- Test confidence interval calculation

### Integration Tests

**`tests/benchmark/test_runner_integration.py`**
- Run single (skill × model × eval case) combination end-to-end
- Verify JSONL output format
- Verify cache creation and reuse

**`tests/benchmark/test_reporter_integration.py`**
- Generate report from synthetic `model_scores.json`
- Verify markdown formatting
- Verify heatmap CSV generation
- Verify regression detection logic

### Eval Case Coverage

Each spec requirement will be validated by running the benchmark harness against specific eval cases:

**Benchmark Harness Spec:**
- `Scenario: Single Skill × Model × Eval Case Run` — Validated by `security-injection.json` case `sql-injection-001` with model `gpt-4o-mini`
- `Scenario: Batch Execution Across Models` — Validated by running all security-injection cases with 3 models (claude, gpt, gemini)
- `Scenario: Cached Results` — Validated by running same case twice, asserting second run reads from cache
- `Scenario: Session-Based Model Access` — Validated by verifying Copilot SDK session creation logs
- `Scenario: BYOK Support` — Validated by running with `--provider-config` pointing to OpenAI API key
- `Scenario: Streaming for Latency Measurement` — Validated by asserting TTFT < total_latency in results

**Model Scoring Spec:**
- `Scenario: Assertion Types` — Validated by running eval case with all 5 assertion types and checking each pass/fail
- `Scenario: LLM-as-Judge Scoring` — Validated by reviewing judge justifications in assertion_results.jsonl
- `Scenario: Counter-Example Scoring` — Validated by `sql-injection-safe-001` counter-example case, asserting no_false_positive passes
- `Scenario: Per-Skill × Model Metrics` — Validated by checking model_scores.json contains all expected metrics
- `Scenario: Best Model Selection` — Validated by verifying `skills/model-scores.yml` updated with highest F1 model

**Reporting Spec:**
- `Scenario: Model Leaderboard` — Validated by checking report.md contains ranked table with F1 scores
- `Scenario: Skill Difficulty Ranking` — Validated by checking report.md contains skills ranked by avg F1
- `Scenario: Adversarial Pairing Recommendations` — Validated by checking report.md contains `recommended_pairings` section
- `Scenario: Model × Skill Heatmap` — Validated by checking heatmap.csv exists and has correct dimensions
- `Scenario: Cross-Run Comparison` — Validated by running twice with different model, checking regression section

### Manual Testing

- **Cost estimation** — Run `--dry-run` with all models, verify estimated cost is reasonable (< $100)
- **Streaming latency** — Run with `--verbose`, verify TTFT logs appear before full response
- **Judge accuracy** — Sample 10 assertion evaluations, manually review judge justifications for correctness
- **Report readability** — Generate report with 3 models × 5 skills, verify markdown renders correctly in GitHub

## Edge Cases

### Edge Case: Model Not Available in Copilot Catalog

**Scenario:** User requests a model that isn't available via `client.list_models()`

**Handling:**
- Runner calls `client.list_models()` at startup
- Validates requested models against available list
- Logs warning for unavailable models: `"Model 'xyz' not available, skipping"`
- Continues with remaining models (does not fail entire run)
- If ALL requested models are unavailable, fails with clear error message

### Edge Case: Rate Limit Hit During Batch Execution

**Scenario:** Copilot API returns 429 rate limit error mid-batch

**Handling:**
- Use `tenacity` library with exponential backoff: `@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=60))`
- On 429, wait (starting at 4s, doubling each retry, max 60s)
- After 3 failed retries, log error and skip this combination
- Continue with remaining combinations
- Report skipped combinations in run summary

### Edge Case: Copilot SDK Session Hangs

**Scenario:** `session.send_and_wait()` never returns (network issue, API bug)

**Handling:**
- Add timeout to all SDK calls: `asyncio.wait_for(session.send_and_wait(...), timeout=120)`
- On timeout, log error with traceback
- Skip this combination, continue with next
- Report timeout count in run summary

### Edge Case: Judge Model Gives Ambiguous Response

**Scenario:** Judge returns "maybe" or "unclear" instead of "pass"/"fail"

**Handling:**
- Judge prompt explicitly instructs: "Respond ONLY with 'pass' or 'fail', followed by a one-line justification"
- Parser checks for exact match on "pass" or "fail" (case-insensitive)
- If neither found, retry up to 2 times with stronger prompt: "Your previous response was ambiguous. Respond with EXACTLY 'pass' or 'fail'."
- If still ambiguous after 2 retries, default to `fail` and log warning

### Edge Case: Skill or Eval Content Changes Mid-Run

**Scenario:** User edits a skill file while benchmark is running

**Handling:**
- Content hash is computed at discovery time (before execution starts)
- Changes during run do not affect current run (cache keys already computed)
- Next run will detect content change and invalidate cache for affected cases

### Edge Case: No Eval Cases for a Skill

**Scenario:** Skill exists but has no matching eval file in `evals/`

**Handling:**
- Runner logs warning: `"No eval file found for skill 'xyz', skipping"`
- Does not fail entire run
- Skill appears in report with "no eval data" note

### Edge Case: All Models Fail Assertions for a Skill

**Scenario:** Every model scores F1 < 0.70 on a skill

**Handling:**
- Reporter flags skill as "unsolved" in difficulty ranking
- Recommendation: "Skill may need prompt tuning or additional eval cases"
- Does not block report generation

### Edge Case: Division by Zero in Metrics

**Scenario:** Skill has only counter-examples (no positive cases), precision/recall undefined

**Handling:**
- Check denominators before computing precision/recall/F1
- If `true_positives + false_negatives == 0`, set `recall = None`
- If `true_positives + false_positives == 0`, set `precision = None`
- If either is None, set `f1 = None`
- Report metrics as "N/A" in tables

### Edge Case: Regression Detection with No Baseline

**Scenario:** User runs `--compare-to` but baseline file doesn't exist

**Handling:**
- Reporter checks if comparison file exists
- If not, logs info: `"No baseline found, skipping regression detection"`
- Generates report without regression section
- Does not fail

### Edge Case: Context Window Exceeded

**Scenario:** Skill prompt + eval code snippet exceeds model's context window

**Handling:**
- Copilot SDK will return error if context too large
- Runner catches error, logs: `"Context window exceeded for model 'xyz' on eval 'abc'"`
- Skips this combination, continues with others
- Report notes which combinations were skipped due to context limits

### Edge Case: Cost Exceeds Budget

**Scenario:** Estimated cost in `--dry-run` is too high

**Handling:**
- Dry run outputs estimated cost before execution
- User can abort and run with fewer models or skills
- No automatic budget enforcement (user responsibility)
- Future enhancement: `--max-cost` flag to abort if estimate exceeds threshold

## Implementation Phasing

### Phase 2.1: Core Harness (Week 1)

**Deliverables:**
- `scripts/benchmark/copilot_client.py` — SDK wrapper with session management
- `scripts/benchmark/cache.py` — Content-addressable caching
- `scripts/benchmark/runner.py` — Extended with Copilot SDK integration, streaming latency, retry logic
- `benchmark-results/` — JSONL output format
- Unit tests for copilot_client and cache

**Validation:** Run single skill × model × eval case end-to-end, verify JSONL output

### Phase 2.2: Scoring Engine (Week 2)

**Deliverables:**
- `scripts/benchmark/judge.py` — LLM-as-judge prompts and evaluation
- `scripts/benchmark/scorer.py` — Metric aggregation (F1, precision, recall)
- Migration script for eval schema (old → new assertions)
- Updated eval files with new schema
- Unit tests for judge and scorer

**Validation:** Run full security-injection skill with 3 models, verify model_scores.json

### Phase 2.3: Reporting & Analysis (Week 3)

**Deliverables:**
- `scripts/benchmark/reporter.py` — Extended with heatmap, regression detection, adversarial pairings
- `benchmark-results/<run-id>/report.md` — Markdown report template
- `benchmark-results/<run-id>/heatmap.csv` — CSV export
- Integration tests for reporter

**Validation:** Generate report from synthetic data, verify all sections present

### Phase 2.4: Production Readiness (Week 4)

**Deliverables:**
- `scripts/benchmark/pricing.json` — Configurable pricing table
- Cost estimation in `--dry-run`
- BYOK support documentation
- CI/CD integration example (GitHub Actions workflow)
- Edge case handling (rate limits, timeouts, ambiguous judge responses)
- End-to-end integration tests

**Validation:** Run full benchmark (all skills, 5 models), generate report, verify cost tracking

## Open Questions for Implementation

1. **Judge Model Selection** — Should we allow per-skill judge models (e.g., security skills use a more capable judge)? Or keep one global judge for consistency?
   - **Recommendation:** Start with global judge (gpt-4o-mini), add per-skill override in Phase 3 if needed

2. **Confidence Threshold for Best Model Selection** — If multiple models have similar F1 (within 0.02), should we prefer faster/cheaper models?
   - **Recommendation:** Yes, add tiebreaker logic: F1 (primary) → latency (secondary) → cost (tertiary)

3. **Counter-Example Ratio** — What ratio of positive:negative cases is ideal per skill? Current evals have ~3:1 ratio.
   - **Recommendation:** Maintain 3:1 ratio (75% positive, 25% counter-examples) to match real-world PR distributions

4. **Cache Expiry** — Should cache expire after 7 days, or should it be permanent with manual invalidation?
   - **Recommendation:** 7-day auto-expiry with `--no-cache` flag for manual override; balances freshness with cost

5. **Parallel Execution Concurrency** — Default concurrency of 4; should this be auto-tuned based on rate limits?
   - **Recommendation:** Start with fixed 4, add `--concurrency N` flag for manual override; auto-tuning in Phase 3

6. **Regression Threshold** — What F1 drop constitutes a "regression"? Spec says 0.05, but should this be configurable?
   - **Recommendation:** Default 0.05, add `--regression-threshold` flag for CI customization

7. **Streaming vs Non-Streaming** — Should streaming be always-on, or optional? (Adds ~10% overhead)
   - **Recommendation:** Always-on for benchmarks (latency is key metric); add `--no-streaming` for debugging if needed
