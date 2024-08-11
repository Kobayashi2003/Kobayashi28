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
