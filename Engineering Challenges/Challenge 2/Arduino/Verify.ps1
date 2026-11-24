$ErrorActionPreference = 'Stop'

$arduinoCli = Join-Path $env:LOCALAPPDATA 'Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe'
$arduinoConfig = Join-Path $env:USERPROFILE '.arduinoIDE\arduino-cli.yaml'
$sketchPath = Join-Path $PSScriptRoot 'Heating_Thermistor_Test'
$buildPath = Join-Path $PSScriptRoot '.build\Heating_Thermistor_Test'

if (-not (Test-Path -LiteralPath $arduinoCli)) {
    throw 'The Arduino IDE bundled CLI was not found in the per-user installation.'
}

& $arduinoCli compile --config-file $arduinoConfig --fqbn 'esp32:esp32:nano_nora:PinNumbers=default,USBMode=default' --warnings more --build-path $buildPath $sketchPath
if ($LASTEXITCODE -ne 0) {
    throw "Arduino compilation failed (exit code $LASTEXITCODE)."
}
