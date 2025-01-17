Script: *list-passwords.ps1*
========================

This PowerShell script lists random passwords.

Parameters
----------
```powershell
D:\Program\code\1_Programing_Language\PowerShell\easy-pwsh\utils\list-passwords.ps1 [[-PasswordLength] <Int32>] [[-Colu
mns] <Int32>] [[-Rows] <Int32>] [<CommonParameters>]

是否必需?                    False
位置?                        1
默认值                15
是否接受管道输入?            false
是否接受通配符?              False

是否必需?                    False
位置?                        2
默认值                6
是否接受管道输入?            false
是否接受通配符?              False

是否必需?                    False
位置?                        3
默认值                30
是否接受管道输入?            false
是否接受通配符?              False

[<CommonParameters>]
    This script supports the common parameters: Verbose, Debug, ErrorAction, ErrorVariable, WarningAction, 
    WarningVariable, OutBuffer, PipelineVariable, and OutVariable.
```

Example
-------
```powershell
PS> ./list-passwords.ps1



"4yE=[mu"Az|IE@   PZ}E9Q"&?.!%49`   zU3[E7`xA)(6W_3   :wd'a(O@fr}.Z8=

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
	Lists random passwords
.DESCRIPTION
	This PowerShell script lists random passwords.
.PARAMETER PasswordLength
	Specifies the length of the password
.PARAMETER Columns
	Specifies the number of columns
.PARAMETER Rows
	Specifies the number of rows
.EXAMPLE
	PS> ./list-passwords.ps1

	"4yE=[mu"Az|IE@   PZ}E9Q"&?.!%49`   zU3[E7`xA)(6W_3   :wd'a(O@fr}.Z8=
	...
.LINK
	https://github.com/fleschutz/PowerShell
.NOTES
	Author: Markus Fleschutz | License: CC0
#>

param([int]$PasswordLength = 15, [int]$Columns = 6, [int]$Rows = 30)

$MinCharCode = 33
$MaxCharCode = 126

try {
	write-output ""
	$Generator = New-Object System.Random
	for ($j = 0; $j -lt $Rows; $j++) {
		$Line = ""
		for ($k = 0; $k -lt $Columns; $k++) {
			for ($i = 0; $i -lt $PasswordLength; $i++) {
				$Line += [char]$Generator.next($MinCharCode,$MaxCharCode)
			}
			$Line += "   "
		}
		write-output "$Line"
	}
	write-output ""
	exit 0 # success
} catch {
	"⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
	exit 1
}
```

*(generated by convert-ps2md.ps1 using the comment-based help of list-passwords.ps1 as of 08/13/2024 16:11:36)*
