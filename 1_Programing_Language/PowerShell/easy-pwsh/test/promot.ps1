##### -- Terminal Prompt -- #####

function prompt {
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

function prompt {
    # The at sign creates an array in case only one history item exists.
    $history = @(Get-History)
    if($history.Count -gt 0)
    {
        $lastItem = $history[$history.Count - 1]
        $lastId = $lastItem.Id
    }

    $nextCommand = $lastId + 1
    $currentDirectory = Get-Location
    "PS: $nextCommand $currentDirectory >"
}

function prompt {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal] $identity
    $adminRole = [Security.Principal.WindowsBuiltInRole]::Administrator

    $(if (Test-Path variable:/PSDebugContext) { '[DBG]: ' }
        elseif($principal.IsInRole($adminRole)) { "[ADMIN]: " }
        else { '' }
    ) + 'PS ' + $(Get-Location) +
        $(if ($NestedPromptLevel -ge 1) { '>>' }) + '> '
}

function prompt {
    $color = Get-Random -Min 1 -Max 16
    Write-Host ("PS " + $(Get-Location) +">") -NoNewLine -ForegroundColor $Color
    return " "
}