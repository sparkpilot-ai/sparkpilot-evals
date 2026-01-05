import json
from pathlib import Path

def load_config(path: str) -> dict:
    """Load configuration from JSON file."""
    with open(path) as f:
        return json.load(f)
