# Launch a console for the project.
param(
    [switch]$Quick,
    [switch]$Verbose
)

$project_root = Split-Path $PSScriptRoot
. $PSScriptRoot\Write-Status.ps1

Write-Status "Plush console"
# Set a global variable to indicate we want to set and update some useful console functions
$Global:plush_functions = $true

$venv = Join-Path $project_root "venv\scripts\Activate.ps1"
if (Test-Path $venv) {
    if (-Not($Quick)) {
        . $PSScriptRoot\Update.ps1 -Verbose:$Verbose
    }
}
else {
    if ($Quick) {
        Write-Warning "No virtual env detected, -Quick will be ignored"
    }
    . $PSScriptRoot\Setup.ps1
}

. $PSScriptRoot\Ensure-Venv.ps1 | Out-Null

Write-Status "Plush ready"
