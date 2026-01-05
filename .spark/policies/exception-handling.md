---
id: EXCEPTION_HANDLING
name: Python Exception Handling
severity: warning
include:
  - "**/*.py"
---

# Python Exception Handling Policy

Avoid catching too broad of exceptions.

## Rules

1. **No Bare Except**: Never use `except:` without specifying exception types
   - Catches KeyboardInterrupt, SystemExit, GeneratorExit
   - Makes debugging impossible - you don't know what failed

2. **Avoid Broad Exception**: Don't catch `Exception` unless re-raising
   - Hides bugs by catching unexpected errors
   - If you must catch Exception, log and re-raise

3. **Catch Specific Exceptions**: List the exceptions you expect
   - `except (ValueError, KeyError)` is clear about what can fail
   - Document why each exception might occur

4. **Never Silent Failures**: Don't use `pass` in except blocks
   - At minimum, log the error
   - Consider whether to continue or abort

## Examples

BAD:
```python
try:
    do_something()
except:  # Catches Ctrl+C!
    pass
```

BAD:
```python
try:
    do_something()
except Exception:  # Too broad
    pass  # Silent failure
```

GOOD:
```python
try:
    do_something()
except ValueError as e:
    logger.warning(f"Invalid value: {e}")
except IOError as e:
    logger.error(f"IO error: {e}")
    raise
```
