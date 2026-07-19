from pydantic import BaseModel, ConfigDict
from datetime import datetime


class DetectionResult(BaseModel):
    rule_name: str
    description: str
    severity: str
    event_id: int


class DetectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    rule_name: str
    description: str
    severity: str
    event_id: int
    created_at: datetime
    updated_at: datetime
