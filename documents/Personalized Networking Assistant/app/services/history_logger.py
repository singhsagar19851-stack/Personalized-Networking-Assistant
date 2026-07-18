import json
from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path("history.json")


def log_conversation(data: dict):
    data["timestamp"] = datetime.now().isoformat()

    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append(data)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def load_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)

    return []