from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.event import Event
from app.schemas.detection import DetectionResult


class BruteForceRule:
    name = "ssh_brute_force"
    description = "Possible SSH brute-force attack detected"
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
            event.source != "ssh"
            or event.event_type != "failed_login"
            or event.source_ip is None
        ):
            return None

        window_start = datetime.now(timezone.utc) - timedelta(
            minutes=self.window_minutes
        )

        statement = select(Event).where(
            Event.source == "ssh",
            Event.event_type == "failed_login",
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
