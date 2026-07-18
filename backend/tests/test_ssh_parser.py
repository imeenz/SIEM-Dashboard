import pytest

from app.parsers.ssh_auth import SSHAuthParser


def test_can_parse_failed_ssh_login():
    parser = SSHAuthParser()

    raw_log = (
        "Jul 19 02:15:43 server01 sshd[1842]: "
        "Failed password for admin from 192.168.1.25 port 54321 ssh2"
    )

    assert parser.can_parse(raw_log) is True


def test_parse_failed_ssh_login():
    parser = SSHAuthParser()

    raw_log = (
        "Jul 19 02:15:43 server01 sshd[1842]: "
        "Failed password for admin from 192.168.1.25 port 54321 ssh2"
    )

    event = parser.parse(raw_log)

    assert event.source == "ssh"
    assert event.event_type == "failed_login"
    assert event.severity.value == "high"
    assert str(event.source_ip) == "192.168.1.25"
    assert event.destination_ip is None
    assert event.message == "Failed SSH login attempt for user admin"
    assert event.raw_log == raw_log


def test_parse_invalid_user_ssh_login():
    parser = SSHAuthParser()

    raw_log = (
        "Jul 19 02:15:43 server01 sshd[1842]: "
        "Failed password for invalid user attacker "
        "from 10.0.0.50 port 54321 ssh2"
    )

    event = parser.parse(raw_log)

    assert str(event.source_ip) == "10.0.0.50"
    assert "attacker" in event.message


def test_cannot_parse_unrelated_log():
    parser = SSHAuthParser()

    raw_log = "Application started successfully"

    assert parser.can_parse(raw_log) is False


def test_parse_unsupported_log_raises_error():
    parser = SSHAuthParser()

    with pytest.raises(ValueError):
        parser.parse("Application started successfully")
