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

    if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
        Write-Host "Please run this script as an administrator." -ForegroundColor Red
        return
    }

    $scoopDir = Read-Host -Prompt "Enter the directory where you want to install Scoop (e.g. $env:USERPROFILE\scoop)"
    if (-not $scoopDir) { $scoopDir = "$env:USERPROFILE\scoop" }
    if (-not (Test-Path $scoopDir)) {
        New-Item -Path $scoopDir -ItemType Directory | Out-Null
    }

    $env:SCOOP_HOME = $scoopDir
    [Environment]::SetEnvironmentVariable('SCOOP_HOME', $scoopDir, 'User')
    Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
    if (-not (Get-Command scoop -ErrorAction SilentlyContinue)) {
        Write-Host "Scoop installation failed. Please try again." -ForegroundColor Red
        return
    }

    Write-Host "Before initializing Scoop, you can set the proxy." -ForegroundColor Yellow
    Write-Host "If you don't want to set the proxy, just press Enter." -ForegroundColor Yellow
    $scoop_proxy = Read-Host -Prompt "Enter proxy address (e.g. noproxy)"
    if ($scoop_proxy) {
        & scoop config proxy $scoop_proxy }

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

    Write-Host "Updating Scoop." -ForegroundColor Yellow
    & scoop update

    if ($?) {
        Write-Host "Scoop has been initialized." -ForegroundColor Green
    } else {
        Write-Host "Scoop updating failed." -ForegroundColor Red
        Write-Host 'You can run `scoop update` to update Scoop again.' -ForegroundColor Red
    }
}

($scoop_apps_installed = @(& scoop list).Name) *>$null
foreach ($app in $global:scoop_apps) {
    if (-not $scoop_apps_installed -contains $app) {
        try {
            Write-Host "Installing $app." -ForegroundColor Yellow
            & scoop install $app
        } catch {
            Write-Host "Failed to install $app." -ForegroundColor Red
            continue
        }
        Write-Host "Installed $app." -ForegroundColor Green
    }
}