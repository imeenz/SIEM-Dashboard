import pytest

from app.parsers.registry import ParserRegistry
from app.parsers.ssh_auth import SSHAuthParser
from app.parsers.syslog import SyslogParser


def test_can_parse_generic_syslog():
    parser = SyslogParser()

    raw_log = "Jul 19 04:30:15 server01 nginx: " "Connection timeout detected"

    assert parser.can_parse(raw_log) is True


def test_parse_generic_syslog():
    parser = SyslogParser()

    raw_log = "Jul 19 04:30:15 server01 nginx: " "Connection timeout detected"

    event = parser.parse(raw_log)

    assert event.source == "syslog:server01"
    assert event.event_type == "nginx_event"
    assert event.severity.value == "low"
    assert event.source_ip is None
    assert event.destination_ip is None
    assert event.message == "Connection timeout detected"


def test_syslog_with_process_id():
    parser = SyslogParser()

    raw_log = "Jul 19 05:10:20 server02 cron[1234]: " "Scheduled task completed"

    event = parser.parse(raw_log)

    assert event.source == "syslog:server02"
    assert event.event_type == "cron_event"
    assert event.message == "Scheduled task completed"


def test_cannot_parse_invalid_syslog():
    parser = SyslogParser()

    assert parser.can_parse("Random unsupported message") is False


def test_parse_invalid_syslog_raises_error():
    parser = SyslogParser()

    with pytest.raises(ValueError):
        parser.parse("Random unsupported message")


def test_registry_prioritizes_ssh_over_generic_syslog():
    registry = ParserRegistry()

    raw_log = (
        "Jul 19 02:15:43 server01 sshd[1842]: "
        "Failed password for admin from "
        "192.168.1.25 port 54321 ssh2"
    )

    parser = registry.find_parser(raw_log)

    assert isinstance(parser, SSHAuthParser)
