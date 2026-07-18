from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.event import EventResponse
from app.schemas.ingestion import FileIngestionResponse, RawLogRequest
from app.services.ingestion import IngestionService

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])

ingestion_service = IngestionService()


@router.post(
    "/log",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
def ingest_log(
    request: RawLogRequest,
    db: Session = Depends(get_db),
) -> EventResponse:
    try:
        return ingestion_service.ingest_log(
            db=db,
            raw_log=request.raw_log,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc


@router.post(
    "/file",
    response_model=FileIngestionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def ingest_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> FileIngestionResponse:
    content = await file.read()

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be UTF-8 encoded",
        ) from exc

    raw_logs = text.splitlines()

    ingested_events, failed_logs = ingestion_service.ingest_logs(
        db=db,
        raw_logs=raw_logs,
    )

    processed = len([raw_log for raw_log in raw_logs if raw_log.strip()])

    return FileIngestionResponse(
        filename=file.filename or "unknown",
        processed=processed,
        ingested=len(ingested_events),
        failed=len(failed_logs),
        failed_logs=failed_logs,
    )
