import subprocess
from pathlib import Path

from app.models.job import JobStatus, TranscodeJob


def run_transcode(job: TranscodeJob) -> TranscodeJob:
    Path(job.output_path).parent.mkdir(parents=True, exist_ok=True)

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
        "-y",
        job.output_path,
    ]

    job.status = JobStatus.processing
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        job.status = JobStatus.failed
        job.error = result.stderr
    else:
        job.status = JobStatus.completed

    return job
