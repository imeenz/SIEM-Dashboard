from sqlalchemy.orm import Session

from app.detection.base import BaseDetectionRule
from app.detection.rules.brute_force import BruteForceRule
from app.detection.rules.critical_ids import CriticalIDSRule
from app.models.event import Event
from app.schemas.detection import DetectionResult
from app.detection.rules.port_scan import PortScanRule
from app.detection.rules.firewall_activity import SuspiciousFirewallActivityRule


class DetectionEngine:
    def __init__(self) -> None:
        self.rules: list[BaseDetectionRule] = [
            CriticalIDSRule(),
            PortScanRule(),
        ]

        self.correlation_rules = [
            BruteForceRule(),
            SuspiciousFirewallActivityRule(),
        ]

    def register_rule(self, rule: BaseDetectionRule) -> None:
        self.rules.append(rule)

    def analyze(self, event: Event) -> list[DetectionResult]:
        results = []

        for rule in self.rules:
            if rule.matches(event):
                results.append(
                    DetectionResult(
                        rule_name=rule.name,
                        description=rule.description,
                        severity=event.severity,
                        event_id=event.id,
                    )
                )

        return results

    def analyze_with_correlation(
        self,
        db: Session,
        event: Event,
    ) -> list[DetectionResult]:
        results = self.analyze(event)

        for rule in self.correlation_rules:
            result = rule.analyze(
                db=db,
                event=event,
            )

            if result is not None:
                results.append(result)

        return results
