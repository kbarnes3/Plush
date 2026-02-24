# This script updates the project to run for its current checkout.
param(
    [switch]$Verbose
)

. $PSScriptRoot\Write-Status.ps1

. $PSScriptRoot\Bootstrap.ps1 -Verbose:$Verbose
