@echo off
cd /d "%~dp0"
if exist "%~dp0.conda\python.exe" (
    "%~dp0.conda\python.exe" "%~dp0clap_launcher.py"
    pause
    exit /b 0
)

python "%~dp0clap_launcher.py"
pause
