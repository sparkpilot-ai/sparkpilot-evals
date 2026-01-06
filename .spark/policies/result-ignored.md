---
id: RESULT_IGNORED
name: Results Must Be Handled
include:
  - "**/*.rs"
exclude:
  - "**/tests/**"
---

# Results Must Be Handled

Ignoring Result values can hide errors silently.

## Problem

```rust
fs::remove_dir_all(path);  // Result ignored
pool.query("DELETE ...");   // Result ignored
```

The operation may fail but the code continues as if it succeeded.

## Solution

Either handle the result or explicitly acknowledge ignoring it:

```rust
fs::remove_dir_all(path)?;
// or
let _ = fs::remove_dir_all(path);  // Explicit ignore
```
