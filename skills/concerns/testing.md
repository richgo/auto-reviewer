---
name: testing
description: >
  Detect testing quality issues: missing test coverage for critical paths, weak assertions,
  flaky test patterns, test isolation problems, and mock overuse. Trigger when reviewing test
  files (*_test.*, *.spec.*, *.test.*, test directories), test configurations, or changes to
  core application logic without corresponding test updates. Covers unit, integration, and E2E tests.
---

# Testing Quality Review

## Purpose
Review test code and coverage for quality issues: inadequate coverage of critical paths, weak or missing assertions, flaky test patterns, test isolation failures, and excessive mocking that masks integration bugs.

## Scope
1. **Missing Test Coverage** — critical paths untested, edge cases ignored, new code without tests
2. **Weak Assertions** — `assert True`, no verification, testing implementation not behavior
3. **Flaky Test Patterns** — timing dependencies, random data, external service calls
4. **Test Isolation** — shared state, order-dependent tests, global mocks not cleaned up
5. **Mock Overuse** — mocking everything, never testing real integrations

## Detection Strategy

### 1. Missing Test Coverage Red Flags
- **New functions without tests** (git diff shows new code, no new tests)
- **Critical paths untested** (auth, payment, data deletion)
- **Edge cases missing** (empty input, null, overflow, boundary conditions)
- **Error handling untested** (exceptions, network failures, invalid input)
- **Platform-specific logic untested** (mobile lifecycle, concurrency)

**High-risk patterns:**
```python
# ❌ UNSAFE: No tests for payment logic
def process_payment(user_id, amount):
    user = get_user(user_id)
    charge_card(user.card, amount)
    create_invoice(user_id, amount)
```

### 2. Weak Assertions Red Flags
- **No assertions** (`test_function(); # Just calls code`)
- **Trivial assertions** (`assert True`, `assert result is not None`)
- **Testing implementation** (`assert mock.called` without checking output)
- **Missing negative cases** (only testing happy path)
- **Assertions commented out** or in try/except with pass

**High-risk patterns:**
```python
# ❌ WEAK
def test_login():
    result = login(username, password)
    assert result is not None  # Doesn't verify correctness!
```

### 3. Flaky Test Patterns Red Flags
- **sleep()** or **time.sleep()** for synchronization
- **Random data** without seeding (`random.randint()`)
- **Date.now()** without mocking time
- **External API calls** in unit tests
- **File system race conditions** (temp files)

**High-risk patterns:**
```python
# ❌ FLAKY
def test_async_operation():
    start_background_task()
    time.sleep(1)  # Hope it finishes in 1 second
    assert task_completed()
```

### 4. Test Isolation Red Flags
- **Shared mutable state** between tests
- **Tests passing/failing based on execution order**
- **setUp/tearDown missing** or incomplete
- **Global mocks** not reset between tests
- **Database state leaking** between tests

**High-risk patterns:**
```python
# ❌ UNSAFE: Shared state
counter = 0

def test_increment():
    global counter
    counter += 1
    assert counter == 1  # Fails if run after another test
```

### 5. Mock Overuse Red Flags
- **Mocking 100%** of dependencies (never testing real integration)
- **Mocking libraries** instead of interfaces
- **Mocking in integration tests** (defeats purpose)
- **No integration/E2E tests** (only unit tests with mocks)

**High-risk patterns:**
```python
# ❌ OVERUSE: Mocking database in integration test
@mock.patch('app.database.query')
def test_api_endpoint(mock_query):
    mock_query.return_value = [{"id": 1}]
    response = client.get('/users')
    # Never actually queries database!
```

## Platform-Specific Guidance

### Web/API
- **Primary risks:** Missing E2E tests for critical flows, mocking all HTTP calls, no database integration tests
- **Key review areas:** API endpoints, authentication flows, data mutations
- **Testing tools:** Playwright, Cypress, Supertest, pytest-httpx

### Android
- **Primary risks:** UI tests missing, lifecycle bugs untested, Robolectric overuse without instrumented tests
- **Key review areas:** Fragment/Activity lifecycle, ViewModel, Compose UI, background tasks
- **Testing tools:** Espresso, Compose Testing, Robolectric, JUnit

### iOS
- **Primary risks:** UI flows untested, async expectations missing, SwiftUI preview divergence
- **Key review areas:** View lifecycle, async/await, Combine publishers, snapshot tests
- **Testing tools:** XCTest, XCUITest, SnapshotTesting

### Microservices
- **Primary risks:** Contract tests missing, service-to-service integration untested, chaos testing absent
- **Key review areas:** API contracts, message queue handlers, distributed transactions
- **Testing tools:** Pact, Testcontainers, Postman/Newman, chaos engineering

## Review Instructions

### Step 1: Check Coverage Metrics
```bash
# Python
pytest --cov=app --cov-report=html
coverage report --fail-under=80

# JavaScript
npm test -- --coverage
# Android
./gradlew jacocoTestReport

# iOS
xcodebuild test -scheme MyApp -enableCodeCoverage YES
```

**Flag missing coverage for:**
- Critical paths: <95% coverage
- Business logic: <90% coverage
- Utilities: <80% coverage

