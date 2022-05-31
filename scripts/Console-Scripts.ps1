. $PSScriptRoot\Invoke-Fabric.ps1

Set-Item function:global:Update-DevEnvironment {
    param([switch]$Verbose)
    . $PSScriptRoot\Update.ps1 -Verbose:$Verbose
} -Force

Set-Item function:global:Upgrade-Requirements {
    Push-Location $PSScriptRoot\..
    & pip-compile --upgrade --extra test --extra publish -o win64-py310-requirements.txt .\python\setup.py
    Pop-Location
    Write-Host 'win64-py310-requirements.txt updated.'
    Write-Host 'Run pip-sync win64-py310-requirements.txt to update your environment.'
}
