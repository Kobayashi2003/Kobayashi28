<#
.SYNOPSIS
    Get the position of a window
.PARAMETER ProcessName
    The name of the process to activate.
.EXAMPLE
    PS> get-window-position -ProcessName "notepad"
#>


param (
    [Parameter(Mandatory)]
    [string] $ProcessName
)

$ProcessName = $ProcessName -replace '\.exe$'

$hWnd = (Get-Process -ErrorAction Ignore $ProcessName).Where({ $_.MainWindowTitle }, 'First').MainWindowHandle

if (-not $hWnd) { Throw "No $ProcessName process with a non-empty window title found." }

$rect = New-Object 'RECT'
[void][WinApi]::GetWindowRect([int]$hWnd,[ref]$rect)

Write-Host "Window position: $($rect.left), $($rect.top)"