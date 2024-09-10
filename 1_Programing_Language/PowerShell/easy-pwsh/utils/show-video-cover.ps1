<#
.SYNOPSIS
    Show video cover
.PARAMETER path
    Path to video
.PARAMETER size
#>

param(
    [Parameter(Mandatory=$true)]
    [string] $path,
    [Parameter(Mandatory=$false)]
    [string] $size
)

$cur_dir = Get-Location
$script_path = Split-Path $MyInvocation.MyCommand.Path
$pixi_folder = Join-Path -Path $script_path -ChildPath "show-video-cover"

if (-not (Test-Path -Path $pixi_folder)) {
    Write-Host "Please put show-video-cover in the same directory with this script" -ForegroundColor Red
    exit 1
}

if (-not $path) {
    $path = $cur_dir
}

if (-not (Test-Path -Path $path)) {
    New-Item -Path $path -ItemType Directory | Out-Null
}

$abs_path = Resolve-Path -Path $path

Set-Location $pixi_folder

if ($size) {
    & pixi run python ./show-video-cover.py -i $path -s $size
} else {
    & pixi run python ./show-video-cover.py -i $path
}

Set-Location $cur_dir
