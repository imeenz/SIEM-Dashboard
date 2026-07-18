from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.event import EventCreate, EventResponse
from app.services.event import EventService

router = APIRouter(prefix="/events", tags=["Events"])


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    event_data: EventCreate,
    db: Session = Depends(get_db),
) -> EventResponse:
    return EventService.create_event(db, event_data)


@router.get("", response_model=list[EventResponse])
def get_events(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
) -> list[EventResponse]:
    return EventService.get_events(
        db,
        skip=skip,
        limit=limit,
    )


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
) -> EventResponse:
    event = EventService.get_event(db, event_id)

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    return event
