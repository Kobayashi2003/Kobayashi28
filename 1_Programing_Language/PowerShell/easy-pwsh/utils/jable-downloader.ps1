<#
.SYNOPSIS
    Download from Jable

.PARAMETER URL
    Jable Vedio URl
.PARAMETER path
    Vedio save path

.EXAMPLE
    jable-download -url https://jable.tv/videos/ipx-660/ -path C:\Users\user\Downloads
#>


param(
    [Parameter(Mandatory=$true)]
    [ValidatePattern('.*jable.tv/videos/.*/')]
    [string[]] $url,
    [Parameter(Mandatory=$false)]
    [string] $path
)

$cur_dir = Get-Location
$script_path = Split-Path $MyInvocation.MyCommand.Path
$jable_dowloader = Join-Path -Path $script_path -ChildPath "jable-downloader"

if (-not (Test-Path -Path $jable_dowloader)) {
    Write-Host "Please put jable-downloader in the same directory with this script" -ForegroundColor Red
    exit 1
}

if (-not $path) {
    $path = $cur_dir
}

if (-not (Test-Path -Path $path)) {
    New-Item -Path $path -ItemType Directory | Out-Null
}

$abs_path = Resolve-Path -Path $path

Set-Location $jable_dowloader

& pixi run python ./jable-downloader.py $url -p $abs_path

Set-Location $cur_dir


