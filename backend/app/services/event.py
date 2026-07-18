from sqlalchemy.orm import Session

from app.models.event import Event
from app.repositories.event import EventRepository
from app.schemas.event import EventCreate


class EventService:
    @staticmethod
    def create_event(db: Session, event_data: EventCreate) -> Event:
        return EventRepository.create(db, event_data)

    @staticmethod
    def get_events(
        db: Session,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Event]:
        return EventRepository.get_all(db, skip=skip, limit=limit)

    @staticmethod
    def get_event(db: Session, event_id: int) -> Event | None:
        return EventRepository.get_by_id(db, event_id)
