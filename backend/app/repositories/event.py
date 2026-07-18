from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.event import Event
from app.schemas.event import EventCreate


class EventRepository:
    @staticmethod
    def create(db: Session, event_data: EventCreate) -> Event:
        data = event_data.model_dump(mode="json")
        event = Event(**data)

        db.add(event)
        db.commit()
        db.refresh(event)

        return event

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Event]:
        statement = (
            select(Event).order_by(Event.created_at.desc()).offset(skip).limit(limit)
        )
        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_id(db: Session, event_id: int) -> Event | None:
        return db.get(Event, event_id)
