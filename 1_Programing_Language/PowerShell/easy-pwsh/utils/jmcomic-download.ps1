<#
.SYNOPSIS
    Download from Jmcomic

.PARAMETER id
    Comic id(s)
.PARAMETER path
    Download path
.PARAMETER file
    Path to CSV file containing comic ids

.EXAMPLE
    jmcomic-download -id 471225,549758 -path C:\Users\user\Downloads
.EXAMPLE
    jmcomic-download -file ids.csv -path C:\Users\user\Downloads
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidatePattern('^[0-9]+$')]
    [string[]] $ids,

    [Parameter(Mandatory=$false)]
    [string] $path,

    [Parameter(Mandatory=$false)]
    [string] $file
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

# Read IDs from CSV file if -f is provided
if ($file) {
    if (-not (Test-Path -Path $file)) {
        Write-Host "CSV file not found: $file" -ForegroundColor Red
        exit 1
    }
    $csv_ids = @(Get-Content $file | ForEach-Object {
        if ($_ -match '^\d+') {
            $matches[0]
        }
    })
    $ids += $csv_ids
}

# Remove duplicates and ensure we have at least one ID
$ids = $ids | Select-Object -Unique
if ($ids.Count -eq 0) {
    Write-Host "No valid comic IDs provided" -ForegroundColor Red
    exit 1
}

Set-Location $jmcomic_dowloader

# save all $ids in .jmhistory file
foreach ($i in $ids) {
    if (-not (Test-Path -Path ".\.jmhistory")) {
        New-Item -Path ".\.jmhistory" -ItemType File | Out-Null
    }
    if (-not (Select-String -Path ".\.jmhistory" -Pattern $i)) {
        Add-Content -Path ".\.jmhistory" -Value $i
    } else {
        Write-Host "You have already downloaded $i" -ForegroundColor Yellow
    }
}

& pixi run python ./jmcomic-downloader.py $ids -d $abs_path

Set-Location $cur_dir