from .base import NotificationProvider
from .telegram import TelegramProvider

# Registry for dynamic strategy resolution
PROVIDERS = {
    "telegram": TelegramProvider
}

def get_provider(name: str) -> NotificationProvider:
    provider_cls = PROVIDERS.get(name.lower())
    if not provider_cls:
        raise ValueError(f"Unsupported notification provider: {name}")
    return provider_cls()