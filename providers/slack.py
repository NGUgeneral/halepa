import json
import urllib.request
import urllib.error
import config
from .base import NotificationProvider

class SlackProvider(NotificationProvider):
    @property
    def raw_targets(self) -> str:
        return config.SLACK_WEBHOOK_URLS

    def _convert_to_slack_markdown(self, html_text: str) -> str:
        return html_text.replace("<b>", "*").replace("</b>", "*").replace("<code>", "`").replace("</code>", "`")

    def _send_to_single_target(self, text: str, target: str) -> bool:
        payload = {"text": self._convert_to_slack_markdown(text)}
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(target, data=data, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status in (200, 201)
        except urllib.error.URLError as e:
            print(f"[ERROR] Slack failed for webhook {target}: {e}")
            return False