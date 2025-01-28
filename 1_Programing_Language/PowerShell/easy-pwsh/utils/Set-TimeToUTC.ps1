<#
.SYNOPSIS
	Sets system time to UTC
.DESCRIPTION
	This PowerShell script sets the system time to UTC by modifying the registry.
.EXAMPLE
	PS> ./Set-TimeToUTC.ps1
	⏳ Setting system time to UTC...
	✔️ System time has been set to UTC.
#>

try {
    $stopWatch = [system.diagnostics.stopwatch]::startNew()

    Write-Host "⏳ Setting system time to UTC..."
    Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\TimeZoneInformation" -Name "RealTimeIsUniversal" -Value 1 -Type DWord -Force

    [int]$elapsed = $stopWatch.Elapsed.TotalSeconds
    "✔️ System time has been set to UTC in $($elapsed)s."
    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}