import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def load_config(path: str) -> dict:
    """Load configuration from JSON file."""
    with open(path) as f:
        return json.load(f)

# BAD: Bare except catches everything including KeyboardInterrupt, SystemExit
def process_data_bad(data: list[dict]) -> list[dict]:
    results = []
    for item in data:
        try:
            result = transform_item(item)
            results.append(result)
        except:  # Catches EVERYTHING - even Ctrl+C!
            logger.error("Failed to process item")
            continue
    return results

# BAD: Catching Exception is better but still too broad
def process_data_also_bad(data: list[dict]) -> list[dict]:
    results = []
    for item in data:
        try:
            result = transform_item(item)
            results.append(result)
        except Exception:  # Too broad - hides bugs
            pass  # Silent failure!
    return results

# GOOD: Catch specific exceptions
def process_data_good(data: list[dict]) -> list[dict]:
    results = []
    for item in data:
        try:
            result = transform_item(item)
            results.append(result)
        except (ValueError, KeyError) as e:
            logger.warning(f"Skipping invalid item: {e}")
            continue
        except TypeError as e:
            logger.error(f"Type error processing item: {e}")
            raise
    return results

def transform_item(item: dict) -> dict:
    return {
        "id": item["id"],
        "value": int(item["value"]) * 2,
    }
