import json
import urllib.request
import urllib.error
from typing import List
import config
from .base import NotificationProvider

class TeamsProvider(NotificationProvider):
    def __init__(self):
        self.raw_targets = config.TEAMS_WEBHOOK_URLS

    def _send_to_single_webhook(self, text: str, webhook_url: str) -> bool:
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "FFA500",
            "summary": "Halepa Alert System",
            "sections": [{
                "activityTitle": "Halepa Notification Engine",
                "text": text.replace("\n", "<br/>")
            }]
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status in (200, 201)
        except urllib.error.URLError as e:
            print(f"[ERROR] MS Teams dispatch failed: {e}")
            return False

    def broadcast_message(self, text: str, targets: List[str] = None) -> bool:
        if targets is not None:
            subscriber_list = targets
        else:
            subscriber_list = [c.strip() for c in self.raw_targets.strip("[] ").split(",") if c.strip()]
            
        if not subscriber_list:
            return False
            
        return all(self._send_to_single_webhook(text, url) for url in subscriber_list)