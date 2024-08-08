﻿<#
.SYNOPSIS
	Sets the working directory to the user's desktop folder
.DESCRIPTION
	This PowerShell script changes the working directory to the user's desktop folder.
.EXAMPLE
	PS> ./cd-desktop
	📂/home/Markus/Desktop
.LINK
	https://github.com/fleschutz/PowerShell
.NOTES
	Author: Markus Fleschutz | License: CC0
#>

function cd-desktop {
    try {
	    if ($IsLinux) {
		    $Path = Resolve-Path "~/Desktop"
	    } else {
		    $Path = [Environment]::GetFolderPath('DesktopDirectory')
	    }
	    if (Test-Path "$Path" -pathType container) {
		    Set-Location "$Path"
		    "📂$Path"
            return
	    }
	    throw "User's desktop folder at 📂$Path doesn't exist (yet)"
    } catch {
	    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    }
}