function rename {

<#
.SYNOPSIS
    Renames a file
.EXAMPLE
    PS> rename C:\temp\foo.txt C:\temp\bar.txt
#>

    param(
        [Parameter(Mandatory)]
        [string]$From,
        [Parameter(Mandatory)]
        [string]$To
    )
    Rename-Item -Path $From -NewName $To
}