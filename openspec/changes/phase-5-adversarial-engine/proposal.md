# Proposal: Adversarial Review Engine

## Intent

Build a multi-model adversarial review system where different LLMs cross-examine each other's findings, challenge assumptions, and debate edge cases. This creates a "panel of experts" approach to code review, surfacing blind spots and reducing both false positives and false negatives through collaborative scrutiny.

## Scope

### In Scope
- Implement adversarial review workflow: multiple models (e.g., GPT-4, Claude Opus, Gemini Pro) independently review code, findings are aggregated, each model challenges others' findings ("Is this really a bug? What if X?"), consensus emerges through debate rounds
- Define roles: Detector (finds issues), Challenger (questions findings), Defender (justifies original finding), Judge (final decision)
- Multi-round protocol: Round 1 (independent detection), Round 2 (challenges issued), Round 3 (defenses provided), Round 4 (judge scores confidence)
- Confidence scoring: Findings that survive adversarial scrutiny get high confidence (✅), Contested findings get flagged for human review (⚠️), Debunked findings are suppressed (❌)

### Out of Scope
- Real-time adversarial review (runs async, results delivered later)
- Fine-tuning models for debate (prompt-based roles only)
- Human-in-the-loop during debate (fully automated)

## Approach

1. **Model Selection:** Choose 3-5 diverse models (different architectures, training data, strengths)
2. **Independent Review:** Each model runs skills independently against PR diff
3. **Finding Aggregation:** Union of all findings from all models
4. **Challenge Phase:** Each model reviews others' findings and issues challenges
5. **Defense Phase:** Original detector model defends its finding
6. **Consensus Scoring:** Judge model (or voting) assigns confidence score
7. **Output:** Findings with high consensus → reported, Low consensus → flagged for human review, Debunked → suppressed

## Impact

### Affected Areas
- New `adversarial/` directory with orchestration logic and debate protocols
- Output skills enhanced to show confidence scores and debate summaries
- May require significant compute (5 models × multiple rounds)

## Risks

1. **Cost:** Running 5 models × 3 rounds = 15x the baseline cost → Mitigation: Reserve for critical PRs (security-sensitive repos, production deployments)
2. **Latency:** Multi-round debate may take minutes → Mitigation: Async execution, deliver results when ready
3. **Debate Quality:** Models may agree on false positives → Mitigation: Include model with known disagreement tendency (e.g., strict vs permissive)
4. **Complexity:** Debate protocol is non-trivial to implement → Mitigation: Start with simple 2-round (detect + challenge), iterate

## Open Questions

1. How many models? (3 minimum for tiebreaking, 5 for diversity)
2. How many debate rounds? (2-4 rounds, tradeoff: depth vs latency)
3. Should models know their role (detector vs challenger) or be blind?
4. How to weight votes (equal weight or model-specific weights based on Phase 2 benchmark)?
5. Should adversarial review replace single-model review or augment it?
