function Set-PythonConsole {
    $launchJsonPath = Join-Path $PSScriptRoot ".vscode\launch.json"
    $launchJson = Get-Content $launchJsonPath -Raw | ConvertFrom-Json

    $pythonConfig = $launchJson.configurations | Where-Object { $_.type -eq "debugpy" }
    if (-not $pythonConfig) {
        Write-Host "No Python configuration found in launch.json"
        return
    }

    $consoleOptions = @(
        "integratedTerminal",
        "integratedConsole",
        "externalTerminal"
    )

    Write-Host "`nPython Console Settings:"
    $choice = Show-Menu -Title "Select Console Type for Python" -Options $consoleOptions

    switch ($choice) {
        1 { $selectedConsole = "integratedTerminal" }
        2 { $selectedConsole = "integratedConsole" }
        3 { $selectedConsole = "externalTerminal" }
        default {
            Write-Host "Invalid choice. No changes made."
            return
        }
    }

    foreach ($config in $pythonConfig) {
        if (-not ($config.PSObject.Properties.Name -contains "console")) {
            $config | Add-Member -NotePropertyName "console" -NotePropertyValue $selectedConsole -Force
        } else {
            $config.console = $selectedConsole
        }
    }

    $launchJson | ConvertTo-Json -Depth 10 | Set-Content $launchJsonPath -Encoding UTF8
    Write-Host "`nPython console setting updated to: $selectedConsole"
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
    Write-Host "========================================"
    $choice = Read-Host "Enter your choice"
    return [int]$choice
}

# Run the main function
Set-PythonConsole