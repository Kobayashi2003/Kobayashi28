<#
.SYNOPSIS
    Group the files by time

.PARAMETER path
    Path of the files
.PARAMETER year
    Group by year
.PARAMETER month
    Group by month
.PARAMETER day
    Group by day
.PARAMETER depth
    Depth to search
.PARAMETER file_only
    Only group files

.EXAMPLE
    group-by-time -path "./" -format HHmmss -depth 0
#>

param (
    [Parameter(Mandatory = $false)]
    [Alias("p")]
    [string]$path = ".",
    [Parameter(Mandatory = $false)]
    [Alias("f")]
    [switch]$year,
    [Parameter(Mandatory = $false)]
    [Alias("m")]
    [switch]$month,
    [Parameter(Mandatory = $false)]
    [Alias("d")]
    [switch]$day,
    [Parameter(Mandatory = $false)]
    [int]$depth = 0,
    [Parameter(Mandatory = $false)]
    [switch]$file_only
)

$items = Get-ChildItem -Path $path -Recurse -Depth $depth
$format = "" + $(if ($year) { "yyyy" }) + $(if ($month) { "MM" }) + $(if ($day) { "dd" }) +
        $(if (-not ($year -or $month -or $day)) { "yyyyMMdd" })

foreach ($item in $items) {
    $lastWriteTime = $item.LastWriteTime.ToString($format)

    if (-not (Test-Path -Path $lastWriteTime)) {
        try {
            New-Item -Path $lastWriteTime -ItemType Directory
        } catch {
            Write-Host "Failed to create directory: $lastWriteTime" -ForegroundColor Red
            exit 1
        }
    }

    $lastWriteTime = (Get-Item -Path $lastWriteTime)

    if (($item.FullName -ne $lastWriteTime.FullName) -and
        ($item.FullName -ne (Join-Path -Path $lastWriteTime.FullName -ChildPath $item.Name)) -and
        (-not ($file_only -and $item.PSIsContainer))) {
        try {
            Move-Item -Path $item.FullName -Destination $lastWriteTime.FullName
            Write-Host "Moved: $($item.FullName)" -ForegroundColor Green
        } catch {
            Write-Host "Failed to move: $($item.FullName)" -ForegroundColor Red
            exit 1
        }
    }
}

Write-Host "Files grouped by time: $path" -ForegroundColor Green
exit 0
