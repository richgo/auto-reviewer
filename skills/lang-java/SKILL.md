---
name: lang java
description: >
  Java-specific code review guidance: Spring Boot security, JPA/Hibernate pitfalls, null handling,
  checked exceptions anti-patterns, thread safety issues, OWASP Java cheat sheets. Trigger when
  reviewing Java code (.java files), Spring applications, Android Java code, or Jakarta EE projects.
---

# Language-Specific Review: Java

## Purpose
Provide Java-specific security, correctness, and idiom guidance for code review. Covers framework issues (Spring Boot, JPA/Hibernate), language pitfalls, and Java-specific anti-patterns.

## Scope
- **Framework security:** Spring Security misconfig, JPA injection, unsafe deserialization
- **Language pitfalls:** NullPointerException, checked exception abuse, mutable statics
- **Thread safety:** Shared mutable state, double-checked locking, concurrent collections
- **Common anti-patterns:** God classes, instanceof chains, string concatenation in loops
- **Security-specific:** XXE, deserialization, SQL injection in JPA

## Framework-Specific Guidance

### Spring Boot Security
**Common vulnerabilities:**
1. **CSRF protection disabled:**
   ```java
   // ❌ UNSAFE
   http.csrf().disable();
   ```

2. **Permitresolve All wildcard:**
   ```java
   // ❌ UNSAFE
   http.authorizeRequests().antMatchers("/**").permitAll();
   ```

3. **Password in plaintext:**
   ```java
   // ❌ UNSAFE
   @Bean
   public UserDetailsService users() {
       UserDetails user = User.builder()
           .username("admin")
           .password("admin123")  // Plaintext!
           .roles("ADMIN")
           .build();
       return new InMemoryUserDetailsManager(user);
   }
   ```

4. **Missing method security:**
   ```java
   // ❌ UNSAFE: No @PreAuthorize
   @GetMapping("/admin/users")
   public List<User> getUsers() {
       return userService.findAll();
   }
   ```

**OWASP Spring references:**
- OWASP doesn't have a Spring-specific cheat sheet, but covers Java security broadly

### JPA/Hibernate Security
**Common vulnerabilities:**
1. **JPQL injection:**
   ```java
   // ❌ UNSAFE
   String jpql = "SELECT u FROM User u WHERE u.username = '" + username + "'";
   Query query = em.createQuery(jpql);
   
   // ✅ SAFE: Named parameters
   String jpql = "SELECT u FROM User u WHERE u.username = :username";
   Query query = em.createQuery(jpql);
   query.setParameter("username", username);
   ```

2. **Native SQL injection:**
   ```java
   // ❌ UNSAFE
   String sql = "SELECT * FROM users WHERE id = " + userId;
   Query query = em.createNativeQuery(sql);
   
   // ✅ SAFE
   String sql = "SELECT * FROM users WHERE id = ?1";
   Query query = em.createNativeQuery(sql);
   query.setParameter(1, userId);
   ```

3. **N+1 query problem:**
   ```java
   // ❌ INEFFICIENT
   List<Order> orders = orderRepository.findAll();
   for (Order order : orders) {
       System.out.println(order.getCustomer().getName());  // N+1 queries
   }
   
   // ✅ FIXED: JOIN FETCH
   @Query("SELECT o FROM Order o JOIN FETCH o.customer")
   List<Order> findAllWithCustomer();
   ```

## Language-Specific Pitfalls

### 1. Null Handling
```java
// ❌ UNSAFE: No null check
public void processUser(User user) {
    String email = user.getEmail().toLowerCase();  // NPE if email is null
}

// ✅ SAFE: Optional
public void processUser(User user) {
    String email = Optional.ofNullable(user.getEmail())
        .map(String::toLowerCase)
        .orElse("no-email@example.com");
}

// ✅ SAFE: @NonNull annotation (with validation)
public void processUser(@NonNull User user) {
    Objects.requireNonNull(user.getEmail(), "Email cannot be null");
    String email = user.getEmail().toLowerCase();
}
```

### 2. Checked Exception Anti-Patterns
```java
// ❌ BAD: Swallowing exception
try {
    riskyOperation();
} catch (Exception e) {
    // Silent failure
}

// ❌ BAD: Generic exception
public void process() throws Exception {
    // Too broad
}

// ✅ GOOD: Specific exceptions with context
public void process() throws ProcessingException {
    try {
        riskyOperation();
    } catch (IOException e) {
        throw new ProcessingException("Failed to process file", e);
    }
}
```

