##### -- Terminal Prompt -- #####

function Prompt {
    $lst_cmd_state = $?
    $esc = $([char]27)
    if (-not $lst_cmd_state) {
        $time = "$esc[1;31m$esc[1;4m" + (Get-Date -Format "HH:mm:ss") + "$esc[0m " # red and italic
    } else {
        $time = "$esc[1;32m$esc[1;4m" + (Get-Date -Format "HH:mm:ss") + "$esc[0m " # green and italic
    }
    $path = ($PWD.Path).Replace($env:USERPROFILE, "~") + ' ' # replace the user profile with ~
    if ($env:CONDA_DEFAULT_ENV) {
        $conda_env = "$esc[1;33m$esc[1;4m($env:CONDA_DEFAULT_ENV)$esc[0m " # yellow and italic
    } else {
        $conda_env = ""
    }
    return $conda_env + $time + $path + "> "
}