<#
.SYNOPSIS
    Simulates smooth mouse wheel scrolling up
.DESCRIPTION
    This PowerShell script simulates smooth mouse wheel scrolling up with specified amount and interval between scroll actions.
.PARAMETER Amount
    The total amount to scroll. Each wheel click is typically 120 units.
.PARAMETER Interval
    The interval between scroll actions in milliseconds. Lower values result in smoother scrolling.
.EXAMPLE
    PS> ./Scroll-Wheel-Up -Amount 480 -Interval 10
#>

param (
    [Parameter(Mandatory=$true)]
    [int]$Amount,
    [Parameter(Mandatory=$true)]
    [int]$Interval
)

try {
    $increment = 20  # Smaller increment for smoother scrolling
    $scrollTimes = [Math]::Ceiling($Amount / $increment)
    for ($i = 0; $i -lt $scrollTimes; $i++) {
        [MouseSimulator]::ScrollWheel($increment)
        Start-Sleep -Milliseconds $Interval
    }
    Write-Host "Mouse wheel smoothly scrolled up by $Amount units with $Interval ms intervals" -ForegroundColor Green
    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}
