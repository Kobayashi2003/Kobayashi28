<#
.SYNOPSIS
    Simulates a left mouse button drag operation
.DESCRIPTION
    This PowerShell script simulates pressing the left mouse button, moving the cursor to a new position, and then releasing the button.
    If start coordinates are not provided, it uses the current mouse position as the starting point.
    If end coordinates are not provided, it uses the current mouse position for the missing coordinate(s).
.PARAMETER StartX
    The starting X coordinate for the drag operation. If not specified, uses current mouse X position.
.PARAMETER StartY
    The starting Y coordinate for the drag operation. If not specified, uses current mouse Y position.
.PARAMETER EndX
    The ending X coordinate for the drag operation. If not specified, uses current mouse X position.
.PARAMETER EndY
    The ending Y coordinate for the drag operation. If not specified, uses current mouse Y position.
.PARAMETER Steps
    The number of steps to take during the drag operation. Higher values result in smoother movement. Default is 20.
.EXAMPLE
    PS> ./Drag-Left -EndX 300
    Simulates a left mouse drag from the current position to X=300 and current Y
.EXAMPLE
    PS> ./Drag-Left -StartX 100 -StartY 100 -EndX 300 -EndY 300 -Steps 50
    Simulates a smoother left mouse drag from (100,100) to (300,300) with 50 steps
#>

param (
    [Parameter(Mandatory=$false)]
    [int]$StartX = -1,

    [Parameter(Mandatory=$false)]
    [int]$StartY = -1,

    [Parameter(Mandatory=$false)]
    [int]$EndX = -1,

    [Parameter(Mandatory=$false)]
    [int]$EndY = -1,

    [Parameter(Mandatory=$false)]
    [int]$Steps = 20
)

try {
    $currentPos = [MouseSimulator]::GetMousePosition()
    $startX = if ($StartX -eq -1) { $currentPos.X } else { $StartX }
    $startY = if ($StartY -eq -1) { $currentPos.Y } else { $StartY }
    $endX = if ($EndX -eq -1) { $currentPos.X } else { $EndX }
    $endY = if ($EndY -eq -1) { $currentPos.Y } else { $EndY }

    [MouseSimulator]::MouseDrag(0, $startX, $startY, $endX, $endY, $Steps)
    Write-Host "Left mouse drag simulated from ($startX,$startY) to ($endX,$endY) in $Steps steps" -ForegroundColor Yellow
    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}