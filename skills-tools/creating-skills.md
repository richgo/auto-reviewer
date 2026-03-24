# Creating and Improving Skills

This document describes the target workflow for authoring skills in `skill-machine`.

The main rethink is simple: this should feel like **one skill pipeline**, not three or four separate tools that happen to live next to each other.

## Recommended Product Shape

User-facing workflow should collapse into **one tool with two primary modes**:

1. `create` - generate or refine a skill and produce evals
2. `tune` - run the tuning cascade and decide whether the skill is ready, benchmark-worthy, or needs manual review

Benchmarking still matters, but it should be a **stage inside the pipeline**, not a separate product the author has to mentally stitch together.

## The Workflow

### Mode 1: Create

`create` should take an idea, repo examples, or an existing draft and do the full authoring pass:

1. Capture the intent of the skill
2. Draft `skills/<skill-name>/SKILL.md`
3. Generate an initial eval set in `evals/<skill-name>.json`
4. Run a quick trigger/detection validation pass
5. Produce a review report showing what looks good and what still needs work

Expected output from `create`:

- `skills/<skill-name>/SKILL.md`
- `evals/<skill-name>.json`
- a small report artifact summarizing trigger quality and obvious gaps

This means the skill author does **not** separately think "now I use skill-creator, now I use eval-viewer, now I wire JSON by hand." The tool should do that in one flow.

### Mode 2: Tune

Once the skill and evals exist, `tune` should start the optimization loop:

1. Load the skill and linked eval set
2. Run the configured cascade
3. Keep the best candidate that improves score without unacceptable regression
4. Record tuning history
5. Optionally benchmark the promoted candidate
6. If the target is still missed, add the skill to `skills-tools/needs-review.md`

Expected output from `tune`:

- tuned skill content or promoted candidate snapshot
- tuning history logs
- optional benchmark report
- `needs-review.md` entry if the cascade fails

## What This Means for the Tooling Split

The current layout suggests four products:

- `skill-creator/`
- `skill-optimizer/`
- `benchmark-runner/`
- `local-calibration/`

That split is probably too literal.

### Suggested shape

- **One authoring front door** for create + tune
- **One shared runtime library** for eval execution, scoring, model access, history, and reporting
- **One optional downstream calibration tool** for repo-specific adaptation after a skill is already good globally

In practice, that means:

- `skill-creator/`, `skill-optimizer/`, and `benchmark-runner/` should converge into a single concept such as `skill-pipeline/`
- `local-calibration/` can stay separate because it solves a different problem: adapting already-good skills to a specific installed repo

## Current Repository Reality

Today the code already hints at this consolidation:

- `skills-tools/skill-creator/scripts/run_loop.py` already combines eval + improve into a loop
- `scripts/skill_machine/autoresearch.py` already owns mutation and acceptance logic
- `scripts/skill_machine/cascade.py` adds staged escalation
- `scripts/benchmark/runner.py` is a downstream validation stage

The bigger problem is that model access and pipeline orchestration are still fragmented.

## Most Important Missing Abstraction: LLM Transport

Right now the repo has duplicated Copilot SDK wrappers:

- `skills-tools/skill-creator/scripts/copilot_sdk.py`
- `scripts/benchmark/copilot_client.py`
- `scripts/skill_machine/llm_client.py` wrapping benchmark transport

That duplication is the clearest sign that the next architectural step is not "more workflow docs" but a shared model layer.

### Recommended interface

Introduce a provider-agnostic transport contract used by create, eval, tune, and benchmark stages.

Example shape:

```python
class LLMTransport(Protocol):
    def list_models(self) -> list[ModelInfo]: ...
    def complete(self, request: CompletionRequest) -> CompletionResponse: ...
    def supports(self, capability: ModelCapability) -> bool: ...
```

With shared types:

- `CompletionRequest`
  - `prompt`
  - `system`
  - `model`
  - `temperature`
  - `max_tokens`
  - `response_format`
- `CompletionResponse`
  - `text`
  - `model`
  - `provider`
  - `usage`
  - `raw`
- `ModelInfo`
  - provider name
  - model id
  - capabilities
  - context size if known

### Providers

Then implement transports such as:

- `CopilotSDKTransport`
- `ClaudeTransport`
- `CodexTransport`

The rest of the pipeline should depend on the interface, not on Copilot-specific session setup.

### Why this matters

This unlocks:

- running the same create/tune flow with Copilot, Claude, or Codex
- comparing provider/model combinations without forking pipeline code
- removing duplicated auth, retry, timeout, and response parsing logic
- making benchmark results more credible because the execution path is shared

## How the Unified Tool Could Work

### Command shape

```bash
python scripts/skill_pipeline.py create --idea "detect insecure deserialization"
python scripts/skill_pipeline.py tune --skill insecure-deserialization
```

Or, if you want a single verb:

```bash
python scripts/skill_pipeline.py run --skill insecure-deserialization --stage create
python scripts/skill_pipeline.py run --skill insecure-deserialization --stage tune
```

### `create` stage responsibilities

`create` should orchestrate these internal steps:

1. Generate or refine the skill draft
2. Generate seed evals from the requirement plus a few negative cases
3. Run quick validation on trigger quality
4. Ask for human review only where necessary
5. Write a manifest linking the skill to its eval file and artifacts

### `tune` stage responsibilities

`tune` should orchestrate these internal steps:

