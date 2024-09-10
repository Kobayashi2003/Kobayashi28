<#
.SYNOPSIS
    This script is used to declare some global variables,
    which will be declared before other scripts run
#>

$global:PSVERSION   = (Get-Host).Version.ToString()
$global:USERPROFILE = [Environment]::GetFolderPath("UserProfile")
$global:DESKTOP     = [Environment]::GetFolderPath("Desktop")
$global:DOCUMENTS   = [Environment]::GetFolderPath("MyDocuments")
$global:MUSIC       = [Environment]::GetFolderPath("MyMusic")
$global:PICTURES    = [Environment]::GetFolderPath("MyPictures")
$global:VIDEeS      = [Environment]::GetFolderPath("MyVideos")
$global:STARTUP     = [Environment]::GetFolderPath("Startup")
$global:STARTMENU   = [Environment]::GetFolderPath("StartMenu")
$global:FONTS       = [Environment]::GetFolderPath("Fonts")
$global:COOKIES     = [Environment]::GetFolderPath("Cookies")
$global:HISTORY     = [Environment]::GetFolderPath("History")
$global:TEMP        = [Environment]::GetFolderPath("Temp")
$global:APPDATA     = [Environment]::GetFolderPath("ApplicationData")
$global:LOCALAPPDATA= [Environment]::GetFolderPath("LocalApplicationData")
$global:WINDOWS     = [Environment]::GetFolderPath("Windows")
$global:SYSTEM      = [Environment]::GetFolderPath("System")
$global:SYSTEMX86   = [Environment]::GetFolderPath("SystemX86")
$global:PROGRAMFILES= [Environment]::GetFolderPath("ProgramFiles")
$global:PROGRAMFILESX86= [Environment]::GetFolderPath("ProgramFilesX86")

$global:set_apps_alias  = $true

$global:modules_import  = $true
$global:modules_check   = $false
$global:show_imported   = $false

$global:scoop_install         = $false
$global:scoop_check           = $false
$global:scoop_apps_install    = $true
$global:scoop_extras_install  = $true

$global:apps = $( if (-not $set_apps_alias) { @{} } else {
@{
    'steam'     = 'D:\Steam\Steam.exe'
    'pikpak'    = 'D:\Temp\PikPak\PikPak.exe'
}})

$global:scoop_apps = $( if (-not $scoop_apps_install) { @() } else {
@(
    'git',      'vim',      'gsudo',
    'bat',      'fzf',      'zoxide',
    'lf',       'chafa',    'mpv',
    'ripgrep',  'posh-git', 'tdm-gcc'
)})

$global:scoop_extras = $( if (-not $scoop_extras_install) { @() } else {
@(
    'scrcpy',       'ffmpeg',
    'altsnap',      'wireshark',
    'quicklook',    'everything',
    'sunshine',     'moonlight',
    'bandizip',     'networkmanager'
)})

$global:modules = $( if (-not $modules_import) { @{} } else {
@{
    "PSReadLine"         = $(if ($global:PSVERSION -ge "7.2.0") { "latest" } else { "==2.3.4" })
    "PSFzf"              = $(if ($global:PSVERSION -ge "7.2.0") { "latest" } else { "==2.0.0" })
    "Get-ChildItemColor" = "latest"
    "Terminal-Icons"     = "latest"
    "WriteAscii"         = "latest"
    "posh-git"           = "latest"
}})
