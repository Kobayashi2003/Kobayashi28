<#
.SYNOPSIS
    Simulates one or more middle mouse clicks
.DESCRIPTION
    This PowerShell script simulates one or more middle mouse clicks at the current cursor position.
    You can specify the number of clicks and the interval between clicks.
.PARAMETER Clicks
    The number of middle mouse clicks to simulate. Default is 1.
.PARAMETER Interval
    The interval between clicks in milliseconds. Default is 0 (no delay).
.EXAMPLE
    PS> ./Click-Middle
    Simulates a single middle mouse click
.EXAMPLE
    PS> ./Click-Middle -Clicks 2 -Interval 100
    Simulates two middle clicks with a 100ms interval between clicks
#>

param (
    [Parameter(Mandatory=$false)]
    [int]$Clicks = 1,

    [Parameter(Mandatory=$false)]
    [int]$Interval = 0
)

try {
    for ($i = 1; $i -le $Clicks; $i++) {
        [MouseSimulator]::MouseClick(1)

        if ($i -lt $Clicks -and $Interval -gt 0) {
            Start-Sleep -Milliseconds $Interval
        }
    }

    $clickText = if ($Clicks -eq 1) { "click" } else { "clicks" }
    Write-Host "$Clicks middle mouse $clickText simulated with $Interval ms interval" -ForegroundColor Magenta
    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}