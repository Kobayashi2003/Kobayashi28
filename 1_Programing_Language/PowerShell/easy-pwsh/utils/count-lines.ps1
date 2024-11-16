<#
.SYNOPSIS
    Counts lines in files of specified types in given directories.
.DESCRIPTION
    This PowerShell script counts the total number of lines in files of specified types
    in given directories and their subdirectories. It supports including or excluding
    file types and directories.
.PARAMETER FileTypes
    The file extensions to count lines for (e.g., "py", "txt"). If not specified, all file types are counted.
.PARAMETER ExcludeFileTypes
    The file extensions to exclude from counting.
.PARAMETER Path
    The directory path(s) to search in. Defaults to the current directory.
.PARAMETER ExcludePath
    The directory path(s) to exclude from the search.
.EXAMPLE
    PS> ./count-lines.ps1 -FileTypes py,txt -Path C:\Projects -ExcludePath C:\Projects\Temp
.EXAMPLE
    PS> ./count-lines.ps1 -ExcludeFileTypes exe,dll
.NOTES
    Author: KOBAYASHI
#>

param(
    [string[]]$FileTypes,
    [string[]]$ExcludeFileTypes,
    [string[]]$Path = ".",
    [string[]]$ExcludePath
)

function Count-LinesInFile {
    param (
        [string]$FilePath
    )
    return (Get-Content $FilePath | Measure-Object -Line).Lines
}

$totalLines = 0
$fileCount = 0
$typeStats = @{}

$getChildItemParams = @{
    Recurse = $true
    File = $true
}

if ($Path) {
    $getChildItemParams.Path = $Path
}

if ($ExcludePath) {
    $getChildItemParams.Exclude = $ExcludePath
}

$files = Get-ChildItem @getChildItemParams

foreach ($file in $files) {
    $extension = $file.Extension.TrimStart(".")

    if (($FileTypes -and $extension -notin $FileTypes) -or
        ($ExcludeFileTypes -and $extension -in $ExcludeFileTypes)) {
        continue
    }

    $lines = Count-LinesInFile -FilePath $file.FullName
    $totalLines += $lines
    $fileCount++

    if (-not $typeStats.ContainsKey($extension)) {
        $typeStats[$extension] = @{
            FileCount = 0
            LineCount = 0
        }
    }
    $typeStats[$extension].FileCount++
    $typeStats[$extension].LineCount += $lines
}

Write-Host "File Type Statistics:"
$typeStats.GetEnumerator() | Sort-Object { $_.Value.LineCount } -Descending | ForEach-Object {
    Write-Host "$($_.Key): $($_.Value.LineCount) lines in $($_.Value.FileCount) files"
}

Write-Host "`nTotal lines across all processed files: $totalLines"
Write-Host "Total number of files processed: $fileCount"

if ($fileCount -eq 0) {
    Write-Host "No matching files found."
    exit 1
}

exit 0 # success