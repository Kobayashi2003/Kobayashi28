<#
.SYNOPSIS
    Initialize ripgrep
.NOTES
    https://github.com/BurntSushi/ripgrep
#>

if (Get-Command 'rg' -ErrorAction SilentlyContinue) {
    Set-Alias -Name grep -Value rg -Option AllScope -Scope Global -Force
}