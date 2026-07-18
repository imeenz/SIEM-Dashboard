import pytest

from app.parsers.firewall import FirewallParser


def test_can_parse_firewall_block():
    parser = FirewallParser()

    raw_log = (
        "Jul 19 03:20:15 firewall01 kernel: "
        "FIREWALL BLOCK SRC=203.0.113.50 DST=192.168.1.10 "
        "PROTO=TCP SPT=45678 DPT=22"
    )

    assert parser.can_parse(raw_log) is True


def test_parse_firewall_block():
    parser = FirewallParser()

    raw_log = (
        "Jul 19 03:20:15 firewall01 kernel: "
        "FIREWALL BLOCK SRC=203.0.113.50 DST=192.168.1.10 "
        "PROTO=TCP SPT=45678 DPT=22"
    )

    event = parser.parse(raw_log)

    assert event.source == "firewall"
    assert event.event_type == "firewall_block"
    assert event.severity.value == "medium"
    assert str(event.source_ip) == "203.0.113.50"
    assert str(event.destination_ip) == "192.168.1.10"
    assert "TCP" in event.message
    assert "22" in event.message


def test_parse_firewall_allow():
    parser = FirewallParser()

    raw_log = (
        "Jul 19 03:20:15 firewall01 kernel: "
        "FIREWALL ALLOW SRC=10.0.0.20 DST=192.168.1.10 "
        "PROTO=TCP SPT=50000 DPT=443"
    )

    event = parser.parse(raw_log)

    assert event.event_type == "firewall_allow"
    assert event.severity.value == "low"


def test_cannot_parse_unrelated_log():
    parser = FirewallParser()

    assert parser.can_parse("Application started successfully") is False


def test_parse_unsupported_log_raises_error():
    parser = FirewallParser()

    with pytest.raises(ValueError):
        parser.parse("Application started successfully")
