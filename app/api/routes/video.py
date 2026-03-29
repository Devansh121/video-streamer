import tempfile
from pathlib import Path

from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse

from app.models.job import TranscodeJob
from app.services.transcoder import run_transcode

router = APIRouter(prefix="/videos", tags=["videos"])


@router.post("/upload", status_code=202)
async def upload_video(file: UploadFile) -> JSONResponse:

    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = Path(temp_dir) / (file.filename or "input.mp4")
        output_path = Path(temp_dir) / "output.mp4"

        contents = await file.read()
        input_path.write_bytes(contents)

        job = TranscodeJob(
            input_path=str(input_path),
            output_path=str(output_path),
        )
        job = run_transcode(job)

    return JSONResponse(
        status_code=202,
        content={"job_id": job.job_id, "status": job.status},
    )
