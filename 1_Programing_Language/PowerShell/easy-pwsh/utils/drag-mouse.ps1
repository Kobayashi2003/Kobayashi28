<#
.SYNOPSIS
    Simulates a mouse drag operation based on two user-specified click positions
.DESCRIPTION
    This PowerShell script simulates a mouse drag operation. It waits for the user to click twice to determine
    the start and end positions of the drag. The user can specify which mouse button to use for the drag operation
    and the number of steps for the drag movement.
.PARAMETER Button
    Specifies which mouse button to use for the drag operation.
    Accepted values: Left, Middle, Right. Default is Left.
.PARAMETER Steps
    Specifies the number of steps to take during the drag operation. Higher values result in smoother movement.
    Default is 20.
.EXAMPLE
    PS> ./Drag-Mouse
    Simulates a left mouse drag based on two user clicks with default 20 steps
.EXAMPLE
    PS> ./Drag-Mouse -Button Right -Steps 50
    Simulates a right mouse drag based on two user clicks with 50 steps
#>

param (
    [Parameter(Mandatory=$false)]
    [ValidateSet("Left", "Middle", "Right")]
    [string]$Button = "Left",

    [Parameter(Mandatory=$false)]
    [int]$Steps = 20
)

function Wait-ForMouseClick {
    $leftButton = 0x01
    $middleButton = 0x04
    $rightButton = 0x02

    while ($true) {
        Start-Sleep -Milliseconds 10
        if ([WinApi]::GetAsyncKeyState($leftButton) -eq -32767) {
            return [MouseSimulator]::GetMousePosition()
        }
        if ([WinApi]::GetAsyncKeyState($middleButton) -eq -32767) {
            return [MouseSimulator]::GetMousePosition()
        }
        if ([WinApi]::GetAsyncKeyState($rightButton) -eq -32767) {
            return [MouseSimulator]::GetMousePosition()
        }
    }
}

try {
    $buttonMap = @{
        "Left" = 0
        "Middle" = 1
        "Right" = 2
    }
    $buttonCode = $buttonMap[$Button]

    Write-Host "Please click to set the start position for the $Button mouse drag..." -ForegroundColor Cyan
    $startPos = Wait-ForMouseClick
    Write-Host "Start position set to ($($startPos.X),$($startPos.Y))" -ForegroundColor Green

    Write-Host "Now click to set the end position for the drag..." -ForegroundColor Cyan
    $endPos = Wait-ForMouseClick
    Write-Host "End position set to ($($endPos.X),$($endPos.Y))" -ForegroundColor Green

    Write-Host "Simulating $Button mouse drag..." -ForegroundColor Yellow
    [MouseSimulator]::MouseDrag($buttonCode, $startPos.X, $startPos.Y, $endPos.X, $endPos.Y, $Steps)
    Write-Host "$Button mouse drag simulated from ($($startPos.X),$($startPos.Y)) to ($($endPos.X),$($endPos.Y)) in $Steps steps" -ForegroundColor Green

    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}
