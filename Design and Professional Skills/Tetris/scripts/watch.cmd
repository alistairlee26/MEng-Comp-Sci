@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" -Interface pygame -Mode auto %*
exit /b %errorlevel%
