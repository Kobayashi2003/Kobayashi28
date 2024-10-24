Script: *remind-me.ps1*
========================

This PowerShell script creates a scheduled task that will display a popup message.

Parameters
----------
```powershell
D:\Program\code\1_Programing_Language\PowerShell\easy-pwsh\utils\remind-me.ps1 [[-Message] <String>] [[-Time] <DateTime
>] [<CommonParameters>]

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
PS> ./remind-me "Dentist" "4/10/2021 12:00 PM"



TaskPath                                       TaskName                          State

--------                                       --------                          -----

\                                              Reminder_451733811                Ready

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
	Creates a scheduled task that will display a popup message
.DESCRIPTION
	This PowerShell script creates a scheduled task that will display a popup message.
.EXAMPLE
	PS> ./remind-me "Dentist" "4/10/2021 12:00 PM"

	TaskPath                                       TaskName                          State
	--------                                       --------                          -----
	\                                              Reminder_451733811                Ready
.LINK
	https://github.com/fleschutz/PowerShell
.NOTES
	Author: Markus Fleschutz | License: CC0
#>

#requires -version 4

param([string]$Message = "", [datetime]$Time)

try {
	if ($Message -eq "") { $Message = read-host "Enter reminder message" }

	$Task = New-ScheduledTaskAction -Execute msg -Argument "* $Message"
	$Trigger = New-ScheduledTaskTrigger -Once -At $Time
	$Random = (Get-Random)
	Register-ScheduledTask -Action $Task -Trigger $Trigger -TaskName "Reminder_$Random" -Description "Reminder"
	exit 0
} catch {
	"鈿狅笍 Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
	exit 1
}
```

*(generated by convert-ps2md.ps1 using the comment-based help of remind-me.ps1 as of 08/13/2024 16:11:37)*
