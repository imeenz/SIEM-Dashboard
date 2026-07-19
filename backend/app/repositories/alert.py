from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.schemas.alert import AlertCreate


class AlertRepository:
    @staticmethod
    def create(
        db: Session,
        alert_data: AlertCreate,
    ) -> Alert:
        alert = Alert(
            title=alert_data.title,
            severity=alert_data.severity,
            detection_id=alert_data.detection_id,
            status="open",
        )

        db.add(alert)
        db.commit()
        db.refresh(alert)

        return alert

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: str | None = None,
        severity: str | None = None,
    ) -> list[Alert]:
        query = db.query(Alert)

        if status is not None:
            query = query.filter(Alert.status == status)

        if severity is not None:
            query = query.filter(Alert.severity == severity)

        return query.order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(
        db: Session,
        alert_id: int,
    ) -> Alert | None:
        return db.query(Alert).filter(Alert.id == alert_id).first()

    @staticmethod
    def update_status(
        db: Session,
        alert: Alert,
        status: str,
    ) -> Alert:
        alert.status = status

        db.commit()
        db.refresh(alert)

        return alert

    @staticmethod
    def get_open_by_detection_rule_and_source(
        db: Session,
        rule_name: str,
        source_ip: str | None,
    ) -> Alert | None:
        from app.models.detection import Detection
        from app.models.event import Event

        query = (
            db.query(Alert)
            .join(
                Detection,
                Alert.detection_id == Detection.id,
            )
            .join(
                Event,
                Detection.event_id == Event.id,
            )
            .filter(
                Detection.rule_name == rule_name,
                Alert.status.in_(["open", "investigating"]),
            )
        )

        if source_ip is None:
            query = query.filter(Event.source_ip.is_(None))
        else:
            query = query.filter(Event.source_ip == source_ip)

        return query.first()
