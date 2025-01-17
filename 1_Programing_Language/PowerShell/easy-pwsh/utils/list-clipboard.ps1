﻿<#
.SYNOPSIS
	Lists the contents of the clipboard
.DESCRIPTION
	This PowerShell script lists the contents of the clipboard.
.EXAMPLE
	PS> ./list-clipboard.ps1
	📋 test
.LINK
	https://github.com/fleschutz/PowerShell
.NOTES
	Author: Markus Fleschutz | License: CC0
#>

try {
	[string]$text = (Get-Clipboard)
	Write-Output "📋 `“ $text `„"
	exit 0 # success
} catch {
	"⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
	exit 1
}