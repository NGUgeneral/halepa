import json
import urllib.request
import urllib.error
from typing import List
import config
from .base import NotificationProvider

class TelegramProvider(NotificationProvider):
    def __init__(self):
        self.token = config.TELEGRAM_BOT_TOKEN
        self.raw_targets = config.TELEGRAM_CHAT_IDS
        
        if not self.token:
            raise ValueError("Missing required TELEGRAM_BOT_TOKEN configuration.")
        
        self.url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def _send_to_single_target(self, text: str, chat_id: str) -> bool:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status == 200
        except urllib.error.URLError as e:
            print(f"[ERROR] Failed to send to Telegram target {chat_id}: {e}")
            return False

    def broadcast_message(self, text: str, targets: List[str] = None) -> bool:
        if targets is not None:
            subscriber_list = targets
        else:
            subscriber_list = [c.strip() for c in self.raw_targets.strip("[] ").split(",") if c.strip()]
        
        if not subscriber_list:
            print("[WARNING] No notification targets available. Aborting broadcast.")
            return False
            
        success_flags = [self._send_to_single_target(text, chat_id) for chat_id in subscriber_list]
        return all(success_flags)