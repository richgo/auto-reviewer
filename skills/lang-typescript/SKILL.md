---
name: lang typescript
description: >
  TypeScript and Node.js code review guidance: Express/NestJS security, async/await patterns,
  type safety, prototype pollution, package vulnerabilities. Trigger when reviewing .ts, .tsx,
  .js, .jsx files or Node.js backend code.
---

# Language-Specific Review: TypeScript / Node.js

## Purpose
Provide TypeScript and Node.js-specific security, correctness, and performance guidance for code review.

## Scope
- **Framework security:** Express, NestJS, Next.js
- **Language pitfalls:** Type coercion, prototype pollution, async misuse
- **Common anti-patterns:** Missing error handling, callback hell, blocking event loop
- **Security-specific:** SQL injection, XSS, command injection, SSRF

## Framework-Specific Guidance

### Express.js Security
```typescript
// ❌ UNSAFE: XSS via template injection
app.get('/search', (req, res) => {
  res.send(`<h1>Results for: ${req.query.q}</h1>`);
});

// ✅ SAFE: Use template engine with auto-escaping
app.get('/search', (req, res) => {
  res.render('search', { query: req.query.q });
});

// ❌ UNSAFE: Missing input validation
app.post('/user', (req, res) => {
  User.create(req.body);
});

// ✅ SAFE: Validate with Joi/Zod
import { z } from 'zod';
const UserSchema = z.object({
  name: z.string().max(100),
  email: z.string().email()
});

app.post('/user', (req, res) => {
  const data = UserSchema.parse(req.body);
  User.create(data);
});

// ❌ UNSAFE: SQL injection
db.query(`SELECT * FROM users WHERE id = ${req.params.id}`);

// ✅ SAFE: Parameterized query
db.query('SELECT * FROM users WHERE id = ?', [req.params.id]);
```

### NestJS Security
```typescript
// ✅ Use ValidationPipe globally
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,  // Strip unknown properties
    forbidNonWhitelisted: true,  // Throw if unknown properties
    transform: true
  }));
  await app.listen(3000);
}

// ✅ DTOs with class-validator
import { IsEmail, IsString, MaxLength } from 'class-validator';
export class CreateUserDto {
  @IsString()
  @MaxLength(100)
  name: string;

  @IsEmail()
  email: string;
}
```

### Next.js Security
```typescript
// ❌ UNSAFE: API route without validation
export default function handler(req, res) {
  const { id } = req.query;
  const user = db.query(`SELECT * FROM users WHERE id = ${id}`);
  res.json(user);
}

// ✅ SAFE: Validate and parameterize
export default function handler(req, res) {
  const id = parseInt(req.query.id as string, 10);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'Invalid ID' });
  }
  const user = db.query('SELECT * FROM users WHERE id = ?', [id]);
  res.json(user);
}
```

## Common TypeScript Pitfalls

### 1. Type Coercion
```typescript
// ❌ UNSAFE: == allows type coercion
if (value == null) { ... }  // Matches null and undefined
if (user.age == '18') { ... }  // Type coercion

// ✅ SAFE: === for strict equality
if (value === null || value === undefined) { ... }
if (user.age === 18) { ... }
```

### 2. Prototype Pollution
```typescript
// ❌ UNSAFE: Assigning to object from user input
function merge(target, source) {
  for (let key in source) {
    target[key] = source[key];  // Pollutes prototype if key is '__proto__'
  }
}

// ✅ SAFE: Check for prototype keys
function merge(target, source) {
  for (let key in source) {
    if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
      continue;
    }
    if (Object.prototype.hasOwnProperty.call(source, key)) {
      target[key] = source[key];
    }
  }
}
```

