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
        # --- Inline HTML-to-Markdown Translation Layer ---
        formatted_text = (
            text.replace("<b>", "**").replace("</b>", "**")      # Bold
                .replace("<i>", "*").replace("</i>", "*")        # Italics
                .replace("<code>", "`").replace("</code>", "`")  # Inline Code
                .replace("<br>", "\n").replace("<br/>", "\n")    # Line Breaks
        )

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
                    "description": formatted_text,
                    "color": color,
                    "footer": {
                        "text": "Halepa"
                    }
                }
            ]
        }
        
        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "HalepaAlertEngine/1.0 (KHTML, like Gecko)"
        }
        req = urllib.request.Request(
            target, 
            data=data, 
            headers=headers, 
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return self._is_successful_status(response.status)
        except urllib.error.URLError as e:
            self._log_failure(target, e)
            return False