<#
.SYNOPSIS
    This script is used to declare some global variables,
    which will be declared before other scripts run
#>

$global:PSVERSION = "$($PSVersionTable.PSVersion.Major).$($PSVersionTable.PSVersion.Minor)"

$global:DOWNLOADS   = Join-Path $env:USERPROFILE -ChildPath "Downloads"
$global:DOCUMENTS   = Join-Path $env:USERPROFILE -ChildPath "Documents"
$global:PICTURES    = Join-Path $env:USERPROFILE -ChildPath "Pictures"
$global:VIDEOS      = Join-Path $env:USERPROFILE -ChildPath "Videos"
$global:APPDATA     = Join-Path $env:USERPROFILE -ChildPath "AppData"

$global:apps = @{
    'steam'     = 'D:\Steam\Steam.exe'
    'pikpak'    = 'D:\Temp\PikPak\PikPak.exe'
}

$global:scoop_apps = @(
    'git',      'vim',      'gsudo',
    'bat',      'fzf',      'zoxide',
    'lf',       'chafa',    'mpv',
    'ripgrep',  'posh-git'
)

$global:scoop_extras = @(
    'scrcpy',       'ffmpeg',
    'altsnap',      'wireshark',
    'quicklook',    'everything',
    'sunshine',     'moonlight',
    'bandizip',     'networkmanager'
)

$global:modules = @{
    "Get-ChildItemColor" = "latest"
    "PSReadLine"         = "==2.3.4"
    "PSFzf"              = "==2.0.0"
    # "Terminal-Icons"     = "latest"
    "WriteAscii"         = "latest"
    # "gsudoModule"        = "latest"
    "posh-git"           = "latest"
}

$global:modules_check = $false

$global:show_imported = $false