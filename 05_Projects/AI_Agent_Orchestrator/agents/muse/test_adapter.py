"""Tests against Muse4AI's REAL documented contract (not a guess) — see the
module docstring in adapter.py for where that contract came from. These mock
httpx itself, since no live Muse4AI instance exists in this environment
(it requires a Windows PC with the app installed and a signed-in Muse
account); they verify this adapter's request/response handling is correct
for the shapes Muse4AI's own OpenAPI document declares.

Run with the backend venv, from the project root:
    PYTHONPATH=. backend/.venv/bin/python -m pytest agents/muse/test_adapter.py -v
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest

from agents.muse.adapter import Muse4AIError, download_output, get_job, submit_video


def _fake_response(status_code=200, json_data=None, text=""):
    response = MagicMock()
    response.status_code = status_code
    response.text = text
    response.json.return_value = json_data or {}
    return response


def test_submit_video_sends_the_documented_request_shape():
    job = {"id": "job_abc123", "kind": "video", "status": "queued", "outputs": []}
    with patch("httpx.post", return_value=_fake_response(202, {"jobs": [job]})) as mock_post:
        result = submit_video("http://127.0.0.1:47821/v1", "msk_test", "a cat on a sofa", repeat=2, account="auto")

    assert result == job
    args, kwargs = mock_post.call_args
    assert args[0] == "http://127.0.0.1:47821/v1/jobs"
    assert kwargs["json"] == {"kind": "video", "prompt": "a cat on a sofa", "repeat": 2, "account": "auto"}
    assert kwargs["headers"]["Authorization"] == "Bearer msk_test"


def test_submit_video_raises_without_config():
    with pytest.raises(Muse4AIError, match="not configured"):
        submit_video("", "", "a cat")


def test_submit_video_raises_on_rfc9457_problem_response():
    problem = {"type": "about:blank", "title": "Unauthorized", "status": 401, "detail": "Invalid API key", "code": "invalid_api_key", "request_id": "r1"}
    with patch("httpx.post", return_value=_fake_response(401, problem)):
        with pytest.raises(Muse4AIError, match="Invalid API key"):
            submit_video("http://127.0.0.1:47821/v1", "msk_bad", "a cat")


def test_get_job_passes_wait_query_param():
    job = {"id": "job_abc123", "status": "succeeded", "outputs": []}
    with patch("httpx.get", return_value=_fake_response(200, job)) as mock_get:
        result = get_job("http://127.0.0.1:47821/v1", "msk_test", "job_abc123", wait_seconds=20)

    assert result == job
    args, kwargs = mock_get.call_args
    assert args[0] == "http://127.0.0.1:47821/v1/jobs/job_abc123"
    assert kwargs["params"] == {"wait": 20}


def test_download_output_writes_file_with_mime_extension(tmp_path):
    output = {"asset_id": "asset_xyz", "mime": "video/mp4", "download_url": "https://signed.example/x"}

    fake_stream_response = MagicMock()
    fake_stream_response.status_code = 200
    fake_stream_response.text = ""
    fake_stream_response.iter_bytes.return_value = [b"fake", b"-mp4-", b"bytes"]

    class _FakeStreamCM:
        def __enter__(self_inner):
            return fake_stream_response

        def __exit__(self_inner, *exc):
            return False

    with patch("httpx.stream", return_value=_FakeStreamCM()):
        path = download_output(output, str(tmp_path))

    assert path == str(tmp_path / "asset_xyz.mp4")
    assert Path(path).read_bytes() == b"fake-mp4-bytes"


def test_download_output_raises_without_download_url():
    with pytest.raises(Muse4AIError, match="no download_url"):
        download_output({"asset_id": "asset_xyz", "mime": "video/mp4", "download_url": None}, "/tmp")
