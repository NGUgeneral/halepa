import json
import urllib.request
import urllib.error
import config
from .base import NotificationProvider

class DiscordProvider(NotificationProvider):
    def __init__(self):
        self.urls = config.DISCORD_WEBHOOK_URLS

    @property
    def raw_targets(self) -> str:
        return self.urls

    def _send_to_single_target(self, text: str, target: str) -> bool:
        if "ALARM" in text.upper():
            color = 15158332  # Crimson Red
            title = "🚨 CloudWatch Alarm Triggered"
        elif "OK" in text.upper():
            color = 3066993   # Emerald Green
            title = "✅ Service Recovery Operational"
        else:
            color = 9807270   # Charcoal Grey
            title = "ℹ️ Halepa System Broadcast"

        payload = {
            "embeds": [
                {
                    "title": title,
                    "description": text,
                    "color": color,
                    "footer": {
                        "text": "Halepa Stateless Monitoring Engine"
                    }
                }
            ]
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            target, 
            data=data, 
            headers={"Content-Type": "application/json"}, 
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status in [200, 204]
        except urllib.error.URLError as e:
            print(f"[ERROR] Discord failed for target webhook: {e}")
            return False