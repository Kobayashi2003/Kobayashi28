<#
.SYNOPSIS
    Initialize yazi
.NOTES
    https://yazi-rs.github.io/docs/installation/
#>

#region bat initialize
if (Get-Command 'yazi' -ErrorAction SilentlyContinue) {
    if (Get-Command 'git' -ErrorAction SilentlyContinue) {
        $env:BAT_CONFIG_DIR = "$env:GIT_INSTALL_ROOT\usr\bin\file.exe"
    }
}
#endregion