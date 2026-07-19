from unittest.mock import MagicMock

from app.detection.rules.brute_force import BruteForceRule
from app.models.event import Event


def create_ssh_event(
    event_id: int = 1,
    source_ip: str = "192.168.1.100",
) -> Event:
    return Event(
        id=event_id,
        source="ssh",
        event_type="failed_login",
        severity="medium",
        source_ip=source_ip,
        destination_ip=None,
        message="Failed SSH login attempt",
        raw_log="SSH failed login",
    )


def test_brute_force_detected_at_threshold():
    rule = BruteForceRule(
        threshold=5,
        window_minutes=5,
    )

    db = MagicMock()
    db.scalars.return_value.all.return_value = [MagicMock() for _ in range(5)]

    event = create_ssh_event()

    result = rule.analyze(
        db=db,
        event=event,
    )

    assert result is not None
    assert result.rule_name == "ssh_brute_force"
    assert result.severity == "high"
    assert result.event_id == 1


def test_brute_force_not_detected_below_threshold():
    rule = BruteForceRule(
        threshold=5,
        window_minutes=5,
    )

    db = MagicMock()
    db.scalars.return_value.all.return_value = [MagicMock() for _ in range(4)]

    event = create_ssh_event()

    result = rule.analyze(
        db=db,
        event=event,
    )

    assert result is None


def test_non_ssh_event_is_ignored():
    rule = BruteForceRule()

    db = MagicMock()

    event = Event(
        id=2,
        source="firewall",
        event_type="firewall_block",
        severity="high",
        source_ip="192.168.1.100",
        destination_ip="192.168.1.10",
        message="Firewall blocked traffic",
        raw_log="FIREWALL BLOCK",
    )

    result = rule.analyze(
        db=db,
        event=event,
    )

    assert result is None
    db.scalars.assert_not_called()


def test_ssh_event_without_source_ip_is_ignored():
    rule = BruteForceRule()

    db = MagicMock()

    event = create_ssh_event()
    event.source_ip = None

    result = rule.analyze(
        db=db,
        event=event,
    )

    assert result is None
    db.scalars.assert_not_called()
