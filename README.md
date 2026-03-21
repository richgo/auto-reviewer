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

1. **Review tasks** → atomic, testable bug detection units
2. **Skills** → composed from tasks, with binary eval assertions
3. **SWE-bench scoring** → score each model × skill × language
4. **Autoresearch tuning** → overnight mutation loops improve skills
5. **Local calibration** → adapt to repo conventions on install

## Project Structure

```
auto-reviewer/
├── .github/agents/          # OpenSpec workflow agents
├── review-tasks/            # Phase 0: atomic review task taxonomy
│   ├── security/
│   ├── concurrency/
│   ├── correctness/
│   ├── testing/
│   ├── performance/
│   ├── reliability/
│   ├── api-design/
│   ├── data/
│   ├── observability/
│   └── code-quality/
├── skills/                  # Phase 1: composed from tasks
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

## Build Phases

- **Phase 0** — Review task taxonomy (current)
- **Phase 1** — Skills from tasks
- **Phase 2** — SWE-bench style scoring
- **Phase 3** — Autoresearch tuning
- **Phase 4** — Composer agent
- **Phase 5** — Adversarial engine

## Packaging

Distributed as an [APM](https://github.com/microsoft/apm) package. Works with Claude Code, GitHub Copilot, Codex, or any agent CLI that supports `agents.md` and `skills.md`.

## License

MIT
