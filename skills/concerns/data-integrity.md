---
name: data-integrity
description: >
  Detect data integrity issues: PII exposure in logs/responses/errors, unsafe database migrations,
  schema drift between services, missing backup validation, and serialization mismatches. Trigger
  when reviewing database migrations, API responses containing user data, error handling that logs
  request details, schema definitions, or serialization/deserialization code. Critical for privacy
  and data consistency.
---

# Data Integrity Review

## Purpose
Review code for data integrity and privacy issues: PII exposure, unsafe migrations, schema drift, backup validation gaps, and serialization mismatches that cause data loss or corruption.

## Scope
1. **PII Exposure** — personal data in logs, error messages, API responses, analytics
2. **Migration Safety** — destructive migrations without backups, data loss, downtime
3. **Schema Drift** — mismatched schemas between services, missing migrations, type conflicts
4. **Backup Validation** — backups not tested, missing point-in-time recovery, no restore drills
5. **Serialization Mismatch** — version skew, missing fields, type changes breaking deserialization

## Detection Strategy

### 1. PII Exposure Red Flags
- **Logging PII** (email, SSN, credit cards, IP addresses)
- **PII in error messages** sent to client
- **Full user object** in API response (includes internal fields)
- **Analytics tracking** with PII (Sentry, Mixpanel)
- **PII in URLs** (GET parameters with email/name)

**High-risk patterns:**
```python
# ❌ UNSAFE
logger.info(f"User login: {user.email}, IP: {request.ip}")
return {"error": f"Invalid card number: {card_number}"}
```

### 2. Migration Safety Red Flags
- **DROP COLUMN/TABLE** without backup
- **ALTER COLUMN** changing type (data loss risk)
- **Non-reversible migrations** (no down() method)
- **Migrations without transactions** (partial apply on failure)
- **No data verification** after migration

**High-risk patterns:**
```sql
-- ❌ UNSAFE
ALTER TABLE users DROP COLUMN middle_name;
ALTER TABLE orders ALTER COLUMN amount TYPE INTEGER;  -- Truncates decimals
```

### 3. Schema Drift Red Flags
- **Microservices with different field types** for same entity
- **Missing migration** in one service after schema change
- **API response doesn't match** client expectations
- **No schema registry** (Avro, Protobuf) for events
- **Database schema mismatch** with ORM models

**High-risk patterns:**
```python
# ❌ DRIFT
# Service A: user.age is string
# Service B: user.age is int
# No schema coordination
```

### 4. Backup Validation Red Flags
- **Automated backups** but no restore testing
- **No point-in-time recovery** capability
- **Backups not encrypted**
- **Single datacenter backups** (disaster recovery risk)
- **Retention policy missing** (compliance risk)

### 5. Serialization Mismatch Red Flags
- **Version skew** (old client with new API)
- **Required field added** without default
- **Field renamed** without alias
- **Pickle/Marshal** for persistent storage (fragile)
- **JSON without schema validation**

**High-risk patterns:**
```python
# ❌ UNSAFE
@dataclass
class User:
    id: int
    email: str
    role: str  # Added without default, breaks old clients
```

## Platform-Specific Guidance

### Web/API
- **Primary risks:** PII in logs, unsafe migrations, schema drift
- **Key review areas:** Logger calls, database migrations, API response serialization
- **Best practices:** Redact PII in logs, reversible migrations, Pydantic for validation

### Android
- **Primary risks:** Room migration data loss, PII in LogCat, backup exposure
- **Key review areas:** Room Migration objects, Log.d/Log.i calls, allowBackup config
- **Best practices:** Destructive migration testing, ProGuard log removal, fullBackupContent rules

### iOS
- **Primary risks:** Core Data migration crashes, PII in OS logs, iCloud backup exposure
- **Key review areas:** Core Data model versions, os_log calls, UserDefaults sync
- **Best practices:** Lightweight migration with fallback, os_log privacy markers

### Microservices
- **Primary risks:** Schema drift across services, event schema evolution, distributed transaction consistency
- **Key review areas:** Service contracts, message queue schemas, saga compensation
- **Best practices:** Schema registry (Confluent), Avro/Protobuf, contract tests

## Review Instructions

### Step 1: Detect PII in Logs
```bash
# Find logging of PII
rg "log.*email|log.*ssn|log.*password|log.*token|log.*credit" --type py
rg "Log\.(d|i|e).*email|Log.*ssn|Log.*user\." --type kotlin
```

**Safe logging pattern:**
```python
# ❌ UNSAFE
logger.info(f"User {user.email} logged in from {request.ip}")

# ✅ SAFE: Redacted
logger.info(f"User {user.id} logged in from {redact_ip(request.ip)}")

# ✅ SAFE: Structured logging with PII filter
import structlog

logger = structlog.get_logger()
logger.info("user_login", user_id=user.id, ip=redact_ip(request.ip))
```

### Step 2: Review Migrations for Safety
```bash
# Find destructive operations
rg "DROP COLUMN|DROP TABLE|ALTER COLUMN.*TYPE|TRUNCATE" db/migrations/
```

**Safe migration pattern:**
```python
# ✅ SAFE: Reversible migration
def upgrade():
    # 1. Add new column (nullable)
    op.add_column('users', sa.Column('full_name', sa.String(255), nullable=True))
    
    # 2. Backfill data
    op.execute("UPDATE users SET full_name = first_name || ' ' || last_name")
    
    # 3. Make non-nullable after backfill
    op.alter_column('users', 'full_name', nullable=False)

def downgrade():
    op.drop_column('users', 'full_name')
```

