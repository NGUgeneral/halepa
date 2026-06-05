from abc import ABC, abstractmethod
from typing import List

class NotificationProvider(ABC):
    @abstractmethod
    def broadcast_message(self, text: str, targets: List[str]) -> bool:
        """
        Dispatches a formatted text message to multiple target IDs/Channels.
        Returns True if all dispatches succeed.
        """
        pass