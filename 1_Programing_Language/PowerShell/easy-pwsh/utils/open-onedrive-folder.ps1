<#
.SYNOPSIS
	Opens the user's onedrive folder
.DESCRIPTION
	This script launches the File Explorer with the user's onedrive folder.
.EXAMPLE
	PS> ./open-onedrive-folder
.NOTES
	Author: KOBAYASHI
#>

try {
	$TargetDir = resolve-path "$HOME/OneDrive"
	if (-not(test-path "$TargetDir" -pathType container)) {
		throw "OneDrive folder at 📂$TargetDir doesn't exist (yet)"
	}
	& "$PSScriptRoot/open-file-explorer.ps1" "$TargetDir"
	exit 0 # success
} catch {
	"⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
	exit 1
}