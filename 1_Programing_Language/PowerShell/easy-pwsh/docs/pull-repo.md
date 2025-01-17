Script: *pull-repo.ps1*
========================

This PowerShell script pulls remote updates into a local Git repository (including submodules).

Parameters
----------
```powershell
D:\Program\code\1_Programing_Language\PowerShell\easy-pwsh\utils\pull-repo.ps1 [[-pathToRepo] <String>] [<CommonParamet
ers>]

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
PS> ./pull-repo.ps1



⏳ (1/4) Searching for Git executable...  git version 2.44.0.windows.1

⏳ (2/4) Checking local repository...     C:\Repos\rust

⏳ (3/4) Pulling remote updates...

⏳ (4/4) Updating submodules...

✔️ Updates pulled into 📂rust repo in 14s.

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
	Pulls updates into a Git repo
.DESCRIPTION
	This PowerShell script pulls remote updates into a local Git repository (including submodules).
.PARAMETER pathToRepo
	Specifies the file path to the local Git repository (default is working directory)
.EXAMPLE
	PS> ./pull-repo.ps1
	⏳ (1/4) Searching for Git executable...  git version 2.44.0.windows.1
	⏳ (2/4) Checking local repository...     C:\Repos\rust
	⏳ (3/4) Pulling remote updates...
	⏳ (4/4) Updating submodules...
	✔️ Updates pulled into 📂rust repo in 14s.
.LINK
	https://github.com/fleschutz/PowerShell
.NOTES
	Author: Markus Fleschutz | License: CC0
#>

param([string]$pathToRepo = "$PWD")

try {
	$stopWatch = [system.diagnostics.stopwatch]::startNew()

	Write-Host "⏳ (1/4) Searching for Git executable...  " -noNewline
	& git --version
	if ($lastExitCode -ne "0") { throw "Can't execute 'git' - make sure Git is installed and available" }

	Write-Host "⏳ (2/4) Checking local repository...     $pathToRepo"
	if (-not(Test-Path "$pathToRepo" -pathType container)) { throw "Can't access folder: $pathToRepo" }
	$result = (git -C "$pathToRepo" status)
	if ("$result" -match "HEAD detached at ") { throw "Nothing to pull due to detached HEAD state (not on a branch!)" }
	$pathToRepoName = (Get-Item "$pathToRepo").Name

	Write-Host "⏳ (3/4) Pulling remote updates...        " -noNewline
        & git -C "$pathToRepo" remote get-url origin
        if ($lastExitCode -ne "0") { throw "'git remote get-url origin' failed with exit code $lastExitCode" }

	& git -C "$pathToRepo" pull --recurse-submodules=yes
	if ($lastExitCode -ne "0") { throw "'git pull' failed with exit code $lastExitCode" }

	Write-Host "⏳ (4/4) Updating submodules... "
	& git -C "$pathToRepo" submodule update --init --recursive
	if ($lastExitCode -ne "0") { throw "'git submodule update' failed with exit code $lastExitCode" }

	[int]$elapsed = $stopWatch.Elapsed.TotalSeconds
	"✔️ Updates pulled into 📂$pathToRepoName repo in $($elapsed)s."
	exit 0 # success
} catch {
	"⚠️ Error: $($Error[0]) in script line $($_.InvocationInfo.ScriptLineNumber)"
	exit 1
}
```

*(generated by convert-ps2md.ps1 using the comment-based help of pull-repo.ps1 as of 08/13/2024 16:11:37)*
