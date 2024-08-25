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
    [string] $str,

    [Parameter(Mandatory=$false)]
    [string] $encode,

    [Parameter(Mandatory=$false)]
    [string] $decode
)

$cur_dir = Get-Location
$script_path = Split-Path $MyInvocation.MyCommand.Path
$python_script_folder = Join-Path -Path $script_path -ChildPath "python-common"

if (-not (Test-Path -Path $python_script_folder)) {
    Write-Host "Please put python-common in the same directory with this script" -ForegroundColor Red
    exit 1
}

if (-not $path) {
    $path = $cur_dir
}

if (-not (Test-Path -Path $path)) {
    New-Item -Path $path -ItemType Directory | Out-Null
}

$abs_path = Resolve-Path -Path $path

Set-Location $python_script_folder

& pixi run python ./exchange-code-str.py $str $(if ($encode) { "-e $encode" }) $(if ($decode) { "-d $decode" })

Set-Location $cur_dir

