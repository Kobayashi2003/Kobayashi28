<#
.SYNOPSIS
    Initialize yazi
.NOTES
    https://yazi-rs.github.io/docs/installation/
#>

#region bat initialize
if (Get-Command 'yazi' -ErrorAction SilentlyContinue) {

    if ($IsLinux) {
        $yazi_config_dir = Join-Path $HOME -ChildPath ".config/yazi"
        $yazi_config_src = Join-Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "config/yazi"

        if (!(Test-Path $yazi_config_dir)) {
            New-Item -Path $yazi_config_dir -ItemType Directory -Force | Out-Null
        }

        # Create symbolic links for configuration files
        $config_files = @("yazi.toml", "keymap.toml", "theme.toml")
        foreach ($file in $config_files) {
            $src = Join-Path $yazi_config_src -ChildPath $file
            $dst = Join-Path $yazi_config_dir -ChildPath $file
            if (!(Test-Path $dst)) {
                & sudo ln -s $src $dst
            }
        }
    } else {
        $yazi_config_dir = Join-Path $env:APPDATA -ChildPath "yazi\config"
        $yazi_config_src = Join-Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "config\yazi"

        if (!(Test-Path $yazi_config_dir)) {
            New-Item -Path $yazi_config_dir -ItemType Directory -Force | Out-Null
        }

        # Create symbolic links for configuration files
        $config_files = @("yazi.toml", "keymap.toml", "theme.toml")
        foreach ($file in $config_files) {
            $src = Join-Path $yazi_config_src -ChildPath $file
            $dst = Join-Path $yazi_config_dir -ChildPath $file
            if (!(Test-Path $dst)) {
                & sudo New-Item -Path $dst -ItemType SymbolicLink -Value $src
            }
        }
    }

    if (Get-Command 'git' -ErrorAction SilentlyContinue) {
        $env:YAZI_FILE_ONE = "$env:GIT_INSTALL_ROOT\usr\bin\file.exe"
    }
}
#endregion