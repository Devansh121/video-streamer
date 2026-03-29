from pathlib import Path

import aioboto3
from botocore.exceptions import ClientError

from app.core.config import settings


def get_session() -> aioboto3.Session:
    return aioboto3.Session(
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region,
    )


async def ensure_bucket_exists() -> None:
    session = get_session()
    async with session.client("s3", endpoint_url=settings.s3_endpoint_url) as s3:
        try:
            await s3.head_bucket(Bucket=settings.s3_bucket)
        except ClientError:
            await s3.create_bucket(Bucket=settings.s3_bucket)


async def upload_hls_output(video_id: str, output_dir: Path) -> None:
    session = get_session()
    async with session.client("s3", endpoint_url=settings.s3_endpoint_url) as s3:
        for file_path in output_dir.rglob("*"):
            if file_path.is_file():
                key = f"videos/{video_id}/{file_path.name}"
                content_type = (
                    "application/x-mpegURL"
                    if file_path.suffix == ".m3u8"
                    else "video/MP2T"
                )
                cache_control = (
                    "no-cache"
                    if file_path.suffix == ".m3u8"
                    else "public, max-age=31536000, immutable"
                )
                await s3.upload_file(
                    str(file_path),
                    settings.s3_bucket,
                    key,
                    ExtraArgs={
                        "ContentType": content_type,
                        "CacheControl": cache_control,
                    },
                )
