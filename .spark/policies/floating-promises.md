---
id: FLOATING_PROMISES
name: No Floating Promises
include:
  - "**/*.ts"
  - "**/*.tsx"
exclude:
  - "**/*.test.*"
---

# No Floating Promises

Promises must be awaited or explicitly handled. Unawaited promises can cause:
- Race conditions
- Silent failures
- Unpredictable execution order

## Problem patterns

```typescript
someAsyncFunction();  // Promise ignored
this.sendEmail(user); // If sendEmail is async
```

## Correct patterns

```typescript
await someAsyncFunction();
// or
void someAsyncFunction(); // Explicit fire-and-forget
// or
someAsyncFunction().catch(handleError);
```
