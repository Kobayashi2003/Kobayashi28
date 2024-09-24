<#
.SYNOPSIS
    Recodes a file.
.PARAMETER path
    The path of the file to be processed.
.PARAMETER encode
    The encoding code.
.PARAMETER decode
    The decoding code.
.PARAMETER cover
    Cover the original file.
.PARAMETER backup
    Backup the original file.

.EXAMPLE
    PS> ./exchange-code.ps1 -path "C:\Users\user\Desktop\test.txt" -encode "utf-8" -decode "gbk" -cover -backup
#>


param(
    [Parameter(Mandatory=$true)]
    [string] $path,

    [Parameter(Mandatory=$false)]
    [string] $encode,

    [Parameter(Mandatory=$false)]
    [string] $decode,

    [Parameter(Mandatory=$false)]
    [switch] $cover,

    [Parameter(Mandatory=$false)]
    [switch] $backup
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

& pixi run python ./exchange-code.py $path $(if ($encode) { "-e $encode" }) $(if ($decode) { "-d $decode" }) $(if ($cover) { "-c" }) $(if ($backup) { "-b" })

Set-Location $cur_dir
