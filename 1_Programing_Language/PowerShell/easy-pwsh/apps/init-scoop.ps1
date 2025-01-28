<#
.SYNOPSIS
    Initialize Scoop, and install Scoop apps.
.NOTES
    https://github.com/lukesampson/scoop
#>

if (!(Get-Command "scoop" -ErrorAction SilentlyContinue)) {

    Write-Host "For the best experience, it is recommended to install Scoop." -ForegroundColor Yellow
    Write-Host "You can continue the installation or install Scoop manually, and then run this script again." -ForegroundColor Yellow
    $confirm = Read-Host -Prompt "Do you want to install Scoop? (y/N)"
    if ($confirm -ne "y" -and $confirm -ne "Y") { return }


    $env:SCOOP = Read-Host -Prompt "Enter the directory where you want to install Scoop (e.g. $env:USERPROFILE\scoop)"
    $env:SCOOP_GLOBAL = Read-Host -Prompt "Enter the directory where you want to install Scoop apps (e.g. $env:USERPROFILE\scoop\apps)"
    if (-not $env:SCOOP) { $env:SCOOP = "$env:USERPROFILE\scoop" }
    if (-not $env:SCOOP_GLOBAL) { $env:SCOOP_GLOBAL = "$env:USERPROFILE\scoop\apps" }
    while ($env:SCOOP_GLOBAL -eq $env:SCOOP) {
        Write-Host "The directory where you want to install Scoop apps cannot be the same as the directory where you want to install Scoop." -ForegroundColor Red
        $env:SCOOP_GLOBAL = Read-Host -Prompt "Enter the directory where you want to install Scoop apps (e.g. $env:USERPROFILE\scoop\apps)"
    }

    if (-not (Test-Path $env:SCOOP)) { New-Item -Path $env:SCOOP -ItemType Directory | Out-Null }
    if (-not (Test-Path $env:SCOOP_GLOBAL)) { New-Item -Path $env:SCOOP_GLOBAL -ItemType Directory | Out-Null }

    $admin_flg = (([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))

    if (-not (Test-Path "$PSScriptRoot\install-scoop.ps1")) {
        Write-Host "Downloading install-scoop.ps1..." -ForegroundColor Yellow
        $install_proxy = Read-Host -Prompt "Set the proxy (Press Enter if you don't want to set the proxy)"
        try {
            if ($install_proxy) {
                & irm get.scoop.sh -outfile $PSScriptRoot\install-scoop.ps1 -Proxy $install_proxy
            } else {
                & irm get.scoop.sh -outfile $PSScriptRoot\install-scoop.ps1
            }
            Write-Host "Downloaded install-scoop.ps1." -ForegroundColor Green
        } catch {
            Write-Error "Error: $($_.Exception.Message)"
            return
        }
    }

    if (Test-Path $PSScriptRoot\install-scoop.ps1) {
        Invoke-Expression "$PSScriptRoot\install-scoop.ps1 -ScoopDir $env:SCOOP -ScoopGlobalDir $env:SCOOP_GLOBAL $(if ($install_proxy) { '-Proxy $install_proxy' }) $(if ($admin_flg) { '-RunAsAdmin' })"
    } else {
        Write-Error "install-scoop.ps1 not found."
        return
    }

    if (-not (Get-Command scoop -ErrorAction SilentlyContinue)) {
        Write-Error "Scoop installation failed. Please try again."
        return
    }

    try {
        if ($admin_flg) {
            [Environment]::SetEnvironmentVariable('SCOOP', $env:SCOOP, 'Machine')
            [Environment]::SetEnvironmentVariable('SCOOP_GLOBAL', $env:SCOOP_GLOBAL, 'Machine')
        } else {
            [Environment]::SetEnvironmentVariable('SCOOP', $env:SCOOP, 'User')
            [Environment]::SetEnvironmentVariable('SCOOP_GLOBAL', $env:SCOOP_GLOBAL, 'User')
        }
    } catch {
        Write-Warning "Failed to set the SCOOP environment variable."
        Write-Host "Please add the SCOOP environment variable manually." -ForegroundColor Yellow
    }
    Write-Host "Scoop has been installed." -ForegroundColor Green

    Write-Host "Before initializing Scoop, you can set the proxy." -ForegroundColor Yellow
    Write-Host "If you don't want to set the proxy, just press Enter." -ForegroundColor Yellow
    $scoop_proxy = Read-Host -Prompt "Enter proxy address (e.g. noproxy)"
    if ($scoop_proxy) {
        & scoop config proxy $scoop_proxy
    }

    if (-not (Get-Command 'git' -ErrorAction SilentlyContinue)) {
        & scoop install git
    }

    if (Get-Command 'git' -ErrorAction SilentlyContinue) {
        $scoop_supported_buckets = @(& scoop bucket known)
        Write-Host "Available buckets:"
        for ($i = 0; $i -lt $scoop_supported_buckets.Length; $i++) {
            Write-Host "$i. " -NoNewline
            Write-Host "$($scoop_supported_buckets[$i])" -ForegroundColor Yellow
        }

        $buckets_to_add = @()
        $numbers = Read-Host -Prompt "Enter the numbers of buckets to add, separated by spaces"
        $numbers.Split(" ") | ForEach-Object { $buckets_to_add += $scoop_supported_buckets[$_] }
        foreach ($bucket in $buckets_to_add) {
            try {
                if (!(@(& scoop bucket list).Name -contains $bucket)) {
                    & scoop bucket add $bucket
                }
            } catch {
                Write-Host "Failed to add $bucket bucket." -ForegroundColor Red
                continue
            }
            Write-Host "Added $bucket bucket." -ForegroundColor Green
        }
    } else {
        Write-Warning 'Git not found. You could add the buckets by running `scoop bucket add <bucket>` in PowerShell.'
    }

    Write-Host "Updating Scoop." -ForegroundColor Yellow
    & scoop update

    if ($?) {
        Write-Host "Scoop has been initialized." -ForegroundColor Green
    } else {
        Write-Warning 'Scoop updating failed. You can run `scoop update` to update Scoop again.'
    }
}

function global:scoop-check-update {
    & scoop update

    ($scoop_apps_update = @(& scoop status | Where-Object { $_.'Latest Version' }).Name) *>$null

    foreach ($app in $scoop_apps_update) {
        if ($global:SCOOP_UPDATE_IGNORE -contains $app) {
            Write-Host "Ignored $app update." -ForegroundColor DarkYellow
            continue
        }
        Write-Host "Updating $app..." -ForegroundColor Yellow
        & scoop update $app
        Write-Host "Updated $app." -ForegroundColor Green
    }
}

function global:scoop-check-install {
    ($scoop_apps_installed = @(& scoop list).Name) *>$null

    foreach ($app in ($global:SCOOP_APPLICATION)) {
        if (-not ($scoop_apps_installed -contains $app)) {
            Write-Warning "$app is not found. Installing..."
            & scoop install $app
            Write-Host "Installed $app." -ForegroundColor Green
        } else {
            Write-Host "$app is already installed." -ForegroundColor Green
        }
    }
}

function global:scoop-check-failed {
    ($scoop_apps_failed = @(& scoop status | Where-Object {$_.INFO.ToString().contains('failed')}).Name) *>$null

    foreach ($app in $scoop_apps_failed) {
        try {
            Write-Host "$app failed to install. Uninstalling..." -ForegroundColor Red
            & scoop uninstall $app
        } catch {
            Write-Error "Failed to uninstall $app."
            continue
        }
        Write-Host "Uninstalled $app" -ForegroundColor Red
    }
}

function global:scoop-check {
    if ($global:SCOOP_CHECK_UPDATE) {
        try {
            Write-Host "⏳ (1/3) Checking scoop update..." -ForegroundColor Yellow
            scoop-check-update
            Write-Host "✅ Update check completed successfully." -ForegroundColor Green
        } catch {
            Write-Host "❌ Update check failed: $($_.Exception.Message)" -ForegroundColor Red
        }
    }

    if ($global:SCOOP_CHECK_INSTALL) {
        try {
            Write-Host "⏳ (2/3) Checking scoop installation..." -ForegroundColor Yellow
            scoop-check-install
            Write-Host "✅ Installation check completed successfully." -ForegroundColor Green
        } catch {
            Write-Host "❌ Installation check failed: $($_.Exception.Message)" -ForegroundColor Red
        }
    }

    if ($global:SCOOP_CHECK_FAILED) {
        try {
            Write-Host "⏳ (3/3) Checking scoop failed..." -ForegroundColor Yellow
            scoop-check-failed
            Write-Host "✅ Failed apps check completed successfully." -ForegroundColor Green
        } catch {
            Write-Host "❌ Failed apps check failed: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

scoop-check