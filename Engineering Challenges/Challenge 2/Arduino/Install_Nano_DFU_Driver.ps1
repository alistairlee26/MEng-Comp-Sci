$ErrorActionPreference = 'Stop'
$driverDirectory = Join-Path $PSScriptRoot '.tools\nano-dfu-driver\esp32-v2.0.17-arduino.5\drivers'
$catalog = Join-Path $driverDirectory 'nanoesp32.cat'
$driverInf = Join-Path $driverDirectory 'nanoesp32.inf'
$logPath = Join-Path $PSScriptRoot 'Nano_DFU_Driver_Install.log'
$exitPath = Join-Path $PSScriptRoot 'Nano_DFU_Driver_Install.exitcode'

try {
    $signature = Get-AuthenticodeSignature -LiteralPath $catalog
    if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notmatch 'CN=Arduino SA') {
        throw 'The Arduino driver catalog signature could not be verified.'
    }
    & "$env:WINDIR\System32\pnputil.exe" /add-driver $driverInf /install 2>&1 |
        Tee-Object -FilePath $logPath
    $installExit = $LASTEXITCODE
    Set-Content -LiteralPath $exitPath -Value $installExit
    exit $installExit
} catch {
    $_ | Out-String | Set-Content -LiteralPath $logPath
    Set-Content -LiteralPath $exitPath -Value 1
    exit 1
}
