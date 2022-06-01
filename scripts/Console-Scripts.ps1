. $PSScriptRoot\Invoke-Fabric.ps1

Set-Item function:global:Update-DevEnvironment {
    param([switch]$Verbose)
    . $PSScriptRoot\Update.ps1 -Verbose:$Verbose
} -Force

Set-Item function:global:Upgrade-Requirements {
    Push-Location $PSScriptRoot\..
    & pip-compile -o .\win64-py310-requirements.txt .\requirements.in
    $requirements = Get-Content .\win64-py310-requirements.txt
    $requirements = $requirements -replace 'file:///.*Plush/python', './python'
    Set-Content -Path .\win64-py310-requirements.txt -Value $requirements
    Pop-Location
    Write-Host 'win64-py310-requirements.txt updated.'
    Write-Host 'Run pip-sync win64-py310-requirements.txt to update your environment.'
}
