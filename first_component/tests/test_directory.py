import base64
import os
import tempfile
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routers.directory import router

@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)

@pytest.fixture
def temp_dir(monkeypatch):
    with tempfile.TemporaryDirectory() as dir:
        monkeypatch.setattr("app.directory.utils.config.BASE_DIR", dir)
        yield dir

def convert_str_to_b64(to_convert: str):
    return base64.b64encode(to_convert.encode()).decode()

class TestDirectoryRouter:
    def test_create(self, client, temp_dir):
        content = "content"
        req = {
            "path": "test.txt",
            "content": convert_str_to_b64(content)
        }

        response = client.post("/directory/create", json=req)
        assert response.status_code == 200

        with open(os.path.join(temp_dir, "test.txt"), "r") as f:
            assert f.read() == content

    def test_update(self, client, temp_dir):
        file_path = os.path.join(temp_dir, "update.txt")

        # Create initial file
        with open(file_path, "w") as f:
            f.write("old content")

        req = {
            "path": "update.txt",
            "content": convert_str_to_b64("new content")
        }

        response = client.post("/directory/update", json=req)
        assert response.status_code == 200

        with open(file_path, "r") as f:
            assert f.read() == "new content"

    def test_delete(self, client, temp_dir):
        file_path = os.path.join(temp_dir, "delete.txt")

        with open(file_path, "w") as f:
            f.write("content")

        req = {"path": "delete.txt"}

        response = client.post("/directory/delete", json=req)
        assert response.status_code == 200
        assert not os.path.exists(file_path)

    def test_list_files(self, client, temp_dir):
        open(os.path.join(temp_dir, "example1.txt"), "w").close()
        open(os.path.join(temp_dir, "example2.log"), "w").close()

        response = client.post("/directory/list")
        assert response.status_code == 200

        files = response.json()["files"]
        assert "example1.txt" in files
        assert "example2.log" in files

    def test_invalid_path_1(self, client, temp_dir):
        req = {
            "path": "/etc/passwd",
            "content": convert_str_to_b64("hacker")
        }

        response = client.post("/directory/create", json=req)
        assert response.status_code == 400

    def test_invalid_path_2(self, client, temp_dir):
        req = {
            "path": temp_dir + "_passwords/client.txt",
            "content": convert_str_to_b64("hacker")
        }

        response = client.post("/directory/create", json=req)
        assert response.status_code == 400