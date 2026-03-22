---
name: security-api
description: >
  Detect API-specific security vulnerabilities: GraphQL injection and DoS, REST API authentication/
  authorization flaws, rate limiting gaps, and transaction authorization bypass. Trigger when
  reviewing API endpoints, GraphQL resolvers, REST controllers, or any code handling API requests,
  especially financial transactions or sensitive operations.
---

# Security Review: API Vulnerabilities

## Purpose
Review API code for security issues specific to REST and GraphQL interfaces: injection attacks, authorization bypass, rate limiting gaps, denial of service through expensive queries, and transaction authorization flaws.

## Scope
This skill covers three major API security classes:
1. **GraphQL Security** — injection, DoS via deep nesting/batching, introspection exposure, authorization bypass in resolvers
2. **REST Security** — IDOR, BOLA, excessive data exposure, function-level authorization, rate limiting
3. **Transaction Authorization** — payment manipulation, amount tampering, insufficient authorization for high-value operations

## Detection Strategy

### 1. GraphQL Security Red Flags
- **Introspection enabled in production** — attackers can discover schema
- **No query depth limiting** — allows deeply nested queries (DoS)
- **No query complexity scoring** — allows expensive batched queries
- **String concatenation in resolvers** — SQL/NoSQL injection
- **Missing authorization checks per field** — over-fetching sensitive data
- **Circular references without depth limits**

**High-risk patterns:**
```graphql
# ❌ UNSAFE: No depth limit
{
  user {
    posts {
      author {
        posts {
          author {
            posts { ... }
          }
        }
      }
    }
  }
}
```

### 2. REST Security Red Flags
- **Direct object reference without authorization** — IDOR/BOLA
- **Function-level authorization missing** — regular user accessing admin endpoints
- **Excessive data exposure** — returning full objects when only subset needed
- **No rate limiting** — brute force attacks
- **Verbose error messages** — leaking stack traces, database schema

**High-risk patterns:**
```javascript
// ❌ UNSAFE: IDOR
app.get('/api/user/:id', (req, res) => {
  const user = db.findById(req.params.id); // No ownership check
  res.json(user);
});
```

### 3. Transaction Authorization Red Flags
- **Amount not re-validated server-side** — client can manipulate
- **Missing additional auth for high-value transactions**
- **Payment amount in client-side request without HMAC**
- **Transaction replay without idempotency keys**
- **No fraud detection checks before processing**

**High-risk patterns:**
```javascript
// ❌ UNSAFE: Client-controlled amount
app.post('/api/payment', (req, res) => {
  const { amount, recipient } = req.body;
  processPayment(req.user.id, recipient, amount); // Amount from client!
});
```

## Platform-Specific Guidance

### Web API
- **Primary risks:** IDOR, function-level auth bypass, excessive data exposure, rate limiting
- **Key review areas:** REST controllers, middleware chains, response serialization, rate limit configuration
- **OWASP references:** REST_Security, REST_Assessment, Authorization

### GraphQL API
- **Primary risks:** Introspection exposure, query complexity DoS, field-level authorization, injection in resolvers
- **Key review areas:** Schema definitions, resolvers, query complexity middleware, introspection toggle
- **OWASP references:** GraphQL

### Microservices API
- **Primary risks:** Internal API trust assumptions, missing service-to-service auth, transaction boundary violations
- **Key review areas:** Gateway auth passthrough, service mesh policies, distributed transaction handling
- **OWASP references:** Microservices_Security

## Review Instructions

### Step 1: Audit GraphQL Security

**Check introspection:**
```javascript
// ❌ UNSAFE
const server = new ApolloServer({
  introspection: true, // In production!
});
```

**Check query limits:**
```javascript
// ✅ SAFE
const server = new ApolloServer({
  plugins: [
    depthLimitPlugin({ maxDepth: 5 }),
    queryComplexityPlugin({ maxComplexity: 1000 })
  ]
});
```

**Check resolver authorization:**
```javascript
// ❌ UNSAFE
const resolvers = {
  Query: {
    user: (parent, { id }, context) => {
      return db.users.findById(id); // No auth check
    }
  }
};

// ✅ SAFE
const resolvers = {
  Query: {
    user: (parent, { id }, context) => {
      if (!context.user) throw new AuthenticationError();
      if (context.user.id !== id && !context.user.isAdmin) {
        throw new ForbiddenError();
      }
      return db.users.findById(id);
    }
  }
};
```

**Check for injection in resolvers:**
```javascript
// ❌ UNSAFE
const resolvers = {
  Query: {
    searchUsers: (parent, { query }, context) => {
      return db.query(`SELECT * FROM users WHERE name LIKE '%${query}%'`);
    }
  }
};
```

### Step 2: Audit REST Security

**Check for IDOR/BOLA:**
```javascript
// ❌ UNSAFE: No ownership check
app.get('/api/documents/:id', async (req, res) => {
  const doc = await Document.findById(req.params.id);
  res.json(doc);
});

// ✅ SAFE: Verify ownership
app.get('/api/documents/:id', async (req, res) => {
  const doc = await Document.findOne({
    _id: req.params.id,
    owner: req.user.id
  });
  if (!doc) return res.status(404).json({ error: 'Not found' });
  res.json(doc);
});
```

