<#
.SYNOPSIS
    Sets the mouse cursor position
.DESCRIPTION
    This PowerShell script sets the mouse cursor to the specified X and Y coordinates.
.PARAMETER X
    The X coordinate to set the mouse cursor to.
.PARAMETER Y
    The Y coordinate to set the mouse cursor to.
.EXAMPLE
    PS> ./Set-Mouse-Position -X 100 -Y 200
#>

param (
    [Parameter(Mandatory=$true)]
    [int]$X,
    [Parameter(Mandatory=$true)]
    [int]$Y
)

try {
    [MouseSimulator]::SetMousePosition($X, $Y)
    Write-Host "Mouse position set to X: $X, Y: $Y" -ForegroundColor Green
    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}