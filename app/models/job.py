import uuid
from enum import StrEnum

from pydantic import BaseModel, Field


class JobStatus(StrEnum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class TranscodeJob(BaseModel):
    job_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    input_path: str
    output_path: str
    status: JobStatus = JobStatus.pending
    error: str | None = None
