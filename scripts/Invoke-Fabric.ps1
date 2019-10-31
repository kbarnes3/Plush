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

Set-Item function:global:Fabric-SetupUser {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Hosts,
        [switch]$PromptForLoginPassword,
        [switch]$PromptForSudoPassword,
        [Parameter(Mandatory=$true)]
        [string]$User,
        [string]$PublicKeyFile,
        [switch]$NoSudoPasswd
    )
    $setupUserArgs = @("setup-user")
    $setupUserArgs += $User
    if ($PublicKeyFile) {
        $setupUserArgs += $PublicKeyFile
    }
    if ($NoSudoPasswd) {
        $setupUserArgs += "--no-sudo-passwd"
    }

    Invoke-Fabric $Hosts -PromptForLoginPassword:$PromptForLoginPassword -PromptForSudoPassword:$PromptForSudoPassword $setupUserArgs


} -Force
