<#
.SYNOPSIS
    Download from Jmcomic

.PARAMETER id
    comic id
.PARAMETER path
    download path

.EXAMPLE
    jmcomic-download -id 471225 549758 -path C:\Users\user\Downloads
#>


param(
    [Parameter(Mandatory=$true)]
    [ValidatePattern('^[0-9]+$')]
    [string[]] $id,
    [Parameter(Mandatory=$false)]
    [string] $path
)

$cur_dir = Get-Location
$script_path = Split-Path $MyInvocation.MyCommand.Path
$jmcomic_dowloader = Join-Path -Path $script_path -ChildPath "jmcomic-downloader"

if (-not (Test-Path -Path $jmcomic_dowloader)) {
    Write-Host "Please put jmcomic-downloader in the same directory with this script" -ForegroundColor Red
    exit 1
}

if (-not $path) {
    $path = $cur_dir
}

if (-not (Test-Path -Path $path)) {
    New-Item -Path $path -ItemType Directory | Out-Null
}

$abs_path = Resolve-Path -Path $path

Set-Location $jmcomic_dowloader

# save all $id in .jmhistory file
foreach ($i in $id) {
    if (-not (Test-Path -Path ".\.jmhistory")) {
        New-Item -Path ".\.jmhistory" -ItemType File | Out-Null
    }
    if (-not (Select-String -Path ".\.jmhistory" -Pattern $i)) {
        Add-Content -Path ".\.jmhistory" -Value $i
    } else {
        Write-Host "You have already downloaded $i" -ForegroundColor Red
    }
}

& pixi run python ./jmcomic-downloader.py $id -d $abs_path

Set-Location $cur_dir

