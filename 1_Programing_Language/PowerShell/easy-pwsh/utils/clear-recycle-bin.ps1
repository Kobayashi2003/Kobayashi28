<#
.SYNOPSIS
	Clears the recycle bin folder
.DESCRIPTION
	This PowerShell script removes the content of the recycle bin folder permanently.
	IMPORTANT NOTE: this cannot be undo!
.EXAMPLE
	PS> ./clear-recycle-bin
.LINK
	https://github.com/fleschutz/PowerShell
.NOTES
	Author: Markus Fleschutz | License: CC0
#>

try {
	Clear-RecycleBin -Confirm:$false *>$null
	if ($lastExitCode -ne "0") { throw "'Clear-RecycleBin' failed" }
    Write-Host "It's clean now." -foregroundcolor green
	exit 0 # success
} catch {
	"⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
	exit 1
}