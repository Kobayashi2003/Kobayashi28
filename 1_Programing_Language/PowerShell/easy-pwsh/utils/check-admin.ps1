function Check-Admin {
<#
.SYNOPSIS
    Checks if the current console is elevated
.EXAMPLE
    if (Check-Admin) { ... }
#>
    $admin = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    if ($admin.IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator") -eq $false) {
        return $false
    }
    return $true
}

check-admin