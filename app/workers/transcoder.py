from pathlib import Path

from app.models.job import TranscodeJob
from app.services.hls import run_hls_segmentation
from app.storage.s3 import upload_hls_output


async def transcode_video(
    ctx: dict[str, object],
    job_dict: dict[str, object],
) -> dict[str, object]:
    job = TranscodeJob.model_validate(job_dict)
    job = await run_hls_segmentation(job)

    if job.status == "completed":
        await upload_hls_output(job.job_id, Path(job.output_path))

    return {"job_id": job.job_id, "status": job.status}
