function Get-ChildItemAll {

<#
    .SYNOPSIS
        List the items in a directory, including hidden items
    .PARAMETER Path
        The path to the directory
#>

    Get-ChildItem $Args[0] -Force -Hidden |
        Format-Table Mode, @{N='Owner';E={(Get-Acl $_.FullName).Owner}}, Length, LastWriteTime, @{N='Name';E={if($_.Target) {$_.Name+' -> '+$_.Target} else {$_.Name}}}
}

Set-Alias -Name 'la' -Value 'Get-ChildItemAll'