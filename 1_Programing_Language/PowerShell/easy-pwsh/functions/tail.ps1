function tail {

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

    Get-Content -Path $Path -Tail $Lines -Wait:$Follow
}