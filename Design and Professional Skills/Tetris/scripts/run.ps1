[CmdletBinding()]
param(
    [ValidateSet('pygame', 'tkinter', 'terminal')]
    [string] $Interface = 'pygame',

    [ValidateSet('manual', 'auto')]
    [string] $Mode = 'auto',

    [switch] $Help,

    [string] $Seed = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $projectRoot '.venv\Scripts\python.exe'
$entryPoint = Join-Path $projectRoot 'scripts\run_local.py'

if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
    throw 'Project Python environment missing. Follow the Local setup instructions in README.md.'
}
if (-not (Test-Path -LiteralPath $entryPoint -PathType Leaf)) {
    throw "Game interface missing: $entryPoint"
}

$gameArguments = @('--interface', $Interface)
if ($Mode -eq 'manual') {
    $gameArguments += '--manual'
}
if ($Seed -ne '') {
    $gameArguments += @('--seed', $Seed)
}
if ($Help) {
    $gameArguments += '--help'
}

# the pygame interface loads its font relative to the current directory
Push-Location -LiteralPath $projectRoot
try {
    & $python $entryPoint @gameArguments
    $gameExitCode = $LASTEXITCODE
}
finally {
    Pop-Location
}
exit $gameExitCode
