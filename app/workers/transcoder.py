from app.models.job import TranscodeJob
from app.services.hls import run_hls_segmentation


async def transcode_video(
    ctx: dict[str, object],
    job_dict: dict[str, object],
) -> dict[str, object]:
    job = TranscodeJob.model_validate(job_dict)
    job = await run_hls_segmentation(job)
    return {"job_id": job.job_id, "status": job.status}
