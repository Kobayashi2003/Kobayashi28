function My-Set-Color {

<#
    .SYNOPSIS
        Set the color of the console window
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

    $default_color = 'White'

    try {
        $host.ui.RawUI.ForegroundColor = $color
    } catch {
        $host.ui.RawUI.ForegroundColor = $default_color
        throw "The color is not ligal, the color is set to default."
    }
}