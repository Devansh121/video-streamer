import subprocess
from pathlib import Path

from app.models.job import JobStatus, TranscodeJob


def run_hls_segmentation(job: TranscodeJob) -> TranscodeJob:
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
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        job.status = JobStatus.failed
        job.error = result.stderr
    else:
        job.status = JobStatus.completed

    return job
