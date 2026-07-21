from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.alert import AlertRepository
from app.schemas.alert import AlertResponse, AlertStatusUpdate
from app.dependencies.auth import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)],
)

VALID_ALERT_STATUSES = {
    "open",
    "investigating",
    "resolved",
}


@router.get(
    "",
    response_model=list[AlertResponse],
)
def get_alerts(
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    severity: str | None = None,
    db: Session = Depends(get_db),
) -> list[AlertResponse]:
    return AlertRepository.get_all(
        db=db,
        skip=skip,
        limit=limit,
        status=status,
        severity=severity,
    )


@router.get(
    "/{alert_id}",
    response_model=AlertResponse,
)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
) -> AlertResponse:
    alert = AlertRepository.get_by_id(
        db=db,
        alert_id=alert_id,
    )

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    return alert


@router.patch(
    "/{alert_id}/status",
    response_model=AlertResponse,
)
def update_alert_status(
    alert_id: int,
    status_update: AlertStatusUpdate,
    db: Session = Depends(get_db),
) -> AlertResponse:
    if status_update.status not in VALID_ALERT_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid alert status",
        )

    alert = AlertRepository.get_by_id(
        db=db,
        alert_id=alert_id,
    )

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    return AlertRepository.update_status(
        db=db,
        alert=alert,
        status=status_update.status,
    )
