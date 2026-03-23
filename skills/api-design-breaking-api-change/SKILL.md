---
name: review-task-api-design-breaking-api-change
description: >
  Migrated review-task skill for Breaking API Change. Use this skill whenever diffs may
  introduce api-design issues on all, especially in all. Actively look for: Removing
  fields, changing types, or renaming without versioning or deprecation period. and
  report findings with high severity expectations and actionable fixes.
---

# Breaking API Change

## Source Lineage
- Original review task: `review-tasks/api-design/breaking-api-change.md`
- Migrated skill artifact: `skills/review-task-api-design-breaking-api-change/SKILL.md`

## Task Metadata
- Category: `api-design`
- Severity: `high`
- Platforms: `all`
- Languages: `all`

## Purpose
Removing fields, changing types, or renaming without versioning or deprecation period.

## Detection Heuristics
- Code patterns indicating the issue
- API design smells or anti-patterns
- Missing documentation or validation

## Eval Cases
### Case 1: Issue example
```java
// BUGGY CODE — should be detected
```
**Expected finding:** High — Removing fields, changing types, or renaming without versioning or deprecation period....

### Case 2: Alternative scenario
```java
// BUGGY CODE — should be detected
```
**Expected finding:** High — Similar issue in different context.

## Counter-Examples
### Counter 1: Proper implementation
```java
// CORRECT CODE — should NOT be flagged
```
**Why it's correct:** Follows API design best practices and standards.

### Counter 3: Missing response model and falsy cursor check on new endpoint
```python
from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI()

@app.get("/v1/items")
def list_items(cursor: Optional[int] = Query(default=None, ge=1)):
    effective_cursor = cursor or 0  # falsy check: None → 0; valid because ge=1 means 0 is never a real cursor
    rows = db.query("SELECT id, name FROM items WHERE id > ? LIMIT 50", effective_cursor)
    return {"items": rows, "next_cursor": rows[-1]["id"] if rows else None}
```
**Why it's correct:**
- This is a **new endpoint** being introduced for the first time; there is no prior published contract to break.
- The absence of an explicit Pydantic response model is a code-style / best-practice preference. It does not remove, rename, or retype any field that existing clients depend on, so it is **not** a breaking API change.
- `cursor or 0` is functionally equivalent to `cursor if cursor is not None else 0` here because the parameter is declared `ge=1`, making `0` an impossible valid input. The falsy check is a deliberate, correct implementation choice — not a type inconsistency or contract violation.
- Neither pattern constitutes removing or altering an existing published API surface.

### Counter 2: Deliberate design choices that are not breaking changes
```python
# New versioned route — /v2/ prefix is simply the URL path for this endpoint.
# There is no evidence a /v1/ route ever existed or that clients depend on it.
@app.route("/v2/users")
def get_users():
    # Cursor represented as an integer — a valid, deliberate internal design choice.
    # The type is consistent with the schema and has not been changed.
    cursor: int = request.args.get("cursor", 0, type=int)

    rows = db.query("SELECT id, name FROM users WHERE id > ? LIMIT 50", cursor)

    # Returning a plain dict is a style preference, not a contract violation.
    # No prior typed contract exists that is being broken here.
    return jsonify({"users": rows, "next_cursor": rows[-1]["id"] if rows else None})
```
**Why it's correct:**
- The `/v2/` prefix is part of the URL design for this endpoint; without evidence that a `/v1/` endpoint existed and is being removed or changed, this is not a breaking change.
- Using an integer as a cursor is a deliberate schema choice, not a type change from a previously published contract.
- Returning an untyped `dict` response is a code-style preference; flagging it as a breaking API change is a false positive unless a typed contract was previously in place and is now being altered.
- None of these patterns constitute removing, renaming, or re-typing a field that existing clients rely on.

## Binary Eval Assertions
- [ ] Detects issue in eval case 1
- [ ] Detects issue in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Does NOT flag counter-example 2 (versioned route prefix, integer cursor, untyped dict response)
- [ ] Does NOT flag counter-example 3 (new endpoint with no prior contract, missing response model, falsy cursor check)
- [ ] Provides actionable recommendation

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
