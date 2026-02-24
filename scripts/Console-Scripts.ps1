. $PSScriptRoot\Invoke-Fabric.ps1

Set-Item function:global:Build-Plush {
    Push-Location $PSScriptRoot\..\python
    uv build
    Pop-Location
}

Set-Item function:global:Update-DevEnvironment {
    param([switch]$Verbose)
    . $PSScriptRoot\Update.ps1 -Verbose:$Verbose
} -Force

Set-Item function:global:Upgrade-Requirements {
    Push-Location $PSScriptRoot\..
    & uv lock --upgrade
    Pop-Location
    Write-Host 'uv.lock updated.'
    Write-Host 'Run uv sync to update your environment.'
}
