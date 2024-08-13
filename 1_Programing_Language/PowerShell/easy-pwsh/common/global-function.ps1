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


function global:Get-ChildItemAll {

<#
    .SYNOPSIS
        List the items in a directory, including hidden items
    .PARAMETER Path
        The path to the directory
#>

    Get-ChildItem $Args[0] -Force |
        Format-Table Mode, @{N='Owner';E={(Get-Acl $_.FullName).Owner}}, Length, LastWriteTime, @{N='Name';E={if($_.Target) {$_.Name+' -> '+$_.Target} else {$_.Name}}}
}


function global:Get-ChildItemList {

<#
    .SYNOPSIS
        List the items in a directory
    .PARAMETER Path
        The path to the directory
#>

    Get-ChildItem $Args[0] |
        Format-Table Mode, @{N='Owner';E={(Get-Acl $_.FullName).Owner}}, Length, LastWriteTime, @{N='Name';E={if($_.Target) {$_.Name+' -> '+$_.Target} else {$_.Name}}}
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


function global:Reload-Script {

<#
    .SYNOPSIS
        Reloads the current script
    .EXAMPLE
        Reload-Script
#>

    Get-Process -Id $PID | Select-Object -ExpandProperty Path | ForEach-Object { Invoke-Command { & "$_" } -NoNewScope }
    exit
}


function global:mkdir-cd {

<#
    .SYNOPSIS
        Creates a new directory and changes to it
    .DESCRIPTION
        Creates a new directory and changes to it
    .PARAMETER Path
        The path to the directory
    .EXAMPLE
        mkcd C:\tem
#>

    param(
        [Parameter(Mandatory)]
        [string]$Path
    )
    try {
        if (Test-Path $Path) {
            Set-Location $Path
        } else {
            New-Item -ItemType Directory -Path $Path
            Set-Location $Path
        }
    } catch {
        Write-Host "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    }
}


function global:tail {

<#
    .SYNOPSIS
        Get the last n lines of a text file.
    .PARAMETER Follow
        output appended data as the file grows
    .PARAMETER Lines
        output the last N lines (default: 10)
    .PARAMETER Path
        path to the text file
    .INPUTS
        System.Int
        IO.FileInfo
    .OUTPUTS
        System.String
    .EXAMPLE
        PS> tail c:\server.log
    .EXAMPLE
        PS> tail -f -n 20 c:\server.log
#>

    [CmdletBinding()]
    [OutputType('System.String')]
    Param(
        [parameter(Mandatory=$false)]
        [Alias("f")]
        [switch] $Follow,

        [parameter(Mandatory=$false)]
        [Alias("n")]
        [Int] $Lines = 10,

        [parameter(Mandatory=$true, Position=5)]
        [ValidateNotNullOrEmpty()]
        [IO.FileInfo] $Path
    )

    if ($Follow)
    {
        Get-Content -Path $Path -Tail $Lines -Wait
    }
    else
    {
        Get-Content -Path $Path -Tail $Lines
    }
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


function global:which {

<#
.SYNOPSIS
    Returns the path to an executable
.EXAMPLE
    PS> which git
#>

    (Get-Command $Args[0] -ErrorAction SilentlyContinue).Source
}