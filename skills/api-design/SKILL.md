---
name: api design
description: >
  Detect API design flaws: missing or inadequate input validation, pagination missing for large
  result sets, breaking API changes without versioning, and inconsistent response shapes. Trigger
  when reviewing API endpoints, route handlers, request validators, response serialization, or
  API versioning logic. Critical for API stability and developer experience.
---

# API Design Review

## Purpose
Review API endpoints for design and implementation flaws: input validation gaps, missing pagination, breaking changes, inconsistent responses, and poor versioning strategy. Ensures API stability, security, and usability.

## Scope
1. **Input Validation** — missing validation, weak regex, type coercion issues, injection vectors
2. **Missing Pagination** — unbounded result sets, memory exhaustion, slow responses
3. **Breaking API Changes** — removing fields, changing types, breaking existing clients
4. **Inconsistent Response Shape** — different error formats, optional fields appearing/disappearing
5. **API Versioning** — no versioning strategy, forced updates, backward compat broken

## Detection Strategy

### 1. Input Validation Red Flags
- **No validation** on request body/query parameters
- **Trusting client data** without sanitization
- **Weak regex** for email/URL validation (`.*@.*`, `/http.*/`)
- **Missing length limits** (DoS via large input)
- **No type checking** (JavaScript type coercion bugs)

**High-risk patterns:**
```python
# ❌ UNSAFE
@app.post('/user')
def create_user(req):
    username = req.json['username']  # No validation
    db.create_user(username)
```

### 2. Missing Pagination Red Flags
- **SELECT * without LIMIT**
- **Returning entire collection** in one response
- **No cursor/offset parameters**
- **Loading all results into memory** before sending

**High-risk patterns:**
```python
# ❌ UNSAFE
@app.get('/products')
def get_products():
    return db.query("SELECT * FROM products")  # Could be 1M rows
```

### 3. Breaking API Changes Red Flags
- **Removing fields** from response without deprecation period
- **Changing field types** (string → int, nullable → required)
- **Renaming fields** without alias
- **Changing error codes** (200 → 201 for same operation)
- **No API versioning** (breaking changes in same endpoint)

**High-risk patterns:**
```python
# ❌ BREAKING: Removed field
# Before: {"id": 1, "name": "Alice", "email": "alice@example.com"}
# After:  {"id": 1, "name": "Alice"}  # email removed without notice
```

### 4. Inconsistent Response Shape Red Flags
- **Different error formats** across endpoints
- **Sometimes array, sometimes object** for same resource
- **Optional fields** appearing/disappearing based on conditions
- **No schema enforcement** (Pydantic, JSON Schema)

**High-risk patterns:**
```python
# ❌ INCONSISTENT
@app.get('/users')
def get_users():
    return {"users": [...]}  # Wrapped

@app.get('/products')
def get_products():
    return [...]  # Not wrapped
```

### 5. API Versioning Red Flags
- **No versioning** (breaking changes in same URL)
- **Query param versioning** (`?v=2`, easy to miss)
- **No deprecation notices** for old versions
- **Forced updates** without grace period (mobile apps)

**High-risk patterns:**
```python
# ❌ UNSAFE: No versioning
@app.post('/order')  # Breaking change pushed directly
def create_order(req):
    # Changed required fields without version bump
```

## Platform-Specific Guidance

### Web/REST API
- **Primary risks:** Missing pagination, breaking changes, inconsistent errors
- **Key review areas:** Route handlers, response serialization, query building
- **Best practices:** API versioning (URL or header), OpenAPI spec, Pydantic validation

### GraphQL API
- **Primary risks:** Over-fetching, N+1 queries, no pagination on connections
- **Key review areas:** Resolvers, schema design, query complexity limits
- **Best practices:** Cursor-based pagination, DataLoader for batching, schema deprecation

### Mobile API
- **Primary risks:** Breaking changes affecting released apps, forced updates, missing backward compat
- **Key review areas:** API versioning, field deprecation, client version checks
- **Best practices:** Semantic versioning, min/max client version headers, graceful degradation

