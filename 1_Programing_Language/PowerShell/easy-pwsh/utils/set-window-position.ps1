<#
.SYNOPSIS
    Set the foreground window to the first instance of a process with a given name.

.PARAMETER ProcessName
    The name of the process to activate.
.PARAMETER Left
    The left position of the window
.PARAMETER Top
    The top position of the window

.EXAMPLE
    PS> set-window-position -ProcessName "notepad" -Left 100 -Top 100
#>

param (
    [Parameter(Mandatory)]
    [string] $ProcessName,
    [Parameter(Mandatory)]
    [int] $Left,
    [Parameter(Mandatory)]
    [int] $Top
)

$ProcessName = $ProcessName -replace '\.exe$'

$hWnd = (Get-Process -ErrorAction Ignore $ProcessName).Where({ $_.MainWindowTitle }, 'First').MainWindowHandle

if (-not $hWnd) { Throw "No $ProcessName process with a non-empty window title found." }

$null = [WinApi]::SetWindowPos([int]$hWnd,$null,$Left,$Top,0,0,1)
$null = [WinApi]::SetForegroundWindow([int]$hWnd)