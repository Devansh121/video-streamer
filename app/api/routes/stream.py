from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(prefix="/stream", tags=["stream"])

HLS_BASE_DIR = Path("/tmp/hls")


@router.get("/{video_id}/playlist.m3u8")
async def get_playlist(video_id: str) -> FileResponse:
    playlist_path = HLS_BASE_DIR / video_id / "playlist.m3u8"
    if not playlist_path.exists():
        raise HTTPException(status_code=404, detail="Playlist not found")
    return FileResponse(playlist_path, media_type="application/x-mpegURL")


@router.get("/{video_id}/{segment}")
async def get_segment(video_id: str, segment: str) -> FileResponse:
    segment_path = HLS_BASE_DIR / video_id / segment
    if not segment_path.exists():
        raise HTTPException(status_code=404, detail="Segment not found")
    return FileResponse(segment_path, media_type="video/MP2T")
