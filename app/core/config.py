from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "video-streamer"
    debug: bool = False
    upload_dir: str = "/tmp/uploads"
    redis_url: str = "redis://localhost:6379"
    s3_bucket: str = "video-streamer"
    s3_endpoint_url: str = "http://localhost:4566"
    aws_access_key_id: str = "test"
    aws_secret_access_key: str = "test"
    aws_region: str = "us-east-1"


settings = Settings()
