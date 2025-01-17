Script: *set-foreground-color.ps1*
========================

Set the color of the console window

Parameters
----------
```powershell
D:\Program\code\1_Programing_Language\PowerShell\easy-pwsh\utils\set-foreground-color.ps1 [-color] <String> [<CommonPar
ameters>]

是否必需?                    True
位置?                        1
默认值
是否接受管道输入?            false
是否接受通配符?              False

[<CommonParameters>]
    This script supports the common parameters: Verbose, Debug, ErrorAction, ErrorVariable, WarningAction, 
    WarningVariable, OutBuffer, PipelineVariable, and OutVariable.
```

Example
-------
```powershell
PS> My-Set-Color -Color "Red"

```

Script Content
--------------
```powershell
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

try {
    $host.ui.RawUI.BackgroundColor = $color
    Write-Host "Background color set to $color"
    exit 0 # sucess
} catch {
    Write-Host "Failed to set the background color" -ForegroundColor Red
    exit 1
}
```

*(generated by convert-ps2md.ps1 using the comment-based help of set-foreground-color.ps1 as of 08/13/2024 16:11:37)*
