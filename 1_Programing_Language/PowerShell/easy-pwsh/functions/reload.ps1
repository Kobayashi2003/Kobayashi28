function Reload-Script {

<#
    .SYNOPSIS
        Reloads the current script
    .EXAMPLE
        Reload-Script
#>

    Get-Process -Id $PID | Select-Object -ExpandProperty Path | ForEach-Object { Invoke-Command { & "$_" } -NoNewScope }
    exit
}

Set-Alias -Name 'reload' -Value 'Reload-Script'