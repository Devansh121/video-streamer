from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "video-streamer"
    debug: bool = False
    upload_dir: str = "/tmp/uploads"
    redis_url: str = "redis://localhost:6379"


settings = Settings()
