from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    mock_redis = MagicMock()
    mock_redis.enqueue_job = AsyncMock()
    app.state.redis = mock_redis
    return TestClient(app)


def test_upload_returns_202(client: TestClient) -> None:
    response = client.post(
        "/videos/upload",
        files={"file": ("test.mp4", b"fake video content", "video/mp4")},
    )
    assert response.status_code == 202
    assert "job_id" in response.json()
    assert response.json()["status"] == "pending"
