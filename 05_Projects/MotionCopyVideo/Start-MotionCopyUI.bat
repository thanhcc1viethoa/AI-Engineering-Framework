@echo off
rem Double-click to open the Motion Copy Video interface.
rem Messages are ASCII-only on purpose so they display correctly in any cmd code page.
setlocal
cd /d "%~dp0motion_copy"

where python >nul 2>nul
if errorlevel 1 (
  echo [!] Chua co Python tren may.
  choice /m "Cai Python 3.12 tu dong bang winget"
  if errorlevel 2 goto :end
  winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
  echo.
  echo Da cai xong Python. Hay DONG cua so nay roi BAM DUP lai file Start-MotionCopyUI.bat.
  goto :end
)

where ffmpeg >nul 2>nul
if errorlevel 1 (
  echo [!] Chua co ffmpeg tren may.
  choice /m "Cai ffmpeg tu dong bang winget"
  if errorlevel 2 goto :end
  winget install -e --id Gyan.FFmpeg --accept-package-agreements --accept-source-agreements
  echo.
  echo Da cai xong ffmpeg. Hay DONG cua so nay roi BAM DUP lai file Start-MotionCopyUI.bat.
  goto :end
)

set "PROJECTS=%USERPROFILE%\Videos\MotionCopy"
if exist D:\ set "PROJECTS=D:\Video\MotionCopy"

echo Lan dau se mat 1-2 phut de cai thu vien. Trinh duyet se tu mo.
echo Du an duoc luu tai: %PROJECTS%
echo GIU cua so nay mo trong luc dung tool. Dong cua so = tat tool.
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0motion_copy\Start-MotionCopyUI.ps1" -ProjectsDir "%PROJECTS%"

:end
echo.
pause
