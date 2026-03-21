# Proposal: Composer Agent — Dynamic APM Package Assembly

## Intent

Users shouldn't manually pick which review skills apply to their project. A **Composer Agent** analyzes a repo, detects its tech stack and platforms, then generates a bespoke `apm.yml` that pulls exactly the right skills — versioned and pinnable.

The key insight: auto-reviewer's skills are published as individual APM packages. The Composer Agent is the bridge between "197 review tasks exist" and "here's a one-command install for YOUR repo."

## Scope

### In Scope

- **Repo analysis agent** — scans a target repo to detect: languages, frameworks, platforms (Android/iOS/Web/Microservices), build systems, existing security tooling, CI/CD setup
- **Skill selection engine** — maps detected stack to relevant concern skills, language skills, and output skills
- **APM package generation** — outputs a complete `apm.yml` with:
  - Versioned skill dependencies (`richgo/auto-reviewer/skills/concerns/security-injection#v1.2.0`)
  - Platform-filtered skills (only Android skills if it's an Android project)
  - Language-filtered skills (only Python + TypeScript if that's what the repo uses)
  - Output skills matching the repo's CI/CD (GitHub Actions → inline-comments, Slack webhook → slack-summary)
  - Model preferences per skill (from `model-scores.yml` benchmark data)
- **Version pinning** — every skill dependency pinned to a specific git tag/commit
- **`apm compile`** — compiles the generated package into agent instructions for the target runtime (Copilot, Claude Code, Cursor, Codex)
- **Reinstall workflow** — user can re-run composer after repo changes to get updated skill selection, then `apm install --update` to pull latest versions

### Out of Scope

- Publishing skills to a registry (skills live in the auto-reviewer repo)
- Modifying the user's source code
- Running actual reviews (that's the review-orchestrator's job)
- APM registry/marketplace integration (future)

## Approach

### 1. Skill Versioning Strategy

Each skill is an APM-installable unit. The auto-reviewer repo is structured so APM can install individual skills:

```
richgo/auto-reviewer/skills/concerns/security-injection    # concern skill
richgo/auto-reviewer/skills/languages/python               # language skill  
richgo/auto-reviewer/skills/outputs/inline-comments        # output skill
richgo/auto-reviewer/skills/core/review-orchestrator       # core skill
richgo/auto-reviewer/skills/tuning/local-calibration       # tuning skill
```

Version pinning uses git tags on the auto-reviewer repo:
```yaml
dependencies:
  apm:
    - richgo/auto-reviewer/skills/core/review-orchestrator#v1.0.0
    - richgo/auto-reviewer/skills/concerns/security-injection#v1.0.0
    - richgo/auto-reviewer/skills/languages/python#v1.0.0
```

Semver tags: `v{major}.{minor}.{patch}` — skills are tagged independently when their content changes.

### 2. Composer Agent Workflow

```
User's repo                    Composer Agent                     Output
┌──────────┐                  ┌──────────────┐                ┌──────────┐
│ Codebase │──analyze stack──▶│ Detect:      │──select───────▶│ apm.yml  │
│          │                  │  Languages   │  skills        │ (pinned) │
│          │                  │  Frameworks  │                │          │
│          │                  │  Platforms   │                │          │
│          │                  │  CI/CD       │                │          │
│          │                  │  Existing    │                │          │
│          │                  │  tooling     │                │          │
└──────────┘                  └──────────────┘                └──────────┘
                                                                   │
                                                              apm install
                                                                   │
                                                              apm compile
                                                                   ▼
                                                          ┌────────────────┐
                                                          │ .github/agents │
                                                          │ .claude/skills │
                                                          │ .cursor/rules  │
                                                          └────────────────┘
```

### 3. Detection Heuristics

| Signal | Detects | Skills Selected |
|--------|---------|-----------------|
| `*.py`, `requirements.txt`, `pyproject.toml` | Python | `languages/python` |
| `*.kt`, `build.gradle.kts`, `AndroidManifest.xml` | Kotlin/Android | `languages/kotlin` + all `*/android/` concerns |
| `*.swift`, `*.xcodeproj`, `Podfile` | Swift/iOS | `languages/swift` + all `*/ios/` concerns |
| `package.json`, `*.ts`, `*.tsx` | TypeScript/Web | `languages/typescript` + all `*/web/` concerns |
| `Dockerfile`, `docker-compose.yml` | Containers | `concerns/security-infrastructure` |
| `k8s/`, `helm/`, `*.tf` | IaC | `concerns/security-infrastructure` |
| `.github/workflows/` | GitHub Actions | `outputs/inline-comments` |
| `build.gradle`, `pom.xml` | Java | `languages/java` |
| SQL files, ORM configs | Database | `concerns/data-integrity` |
| `openapi.yml`, GraphQL schemas | API | `concerns/security-api`, `concerns/api-design` |

### 4. User Workflow

```bash
# First time: Composer analyzes repo and generates apm.yml
cd my-project
npx auto-reviewer compose
# → Generates apm.yml with pinned skill dependencies

# Install skills into your agent setup
apm install

# Compile for your runtime (Copilot, Claude Code, Cursor)
apm compile

# Later: update to latest skill versions
apm install --update

# Or: re-run composer after adding a new platform
npx auto-reviewer compose --update
```

### 5. Generated apm.yml Structure

```yaml
# Generated by auto-reviewer composer v1.0.0
# Detected: Python (Django), TypeScript (React), Docker, GitHub Actions
# Generated: 2026-03-21T12:00:00Z
name: my-project-review
version: 1.0.0
description: Auto-reviewer skills for my-project

dependencies:
  apm:
    # Core (always included)
    - richgo/auto-reviewer/skills/core/review-orchestrator#v1.0.0
    - richgo/auto-reviewer/skills/core/diff-analysis#v1.0.0

    # Concern skills (filtered by detected stack)
    - richgo/auto-reviewer/skills/concerns/security-injection#v1.0.0
    - richgo/auto-reviewer/skills/concerns/security-auth#v1.0.0
    - richgo/auto-reviewer/skills/concerns/security-data-protection#v1.0.0
    - richgo/auto-reviewer/skills/concerns/security-network#v1.0.0
    - richgo/auto-reviewer/skills/concerns/concurrency#v1.0.0
    - richgo/auto-reviewer/skills/concerns/correctness#v1.0.0
    - richgo/auto-reviewer/skills/concerns/performance#v1.0.0
    - richgo/auto-reviewer/skills/concerns/reliability#v1.0.0
    - richgo/auto-reviewer/skills/concerns/security-infrastructure#v1.0.0

    # Language skills (detected)
    - richgo/auto-reviewer/skills/languages/python#v1.0.0
    - richgo/auto-reviewer/skills/languages/typescript#v1.0.0

    # Output skills (matched to CI/CD)
    - richgo/auto-reviewer/skills/outputs/inline-comments#v1.0.0
    - richgo/auto-reviewer/skills/outputs/review-report#v1.0.0

    # Tuning (optional, for local calibration)
    - richgo/auto-reviewer/skills/tuning/local-calibration#v1.0.0

config:
  auto_reviewer:
    platforms: [web]
    languages: [python, typescript]
    severity_threshold: medium
    adversarial:
      enabled: true
      models: [claude-sonnet-4-20250514, gpt-4o]
    outputs: [inline-comments, review-report]
```

### 6. Version Pinning & Updates

- **Initial install**: Composer pins to latest stable tag for each skill
- **Lock file**: `apm.lock.yaml` records exact commit SHAs (like `package-lock.json`)
- **Selective updates**: User can update individual skills: `apm install richgo/auto-reviewer/skills/concerns/security-injection#v1.1.0`
- **Bulk update**: `apm install --update` pulls latest for all pinned skills
- **Breaking changes**: Major version bumps require explicit opt-in (`#v2.0.0`)
- **Rollback**: Change version pin in `apm.yml` and `apm install`

## Impact

- Every skill needs to be a valid APM-installable package (needs `SKILL.md` in correct location)
- The auto-reviewer repo needs git tags for versioning
- Skills may need `apm.yml` at their level for metadata
- `apm compile` integration needs testing across all target runtimes

## Risks

- **APM is young** — API may change, features we depend on might not exist yet
- **Monorepo vs multi-repo** — all skills in one repo means one tag version for all; may need per-skill tagging strategy
- **Transitive deps** — skills that reference review-tasks need those tasks available at runtime
- **Model scores drift** — benchmark data used for model selection may become stale

## Open Questions

1. Should each skill be its own repo (multi-repo) or stay in the monorepo with path-based installs?
2. Does APM support per-subdirectory versioning, or only repo-level tags?
3. How do we handle skill dependencies (e.g., `security-injection` needs `review-tasks/security/sql-injection.md` at runtime)?
4. Should the Composer Agent run as a GitHub Action, CLI tool, or both?
5. How do we handle private/enterprise skills that extend the public taxonomy?
