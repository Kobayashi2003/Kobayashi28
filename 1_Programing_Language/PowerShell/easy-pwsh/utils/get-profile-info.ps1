function Get-ProfileInfo {

<#
    .SYNOPSIS
        Get profile information
    .EXAMPLE
        Get-ProfileInfo
#>

    Get-Item -Path $PROFILE | Select-Object -Property * | Format-List -Property * | Write-Output
}

& Get-ProfileInfo