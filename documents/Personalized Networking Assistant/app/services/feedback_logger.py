import json
from datetime import datetime
from pathlib import Path

FEEDBACK_FILE = Path("feedback.json")


def log_feedback(suggestion: str, action: str):
    entry = {
        "suggestion": suggestion,
        "feedback": action,
        "timestamp": datetime.now().isoformat()
    }

    if FEEDBACK_FILE.exists():
        with open(FEEDBACK_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_feedback():
    if FEEDBACK_FILE.exists():
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)

    return []   