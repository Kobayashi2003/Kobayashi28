function Set-PythonParams {
    $launchJsonPath = Join-Path $PSScriptRoot ".vscode\launch.json"
    $launchJson = Get-Content $launchJsonPath -Raw | ConvertFrom-Json

    $pythonConfig = $launchJson.configurations | Where-Object { $_.type -eq "debugpy" }
    if (-not $pythonConfig) {
        Write-Host "No Python configuration found in launch.json"
        return
    }

    $params = @(
        "Program Path",
        "Arguments",
        "Working Directory",
        "Console Type"
    )

    while ($true) {
        $choice = Show-Menu -Title "Set Python Parameters" -Options $params
        switch ($choice) {
            1 {
                $pythonConfig.program = Read-Host "Enter the program path (e.g., `${file})"
            }
            2 {
                $args = Read-Host "Enter arguments (space-separated)"
                $pythonConfig.args = $args -split " "
            }
            3 {
                $pythonConfig.cwd = Read-Host "Enter the working directory (e.g., `${fileDirname})"
            }
            4 {
                $consoleTypes = @("integratedTerminal", "externalTerminal", "internalConsole")
                $consoleChoice = Show-Menu -Title "Select Console Type" -Options $consoleTypes
                if ($consoleChoice -ge 1 -and $consoleChoice -le 3) {
                    $pythonConfig.console = $consoleTypes[$consoleChoice - 1]
                }
            }
            default { break }
        }
    }

    $launchJson | ConvertTo-Json -Depth 10 | Set-Content $launchJsonPath -Encoding UTF8
    Write-Host "Python parameters updated"
}

function Show-Menu {
    param (
        [string]$Title,
        [array]$Options
    )
    Write-Host "================ $Title ================"
    for ($i = 0; $i -lt $Options.Count; $i++) {
        Write-Host "$($i+1). $($Options[$i])"
    }
    Write-Host "Q. Quit"
    Write-Host "========================================"
    $choice = Read-Host "Enter your choice"
    return $choice
}

Set-PythonParams