from typing import Iterator
import config
from .base import NotificationProvider
from .telegram import TelegramProvider

PROVIDER_MAPPING = {
    "telegram": (config.TELEGRAM_BOT_TOKEN, TelegramProvider),
    # "slack": (config.SLACK_WEBHOOK_URLS, SlackProvider),
    # "teams": (config.TEAMS_WEBHOOK_URLS, TeamsProvider),
}

def get_active_providers() -> Iterator[NotificationProvider]:
    for name, (credential, provider_cls) in PROVIDER_MAPPING.items():
        if credential:
            yield provider_cls()