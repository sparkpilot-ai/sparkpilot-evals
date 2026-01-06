---
id: NO_SENSITIVE_LOGGING
name: No Sensitive Data in Logs
include:
  - "**/*.ts"
  - "**/*.tsx"
exclude:
  - "**/*.test.*"
---

# No Sensitive Data in Logs

Never log sensitive information that could be exposed in log files or monitoring systems.

## Never log

- Passwords or credentials
- Full authentication tokens
- Credit card numbers
- Personal identification numbers
- API keys or secrets
- Password reset tokens

## Example violations

```typescript
console.log('Login attempt:', credentials);
console.log(`Reset token: ${token}`);
```

## Acceptable logging

```typescript
console.log('Login attempt for user:', credentials.email);
console.log('Password reset requested for:', email);
```
