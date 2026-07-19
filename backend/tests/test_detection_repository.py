from app.models.detection import Detection
from app.repositories.detection import DetectionRepository
from app.schemas.detection import DetectionResult


def test_create_detection(db_session):
    detection_data = DetectionResult(
        rule_name="critical_ids_alert",
        description="Critical IDS alert detected",
        severity="critical",
        event_id=1,
    )

    detection = DetectionRepository.create(
        db=db_session,
        detection_data=detection_data,
    )

    assert detection.id is not None
    assert detection.rule_name == "critical_ids_alert"
    assert detection.description == "Critical IDS alert detected"
    assert detection.severity == "critical"
    assert detection.event_id == 1

    stored_detection = (
        db_session.query(Detection).filter(Detection.id == detection.id).first()
    )

    assert stored_detection is not None
    assert stored_detection.rule_name == "critical_ids_alert"
