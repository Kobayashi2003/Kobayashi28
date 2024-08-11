<#
    .SYNOPSIS
        Set the background color of the console window
    .PARAMETER Color
        The color to set
    .EXAMPLE
        PS> My-Set-Color -Color "Red"
#>

param (
    [Parameter(Mandatory=$true)]
    [ArgumentCompleter({ param (
        $commandName,
        $parameterName,
        $wordToComplete,
        $commandAst,
        $fakeBoundParameters )
        @(
            "Black"   , "DarkBlue", "DarkGreen", "DarkCyan",
            "DarkRed" , "DarkMagenta", "DarkYellow", "Gray",
            "DarkGray", "Blue"    , "Green"    , "Cyan",
            "Red"     , "Magenta" , "Yellow"   , "White"
        ) | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object { $_ } })]
    [string] $color
)

try {
    $host.ui.RawUI.BackgroundColor = $color
    Write-Host "Background color set to $color"
    exit 0 # sucess
} catch {
    Write-Host "Failed to set the background color" -ForegroundColor Red
    exit 1
}
