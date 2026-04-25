@echo off
cd /d "%~dp0"
if exist "%~dp0.conda\python.exe" (
    start "" /B "%~dp0.conda\python.exe" "%~dp0clap_launcher.py" > "%~dp0clap_listener_log.txt" 2>&1
    exit /b 0
)

where python >nul 2>nul
if %errorlevel%==0 (
    start "" /B python "%~dp0clap_launcher.py" > "%~dp0clap_listener_log.txt" 2>&1
    exit /b 0
)

echo Python not found. Also checked "%~dp0.conda\python.exe".
pause
