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
                os.environ[key.strip()] = val.strip().strip("'").strip('"')

load_env_file()

# Telegram
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_IDS = os.environ.get("TELEGRAM_CHAT_IDS", "")

# Slack
SLACK_WEBHOOK_URLS = os.environ.get("SLACK_WEBHOOK_URLS", "")

# MS Teams
TEAMS_WEBHOOK_URLS = os.environ.get("TEAMS_WEBHOOK_URLS", "")

# WhatsApp
WHATSAPP_API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_TARGET_PHONES = os.environ.get("WHATSAPP_TARGET_PHONES", "")