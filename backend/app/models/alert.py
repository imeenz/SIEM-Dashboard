from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Alert(BaseModel):
    __tablename__ = "alerts"

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="open",
        index=True,
    )

    detection_id: Mapped[int] = mapped_column(
        ForeignKey("detections.id"),
        nullable=False,
        index=True,
    )
