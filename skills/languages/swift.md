---
name: swift
description: >
  Swift-specific code review for iOS: optionals, ARC/retain cycles, Combine/async-await pitfalls,
  SwiftUI lifecycle, memory management. Trigger when reviewing Swift (.swift) files, especially
  iOS projects with UIKit, SwiftUI, Combine, or async/await patterns.
---

# Language-Specific Review: Swift

## Purpose
Swift-specific guidance for iOS development: optionals, memory management, concurrency, SwiftUI, and iOS-specific patterns.

## Key Areas

### 1. Optional Handling
```swift
// ❌ UNSAFE: Force unwrap
let email = user.email!  // Fatal error if nil

// ✅ SAFE: Optional binding
if let email = user.email {
    sendEmail(to: email)
}

// ✅ SAFE: Nil coalescing
let email = user.email ?? "no-email@example.com"

// ❌ UNSAFE: Implicitly unwrapped optional in production
var token: String!

// ✅ SAFE: Regular optional
var token: String?
```

### 2. Retain Cycles
```swift
// ❌ UNSAFE: Strong reference cycle
class ViewController: UIViewController {
    var onComplete: (() -> Void)?
    
    func setupHandler() {
        onComplete = {
            self.dismiss(animated: true)  // Strong reference to self
        }
    }
}

// ✅ SAFE: [weak self]
func setupHandler() {
    onComplete = { [weak self] in
        self?.dismiss(animated: true)
    }
}

// ❌ UNSAFE: Delegate strong reference
class MyView: UIView {
    var delegate: MyViewDelegate?  // Should be weak
}

// ✅ SAFE: weak delegate
class MyView: UIView {
    weak var delegate: MyViewDelegate?
}
```

### 3. Async/Await Patterns
```swift
// ❌ UNSAFE: Blocking main thread
func loadData() {
    let data = fetchFromNetwork()  // Synchronous on main!
    updateUI(with: data)
}

// ✅ SAFE: async/await
func loadData() async {
    let data = await fetchFromNetwork()
    await MainActor.run {
        updateUI(with: data)
    }
}

// ❌ UNSAFE: Unstructured Task
func viewDidLoad() {
    Task {
        await loadData()  // Not canceled when view deallocates
    }
}

// ✅ SAFE: Task with lifecycle
class MyViewModel: ObservableObject {
    private var loadTask: Task<Void, Never>?
    
    func load() {
        loadTask = Task {
            await loadData()
        }
    }
    
    deinit {
        loadTask?.cancel()
    }
}
```

### 4. SwiftUI State Management
```swift
// ❌ BAD: @State for reference types
struct ContentView: View {
    @State var viewModel = MyViewModel()  // Wrong!
}

// ✅ GOOD: @StateObject for reference types
struct ContentView: View {
    @StateObject var viewModel = MyViewModel()
}

// ❌ BAD: Unnecessary @Published
class ViewModel: ObservableObject {
    @Published var data: [Item] = []
    @Published var isLoading: Bool = false
    
    func load() {
        // Both trigger view updates even if unrelated
    }
}

// ✅ GOOD: Single published state
class ViewModel: ObservableObject {
    @Published var state: LoadingState = .idle
}

enum LoadingState {
    case idle
    case loading
    case loaded([Item])
    case error(Error)
}
```

### 5. Memory Management
```swift
// ❌ UNSAFE: Captured self in async
Task {
    await someOperation()
    self.data = result  // Keeps self alive
}

// ✅ SAFE: [weak self] check
Task { [weak self] in
    await someOperation()
    guard let self else { return }
    self.data = result
}

// ❌ UNSAFE: NotificationCenter leak
NotificationCenter.default.addObserver(
    self,
    selector: #selector(handleNotification),
    name: .myNotification,
    object: nil
)  // Never removed

// ✅ SAFE: Remove observer
deinit {
    NotificationCenter.default.removeObserver(self)
}
```

## iOS-Specific Security
```swift
// ❌ UNSAFE: UserDefaults for sensitive data
UserDefaults.standard.set(token, forKey: "authToken")

// ✅ SAFE: Keychain
let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "authToken",
    kSecValueData as String: token.data(using: .utf8)!,
    kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly
]
SecItemAdd(query as CFDictionary, nil)

// ❌ UNSAFE: ATS bypass
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>

// ✅ SAFE: ATS enabled (default)
```

## OWASP References
- [Mobile Application Security](https://cheatsheetseries.owasp.org/cheatsheets/Mobile_Application_Security_Cheat_Sheet.html)
- [OWASP MASVS](https://mas.owasp.org/MASVS/)

## Quick Checklist
- [ ] No force unwraps (!) in production code
- [ ] [weak self] in closures capturing self
- [ ] Delegates marked weak
- [ ] async/await used for network/IO
- [ ] @StateObject (not @State) for ViewModels
- [ ] NotificationCenter observers removed
- [ ] Keychain used for sensitive data
- [ ] ATS enabled (no NSAllowsArbitraryLoads)
