from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/videos", tags=["videos"])


@router.post("/upload", status_code=202)
async def upload_video(file: UploadFile) -> JSONResponse:
    return JSONResponse(
        status_code=202,
        content={"message": "Upload accepted", "filename": file.filename},
    )
