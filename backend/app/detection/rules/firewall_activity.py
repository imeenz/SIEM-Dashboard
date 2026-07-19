from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.event import Event
from app.schemas.detection import DetectionResult


class SuspiciousFirewallActivityRule:
    name = "suspicious_firewall_activity"
    description = "Repeated firewall blocks from the same source IP detected"
    severity = "high"

    def __init__(
        self,
        threshold: int = 5,
        window_minutes: int = 5,
    ) -> None:
        self.threshold = threshold
        self.window_minutes = window_minutes

    def analyze(
        self,
        db: Session,
        event: Event,
    ) -> DetectionResult | None:
        if (
            event.source != "firewall"
            or event.event_type != "firewall_block"
            or event.source_ip is None
        ):
            return None

        window_start = datetime.now(timezone.utc) - timedelta(
            minutes=self.window_minutes
        )

        statement = select(Event).where(
            Event.source == "firewall",
            Event.event_type == "firewall_block",
            Event.source_ip == event.source_ip,
            Event.created_at >= window_start,
        )

        matching_events = db.scalars(statement).all()

        if len(matching_events) < self.threshold:
            return None

        return DetectionResult(
            rule_name=self.name,
            description=self.description,
            severity=self.severity,
            event_id=event.id,
        )
