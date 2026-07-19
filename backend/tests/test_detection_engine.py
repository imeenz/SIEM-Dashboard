from app.detection.engine import DetectionEngine
from app.models.event import Event
from unittest.mock import MagicMock


def test_detect_critical_ids_alert():
    engine = DetectionEngine()

    event = Event(
        id=1,
        source="ids",
        event_type="intrusion_alert",
        severity="critical",
        source_ip="203.0.113.100",
        destination_ip="192.168.1.10",
        message="IDS detected security threat: SQL_INJECTION",
        raw_log="IDS ALERT",
    )

    results = engine.analyze(event)

    assert len(results) == 1
    assert results[0].rule_name == "critical_ids_alert"
    assert results[0].severity == "critical"
    assert results[0].event_id == 1


def test_high_ids_alert_not_detected_by_critical_rule():
    engine = DetectionEngine()

    event = Event(
        id=2,
        source="ids",
        event_type="intrusion_alert",
        severity="high",
        source_ip="10.0.0.50",
        destination_ip="192.168.1.20",
        message="IDS detected security threat: SUSPICIOUS_TRAFFIC",
        raw_log="IDS ALERT",
    )

    results = engine.analyze(event)

    assert results == []


def test_non_ids_event_not_detected():
    engine = DetectionEngine()

    event = Event(
        id=3,
        source="firewall",
        event_type="firewall_block",
        severity="critical",
        source_ip="203.0.113.50",
        destination_ip="192.168.1.10",
        message="Firewall blocked traffic",
        raw_log="FIREWALL BLOCK",
    )

    results = engine.analyze(event)

    assert results == []


def test_engine_detects_brute_force_with_correlation():
    engine = DetectionEngine()

    db = MagicMock()
    db.scalars.return_value.all.return_value = [MagicMock() for _ in range(5)]

    event = Event(
        id=10,
        source="ssh",
        event_type="failed_login",
        severity="high",
        source_ip="192.168.1.100",
        destination_ip=None,
        message="Failed SSH login attempt",
        raw_log="SSH failed login",
    )

    results = engine.analyze_with_correlation(
        db=db,
        event=event,
    )

    assert len(results) == 1
    assert results[0].rule_name == "ssh_brute_force"
    assert results[0].severity == "high"


def test_engine_returns_no_brute_force_below_threshold():
    engine = DetectionEngine()

    db = MagicMock()
    db.scalars.return_value.all.return_value = [MagicMock() for _ in range(4)]

    event = Event(
        id=11,
        source="ssh",
        event_type="failed_login",
        severity="high",
        source_ip="192.168.1.100",
        destination_ip=None,
        message="Failed SSH login attempt",
        raw_log="SSH failed login",
    )

    results = engine.analyze_with_correlation(
        db=db,
        event=event,
    )

    assert results == []
