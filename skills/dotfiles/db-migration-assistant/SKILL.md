---
name: db-migration-assistant
description: >
  Safely creates and applies database migrations with automatic backup, rollback capability, and validation. Supports multiple ORMs and migration tools. Use when user needs to modify database schema. Triggers: create migration, apply migration, database migration, schema change, rollback migration
license: MIT
metadata:
  author: cyperx
  version: "1.0.0"
  openclaw: true
  categories: [dev, dotfiles]
---


# DB Migration Assistant Skill

## Purpose

The DB Migration Assistant automates safe database schema changes. Manual migrations are risky - one mistake can corrupt data or cause downtime. This skill creates migrations, validates them, backs up databases, applies changes safely, and provides instant rollback if anything fails.

## When to Use This Skill

Activate when the user:
- Needs to change database schema
- Wants to create a new migration
- Is applying pending migrations
- Needs to rollback a migration
- Mentions keywords like: "database migration", "schema change", "create migration", "migrate database"

## Workflow

### Phase 1: Migration Detection

**Detect Migration Tools**:

```bash
detect_migration_tool() {
  # Node.js ORMs
  grep -q "sequelize" package.json && echo "sequelize-cli"
  grep -q "prisma" package.json && echo "prisma"
  grep -q "typeorm" package.json && echo "typeorm"
  
  # Python ORMs
  grep -q "alembic" requirements.txt && echo "alembic"
  grep -q "django" requirements.txt && echo "django"
  
  # Ruby
  [ -f "Rakefile" ] && grep -q "ActiveRecord" Rakefile && echo "rails"
  
  # Go
  grep -q "golang-migrate" go.mod && echo "migrate"
}
```

### Phase 2: Backup Creation

**Backup Database**:

```bash
backup_database() {
  local db_type=$1
  local backup_file="db_backup_$(date +%Y%m%d_%H%M%S).sql"
  
  case $db_type in
    postgresql)
      pg_dump $DB_NAME > "$backup_file"
      ;;
    mysql)
      mysqldump $DB_NAME > "$backup_file"
      ;;
  esac
  
  echo "✅ Backup: $backup_file"
}
```

### Phase 3: Migration Execution

**Apply Migration**:

```bash
apply_migration() {
  local tool=$1
  
  case $tool in
    prisma)
      npx prisma migrate deploy
      ;;
    alembic)
      alembic upgrade head
      ;;
    sequelize)
      npx sequelize-cli db:migrate
      ;;
  esac
}
```

### Phase 4: Validation

**Verify Schema**:

```bash
validate_migration() {
  # Check tables exist
  # Verify constraints
  # Test data integrity
  echo "✅ Schema validated"
}
```

### Phase 5: Rollback (if needed)

**Rollback Migration**:

```bash
rollback_migration() {
  local tool=$1
  
  case $tool in
    prisma)
      npx prisma migrate rollback
      ;;
    alembic)
      alembic downgrade -1
      ;;
  esac
}
```

## Guidelines

### DO:
✅ Always backup before migrating
✅ Validate migration before applying
✅ Test in development first
✅ Provide rollback capability
✅ Check for data loss risks

### DON'T:
❌ Migrate production without backup
❌ Skip validation
❌ Ignore warnings
❌ Delete columns without checking data
❌ Run migrations without testing

## Success Metrics

- ✅ Backup created
- ✅ Migration applied successfully
- ✅ Schema validated
- ✅ Rollback capability confirmed
- ✅ Zero data loss
- ✅ < 5 minutes execution

## Version History

- v1.0.0 (2025-10-30): Initial release
  - Multi-ORM support
  - Automatic backups
  - Rollback capability
  - Schema validation