### Step 3: Validate Schema Consistency
```python
# ✅ GOOD: Pydantic for schema validation
from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    email: str
    created_at: datetime
    
    class Config:
        # Fail if extra fields present
        extra = 'forbid'

# Use across all services
@app.post('/users')
def create_user(user: UserSchema):
    # Guaranteed schema match
```

### Step 4: Test Backups
```bash
# ✅ GOOD: Automated restore test
# cron job: daily-backup-restore-test.sh

#!/bin/bash
# 1. Create backup
pg_dump dbname > backup.sql

# 2. Restore to test database
psql test_db < backup.sql

# 3. Verify data integrity
python verify_data.py test_db

# 4. Alert if mismatch
if [ $? -ne 0 ]; then
    send_alert "Backup restore test failed"
fi
```

### Step 5: Handle Serialization Versions
```python
# ✅ GOOD: Versioned serialization
from pydantic import BaseModel, Field

class UserV1(BaseModel):
    id: int
    name: str

class UserV2(BaseModel):
    id: int
    full_name: str = Field(alias="name")  # Backward compat
    email: str
    
    @validator('full_name', pre=True, always=True)
    def migrate_name(cls, v, values):
        # Handle old clients sending "name"
        return v or values.get('name')
```

## Platform-Specific Examples

### Android: Room Migration
```kotlin
// ❌ UNSAFE: Destructive migration
val MIGRATION_2_3 = object : Migration(2, 3) {
    override fun migrate(database: SupportSQLiteDatabase) {
        database.execSQL("ALTER TABLE users DROP COLUMN middle_name")
    }
}

// ✅ SAFE: Tested migration with fallback
val MIGRATION_2_3 = object : Migration(2, 3) {
    override fun migrate(database: SupportSQLiteDatabase) {
        // 1. Create new table with desired schema
        database.execSQL("CREATE TABLE users_new (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT)")
        
        // 2. Copy data
        database.execSQL("INSERT INTO users_new SELECT id, first_name, last_name FROM users")
        
        // 3. Drop old table
        database.execSQL("DROP TABLE users")
        
        // 4. Rename
        database.execSQL("ALTER TABLE users_new RENAME TO users")
    }
}

// Test migration
@Test
fun testMigration2To3() {
    val helper = MigrationTestHelper(...)
    val db = helper.createDatabase(TEST_DB, 2)
    
    db.execSQL("INSERT INTO users VALUES (1, 'Alice', 'M', 'Smith')")
    db.close()
    
    val migratedDb = helper.runMigrationsAndValidate(TEST_DB, 3, true, MIGRATION_2_3)
    
    val cursor = migratedDb.query("SELECT * FROM users WHERE id = 1")
    assertTrue(cursor.moveToFirst())
    assertEquals("Alice", cursor.getString(cursor.getColumnIndex("first_name")))
}
```

### iOS: Core Data Migration
```swift
// ✅ SAFE: Lightweight migration with error handling
lazy var persistentContainer: NSPersistentContainer = {
    let container = NSPersistentContainer(name: "Model")
    
    let description = container.persistentStoreDescriptions.first
    description?.shouldMigrateStoreAutomatically = true
    description?.shouldInferMappingModelAutomatically = true
    
    container.loadPersistentStores { storeDescription, error in
        if let error = error {
            // Log but don't crash
            os_log("Core Data migration failed: %@", log: .default, type: .error, error.localizedDescription)
            
            // Fallback: Delete and recreate (with user consent)
            self.handleMigrationFailure(container: container)
        }
    }
    
    return container
}()

func handleMigrationFailure(container: NSPersistentContainer) {
    // Prompt user
    let alert = UIAlertController(title: "Data Migration Required", message: "Would you like to reset app data?", preferredStyle: .alert)
    alert.addAction(UIAlertAction(title: "Reset", style: .destructive) { _ in
        self.deleteAndRecreateStore(container: container)
    })
    present(alert, animated: true)
}
```

### Microservices: Schema Registry
```python
# ✅ GOOD: Avro schema with evolution
from confluent_kafka import avro

# Schema v1
user_schema_v1 = avro.loads('''
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"}
  ]
}
''')

# Schema v2 with backward compat
user_schema_v2 = avro.loads('''
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": ["null", "string"], "default": null}
  ]
}
''')

# Producer with schema registry
producer = AvroProducer({
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://localhost:8081'
}, default_value_schema=user_schema_v2)

# Consumer handles both versions
consumer = AvroConsumer({
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://localhost:8081',
    'group.id': 'mygroup'
})
```

## Related Review Tasks
- `review-tasks/data/pii-exposure.md`
- `review-tasks/data/migration-safety.md`
- `review-tasks/data/schema-validation.md`
- `review-tasks/data/serialization-mismatch.md`
- Platform-specific: `review-tasks/data/{android,ios,microservices}/*.md`

## OWASP References
- [User Privacy Protection](https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html)
- [Database Security](https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html)

## Quick Checklist
- [ ] No PII in logs (email, SSN, tokens, credit cards)
- [ ] Database migrations tested in staging first
- [ ] Reversible migrations with down() methods
- [ ] Migrations wrapped in transactions
- [ ] Schema validation (Pydantic, JSON Schema, Avro)
- [ ] Backup restore tested regularly
- [ ] Backups encrypted and geo-redundant
- [ ] Serialization handles version skew
- [ ] Required fields have defaults for backward compat
- [ ] Schema registry for cross-service events
