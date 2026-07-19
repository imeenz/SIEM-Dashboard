from unittest.mock import MagicMock

from app.detection.rules.firewall_activity import (
    SuspiciousFirewallActivityRule,
)
from app.models.event import Event


def create_firewall_event(
    event_id: int = 1,
    source_ip: str = "203.0.113.50",
) -> Event:
    return Event(
        id=event_id,
        source="firewall",
        event_type="firewall_block",
        severity="medium",
        source_ip=source_ip,
        destination_ip="192.168.1.10",
        message="Firewall blocked suspicious traffic",
        raw_log="FIREWALL BLOCK",
    )


def test_suspicious_firewall_activity_detected_at_threshold():
    rule = SuspiciousFirewallActivityRule(
        threshold=5,
        window_minutes=5,
    )

    db = MagicMock()
    db.scalars.return_value.all.return_value = [MagicMock() for _ in range(5)]

    event = create_firewall_event()

    result = rule.analyze(
        db=db,
        event=event,
    )

    assert result is not None
    assert result.rule_name == "suspicious_firewall_activity"
    assert result.severity == "high"
    assert result.event_id == 1


def test_firewall_activity_not_detected_below_threshold():
    rule = SuspiciousFirewallActivityRule(
        threshold=5,
        window_minutes=5,
    )

    db = MagicMock()
    db.scalars.return_value.all.return_value = [MagicMock() for _ in range(4)]

    event = create_firewall_event()

    result = rule.analyze(
        db=db,
        event=event,
    )

    assert result is None


def test_non_firewall_event_is_ignored():
    rule = SuspiciousFirewallActivityRule()

    db = MagicMock()

    event = Event(
        id=2,
        source="ssh",
        event_type="failed_login",
        severity="medium",
        source_ip="203.0.113.50",
        destination_ip=None,
        message="Failed SSH login",
        raw_log="SSH failed login",
    )

    result = rule.analyze(
        db=db,
        event=event,
    )

    assert result is None
    db.scalars.assert_not_called()


def test_firewall_event_without_source_ip_is_ignored():
    rule = SuspiciousFirewallActivityRule()

    db = MagicMock()

    event = create_firewall_event()
    event.source_ip = None

    result = rule.analyze(
        db=db,
        event=event,
    )

    assert result is None
    db.scalars.assert_not_called()
