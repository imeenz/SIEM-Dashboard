from abc import ABC, abstractmethod

from app.models.event import Event


class BaseDetectionRule(ABC):
    name: str
    description: str

    @abstractmethod
    def matches(self, event: Event) -> bool:
        """Return True when the event matches this detection rule."""
        raise NotImplementedError
