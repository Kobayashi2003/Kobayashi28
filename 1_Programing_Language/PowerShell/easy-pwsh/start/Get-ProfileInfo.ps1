function Get-ProfileInfo {
    Get-Item -Path $PROFILE | Select-Object -Property * | Format-List -Property * | Write-Output
}

if ($MyInvocation.InvocationName -ne '.') {
    Get-ProfileInfo
}