<#
.SYNOPSIS
	Restores default right-click menu
.DESCRIPTION
	This PowerShell script restores the default right-click menu by modifying the registry.
.EXAMPLE
	PS> ./Restore-DefaultRightClickMenu.ps1
	⏳ Restoring default right-click menu...
	✔️ Default right-click menu has been restored.
#>

try {
    $stopWatch = [system.diagnostics.stopwatch]::startNew()

    Write-Host "⏳ Restoring default right-click menu..."
    Remove-Item -Path "HKCU:\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}" -Recurse -ErrorAction SilentlyContinue

    [int]$elapsed = $stopWatch.Elapsed.TotalSeconds
    "✔️ Default right-click menu has been restored in $($elapsed)s."
    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}