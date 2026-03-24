# Creating and Improving Skills

This document describes the complete workflow for creating new skills in auto-reviewer and iteratively improving them.

## The Workflow

The skill creation and improvement process consists of 4 main phases:

### Phase 1: Draft & Create with Skill Creator

**Tool:** `skills-tools/skill-creator/` (Copilot skill)

The skill creator is an interactive agent that guides you through:

1. **Capture Intent** — Understand what the skill should detect/enable and when it should trigger
2. **Interview & Research** — Ask probing questions about edge cases, formats, and success criteria
3. **Write SKILL.md** — Create the skill with frontmatter (name, description) and detection logic
4. **Draft Test Cases** — Create a few representative code examples to test against

The skill creator helps with:
- Writing the SKILL.md file with proper formatting and structure
- Debugging early detection logic
- Creating test case datasets
- Generating quantitative evaluations (JSON assertions)

**Input:** Your problem description or existing code patterns
**Output:** A `skills/<skill-name>/SKILL.md` file and initial test cases

**Key Scripts:**
- `quick_validate.py` — Syntax-check and lint your SKILL.md
- `package_skill.py` — Bundle skill for distribution
- `run_eval.py` — Run eval cases against a skill

---

### Phase 2: Evaluate Triggers with Skill Creator

**Tool:** `skills-tools/skill-creator/eval-viewer/` + `run_eval.py`

After drafting, evaluate how well your skill triggers and detects the patterns it's designed for.

1. **Create Test Prompts** — Write concrete code examples that should/shouldn't trigger
2. **Run Evaluations** — Execute the skill against test cases with a specific LLM
3. **Analyze Results** — Review raw outputs and quantitative metrics (precision, recall, F1)
4. **Iterate** — Refine skill description and detection logic based on results

**Process:**
```bash
cd skills-tools/skill-creator
python scripts/run_eval.py \
  --skill security-injection \
  --eval-file evals/security-injection.json \
  --model gpt-5-mini
```

Then use `generate_review.py` to visualize results for analysis.

**Key Files:**
- `evals/<skill-name>.json` — Test cases with expected findings and assertions
- Counter-examples in evals prevent false positives
- Assertions check: detection, severity, actionable advice, evidence cited

**Success Criteria:**
- ✓ Skill detects true positives reliably (recall > 90%)
- ✓ Minimal false positives (FPR < 5%)
- ✓ Clear, actionable finding descriptions
- ✓ Passes all eval assertions

---

### Phase 3: Tune with Autoresearch

**Tool:** `scripts/tune/autoresearch.py` + `scripts/tune/cascade.py`

After the skill is stable, use automated tuning to improve it across model × skill combinations.

Autoresearch runs mutation loops that:
1. Analyze failure patterns in eval cases
2. Generate prompt variants to address failures
3. Score mutations against full eval suite
4. Accept mutations that improve metrics (F1, FPR)
5. Repeat until convergence or max iterations

**Multi-Model Cascade:**

If a skill fails to reach 95% pass rate in tuning:

1. **Stage 1** (gpt-5-mini): 5 iterations
   - Fast, cheap model for initial improvement
   - If reaches 95% → ✓ complete
   - If < 95% → escalate to Stage 2

2. **Stage 2** (claude-haiku-4.5): 3 iterations
   - More capable model for difficult cases
   - If reaches 95% → ✓ complete with better model
   - If < 95% → mark for manual review

3. **Failure Tracking** (skills-tools/needs-review.md)
   - Skills that failed cascade are tracked with:
     - Best model attempted
     - Best pass rate achieved
     - Link to tuning history
   - Awaits manual intervention

**Running Tuning:**
```bash
python scripts/tune/autoresearch.py \
  --skills security-injection \
  --models gpt-5-mini \
  --max-rounds 10
```

**Configuration:** `scripts/tune/config.yaml`
- Controls max rounds, convergence thresholds, mutation budgets
- Cascade models and iteration limits
- F1/FPR improvement gates

**Artifacts:**
- `tune-history/<skill>/<model>.jsonl` — Immutable run history
- `skills/model-scores.yml` — Best-per-model skill snapshots
- Automatic git commits with performance deltas

---

### Phase 4: Benchmark Against Tasks

**Tool:** `scripts/benchmark/runner.py` + `scripts/benchmark/scorer.py`

After tuning, benchmark the skill against a reference task suite to measure final performance.

Benchmarking provides:
- **Absolute metrics** — How well does this skill detect real-world bugs?
- **Comparison** — How does this model × skill perform vs. others?
- **Variance analysis** — How consistent are results across runs?

**Running Benchmarks:**
```bash
python scripts/benchmark/runner.py \
  --skills security-injection \
  --models gpt-5-mini,claude-haiku-4.5 \
  --evals evals/ \
  --output benchmark-results/
```

**Output:**
- Pass/fail rates per skill × model
- Precision, recall, F1 scores
- False positive rate, false negative rate
- Variance across multiple runs
- Detailed failure reports

**Acceptance Criteria:**
- ✓ F1 ≥ 0.85 (good balance of precision & recall)
- ✓ FPR ≤ 5% (minimal false alarms)
- ✓ FNR ≤ 10% (catches most real issues)
- ✓ Variance < 5% (consistent across runs)

