# Runs Fabric from a consistent context
# Any arguments passed into this function are passed to fab
Set-Item function:global:Invoke-Fabric {
    [CmdletBinding(DefaultParameterSetName="none")]
    param(
        [Parameter(Position=0, Mandatory=$true, ParameterSetName="run")]
        [string]$Hosts,
        [Parameter(ParameterSetName="run")]
        [switch]$PromptForPassphrase,
        [Parameter(ParameterSetName="run")]
        [switch]$PromptForLoginPassword,
        [Parameter(ParameterSetName="run")]
        [switch]$PromptForSudoPassword,
        [Parameter(Position=1, ValueFromRemainingArguments, ParameterSetName="run")]
        [string[]]$FabricTask,
        [Parameter(ParameterSetName="list")]
        [switch]$ListTasks
    )
    $listFunctions = $False
    $project_root = Split-Path $PSScriptRoot
    $already_activated = . $PSScriptRoot\Ensure-Venv.ps1

    $fabric = Join-Path $project_root "venv\Scripts\fab.exe"
    if ($ListTasks -or -not $Hosts) {
        $listFunctions = $True
        $fabricArgs = "--list"
    } else {
        $fabricArgs = @("--hosts", $Hosts)
        if ($PromptForPassphrase) {
            $fabricArgs += "--prompt-for-passphrase"
        }
        if ($PromptForLoginPassword) {
            $fabricArgs += "--prompt-for-login-password"
        }
        if ($PromptForSudoPassword) {
            $fabricArgs += "--prompt-for-sudo-password"
        }
        $fabricArgs += $FabricTask
    }

    Push-Location $project_root
    Start-Process $fabric -ArgumentList $fabricArgs -NoNewWindow -Wait
    Pop-Location

    if ($listFunctions) {
        Write-Host "Fabric tasks are also available as PowerShell functions:`n"
        $fabricFunctions = Get-Item function:Fabric-* | Sort-Object -Property Name
        $fabricFunctions | ForEach-Object { Write-Host "  $($_.Name)" }
        Write-Host ""
    }

    if (-Not $already_activated) {
        deactivate
    }
} -Force

Set-Item function:global:Fabric-SetupUser {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Hosts,
        [switch]$PromptForPassphrase,
        [switch]$PromptForLoginPassword,
        [switch]$PromptForSudoPassword,
        [Parameter(Mandatory=$true)]
        [string]$User,
        [string]$PublicKeyFile,
        [switch]$NoSudoPasswd
    )
    $setupUserArgs = @("setup-user")
    $setupUserArgs += "--user"
    $setupUserArgs += $User
    if ($PublicKeyFile) {
        $setupUserArgs += "--public-key-file"
        $setupUserArgs += $PublicKeyFile
    }
    if ($NoSudoPasswd) {
        $setupUserArgs += "--no-sudo-passwd"
    }

    Invoke-Fabric $Hosts -PromptForPassphrase:$PromptForPassphrase -PromptForLoginPassword:$PromptForLoginPassword -PromptForSudoPassword:$PromptForSudoPassword $setupUserArgs
} -Force

Set-Item function:global:Fabric-AddAuthorizedKey {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Hosts,
        [switch]$PromptForPassphrase,
        [switch]$PromptForLoginPassword,
        [switch]$PromptForSudoPassword,
        [Parameter(Mandatory=$true)]
        [string]$User,
        [Parameter(Mandatory=$true)]
        [string]$PublicKeyFile
    )
    $addAuthorizedKeyArgs = @("add-authorized-key")
    $addAuthorizedKeyArgs += "--user"
    $addAuthorizedKeyArgs += $User
    $addAuthorizedKeyArgs += "--public-key-file"
    $addAuthorizedKeyArgs += $PublicKeyFile

    Invoke-Fabric $Hosts -PromptForPassphrase:$PromptForPassphrase -PromptForLoginPassword:$PromptForLoginPassword -PromptForSudoPassword:$PromptForSudoPassword $addAuthorizedKeyArgs
} -Force

Set-Item function:global:Fabric-TestDeploy {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Hosts,
        [switch]$PromptForPassphrase,
        [switch]$PromptForLoginPassword,
        [switch]$PromptForSudoPassword,
        [Parameter(Mandatory=$true)]
        [string]$Repo
    )
    $testDeployArgs = @("test-deploy")
    $testDeployArgs += "--repo"
    $testDeployArgs += $Repo

    Invoke-Fabric $Hosts -PromptForPassphrase:$PromptForPassphrase -PromptForLoginPassword:$PromptForLoginPassword -PromptForSudoPassword:$PromptForSudoPassword $testDeployArgs
} -Force
