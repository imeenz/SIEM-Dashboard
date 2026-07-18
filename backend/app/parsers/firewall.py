import re

from app.parsers.base import BaseLogParser
from app.schemas.event import EventCreate


class FirewallParser(BaseLogParser):
    FIREWALL_PATTERN = re.compile(
        r"FIREWALL (?P<action>BLOCK|ALLOW) "
        r"SRC=(?P<source_ip>\S+) "
        r"DST=(?P<destination_ip>\S+) "
        r"PROTO=(?P<protocol>\S+) "
        r"SPT=(?P<source_port>\d+) "
        r"DPT=(?P<destination_port>\d+)"
    )

    def can_parse(self, raw_log: str) -> bool:
        return bool(self.FIREWALL_PATTERN.search(raw_log))

    def parse(self, raw_log: str) -> EventCreate:
        match = self.FIREWALL_PATTERN.search(raw_log)

        if match is None:
            raise ValueError("Unsupported firewall log format")

        action = match.group("action")
        source_ip = match.group("source_ip")
        destination_ip = match.group("destination_ip")
        protocol = match.group("protocol")
        destination_port = match.group("destination_port")

        severity = "medium" if action == "BLOCK" else "low"

        return EventCreate(
            source="firewall",
            event_type=f"firewall_{action.lower()}",
            severity=severity,
            source_ip=source_ip,
            destination_ip=destination_ip,
            message=(
                f"Firewall {action.lower()} event: "
                f"{protocol} traffic to port {destination_port}"
            ),
            raw_log=raw_log,
        )
