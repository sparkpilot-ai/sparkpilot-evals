---
id: ASYNC_ERROR_HANDLING
name: Async Error Handling
include:
  - "**/*.ts"
  - "**/*.tsx"
exclude:
  - "**/*.test.*"
---

# Async Error Handling

Async operations must have proper error handling to prevent unhandled rejections.

## Requirements

1. Controller methods should wrap async operations in try/catch
2. Database queries that can fail should have error handling
3. External API calls should handle network failures

## Watch for

- Async functions without try/catch around I/O operations
- Missing error responses in catch blocks
- Errors that are caught but silently swallowed
