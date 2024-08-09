function Get-CmdletAlias {
    param (
        [Parameter(Mandatory = $true)]
        [string] $cmd
    )

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
}
