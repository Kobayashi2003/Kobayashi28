<#
.SYNOPSIS
    Initialize bat
.NOTES
    https://github.com/sharkdp/bat
#>

#region bat initialize
if (Get-Command 'bat' -ErrorAction SilentlyContinue) {
    Set-Alias -Name cat -Value bat -Option AllScope -Scope Global -Force
}
#endregion