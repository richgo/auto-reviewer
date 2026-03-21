---
name: kotlin
description: >
  Kotlin-specific code review for Android: coroutines pitfalls, null safety issues, data class misuse,
  sealed classes, Jetpack Compose patterns. Trigger when reviewing Kotlin (.kt) files, especially
  Android projects with coroutines, Flow, Compose UI, or ViewModel implementations.
---

# Language-Specific Review: Kotlin

## Purpose
Kotlin-specific guidance for Android development: coroutines, null safety, Compose, data classes, and Android-specific patterns.

## Key Areas

### 1. Coroutines Pitfalls
```kotlin
// ❌ UNSAFE: Wrong dispatcher
viewModelScope.launch {
    val data = fetchFromNetwork()  // Network on Main dispatcher!
}

// ✅ SAFE: IO dispatcher
viewModelScope.launch(Dispatchers.IO) {
    val data = fetchFromNetwork()
}

// ❌ UNSAFE: Leaked scope
GlobalScope.launch { }  // Never gets canceled

// ✅ SAFE: Structured concurrency
viewModelScope.launch { }  // Canceled with ViewModel
```

### 2. Null Safety Issues
```kotlin
// ❌ UNSAFE: Force unwrap
val email = user.email!!  // NPE if null

// ✅ SAFE: Safe call + elvis
val email = user.email ?: "no-email@example.com"

// ❌ UNSAFE: lateinit without check
lateinit var data: String
fun process() {
    println(data)  // UninitializedPropertyAccessException
}

// ✅ SAFE: Check initialization
lateinit var data: String
fun process() {
    if (::data.isInitialized) {
        println(data)
    }
}
```

### 3. Data Class Misuse
```kotlin
// ❌ BAD: Mutable data class
data class User(var name: String, var email: String)

// ✅ GOOD: Immutable
data class User(val name: String, val email: String)

// ❌ BAD: Data class with logic
data class Order(val id: Int) {
    fun processPayment() { }  // Logic in data class
}

// ✅ GOOD: Separate concerns
data class Order(val id: Int)
class OrderService {
    fun processPayment(order: Order) { }
}
```

### 4. Sealed Classes for State
```kotlin
// ✅ GOOD: Sealed class for UI state
sealed class UiState {
    object Loading : UiState()
    data class Success(val data: List<Item>) : UiState()
    data class Error(val message: String) : UiState()
}

when (state) {
    is UiState.Loading -> showLoading()
    is UiState.Success -> showData(state.data)
    is UiState.Error -> showError(state.message)
}  // Exhaustive when
```

### 5. Jetpack Compose Patterns
```kotlin
// ❌ BAD: State hoisting violation
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }
    Button(onClick = { count++ }) {
        Text("Count: $count")
    }
}

// ✅ GOOD: Hoisted state
@Composable
fun Counter(count: Int, onIncrement: () -> Unit) {
    Button(onClick = onIncrement) {
        Text("Count: $count")
    }
}

// ❌ BAD: Side effects without LaunchedEffect
@Composable
fun MyScreen(userId: String) {
    loadUser(userId)  // Called on every recomposition!
}

// ✅ GOOD: LaunchedEffect
@Composable
fun MyScreen(userId: String) {
    LaunchedEffect(userId) {
        loadUser(userId)  // Only when userId changes
    }
}
```

## Android-Specific Security
```kotlin
// ❌ UNSAFE: Hardcoded secret
const val API_KEY = "sk_live_abc123"

// ✅ SAFE: From BuildConfig or SecureStorage
val apiKey = BuildConfig.API_KEY

// ❌ UNSAFE: Logging sensitive data
Log.d("Auth", "User token: $token")

// ✅ SAFE: No PII in logs (or only in debug)
if (BuildConfig.DEBUG) {
    Log.d("Auth", "Auth flow completed")
}
```

## OWASP References
- [Mobile Application Security](https://cheatsheetseries.owasp.org/cheatsheets/Mobile_Application_Security_Cheat_Sheet.html)
- [OWASP MASVS](https://mas.owasp.org/MASVS/)

## Quick Checklist
- [ ] Coroutines use appropriate dispatcher (IO for network/DB)
- [ ] No GlobalScope (use viewModelScope/lifecycleScope)
- [ ] No force unwraps (!!)
- [ ] Data classes immutable (val not var)
- [ ] Sealed classes for state management
- [ ] Compose side effects in LaunchedEffect
- [ ] No hardcoded secrets
- [ ] No PII in Logcat
