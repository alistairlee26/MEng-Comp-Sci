@echo off
setlocal
"%LOCALAPPDATA%\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe" compile --config-file "%USERPROFILE%\.arduinoIDE\arduino-cli.yaml" --fqbn "esp32:esp32:nano_nora:PinNumbers=default,USBMode=default" --warnings more --build-path "%~dp0.build\Heating_Thermistor_Test" "%~dp0Heating_Thermistor_Test"
exit /b %ERRORLEVEL%