### 3. Async/Await Misuse
```typescript
// ❌ INEFFICIENT: Sequential awaits
async function fetchAll(ids: string[]) {
  const results = [];
  for (const id of ids) {
    results.push(await fetchItem(id));  // Serial
  }
  return results;
}

// ✅ EFFICIENT: Parallel awaits
async function fetchAll(ids: string[]) {
  return Promise.all(ids.map(id => fetchItem(id)));
}

// ❌ UNSAFE: Unhandled rejection
async function process() {
  await riskyOperation();  // If no try/catch, crashes on rejection
}

// ✅ SAFE: Handle errors
async function process() {
  try {
    await riskyOperation();
  } catch (error) {
    logger.error('Operation failed', error);
    throw new Error('Processing failed');
  }
}
```

### 4. Missing Null Checks
```typescript
// ❌ UNSAFE: Optional chaining not used
const name = user.profile.name;  // Crash if user or profile is null

// ✅ SAFE: Optional chaining
const name = user?.profile?.name ?? 'Unknown';
```

### 5. Any Type Escape Hatch
```typescript
// ❌ BAD: Losing type safety
function process(data: any) {
  return data.value.toUpperCase();  // No compile-time check
}

// ✅ GOOD: Use proper types
interface Data {
  value: string;
}
function process(data: Data) {
  return data.value.toUpperCase();
}
```

## Security-Specific Patterns

### Command Injection
```typescript
// ❌ UNSAFE
import { exec } from 'child_process';
exec(`ping -c 4 ${req.query.host}`);

// ✅ SAFE
import { execFile } from 'child_process';
execFile('ping', ['-c', '4', req.query.host]);
```

### Path Traversal
```typescript
// ❌ UNSAFE
import fs from 'fs';
app.get('/download', (req, res) => {
  const file = fs.readFileSync(`/uploads/${req.query.file}`);
  res.send(file);
});

// ✅ SAFE
import path from 'path';
app.get('/download', (req, res) => {
  const filename = path.basename(req.query.file);
  const filepath = path.join('/uploads', filename);
  if (!filepath.startsWith('/uploads')) {
    return res.status(400).send('Invalid path');
  }
  const file = fs.readFileSync(filepath);
  res.send(file);
});
```

### SSRF
```typescript
// ❌ UNSAFE
app.get('/proxy', async (req, res) => {
  const response = await fetch(req.query.url);
  res.send(await response.text());
});

// ✅ SAFE: Allowlist domains
const ALLOWED_DOMAINS = ['api.example.com'];
app.get('/proxy', async (req, res) => {
  const url = new URL(req.query.url);
  if (!ALLOWED_DOMAINS.includes(url.hostname)) {
    return res.status(400).send('Domain not allowed');
  }
  const response = await fetch(url.toString());
  res.send(await response.text());
});
```

## TypeScript Idioms to Encourage

### 1. Strict TypeScript Config
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUncheckedIndexedAccess": true
  }
}
```

### 2. Discriminated Unions
```typescript
type Result<T> =
  | { success: true; value: T }
  | { success: false; error: string };

function handle(result: Result<User>) {
  if (result.success) {
    return result.value.name;  // Type-safe access
  } else {
    return result.error;
  }
}
```

### 3. Zod for Runtime Validation
```typescript
import { z } from 'zod';
const UserSchema = z.object({
  id: z.number(),
  email: z.string().email(),
  age: z.number().min(0).max(120)
});

type User = z.infer<typeof UserSchema>;  // Derive TS type from schema
```

## Anti-Patterns to Flag

1. **Using `any` excessively** — Defeats type safety
2. **Ignoring TypeScript errors with `@ts-ignore`** — Technical debt
3. **Not handling promise rejections** — Unhandled crashes
4. **Blocking the event loop** — CPU-intensive sync work
5. **Missing error handling in middleware** — Silent failures

## Related Security Tasks

## Quick TypeScript Security Checklist
- [ ] No SQL injection (parameterized queries)
- [ ] No XSS (template engines with auto-escape)
- [ ] No command injection (use execFile with args)
- [ ] Input validation (Joi/Zod) on all user inputs
- [ ] No prototype pollution (check __proto__, constructor)
- [ ] SSRF protected (allowlist domains)
- [ ] Promises have error handlers
- [ ] No sensitive data in logs
- [ ] HTTPS enforced
- [ ] Secrets from environment, not hardcoded
