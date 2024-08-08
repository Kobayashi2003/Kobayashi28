<#
.SYNOPSIS
    Checks if the current console is elevated
#>

function Check-Admin {
    $admin = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    if ($admin.IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator") -eq $false) {
        return $false
    }
    return $true
}

if ($MyInvocation.InvocationName -ne '.') {

    try {
        if (Check-Admin) {
            Write-Host "Elevated" -ForegroundColor Green
        } else {
            Write-Host "Not elevated" -ForegroundColor Red
        }
    } catch {
	    Write-Host "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    }

}