**Check for function-level authorization:**
```javascript
// ❌ UNSAFE: No role check
app.delete('/api/users/:id', async (req, res) => {
  await User.deleteById(req.params.id);
  res.json({ success: true });
});

// ✅ SAFE: Admin-only
app.delete('/api/users/:id', requireAdmin, async (req, res) => {
  await User.deleteById(req.params.id);
  res.json({ success: true });
});
```

**Check for excessive data exposure:**
```javascript
// ❌ UNSAFE: Exposing password hash
app.get('/api/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  res.json(user); // Includes passwordHash, email, internal fields
});

// ✅ SAFE: Projection
app.get('/api/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id)
    .select('name username avatarUrl');
  res.json(user);
});
```

**Check rate limiting:**
```javascript
// ❌ UNSAFE: No rate limit
app.post('/api/auth/login', loginHandler);

// ✅ SAFE
const rateLimit = require('express-rate-limit');
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5
});
app.post('/api/auth/login', loginLimiter, loginHandler);
```

### Step 3: Audit Transaction Authorization

**Check amount validation:**
```javascript
// ❌ UNSAFE: Trust client amount
app.post('/api/checkout', async (req, res) => {
  const { cartId, amount } = req.body;
  await processPayment(req.user.id, amount);
});

// ✅ SAFE: Recalculate server-side
app.post('/api/checkout', async (req, res) => {
  const { cartId } = req.body;
  const cart = await Cart.findById(cartId);
  const amount = cart.items.reduce((sum, item) => sum + item.price, 0);
  await processPayment(req.user.id, amount);
});
```

**Check high-value transaction auth:**
```javascript
// ❌ UNSAFE: No additional auth for large amounts
app.post('/api/transfer', async (req, res) => {
  const { recipient, amount } = req.body;
  await transfer(req.user.id, recipient, amount);
});

// ✅ SAFE: Require 2FA for large amounts
app.post('/api/transfer', async (req, res) => {
  const { recipient, amount, totpCode } = req.body;
  if (amount > 10000 && !verifyTOTP(req.user.id, totpCode)) {
    return res.status(403).json({ error: 'TOTP required for large transfers' });
  }
  await transfer(req.user.id, recipient, amount);
});
```

**Check idempotency:**
```javascript
// ❌ UNSAFE: No idempotency key
app.post('/api/payment', async (req, res) => {
  await processPayment(req.body);
});

// ✅ SAFE: Idempotency key
app.post('/api/payment', async (req, res) => {
  const idempotencyKey = req.headers['idempotency-key'];
  if (!idempotencyKey) return res.status(400).json({ error: 'Idempotency-Key required' });
  
  const existing = await PaymentAttempt.findByKey(idempotencyKey);
  if (existing) return res.json(existing.response);
  
  const result = await processPayment(req.body);
  await PaymentAttempt.create({ key: idempotencyKey, response: result });
  res.json(result);
});
```

## Examples

### ✅ SAFE: GraphQL with Depth Limit
```javascript
const { ApolloServer } = require('apollo-server');
const depthLimit = require('graphql-depth-limit');

const server = new ApolloServer({
  schema,
  introspection: process.env.NODE_ENV !== 'production',
  validationRules: [depthLimit(5)]
});
```

### ❌ UNSAFE: GraphQL No Limits
```javascript
const server = new ApolloServer({ schema });
```
**Finding:** High — GraphQL introspection enabled in production + no query depth limit. Vulnerable to schema discovery and DoS.

### ✅ SAFE: REST with Authorization
```javascript
app.get('/api/orders/:id', async (req, res) => {
  const order = await Order.findOne({
    _id: req.params.id,
    userId: req.user.id
  });
  if (!order) return res.status(404).json({ error: 'Not found' });
  res.json(order);
});
```

### ❌ UNSAFE: REST IDOR
```javascript
app.get('/api/orders/:id', async (req, res) => {
  const order = await Order.findById(req.params.id);
  res.json(order);
});
```
**Finding:** Critical — IDOR vulnerability. Any user can access any order by guessing ID.

### ✅ SAFE: Transaction with Server-Side Validation
```javascript
app.post('/api/purchase', async (req, res) => {
  const { productId, quantity } = req.body;
  const product = await Product.findById(productId);
  const amount = product.price * quantity;
  await processPayment(req.user.id, amount);
});
```

### ❌ UNSAFE: Transaction with Client Amount
```javascript
app.post('/api/purchase', async (req, res) => {
  const { amount } = req.body;
  await processPayment(req.user.id, amount);
});
```
**Finding:** Critical — Client-controlled payment amount. Attacker can set amount to $0.01 for any purchase.

## Migration Coverage
Review guidance from the legacy review-task corpus is now consolidated in this skill and validated via the migration inventory (`openspec/changes/research-changes/artifacts/review-task-skill-map.csv`).

## OWASP References
- [GraphQL Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html)
- [REST Security](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
- [REST Assessment](https://cheatsheetseries.owasp.org/cheatsheets/REST_Assessment_Cheat_Sheet.html)
- [Transaction Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html)
- [Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

## Quick Checklist
- [ ] GraphQL introspection disabled in production
- [ ] GraphQL query depth and complexity limits enforced
- [ ] All resolvers include authorization checks
- [ ] REST endpoints verify resource ownership
- [ ] Function-level authorization for admin/privileged endpoints
- [ ] Rate limiting on authentication and sensitive endpoints
- [ ] Transaction amounts validated server-side
- [ ] High-value transactions require additional authentication
- [ ] Idempotency keys enforced for financial operations
- [ ] Minimal data exposure (projection/serialization)
