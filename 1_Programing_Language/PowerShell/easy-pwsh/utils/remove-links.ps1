<#
.SYNOPSIS
    Remove symbolic links in the give directory path

.PARAMETER path
    The path to remove links in
#>


param (
    [Parameter(Mandatory = $true)]
    [String] $path
)

$items = Get-ChildItem "$path" -Force -ErrorAction SilentlyContinue

foreach ($item in $items) {
    if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
        Remove-Item $item -Force -Recurs -ErrorAction SilentlyContinue
        Write-Host "Removed link for $($item.FullName)" -ForegroundColor Yellow
    }
}

Write-Host "Removed all symbolic links in $path" -ForegroundColor Green