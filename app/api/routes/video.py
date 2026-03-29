from pathlib import Path

from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import JSONResponse

from app.models.job import JobStatus, TranscodeJob

router = APIRouter(prefix="/videos", tags=["videos"])

HLS_BASE_DIR = Path("/tmp/hls")


@router.post("/upload", status_code=202)
async def upload_video(file: UploadFile, request: Request) -> JSONResponse:
    job = TranscodeJob(
        input_path="",
        output_path="",
    )

    input_path = Path(f"/tmp/{job.job_id}_input.mp4")
    output_path = HLS_BASE_DIR / job.job_id

    contents = await file.read()
    input_path.write_bytes(contents)

    job.input_path = str(input_path)
    job.output_path = str(output_path)

    await request.app.state.redis.enqueue_job("transcode_video", job.model_dump())

    return JSONResponse(
        status_code=202,
        content={"job_id": job.job_id, "status": JobStatus.pending},
    )
