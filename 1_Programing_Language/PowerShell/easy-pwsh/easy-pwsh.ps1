<#
.SYNOPSIS
    Initialize easy-pwsh
.PARAMETER help
    -h, --help     Show this help message and exit
.PARAMETER version
    -v, --version  Show version information and exit
.PARAMETER init
    -i, --init     Initialize easy-pwsh
.EXAMPLE
    [Admin] PS C:\> easy-pwsh -i
#>

[CmdletBinding(DefaultParameterSetName = 'Default')]
param (
    [Parameter(ParameterSetName = 'Help')]
    [Alias('h')] [switch] $Help,

    [Parameter(ParameterSetName = 'Version')]
    [Alias('v')] [switch] $Version,

    [Parameter(ParameterSetName = 'Init')]
    [Alias('i')] [switch] $Init,

    [Parameter(ParameterSetName = 'Run')]
    [Alias('r')] [switch] $Run)


Write-Host "__   __   __                                                        _           __   __   __"    -ForegroundColor DarkCyan
Write-Host "\ \  \ \  \ \      ___   __ _  ___  _   _     _ __  __      __ ___ | |__       / /  / /  / /"    -ForegroundColor DarkCyan
Write-Host " \ \  \ \  \ \    / _ \ / _`` |/ __|| | | |   | '_ \ \ \ /\ / // __|| '_ \     / /  / /  / /"    -ForegroundColor DarkCyan
Write-Host " / /  / /  / /   |  __/| (_| |\__ \| |_| |   | |_) | \ V  V / \__ \| | | |    \ \  \ \  \ \ "    -ForegroundColor DarkCyan
Write-Host "/_/  /_/  /_/     \___| \__,_||___/ \__, |   | .__/   \_/\_/  |___/|_| |_|     \_\  \_\  \_\"    -ForegroundColor DarkCyan
Write-Host "                                    |___/    |_|                                            "    -ForegroundColor DarkCyan


if ($PSCmdlet.ParameterSetName -eq 'Default' -or $PSCmdlet.ParameterSetName -eq 'Help') {
    Write-Host "Usage: easy-pwsh [-h] [-v] [-i] [-r]"
    Write-Host "  -h, --help     Show this help message and exit"
    Write-Host "  -v, --version  Show version information and exit"
    Write-Host "  -i, --init     Initialize easy-pwsh"
    Write-Host "  -r, --run      Run easy-pwsh"
    return
}

if ($Version) {
    Write-Host "Version: 1.0.0" -ForegroundColor DarkBlue
    return
}

if ($Init) {

    $current_script_dir = Split-Path $MyInvocation.MyCommand.Definition

    if (-not (Test-Path -Path $profile)) {
        New-Item -Path $profile -ItemType File -Force }

    $startup_content = ". $(Join-Path -Path $current_script_dir -ChildPath 'core\init.ps1')"

    if (-not (Select-String -Path $profile -Pattern $startup_content -SimpleMatch)) {
        Add-Content -Path $profile -Value $startup_content }

    if (-not ($env:PSModulePath -like "*$current_script_dir\downloads\Modules*")) {
        [Environment]::SetEnvironmentVariable('PSModulePath', "$current_script_dir\downloads\Modules;$env:PSModulePath", 'User') }

    . $profile

    return
}

if ($Run) {
    $current_script_dir = Split-Path $MyInvocation.MyCommand.Definition
    . $(Join-Path -Path $current_script_dir -ChildPath 'core\init.ps1')
}