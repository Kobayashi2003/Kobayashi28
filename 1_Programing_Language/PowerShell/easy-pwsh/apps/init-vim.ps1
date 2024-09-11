<#
.SYNOPSIS
    Initialize Vim
.NOTES
    https://github.com/vim/vim
#>

if (Get-Command "vim" -ErrorAction SilentlyContinue) {
    if ($IsLinux) {
        $vim_conf = Join-Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "config\vim\.vimrc"
        $vim_conf_current_user = Join-Path $env:USERPROFILE -ChildPath ".vimrc"
    } else {
        $vim_conf = Join-Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "config\vim\_vimrc"
        $vim_conf_current_user = Join-Path $env:USERPROFILE -ChildPath "_vimrc"
    }

    if (!(Test-Path $vim_conf_current_user)) {
        if ($IsLinux) {
            & sudo ln -s $vim_conf $vim_conf_current_user
        } else {
            & sudo New-Item -Path $vim_conf_current_user -ItemType SymbolicLink -Value $vim_conf
        }
    }
}