### Microservices API
- **Primary risks:** Breaking service contracts, inconsistent error propagation, no API governance
- **Key review areas:** Service contracts (OpenAPI/Protobuf), version negotiation
- **Best practices:** Contract testing (Pact), API gateway for versioning, schema registry

## Review Instructions

### Step 1: Validate Input Validation
```bash
# Find endpoints without validation
rg "@app\.(get|post|put|delete)" --type py -A 5 | rg -v "validator|pydantic|schema"
```

**Safe validation pattern:**
```python
# ✅ GOOD: Pydantic validation
from pydantic import BaseModel, EmailStr, constr

class CreateUserRequest(BaseModel):
    username: constr(min_length=3, max_length=20, regex='^[a-zA-Z0-9_]+$')
    email: EmailStr
    age: int = Field(ge=13, le=120)

@app.post('/user')
def create_user(req: CreateUserRequest):
    db.create_user(req.username, req.email, req.age)
```

### Step 2: Add Pagination
```bash
# Find queries without LIMIT
rg "SELECT \*|db\.query.*SELECT" --type py | rg -v "LIMIT"
```

**Safe pagination pattern:**
```python
# ✅ GOOD: Cursor-based pagination
@app.get('/products')
def get_products(cursor: Optional[str] = None, limit: int = 20):
    if limit > 100:
        limit = 100  # Max limit
    
    query = "SELECT * FROM products"
    if cursor:
        query += f" WHERE id > {cursor}"
    query += f" ORDER BY id LIMIT {limit + 1}"
    
    results = db.query(query)
    has_more = len(results) > limit
    items = results[:limit]
    
    return {
        "items": items,
        "next_cursor": items[-1]["id"] if has_more else None,
        "has_more": has_more
    }
```

### Step 3: Detect Breaking Changes
```bash
# Compare API schemas before/after
git diff main -- openapi.yaml
git diff main -- api/schema.py
```

**Safe evolution pattern:**
```python
# ✅ GOOD: Deprecation with alias
from pydantic import BaseModel, Field

class UserResponse(BaseModel):
    id: int
    full_name: str = Field(alias="name")  # Deprecated: use full_name
    name: str  # Keep for backward compat
    
    class Config:
        populate_by_name = True  # Accept both names
```

### Step 4: Enforce Response Consistency
```python
# ✅ GOOD: Consistent envelope
from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    data: T
    meta: dict = {}

class ApiError(BaseModel):
    error: str
    code: str
    details: dict = {}

@app.get('/users')
def get_users() -> ApiResponse[List[User]]:
    users = db.get_users()
    return ApiResponse(data=users, meta={"count": len(users)})

@app.exception_handler(Exception)
def handle_error(request, exc):
    return JSONResponse(
        status_code=500,
        content=ApiError(error=str(exc), code="INTERNAL_ERROR").dict()
    )
```

### Step 5: Implement API Versioning
```python
# ✅ GOOD: URL versioning
@app.get('/v1/users')
def get_users_v1():
    return [{"id": 1, "name": "Alice"}]

@app.get('/v2/users')
def get_users_v2():
    return {"users": [{"id": 1, "full_name": "Alice Smith", "email": "alice@example.com"}]}

# ✅ GOOD: Header versioning
@app.get('/users')
def get_users(request: Request):
    version = request.headers.get('API-Version', '1')
    if version == '2':
        return get_users_v2()
    return get_users_v1()
```

## Platform-Specific Examples

### Mobile: Backward Compatibility
```python
# ✅ GOOD: Support old and new clients
@app.post('/order')
def create_order(req: Request):
    client_version = req.headers.get('App-Version', '1.0.0')
    
    # New field required in v2+
    if semver.compare(client_version, '2.0.0') >= 0:
        if 'delivery_address' not in req.json:
            raise ValidationError("delivery_address required in v2+")
    else:
        # Old clients: use default address
        req.json.setdefault('delivery_address', get_user_default_address())
    
    return process_order(req.json)
```

