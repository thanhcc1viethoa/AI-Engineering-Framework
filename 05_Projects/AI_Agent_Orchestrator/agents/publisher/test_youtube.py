"""Tests against YouTube's real documented resumable-upload contract — mocks
httpx since no real Google Cloud project/OAuth token exists in this
environment. Run with the backend venv from the project root:
    PYTHONPATH=. backend/.venv/bin/python -m pytest agents/publisher/test_youtube.py -v
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest

from agents.publisher.youtube import YouTubeError, get_video_status, upload_video


def _fake_response(status_code=200, json_data=None, text="", headers=None):
    response = MagicMock()
    response.status_code = status_code
    response.text = text
    response.json.return_value = json_data or {}
    response.headers = headers or {}
    return response


def _write_token_file(tmp_path) -> str:
    token_path = tmp_path / "youtube_token.json"
    token_path.write_text(json.dumps({"refresh_token": "r1", "client_id": "c1", "client_secret": "s1"}))
    return str(token_path)


def test_upload_video_sends_documented_requests(tmp_path):
    token_path = _write_token_file(tmp_path)
    video_path = tmp_path / "video.mp4"
    video_path.write_bytes(b"fake video bytes")

    token_response = _fake_response(200, {"access_token": "at1"})
    init_response = _fake_response(200, headers={"Location": "https://upload.example/session1"})
    upload_response = _fake_response(200, {"id": "vid123"})

    with patch("httpx.post", side_effect=[token_response, init_response]) as mock_post, patch(
        "httpx.put", return_value=upload_response
    ) as mock_put:
        result = upload_video(token_path, str(video_path), title="My video", description="desc")

    assert result == {"video_id": "vid123", "url": "https://youtu.be/vid123"}

    token_args, token_kwargs = mock_post.call_args_list[0]
    assert token_args[0] == "https://oauth2.googleapis.com/token"
    assert token_kwargs["data"]["refresh_token"] == "r1"

    init_args, init_kwargs = mock_post.call_args_list[1]
    assert init_args[0] == "https://www.googleapis.com/upload/youtube/v3/videos"
    assert init_kwargs["params"] == {"uploadType": "resumable", "part": "snippet,status"}
    assert init_kwargs["json"]["snippet"]["title"] == "My video"
    assert init_kwargs["headers"]["Authorization"] == "Bearer at1"

    put_args, put_kwargs = mock_put.call_args
    assert put_args[0] == "https://upload.example/session1"
    assert put_kwargs["content"] == b"fake video bytes"


def test_upload_video_raises_when_token_file_missing(tmp_path):
    video_path = tmp_path / "video.mp4"
    video_path.write_bytes(b"abc")
    with pytest.raises(YouTubeError, match="No YouTube OAuth token file"):
        upload_video(str(tmp_path / "missing.json"), str(video_path), title="t")


def test_upload_video_raises_when_video_file_missing(tmp_path):
    token_path = _write_token_file(tmp_path)
    with pytest.raises(YouTubeError, match="Video file not found"):
        upload_video(token_path, str(tmp_path / "missing.mp4"), title="t")


def test_get_video_status_parses_response(tmp_path):
    token_path = _write_token_file(tmp_path)
    token_response = _fake_response(200, {"access_token": "at1"})
    status_response = _fake_response(200, {"items": [{"id": "vid123", "status": {"uploadStatus": "uploaded"}}]})

    with patch("httpx.post", return_value=token_response), patch("httpx.get", return_value=status_response) as mock_get:
        result = get_video_status(token_path, "vid123")

    assert result["id"] == "vid123"
    _, kwargs = mock_get.call_args
    assert kwargs["params"]["id"] == "vid123"


def test_get_video_status_raises_when_not_found(tmp_path):
    token_path = _write_token_file(tmp_path)
    token_response = _fake_response(200, {"access_token": "at1"})
    status_response = _fake_response(200, {"items": []})

    with patch("httpx.post", return_value=token_response), patch("httpx.get", return_value=status_response):
        with pytest.raises(YouTubeError, match="not found"):
            get_video_status(token_path, "missing")
