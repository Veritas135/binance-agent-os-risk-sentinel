import json


def parse_snapshot(text: str):
    """Parse a JSON snapshot exported/pasted from an Agent OS-compatible client."""
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON snapshot: {exc}") from exc

    if not isinstance(value, dict):
        raise ValueError("Snapshot must be a JSON object.")

    return value
