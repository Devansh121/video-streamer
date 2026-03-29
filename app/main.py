from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import stream, video
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # statup: runs before the app starts accepting requests
    yield
    # shutdown: runs after the app stops accepting requests


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, debug=settings.debug)
    app.include_router(video.router)
    app.include_router(stream.router)
    app.router.lifespan_context = lifespan
    return app


app = create_app()
