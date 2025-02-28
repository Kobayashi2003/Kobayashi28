#Requires -RunAsAdministrator
<#
.DESCRIPTION
Auto-restart network authentication client when internet connection is lost or when the client is not running properly

.PARAMETER TestAddress
The address to test network connectivity. Default is "8.8.8.8".

.PARAMETER CheckInterval
The interval in seconds between each check. Default is 600 seconds (10 minutes).

.PARAMETER InstallPath
The installation path of the 8021x client. If not provided, the script will try to use the default shortcut or prompt for the path.
#>

param(
    [string]$TestAddress = "8.8.8.8",
    [int]$CheckInterval = 600,
    [string]$InstallPath = ""
)

# Global variables
$clientShortcut = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\中山大学认证客户端\中山大学认证客户端.lnk"
$useShortcut = $true
$clientExePath = ""

# Function to validate and set the client executable path
function Set-ClientExePath {
    param([string]$Path)

    $exePath = Join-Path -Path $Path -ChildPath "RuijieSupplicant.exe"
    if (Test-Path $exePath) {
        $script:clientExePath = $exePath
        $script:useShortcut = $false
        Write-Host "Found RuijieSupplicant.exe at: $clientExePath" -ForegroundColor Green
        return $true
    } else {
        Write-Host "RuijieSupplicant.exe not found at: $exePath." -ForegroundColor Red
        return $false
    }
}

# Check if InstallPath is provided
if ($InstallPath -ne "") {
    if (-not (Set-ClientExePath $InstallPath)) {
        Write-Host "Invalid installation path provided. Exiting script." -ForegroundColor Red
        exit
    }
}
# Check if the default shortcut exists
elseif (-not (Test-Path $clientShortcut)) {
    $useShortcut = $false
    Write-Host "Default shortcut not found: $clientShortcut" -ForegroundColor Yellow
    Write-Host "Please enter the installation path of the 8021x client (e.g., C:\Program Files\RuijieSupplicant):" -ForegroundColor Cyan

    do {
        $installPath = Read-Host "Installation path"
    } while (-not (Set-ClientExePath $installPath))
}

function Test-NetworkConnection {
    param(
        [string]$Address = $TestAddress,
        [int]$RetryCount = 3,
        [int]$Timeout = 1
    )

    $success = 0
    for ($i = 0; $i -lt $RetryCount; $i++) {
        if (Test-Connection -TargetName $Address -Count 1 -TimeoutSeconds $Timeout -Quiet) {
            $success++
        }
        Start-Sleep -Seconds 1
    }
    return ($success -eq 0)  # Returns True if all attempts failed
}

function Test-8021xClient {
    # Check if the 8021x process is running
    $process = Get-Process -Name "8021x" -ErrorAction SilentlyContinue

    if (-not $process) {
        Write-Host "[$(Get-Date)] 8021x client is not running" -ForegroundColor Yellow
        return $false
    }

    # Additional checks could be added here to verify the client is functioning correctly
    # For example, checking if the process is responding or if specific services are running

    return $true
}

function Restart-8021xClient {
    Write-Host "[$(Get-Date)] Restarting 8021x client..." -ForegroundColor Yellow

    # Terminate existing process if it exists
    if (Get-Process -Name "8021x" -ErrorAction SilentlyContinue) {
        Stop-Process -Name "8021x" -Force
        Start-Sleep -Seconds 2
    }

    # Launch new client instance based on what's available
    if ($useShortcut) {
        Start-Process -FilePath $clientShortcut
        Write-Host "[$(Get-Date)] 8021x client started using shortcut" -ForegroundColor Green
    } else {
        # Change to the installation directory and execute the program
        $installDir = Split-Path -Parent $clientExePath
        Push-Location $installDir
        Start-Process -FilePath $clientExePath
        Pop-Location
        Write-Host "[$(Get-Date)] 8021x client started using direct executable: $clientExePath" -ForegroundColor Green
    }

    # Allow time for client initialization
    Start-Sleep -Seconds 10
}

# Display startup information
Write-Host "Network monitoring started with the following settings:" -ForegroundColor Cyan
Write-Host "  - Test address: $TestAddress" -ForegroundColor Cyan
Write-Host "  - Check interval: $CheckInterval seconds" -ForegroundColor Cyan
if ($useShortcut) {
    Write-Host "  - Using client shortcut: $clientShortcut" -ForegroundColor Cyan
} else {
    Write-Host "  - Using client executable: $clientExePath" -ForegroundColor Cyan
}
Write-Host "Press Ctrl+C to stop the script" -ForegroundColor Cyan
Write-Host "-----------------------------------------------------" -ForegroundColor Cyan

# Main monitoring loop
while ($true) {
    $networkFailed = Test-NetworkConnection
    $clientRunning = Test-8021xClient

    # Check both conditions in parallel
    if ($networkFailed) {
        Write-Host "[$(Get-Date)] Network connection lost - Restarting client..." -ForegroundColor Red
        Restart-8021xClient

        # Allow more time for network to reconnect
        Start-Sleep -Seconds 30
    }
    elseif (-not $clientRunning) {
        Write-Host "[$(Get-Date)] Client isn't running - Restarting client..." -ForegroundColor Red
        Restart-8021xClient
    }
    else {
        Write-Host "[$(Get-Date)] Network connection active and 8021x client running" -ForegroundColor Green
    }

    # Check interval (user-defined)
    Start-Sleep -Seconds $CheckInterval
}