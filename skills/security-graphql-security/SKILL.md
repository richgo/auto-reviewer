---
name: security graphql security
description: >
  GraphQL Security Issues. Use this skill whenever diffs
  may introduce security issues on web, api, especially in JavaScript, TypeScript,
  Python, Java. Actively look for: GraphQL security issues include query
  depth/complexity attacks (DoS), introspection exposure in production, missing
  authorization on fields, batching attacks,... and report findings with high severity
  expectations and actionable fixes.
---

# GraphQL Security Issues
## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `web, api`
- Languages: `JavaScript, TypeScript, Python, Java`

## Purpose
GraphQL security issues include query depth/complexity attacks (DoS), introspection exposure in production, missing authorization on fields, batching attacks, and injection via unsanitized variables in resolvers.

## Detection Heuristics
- Introspection enabled in production environments
- No query depth or complexity limits (allows nested query DoS)
- Missing field-level authorization checks in resolvers
- Batch query limits not enforced (allows amplification attacks)
- Direct database queries in resolvers without parameterization
- Missing rate limiting on GraphQL endpoint

## Eval Cases
### Case 1: Introspection enabled in production
```javascript
// BUGGY CODE — should be detected
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: true, // Exposed in production!
  playground: true
});
```
**Expected finding:** Medium — GraphQL introspection enabled in production. Exposes full schema to attackers for reconnaissance. Disable introspection and playground in production: `introspection: process.env.NODE_ENV !== 'production'`.

### Case 2: No query depth limit
```python
# BUGGY CODE — should be detected
from ariadne import make_executable_schema
schema = make_executable_schema(type_defs, query, mutation)
# No depth limiting middleware
```
**Expected finding:** High — Missing query depth/complexity limits. Attacker can craft deeply nested queries causing DoS: `{users{posts{comments{author{posts{comments...}}}}}}`. Use validation rules to limit depth (< 10) and complexity.

### Case 3: Missing field authorization
```typescript
// BUGGY CODE — should be detected
const resolvers = {
  User: {
    email: (parent) => parent.email, // No auth check!
    ssn: (parent) => parent.ssn
  }
};
```
**Expected finding:** High — Missing field-level authorization. Sensitive fields (email, SSN) exposed without checking requester permissions. Add resolver-level auth checks or use graphql-shield for declarative permissions.

## Counter-Examples
### Counter 1: Depth limiting with graphql-depth-limit
```javascript
// CORRECT CODE — should NOT be flagged
const depthLimit = require('graphql-depth-limit');
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production',
  validationRules: [depthLimit(10)]
});
```
**Why it's correct:** Introspection disabled in prod, query depth limited to 10 levels.

### Counter 2: Field-level authorization
```typescript
// CORRECT CODE — should NOT be flagged
const resolvers = {
  User: {
    email: (parent, args, context) => {
      if (!context.user || context.user.id !== parent.id) {
        throw new ForbiddenError('Unauthorized');
      }
      return parent.email;
    }
  }
};
```
**Why it's correct:** Authorization check before returning sensitive field.

## Binary Eval Assertions
- [ ] Detects introspection in production in eval case 1
- [ ] Detects missing depth limit in eval case 2
- [ ] Detects missing field authorization in eval case 3
- [ ] Does NOT flag counter-example 1 (depth limiting)
- [ ] Does NOT flag counter-example 2 (field authorization)
- [ ] Finding references OWASP GraphQL Cheat Sheet
- [ ] Severity assigned as high for authorization gaps
