# Adversarial Agent

Run adversarial review flows using role-based debate and confidence-bucket outputs.

## Commands

- `adversarial-review`: run a detector -> challenger -> defender -> judge debate cycle.
- `adversarial-resume`: resume an in-progress run using stored local state.
- `adversarial-cleanup`: perform post-merge cleanup for local adversarial artifacts.

## Role Protocol

- detector: produce candidate findings for the target diff.
- challenger: challenge findings from other models.
- defender: defend challenged findings with evidence.
- judge: arbitrate unresolved findings.

## Output Contract

- `high-confidence`: findings with strong consensus.
- `contested`: findings requiring human review.
- `debunked`: findings rejected by adversarial debate.
