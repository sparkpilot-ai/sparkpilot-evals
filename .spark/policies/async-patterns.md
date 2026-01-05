---
id: ASYNC_PATTERNS
name: Async Patterns
severity: warning
include:
  - "**/*.ts"
  - "**/*.tsx"
---

# Async/Await Patterns Policy

Ensure proper handling of asynchronous operations in TypeScript/JavaScript.

## Rules

1. **Floating Promises**: All Promises must be awaited or explicitly handled
   - `Promise.all()`, `Promise.race()`, `Promise.allSettled()` must be awaited
   - Async function calls must be awaited or have `.then()/.catch()`

2. **Async in Loops**: Avoid async functions in `forEach`
   - Use `for...of` or `Promise.all(array.map(...))` instead

3. **Error Handling**: Async operations should have error handling
   - Use try/catch around await expressions
   - Or use `.catch()` on promise chains

## Examples

BAD:
```typescript
function loadData() {
  Promise.all([fetchA(), fetchB()]);  // Floating promise!
  return 'done';
}
```

GOOD:
```typescript
async function loadData() {
  await Promise.all([fetchA(), fetchB()]);
  return 'done';
}
```
