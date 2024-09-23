<#
.SYNOPSIS
	Lists all PowerShell win32 wmi classes.
.DESCRIPTION
	This PowerShell scripts lists all win32 wmi classes.
.EXAMPLE
	PS> ./list-win32.ps1

    CimClassName
    ------------
    Win32_1394Controller
    Win32_1394ControllerDevice
    Win32_Account
    ...
#>

try {
	Get-CimClass -Namespace root/CIMV2 |
    Where-Object CimClassName -like Win32* |
    Select-Object CimClassName |
    Sort-Object -Property CimClassName
	exit 0 # success
} catch {
	"⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
	exit 1
}