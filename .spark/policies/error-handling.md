---
id: ERROR_HANDLING
name: Rust Error Handling
severity: warning
include:
  - "**/*.rs"
---

# Rust Error Context Policy

Errors should include context for debugging.

## Rules

1. **Add Context**: Use `.context()` or `.with_context()` from anyhow
   - Every `?` should ideally have context explaining what operation failed

2. **Include Dynamic Info**: Use `.with_context(|| format!(...))` to include
   file paths, IDs, or other dynamic information in error messages

3. **Chain Errors**: Don't swallow errors - propagate with context

## Examples

BAD:
```rust
fn load_user(id: u64) -> Result<User> {
    let data = db.query(id)?;  // "record not found" - which record?
    Ok(parse_user(data)?)
}
```

GOOD:
```rust
fn load_user(id: u64) -> Result<User> {
    let data = db.query(id)
        .with_context(|| format!("Failed to load user {}", id))?;
    parse_user(data)
        .context("Failed to parse user data")
}
```
