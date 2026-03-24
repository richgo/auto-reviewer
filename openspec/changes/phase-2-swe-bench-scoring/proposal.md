# Proposal: SWE-bench-Style Scoring

## Intent

Build a comprehensive scoring harness to evaluate model × skill performance on real-world code review scenarios, inspired by SWE-bench's approach to measuring software engineering capabilities. Uses the **GitHub Copilot SDK** as the unified LLM client — giving access to all models (Claude, GPT, Gemini, etc.) through a single interface with built-in auth, streaming, and tool support.

## Scope

### In Scope
- Implement test harness using the Copilot SDK (`github-copilot-sdk`) for model access
- Run skills against eval cases with different LLM models via `CopilotClient.create_session(model=<model>)`
- Measure precision, recall, F1, false positive rate, latency (TTFT + total), and cost per skill × model combination
- Generate performance matrix comparing all available Copilot models across 40+ skills
- Identify optimal model for each skill category
- Create leaderboard showing model rankings per concern area
- Support BYOK (Bring Your Own Key) for models not in the Copilot catalog
- Build custom harness tools exposed to the Copilot agent for structured review output

### Out of Scope
- Live deployment to production (Phase 3)
- Auto-fix implementation (Phase 4)
- Adversarial multi-model review (Phase 5)
- Custom model fine-tuning (future work)

## Approach

### 1. Copilot SDK as Unified LLM Client

Instead of building separate HTTP clients for each provider, we use the Copilot SDK:

```python
from copilot import CopilotClient, PermissionHandler

client = CopilotClient()
await client.start()

# Discover available models
models = await client.list_models()

# Create a session with a specific model
session = await client.create_session(
    model="claude-sonnet-4-20250514",
    system_message={"content": skill_body},  # SKILL.md content
    on_permission_request=PermissionHandler.approve_all,
)

# Send eval case and get review
response = await session.send_and_wait({"prompt": code_snippet})
review_output = response.data.content
```

**Why Copilot SDK:**
- **All models, one interface** — Claude, GPT, Gemini, DeepSeek, etc. without separate API keys/clients
- **Built-in auth** — uses GitHub Copilot subscription or BYOK
- **Streaming** — time-to-first-token measurement via `assistant.message_delta` events
- **Custom tools** — expose structured review output tools to the agent (severity, evidence, fix suggestion)
- **Session management** — handles retries, context, cleanup automatically

### 2. Custom Harness Tools

Define tools that structure the review output for easier scoring:

```python
from copilot import define_tool
from pydantic import BaseModel, Field

class ReviewFinding(BaseModel):
    vulnerability: str = Field(description="Type of vulnerability or issue found")
    severity: str = Field(description="critical, high, medium, or low")
    line_numbers: list[int] = Field(description="Affected line numbers")
    evidence: str = Field(description="Code snippet showing the issue")
    fix: str = Field(description="Suggested fix with corrected code")

@define_tool(description="Report a code review finding", skip_permission=True)
async def report_finding(params: ReviewFinding) -> str:
    findings.append(params)
    return f"Finding recorded: {params.vulnerability}"
```

This gives us structured output instead of parsing free-text reviews.

### 3. Benchmark Execution

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Eval Cases  │────▶│ Copilot SDK  │────▶│   Scorer     │
│  (JSON)      │     │ (model X)    │     │ (assertions) │
│              │     │              │     │              │
│  code_snippet│     │ session with │     │ pass/fail    │
│  assertions  │     │ skill body   │     │ per assertion│
│              │     │ + tools      │     │              │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                                           model_scores.json
                                           + leaderboard.md
                                           + heatmap.csv
```

### 4. Multi-Model Testing

Run each skill with all available Copilot models:

```bash
python scripts/benchmark/runner.py \
  --models claude-sonnet-4-20250514,gpt-4.1,gemini-2.5-pro,o3-mini \
  --output benchmark-results/
```

Or discover and run all available models:

```bash
python scripts/benchmark/runner.py --all-models --output benchmark-results/
```

### 5. Metrics Collection

Per (skill, model) combination:
- **Detection rate** — did it find the bug?
- **False positive rate** — did it flag safe code?
- **Actionability** — did it suggest a working fix?
- **Severity accuracy** — did it assign the right severity?
- **Evidence quality** — did it cite specific code?
- **TTFT** — time to first token (streaming latency)
- **Total latency** — wall-clock time for full response
- **Token usage** — input + output tokens
- **Estimated cost** — based on configurable pricing table

## Impact

### Affected Areas
- New `scripts/benchmark/` with Copilot SDK-based runner
- Skills' system prompts loaded and sent via Copilot SDK sessions
- Custom tools for structured review output
- `benchmark-results/` for run data, model scores, and reports
- `skills/model-scores.yml` updated with best model per skill
- CI/CD integration via GitHub Actions (Copilot SDK works in CI with auth)

## Risks

1. **Copilot SDK is Technical Preview** — API may change → Mitigation: pin SDK version, abstract behind thin wrapper
2. **API Cost** — Running 40 skills × 10 models × 200 eval cases → Mitigation: use `--dry-run` for cost estimation, cache results, run incrementally
3. **Rate Limits** — Premium request quotas → Mitigation: configurable concurrency, backoff, BYOK for high-volume runs
4. **Model Availability** — some models may not be available in all regions → Mitigation: `list_models()` discovery, skip unavailable with warning

## Open Questions

1. ~~Should we build separate API clients per provider?~~ → **Resolved: use Copilot SDK**
2. Should we use custom tools for structured output or parse free-text reviews?
3. How to handle models with different context windows (some skills + code may exceed limits)?
4. What threshold defines "good enough" performance (F1 > 0.85? 0.90?)?
5. Should we weight metrics differently by concern (e.g., recall > precision for security)?
6. BYOK vs Copilot subscription for high-volume benchmark runs — which is more cost-effective?
