<#
.SYNOPSIS
    Starts a new CMD window and closes the current PowerShell session.
.DESCRIPTION
    This script launches a new CMD window as an independent process and then
    closes the current PowerShell session. The new CMD window is not a child
    process of the PowerShell session.
.EXAMPLE
    PS> .\open-cmd.ps1
.NOTES
    Author: AI Assistant | License: CC0
#>

try {
    # Get the path to cmd.exe
    $cmdPath = "$env:SystemRoot\System32\cmd.exe"

    # Create a new process start info
    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = $cmdPath
    $startInfo.UseShellExecute = $true  # This ensures it's not a child process

    # Start the new CMD process
    [System.Diagnostics.Process]::Start($startInfo)

    exit 0 # success
}
catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}