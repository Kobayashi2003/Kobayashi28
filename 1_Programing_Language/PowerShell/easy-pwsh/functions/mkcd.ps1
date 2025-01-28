function mkcd {

<#
    .SYNOPSIS
        Creates a new directory and changes to it
    .DESCRIPTION
        Creates a new directory and changes to it
    .PARAMETER Path
        The path to the directory
    .EXAMPLE
        mkcd C:\tem
#>

    param(
        [Parameter(Mandatory)]
        [string]$Path
    )
    try {
        if (Test-Path $Path) {
            Set-Location $Path
        } else {
            New-Item -ItemType Directory -Path $Path
            Set-Location $Path
        }
    } catch {
        Write-Host "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    }
}