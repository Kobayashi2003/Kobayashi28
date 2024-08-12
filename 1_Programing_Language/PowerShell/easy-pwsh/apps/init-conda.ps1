<#
.SYNOPSIS
    Initialize conda
.NOTES
    https://github.com/conda/conda
#>

#region conda initialize
if (Get-Command 'conda' -ErrorAction SilentlyContinue) {
    # (& { conda config --set changeps1 False })
    (& { conda config --set auto_activate_base False })
    Invoke-Expression (& { (conda "shell.powershell" "hook") | Out-String })
}
#endregion