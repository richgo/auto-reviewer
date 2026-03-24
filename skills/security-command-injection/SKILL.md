---
name: security command injection
description: >
  Command Injection. Use this skill whenever diffs may
  introduce security issues on all, especially in all. Actively look for: Command
  injection occurs when user-controlled input is passed unsanitized to shell execution
  functions, allowing attackers to execute arbitrary... and report findings with
  critical severity expectations and actionable fixes.
---

# Command Injection
## Task Metadata
- Category: `security`
- Severity: `critical`
- Platforms: `all`
- Languages: `all`

## Purpose
Command injection occurs when user-controlled input is passed unsanitized to shell execution functions, allowing attackers to execute arbitrary system commands with the application's privileges.

## Detection Heuristics
- Shell execution functions with user input: exec, system, popen, subprocess.call with shell=True
- String concatenation/interpolation building shell commands
- Missing input validation or escaping before shell execution
- Dangerous characters not sanitized: ; & | ` $ ( ) < > \n
- Use of shell interpreters instead of direct program execution

## Eval Cases
### Case 1: Python subprocess with shell=True
```python
# BUGGY CODE — should be detected
import subprocess
filename = request.args.get('file')
subprocess.call(f'cat /var/logs/{filename}', shell=True)
```
**Expected finding:** Critical — Command injection via subprocess.call with shell=True. User-controlled `filename` allows injection with `; rm -rf /` or `$(malicious)`. Use shell=False with argument list or validate against allowlist.

### Case 2: Node.js child_process.exec
```javascript
// BUGGY CODE — should be detected
const { exec } = require('child_process');
const userInput = req.query.cmd;
exec(`ping -c 4 ${userInput}`, (error, stdout) => {
  res.send(stdout);
});
```
**Expected finding:** Critical — Command injection via exec(). User input `cmd` flows to shell command. Attacker can inject `8.8.8.8; cat /etc/passwd`. Use execFile() with argument array or validate input strictly.

### Case 3: Java Runtime.exec with string
```java
// BUGGY CODE — should be detected
String ip = request.getParameter("ip");
Runtime.getRuntime().exec("ping " + ip);
```
**Expected finding:** Critical — Command injection via Runtime.exec(). User-controlled `ip` concatenated into shell command. Use ProcessBuilder with separate arguments instead.

## Counter-Examples
### Counter 1: subprocess with argument list
```python
# CORRECT CODE — should NOT be flagged
import subprocess
filename = request.args.get('file')
# Validate filename first
if not re.match(r'^[a-zA-Z0-9_\-\.]+$', filename):
    abort(400)
subprocess.call(['cat', f'/var/logs/{filename}'], shell=False)
```
**Why it's correct:** shell=False with argument list prevents command injection. Validation ensures filename has no dangerous characters.

### Counter 2: ProcessBuilder with separate args
```java
// CORRECT CODE — should NOT be flagged
ProcessBuilder pb = new ProcessBuilder("ping", "-c", "4", userInput);
Process process = pb.start();
```
**Why it's correct:** ProcessBuilder with separate arguments prevents shell interpretation of special characters.

## Binary Eval Assertions
- [ ] Detects command injection in eval case 1 (subprocess with shell=True)
- [ ] Detects command injection in eval case 2 (child_process.exec)
- [ ] Detects command injection in eval case 3 (Runtime.exec string concat)
- [ ] Does NOT flag counter-example 1 (subprocess with argument list)
- [ ] Does NOT flag counter-example 2 (ProcessBuilder with separate args)
- [ ] Finding includes recommendation to use argument arrays
- [ ] Severity assigned as critical
