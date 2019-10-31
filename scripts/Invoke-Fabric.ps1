# Runs Fabric from a consistent context
# Any arguments passed into this function are passed to fab
Set-Item function:global:Invoke-Fabric {
    param(
        [Parameter(Position=0, Mandatory=$true)]
        [string]$Hosts,
        [switch]$PromptForLoginPassword,
        [switch]$PromptForSudoPassword,
        [Parameter(Position=1, ValueFromRemainingArguments)]
        [string[]]$FabricTask
    )

    $project_root = Split-Path $PSScriptRoot
    $already_activated = . $PSScriptRoot\Ensure-Venv.ps1

    $fabric = Join-Path $project_root "venv\Scripts\fab.exe"
    $fabricArgs = @("--hosts", $Hosts)
    if ($PromptForLoginPassword) {
        $fabricArgs += "--prompt-for-login-password"
    }
    if ($PromptForSudoPassword) {
        $fabricArgs += "--prompt-for-sudo-password "
    }
    
    $fabricArgs += $FabricTask

    Push-Location $project_root
    Start-Process $fabric -ArgumentList $fabricArgs -NoNewWindow -Wait
    Pop-Location

    if (-Not $already_activated) {
        deactivate
    }
} -Force
