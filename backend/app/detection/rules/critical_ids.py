from app.detection.base import BaseDetectionRule
from app.models.event import Event


class CriticalIDSRule(BaseDetectionRule):
    name = "critical_ids_alert"
    description = "Critical IDS alert detected"

    def matches(self, event: Event) -> bool:
        return (
            event.source == "ids"
            and event.event_type == "intrusion_alert"
            and event.severity == "critical"
        )
