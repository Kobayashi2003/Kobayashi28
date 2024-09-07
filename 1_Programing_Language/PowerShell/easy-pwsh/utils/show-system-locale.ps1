<#
.SYNOPSIS
    Show the system locale
#>

try {
    $locale = Get-WinSystemLocale
    Write-Host "Current system locale is $locale"
    exit 0 # sucess
} catch {
    Write-Host "Failed to get system locale" -ForegroundColor Red
    exit 1
}