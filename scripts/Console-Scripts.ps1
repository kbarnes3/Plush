. $PSScriptRoot\Invoke-Fabric.ps1

Set-Item function:global:Build-Plush {
    Push-Location $PSScriptRoot\..\python
    python -m build
    Pop-Location
}

Set-Item function:global:Publish-Plush {
    param(
        [Parameter(Mandatory=$true)]
        [ValidateSet('TestPyPI','PyPI')]
        [string]$Repository
    )
    Push-Location $PSScriptRoot\..\python
    $version = Get-PlushVersion
    if ($Repository -eq 'PyPI') {
        python -m twine upload "dist/*$version*"
    } else {
        python -m twine upload --repository testpypi "dist/*$version*"
    }
    Pop-Location
}

Set-Item function:global:Get-PlushVersion {
    Push-Location $PSScriptRoot\..
    $regex = 'version = (.+)'
    $matchingLines = (Get-Content .\python\setup.cfg) -match $regex
    $matchingLines[0] -match $regex | Out-Null
    $version = $Matches[1]
    Pop-Location
    return $version
} -Force

Set-Item function:global:Update-DevEnvironment {
    param([switch]$Verbose)
    . $PSScriptRoot\Update.ps1 -Verbose:$Verbose
} -Force

Set-Item function:global:Upgrade-Requirements {
    Push-Location $PSScriptRoot\..
    & pip-compile --upgrade --output-file=win64-py310-requirements.txt .\requirements.in
    $requirements = Get-Content .\win64-py310-requirements.txt
    $requirements = $requirements -replace 'file:///.*Plush/python', './python'
    Set-Content -Path .\win64-py310-requirements.txt -Value $requirements
    Pop-Location
    Write-Host 'win64-py310-requirements.txt updated.'
    Write-Host 'Run pip-sync win64-py310-requirements.txt to update your environment.'
}
