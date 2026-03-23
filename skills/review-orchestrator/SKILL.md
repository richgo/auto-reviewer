---
name: review-orchestrator
description: >
  Main orchestration skill for code review. Analyzes PR diffs, identifies languages and platforms,
  dispatches to appropriate concern and language skills, deduplicates findings, ranks by severity,
  and produces final report. This is the entry point for all automated code reviews.
---

# Code Review Orchestrator

## Purpose
Coordinate the automated code review process: parse diffs, identify review areas, invoke specialized skills, aggregate findings, deduplicate, rank, and format output.

## Orchestration Flow

```
1. Parse PR/diff
   ↓
2. Identify languages & platforms
   ↓
3. Detect review areas (auth, SQL, crypto, etc.)
   ↓
4. Invoke concern + language skills
   ↓
5. Collect findings
   ↓
6. Deduplicate
   ↓
7. Rank by severity
   ↓
8. Format output
```

## Step-by-Step Instructions

### Step 1: Parse PR Diff
Use the **diff-analysis** skill to extract:
- Changed files
- Added/modified lines
- Removed lines (note: deletion-only diffs have low risk)
- File paths → language detection
- Context lines for dataflow analysis

**Output:** Structured diff with file list, changed functions, and line ranges.

### Step 2: Identify Languages & Platforms
Map file extensions to languages:
- `.py` → Python
- `.ts`, `.tsx`, `.js`, `.jsx` → TypeScript/JavaScript
- `.java` → Java
- `.kt` → Kotlin
- `.swift` → Swift
- `.go` → Go
- `.rs` → Rust
- `.cs` → C#
- `.cpp`, `.cc`, `.h` → C++
- `.rb` → Ruby
- `.php` → PHP

Detect platforms from context:
- **Android:** `AndroidManifest.xml`, `build.gradle`, Kotlin/Java with Android imports
- **iOS:** `.xcodeproj`, `Info.plist`, Swift/Objective-C with UIKit/SwiftUI
- **Web:** `.html`, `.css`, React/Vue/Angular imports, Express/Flask routes
- **Microservices:** Kubernetes YAML, Docker files, service mesh configs, gRPC/REST APIs

### Step 3: Detect Review Areas
Scan changed lines for high-risk patterns to determine which concern skills to invoke:

**Injection concerns:** SQL keywords (`SELECT`, `INSERT`), HTML rendering (`innerHTML`, templates), shell commands (`subprocess`, `exec`), LDAP queries
**Auth concerns:** Login/logout, password operations, session management, OAuth flows, permission checks
**Data protection:** Crypto imports, file operations, serialization (`pickle`, `YAML`), logging, secrets
**Network:** HTTP requests, URL construction, CORS headers, TLS config, redirects
**Concurrency:** Threading, async/await, locks, shared state
**Correctness:** Null checks, array indexing, arithmetic, lifecycle methods
**Performance:** Database queries (N+1), loops, large collections, memory allocation
**Reliability:** Error handling, try/catch, timeouts, retries, graceful degradation

**Heuristic:** If pattern detected → invoke corresponding concern skill.

### Step 4: Invoke Specialized Skills
For each detected concern:
1. **Load concern skill** (e.g., `security-injection`, `concurrency`)
2. **Load language skill** (e.g., `python`, `typescript`)
3. **Run both skills** on the relevant diff sections
4. **Collect findings** from each

