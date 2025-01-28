<#
.SYNOPSIS
	Sets classic right-click menu
.DESCRIPTION
	This PowerShell script sets the classic right-click menu by modifying the registry.
.EXAMPLE
	PS> ./Set-ClassicRightClickMenu.ps1
	⏳ Setting classic right-click menu...
	✔️ Classic right-click menu has been set.
#>

try {
    $stopWatch = [system.diagnostics.stopwatch]::startNew()

    Write-Host "⏳ Setting classic right-click menu..."
    New-Item -Path "HKCU:\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}" -Name "InprocServer32" -Force | Out-Null
    New-ItemProperty -Path "HKCU:\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" -Name "(Default)" -Value "" -PropertyType String -Force | Out-Null

    [int]$elapsed = $stopWatch.Elapsed.TotalSeconds
    "✔️ Classic right-click menu has been set in $($elapsed)s."
    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}