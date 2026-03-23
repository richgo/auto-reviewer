---
name: lang cpp
description: >
  C++ code review: memory management, RAII, undefined behavior, smart pointers, buffer overflows.
  Trigger when reviewing C++ (.cpp, .h) files, especially manual memory management, raw pointers,
  or performance-critical code.
---

# Language-Specific Review: C++

## Purpose
C++-specific guidance: memory safety, RAII, undefined behavior, and modern C++ patterns.

## Key Areas

### 1. Memory Management
```cpp
// ❌ UNSAFE: Manual delete
Widget* widget = new Widget();
widget->process();
delete widget;  // Might not be called if process() throws

// ✅ SAFE: unique_ptr
auto widget = std::make_unique<Widget>();
widget->process();  // Automatically deleted

// ❌ UNSAFE: Raw pointer ownership unclear
Widget* create() {
    return new Widget();  // Who owns this?
}

// ✅ SAFE: Return unique_ptr
std::unique_ptr<Widget> create() {
    return std::make_unique<Widget>();
}
```

### 2. Buffer Overflows
```cpp
// ❌ UNSAFE: strcpy
char dest[10];
strcpy(dest, userInput);  // Buffer overflow

// ✅ SAFE: strncpy or std::string
strncpy(dest, userInput, sizeof(dest) - 1);
dest[sizeof(dest) - 1] = '\0';

// ✅ BETTER: Use std::string
std::string dest = userInput;
```

### 3. Undefined Behavior
```cpp
// ❌ UNDEFINED: Use after free
int* ptr = new int(42);
delete ptr;
std::cout << *ptr;  // Undefined behavior

// ❌ UNDEFINED: Double delete
delete ptr;
delete ptr;  // Crash or corruption

// ✅ SAFE: smart pointers
auto ptr = std::make_unique<int>(42);
// Automatic cleanup, no double-delete possible
```

### 4. RAII Pattern
```cpp
// ❌ BAD: Manual cleanup
void process() {
    FILE* file = fopen("data.txt", "r");
    // ... processing ...
    fclose(file);  // Might be skipped if exception
}

// ✅ GOOD: RAII wrapper
class FileHandle {
    FILE* file_;
public:
    FileHandle(const char* path) : file_(fopen(path, "r")) {}
    ~FileHandle() { if (file_) fclose(file_); }
    FILE* get() { return file_; }
};

void process() {
    FileHandle file("data.txt");
    // Automatically closed
}

// ✅ BETTER: std::fstream
void process() {
    std::ifstream file("data.txt");
}
```

### 5. Smart Pointers
```cpp
// ❌ BAD: shared_ptr cycles
struct Node {
    std::shared_ptr<Node> next;  // Circular reference leak
};

// ✅ GOOD: Use weak_ptr
struct Node {
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> prev;  // Breaks cycle
};

// ❌ BAD: Mixing raw and smart pointers
auto widget = std::make_shared<Widget>();
Widget* raw = widget.get();
delete raw;  // Double-delete when widget destructs
```

## OWASP References
- [C-Based Toolchain Hardening](https://cheatsheetseries.owasp.org/cheatsheets/C-Based_Toolchain_Hardening_Cheat_Sheet.html)

## Quick Checklist
- [ ] No manual new/delete (use smart pointers)
- [ ] No strcpy/strcat (use strncpy or std::string)
- [ ] RAII for resource management
- [ ] weak_ptr to break cycles
- [ ] No use-after-free or double-delete
