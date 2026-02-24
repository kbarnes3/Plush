# Resolve all dependencies that the project requires to run.
param(
    [switch]$Verbose
)

. $PSScriptRoot\Write-Status.ps1

if ($Verbose) {
    $quiet = $null
}
else {
    $quiet = "--quiet"
}

$project_root = Split-Path $PSScriptRoot

Push-Location $project_root

# Ensure uv is installed
if (-Not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Status "Installing uv via winget"
    winget install --id=astral-sh.uv -e
    Write-Warning "uv was just installed. You may need to restart your terminal for it to take effect."
}

Write-Status "Updating requirements"
& uv sync $quiet

if ($Global:console_functions) {
    # Define or update the console scripts if we want them
    . $PSScriptRoot\Console-Scripts.ps1
}

Pop-Location
