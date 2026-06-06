import json
import urllib.request
import urllib.error
import config
from .base import NotificationProvider

class TelegramProvider(NotificationProvider):
    def __init__(self):
        self.token = config.TELEGRAM_BOT_TOKEN
        if not self.token:
            raise ValueError("Missing required TELEGRAM_BOT_TOKEN configuration.")
        self.url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    @property
    def raw_targets(self) -> str:
        return config.TELEGRAM_CHAT_IDS

    def _send_to_single_target(self, text: str, target: str) -> bool:
        payload = {
            "chat_id": target,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.url, data=data, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return self._is_successful_status(response.status)
        except urllib.error.URLError as e:
            self._log_failure(target, e)
            return False