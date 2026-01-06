---
id: NO_HARDCODED_SECRETS
name: No Hardcoded Secrets
include:
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.js"
exclude:
  - "**/*.test.*"
  - "**/*.spec.*"
---

# No Hardcoded Secrets

Sensitive credentials must never be hardcoded in source files.

## What to look for

- Database connection strings with passwords
- API keys (especially those starting with `sk_`, `pk_`, `api_`, etc.)
- JWT secrets or signing keys
- OAuth client secrets
- Encryption keys
- Any password or token literals

## Correct approach

Use environment variables via `process.env` for all secrets:

```typescript
const apiKey = process.env.API_KEY;
const dbUrl = process.env.DATABASE_URL;
```
