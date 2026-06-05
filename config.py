import os
from pathlib import Path

def load_env_file():
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        return
        
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip("'").strip('"')
                if key:
                    os.environ[key] = val

load_env_file()

HALEPA_PROVIDER = os.environ.get("HALEPA_PROVIDER", "telegram")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_IDS = os.environ.get("TELEGRAM_CHAT_IDS", "")
