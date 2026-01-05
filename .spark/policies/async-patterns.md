---
id: ASYNC_PATTERNS
name: Async Patterns
severity: warning
include:
  - "**/*.ts"
  - "**/*.tsx"
---

# Async/Await Error Handling Policy

Ensure async operations have proper error handling.

## Rules

1. **Try/Catch Required**: Async functions that perform I/O should have try/catch
   - Database operations
   - Network requests (fetch, axios)
   - File system operations

2. **Response Validation**: Check response.ok before parsing JSON
   - `if (!response.ok)` should be checked

3. **Error Propagation**: Errors should be logged and re-thrown or handled

## Examples

BAD:
```typescript
async function fetchData() {
  const response = await fetch('/api/data');
  return response.json();  // No error handling!
}
```

GOOD:
```typescript
async function fetchData() {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Fetch failed:', error);
    throw error;
  }
}
```
