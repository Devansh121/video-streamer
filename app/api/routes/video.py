from pathlib import Path

from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse

from app.models.job import TranscodeJob
from app.services.hls import run_hls_segmentation

router = APIRouter(prefix="/videos", tags=["videos"])

HLS_BASE_DIR = Path("/tmp/hls")


@router.post("/upload", status_code=202)
async def upload_video(file: UploadFile) -> JSONResponse:
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
    job = run_hls_segmentation(job)

    input_path.unlink(missing_ok=True)

    return JSONResponse(
        status_code=202,
        content={"job_id": job.job_id, "status": job.status},
    )
