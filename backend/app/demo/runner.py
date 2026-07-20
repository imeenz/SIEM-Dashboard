from sqlalchemy.orm import Session

from app.demo.producer import DemoLogProducer
from app.services.ingestion import IngestionService


def create_demo_producer(
    db: Session,
    interval_seconds: float = 5.0,
) -> DemoLogProducer:
    ingestion_service = IngestionService()

    def ingest_demo_log(raw_log: str) -> None:
        ingestion_service.ingest_log(
            db=db,
            raw_log=raw_log,
        )

    return DemoLogProducer(
        handler=ingest_demo_log,
        interval_seconds=interval_seconds,
    )
