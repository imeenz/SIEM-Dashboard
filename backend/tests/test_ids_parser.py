import pytest

from app.parsers.ids_alert import IDSAlertParser


def test_can_parse_ids_alert():
    parser = IDSAlertParser()

    raw_log = (
        "IDS ALERT SRC=203.0.113.100 DST=192.168.1.10 "
        "SIGNATURE=SQL_INJECTION SEVERITY=critical"
    )

    assert parser.can_parse(raw_log) is True


def test_parse_ids_alert():
    parser = IDSAlertParser()

    raw_log = (
        "IDS ALERT SRC=203.0.113.100 DST=192.168.1.10 "
        "SIGNATURE=SQL_INJECTION SEVERITY=critical"
    )

    event = parser.parse(raw_log)

    assert event.source == "ids"
    assert event.event_type == "intrusion_alert"
    assert event.severity.value == "critical"
    assert str(event.source_ip) == "203.0.113.100"
    assert str(event.destination_ip) == "192.168.1.10"
    assert "SQL_INJECTION" in event.message


def test_parse_ids_alert_high_severity():
    parser = IDSAlertParser()

    raw_log = (
        "IDS ALERT SRC=10.0.0.50 DST=192.168.1.20 " "SIGNATURE=PORT_SCAN SEVERITY=high"
    )

    event = parser.parse(raw_log)

    assert event.severity.value == "high"
    assert "PORT_SCAN" in event.message


def test_cannot_parse_unrelated_log():
    parser = IDSAlertParser()

    assert parser.can_parse("Application started successfully") is False


def test_parse_unsupported_ids_log_raises_error():
    parser = IDSAlertParser()

    with pytest.raises(ValueError):
        parser.parse("Application started successfully")
