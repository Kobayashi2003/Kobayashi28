<#
.SYNOPSIS
    Gets the public IP address of the current machine
.DESCRIPTION
    This PowerShell script retrieves the public IP address of the current machine by querying an external service (ifconfig.me).
.EXAMPLE
    PS> ./Get-PubIP.ps1
    ⏳ Retrieving public IP address...
    ✔️ Your public IP address is: 203.0.113.1 (retrieved in 2s)
#>

try {
    $stopWatch = [system.diagnostics.stopwatch]::startNew()

    Write-Host "⏳ Retrieving public IP address..." -ForegroundColor Yellow

    $publicIP = (Invoke-WebRequest -Uri "http://ifconfig.me/ip" -UseBasicParsing -ErrorAction Stop).Content

    if ([string]::IsNullOrWhiteSpace($publicIP)) {
        throw "Retrieved IP address is empty or null"
    }

    [int]$elapsed = $stopWatch.Elapsed.TotalSeconds
    Write-Host "✔️ Your public IP address is: $publicIP (retrieved in $($elapsed)s)" -ForegroundColor Green

    exit 0 # success
} catch {
    Write-Host "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])" -ForegroundColor Red
    exit 1
}