# Proposal: Adversarial Review Engine

## Intent

Current review behavior does not clearly separate multi-model issue discovery from adversarial scrutiny, and it does not enforce reviewer independence from the original finder. This can weaken trust in adjudication quality and make provenance/auditability unclear when recovering interrupted runs. The change aims to ensure that multiple LLMs first run code-review skills over a codebase or PR/diff, findings are durably deduplicated in the database, and adversarial review is performed only after detection is complete by reviewers that are not the same model that authored the finding.

## Scope

### In Scope
- Multi-LLM detection phase where multiple models run review skills against the target codebase or PR/diff.
- Persistent finding capture in SQLite including deduped/canonicalized issue records before adversarial review begins.
- Explicit phase boundary: adversarial challenge/defense/judgment starts only after detection completion criteria are met.
- Reviewer independence requirement: the model reviewing/challenging a finding must be different from the model that found/wrote that finding.
- Provenance tracking in DB for both sides of each issue lifecycle: who found an issue and who reviewed/judged it.
- Resume-safe persistence semantics for detection and adversarial phases so interrupted runs can continue without losing finder/reviewer attribution.

### Out of Scope
- Real-time adversarial review (runs async, results delivered later)
- Fine-tuning models for debate (prompt-based roles only)
- Human-in-the-loop during debate (fully automated)
- Replacing non-adversarial review paths outside this phase boundary definition
- Model-training or benchmark policy changes unrelated to finder/reviewer separation and provenance

## Approach

Use a two-phase lifecycle with a strict gate between discovery and adversarial scrutiny. First, run independent multi-model detection and persist normalized, deduplicated findings as the shared source of truth. Then run adversarial review over that finalized finding set with enforced model separation between finder and reviewer roles, preserving complete finder/reviewer attribution in database records for auditability and recovery.

## Impact

### Affected Areas
- `agents/adversarial/agent.md` proposal contract expectations for phase ordering, reviewer independence, and provenance requirements.
- SQLite persistence contract surfaces for detection records, deduped findings, and reviewer attribution.
- Review orchestration expectations where adversarial processing depends on completion of multi-model detection.
- Output/reporting expectations that rely on stored finder/reviewer identity metadata.

## Risks

1. **Latency increase:** waiting for full detection completion before adversarial review may delay final output.
2. **Assignment constraints:** enforcing reviewer/finder model separation may reduce scheduling flexibility when model availability is limited.
3. **Deduplication correctness:** incorrect canonicalization could merge distinct issues or split duplicates, affecting later adversarial review quality.
4. **Provenance integrity:** incomplete or inconsistent finder/reviewer attribution can undermine auditability and resume behavior.

## Open Questions

1. What defines detection completion for starting adversarial review (all detector tasks complete vs quorum-based completion)?
2. How should the system behave when no eligible reviewer model remains that differs from the finding author model?
3. What minimum provenance fields are required in outputs versus retained only in DB?
4. Should dedupe happen strictly before adversarial review only, or also allow additional dedupe checkpoints after adversarial stages?
