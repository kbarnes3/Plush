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

$venv = Join-Path $project_root "venv"
if (-Not (Test-Path $venv)) {
    Write-Status "Creating venv in $venv"
    . $PSScriptRoot\Invoke-NonVenvPython.ps1 @('-m', 'venv', $venv)
}

$already_activated = . $PSScriptRoot\Ensure-Venv.ps1

Write-Status "Updating pip"
& python -m pip install --upgrade pip $quiet
Write-Status "Updating pip-tools"
& python -m pip install --upgrade pip-tools $quiet
Write-Status "Updating requirements"
& pip-sync .\win64-py310-requirements.txt $quiet

if ($Global:console_functions) {
    # Define or update the console scripts if we want them
    . $PSScriptRoot\Console-Scripts.ps1
}

Pop-Location

if (-Not $already_activated) {
    deactivate
}
