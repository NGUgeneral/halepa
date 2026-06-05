import json
import urllib.request
import urllib.error
import config
from .base import NotificationProvider

class TeamsProvider(NotificationProvider):
    @property
    def raw_targets(self) -> str:
        return config.TEAMS_WEBHOOK_URLS

    def _send_to_single_target(self, text: str, target: str) -> bool:
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "FFA500",
            "summary": "Halepa Alert System",
            "sections": [{"activityTitle": "Halepa Notification Engine", "text": text.replace("\n", "<br/>")}]
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(target, data=data, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status in (200, 201)
        except urllib.error.URLError as e:
            print(f"[ERROR] MS Teams failed for webhook {target}: {e}")
            return False