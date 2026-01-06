---
id: SQL_INJECTION
name: SQL Injection Prevention
include:
  - "**/*.ts"
  - "**/*.tsx"
exclude:
  - "**/*.test.*"
---

# SQL Injection Prevention

Never interpolate user input directly into SQL queries.

## Vulnerable patterns

String interpolation in queries:
```typescript
pool.query(`SELECT * FROM users WHERE id = '${userId}'`)
pool.query(`SELECT * FROM users WHERE name LIKE '%${search}%'`)
```

## Safe patterns

Use parameterized queries:
```typescript
pool.query('SELECT * FROM users WHERE id = $1', [userId])
pool.query('SELECT * FROM users WHERE name LIKE $1', [`%${search}%`])
```
