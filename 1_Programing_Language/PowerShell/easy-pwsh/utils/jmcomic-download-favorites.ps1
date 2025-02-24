<#
.SYNOPSIS
    Export favorites from Jmcomic

.PARAMETER path
    Download path

.EXAMPLE
    jmcomic-download -path C:\Users\user\Downloads
#>

param(
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

& pixi run python ./jmcomic-export-favorites.py

$export_path = Join-Path -Path $jmcomic_dowloader -ChildPath "export"
$ids = @()

if (Test-Path -Path $export_path) {
    $csv_files = Get-ChildItem -Path $export_path -Filter *.csv

    foreach ($csv_file in $csv_files) {
        $csv_ids = @(Get-Content $csv_file.FullName | ForEach-Object {
            if ($_ -match '^\d+') {
                $matches[0]
            }
        })
        $ids += $csv_ids
    }

    # Remove duplicates
    $ids = $ids | Select-Object -Unique
} else {
    Write-Host "No export folder found. Make sure the export was successful." -ForegroundColor Red
    return
}

if ($ids.Count -gt 0) {
    Write-Host "Total unique IDs found: $($ids.Count)" -ForegroundColor Cyan
} else {
    Write-Host "No valid comic IDs found in any CSV file" -ForegroundColor Red
    return
}

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

Write-Host "All comics have already been downloaded." -ForegroundColor Yellow
Set-Location $cur_dir