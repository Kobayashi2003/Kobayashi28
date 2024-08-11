<#
.SYNOPSIS
    Initialize zoxide
.NOTES
    https://github.com/ajeetdsouza/zoxide
#>

#region zoxide initialize
if (Get-Command 'zoxide' -ErrorAction SilentlyContinue) {
    Invoke-Expression (& { (zoxide init powershell | Out-String) })
    Set-Alias -Name cd -Value z -Option AllScope -Scope Global -Force
}
#endregion