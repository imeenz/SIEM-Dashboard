from pydantic import BaseModel


class RawLogRequest(BaseModel):
    raw_log: str


class FileIngestionResponse(BaseModel):
    filename: str
    processed: int
    ingested: int
    failed: int
    failed_logs: list[str]
