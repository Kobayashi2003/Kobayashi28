function Get-ChildItemList {

<#
    .SYNOPSIS
        List the items in a directory
    .PARAMETER Path
        The path to the directory
#>

    Get-ChildItem $Arg[0] -Force |
        Format-Table Mode, @{N='Owner';E={(Get-Acl $_.FullName).Owner}}, Length, LastWriteTime, @{N='Name';E={if($_.Target) {$_.Name+' -> '+$_.Target} else {$_.Name}}}
}

Set-Alias -Name 'll' -Value 'Get-ChildItemList'