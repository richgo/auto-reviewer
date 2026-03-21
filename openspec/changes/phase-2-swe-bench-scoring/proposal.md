# Proposal: SWE-bench-Style Scoring

## Intent

Build a comprehensive scoring harness to evaluate model × skill performance on real-world code review tasks, inspired by SWE-bench's approach to measuring software engineering capabilities. This enables data-driven selection of the best model for each skill and provides a benchmark for continuous improvement.

## Scope

### In Scope
- Implement test harness that runs skills against eval cases with different LLM models
- Measure precision, recall, F1, false positive rate, latency, and cost per skill × model combination
- Generate performance matrix comparing models (GPT-4, Claude, Gemini, DeepSeek, etc.) across all 40 skills
- Identify optimal model for each skill category (e.g., Claude Opus for security-injection, GPT-4 for correctness)
- Create leaderboard showing model rankings per concern area
- Support model-specific prompt tuning (different prompts for different models)

### Out of Scope
- Live deployment to production (Phase 3)
- Auto-fix implementation (Phase 4)
- Adversarial multi-model review (Phase 5)
- Custom model fine-tuning (future work)

## Approach

1. **Harness Implementation:** Build runner that executes skill + model combinations against eval JSON files
2. **Multi-Model Testing:** Run each skill with 5-10 different LLM models (various providers, sizes, capabilities)
3. **Metrics Collection:** Capture detection accuracy, false positive rate, latency (time to analyze), cost (API tokens)
4. **Performance Matrix:** Generate skill × model matrix with scores for each dimension
5. **Optimization:** Use results to select best model per skill and tune prompts for each model

## Impact

### Affected Areas
- New `benchmark/` directory with runner script, results storage, leaderboard generation
- Skills may need model-specific prompt variants (separate frontmatter sections)
- CI/CD integration for continuous benchmarking on new eval cases

## Risks

1. **API Cost:** Running 40 skills × 10 models × 200 eval cases = 80,000 LLM calls → Mitigation: Use cheaper models for initial runs, cache results, run incrementally
2. **Latency:** Benchmark runs may take hours → Mitigation: Parallelize execution, use streaming APIs
3. **Model Availability:** Some models may be rate-limited or unavailable → Mitigation: Graceful degradation, retry logic
4. **Eval Realism:** Synthetic test cases may not reflect production performance → Mitigation: Phase 3 adds real-world validation

## Open Questions

1. Should we use same prompt for all models or model-specific prompts?
2. How to handle models with different context windows (8k vs 128k)?
3. What threshold defines "good enough" performance (F1 > 0.85? 0.90?)?
4. Should we weight metrics (prioritize recall over precision for security)?
