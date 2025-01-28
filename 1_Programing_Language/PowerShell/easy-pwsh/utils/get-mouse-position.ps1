<#
.SYNOPSIS
    Gets the current mouse cursor position
.DESCRIPTION
    This PowerShell script retrieves and displays the current X and Y coordinates of the mouse cursor.
    If the AfterClick switch is used, it waits for a mouse click before reporting the position.
.PARAMETER AfterClick
    If specified, the script waits for a mouse click before reporting the cursor position.
.EXAMPLE
    PS> ./Get-Mouse-Position
    Reports the current mouse position immediately.
.EXAMPLE
    PS> ./Get-Mouse-Position -AfterClick
    Waits for a mouse click, then reports the position where the click occurred.
#>

param (
    [switch]$AfterClick
)

try {
    if ($AfterClick) {
        Write-Host "Click the mouse to get its position..." -ForegroundColor Yellow
        $VK_LBUTTON = 0x01
        $VK_RBUTTON = 0x02
        $VK_MBUTTON = 0x04

        while ($true) {
            if ([WinApi]::GetAsyncKeyState($VK_LBUTTON) -band 0x8000 -or
                [WinApi]::GetAsyncKeyState($VK_RBUTTON) -band 0x8000 -or
                [WinApi]::GetAsyncKeyState($VK_MBUTTON) -band 0x8000) {
                Start-Sleep -Milliseconds 10  # Small delay to ensure click is registered
                break
            }
            Start-Sleep -Milliseconds 10
        }
    }

    $position = [MouseSimulator]::GetMousePosition()
    Write-Host "Current mouse position: X: $($position.X), Y: $($position.Y)" -ForegroundColor Cyan
    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}