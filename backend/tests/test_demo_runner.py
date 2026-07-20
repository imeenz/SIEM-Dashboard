from app.demo.runner import create_demo_producer
from app.models.event import Event


def test_demo_producer_ingests_event(db_session):
    producer = create_demo_producer(
        db=db_session,
        interval_seconds=0,
    )

    producer.produce_once()

    events = db_session.query(Event).all()

    assert len(events) >= 1
