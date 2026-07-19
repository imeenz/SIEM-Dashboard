from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertCreate(BaseModel):
    title: str
    severity: str
    detection_id: int


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    severity: str
    status: str
    detection_id: int
    created_at: datetime
    updated_at: datetime


class AlertStatusUpdate(BaseModel):
    status: str
