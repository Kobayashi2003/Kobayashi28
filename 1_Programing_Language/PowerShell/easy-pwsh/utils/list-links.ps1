<#
.SYNOPSIS
    list symbolic links in the give directory path.

.PARAMETER path
    The path to list links in.
#>


param (
    [Parameter(Mandatory = $true)]
    [String] $path
)

$items = Get-ChildItem "$path" -Force -ErrorAction SilentlyContinue

foreach ($item in $items) {
    if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
        Write-Host "Link: $($item.FullName) ->" -ForegroundColor Yellow -NoNewLine
        Write-Host " $($item.Target)" -ForegroundColor Green
    }
}