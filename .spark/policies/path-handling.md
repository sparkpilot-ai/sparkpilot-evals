---
id: PATH_HANDLING
name: Safe Path Handling
include:
  - "**/*.rs"
---

# Safe Path Handling

Path operations can fail and should be handled safely.

## Risky patterns

```rust
path.to_str().unwrap()
path.extension().unwrap()
path.canonicalize().unwrap()
```

## Safe patterns

```rust
path.to_str().unwrap_or_default()
path.extension().and_then(|e| e.to_str())
path.canonicalize().ok()
```

## Consider

- Paths may not be valid UTF-8
- Files may not exist when canonicalizing
- Extensions may be missing