### Step 2: Audit Assertions
```bash
# Find tests with no/weak assertions
rg "def test.*:\s*$" test/
rg "it\('.*', \(\) => \{\s*\}\)" test/
rg "assert True|assert.*is not None" test/
```

**Good assertion pattern:**
```python
# ✅ GOOD: Specific assertions
def test_calculate_discount():
    result = calculate_discount(price=100, code="SAVE10")
    assert result == 90
    assert result < 100
    assert isinstance(result, Decimal)
```

### Step 3: Detect Flaky Patterns
```bash
# Find timing dependencies
rg "time\.sleep|Thread\.sleep|setTimeout|Task\.delay" test/

# Find external calls
rg "requests\.get|fetch\(|URLSession" test/

# Find random without seed
rg "random\.|Math\.random|arc4random" test/
```

**Fix flaky timing:**
```python
# ❌ FLAKY
def test_background_task():
    start_task()
    time.sleep(2)
    assert task_done()

# ✅ FIXED: Use event/condition
def test_background_task():
    event = threading.Event()
    start_task(callback=lambda: event.set())
    assert event.wait(timeout=5), "Task didn't complete"
```

### Step 4: Check Test Isolation
```python
# ✅ GOOD: Isolated tests
@pytest.fixture(autouse=True)
def reset_database():
    db.clear()
    yield
    db.clear()

def test_create_user():
    user = create_user("alice")
    assert user.name == "alice"

def test_delete_user():
    user = create_user("bob")
    delete_user(user.id)
    assert get_user(user.id) is None
```

### Step 5: Balance Mocks and Integration
```python
# ✅ GOOD: Unit test with mock
@mock.patch('app.send_email')
def test_registration_sends_email(mock_send):
    register_user("alice@example.com")
    mock_send.assert_called_once()

# ✅ GOOD: Integration test without mock
def test_registration_flow():
    with test_mail_server():
        register_user("alice@example.com")
        assert mailbox.has_email_to("alice@example.com")
```

## Platform-Specific Examples

### Android: UI Test Gap
```kotlin
// ❌ MISSING: No UI test
class LoginActivity : AppCompatActivity() {
    fun onLoginClick() {
        val username = usernameField.text.toString()
        val password = passwordField.text.toString()
        viewModel.login(username, password)
    }
}

// ✅ ADD: Espresso test
@Test
fun testLoginFlow() {
    onView(withId(R.id.username)).perform(typeText("user"))
    onView(withId(R.id.password)).perform(typeText("pass"))
    onView(withId(R.id.loginButton)).perform(click())
    onView(withText("Welcome")).check(matches(isDisplayed()))
}
```

### iOS: Async Expectation Missing
```swift
// ❌ WEAK: No async handling
func testFetchUser() {
    viewModel.fetchUser(id: 1)
    XCTAssertNotNil(viewModel.user)  // Fails, async not complete
}

// ✅ FIXED: XCTestExpectation
func testFetchUser() {
    let expectation = XCTestExpectation(description: "Fetch user")
    viewModel.fetchUser(id: 1) {
        XCTAssertEqual(viewModel.user?.name, "Alice")
        expectation.fulfill()
    }
    wait(for: [expectation], timeout: 5.0)
}
```

### Web: E2E Test Gap
```javascript
// ❌ MISSING: No E2E test for checkout
router.post('/checkout', async (req, res) => {
  const { cartId, payment } = req.body;
  await processPayment(payment);
  await clearCart(cartId);
  res.json({ success: true });
});

// ✅ ADD: Playwright E2E test
test('checkout flow', async ({ page }) => {
  await page.goto('/cart');
  await page.click('text=Checkout');
  await page.fill('[name=card]', '4242424242424242');
  await page.click('text=Pay');
  await expect(page.locator('text=Order confirmed')).toBeVisible();
});
```

### Microservices: Contract Test Missing
```python
# ❌ MISSING: No contract test
@app.post('/orders')
def create_order(order: Order):
    return {"id": save_order(order)}

# ✅ ADD: Pact contract test
def test_order_creation_contract(pact):
    pact.given('product 123 exists').upon_receiving(
        'a request to create an order'
    ).with_request(
        method='POST', path='/orders', body={'product_id': '123', 'qty': 1}
    ).will_respond_with(200, body={'id': Like(1)})
    
    with pact:
        result = client.post('/orders', json={'product_id': '123', 'qty': 1})
        assert result.json()['id'] is not None
```

## Related Review Tasks
- `review-tasks/testing/missing-test-coverage.md`
- `review-tasks/testing/weak-assertions.md`
- `review-tasks/testing/flaky-test-patterns.md`
- `review-tasks/testing/test-isolation.md`
- `review-tasks/testing/mock-overuse.md`
- Platform-specific: `review-tasks/testing/{android,ios,web,microservices}/*.md`

## Quick Checklist
- [ ] Critical paths have >95% coverage
- [ ] New code includes corresponding tests
- [ ] Assertions verify behavior, not just "not None"
- [ ] No time.sleep() or random data without seeding
- [ ] Tests pass in any order (no shared state)
- [ ] Mix of unit, integration, and E2E tests
- [ ] Edge cases tested (empty, null, overflow)
- [ ] Error handling tested
- [ ] Platform lifecycle tested (mobile)
- [ ] Contract tests for service boundaries (microservices)
