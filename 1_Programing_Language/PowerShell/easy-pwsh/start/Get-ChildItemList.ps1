function Get-ChildItemList {
    Get-ChildItem $Args[0] |
        Format-Table Mode, @{N='Owner';E={(Get-Acl $_.FullName).Owner}}, Length, LastWriteTime, @{N='Name';E={if($_.Target) {$_.Name+' -> '+$_.Target} else {$_.Name}}}
}