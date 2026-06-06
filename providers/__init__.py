from typing import Iterator
import config
from providers.discord import DiscordProvider
from .base import NotificationProvider
from .telegram import TelegramProvider
from .slack import SlackProvider
from .teams import TeamsProvider
from .whatsapp import WhatsAppProvider

PROVIDER_MAPPING = {
    "discord": (config.DISCORD_WEBHOOK_URLS, DiscordProvider),
    "telegram": (config.TELEGRAM_BOT_TOKEN, TelegramProvider),
    "slack": (config.SLACK_WEBHOOK_URLS, SlackProvider),
    "teams": (config.TEAMS_WEBHOOK_URLS, TeamsProvider),
    "whatsapp": (config.WHATSAPP_API_TOKEN, WhatsAppProvider),
}

def get_active_providers() -> Iterator[NotificationProvider]:
    for name, (credential, provider_cls) in PROVIDER_MAPPING.items():
        if credential:
            yield provider_cls()