### 3. Thread Safety Issues
```java
// ❌ UNSAFE: Mutable static
public class Cache {
    private static Map<String, Object> cache = new HashMap<>();  // Not thread-safe
    
    public static void put(String key, Object value) {
        cache.put(key, value);  // Race condition
    }
}

// ✅ SAFE: ConcurrentHashMap
public class Cache {
    private static final Map<String, Object> cache = new ConcurrentHashMap<>();
    
    public static void put(String key, Object value) {
        cache.put(key, value);
    }
}

// ❌ UNSAFE: Double-checked locking (broken in Java <5)
private static volatile Singleton instance;

public static Singleton getInstance() {
    if (instance == null) {
        synchronized (Singleton.class) {
            if (instance == null) {
                instance = new Singleton();  // Broken without volatile
            }
        }
    }
    return instance;
}

// ✅ SAFE: Initialization-on-demand holder
public class Singleton {
    private Singleton() {}
    
    private static class Holder {
        static final Singleton INSTANCE = new Singleton();
    }
    
    public static Singleton getInstance() {
        return Holder.INSTANCE;
    }
}
```

### 4. Resource Management
```java
// ❌ UNSAFE: Resource leak
FileInputStream fis = new FileInputStream("file.txt");
int data = fis.read();
fis.close();  // Not called if read() throws

// ✅ SAFE: try-with-resources
try (FileInputStream fis = new FileInputStream("file.txt")) {
    int data = fis.read();
}  // Automatically closed
```

## Security-Specific Patterns

### 1. Deserialization
```java
// ❌ UNSAFE: Arbitrary deserialization
ObjectInputStream ois = new ObjectInputStream(userInputStream);
Object obj = ois.readObject();  // RCE risk

// ✅ SAFE: Whitelist classes
ObjectInputStream ois = new ObjectInputStream(userInputStream) {
    @Override
    protected Class<?> resolveClass(ObjectStreamClass desc) throws IOException, ClassNotFoundException {
        if (!desc.getName().equals("com.example.SafeClass")) {
            throw new InvalidClassException("Unauthorized deserialization");
        }
        return super.resolveClass(desc);
    }
};
```

### 2. XXE Prevention
```java
// ❌ UNSAFE: XXE vulnerable
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
DocumentBuilder db = dbf.newDocumentBuilder();
Document doc = db.parse(userFile);

// ✅ SAFE: XXE protection
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
dbf.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
dbf.setXIncludeAware(false);
dbf.setExpandEntityReferences(false);
DocumentBuilder db = dbf.newDocumentBuilder();
Document doc = db.parse(userFile);
```

### 3. Command Injection
```java
// ❌ UNSAFE
String cmd = "ping -c 4 " + userInput;
Runtime.getRuntime().exec(cmd);

// ✅ SAFE: Array instead of string
String[] cmd = {"ping", "-c", "4", userInput};
Runtime.getRuntime().exec(cmd);
```

## Modern Java Idioms

### 1. Streams
```java
// ✅ GOOD: Functional style
List<String> names = users.stream()
    .filter(user -> user.isActive())
    .map(User::getName)
    .collect(Collectors.toList());
```

### 2. Records (Java 14+)
```java
// ✅ GOOD: Immutable data class
public record User(int id, String name, String email) {
    // Auto-generates constructor, getters, equals, hashCode, toString
}
```

### 3. Pattern Matching (Java 16+)
```java
// ✅ GOOD: instanceof with pattern variable
if (obj instanceof String s) {
    System.out.println(s.length());  // No cast needed
}
```

### 4. Text Blocks (Java 15+)
```java
// ✅ GOOD: Multi-line strings
String json = """
    {
      "name": "Alice",
      "age": 30
    }
    """;
```

## Anti-Patterns to Flag

1. **String concatenation in loops:** Use `StringBuilder`
2. **Finalizers:** Use try-with-resources or `Cleaner`
3. **`instanceof` chains:** Use polymorphism or visitor pattern
4. **Mutable collections in public APIs:** Return `Collections.unmodifiableList()`
5. **Raw types:** Use generics (`List` → `List<String>`)

## Related Security Tasks
- `review-tasks/security/sql-injection.md`
- `review-tasks/security/command-injection.md`
- `review-tasks/security/insecure-deserialization.md`
- `review-tasks/security/xml-external-entity.md`

## OWASP References
- [Java Security](https://cheatsheetseries.owasp.org/cheatsheets/Java_Security_Cheat_Sheet.html)
- [JAAS Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JAAS_Cheat_Sheet.html)
- [Injection Prevention in Java](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_in_Java_Cheat_Sheet.html)
- [Bean Validation](https://cheatsheetseries.owasp.org/cheatsheets/Bean_Validation_Cheat_Sheet.html)

## Quick Java Security Checklist
- [ ] No JPQL/SQL string concatenation
- [ ] Spring Security CSRF not disabled
- [ ] Passwords hashed with BCryptPasswordEncoder
- [ ] Method-level security with @PreAuthorize
- [ ] ObjectInputStream validates classes
- [ ] XML parsers have XXE protection
- [ ] Commands use array form, not string
- [ ] Resources closed with try-with-resources
- [ ] Thread-safe collections for shared state
- [ ] Null checks or Optional usage
