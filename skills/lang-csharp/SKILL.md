---
name: lang csharp
description: >
  C#-specific code review: .NET/ASP.NET Core security, async/await pitfalls, LINQ issues, Entity
  Framework, OWASP .NET cheat sheets. Trigger when reviewing C# (.cs) files, ASP.NET applications,
  or .NET microservices.
---

# Language-Specific Review: C#

## Purpose
C#-specific guidance: ASP.NET security, async/await, LINQ, EF Core, and .NET patterns.

## Key Areas

### 1. ASP.NET Core Security
```csharp
// ❌ UNSAFE: SQL injection
public User GetUser(string username)
{
    var sql = $"SELECT * FROM Users WHERE Username = '{username}'";
    return db.Database.ExecuteSqlRaw(sql);
}

// ✅ SAFE: Parameterized query
public User GetUser(string username)
{
    return db.Users.FromSqlInterpolated($"SELECT * FROM Users WHERE Username = {username}").FirstOrDefault();
}

// ❌ UNSAFE: CSRF protection disabled
services.AddControllersWithViews(options => {
    options.Filters.Add(new IgnoreAntiforgeryTokenAttribute());
});

// ✅ SAFE: CSRF enabled (default)
services.AddControllersWithViews();
```

### 2. Async/Await Pitfalls
```csharp
// ❌ BAD: Async void (except event handlers)
public async void ProcessData()
{
    await FetchData();  // Exceptions can't be caught
}

// ✅ GOOD: Async Task
public async Task ProcessDataAsync()
{
    await FetchData();
}

// ❌ BAD: .Result deadlock
public void Process()
{
    var result = FetchDataAsync().Result;  // Deadlocks in UI thread
}

// ✅ GOOD: await
public async Task ProcessAsync()
{
    var result = await FetchDataAsync();
}

// ❌ BAD: ConfigureAwait misuse
public async Task<string> GetDataAsync()
{
    var data = await httpClient.GetStringAsync(url).ConfigureAwait(false);
    textBox.Text = data;  // Crashes! Not on UI thread
}

// ✅ GOOD: No ConfigureAwait in UI code
public async Task<string> GetDataAsync()
{
    var data = await httpClient.GetStringAsync(url);
    textBox.Text = data;  // Safe
}
```

### 3. LINQ Issues
```csharp
// ❌ BAD: Deferred execution trap
var users = db.Users.Where(u => u.IsActive);
db.Database.CloseConnection();
var count = users.Count();  // Exception! Query executes here

// ✅ GOOD: Materialize with ToList
var users = db.Users.Where(u => u.IsActive).ToList();
db.Database.CloseConnection();
var count = users.Count();  // Safe

// ❌ BAD: Multiple enumeration
public IEnumerable<User> GetActiveUsers()
{
    return db.Users.Where(u => u.IsActive);
}

var users = GetActiveUsers();
var count = users.Count();  // Query 1
var first = users.First();   // Query 2

// ✅ GOOD: Return List
public List<User> GetActiveUsers()
{
    return db.Users.Where(u => u.IsActive).ToList();
}
```

### 4. Entity Framework
```csharp
// ❌ BAD: N+1 query problem
var orders = db.Orders.ToList();
foreach (var order in orders)
{
    Console.WriteLine(order.Customer.Name);  // N+1 queries
}

// ✅ GOOD: Include
var orders = db.Orders.Include(o => o.Customer).ToList();
foreach (var order in orders)
{
    Console.WriteLine(order.Customer.Name);
}
```

### 5. Disposal Patterns
```csharp
// ❌ BAD: No disposal
var stream = File.OpenRead("file.txt");
var data = stream.ReadByte();

// ✅ GOOD: using statement
using (var stream = File.OpenRead("file.txt"))
{
    var data = stream.ReadByte();
}

// ✅ BETTER: using declaration (C# 8+)
using var stream = File.OpenRead("file.txt");
var data = stream.ReadByte();
```

## OWASP References
- [DotNet Security](https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html)

## Quick Checklist
- [ ] No SQL string concatenation
- [ ] async Task (not async void)
- [ ] No .Result or .Wait()
- [ ] LINQ queries materialized before disposal
- [ ] EF Include for related data
- [ ] IDisposable wrapped in using
