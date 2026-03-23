---
name: review-task-reliability-resource-cleanup
description: >
  Migrated review-task skill for Resource Cleanup. Use this skill whenever diffs may
  introduce reliability issues on all, especially in all. Actively look for: File
  handles, database connections, network sockets, or locks opened but not properly
  closed in all code paths (including... and report findings with high severity
  expectations and actionable fixes.
---

# Resource Cleanup

## Source Lineage
- Original review task: `review-tasks/reliability/resource-cleanup.md`
- Migrated skill artifact: `skills/review-task-reliability-resource-cleanup/SKILL.md`

## Task Metadata
- Category: `reliability`
- Severity: `high`
- Platforms: `all`
- Languages: `all`

## Purpose
File handles, database connections, network sockets, or locks opened but not properly closed in all code paths (including error paths), causing resource exhaustion.

## Detection Heuristics
- `open()` / `new Connection()` without `finally` block or context manager
- Resources assigned but not closed if exception occurs between open and close
- Missing `using`/`with`/`try-with-resources` for disposable resources
- Connection pool exhaustion patterns (checkout without return)

## Eval Cases
### Case 1: File not closed on error
```python
def read_config(path):
    f = open(path)
    data = json.load(f)  # if this throws, f is never closed
    f.close()
    return data
```
**Expected finding:** High — Resource leak. If `json.load()` raises, file handle is never closed. Use context manager: `with open(path) as f:`

### Case 2: JDBC connection leak
```java
public List<User> getUsers() throws SQLException {
    Connection conn = dataSource.getConnection();
    Statement stmt = conn.createStatement();
    ResultSet rs = stmt.executeQuery("SELECT * FROM users");
    List<User> users = mapResults(rs);
    conn.close(); // never reached if mapResults throws
    return users;
}
```
**Expected finding:** High — Connection leak. Use try-with-resources: `try (Connection conn = ...; Statement stmt = ...)`

## Counter-Examples
### Counter 1: Context manager
```python
def read_config(path):
    with open(path) as f:
        return json.load(f)
```
**Why it's correct:** `with` guarantees file is closed even on exception.

## Binary Eval Assertions
- [ ] Detects resource leak in eval case 1
- [ ] Detects connection leak in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding suggests context manager / try-with-resources
- [ ] Severity assigned as high

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
