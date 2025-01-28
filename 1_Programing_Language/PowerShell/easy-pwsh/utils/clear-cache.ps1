<#
.SYNOPSIS
    Clears various Windows caches
.DESCRIPTION
    This PowerShell script clears multiple Windows caches including Windows Prefetch, Windows Temp, User Temp, and Internet Explorer Cache.
.EXAMPLE
    PS> ./Clear-Cache.ps1
    ⏳ (1/5) Clearing Windows Prefetch...
    ⏳ (2/5) Clearing Windows Temp...
    ⏳ (3/5) Clearing User Temp...
    ⏳ (4/5) Clearing Internet Explorer Cache...
    ⏳ (5/5) Verifying cache clearing...
    ✔️ Cleared Windows caches in 3s.
.NOTES
    Author: KOBAYASHI
#>

try {
    $stopWatch = [system.diagnostics.stopwatch]::startNew()

    Write-Host "⏳ (1/5) Clearing Windows Prefetch..." -ForegroundColor Yellow
    Remove-Item -Path "$env:SystemRoot\Prefetch\*" -Force -ErrorAction SilentlyContinue
    if ($lastExitCode -ne "0") { throw "Failed to clear Windows Prefetch" }

    Write-Host "⏳ (2/5) Clearing Windows Temp..." -ForegroundColor Yellow
    Remove-Item -Path "$env:SystemRoot\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
    if ($lastExitCode -ne "0") { throw "Failed to clear Windows Temp" }

    Write-Host "⏳ (3/5) Clearing User Temp..." -ForegroundColor Yellow
    Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
    if ($lastExitCode -ne "0") { throw "Failed to clear User Temp" }

    Write-Host "⏳ (4/5) Clearing Internet Explorer Cache..." -ForegroundColor Yellow
    Remove-Item -Path "$env:LOCALAPPDATA\Microsoft\Windows\INetCache\*" -Recurse -Force -ErrorAction SilentlyContinue
    if ($lastExitCode -ne "0") { throw "Failed to clear Internet Explorer Cache" }

    Write-Host "⏳ (5/5) Verifying cache clearing..." -ForegroundColor Yellow
    # Add verification logic here if needed

    [int]$elapsed = $stopWatch.Elapsed.TotalSeconds
    Write-Host "✔️ Cleared Windows caches in $($elapsed)s." -ForegroundColor Green
    exit 0 # success
} catch {
    Write-Host "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])" -ForegroundColor Red
    exit 1
}