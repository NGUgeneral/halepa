from abc import ABC, abstractmethod
from typing import List

class NotificationProvider(ABC):
    @property
    @abstractmethod
    def raw_targets(self) -> str:
        """Must return the raw configuration string from config.py (e.g., config.SLACK_WEBHOOK_URLS)."""
        pass

    @abstractmethod
    def _send_to_single_target(self, text: str, target: str) -> bool:
        """Must execute the platform-specific HTTP payload dispatch."""
        pass

    def broadcast_message(self, text: str, targets: List[str] = None) -> bool:
        """
        Unified fan-out orchestration layer. Handles target normalization
        and sequential execution across all downstream providers.
        """
        if targets is not None:
            subscriber_list = targets
        else:
            subscriber_list = [c.strip() for c in self.raw_targets.strip("[] ").split(",") if c.strip()]

        if not subscriber_list:
            print(f"[WARNING] {self.__class__.__name__} initialized with zero targets. Skipping.")
            return False

        success_flags = [self._send_to_single_target(text, target) for target in subscriber_list]
        return all(success_flags)
    
    def _is_successful_status(self, status: int) -> bool:
        return status in (200, 201, 204)
    
    def _log_failure(self, target: str, exception: Exception):
        print(f"[ERROR] {self.__class__.__name__} failed for target {target}: {exception}")