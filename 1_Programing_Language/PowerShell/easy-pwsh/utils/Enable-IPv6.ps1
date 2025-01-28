<#
.SYNOPSIS
	Enables IPv6 on all network adapters
.DESCRIPTION
	This PowerShell script enables IPv6 on all network adapters in the system.
.EXAMPLE
	PS> ./Enable-IPv6.ps1
	⏳ Enabling IPv6 on all network adapters...
	✔️ IPv6 has been enabled on all network adapters.
#>

try {
    $stopWatch = [system.diagnostics.stopwatch]::startNew()

    Write-Host "⏳ Enabling IPv6 on all network adapters..."
    Enable-NetAdapterBinding -Name "*" -ComponentID ms_tcpip6 -ErrorAction Stop

    [int]$elapsed = $stopWatch.Elapsed.TotalSeconds
    "✔️ IPv6 has been enabled on all network adapters in $($elapsed)s."
    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}