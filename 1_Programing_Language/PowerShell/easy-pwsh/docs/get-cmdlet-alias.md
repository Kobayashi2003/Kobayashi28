Script: *get-cmdlet-alias.ps1*
========================

Get the aliases of a cmdlet

Parameters
----------
```powershell
D:\Program\code\1_Programing_Language\PowerShell\easy-pwsh\utils\get-cmdlet-alias.ps1 [-cmd] <String> [<CommonParameter
s>]

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
PS> Get-CmdletAlias Get-ChildItem

```

Example
-------
```powershell
PS> Get-CmdletAlias ls

```

Script Content
--------------
```powershell
<#
    .SYNOPSIS
        Get the aliases of a cmdlet
    .PARAMETER cmd
        The name of the cmdlet or alias
    .EXAMPLE
        PS> Get-CmdletAlias Get-ChildItem
    .EXAMPLE
        PS> Get-CmdletAlias ls
#>

param (
    [Parameter(Mandatory = $true)]
    [string] $cmd
)

try {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Host "Command not found: $cmd"
        return
    }

    if (Get-Alias $cmd -ErrorAction SilentlyContinue) {
        Get-Alias $cmd | Format-Table -Property Definition, Name -AutoSize
    } else {
        Get-Alias | Where-Object -FilterScript { $_.Definition -eq $cmd } |
            Format-Table -Property Definition, Name -AutoSize
    }

    exit 0 # sucess

} catch {
    Write-Host "Failed to get cmdlet alias: $cmd"
    exit 1
}
```

*(generated by convert-ps2md.ps1 using the comment-based help of get-cmdlet-alias.ps1 as of 08/13/2024 16:11:35)*
