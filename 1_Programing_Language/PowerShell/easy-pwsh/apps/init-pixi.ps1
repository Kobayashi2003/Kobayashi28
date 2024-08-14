<#
.SYNOPSIS
    Initialize pixi
.NOTES
    https://github.com/prefix-dev/pixi
#>

#region pixi initialize
if (Get-Command "pixi" -ErrorAction SilentlyContinue) {
    (& pixi completion --shell powershell) | Out-String | Invoke-Expression
} else {
    Write-Host "pixi not installed. Installing..." -ForegroundColor Yellow
    try {
        iwr -useb https://pixi.sh/install.ps1 | iex
        Write-Host "pixi installed." -ForegroundColor Green
        (& pixi completion --shell powershell) | Out-String | Invoke-Expression
    } catch {
        Write-Host "Failed to install pixi." -ForegroundColor Red
    }
}
#endregion
