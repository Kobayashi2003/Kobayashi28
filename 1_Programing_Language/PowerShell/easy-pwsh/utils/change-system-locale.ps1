<#
    .SYNOPSIS
        Change the system locale
    .PARAMETER Locale
        The locale to set
    .EXAMPLE
        PS> Change-SystemLocale en-US
#>

[CmdletBinding()]
param (
    [Parameter(Mandatory = $true)]
    [ArgumentCompleter({ param (
        $commandName,
        $parameterName,
        $wordToComplete,
        $commandAst,
        $fakeBoundParameters )
        @( 'zh-CN', 'ja-JP', 'en-US' ) |
            Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object { $_ } })]
    [string] $Locale
)

try {
    $admin = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    if (-not $admin.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        Write-Host "You need to run this script as Administrator" -ForegroundColor Red
        return
    }

    Set-WinSystemLocale -SystemLocale $Locale
    Write-Host "System locale changed to $Locale, restart to take effect"
    $restart = Read-Host "Do you want to restart now? (Y/n)"
    if (-not $restart -or $restart -eq 'y' -or $restart -eq 'Y') {
        Restart-Computer
    }
    exit 0 # sucess
} catch {
    Write-Host "Failed to change system locale" -ForegroundColor Red
    exit 1
}
