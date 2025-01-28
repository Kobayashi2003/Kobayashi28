function which {

<#
.SYNOPSIS
    Returns the path to an executable
.EXAMPLE
    PS> which git
#>

    (Get-Command $Args[0] -ErrorAction SilentlyContinue).Source
}