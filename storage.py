import json
import os

FILE_PATH = "data/seen.json"

def load_seen():
    if not os.path.exists(FILE_PATH):
        return set()

    try:
        with open(FILE_PATH, "r") as f:
            content = f.read().strip()

            if not content:
                return set()

            return set(json.loads(content))

    except json.JSONDecodeError:
        print("[WARN] seen.json corrompido. Resetando...")
        return set()

def save_seen(seen):
    os.makedirs("data", exist_ok=True)

    with open(FILE_PATH, "w") as f:
        json.dump(list(seen), f, indent=2)