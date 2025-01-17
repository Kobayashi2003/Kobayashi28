Script: *list-submodules.ps1*
========================

This PowerShell script lists the submodules in the given Git repository.

Parameters
----------
```powershell
D:\Program\code\1_Programing_Language\PowerShell\easy-pwsh\utils\list-submodules.ps1 [[-RepoDir] <String>] [<CommonPara
meters>]

是否必需?                    False
位置?                        1
默认值                "$PWD"
是否接受管道输入?            false
是否接受通配符?              False

[<CommonParameters>]
    This script supports the common parameters: Verbose, Debug, ErrorAction, ErrorVariable, WarningAction, 
    WarningVariable, OutBuffer, PipelineVariable, and OutVariable.
```

Example
-------
```powershell
PS> ./list-submodules.ps1 C:\MyRepo

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
	Lists the submodules in a Git repository
.DESCRIPTION
	This PowerShell script lists the submodules in the given Git repository.
.PARAMETER RepoDir
	Specifies the path to the repository (current working directory by default)
.EXAMPLE
	PS> ./list-submodules.ps1 C:\MyRepo
.LINK
	https://github.com/fleschutz/PowerShell
.NOTES
	Author: Markus Fleschutz | License: CC0
#>

param([string]$RepoDir = "$PWD")

try {
	Write-Host "⏳ (1/4) Searching for Git executable...   " -noNewline
	& git --version
	if ($lastExitCode -ne "0") { throw "Can't execute 'git' - make sure Git is installed and available" }

	$RepoDirName = (Get-Item "$RepoDir").Name
	Write-Host "⏳ (2/4) Checking Git repository...        📂$RepoDirName"
	if (-not(Test-Path "$RepoDir" -pathType container)) { throw "Can't access folder: $RepoDir" }

	Write-Host "⏳ (3/4) Fetching latest updates... "
	& git -C "$RepoDir" fetch
	if ($lastExitCode -ne "0") { throw "'git fetch' failed" }

	Write-Host "⏳ (4/4) Listing submodules... "
	& git -C "$RepoDir" submodule
	if ($lastExitCode -ne "0") { throw "'git submodule' failed" }

	exit 0 # success
} catch {
	"⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
	exit 1
}
```

*(generated by convert-ps2md.ps1 using the comment-based help of list-submodules.ps1 as of 08/13/2024 16:11:36)*
