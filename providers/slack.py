import json
import urllib.request
import urllib.error
from typing import List
import config
from .base import NotificationProvider

class SlackProvider(NotificationProvider):
    def __init__(self):
        self.raw_targets = config.SLACK_WEBHOOK_URLS

    def _convert_to_slack_markdown(self, html_text: str) -> str:
        return html_text.replace("<b>", "*").replace("</b>", "*") \
                        .replace("<code>", "`").replace("</code>", "`") \
                        .replace("\n", "\n")

    def _send_to_single_webhook(self, text: str, webhook_url: str) -> bool:
        payload = {"text": self._convert_to_slack_markdown(text)}
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
            print(f"[ERROR] Slack dispatch failed for webhook: {e}")
            return False

    def broadcast_message(self, text: str, targets: List[str] = None) -> bool:
        if targets is not None:
            subscriber_list = targets
        else:
            subscriber_list = [c.strip() for c in self.raw_targets.strip("[] ").split(",") if c.strip()]
            
        if not subscriber_list:
            return False
            
        return all(self._send_to_single_webhook(text, url) for url in subscriber_list)