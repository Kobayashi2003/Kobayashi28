function My-Set-Color {
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