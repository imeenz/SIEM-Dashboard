import re

from app.parsers.base import BaseLogParser
from app.schemas.event import EventCreate


class SyslogParser(BaseLogParser):
    SYSLOG_PATTERN = re.compile(
        r"^(?P<timestamp>[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}) "
        r"(?P<hostname>\S+) "
        r"(?P<process>[\w.-]+)(?:\[\d+\])?: "
        r"(?P<message>.+)$"
    )

    def can_parse(self, raw_log: str) -> bool:
        return bool(self.SYSLOG_PATTERN.search(raw_log))

    def parse(self, raw_log: str) -> EventCreate:
        match = self.SYSLOG_PATTERN.search(raw_log)

        if match is None:
            raise ValueError("Unsupported syslog format")

        hostname = match.group("hostname")
        process = match.group("process")
        message = match.group("message")

        return EventCreate(
            source=f"syslog:{hostname}",
            event_type=f"{process}_event",
            severity="low",
            source_ip=None,
            destination_ip=None,
            message=message,
            raw_log=raw_log,
        )
