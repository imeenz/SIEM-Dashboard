from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Event(BaseModel):
    __tablename__ = "events"

    source: Mapped[str] = mapped_column(String(100), nullable=False)

    event_type: Mapped[str] = mapped_column(String(100), nullable=False)

    severity: Mapped[str] = mapped_column(String(20), nullable=False)

    source_ip: Mapped[str | None] = mapped_column(String(45), nullable=True)

    destination_ip: Mapped[str | None] = mapped_column(String(45), nullable=True)

    message: Mapped[str] = mapped_column(Text, nullable=False)

    raw_log: Mapped[str] = mapped_column(Text, nullable=False)
