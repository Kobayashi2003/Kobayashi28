<#
.SYNOPSIS
    Restarts the Windows Explorer process.
.DESCRIPTION
    This script restarts the Windows Explorer process.
.EXAMPLE
    PS> Restart-Explorer
#>

try {
    Stop-Process -Name explorer -Force
    Start-Process -FilePath explorer.exe
    "✔ Restarted Windows Explorer"
    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
n}