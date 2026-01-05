---
id: ERROR_HANDLING
name: Rust Error Handling
severity: warning
include:
  - "**/*.rs"
---

# Rust Error Handling Policy

Avoid panicking in production Rust code.

## Rules

1. **No unwrap()**: Do not use `.unwrap()` except in tests
   - Use `?` operator to propagate errors
   - Use `.unwrap_or()`, `.unwrap_or_default()`, or `.unwrap_or_else()` for defaults

2. **No expect() in libraries**: Library code should return Result, not panic
   - `expect()` is acceptable in binaries/main.rs after proper error handling

3. **Error Context**: Use `anyhow` or `thiserror` for error context
   - `.context("message")` instead of `.expect("message")`

## Examples

BAD:
```rust
fn load_file(path: &str) -> String {
    fs::read_to_string(path).unwrap()
}
```

GOOD:
```rust
fn load_file(path: &str) -> Result<String, io::Error> {
    fs::read_to_string(path)
}
```
