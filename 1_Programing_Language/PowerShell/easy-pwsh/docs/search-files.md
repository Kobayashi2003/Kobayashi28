Script: *search-files.ps1*
========================

This PowerShell script searches for the given pattern in the given files.

Parameters
----------
```powershell
D:\Program\code\1_Programing_Language\PowerShell\easy-pwsh\utils\search-files.ps1 [[-textPattern] <String>] [[-filePatt
ern] <String>] [<CommonParameters>]

是否必需?                    False
位置?                        1
默认值
是否接受管道输入?            false
是否接受通配符?              False

是否必需?                    False
位置?                        2
默认值
是否接受管道输入?            false
是否接受通配符?              False

[<CommonParameters>]
    This script supports the common parameters: Verbose, Debug, ErrorAction, ErrorVariable, WarningAction, 
    WarningVariable, OutBuffer, PipelineVariable, and OutVariable.
```

Example
-------
```powershell
PS> ./search-files.ps1 UFO *.ps1



FILE                                              LINE

----                                              ----

/home/Markus/PowerShell/scripts/check-month.ps1   17: $MonthName = (Get-Date -UFormat %B)

...

```

Notes
-----
Author: Markus Fleschutz | License: CC0

Related Links
-------------
https://github.com/fleschutz/PowerShell

Script Content
--------------
```powershell
<#
.SYNOPSIS
	Searches for a text pattern in files
.DESCRIPTION
	This PowerShell script searches for the given pattern in the given files.
.PARAMETER textPattern
	Specifies the text pattern to search for
.PARAMETER filePattern
	Specifies the files to search
.EXAMPLE
	PS> ./search-files.ps1 UFO *.ps1

	FILE                                              LINE
	----                                              ----
	/home/Markus/PowerShell/scripts/check-month.ps1   17: $MonthName = (Get-Date -UFormat %B)
	...
.LINK
	https://github.com/fleschutz/PowerShell
.NOTES
	Author: Markus Fleschutz | License: CC0
#>

param([string]$textPattern = "", [string]$filePattern = "")

function ListLocations { param([string]$Pattern, [string]$Path)
	$list = Select-String -path $Path -pattern "$Pattern"
	foreach ($item in $list) {
		New-Object PSObject -Property @{ 'FILE'="$($item.Path)"; 'LINE'="$($item.LineNumber):$($item.Line)" }
	}
	Write-Output "✔️ Found $($list.Count) lines containing '$Pattern' in $filePattern."
}

try {
	if ($textPattern -eq "" ) { $textPattern = Read-Host "Enter the text pattern (e.g. 'UFO')" }
	if ($filePattern -eq "" ) { $filePattern = Read-Host "Enter the file pattern (e.g. '*.ps1')" }

	ListLocations $textPattern $filePattern | Format-Table -property FILE,LINE -autoSize
	exit 0 # success
} catch {
	"⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
	exit 1
}
```

*(generated by convert-ps2md.ps1 using the comment-based help of search-files.ps1 as of 08/13/2024 16:11:37)*
