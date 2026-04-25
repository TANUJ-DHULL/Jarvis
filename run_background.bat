@echo off
:: This batch file launches the double-clap listener in the background.
cd /d "%~dp0"
start /B "" "c:\Jarvis Anti\.conda\python.exe" "c:\Jarvis Anti\clap_launcher.py" > "c:\Jarvis Anti\clap_listener_log.txt" 2>&1
exit
