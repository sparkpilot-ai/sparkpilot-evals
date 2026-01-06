---
id: NO_UNWRAP
name: No Unwrap in Library Code
include:
  - "**/*.rs"
exclude:
  - "**/tests/**"
  - "**/*_test.rs"
  - "**/main.rs"
---

# No Unwrap in Library Code

Library code should propagate errors rather than panic.

## Problematic patterns

- `.unwrap()` on Result or Option
- `.expect("...")` in library modules

## Preferred alternatives

- Use `?` operator to propagate errors
- Use `.unwrap_or()` or `.unwrap_or_default()` for defaults
- Return `Result<T, E>` from functions
