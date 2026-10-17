# Usage: .\Start-MotionCopy.ps1 prepare D:\Video\ep05\project.json
$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
  throw "ffmpeg not found on PATH. Install it first: winget install Gyan.FFmpeg"
}

if (-not (Test-Path ".venv")) {
  python -m venv .venv
}

.\.venv\Scripts\python.exe -m pip install -q -r requirements.txt
.\.venv\Scripts\python.exe .\motion_copy.py @args
exit $LASTEXITCODE
