# Proposal: Autoresearch Tuning

## Intent

Implement continuous improvement loops that automatically optimize each skill × model combination using autoresearch-style mutation and evaluation. This creates a self-improving code review system that learns from failures and adapts to new attack patterns over time.

## Scope

### In Scope
- Activate the skill-optimizer skill (built in Phase 1) to run autoresearch loops
- Mutate skill prompts based on eval failures (add heuristics, refine examples, adjust severity thresholds)
- Test mutations against benchmark suite (Phase 2 harness)
- Commit improvements that increase F1 score or reduce false positive rate
- Run tuning loops on schedule (weekly) or triggered by new eval cases
- Track improvement history (skill version → metrics trajectory)

### Out of Scope
- Manual prompt engineering (fully automated)
- Fine-tuning model weights (prompt-level tuning only)
- Real-time adaptation during PR review (tuning runs offline)

## Approach

1. **Baseline Measurement:** Run Phase 2 benchmark to establish current performance
2. **Failure Analysis:** skill-optimizer identifies patterns in false negatives and false positives
3. **Mutation Generation:** Generate candidate prompt variants (add detection rules, remove noisy patterns, refine examples)
4. **Evaluation:** Test each mutation against full eval suite
5. **Selection:** Keep mutations that improve metrics (F1 +5%, FPR -10%)
6. **Iteration:** Repeat until convergence or max iterations (10 rounds)
7. **Deployment:** Commit improved skills to main branch

## Impact

### Affected Areas
- Skills will evolve over time with version metadata tracking changes
- Benchmark infrastructure (Phase 2) will be invoked regularly
- Git history will show autoresearch commits with performance deltas

## Risks

1. **Overfitting:** Tuning to eval cases may not generalize to real code → Mitigation: Phase 4 validates on live PRs
2. **Churn:** Frequent skill updates may cause confusion → Mitigation: Semantic versioning, changelog generation
3. **Degradation:** Mutations may accidentally worsen performance → Mitigation: Require metric improvement before commit, automated rollback
4. **Compute Cost:** Autoresearch loops are expensive (many LLM calls) → Mitigation: Run weekly, cache results, use cheaper models for initial screening

## Amendment: Multi-Model Tuning Cascade

### Feature: Staged Model Progression with Escalation

**New capability:** When a skill fails to reach 95% benchmark pass rate, automatically escalate to a more capable model before marking as unresolved.

**Cascade sequence:**
1. **Stage 1 (Fast/Cheap):** Run tuning with `gpt-5-mini` for up to 5 iterations or until 95% pass rate
2. **Stage 2 (Mid-Tier):** If not at 95%, escalate to `claude-haiku-4.5` for up to 3 iterations or until 95%
3. **Stage 3 (Unresolved):** If still below 95%, add skill to `skills-tools/needs-review.md` for manual review

**Benefits:**
- Cost-effective initial tuning with fast models
- Automatic escalation for difficult skills
- Explicit tracking of skills requiring human attention
- Reproducible decision trail in tuning history

**Configuration:**
- Cascade models configurable in `scripts/tune/config.yaml`
- Per-stage iteration limits and threshold targets
- Automatic needs-review list generation and maintenance

## Open Questions

1. What's the stopping criteria for tuning loops (convergence threshold)?
   - **Answer:** 95% benchmark pass rate or iteration limit, whichever comes first
2. Should tuning be per-skill or per-skill-model combination?
   - **Answer:** Per-skill-model combination, with cascade per skill
3. How to handle conflicting objectives (high recall but acceptable FPR)?
4. Should mutations be constrained to preserve skill readability?
5. Should cascade be mandatory or optional per skill?
   - **Answer:** Mandatory; driven by convergence failure detection
