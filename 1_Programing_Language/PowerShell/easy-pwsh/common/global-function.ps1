<#
.SYNOPSIS
    This script is used to declare some global functions,
    which will be declared before other scripts run
#>


function global:Reload-Envrioment-Path {
<#
    .SYNOPSIS
        Reload the environment variable
#>
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}


function global:Check-Admin {
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