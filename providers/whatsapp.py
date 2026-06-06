import json
import urllib.request
import urllib.error
import config
from .base import NotificationProvider

class WhatsAppProvider(NotificationProvider):
    def __init__(self):
        self.token = config.WHATSAPP_API_TOKEN
        self.phone_id = config.WHATSAPP_PHONE_NUMBER_ID
        self.url = f"https://graph.facebook.com/v18.0/{self.phone_id}/messages" if self.phone_id else None

    @property
    def raw_targets(self) -> str:
        return config.WHATSAPP_TARGET_PHONES

    def _strip_html_tags(self, html_text: str) -> str:
        return html_text.replace("<b>", "").replace("</b>", "").replace("<code>", "").replace("</code>", "")

    def _send_to_single_target(self, text: str, target: str) -> bool:
        if not self.url or not self.token:
            return False
        payload = {
            "messaging_product": "whatsapp",
            "to": target,
            "type": "text",
            "text": {"body": self._strip_html_tags(text)}
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.url,
            data=data,
            headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return self._is_successful_status(response.status)
        except urllib.error.URLError as e:
            self._log_failure(target, e)
            return False