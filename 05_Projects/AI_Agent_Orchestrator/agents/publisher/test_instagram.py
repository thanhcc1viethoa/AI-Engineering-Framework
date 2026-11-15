"""Tests against Instagram's real documented Graph API content-publishing
contract — mocks httpx since no real Meta app/token exists in this
environment."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest

from agents.publisher.instagram import InstagramError, create_reel_container, get_container_status, publish_container


def _fake_response(status_code=200, json_data=None):
    response = MagicMock()
    response.status_code = status_code
    response.json.return_value = json_data or {}
    response.text = str(json_data)
    return response


def test_create_reel_container_sends_documented_request():
    response = _fake_response(200, {"id": "creation123"})
    with patch("httpx.post", return_value=response) as mock_post:
        creation_id = create_reel_container("token1", "igid1", "https://example.com/video.mp4", caption="hi")

    assert creation_id == "creation123"
    args, kwargs = mock_post.call_args
    assert args[0].endswith("/igid1/media")
    assert kwargs["params"]["media_type"] == "REELS"
    assert kwargs["params"]["video_url"] == "https://example.com/video.mp4"


def test_get_container_status_parses_response():
    response = _fake_response(200, {"status_code": "FINISHED"})
    with patch("httpx.get", return_value=response):
        status = get_container_status("token1", "creation123")
    assert status == "FINISHED"


def test_publish_container_sends_documented_request():
    response = _fake_response(200, {"id": "media123"})
    with patch("httpx.post", return_value=response) as mock_post:
        media_id = publish_container("token1", "igid1", "creation123")

    assert media_id == "media123"
    args, kwargs = mock_post.call_args
    assert args[0].endswith("/igid1/media_publish")
    assert kwargs["params"]["creation_id"] == "creation123"


def test_create_reel_container_raises_on_api_error():
    response = _fake_response(400, {"error": {"message": "Invalid video_url"}})
    with patch("httpx.post", return_value=response):
        with pytest.raises(InstagramError, match="Invalid video_url"):
            create_reel_container("token1", "igid1", "not-a-url")
