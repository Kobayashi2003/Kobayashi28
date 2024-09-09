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

    if (([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
        Write-Error "This scirpt can not be run as an administrator."
        return
    }

    if (-not (Test-Path "$PSScriptRoot\install-scoop.ps1")) {
        Write-Host "Downloading install-scoop.ps1..." -ForegroundColor Yellow
        $install_proxy = Read-Host -Prompt "Set the proxy (Press Enter if you don't want to set the proxy)"
        try {
            if ($install_proxy) {
                & irm get.scooop.sh -outfile 'install-scoop.ps1' -proxy $install_proxy
            } else {
                & irm get.scooop.sh -outfile 'install-scoop.ps1'
            }
            Write-Host "Downloaded install-scoop.ps1." -ForegroundColor Green
        } catch {
            Write-Error "Error: $($_.Exception.Message)"
            return
        }
    }

    if (Test-Path "$PSScriptRoot\install-scoop.ps1") {
        if ($install_proxy) {
            . $PSScriptRoot\install-scoop.ps1 -ScoopDir $env:SCOOP -ScoopGlobalDir $env:SCOOP_GLOBAL -Proxy $install_proxy
        } else {
            . $PSScriptRoot\install-scoop.ps1 -ScoopDir $env:SCOOP -ScoopGlobalDir $env:SCOOP_GLOBAL -NoProxy
        }
    } else {
        [Environment]::SetEnvironmentVariable('SCOOP_GLOBAL', $env:SCOOP_GLOBAL, 'Machine')
        if ($install_proxy) {
            & irm get.scoop.sh -Proxy $install_proxy | iex
        } else {
            & irm get.scoop.sh | iex
        }
    }

    if (-not (Get-Command scoop -ErrorAction SilentlyContinue)) {
        Write-Error "Scoop installation failed. Please try again."
        return
    }

    # TODO: if install success, i should add the scoop path to the system environment variables

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

($scoop_apps_installed = @(& scoop list).Name) *>$null
foreach ($app in ($global:scoop_apps + $global:scoop_extras)) {
    if (-not ($scoop_apps_installed -contains $app)) {
        try {
            Write-Warning "$app is not installed. Installing..."
            & scoop install $app
        } catch {
            Write-Error "Failed to install $app."
            & scoop uninstall $app
            continue
        }
        Write-Host "Installed $app." -ForegroundColor Green
    }
}