**Parallel execution:** Run concern skills in parallel if possible (they're independent).

**Context passing:** Provide each skill with:
- Relevant diff section (file, line range)
- Language context
- Platform context
- Full file content if needed (for dataflow analysis)

### Step 5: Collect Findings
Each skill returns findings in this structure:
```json
{
  "severity": "critical|high|medium|low",
  "category": "security|concurrency|correctness|...",
  "subcategory": "sql-injection|race-condition|null-deref|...",
  "file": "path/to/file.py",
  "line": 42,
  "function": "function_name",
  "description": "User input flows to SQL query without parameterization",
  "code_snippet": "cursor.execute(f'SELECT * FROM users WHERE id={user_id}')",
  "fix_suggestion": "Use parameterized query: cursor.execute('SELECT * FROM users WHERE id=%s', (user_id,))",
  "reference": "https://owasp.org/...",
  "confidence": 0.95
}
```

**Aggregate:** Collect all findings into a single list.

### Step 6: Deduplicate Findings
Multiple skills may flag the same issue (e.g., both `security-injection` and `python` detect SQL injection).

**Deduplication strategy:**
1. **Group by file + line + subcategory**
2. **Merge descriptions** if different angles
3. **Keep highest severity** if conflicting
4. **Combine fix suggestions** if complementary
5. **Prefer higher confidence** finding

**Example merge:**
- Finding 1: "SQL injection via f-string" (from security-injection)
- Finding 2: "Avoid f-strings in SQL queries" (from python skill)
- **Merged:** "SQL injection via f-string. Use parameterized query instead."

### Step 7: Rank by Severity
Sort findings:
1. **Critical** — immediate security risk (SQL injection, RCE, auth bypass)
2. **High** — significant risk or likely crash (XSS, race condition, null deref)
3. **Medium** — moderate risk or quality issue (CSRF, async misuse, off-by-one)
4. **Low** — minor issue or style (dead code, naming, missing docs)

Within each severity tier, sort by:
- **Confidence** (higher first)
- **Category** (security > correctness > performance > quality)
- **File path** (group by file)

### Step 8: Format Output
Invoke an **output skill** based on desired format:
- **review-report.md** — Markdown summary for PR comment
- **inline-comments.md** — Individual inline comments per finding
- **fix-pr.md** — Generate auto-fix PR
- **create-issues.md** — Create GitHub issues for findings
- **slack-summary.md** — Brief Slack notification

**Default:** Use `review-report.md` for comprehensive review comment.

### Step 9: Adversarial Handoff (Optional)
When adversarial mode is enabled, hand off to adversarial commands:

- `adversarial-review` for a new run
- `adversarial-resume` for an existing run

Pass run identity fields: `repo`, `pr`, and `commit_sha`.

If adversarial checks fail (for example provider/quorum issues), emit explicit `degraded` status metadata and continue baseline output flow.

## Example Orchestration

**Input:** PR with Python Flask changes
```diff
diff --git a/app.py b/app.py
+@app.route('/user/<id>')
+def get_user(id):
+    query = f"SELECT * FROM users WHERE id = {id}"
+    cursor.execute(query)
+    return jsonify(cursor.fetchone())
```

**Step 1: Parse diff**
- File: `app.py` (Python)
- Added lines: 10-13
- Function: `get_user`

**Step 2: Identify**
- Language: Python
- Platform: Web (Flask route)

**Step 3: Detect concerns**
- Pattern: `SELECT` + f-string → **security-injection**
- Pattern: `@app.route` + no auth → **security-auth**

**Step 4: Invoke skills**
- `security-injection` + `python` → Finding: SQL injection
- `security-auth` + `python` → Finding: No auth check on user endpoint

**Step 5: Collect findings**
```json
[
  {
    "severity": "critical",
    "category": "security",
    "subcategory": "sql-injection",
    "file": "app.py",
    "line": 11,
    "description": "SQL injection via f-string",
    "fix_suggestion": "Use parameterized query: cursor.execute('SELECT * FROM users WHERE id = %s', (id,))"
  },
  {
    "severity": "high",
    "category": "security",
    "subcategory": "auth-bypass",
    "file": "app.py",
    "line": 10,
    "description": "No authentication on user endpoint",
    "fix_suggestion": "Add @login_required decorator"
  }
]
```

**Step 6: Deduplicate**
- No duplicates in this case

**Step 7: Rank**
1. Critical: SQL injection (line 11)
2. High: Auth bypass (line 10)

**Step 8: Format**
Invoke `review-report.md` to generate PR comment.

## Error Handling

**Skill invocation failure:**
- Log warning
- Continue with other skills
- Report "Partial review (some skills failed)"

**Parse failure:**
- Report error immediately
- Don't attempt review

**Empty diff:**
- Report "No changes detected"

**Too large diff:**
- Warn if >1000 files or >50K lines
- Sample or focus on high-risk files

## Optimization Strategies

**Incremental review:**
- Cache findings from previous commits
- Only review changed sections
- Mark unchanged findings as "still present"

**Parallel execution:**
- Run concern skills in parallel
- Run language skills in parallel
- Aggregate results

**Smart sampling:**
- If PR has 1000 files, prioritize:
  1. Security-sensitive files (auth, crypto, db)
  2. Modified functions (not just whitespace)
  3. New files over edited files

## Configuration

Allow repo-specific configuration (`.autoreview.yml`):
```yaml
enabled_concerns:
  - security-injection
  - security-auth
  - concurrency
  - correctness
disabled_concerns:
  - code-quality  # Too noisy for this repo

severity_threshold: medium  # Only report medium and above

custom_rules:
  - pattern: "SECRET_KEY = "
    severity: critical
    message: "Secret key hardcoded"

ignore_paths:
  - tests/
  - vendor/
```

## Related Skills
- **diff-analysis** — Parse and understand PR diffs
- **security-injection** — Detect injection vulnerabilities
- **security-auth** — Detect auth/session issues
- **concurrency** — Detect concurrency bugs
- **correctness** — Detect logic errors
- **python**, **typescript**, etc. — Language-specific guidance
- **review-report**, **inline-comments**, etc. — Output formatting

## Quick Orchestrator Checklist
- [ ] Diff parsed successfully
- [ ] Languages identified
- [ ] Platforms detected
- [ ] Relevant concern skills invoked
- [ ] Language skills invoked
- [ ] Findings collected
- [ ] Deduplication applied
- [ ] Ranked by severity
- [ ] Output formatted
- [ ] Performance acceptable (<30s for typical PR)
