from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_returns_202() -> None:
    response = client.post(
        "/videos/upload",
        files={"file": ("test.mp4", b"fake video content", "video/mp4")},
    )
    assert response.status_code == 202
    assert response.json()["filename"] == "test.mp4"
