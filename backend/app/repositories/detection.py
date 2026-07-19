from sqlalchemy.orm import Session

from app.models.detection import Detection
from app.schemas.detection import DetectionResult


class DetectionRepository:
    @staticmethod
    def create(
        db: Session,
        detection_data: DetectionResult,
    ) -> Detection:
        detection = Detection(
            rule_name=detection_data.rule_name,
            description=detection_data.description,
            severity=detection_data.severity,
            event_id=detection_data.event_id,
        )

        db.add(detection)
        db.commit()
        db.refresh(detection)

        return detection

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Detection]:
        return (
            db.query(Detection)
            .order_by(Detection.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        detection_id: int,
    ) -> Detection | None:
        return db.query(Detection).filter(Detection.id == detection_id).first()
