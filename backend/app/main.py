from fastapi import FastAPI

from app.api.v1.events import router as events_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.api.v1.ingestion import router as ingestion_router

configure_logging()

app = FastAPI(
    title=settings.app_name,
    description="A modern Security Information and Event Management platform built with FastAPI, React, and PostgreSQL.",
    version=settings.app_version,
)

app.include_router(
    events_router,
    prefix="/api/v1",
)
app.include_router(
    ingestion_router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {"message": "SIEM Dashboard API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
