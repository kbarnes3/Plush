# Resolve all dependencies that the project requires to run.
param(
    [switch]$Verbose
)

. $PSScriptRoot\Write-Status.ps1

if ($Verbose) {
    $quiet = ""
}
else {
    $quiet = "--quiet"
}

$project_root = Split-Path $PSScriptRoot
$already_activated = . $PSScriptRoot\Ensure-Venv.ps1

Push-Location $project_root

Write-Status "Updating pip"
& python -m pip install --upgrade pip $quiet
Write-Status "Updating requirements"
& pip install -r (Join-Path $project_root "requirements.txt") $quiet
Write-Status "Updating upgradable requirements"
& pip install --upgrade -r (Join-Path $project_root "upgrade-requirements.txt") $quiet

if ($Global:plush_functions) {
    # Define or update the console scripts if we want them
    . $PSScriptRoot\Console-Scripts.ps1
}

Pop-Location

if (-Not $already_activated) {
    deactivate
}
