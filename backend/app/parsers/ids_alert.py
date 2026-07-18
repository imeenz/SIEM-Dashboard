import re

from app.parsers.base import BaseLogParser
from app.schemas.event import EventCreate


class IDSAlertParser(BaseLogParser):
    IDS_PATTERN = re.compile(
        r"IDS ALERT "
        r"SRC=(?P<source_ip>\S+) "
        r"DST=(?P<destination_ip>\S+) "
        r"SIGNATURE=(?P<signature>\S+) "
        r"SEVERITY=(?P<severity>low|medium|high|critical)"
    )

    def can_parse(self, raw_log: str) -> bool:
        return bool(self.IDS_PATTERN.search(raw_log))

    def parse(self, raw_log: str) -> EventCreate:
        match = self.IDS_PATTERN.search(raw_log)

        if match is None:
            raise ValueError("Unsupported IDS alert format")

        source_ip = match.group("source_ip")
        destination_ip = match.group("destination_ip")
        signature = match.group("signature")
        severity = match.group("severity")

        return EventCreate(
            source="ids",
            event_type="intrusion_alert",
            severity=severity,
            source_ip=source_ip,
            destination_ip=destination_ip,
            message=f"IDS detected security threat: {signature}",
            raw_log=raw_log,
        )
