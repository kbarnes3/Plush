. $PSScriptRoot\Invoke-Fabric.ps1

Set-Item function:global:Update-DevEnvironment {
    param([switch]$Verbose)
    . $PSScriptRoot\Update.ps1 -Verbose:$Verbose
} -Force
