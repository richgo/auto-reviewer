# Benchmark Harness Specification Delta

## ADDED Requirements

### Requirement: Eval Case Execution

The system SHALL execute review skills against eval cases by sending the skill's SKILL.md as system instructions and the eval case's code snippet as user input to an LLM API.

#### Scenario: Single Skill × Model × Eval Case Run

- GIVEN a skill at `skills/concerns/security-injection/SKILL.md`
- AND an eval case from `evals/security-injection.json` with a SQL injection code snippet
- AND a target model `claude-sonnet-4-20250514`
- WHEN the benchmark harness executes this combination
- THEN it SHALL send the skill body as system prompt and the code snippet as user message
- AND it SHALL capture the model's review output as raw text
- AND it SHALL record wall-clock latency in milliseconds
- AND it SHALL record input and output token counts
- AND it SHALL store the result in a structured JSON format

#### Scenario: Batch Execution Across Models

- GIVEN a set of skills, a set of eval JSON files, and a list of target models
- WHEN the harness runs in batch mode
- THEN it SHALL execute every (skill × model × eval case) combination
- AND it SHALL support parallel execution with configurable concurrency (default: 4)
- AND it SHALL handle rate limits with exponential backoff and retry (max 3 retries)
- AND it SHALL continue processing remaining combinations if one fails

#### Scenario: Cached Results

- GIVEN a (skill × model × eval case) combination has already been executed
- AND the skill content hash and eval case content hash have not changed
- WHEN the harness encounters this combination
- THEN it SHALL skip execution and reuse the cached result
- AND it SHALL log that the result was cached

### Requirement: Copilot SDK Integration

The system SHALL use the GitHub Copilot SDK (`github-copilot-sdk`) as the unified LLM client, providing access to all models through a single interface.

#### Scenario: Session-Based Model Access

- GIVEN the Copilot CLI is installed and authenticated
- AND a target model is specified (e.g., `claude-sonnet-4-20250514`, `gpt-4.1`, `gemini-2.5-pro`)
- WHEN the harness creates a benchmark session
- THEN it SHALL use `CopilotClient.create_session(model=<model>)` to create a session for each model
- AND it SHALL send the skill's SKILL.md as the system message
- AND it SHALL send the eval case's code snippet as the user prompt via `session.send_and_wait()`
- AND it SHALL capture the response content, latency, and token usage

#### Scenario: BYOK (Bring Your Own Key) Support

- GIVEN the user configures BYOK via provider settings
- WHEN the harness runs with a BYOK model
- THEN it SHALL pass the provider configuration to `create_session(provider=<config>)`
- AND it SHALL support OpenAI, Anthropic, and Azure AI Foundry endpoints via BYOK

#### Scenario: Available Models Discovery

- GIVEN the Copilot CLI is authenticated
- WHEN the harness starts
- THEN it SHALL call `client.list_models()` to discover available models
- AND it SHALL validate requested models against the available list
- AND it SHALL skip unavailable models with a warning (not fail the entire batch)

#### Scenario: Streaming for Latency Measurement

- GIVEN streaming is enabled for a benchmark session
- WHEN the harness measures latency
- THEN it SHALL record time-to-first-token (TTFT) from `assistant.message_delta` events
- AND it SHALL record total completion time from `session.idle` events
- AND both metrics SHALL be stored in the result

### Requirement: Result Storage

The system SHALL store benchmark results in a structured, append-friendly format.

#### Scenario: Result File Structure

- GIVEN a benchmark run has completed
- WHEN results are written
- THEN each result SHALL be stored as a JSON object in a JSONL file at `benchmark-results/<run-id>.jsonl`
- AND each line SHALL contain: run_id, skill_name, model_id, eval_case_id, raw_output, latency_ms, input_tokens, output_tokens, timestamp, skill_content_hash, eval_content_hash

#### Scenario: Run Metadata

- GIVEN a benchmark run is initiated
- WHEN the run starts
- THEN the harness SHALL create a `benchmark-results/<run-id>/metadata.json` containing: run_id, start_time, models, skills, eval_files, git_commit, harness_version

### Requirement: CLI Interface

The system SHALL provide a command-line interface for running benchmarks.

#### Scenario: Full Benchmark Run

- GIVEN the user runs `python scripts/benchmark/runner.py --models claude-sonnet-4-20250514,gpt-4o --output benchmark-results/`
- WHEN the command executes
- THEN it SHALL discover all skills in `skills/` and their matching eval files in `evals/`
- AND it SHALL execute all combinations and write results

#### Scenario: Single Skill Benchmark

- GIVEN the user runs `python scripts/benchmark/runner.py --skill skills/concerns/security-injection --models claude-sonnet-4-20250514`
- WHEN the command executes
- THEN it SHALL run only the specified skill against its matching eval file
- AND it SHALL output results for only that skill

#### Scenario: Dry Run

- GIVEN the user passes `--dry-run`
- WHEN the command executes
- THEN it SHALL list all (skill × model × eval case) combinations that would be executed
- AND it SHALL NOT make any LLM API calls
- AND it SHALL report the estimated number of API calls and approximate token cost
