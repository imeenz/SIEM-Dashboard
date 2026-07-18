from app.parsers.base import BaseLogParser
from app.parsers.ssh_auth import SSHAuthParser
from app.schemas.event import EventCreate
from app.parsers.firewall import FirewallParser
from app.parsers.ids_alert import IDSAlertParser
from app.parsers.syslog import SyslogParser


class ParserRegistry:
    def __init__(self) -> None:
        self.parsers: list[BaseLogParser] = [
            SSHAuthParser(),
            FirewallParser(),
            IDSAlertParser(),
            SyslogParser(),
        ]

    def find_parser(self, raw_log: str) -> BaseLogParser | None:
        for parser in self.parsers:
            if parser.can_parse(raw_log):
                return parser

        return None

    def parse(self, raw_log: str) -> EventCreate:
        parser = self.find_parser(raw_log)

        if parser is None:
            raise ValueError("No suitable parser found for the provided log")

        return parser.parse(raw_log)
