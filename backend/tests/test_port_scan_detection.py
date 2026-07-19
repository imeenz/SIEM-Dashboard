from app.detection.rules.port_scan import PortScanRule
from app.models.event import Event


def test_port_scan_detected():
    rule = PortScanRule()

    event = Event(
        id=1,
        source="ids",
        event_type="intrusion_alert",
        severity="high",
        source_ip="10.0.0.50",
        destination_ip="192.168.1.20",
        message="IDS detected security threat: PORT_SCAN",
        raw_log="IDS ALERT",
    )

    assert rule.matches(event) is True


def test_non_port_scan_ids_alert_not_detected():
    rule = PortScanRule()

    event = Event(
        id=2,
        source="ids",
        event_type="intrusion_alert",
        severity="critical",
        source_ip="203.0.113.100",
        destination_ip="192.168.1.10",
        message="IDS detected security threat: SQL_INJECTION",
        raw_log="IDS ALERT",
    )

    assert rule.matches(event) is False


def test_non_ids_event_not_detected_as_port_scan():
    rule = PortScanRule()

    event = Event(
        id=3,
        source="firewall",
        event_type="firewall_block",
        severity="high",
        source_ip="10.0.0.50",
        destination_ip="192.168.1.20",
        message="PORT_SCAN",
        raw_log="FIREWALL BLOCK",
    )

    assert rule.matches(event) is False
