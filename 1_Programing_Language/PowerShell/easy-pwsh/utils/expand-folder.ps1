<#
.SYNOPSIS
    expand the files to the current directory

.PARAMETER path
    Path of the files
.PARAMETER depth
    Depth to search

.EXAMPLE
    expand-folder -path "./" -depth 0
#>

param (
    [Parameter(Mandatory = $false)]
    [Alias("p")]
    [string]$path = ".",
    [Parameter(Mandatory = $false)]
    [int]$depth = 0
)

try {
    for ($i = 0; $i -lt $depth; $i++) {
        $dirsList = [System.Collections.ArrayList]::new()
        $items = Get-ChildItem -Path $path
        foreach ($item in $items) {
            if ($item -is [System.IO.DirectoryInfo]) {
                $null = $dirsList.Add($item)
            }
        }
        for ($j = 0; $j -lt $dirsList.Count; $j++) {
            $dir = $dirsList[$j]
            Write-Host "Directory: $($dir.FullName)" -ForegroundColor Green
            $dirPath = $dir.FullName
            $dirItems = Get-ChildItem -Path $dirPath
            $dirItems | Foreach-Object {Write-Host "File: $($_.FullName)" -ForegroundColor Yellow}
            $dirItems | forEach-Object { Move-Item -Path $_.FullName -Destination $path }
        }
    }
    Write-Host "Files expanded: $path" -ForegroundColor Green
    exit 0
} catch {
    Write-Host "Failed to expand folder: $path" -ForegroundColor Red
    exit 1
}
