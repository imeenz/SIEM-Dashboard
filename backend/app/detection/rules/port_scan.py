from app.detection.base import BaseDetectionRule
from app.models.event import Event


class PortScanRule(BaseDetectionRule):
    name = "port_scan_detected"
    description = "Network port scan activity detected"

    def matches(self, event: Event) -> bool:
        return (
            event.source == "ids"
            and event.event_type == "intrusion_alert"
            and "PORT_SCAN" in event.message.upper()
        )
