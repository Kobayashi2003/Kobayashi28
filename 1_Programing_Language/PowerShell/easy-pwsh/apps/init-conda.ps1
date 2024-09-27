<#
.SYNOPSIS
    Initialize conda
.NOTES
    https://github.com/conda/conda
#>

#region conda initialize
if (Get-Command 'conda' -ErrorAction SilentlyContinue) {

    # (& { conda config --set changeps1 False })
    # (& { conda config --set auto_activate_base False })

    $conda_conf = Join-Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "config\conda\.condarc"
    $conda_conf_current_user = Join-Path $env:USERPROFILE -ChildPath ".condarc"

    if (!(Test-Path $conda_conf_current_user)) {
        & sudo New-Item -Path $conda_conf_current_user -ItemType SymbolicLink -Value $conda_conf
    }

    Invoke-Expression (& { (conda "shell.powershell" "hook") | Out-String })
}
#endregion