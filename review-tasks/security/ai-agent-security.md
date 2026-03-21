# Task: AI Agent Security

## Category
security

## Severity
high

## Platforms
all

## Languages
all

## Description
AI agents with tool use, code execution, or multi-step workflows face risks including unauthorized tool invocation, insufficient sandboxing, resource abuse, and failure to validate tool outputs before using them in subsequent steps.

## Detection Heuristics
- Tool execution without permission scoping or allowlisting
- Missing sandboxing for code execution tools
- No resource limits (timeout, memory, API call quotas)
- Tool outputs used without validation in chained operations
- Agent loops without termination conditions
- Missing audit logging of tool invocations

## Eval Cases

### Case 1: Code execution without sandbox
```python
# BUGGY CODE — should be detected
def execute_code_tool(code: str):
    result = exec(code)  # Direct exec!
    return result

agent_tools = [execute_code_tool, read_file, write_file]
agent = Agent(tools=agent_tools)
```
**Expected finding:** Critical — Code execution tool without sandboxing. Agent can execute arbitrary Python, access filesystem, escalate privileges. Use containerized sandbox (gVisor, Firecracker) or restricted environments (Pyodide, isolated subprocess with seccomp).

### Case 2: No resource limits on agent
```javascript
// BUGGY CODE — should be detected
const agent = new Agent({
  tools: [searchWeb, callAPI, generateImage],
  maxIterations: Infinity, // No limit!
  maxExecutionTime: null
});

app.post('/agent/run', async (req, res) => {
  const result = await agent.run(req.body.goal);
  res.json(result);
});
```
**Expected finding:** High — AI agent without resource limits. Can run indefinitely, exhaust API quotas, cause DoS. Set `maxIterations` (< 50), `maxExecutionTime` (< 5 min), per-user API rate limits.

### Case 3: Unvalidated tool outputs in chain
```python
# BUGGY CODE — should be detected
def multi_step_agent(user_query):
    search_results = tools.search_web(user_query)
    # Directly using untrusted search results in next tool
    email_content = tools.generate_email(search_results)
    tools.send_email(to='admin@company.com', body=email_content)
```
**Expected finding:** High — Tool chain without output validation. Malicious search results can poison email content sent to admin. Validate/sanitize tool outputs before passing to subsequent tools, implement content policy checks.

## Counter-Examples

### Counter 1: Sandboxed code execution
```python
# CORRECT CODE — should NOT be flagged
import docker

def execute_code_tool(code: str):
    client = docker.from_env()
    container = client.containers.run(
        'python:3.11-alpine',
        f'python -c "{code}"',
        mem_limit='128m',
        cpu_period=100000,
        cpu_quota=50000,
        network_disabled=True,
        remove=True,
        timeout=5
    )
    return container.decode('utf-8')
```
**Why it's correct:** Code runs in isolated Docker container with resource limits, no network access.

### Counter 2: Resource-constrained agent
```javascript
// CORRECT CODE — should NOT be flagged
const agent = new Agent({
  tools: [searchWeb, callAPI],
  maxIterations: 20,
  maxExecutionTime: 60000, // 1 minute
  rateLimits: {
    searchWeb: { max: 10, window: '1m' },
    callAPI: { max: 5, window: '1m' }
  }
});
```
**Why it's correct:** Agent has iteration limit, timeout, per-tool rate limits.

## Binary Eval Assertions
- [ ] Detects unsandboxed code execution in eval case 1
- [ ] Detects missing resource limits in eval case 2
- [ ] Detects unvalidated tool chain in eval case 3
- [ ] Does NOT flag counter-example 1 (Docker sandbox)
- [ ] Does NOT flag counter-example 2 (resource constraints)
- [ ] Finding references OWASP AI Agent Security principles
- [ ] Severity assigned as high or critical for code exec
