from sqlalchemy.orm import Session

from app.models.event import Event
from app.parsers.registry import ParserRegistry
from app.repositories.event import EventRepository


class IngestionService:
    def __init__(self) -> None:
        self.registry = ParserRegistry()

    def ingest_log(self, db: Session, raw_log: str) -> Event:
        event_data = self.registry.parse(raw_log)

        return EventRepository.create(
            db=db,
            event_data=event_data,
        )

    def ingest_logs(
        self,
        db: Session,
        raw_logs: list[str],
    ) -> tuple[list[Event], list[str]]:
        ingested_events = []
        failed_logs = []

        for raw_log in raw_logs:
            raw_log = raw_log.strip()

            if not raw_log:
                continue

            try:
                event = self.ingest_log(
                    db=db,
                    raw_log=raw_log,
                )
                ingested_events.append(event)
            except ValueError:
                failed_logs.append(raw_log)

        return ingested_events, failed_logs
