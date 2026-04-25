import json
from datetime import datetime
from pathlib import Path

# History file stored next to this module
HISTORY_PATH = Path(__file__).parent / "history.json"


def _load_history() -> list:
    """Load existing history entries from disk."""
    if not HISTORY_PATH.exists():
        return []

    try:
        return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
    except Exception:
        # If the file is corrupted or unreadable, start fresh
        return []


def _write_history(entries: list) -> None:
    """Persist history entries to disk."""
    HISTORY_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")


def save_entry(query: str, action: str = "", note: str = "") -> None:
    """Save an interaction entry.

    Args:
        query: The raw text/command that was processed.
        action: A short description of what the system did.
        note: Optional additional information (e.g., errors, results).
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "query": query,
        "action": action,
        "note": note,
    }

    history = _load_history()
    history.append(entry)
    _write_history(history)


def read_history() -> list:
    """Return the list of saved history entries."""
    return _load_history()
