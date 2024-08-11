<#
.SYNOPSIS
    This script is used to declare some global variables,
    which will be declared before other scripts run
#>

$global:DOWNLOADS   = Join-Path $env:USERPROFILE -ChildPath "Downloads"
$global:DOCUMENTS   = Join-Path $env:USERPROFILE -ChildPath "Documents"
$global:PICTURES    = Join-Path $env:USERPROFILE -ChildPath "Pictures"
$global:VIDEOS      = Join-Path $env:USERPROFILE -ChildPath "Videos"
$global:APPDATA     = Join-Path $env:USERPROFILE -ChildPath "AppData"

$global:apps = @{
    'steam' = 'D:\Steam\Steam.exe'
    'pikpak' = 'D:\Temp\PikPak\PikPak.exe'
}

$global:scoop_apps = @(
    'git', 'vim', 'gsudo',
    'bat', 'fzf', 'zoxide',
    'lf','chafa', 'posh-git')

$global:modules = @(
    "Get-ChildItemColor",
    "PSReadLine",
    "PSFzf",
    "Terminal-Icons",
    "WriteAscii",
    "gsudoModule"
    "posh-git"
)

$global:show_imported = $false