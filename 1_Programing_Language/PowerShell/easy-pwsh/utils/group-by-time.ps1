<#
.SYNOPSIS
    Group the files by time

.PARAMETER path
    Path of the files
.PARAMETER format
    Format of the files
.PARAMETER depth
    Depth to search

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
    [int]$depth = 0
)

$files = Get-ChildItem -Path $path -Recurse -Depth $depth
$format = "" + $(if ($year) { "yyyy" }) + $(if ($month) { "MM" }) + $(if ($day) { "dd" }) +
        $(if (-not ($year -or $month -or $day)) { "yyyyMMdd" })

foreach ($file in $files) {
    $lastWriteTime = $file.LastWriteTime.ToString($format)

    if (-not (Test-Path -Path $lastWriteTime)) {
        try {
            New-Item -Path $lastWriteTime -ItemType Directory
        } catch {
            Write-Host "Failed to create directory: $lastWriteTime" -ForegroundColor Red
            exit 1
        }
    }

    $lastWriteTime = (Get-Item -Path $lastWriteTime)

    if (($file.FullName -ne $lastWriteTime.FullName) -and
        ($file.FullName -ne (Join-Path -Path $lastWriteTime.FullName -ChildPath $file.Name))) {
        try {
            Move-Item -Path $file.FullName -Destination $lastWriteTime.FullName
            Write-Host "Moved file: $($file.FullName)" -ForegroundColor Green
        } catch {
            Write-Host "Failed to move file: $($file.FullName)" -ForegroundColor Red
            exit 1
        }
    }
}

Write-Host "Files grouped by time: $path" -ForegroundColor Green
exit 0
