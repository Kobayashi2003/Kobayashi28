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

$global:SET_APPS_ALIAS  = $true

$global:IMPORT_MODULES  = $true
$global:CHECK_MODULES   = $false
$global:SHOW_MODULES    = $false

$global:SCOOP_MAIN_FLAG    = $true
$global:SCOOP_EXTRAS_FLAG  = $false
$global:SCOOP_VERSION_FLAG = $false

$global:SCOOP_CHECK_UPDATE = $false
$global:SCOOP_CHECK_INSTALL = $false
$global:SCOOP_CHECK_FAILED = $false

$global:APPS_ALIAS = $( if (-not $SET_APPS_ALIAS) { @{} } else {
@{
    'steam'     = 'D:\Steam\Steam.exe'
    'pikpak'    = 'D:\Temp\PikPak\PikPak.exe'

    'wechat'    = 'C:\Program Files (x86)\Tencent\WeChat\WeChat.exe'
}})

$global:SCOOP_APPLICATION_MAIN = $( if (-not $SCOOP_MAIN_FLAG) { @() } else {
@(
    '7zip',     'aria2',    'bat',
    'chafa',    'fd',       'ffmpeg',
    'fzf',      'git',      'gsudo',
    'lf',       'prince',   'ripgrep',
    'scrcpy',   'sudo',     'vim',
    'zoxide',   'miniconda3', 'yazi',
    'pandoc',   'latex',    'postgresql',
    'jq',       'poppler',  'imagemagick'
)})

$global:SCOOP_APPLICATION_EXTRAS = $( if (-not $SCOOP_EXTRAS_FLAG) { @() } else {
@(
    'altsnap',          'bandizip',
    'everything',       'imageglass',
    'moonlight',        'mpv',
    'cheat-engine',     'posh-git',
    'putty',            'quicklook',
    'recuva',           'sunshine',
    'vscode',           'winmerge'
)})

$global:SCOOP_APPLICATION_VERSION = $( if (-not $SCOOP_VERSION_FLAG) { @() } else {
@(
    'tdm-gcc'
)})

$global:SCOOP_APPLICATION = $(if (-not $SCOOP_CHECK_INSTALL) { @() } else {
    $scoop_buckets = (& scoop bucket list).Name
    @() + `
    $(if ($scoop_buckets -contains "main") { $global:SCOOP_APPLICATION_MAIN } else { @() }) + `
    $(if ($scoop_buckets -contains "extras") { $global:SCOOP_APPLICATION_EXTRAS } else { @() }) + `
    $(if ($scoop_buckets -contains "versions") { $global:SCOOP_APPLICATION_VERSION } else { @() })
})

$global:SCOOP_UPDATE_IGNORE = @(
    'postgresql', 'mysql'
)

$global:MODULES = $( if (-not $IMPORT_MODULES) { @{} } else {
@{
    "PSReadLine"         = $(if ($global:PSVERSION -ge "7.2.0") { "latest" } else { "==2.3.4" })
    # "PSFzf"              = $(if ($global:PSVERSION -ge "7.2.0") { "latest" } else { "==2.0.0" })
    # "Get-ChildItemColor" = "latest"
    "WriteAscii"         = "latest"
    # "Terminal-Icons"     = "latest"
    # "posh-git"           = "latest"
}})
