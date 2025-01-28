function sh {
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