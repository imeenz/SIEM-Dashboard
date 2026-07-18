import re

from app.parsers.base import BaseLogParser
from app.schemas.event import EventCreate


class SSHAuthParser(BaseLogParser):
    FAILED_LOGIN_PATTERN = re.compile(
        r"Failed password for (?:invalid user )?(?P<user>\S+) "
        r"from (?P<source_ip>\S+)"
    )

    def can_parse(self, raw_log: str) -> bool:
        return bool(self.FAILED_LOGIN_PATTERN.search(raw_log))

    def parse(self, raw_log: str) -> EventCreate:
        match = self.FAILED_LOGIN_PATTERN.search(raw_log)

        if match is None:
            raise ValueError("Unsupported SSH authentication log format")

        source_ip = match.group("source_ip")
        user = match.group("user")

        return EventCreate(
            source="ssh",
            event_type="failed_login",
            severity="high",
            source_ip=source_ip,
            destination_ip=None,
            message=f"Failed SSH login attempt for user {user}",
            raw_log=raw_log,
        )
