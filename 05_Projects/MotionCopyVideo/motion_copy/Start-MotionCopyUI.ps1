# Opens the Motion Copy Video interface in your browser (http://127.0.0.1:8765).
# Projects are stored in %USERPROFILE%\Videos\MotionCopy unless -ProjectsDir is given.
param([string]$ProjectsDir = "$env:USERPROFILE\Videos\MotionCopy")
$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
  throw "ffmpeg not found on PATH. Install it first: winget install Gyan.FFmpeg"
}

if (-not (Test-Path ".venv")) {
  python -m venv .venv
}

.\.venv\Scripts\python.exe -m pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) {
  throw "Installing Python packages failed (see the messages above). Python 3.10 or newer is required."
}
.\.venv\Scripts\python.exe .\app.py --projects-dir $ProjectsDir
