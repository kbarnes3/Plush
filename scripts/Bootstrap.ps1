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

Write-Status "Updating requirements"
& uv sync $quiet

if ($Global:console_functions) {
    # Define or update the console scripts if we want them
    . $PSScriptRoot\Console-Scripts.ps1
}

Pop-Location
