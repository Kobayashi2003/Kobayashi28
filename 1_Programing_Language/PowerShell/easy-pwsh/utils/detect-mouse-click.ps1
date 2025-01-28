<#
.SYNOPSIS
    Detects and displays all mouse click events using GetAsyncKeyState
.DESCRIPTION
    This PowerShell script continuously monitors mouse click events including button presses,
    releases. It uses the GetAsyncKeyState method from the WinApi
    class to detect mouse events and displays them in real-time.
.EXAMPLE
    PS> ./Detect-Mouse-Click.ps1
    Starts detecting and displaying mouse click events. Press Ctrl+C to stop.
#>

function Get-KeyState($key) {
    return [WinApi]::GetAsyncKeyState($key) -band 0x8000
}

$VK_LBUTTON = 0x01
$VK_RBUTTON = 0x02
$VK_MBUTTON = 0x04

$prevLeftState = $false
$prevRightState = $false
$prevMiddleState = $false

Write-Host "Detecting mouse events. Press Ctrl+C to stop." -ForegroundColor Yellow

try {
    while ($true) {
        $currentPos = [MouseSimulator]::GetMousePosition()

        # Left Button
        $leftState = Get-KeyState $VK_LBUTTON
        if ($leftState -and -not $prevLeftState) {
            Write-Host "Left button pressed at X: $($currentPos.X), Y: $($currentPos.Y)" -ForegroundColor Cyan
        }
        elseif (-not $leftState -and $prevLeftState) {
            Write-Host "Left button released at X: $($currentPos.X), Y: $($currentPos.Y)" -ForegroundColor Cyan
        }
        $prevLeftState = $leftState

        # Right Button
        $rightState = Get-KeyState $VK_RBUTTON
        if ($rightState -and -not $prevRightState) {
            Write-Host "Right button pressed at X: $($currentPos.X), Y: $($currentPos.Y)" -ForegroundColor Magenta
        }
        elseif (-not $rightState -and $prevRightState) {
            Write-Host "Right button released at X: $($currentPos.X), Y: $($currentPos.Y)" -ForegroundColor Magenta
        }
        $prevRightState = $rightState

        # Middle Button
        $middleState = Get-KeyState $VK_MBUTTON
        if ($middleState -and -not $prevMiddleState) {
            Write-Host "Middle button pressed at X: $($currentPos.X), Y: $($currentPos.Y)" -ForegroundColor Green
        }
        elseif (-not $middleState -and $prevMiddleState) {
            Write-Host "Middle button released at X: $($currentPos.X), Y: $($currentPos.Y)" -ForegroundColor Green
        }
        $prevMiddleState = $middleState

        Start-Sleep -Milliseconds 10  # Reduce CPU usage
    }
}
finally {
    Write-Host "`nMouse event detection stopped." -ForegroundColor Yellow
}
