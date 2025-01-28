<#
.SYNOPSIS
	Disables IPv6 on all network adapters
.DESCRIPTION
	This PowerShell script disables IPv6 on all network adapters in the system.
.EXAMPLE
	PS> ./Disable-IPv6.ps1
	⏳ Disabling IPv6 on all network adapters...
	✔️ IPv6 has been disabled on all network adapters.
#>

try {
    $stopWatch = [system.diagnostics.stopwatch]::startNew()

    Write-Host "⏳ Disabling IPv6 on all network adapters..."
    Disable-NetAdapterBinding -Name "*" -ComponentID ms_tcpip6 -ErrorAction Stop

    [int]$elapsed = $stopWatch.Elapsed.TotalSeconds
    "✔️ IPv6 has been disabled on all network adapters in $($elapsed)s."
    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}