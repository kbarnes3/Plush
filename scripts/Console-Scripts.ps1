. $PSScriptRoot\Invoke-Fabric.ps1

$project_root = Split-Path $PSScriptRoot

Set-Item function:global:Update-DevEnvironment {
    param([switch]$Verbose)
    . $PSScriptRoot\Update.ps1 -Verbose:$Verbose
} -Force

Set-Item function:global:Invoke-Flake8 {
    Push-Location $project_root
    & flake8.exe .\fabfile.py
    & flake8.exe .\python
    Pop-Location
}