---

## What's in Skills-Tools

### Subdirectories

- **skill-creator/** — Interactive skill creation and evaluation (phase 1-2)
  - Scripts for drafting, testing, and reporting on skills
  - Eval viewer for analyzing detection patterns
  - Integration with Copilot SDK for model access

- **skill-optimizer/** — Autoresearch mutation engine (documentation, see phase 3)
  - Links to tuning scripts in scripts/tune/

- **benchmark-runner/** — Benchmark execution and scoring (documentation, see phase 4)
  - Links to scoring scripts in scripts/benchmark/

- **local-calibration/** — Repository-specific skill adaptation
  - Tools to collect local evals and overlay on global benchmarks
  - Helps skills adapt to repo conventions and patterns

### What's NO LONGER NEEDED

❌ **Legacy skill paths** — Single files, scattered across folders
- All skills now follow `skills/<skill-name>/SKILL.md` canonical format
- Phase 1 (skills-from-tasks) established this structure
- Simplified routing and composition

❌ **Manual benchmark aggregation**
- Autoresearch + benchmark runner automate iteration
- No need for manual result compilation

❌ **Provider-specific CLI wrappers**
- All model access now via Copilot SDK + GitHub CLI auth
- Unified authentication and model selection

---

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: DRAFT & CREATE                                     │
│ Tool: skill-creator (interactive agent)                     │
│ Output: skills/<skill>/SKILL.md + initial evals             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: EVALUATE TRIGGERS                                  │
│ Tool: skill-creator eval-viewer + run_eval.py              │
│ Process: Test prompts → Run → Analyze → Refine             │
│ Success: Recall > 90%, FPR < 5%                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3: TUNE WITH AUTORESEARCH                             │
│ Tool: scripts/tune/autoresearch.py + cascade.py            │
│ Process: Mutate → Score → Accept/Reject → Iterate          │
│ Cascade: gpt-5-mini (5 iter) → claude-haiku-4.5 (3 iter)   │
│ Failure: Track in skills-tools/needs-review.md             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 4: BENCHMARK AGAINST TASKS                            │
│ Tool: scripts/benchmark/runner.py + scorer.py              │
│ Metrics: F1, precision, recall, FPR, variance              │
│ Acceptance: F1 ≥ 0.85, FPR ≤ 5%, stable results            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
          ✓ SKILL READY FOR PRODUCTION
           (Added to skill library & APM package)
```

---

## What's Missing from the Process

### Gaps to Address (Future Phases)

1. **Language-Specific Tuning**
   - Current: Tuning per model (gpt-5-mini, claude-haiku-4.5)
   - Missing: Language-specific variants (Python, TypeScript, Java, etc.)
   - Impact: Skills may not generalize well across languages
   - Solution: Extend cascade to include language-specific models

2. **Platform-Specific Variants**
   - Current: Generic skill prompts apply equally to all platforms
   - Missing: Mobile (Android/iOS), web, microservices, cloud variants
   - Impact: Mobile-specific bugs may not trigger reliably
   - Solution: Create platform-aware subsections in skills

3. **Regression Prevention in Production**
   - Current: Benchmark once at tuning completion
   - Missing: Continuous monitoring of skill performance on live PRs
   - Impact: Skills may degrade over time with new code patterns
   - Solution: Add periodic re-benchmarking in CI/CD (Phase 5+)

4. **Cross-Skill Interaction Testing**
   - Current: Skills tuned and tested independently
   - Missing: Testing combinations (e.g., auth + crypto skills together)
   - Impact: May miss ordering/interaction issues in reports
   - Solution: Add integration test suite combining related skills

5. **Skill Deprecation & Archival**
   - Current: No mechanism to retire obsolete skills
   - Missing: Version management, transition paths for renamed skills
   - Impact: Technical debt accumulates
   - Solution: Add skill lifecycle management (Phase 5+)

---

## Quick Reference

### Creating a New Skill

1. Use `skill-creator` agent:
   ```
   "I want to create a skill for detecting X in code"
   ```

2. Let the agent guide you through intent capture, research, and SKILL.md writing

3. Test with eval cases using `run_eval.py`

4. Refine based on results (repeat until stable)

### Tuning an Existing Skill

```bash
python scripts/tune/autoresearch.py \
  --skills <skill-name> \
  --models gpt-5-mini,claude-haiku-4.5 \
  --cascade-enabled
```

Monitor `skills-tools/needs-review.md` for skills that need manual attention.

### Benchmarking Results

```bash
python scripts/benchmark/runner.py \
  --skills <skill-name> \
  --models gpt-5-mini,claude-haiku-4.5 \
  --output benchmark-results/
```

Check `benchmark-results/<skill>/<model>/report.md` for detailed analysis.

---

## Helpful Resources

- **Skill Creator:** `skills-tools/skill-creator/SKILL.md` — Interactive agent documentation
- **Autoresearch Design:** `openspec/changes/phase-3-autoresearch-tuning/design.md`
- **Phase 1 Skills:** `skills/` — 234+ examples to learn from
- **Eval Format:** `evals/<skill>.json` — Test case structure reference
- **Benchmark Scoring:** `scripts/benchmark/scorer.py` — Metric definitions