### GraphQL: Pagination
```graphql
# ✅ GOOD: Connection pattern
type Query {
  products(first: Int, after: String): ProductConnection!
}

type ProductConnection {
  edges: [ProductEdge!]!
  pageInfo: PageInfo!
}

type ProductEdge {
  node: Product!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  endCursor: String
}
```

### Microservices: Contract Versioning
```python
# ✅ GOOD: OpenAPI with versioning
from fastapi import FastAPI, Header
from typing import Optional

app = FastAPI()

@app.post('/orders', responses={
    200: {"model": OrderResponseV2},
    "4XX": {"model": ErrorResponse}
})
def create_order(order: OrderRequest, accept_version: Optional[str] = Header("1")):
    if accept_version == "2":
        return create_order_v2(order)
    return create_order_v1(order)
```

## Counter-Examples (Safe Code — Do NOT Flag)

### Safe Cursor Pagination with Pydantic-Constrained Cursor

When a cursor field carries a `ge=1` (or similar) Pydantic constraint, the value `0` is **impossible** — Pydantic rejects it before the handler runs. The `or 0` fallback is therefore a safe default for "no cursor" and must **not** be flagged as a falsy-zero bug.

```python
# ✅ SAFE: cursor ge=1 makes `req.cursor or 0` correct
from pydantic import BaseModel, Field
from typing import Optional

class ProductsRequest(BaseModel):
    cursor: Optional[int] = Field(default=None, ge=1)  # 0 is impossible; None means "start"
    limit: int = Field(default=20, ge=1, le=100)

@app.get('/products')
def get_products(req: ProductsRequest = Depends()):
    after_id = req.cursor or 0  # Safe: 0 means "from the beginning"; cursor=0 is rejected by Pydantic
    rows = db.query(
        "SELECT * FROM products WHERE id > ? ORDER BY id LIMIT ?",
        after_id, req.limit + 1
    )
    has_more = len(rows) > req.limit
    items = rows[:req.limit]
    return {
        "items": items,
        "next_cursor": items[-1]["id"] if has_more else None,
        "has_more": has_more,
    }
```

**Why this is safe — do not raise findings for:**
- **`req.cursor or 0`** — `cursor` is declared `ge=1`, so Pydantic will reject any request that supplies `cursor=0` with a 422 before this code runs. The `or 0` branch is only reached when `cursor` is `None` (omitted), making `0` a safe sentinel for "fetch from the beginning".
- **`has_more` presence** — the field is always present in the response; its value is a boolean derived from the fetch-one-extra pattern. This is a well-established pagination idiom, not a bug.

**Key principle:** When Pydantic (or any schema validator) enforces a lower bound that excludes a falsy value, `field or default` patterns that rely on that exclusion are valid. Flag only cases where no such constraint exists.

### Null/Non-Null `next_cursor` as Pagination Signal (No `has_more` Required)

A cursor pagination response that omits a separate `has_more` field and relies solely on `next_cursor` being `null` vs. a value is a **well-established, correct pattern**. Do not flag the absence of `has_more` as a bug or "fragile" design.

```python
# ✅ SAFE: null/non-null next_cursor is a complete and correct pagination signal
@app.get('/items')
def get_items(cursor: Optional[str] = None, limit: int = 20):
    rows = db.query(
        "SELECT * FROM items WHERE id > ? ORDER BY id LIMIT ?",
        cursor or 0, limit + 1
    )
    items = rows[:limit]
    return {
        "items": items,
        "next_cursor": items[-1]["id"] if len(rows) > limit else None,
        # No has_more field — next_cursor being non-null IS has_more
    }
```

**Why this is safe — do not raise findings for:**
- **Missing `has_more` field** — `next_cursor: null` unambiguously signals no more pages; `next_cursor: <id>` signals more pages exist. This is a standard industry pattern (GitHub API, Stripe API, etc.) and is not fragile or incomplete.

