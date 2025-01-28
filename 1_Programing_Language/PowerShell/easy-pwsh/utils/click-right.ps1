<#
.SYNOPSIS
    Simulates one or more right mouse clicks
.DESCRIPTION
    This PowerShell script simulates one or more right mouse clicks at the current cursor position.
    You can specify the number of clicks and the interval between clicks.
.PARAMETER Clicks
    The number of right mouse clicks to simulate. Default is 1.
.PARAMETER Interval
    The interval between clicks in milliseconds. Default is 0 (no delay).
.EXAMPLE
    PS> ./Click-Right
    Simulates a single right mouse click
.EXAMPLE
    PS> ./Click-Right -Clicks 2 -Interval 100
    Simulates two right clicks with a 100ms interval between clicks
#>

param (
    [Parameter(Mandatory=$false)]
    [int]$Clicks = 1,

    [Parameter(Mandatory=$false)]
    [int]$Interval = 0
)

try {
    for ($i = 1; $i -le $Clicks; $i++) {
        [MouseSimulator]::MouseClick(2)

        if ($i -lt $Clicks -and $Interval -gt 0) {
            Start-Sleep -Milliseconds $Interval
        }
    }

    $clickText = if ($Clicks -eq 1) { "click" } else { "clicks" }
    Write-Host "$Clicks right mouse $clickText simulated with $Interval ms interval" -ForegroundColor Blue
    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}