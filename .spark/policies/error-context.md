---
id: ERROR_CONTEXT
name: Error Context Required
include:
  - "**/*.rs"
exclude:
  - "**/tests/**"
---

# Error Context Required

Errors should include context about what operation failed.

## Problem

Using just `?` loses context about what was being attempted:

```rust
let content = fs::read_to_string(path)?;
```

## Better approach

Add context using anyhow or map_err:

```rust
let content = fs::read_to_string(path)
    .map_err(|e| format!("Failed to read {}: {}", path.display(), e))?;
```

Or with anyhow:

```rust
let content = fs::read_to_string(path)
    .context("Failed to read configuration file")?;
```
