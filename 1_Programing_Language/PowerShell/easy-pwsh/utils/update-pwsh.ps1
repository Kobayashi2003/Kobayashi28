<#
.SYNOPSIS
    Updates PowerShell to the latest version.
.DESCRIPTION
    This PowerShell script checks for the latest version of PowerShell, downloads and installs it if a newer version is available.
.EXAMPLE
    PS> ./update-pwsh.ps1
    Current PowerShell version: 7.4.6
    Latest PowerShell version: 7.5.0
    A new version is available. Downloading...
    Installing new version...
    PowerShell has been updated to version 7.5.0
    Please restart your PowerShell session to use the new version.
.LINK
    https://github.com/PowerShell/PowerShell/releases
.NOTES
    Author: KOBAYASHI
#>

function Compare-Versions($current, $latest) {
    $currentVersion = [Version]$current
    $latestVersion = [Version]$latest
    return $currentVersion -lt $latestVersion
}

try {
    $currentVersion = $PSVersionTable.PSVersion.ToString()
    "Current PowerShell version: $currentVersion"

    $releaseUrl = "https://api.github.com/repos/PowerShell/PowerShell/releases/latest"
    $latestRelease = Invoke-RestMethod -Uri $releaseUrl

    $latestVersion = $latestRelease.tag_name -replace '^v', ''
    "Latest PowerShell version: $latestVersion"

    # if (Compare-Versions $currentVersion $latestVersion) {
    #     Write-Host "Updating PowerShell..." -ForegroundColor Yellow
    #     Start-Process powershell.exe -ArgumentList "-NoProfile -Command winget upgrade Microsoft.PowerShell --accept-source-agreements --accept-package-agreements" -Wait -NoNewWindow
    #     Write-Host "PowerShell has been updated. Please restart your shell to reflect changes" -ForegroundColor Magenta
    # }

    if (Compare-Versions $currentVersion $latestVersion) {
        "A new version is available. Downloading..."

        $asset = $latestRelease.assets | Where-Object { $_.name -like "*win-x64.msi" }

        if ($asset) {
            $downloadUrl = $asset.browser_download_url
            $installerPath = Join-Path $env:TEMP "PowerShell-$latestVersion-win-x64.msi"

            Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath

            "Download complete. Starting installer in a new process..."

            # Create a new process start info
            $startInfo = New-Object System.Diagnostics.ProcessStartInfo
            $startInfo.FileName = "msiexec.exe"
            $startInfo.Arguments = "/i `"$installerPath`""
            $startInfo.UseShellExecute = $true

            # Start the new process
            [System.Diagnostics.Process]::Start($startInfo)

            "Please follow the installation wizard to complete the update."
            "After installation, please restart your PowerShell session to use the new version."
        } else {
            throw "Couldn't find the installer for the latest version."
        }
    } else {
        "You are already running the latest version of PowerShell."
    }

    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}