from abc import ABC, abstractmethod

from app.schemas.event import EventCreate


class BaseLogParser(ABC):
    @abstractmethod
    def can_parse(self, raw_log: str) -> bool:
        """Return True if this parser can handle the given log."""
        pass

    @abstractmethod
    def parse(self, raw_log: str) -> EventCreate:
        """Parse a raw log into the normalized SIEM event format."""
        pass
