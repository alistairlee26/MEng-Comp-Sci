$ErrorActionPreference = 'Stop'
$arduinoIde = Join-Path $env:LOCALAPPDATA 'Programs\Arduino IDE\Arduino IDE.exe'
$sketchFile = Join-Path $PSScriptRoot 'Heating_Thermistor_Test\Heating_Thermistor_Test.ino'
if (-not (Test-Path -LiteralPath $arduinoIde)) {
    throw 'Arduino IDE was not found in the per-user installation.'
}
Start-Process -FilePath $arduinoIde -ArgumentList ('"' + $sketchFile + '"') -WindowStyle Normal
