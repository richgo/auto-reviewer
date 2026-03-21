# Proposal: Composer Agent — Dynamic APM Package Assembly

## Intent

Users shouldn't manually pick which review skills apply to their project. A **Composer Agent** analyzes a repo, detects its tech stack and platforms, then generates a bespoke `apm.yml` that pulls exactly the right skills from the auto-reviewer monorepo — version-pinned, platform-compiled, ready for any agent runtime.

## Scope

### In Scope

- **Repo analysis agent** — scans a target repo to detect languages, frameworks, platforms (Android/iOS/Web/Microservices), build systems, CI/CD setup, existing security tooling
- **Skill selection engine** — maps detected stack to relevant concern, language, and output skills
- **APM manifest generation** — outputs a complete `apm.yml` with version-pinned skill dependencies
- **Multi-platform compilation** — `apm compile` generates agent instructions for detected runtimes (Copilot/Claude Code/Cursor/OpenCode)
- **Version pinning** — every skill pinned to a git tag or commit; `apm.lock.yaml` locks exact SHAs
- **Reinstall workflow** — re-run composer after repo changes → `apm install --update` to pull latest

### Out of Scope

- Publishing to an APM registry (skills live in the auto-reviewer monorepo)
- Running actual reviews (that's the review-orchestrator skill)
- Modifying user source code

## Approach

### 1. Auto-Reviewer as APM Monorepo

The `richgo/auto-reviewer` repo IS the package source. APM supports monorepo subdirectory installs natively — each skill folder has a `SKILL.md` and is installable independently:

```bash
# Install individual skills from the monorepo
apm install richgo/auto-reviewer/skills/concerns/security-injection#v1.0.0
apm install richgo/auto-reviewer/skills/languages/python#v1.0.0
apm install richgo/auto-reviewer/skills/outputs/inline-comments#v1.0.0
```

APM detects the `SKILL.md` in each subdirectory and treats it as a virtual subdirectory package. On install, skills are copied to `.github/skills/`, `.claude/skills/`, `.cursor/skills/` etc. based on which runtimes the user's project supports.

### 2. Version Pinning Strategy

Version pinning uses git refs on the auto-reviewer repo (tags, branches, or commit SHAs):

```yaml
dependencies:
  apm:
    # Pinned to stable release tag (immutable)
    - richgo/auto-reviewer/skills/core/review-orchestrator#v1.0.0
    
    # Pinned to specific commit (maximum reproducibility)
    - richgo/auto-reviewer/skills/concerns/security-injection#a1b2c3d
    
    # Track a branch (latest, may change)
    - richgo/auto-reviewer/skills/languages/python#main
```

The `apm.lock.yaml` lockfile records the exact resolved commit SHA for every dependency, regardless of how the ref was specified. This gives users three levels of control:

| Strategy | Ref Format | Trade-off |
|----------|-----------|-----------|
| **Stable releases** | `#v1.0.0` (tag) | Immutable, tested, recommended |
| **Exact commit** | `#a1b2c3d` (SHA) | Maximum reproducibility |
| **Latest** | `#main` (branch) | Always current, may break |
| **No ref** | (omitted) | Lockfile pins on first install |

### 3. Composer Agent Workflow

```
┌──────────────┐         ┌─────────────────┐         ┌──────────────┐
│  User's Repo │──scan──▶│  Composer Agent  │──emit──▶│   apm.yml    │
│              │         │                 │         │  (generated) │
│  - languages │         │  1. Detect stack│         │              │
│  - frameworks│         │  2. Select skills│        │  - pinned    │
│  - platforms │         │  3. Pick outputs│         │  - filtered  │
│  - CI/CD     │         │  4. Set config  │         │  - compiled  │
└──────────────┘         └─────────────────┘         └──────┬───────┘
                                                            │
                                                     apm install
                                                            │
                                                     apm compile
                                                            ▼
                                                   ┌────────────────┐
                                                   │ Agent-ready:   │
                                                   │ .github/skills/│
                                                   │ .claude/skills/│
                                                   │ .cursor/skills/│
                                                   │ AGENTS.md      │
                                                   │ CLAUDE.md      │
                                                   └────────────────┘
```

### 4. Detection Heuristics

| Signal | Detects | Skills Selected |
|--------|---------|-----------------|
| `*.py`, `requirements.txt`, `pyproject.toml` | Python | `languages/python` |
| `*.kt`, `build.gradle.kts`, `AndroidManifest.xml` | Kotlin/Android | `languages/kotlin` + `*/android/*` concerns |
| `*.swift`, `*.xcodeproj`, `Podfile` | Swift/iOS | `languages/swift` + `*/ios/*` concerns |
| `package.json`, `*.ts`, `*.tsx` | TypeScript/Web | `languages/typescript` + `*/web/*` concerns |
| `Dockerfile`, `docker-compose.yml` | Containers | `concerns/security-infrastructure` |
| `k8s/`, `helm/`, `*.tf` | IaC | `concerns/security-infrastructure` |
| `.github/workflows/` | GitHub Actions | `outputs/inline-comments` |
| `build.gradle`, `pom.xml` | Java | `languages/java` |
| SQL files, ORM configs | Database | `concerns/data-integrity` |
| `openapi.yml`, GraphQL schemas | API | `concerns/security-api`, `concerns/api-design` |
| `Gemfile`, `*.rb` | Ruby | `languages/ruby` |
| `composer.json`, `*.php` | PHP | `languages/php` |
| `go.mod`, `*.go` | Go | `languages/go` |
| `Cargo.toml`, `*.rs` | Rust | `languages/rust` |
| `*.csproj`, `*.sln` | C# | `languages/csharp` |

### 5. Generated apm.yml

```yaml
# Generated by auto-reviewer composer v1.0.0
# Stack: Python (Django), TypeScript (React), Docker, GitHub Actions
# Platforms: web, microservices
# Generated: 2026-03-21T13:00:00Z
name: my-project-review
version: 1.0.0
description: Auto-reviewer skills tailored for my-project

target: all  # compile for all detected runtimes

dependencies:
  apm:
    # Core (always included)
    - richgo/auto-reviewer/skills/core/review-orchestrator#v1.0.0
    - richgo/auto-reviewer/skills/core/diff-analysis#v1.0.0

    # Security concerns (filtered by platform)
    - richgo/auto-reviewer/skills/concerns/security-injection#v1.0.0
    - richgo/auto-reviewer/skills/concerns/security-auth#v1.0.0
    - richgo/auto-reviewer/skills/concerns/security-data-protection#v1.0.0
    - richgo/auto-reviewer/skills/concerns/security-network#v1.0.0
    - richgo/auto-reviewer/skills/concerns/security-infrastructure#v1.0.0
    - richgo/auto-reviewer/skills/concerns/security-client-side#v1.0.0
    - richgo/auto-reviewer/skills/concerns/security-api#v1.0.0
    # NOT included: security-mobile (no Android/iOS detected)

    # Quality concerns
    - richgo/auto-reviewer/skills/concerns/concurrency#v1.0.0
    - richgo/auto-reviewer/skills/concerns/correctness#v1.0.0
    - richgo/auto-reviewer/skills/concerns/performance#v1.0.0
    - richgo/auto-reviewer/skills/concerns/reliability#v1.0.0
    - richgo/auto-reviewer/skills/concerns/testing#v1.0.0
    - richgo/auto-reviewer/skills/concerns/code-quality#v1.0.0

    # Language skills (detected)
    - richgo/auto-reviewer/skills/languages/python#v1.0.0
    - richgo/auto-reviewer/skills/languages/typescript#v1.0.0

    # Output skills (matched to CI/CD)
    - richgo/auto-reviewer/skills/outputs/inline-comments#v1.0.0
    - richgo/auto-reviewer/skills/outputs/review-report#v1.0.0

compilation:
  target: all
  strategy: distributed
```

### 6. User Workflow

```bash
# FIRST TIME: Composer analyzes repo and generates apm.yml
cd my-project
npx auto-reviewer compose     # generates apm.yml

# Install skills
apm install                    # downloads pinned skills to apm_modules/
                               # copies to .github/skills/, .claude/skills/ etc.

# Compile for agent runtimes
apm compile                    # generates AGENTS.md, CLAUDE.md etc.

# UPDATES: pull latest skill versions
apm install --update           # re-resolves refs, updates lockfile

# RE-COMPOSE: after adding a new platform (e.g., mobile)
npx auto-reviewer compose --update   # re-analyzes, adds new skills

# BUNDLE: for CI/CD or distribution
apm pack --archive             # creates portable .tar.gz
apm pack --format plugin       # creates standalone plugin directory
```

### 7. Multi-Language & Multi-Platform Monorepo Support

A key requirement: the generated `apm.yml` must work for monorepos with multiple languages and platforms. The Composer Agent handles this by:

1. **Scanning all subdirectories** — not just root-level files
2. **Per-directory language detection** — `backend/` might be Python, `frontend/` might be TypeScript, `mobile/` might be Kotlin + Swift
3. **Union of all detected platforms** — if the monorepo has Android + iOS + Web + microservices, ALL platform-specific skills are included
4. **APM's distributed compilation** — `strategy: distributed` generates per-directory agent instructions, so each subdirectory gets relevant skills

```yaml
# Example: monorepo with backend (Python), frontend (React), mobile (Kotlin + Swift)
dependencies:
  apm:
    # All platforms detected
    - richgo/auto-reviewer/skills/concerns/security-mobile#v1.0.0
    - richgo/auto-reviewer/skills/concerns/security-client-side#v1.0.0
    - richgo/auto-reviewer/skills/concerns/security-infrastructure#v1.0.0
    
    # All detected languages
    - richgo/auto-reviewer/skills/languages/python#v1.0.0
    - richgo/auto-reviewer/skills/languages/typescript#v1.0.0
    - richgo/auto-reviewer/skills/languages/kotlin#v1.0.0
    - richgo/auto-reviewer/skills/languages/swift#v1.0.0
```

### 8. Version Management Lifecycle

```
v1.0.0  ─── Initial release (all skills)
  │
  ├── User pins: richgo/auto-reviewer/skills/concerns/security-injection#v1.0.0
  │
v1.1.0  ─── Security skill improvements (autoresearch-tuned)
  │
  ├── User can: apm install --update  (pulls v1.1.0 for unpinned deps)
  ├── Or: manually change #v1.0.0 → #v1.1.0 in apm.yml
  │
v2.0.0  ─── Breaking changes (new skill format)
  │
  ├── User stays on v1.x until they explicitly opt in
  └── Re-run composer: npx auto-reviewer compose --update
```

## Impact

- Each skill directory needs a valid `SKILL.md` (already done)
- Auto-reviewer repo needs semver git tags for releases
- Need a `scripts/compose/` CLI tool that generates the `apm.yml`
- APM must be installed in the user's environment (`curl -sSL https://aka.ms/apm-unix | sh`)

## Risks

- **APM is v0.1 (Working Draft)** — manifest schema may change
- **Monorepo versioning** — git tags apply to the whole repo, not individual skills. A change to one skill bumps the version for all. Could mitigate with branch-per-skill or accept repo-level versioning.
- **Skill interdependencies** — concern skills reference review-tasks at prompt-time. These references are documentation, not runtime deps, so this should be fine — the skill's `SKILL.md` body contains all needed instructions.
- **Large dependency tree** — a full install might pull 30+ skills. APM handles this via parallel downloads and lockfile caching.

## Open Questions

1. **Release cadence** — tag releases manually, or automate via CI on merge to main?
2. **Skill independence** — should skills be fully self-contained (inline all review-task content) or reference review-tasks as a separate dependency?
3. **Config merging** — if a user already has an `apm.yml`, should the composer merge or create a separate file?
4. **`apm pack` for distribution** — should we publish pre-packed bundles as GitHub release artifacts for air-gapped installs?
