# Function to display a menu and get user choice
function Show-Menu {
    param (
        [string]$Title,
        [array]$Options
    )
    Clear-Host
    Write-Host "================ $Title ================"
    for ($i = 0; $i -lt $Options.Count; $i++) {
        Write-Host "$($i+1). $($Options[$i])"
    }
    Write-Host "Q. Quit"
    Write-Host "========================================"
    $choice = Read-Host "Enter your choice"
    return $choice
}

# Function to edit a configuration
function Edit-Configuration {
    param (
        [PSCustomObject]$Config
    )
    $properties = $Config.PSObject.Properties | Where-Object { $_.MemberType -eq "NoteProperty" }
    while ($true) {
        $propertyNames = $properties | ForEach-Object { $_.Name }
        $choice = Show-Menu -Title "Edit Configuration: $($Config.name)" -Options $propertyNames
        if ($choice -eq "Q") { break }
        $index = [int]$choice - 1
        if ($index -ge 0 -and $index -lt $propertyNames.Count) {
            $propName = $propertyNames[$index]
            $newValue = Read-Host "Enter new value for $propName (current: $($Config.$propName))"
            $Config.$propName = $newValue
        }
    }
}

# Function to add a new configuration
function Add-NewConfiguration {
    $newConfig = [PSCustomObject]@{
        name = Read-Host "Enter configuration name"
        type = Read-Host "Enter configuration type"
        request = Read-Host "Enter request type (e.g., launch)"
    }
    while ($true) {
        $addMore = Read-Host "Add another property? (Y/N)"
        if ($addMore -ne "Y") { break }
        $propName = Read-Host "Enter property name"
        $propValue = Read-Host "Enter property value"
        $newConfig | Add-Member -NotePropertyName $propName -NotePropertyValue $propValue
    }
    return $newConfig
}

# Main script
$launchJsonPath = Join-Path $PSScriptRoot ".vscode\launch.json"
$launchJson = Get-Content $launchJsonPath -Raw | ConvertFrom-Json
$configurations = $launchJson.configurations

while ($true) {
    $mainOptions = @("View Configurations", "Edit Configuration", "Add Configuration", "Remove Configuration", "Save Changes")
    $choice = Show-Menu -Title "Launch.json Manager" -Options $mainOptions

    switch ($choice) {
        "1" {  # View Configurations
            foreach ($config in $configurations) {
                Write-Host "`n$($config.name):"
                $config | ConvertTo-Json -Depth 5
            }
            Read-Host "Press Enter to continue"
        }
        "2" {  # Edit Configuration
            $configNames = $configurations | ForEach-Object { $_.name }
            $editChoice = Show-Menu -Title "Select Configuration to Edit" -Options $configNames
            if ($editChoice -ne "Q") {
                $index = [int]$editChoice - 1
                if ($index -ge 0 -and $index -lt $configurations.Count) {
                    Edit-Configuration -Config $configurations[$index]
                }
            }
        }
        "3" {  # Add Configuration
            $newConfig = Add-NewConfiguration
            $configurations += $newConfig
        }
        "4" {  # Remove Configuration
            $configNames = $configurations | ForEach-Object { $_.name }
            $removeChoice = Show-Menu -Title "Select Configuration to Remove" -Options $configNames
            if ($removeChoice -ne "Q") {
                $index = [int]$removeChoice - 1
                if ($index -ge 0 -and $index -lt $configurations.Count) {
                    $configurations = $configurations | Where-Object { $_ -ne $configurations[$index] }
                }
            }
        }
        "5" {  # Save Changes
            $launchJson.configurations = $configurations
            $launchJson | ConvertTo-Json -Depth 10 | Set-Content $launchJsonPath -Encoding UTF8
            Write-Host "Changes saved to launch.json"
            Read-Host "Press Enter to continue"
        }
        "Q" {
            $savePrompt = Read-Host "Save changes before exiting? (Y/N)"
            if ($savePrompt -eq "Y") {
                $launchJson.configurations = $configurations
                $launchJson | ConvertTo-Json -Depth 10 | Set-Content $launchJsonPath -Encoding UTF8
                Write-Host "Changes saved to launch.json"
            }
            exit
        }
    }
}