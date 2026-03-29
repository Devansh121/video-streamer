from arq.connections import RedisSettings

from app.core.config import settings
from app.workers.transcoder import transcode_video


class WorkerSettings:
    functions = [transcode_video]
    redis_settings = RedisSettings.from_dsn(settings.redis_url)