1. Resolve the skill manifest
2. Choose provider/model sequence from config
3. Run cascade stage 1
4. Escalate if target is missed
5. Promote the best candidate
6. Optionally run benchmark before final promotion
7. Record failure in `needs-review.md` if the target still is not met

## Add a Skill Manifest

The pipeline gets simpler if each skill has lightweight metadata describing where its artifacts live.

Suggested example:

```yaml
skill: insecure-deserialization
skill_path: skills/insecure-deserialization/SKILL.md
eval_path: evals/insecure-deserialization.json
owner: security
status: draft
benchmark_profile: default
```

This avoids hard-coding path conventions into every script and makes resume/retry flows much easier.

## What Should Probably Change in `skills-tools/`

### Keep

- documentation for the authoring workflow
- `needs-review.md`
- any human-facing review/report helpers

### Consolidate

- `skill-creator/`
- `skill-optimizer/`
- `benchmark-runner/`

These should read as implementation details or modules of the same pipeline, not as separate end-user tools.

### Keep separate

- `local-calibration/`

That belongs after the global skill pipeline, because it tunes for local repo conventions rather than for the canonical skill itself.

## What Is No Longer Needed

### Separate product boundaries for create / optimize / benchmark

Authors should not have to decide which tool owns the next step. The pipeline should know.

### Duplicate provider wrappers

The current multiple Copilot-specific wrappers should be replaced by one shared transport layer.

### Copilot-specific assumptions in pipeline docs

Copilot SDK can remain the default transport for this repo, but the architecture should not require it.

## Better Gaps to Track

The old gaps section focused too early on language and platform specialization. Those are real, but they are not the first-order architecture problem.

The more important gaps are:

1. **Unified entrypoint**
   - Current: authoring, tuning, and benchmarking are described as separate tools
   - Missing: one pipeline command with `create` and `tune` modes
   - Why it matters: lower cognitive overhead and clearer automation

2. **Provider-agnostic LLM transport**
   - Current: Copilot wrapper logic exists in multiple places
   - Missing: shared transport abstraction for Copilot, Claude, and Codex
   - Why it matters: easier experimentation, less duplication, cleaner testing

3. **Shared workflow state**
   - Current: each script infers paths and state on its own
   - Missing: manifest or run state linking skill, evals, logs, benchmark outputs, and promotion status
   - Why it matters: resumability and traceability

4. **Generated eval quality control**
   - Current: eval generation is part of the story, but not strongly governed
   - Missing: explicit checks for class balance, negative examples, language coverage, and assertion quality
   - Why it matters: tuning only works if the eval set is trustworthy

5. **Promotion gates**
   - Current: tuning and benchmark stages exist, but promotion policy is implied
   - Missing: explicit rules for when a candidate becomes the new default
   - Why it matters: avoids accidental regressions and makes automation safe

6. **Structured manual review queue**
   - Current: `needs-review.md` is useful for humans
   - Missing: optional machine-readable companion data for automation and dashboards
   - Why it matters: easier follow-up and triage at scale

7. **Cross-skill and regression checks**
   - Current: most evaluation is skill-local
   - Missing: checks for interaction effects and scheduled revalidation
   - Why it matters: production quality depends on the whole system, not just one isolated skill

8. **Lifecycle management**
   - Current: skill creation is documented better than skill retirement
   - Missing: deprecation, replacement, archival, and migration guidance
   - Why it matters: the corpus will otherwise accumulate stale skills

## Additional Improvements Worth Considering

Beyond the transport abstraction and unified CLI, the next useful moves would be:

- **Separate deterministic logic from model logic**
  - scoring, file IO, manifests, artifact writing, and report generation should not depend on provider code

- **Use structured outputs where possible**
  - eval generation, mutation proposals, and benchmark summaries should prefer schema-shaped responses over free-form text

- **Support resume/replay**
  - long-running tuning jobs should be restartable from logs and manifests instead of starting over

- **Add explicit model roles**
  - one model can draft evals, another can mutate skills, another can judge outputs; this should be configured, not hard-coded

- **Make benchmark a policy stage**
  - benchmark should be invocable from `tune` as a gate, not treated as a disconnected tool

- **Introduce artifact directories per skill**
  - for example `artifacts/<skill>/create/`, `artifacts/<skill>/skill_machine/`, `artifacts/<skill>/benchmark/`

## Quick Reference

### Recommended future UX

```bash
python scripts/skill_pipeline.py create --idea "detect weak JWT validation"
python scripts/skill_pipeline.py tune --skill weak-jwt-validation
```

### Reasonable internal implementation split

- `scripts/skill_pipeline.py` - orchestration entrypoint
- `scripts/llm/` - provider transports and shared request/response types
- `scripts/evals/` - eval generation, loading, validation
- `scripts/skill_machine/` - mutation, scoring, cascade, promotion
- `scripts/benchmark/` - final benchmark execution and reporting

## Helpful References

- `skills-tools/skill-creator/SKILL.md` - current authoring guidance
- `skills-tools/skill-creator/scripts/run_loop.py` - existing eval/improve loop
- `scripts/skill_machine/autoresearch.py` - current tuning loop
- `scripts/skill_machine/cascade.py` - staged escalation logic
- `scripts/skill_machine/llm_client.py` - current tune-side model interface
- `scripts/benchmark/copilot_client.py` - current benchmark-side transport
