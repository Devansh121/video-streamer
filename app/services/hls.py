import asyncio
from pathlib import Path

from app.models.job import JobStatus, TranscodeJob


async def run_hls_segmentation(job: TranscodeJob) -> TranscodeJob:
    output_dir = Path(job.output_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    playlist_path = output_dir / "playlist.m3u8"

    cmd = [
        "ffmpeg",
        "-i",
        job.input_path,
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-preset",
        "fast",
        "-hls_time",
        "6",
        "-hls_playlist_type",
        "vod",
        "-hls_segment_filename",
        str(output_dir / "segment_%03d.ts"),
        "-y",
        str(playlist_path),
    ]

    job.status = JobStatus.processing
    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    _, stderr = await process.communicate()

    if process.returncode != 0:
        job.status = JobStatus.failed
        job.error = stderr.decode()
    else:
        job.status = JobStatus.completed

    return job
