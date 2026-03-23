---
name: code-quality
description: >
  Detect code quality issues: dead/unreachable code, DRY violations with duplicated logic, poor
  naming and readability, missing or inadequate documentation, and excessive complexity (cyclomatic,
  cognitive). Trigger when reviewing any code, especially complex functions, duplicated patterns,
  unclear variable names, or undocumented public APIs. Enhances maintainability and team velocity.
---

# Code Quality Review

## Purpose
Review code for maintainability and readability issues: dead code, duplication (DRY violations), poor naming, missing documentation, and excessive complexity. Improves long-term codebase health and developer experience.

## Scope
1. **Dead Code** — unreachable code, unused functions/variables, commented-out code
2. **DRY Violations** — copy-pasted logic, repeated patterns without abstraction
3. **Naming & Readability** — unclear names, inconsistent conventions, deeply nested logic
4. **Missing Documentation** — undocumented public APIs, complex logic without comments, missing README
5. **Excessive Complexity** — high cyclomatic complexity, cognitive overload, god objects

## Detection Strategy

### 1. Dead Code Red Flags
- **Unreachable code** after return/break/continue
- **Unused imports** and functions
- **Commented-out code blocks** (remove, don't comment)
- **Conditional always false** (`if False:`, `if (0)`)
- **Unused function parameters**

**High-risk patterns:**
```python
# ❌ DEAD CODE
def process():
    return result
    print("This never runs")  # Unreachable
    
def unused_function():  # Never called
    pass

# import pandas as pd  # Commented-out import
```

### 2. DRY Violations Red Flags
- **Copy-pasted functions** with minor variations
- **Repeated validation logic** across endpoints
- **Duplicated constants** in multiple files
- **Similar if/else chains** that could be a lookup table
- **Magic numbers** repeated throughout code

**High-risk patterns:**
```python
# ❌ DRY VIOLATION
def calculate_discount_bronze(price):
    return price * 0.95

def calculate_discount_silver(price):
    return price * 0.90

def calculate_discount_gold(price):
    return price * 0.85
```

### 3. Naming & Readability Red Flags
- **Single-letter variables** (except loop counters)
- **Abbreviations without explanation** (`usrMgr`, `tmpData`)
- **Inconsistent naming conventions** (camelCase and snake_case mixed)
- **Magic numbers without constants** (`if x > 86400`)
- **Deeply nested code** (>3 levels)

**High-risk patterns:**
```python
# ❌ UNCLEAR
def proc(d):
    for x in d:
        if x > 100:
            for y in x:
                if y:
                    return y
```

### 4. Missing Documentation Red Flags
- **Public APIs without docstrings**
- **Complex algorithms without explanation**
- **No README** in project root
- **No inline comments** for non-obvious logic
- **Type hints missing** (Python, TypeScript)

**High-risk patterns:**
```python
# ❌ NO DOCS
def calculate_tax(amount, state, category):
    if state in ['CA', 'NY']:
        if category == 'food':
            return amount * 0.08
        return amount * 0.10
    return amount * 0.05
```

### 5. Excessive Complexity Red Flags
- **Cyclomatic complexity >10** (too many branches)
- **Functions >50 lines** (god functions)
- **Classes with >10 methods** (god objects)
- **Deeply nested conditionals** (>3 levels)
- **Long parameter lists** (>4 parameters)

**High-risk patterns:**
```python
# ❌ COMPLEX: Cyclomatic complexity = 12
def process_order(order, user, payment, shipping, discount, taxes):
    if order.status == 'pending':
        if user.is_verified:
            if payment.is_valid:
                if shipping.is_available:
                    if discount.is_applicable:
                        # ... 50 more lines
```

## Platform-Specific Guidance

### Web/API
- **Primary risks:** God objects (services with 20+ methods), magic numbers, missing API docs
- **Key review areas:** Route handlers, service classes, utility functions
- **Best practices:** OpenAPI docs, small focused functions, constants file

### Android
- **Primary risks:** God Activities/Fragments, R.string not used, deprecated APIs without migration
- **Key review areas:** Activity/Fragment lifecycle methods, ViewModels, hardcoded strings
- **Best practices:** MVVM, string resources, accessibility labels, Kotlin docs

### iOS
- **Primary risks:** Massive view controllers, hardcoded constants, missing accessibility labels
- **Key review areas:** UIViewController/SwiftUI View, computed properties, extensions
- **Best practices:** MVVM, Constants enum, SwiftLint, DocC documentation

### Microservices
- **Primary risks:** Inconsistent naming across services, missing API documentation, duplicated validation
- **Key review areas:** Service contracts, shared libraries, error handling
- **Best practices:** OpenAPI specs, shared validation library, naming conventions guide

## Review Instructions

### Step 1: Detect Dead Code
```bash
# Python: Find unused imports
ruff check --select F401

# JavaScript: Find unused exports
npx ts-prune

# Find commented-out code
rg "^\s*#\s*(def |class |import )" --type py
rg "^\s*//\s*(function |const |import )" --type js
```

**Fix:**
```python
# ❌ DEAD
import pandas as pd  # Unused
# def old_function():  # Commented out
#     pass

# ✅ CLEANED
# (just remove them)
```

### Step 2: Refactor DRY Violations
```python
# ❌ DUPLICATION
def calculate_discount_bronze(price):
    return price * 0.95

def calculate_discount_silver(price):
    return price * 0.90

# ✅ REFACTORED
DISCOUNT_RATES = {
    'bronze': 0.95,
    'silver': 0.90,
    'gold': 0.85
}

def calculate_discount(price, tier):
    return price * DISCOUNT_RATES[tier]
```

### Step 3: Improve Naming
```python
# ❌ UNCLEAR
def proc(d, x, y):
    tmp = []
    for i in d:
        if i > x:
            tmp.append(i * y)
    return tmp

# ✅ CLEAR
def calculate_adjusted_values(values: List[float], threshold: float, multiplier: float) -> List[float]:
    """Filter values above threshold and multiply."""
    return [value * multiplier for value in values if value > threshold]
```

### Step 4: Add Documentation
```python
# ✅ GOOD: Documented
def calculate_tax(amount: float, state: str, category: str) -> float:
    """
    Calculate sales tax based on state and product category.
    
    Args:
        amount: Pre-tax amount in dollars
        state: Two-letter state code (e.g., 'CA', 'NY')
        category: Product category ('food', 'electronics', etc.)
    
    Returns:
        Total tax amount in dollars
    
    Examples:
        >>> calculate_tax(100, 'CA', 'food')
        8.0
    """
    # California and NY have higher rates
    if state in ['CA', 'NY']:
        # Food is taxed at reduced rate
        if category == 'food':
            return amount * 0.08
        return amount * 0.10
    
    # Default rate for other states
    return amount * 0.05
```

### Step 5: Reduce Complexity
```python
# ❌ COMPLEX: Cyclomatic complexity = 12
def process_order(order, user, payment, shipping, discount, taxes):
    if order.status == 'pending':
        if user.is_verified:
            if payment.is_valid:
                if shipping.is_available:
                    # ... nested hell

# ✅ SIMPLIFIED: Early returns
def process_order(order, user, payment, shipping, discount, taxes):
    # Validation with early returns
    if order.status != 'pending':
        raise OrderError("Order not pending")
    
    if not user.is_verified:
        raise UserError("User not verified")
    
    if not payment.is_valid:
        raise PaymentError("Payment invalid")
    
    if not shipping.is_available:
        raise ShippingError("Shipping unavailable")
    
    # Happy path is now flat
    total = calculate_total(order, discount, taxes)
    charge_payment(payment, total)
    schedule_shipping(order, shipping)
    return order
```

**Or extract to helper functions:**
```python
# ✅ EXTRACTED
def validate_order_preconditions(order, user, payment, shipping):
    if order.status != 'pending':
        raise OrderError("Order not pending")
    if not user.is_verified:
        raise UserError("User not verified")
    if not payment.is_valid:
        raise PaymentError("Payment invalid")
    if not shipping.is_available:
        raise ShippingError("Shipping unavailable")

def process_order(order, user, payment, shipping, discount, taxes):
    validate_order_preconditions(order, user, payment, shipping)
    total = calculate_total(order, discount, taxes)
    charge_payment(payment, total)
    schedule_shipping(order, shipping)
    return order
```

## Platform-Specific Examples

### Android: String Resources
```kotlin
// ❌ HARDCODED
textView.text = "Welcome to our app!"
Toast.makeText(context, "Error occurred", Toast.LENGTH_SHORT).show()

// ✅ STRING RESOURCE
textView.text = getString(R.string.welcome_message)
Toast.makeText(context, getString(R.string.error_generic), Toast.LENGTH_SHORT).show()
```

### iOS: Constants
```swift
// ❌ MAGIC NUMBERS
let maxRetries = 3
// ... 50 lines later
if attempt < 3 { ... }

// ✅ CONSTANTS
enum NetworkConfig {
    static let maxRetries = 3
    static let timeout: TimeInterval = 30
    static let baseURL = "https://api.example.com"
}

if attempt < NetworkConfig.maxRetries { ... }
```

### Web: Extract Duplicated Logic
```javascript
// ❌ DUPLICATION
router.post('/users', (req, res) => {
  if (!req.body.email || !req.body.email.includes('@')) {
    return res.status(400).json({ error: 'Invalid email' });
  }
  // ...
});

router.put('/users/:id', (req, res) => {
  if (!req.body.email || !req.body.email.includes('@')) {
    return res.status(400).json({ error: 'Invalid email' });
  }
  // ...
});

// ✅ EXTRACTED MIDDLEWARE
function validateEmail(req, res, next) {
  if (!req.body.email || !req.body.email.includes('@')) {
    return res.status(400).json({ error: 'Invalid email' });
  }
  next();
}

router.post('/users', validateEmail, (req, res) => { ... });
router.put('/users/:id', validateEmail, (req, res) => { ... });
```

## Migration Coverage
Review guidance from the legacy review-task corpus is now consolidated in this skill and validated via the migration inventory (`openspec/changes/research-changes/artifacts/review-task-skill-map.csv`).

## Quick Checklist
- [ ] No unreachable or commented-out code
- [ ] No unused imports/functions
- [ ] Duplicated logic extracted to shared functions
- [ ] Clear, descriptive variable/function names
- [ ] Constants used instead of magic numbers
- [ ] Public APIs documented (docstrings, JSDoc, etc.)
- [ ] Cyclomatic complexity <10 per function
- [ ] Functions <50 lines (preferably <30)
- [ ] Nesting depth <3 levels
- [ ] Type hints provided (Python, TypeScript)
