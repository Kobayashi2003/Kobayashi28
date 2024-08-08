function Set-BackgroundColor {
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

    $default_background_color = 'DarkBlue'

    try {
        $host.ui.RawUI.BackgroundColor = $color
    } catch {
        $host.ui.RawUI.BackgroundColor = $default_background_color
        throw "The background color is not ligal, the background color is set to default."
    }
}