@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" -Interface terminal -Mode auto %*
exit /b %errorlevel%
