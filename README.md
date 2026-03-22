# auto-reviewer

Adversarial, multi-model code review system — APM-packaged, self-tuning, community-extensible.

## Vision

An open-source code review system where **multiple LLMs independently review code, then cross-examine each other's findings**. Skills are tuned per-model using autoresearch loops, scored via SWE-bench style benchmarks, and dynamically composed into bespoke APM packages for each project.

## How It Works

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  SKILL LIBRARY   │────▶│  COMPOSER AGENT  │────▶│  ADVERSARIAL     │
│  (pre-tuned,     │     │  (scans repo,    │     │  REVIEW ENGINE   │
│   scored/model)  │     │   builds bespoke │     │  (multi-model,   │
│                  │     │   apm.yml)       │     │   cross-examine) │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

### Adversarial Review

For each concern, multiple models review independently, then challenge each other:

- **Consensus findings** → high confidence, auto-action
- **Disputed findings** → present both sides with evidence
- **Unique findings** → flagged for human review

### Self-Tuning Pipeline

1. **Skills** → atomic, testable bug detection units and canonical review guidance
2. **Skill-linked evals** → benchmark/tuning inputs keyed directly by skill identifier
3. **SWE-bench scoring** → score each model × skill × language
4. **Autoresearch tuning** → overnight mutation loops improve skills
5. **Local calibration** → adapt to repo conventions on install

## Project Structure

```
auto-reviewer/
├── .github/agents/          # OpenSpec workflow agents
├── skills/                  # Canonical atomic skill corpus
│   ├── core/
│   ├── languages/
│   ├── concerns/
│   ├── outputs/
│   └── tuning/
├── agents/                  # Orchestrator + composer agents
├── evals/                   # Eval datasets + assertions
├── config/                  # Default configs + model scores
├── scripts/                 # Benchmark + tuning scripts
├── actions/                 # GitHub Action workflows
└── openspec/                # OpenSpec change management
```

Active skill identity is canonicalized to one folder per skill with a `SKILL.md` entry contract, with **no legacy skill path support** in active composition and routing flows.

## Build Phases

- **Phase 1** — Skill-first atomic corpus
- **Phase 2** — SWE-bench style scoring
- **Phase 3** — Autoresearch tuning
- **Phase 4** — Composer agent
- **Phase 5** — Adversarial engine

## Packaging

Distributed as an [APM](https://github.com/microsoft/apm) package. Works with Claude Code, GitHub Copilot, Codex, or any agent CLI that supports `agents.md` and `skills.md`.

## Composer workflow (Phase 4)

The Composer Agent generates and updates `apm.yml` using repository signals and a deterministic composition policy.

- Policy file: `scripts/compose/policy.yaml`
- Agent entry: `agents/composer/agent.md`
- Pipeline: detect signals -> select policy-mapped skills -> apply refs -> validate -> merge/write

### Generate

1. Run compose in generate mode for a repository.
2. Composer writes `apm.yml` with composer-managed `dependencies.apm`.
3. Generated dependencies default to stable tag pins (`#v1.0.0`) unless override strategy is used.

### Update

1. Re-run compose in update mode after repository stack changes.
2. Only composer-managed `richgo/auto-reviewer/skills/*` dependencies are refreshed.
3. Non-managed dependencies and other `apm.yml` sections remain preserved.

### Pin overrides

- `tag` (default): append a stable tag ref (for example `#v1.0.0`)
- `sha`: append commit SHA
- `branch`: append branch name
- `none`: keep dependency path without ref

### APM lifecycle

After compose output is written and validated:

1. `apm install` resolves dependencies and updates lock data.
2. `apm compile` compiles agent artifacts for detected runtime profile.

For multi-runtime repositories, composer writes distributed compilation defaults.

## Adversarial workflow (Phase 5)

The adversarial agent adds multi-model debate routing with local SQLite persistence.

- Agent entry: `agents/adversarial/agent.md`
- Cleanup contract: `agents/adversarial/cleanup.md`
- Local state DB: `.auto-reviewer/adversarial.db`

### Commands

- `adversarial-review`: run detector/challenger/defender/judge debate for a run identity.
- `adversarial-resume`: continue an existing run for `(repo, pr, commit_sha)`.
- `adversarial-cleanup`: apply post-merge archive/purge/prune/vacuum steps.

### Reliability and fallback

- If model quorum checks fail or provider availability drops, mark the run as degraded.
- In degraded mode, fallback to baseline review output while preserving explicit status metadata.

### Retention and cleanup

- Keep lightweight run summaries for audit.
- Purge transient debate artifacts after merge.
- Prune stale SQLite rows by retention policy and vacuum database storage.

## License

MIT
