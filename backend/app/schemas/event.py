from datetime import datetime
from enum import Enum
from ipaddress import IPv4Address, IPv6Address

from pydantic import BaseModel, ConfigDict


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EventCreate(BaseModel):
    source: str
    event_type: str
    severity: Severity
    source_ip: IPv4Address | IPv6Address | None = None
    destination_ip: IPv4Address | IPv6Address | None = None
    message: str
    raw_log: str


class EventResponse(EventCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
