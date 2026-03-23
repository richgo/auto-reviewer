---
name: data migration safety
description: >
  Migrated review-task skill for Migration Safety. Use this skill whenever diffs may
  introduce data issues on web, api, especially in all. Actively look for: Database
  migrations that are destructive, non-reversible, or unsafe to run on production —
  dropping columns/tables, changing types with... and report findings with high severity
  expectations and actionable fixes.
---

# Migration Safety

## Source Lineage
- Original review task: `review-tasks/data/migration-safety.md`
- Migrated skill artifact: `skills/review-task-data-migration-safety/SKILL.md`

## Task Metadata
- Category: `data`
- Severity: `high`
- Platforms: `web, api`
- Languages: `all`

## Purpose
Database migrations that are destructive, non-reversible, or unsafe to run on production — dropping columns/tables, changing types with data loss, or running long-locking operations on large tables.

## Detection Heuristics
- `DROP TABLE`, `DROP COLUMN` without data backup step
- Column type changes that truncate data (varchar→char, bigint→int)
- `NOT NULL` added without default on existing column
- Large table `ALTER` without online DDL / concurrent index
- Missing `down` / rollback migration
- Renaming columns (breaks running code during deploy)

## Eval Cases
### Case 1: Drop column without backup
```python
# migration
def upgrade():
    op.drop_column('users', 'legacy_email')
```
**Expected finding:** High — Destructive migration. Dropping `legacy_email` column is irreversible. Add data backup step or soft-delete (rename to `_deprecated_legacy_email`).

### Case 2: NOT NULL without default
```sql
ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(50) NOT NULL;
```
**Expected finding:** High — Adding NOT NULL column without DEFAULT on existing table will fail if rows exist. Add `DEFAULT ''` or make nullable first, backfill, then add constraint.

## Counter-Examples
### Counter 1: Safe additive migration
```python
def upgrade():
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))
```
**Why it's correct:** Adding a nullable column is safe — no existing data affected.

## Binary Eval Assertions
- [ ] Detects destructive drop in eval case 1
- [ ] Detects NOT NULL without default in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding suggests safe alternative
- [ ] Severity assigned as high

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
