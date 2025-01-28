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





function global:sh {
<#
.SYNOPSIS
    This is an alias for powershell
.EXAMPLE
    PS> sh -c "Get-ChildItem | Format-Table Mode, Owner, Length, LastWriteTime, Name"
#>
    if ($global:PSVERSION -lt 7.0) {
        powershell $Args
    } else {
        pwsh $Args
    }
}
