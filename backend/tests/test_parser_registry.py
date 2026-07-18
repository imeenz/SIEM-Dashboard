import pytest

from app.parsers.registry import ParserRegistry
from app.parsers.ssh_auth import SSHAuthParser


def test_registry_finds_ssh_parser():
    registry = ParserRegistry()

    raw_log = (
        "Jul 19 02:15:43 server01 sshd[1842]: "
        "Failed password for admin from 192.168.1.25 port 54321 ssh2"
    )

    parser = registry.find_parser(raw_log)

    assert isinstance(parser, SSHAuthParser)


def test_registry_parses_ssh_log():
    registry = ParserRegistry()

    raw_log = (
        "Jul 19 02:15:43 server01 sshd[1842]: "
        "Failed password for admin from 192.168.1.25 port 54321 ssh2"
    )

    event = registry.parse(raw_log)

    assert event.source == "ssh"
    assert event.event_type == "failed_login"
    assert str(event.source_ip) == "192.168.1.25"


def test_registry_returns_none_for_unknown_log():
    registry = ParserRegistry()

    parser = registry.find_parser("Unknown application message")

    assert parser is None


def test_registry_raises_error_for_unknown_log():
    registry = ParserRegistry()

    with pytest.raises(ValueError):
        registry.parse("Unknown application message")
