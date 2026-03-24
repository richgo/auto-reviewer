# Proposal: Unified Skill Pipeline

## Intent

Skill authoring is currently described and organized as several adjacent tools for creation, evaluation, tuning, and benchmarking. That split makes the workflow harder to understand, harder to automate, and harder to evolve consistently across providers. At the same time, model access is fragmented across multiple Copilot-specific wrappers, which makes it difficult to reuse the same pipeline with Codex, Claude, or other transports.

This change proposes redefining skill authoring as one coherent pipeline with a simpler user-facing workflow and a shared provider-agnostic model layer. The goal is to reduce cognitive overhead for skill authors, remove duplicated runtime concerns, and establish clearer boundaries between authoring, tuning, benchmarking, and repo-local calibration.

## Scope

### In Scope
- Reframe skill authoring as a unified pipeline rather than separate end-user tools
- Define a simpler user-facing workflow centered on creating a skill with evals, then tuning it
- Establish the need for a shared provider-agnostic LLM abstraction usable by authoring, eval, tuning, and benchmark flows
- Clarify the intended role of benchmarking as part of the pipeline lifecycle
- Clarify which responsibilities belong in the canonical global skill pipeline versus local calibration
- Identify the workflow state and artifact relationships the pipeline must manage consistently
- Implementing provider adapters for Copilot SDK, Claude, or Codex

### Out of Scope
- Implementing the unified CLI or orchestration entrypoint
- Changing existing skill content, eval datasets, or tuning logic as part of this proposal
- Designing specific manifest schemas, file layouts, or artifact storage formats
- Replacing local calibration behavior for repo-specific adaptation

## Approach

Shift the product framing from a collection of loosely related tools to a single authoring pipeline with a small number of primary user actions. Treat skill creation, eval generation, tuning, and benchmark validation as stages of the same lifecycle rather than as separate products the user must compose manually.

At the same time, separate pipeline behavior from provider behavior. The system should define model interaction in a way that does not assume GitHub Copilot SDK as the only transport, even if Copilot remains the default in this repository. This creates a stable boundary so the same workflow can be executed across different model providers without forking the surrounding pipeline.

The proposal also distinguishes global skill quality work from repo-local calibration. Global authoring and tuning should remain one coherent pipeline for canonical skills, while local calibration remains a downstream adaptation step for repository-specific conventions.

## Impact

This change affects how the repository describes and eventually structures skill authoring across several existing areas:

- `skills-tools/` documentation and tool boundaries
- `scripts/tune/` lifecycle expectations, especially tuning and escalation flows
- `scripts/benchmark/` as a validation stage in the authoring lifecycle
- model access code currently duplicated across skill-creator, benchmark, and tuning paths
- OpenSpec requirements for skills, eval ownership, and tuning workflow boundaries

It may also affect how future changes describe authoring artifacts, run history, manual review queues, and promotion decisions for tuned skills.

## Risks

- The proposal could over-consolidate concerns and blur meaningful internal module boundaries
- A provider-agnostic abstraction could become too generic and fail to reflect real capability differences between transports
- Treating benchmark as part of the pipeline could unintentionally weaken its role as an independent validation gate if boundaries are not kept explicit
- Unifying workflow language without aligning existing scripts could create confusion during the transition period
- Local calibration could become entangled with canonical skill authoring if the separation is not clearly preserved

## Open Questions

- Should the unified workflow expose two primary actions (`create` and `tune`) or one command with staged submodes?
- Should benchmark validation be mandatory before promotion, or optional based on policy/configuration?
- What minimal workflow state must be tracked so runs can be resumed, audited, and compared across providers?
- Which model capabilities need to be represented explicitly in the shared abstraction to support current and future providers?
- How should manual review outputs be represented so they remain useful to humans while also supporting future automation?