### Cursor Without Lower-Bound Constraint Is Not a Security Issue

A cursor parameter with no `ge=0` lower-bound constraint is **not** a security vulnerability when the query uses parameterized statements. Negative cursor values with `id > -5` simply return rows from the beginning — same as `id > 0` — which is harmless. Do not flag the absence of `ge=0` as a medium or security issue.

```python
# ✅ SAFE: No ge=0 on cursor — parameterized query makes negative values harmless
class ItemsRequest(BaseModel):
    cursor: Optional[int] = None  # No ge constraint; negative values are safe
    limit: int = Field(default=20, ge=1, le=100)

@app.get('/items')
def get_items(req: ItemsRequest = Depends()):
    rows = db.query(
        "SELECT * FROM items WHERE id > ? ORDER BY id LIMIT ?",
        req.cursor or 0, req.limit + 1  # Parameterized — no injection risk
    )
    items = rows[:req.limit]
    return {"items": items, "next_cursor": items[-1]["id"] if len(rows) > req.limit else None}
```

**Why this is safe — do not raise findings for:**
- **No `ge=0` on cursor** — with a parameterized query there is no injection risk. A negative cursor returns rows with `id > -N`, which behaves identically to starting from the beginning. This is a correctness non-issue, not a security issue. Only flag cursor validation if the cursor is interpolated directly into a query string.

### Correct Keyset Pagination Cursor and FastAPI Pydantic GET Parameters

The `rows[-1]` index used as the next cursor in keyset pagination is correct, and FastAPI GET handlers that accept a Pydantic model directly (without `Depends()`) are valid. Do not flag either pattern.

```python
# ✅ SAFE: correct cursor index and valid FastAPI Pydantic GET parameter binding
from pydantic import BaseModel, Field
from typing import Optional

class ProductsRequest(BaseModel):
    cursor: Optional[int] = None
    limit: int = Field(default=20, ge=1, le=100)

@app.get('/products')
def get_products(req: ProductsRequest):  # No Depends() — FastAPI accepts Pydantic models as query params in GET handlers
    rows = db.query(
        "SELECT * FROM products WHERE id > ? ORDER BY id LIMIT ?",
        req.cursor or 0, req.limit + 1  # fetch one extra to detect has_more
    )
    has_more = len(rows) > req.limit
    items = rows[:req.limit]
    return {
        "items": items,
        # rows[-1] here is rows[req.limit] — the probe row's ID, correctly excluded from items
        "next_cursor": rows[-1]["id"] if has_more else None,
    }
```

**Why this is safe — do not raise findings for:**
- **`rows[-1]` as next cursor** — when `has_more` is true, `rows` contains `req.limit + 1` elements, so `rows[-1]` is `rows[req.limit]`, the probe row. That row is excluded from `items` (sliced to `[:req.limit]`) and its ID is used as the cursor. The next query's `WHERE id > cursor` then correctly starts after it. This is standard keyset/cursor pagination and is not a bug.
- **Pydantic model parameter without `Depends()`** — FastAPI automatically treats fields of a Pydantic `BaseModel` parameter as query parameters in GET route handlers. `Depends()` is optional; omitting it is valid and documented FastAPI behavior. Do not flag its absence as an error.

## Migration Coverage

## OWASP References
- [Input Validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [Bean Validation](https://cheatsheetseries.owasp.org/cheatsheets/Bean_Validation_Cheat_Sheet.html)
- [REST Security](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)

## Quick Checklist
- [ ] All inputs validated with schema (Pydantic, JSON Schema, etc.)
- [ ] Pagination implemented for list endpoints (limit, cursor)
- [ ] API versioned (URL or header)
- [ ] Breaking changes go through deprecation period
- [ ] Response shape consistent across endpoints
- [ ] Error responses follow standard format
- [ ] OpenAPI/Swagger spec maintained
- [ ] Max limits enforced (page size, request body size)
- [ ] Field aliases for backward compat during renames
- [ ] Client version header checked for mobile APIs
