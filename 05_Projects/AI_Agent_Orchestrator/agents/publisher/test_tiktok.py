"""Tests against TikTok's real documented Content Posting API contract —
mocks httpx since no real TikTok developer app/token exists in this
environment."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest

from agents.publisher.tiktok import TikTokError, get_publish_status, post_video


def _fake_response(status_code=200, json_data=None, text=""):
    response = MagicMock()
    response.status_code = status_code
    response.text = text
    response.json.return_value = json_data or {}
    return response


def test_post_video_sends_documented_init_and_upload_requests(tmp_path):
    video_path = tmp_path / "video.mp4"
    video_path.write_bytes(b"abc")

    init_response = _fake_response(
        200, {"error": {"code": "ok"}, "data": {"publish_id": "pub1", "upload_url": "https://upload.example/x"}}
    )
    upload_response = _fake_response(200)

    with patch("httpx.post", return_value=init_response) as mock_post, patch(
        "httpx.put", return_value=upload_response
    ) as mock_put:
        publish_id = post_video("token1", str(video_path), title="My TikTok", privacy_level="SELF_ONLY")

    assert publish_id == "pub1"

    args, kwargs = mock_post.call_args
    assert args[0].endswith("/post/publish/video/init/")
    assert kwargs["json"]["post_info"] == {"title": "My TikTok", "privacy_level": "SELF_ONLY"}
    assert kwargs["json"]["source_info"]["video_size"] == 3
    assert kwargs["headers"]["Authorization"] == "Bearer token1"

    put_args, put_kwargs = mock_put.call_args
    assert put_args[0] == "https://upload.example/x"
    assert put_kwargs["headers"]["Content-Range"] == "bytes 0-2/3"


def test_post_video_raises_on_api_error_code(tmp_path):
    video_path = tmp_path / "video.mp4"
    video_path.write_bytes(b"abc")
    response = _fake_response(200, {"error": {"code": "invalid_param", "message": "bad title"}})

    with patch("httpx.post", return_value=response):
        with pytest.raises(TikTokError, match="bad title"):
            post_video("token1", str(video_path), title="x")


def test_post_video_raises_when_file_missing():
    with pytest.raises(TikTokError, match="not found"):
        post_video("token1", "/tmp/does-not-exist-xyz-tiktok-test.mp4", title="x")


def test_get_publish_status_parses_response():
    response = _fake_response(200, {"error": {"code": "ok"}, "data": {"status": "PUBLISH_COMPLETE"}})
    with patch("httpx.post", return_value=response):
        result = get_publish_status("token1", "pub1")
    assert result["status"] == "PUBLISH_COMPLETE"
