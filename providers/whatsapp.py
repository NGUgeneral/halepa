import json
import urllib.request
import urllib.error
from typing import List
import config
from .base import NotificationProvider

class WhatsAppProvider(NotificationProvider):
    def __init__(self):
        self.token = config.WHATSAPP_API_TOKEN
        self.phone_id = config.WHATSAPP_PHONE_NUMBER_ID
        self.raw_targets = config.WHATSAPP_TARGET_PHONES
        
        self.url = f"https://graph.facebook.com/v18.0/{self.phone_id}/messages" if self.phone_id else None

    def _strip_html_tags(self, html_text: str) -> str:
        """Simplifies the engine output to plain text for WhatsApp compatibility."""
        return html_text.replace("<b>", "").replace("</b>", "") \
                        .replace("<code>", "").replace("</code>", "")

    def _send_to_single_phone(self, text: str, phone: str) -> bool:
        if not self.url or not self.token:
            return False
            
        payload = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "text",
            "text": {"body": self._strip_html_tags(text)}
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.url,
            data=data,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status in (200, 201)
        except urllib.error.URLError as e:
            print(f"[ERROR] WhatsApp dispatch failed to {phone}: {e}")
            return False

    def broadcast_message(self, text: str, targets: List[str] = None) -> bool:
        if targets is not None:
            subscriber_list = targets
        else:
            subscriber_list = [c.strip() for c in self.raw_targets.strip("[] ").split(",") if c.strip()]
            
        if not subscriber_list or not self.token:
            return False
            
        return all(self._send_to_single_phone(text, num) for num in subscriber_list)