<#
.SYNOPSIS
    Initialize lf
.NOTES
    https://github.com/gokcehan/lf
#>

if (Get-Command "lf" -ErrorAction SilentlyContinue) {

    $lf_config = (Join-Path $global:current_script_directory -ChildPath "config\lf\lfrc").replace('\','/')
    $lf_previewer = (Join-Path $global:current_script_directory -ChildPath "config\lf\lfpreview.cmd").replace('\','/')

    $env:LF_CONFIG_FILE = $lf_config
    $env:LF_PREVIEWER = $lf_previewer

    function global:lfc { & lf -config $env:LF_CONFIG_FILE $args }
}