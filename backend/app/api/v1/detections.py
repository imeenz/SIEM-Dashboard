from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.detection import DetectionRepository
from app.schemas.detection import DetectionResponse

router = APIRouter()


@router.get(
    "",
    response_model=list[DetectionResponse],
)
def get_detections(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[DetectionResponse]:
    return DetectionRepository.get_all(
        db=db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{detection_id}",
    response_model=DetectionResponse,
)
def get_detection(
    detection_id: int,
    db: Session = Depends(get_db),
) -> DetectionResponse:
    detection = DetectionRepository.get_by_id(
        db=db,
        detection_id=detection_id,
    )

    if detection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Detection not found",
        )

    return detection
