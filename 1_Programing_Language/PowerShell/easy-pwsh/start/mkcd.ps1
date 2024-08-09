function mkcd {
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

if ($MyInvocation.InvocationName -ne '.') {
    mkcd $args[0]
}