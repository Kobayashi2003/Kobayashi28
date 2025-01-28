function head {

<#
    .SYNOPSIS
        Get the first n lines of a text file.
    .PARAMETER Lines
        output the first N lines (default: 10)
    .PARAMETER Path
        path to the text file
    .EXAMPLE
        PS> head c:\server.log
    .EXAMPLE
        PS> head -n 20 c:\server.log
#>

    [CmdletBinding()]
    [OutputType('System.String')]
    Param(
        [parameter(Mandatory=$false)]
        [Alias("n")]
        [Int] $Lines = 10,

        [parameter(Mandatory=$true, Position=5)]
        [ValidateNotNullOrEmpty()]
        [IO.FileInfo] $Path
    )

    Get-Content -Path $Path -Head $Lines
}