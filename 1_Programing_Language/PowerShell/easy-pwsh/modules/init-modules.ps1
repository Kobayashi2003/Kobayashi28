function global:check-module {
<#
.SYNOPSIS
    Check if module is installed

.PARAMETER name
    Name of the module
.PARAMETER version
    Version of the module

.EXAMPLE
    check-module -name Terminal-Icons
.EXAMPLE
    check-module -name PSReadLine -version '==2.3.4'
    check-module -name PSReadLine -version '>=2.0.0'
    check-module -name PSReadLine -version '<=2.3.4'
    check-module -name PSReadLine -version '<2.3.4'
    check-module -name PSReadLine -version '>2.3.4'

.OUTPUTS
    if valid, an a valiable version of the module [string]
    if invalid, return $null
#>

    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [string] $name,
        [Parameter(Mandatory = $false)]
        [ValidatePattern('(^(==|>=|<=|>|<)([0-9]+\.[0-9]+\.[0-9]+)$)|(^(latest)$)')]
        [string] $version = "latest"
    )

    $installed_versions = @(
        Get-Module -ListAvailable |
        Where-Object { $_.Name -eq $name } |
        Sort-Object -Property Version -Descending |
        foreach { $_.Version.ToString() })

    if ($version -eq "latest") {
        if ($installed_versions.Length -gt 0) {
            return $installed_versions[0]
        }
        try {
            Write-Host "Module $name not found. Installing..." -ForegroundColor Yellow
            $new_version = (Find-Module -Name $name).Version
            if ($new_version -eq $null) {
                throw "Unable to find latest version of $name module"
            }
            sudo Install-Module -Name $name -RequiredVersion $new_version -Force
        } catch {
            Write-Host "Failed to install $name module: $_" -ForegroundColor Red
            return  $null
        }
        return $new_version
    }

    $version_raw = $version.replace('=', '').replace('>', '').replace('<', '')

    if (-not ($version_raw -match '^[0-9]+\.[0-9]+\.[0-9]+$')) {
        throw "Invalid version format:$version_raw"
    }

    if ($version.contains('>')) {
        foreach ($v in $installed_versions) {
            if ($v -gt $version_raw) {
                return $v
            } elseif (($v -eq $version_raw) -and ($version.contains('='))) {
                return $v
            }
        }
        try {
            Write-Warning "Unable to find a version satisfying $version. Installing..."
            $new_version = (Find-Module -Name $name -MinimumVersion $version_raw).Version
            if ($new_version -eq $null) {
                throw "Unable to find latest version of $name module"
            }
            sudo Install-Module -Name $name -RequiredVersion $new_version -Force
        } catch {
            Write-Host "Failed to install $name module: $_" -ForegroundColor Red
            return  $null
        }
        return $new_version
    }

    if ($_version.contains('<')) {
        foreach ($v in $installed_versions) {
            if ($v -lt $version_raw) {
                return $v
            } elseif (($v -eq $version_raw) -and ($version.contains('='))) {
                return $v
            }
        }
        try {
            Write-Warning "Unable to find a version satisfying $version. Installing..."
            $new_version = (Find-Module -Name $name -MaximumVersion $version_raw).Version
            if ($new_version -eq $null) {
                throw "Unable to find latest version of $name module"
            }
            sudo Install-Module -Name $name -RequiredVersion $new_version -Force
        } catch {
            Write-Host "Failed to install $name module: $_" -ForegroundColor Red
            return  $null
        }
        return $new_version
    }

    if ($_version.contains('==')) {
        if ($installed_versions -contains $version_raw) {
            return $version_raw
        }
        try {
            Write-Warning "Unable to find a version satisfying $version. Installing..."
            $new_version = (Find-Module -Name $name -RequiredVersion $version_raw).Version
            if ($new_version -eq $null) {
                throw "Unable to find latest version of $name module"
            }
            sudo Install-Module -Name $name -RequiredVersion $new_version -Force
        } catch {
            Write-Host "Failed to install $name module: $_" -ForegroundColor Red
            return  $null
        }
    }

    throw "Unexpected Exception"
}


function global:check-imported {
<#
.SYNOPSIS
    Check if module is imported
.PARAMETER name
    Name of the module
.PARAMETER imported_list
    List of modules imported
.EXAMPLE
    check-imported -name Terminal-Icons
.EXAMPLE
    check-imported -name Terminal-Icons -modules_imported $global:imported_list
#>

    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [string] $name,

        [Parameter(Mandatory = $false)]
        [array] $imported_list
    )

    if (-not $imported_list) {
        $imported_list = (Get-Module -ListAvailable -Name $name).Name
    }

    if ($imported_list -notcontains $name) {
        Write-Host "module" -ForegroundColor Red -NoNewline
        Write-Host " $name " -ForegroundColor Yellow -NoNewline
        Write-Host "is not imported" -ForegroundColor Red
        return $false
    }

    if ($global:show_imported) {
        Write-Host "module" -ForegroundColor Green -NoNewline
        Write-Host " $name " -ForegroundColor Yellow -NoNewline
        Write-Host "is imported" -ForegroundColor Green
    }
    return $true
}


$global:modules_imported = @()

# $global:modules is a map
# key:   module name
# value: module version

$global:modules.GetEnumerator() |
    ForEach-Object { if ((-not $global:modules_check) -or (check-module -Name $_.Key -Version $_.Value)) {
        try {
            if ($_.Value -eq "latest") {
                Import-Module -Name $_.Key
            } else {
                Import-Module -Name $_.Key -RequiredVersion $_.Value.Replace('=','').Replace('>','').Replace('<','')
            }
            $global:modules_imported += $_.Key } catch {}
        }
    }

$global:modules_imported | ForEach-Object {
    $private:modulename = $_
    $private:filename = "module.$modulename.ps1"
    $private:dirname = Join-Path -Path $global:current_script_directory -ChildPath "modules"
    if (-not (Test-Path (Join-Path -Path $dirname -ChildPath $filename))) {
        New-Item -Path $dirname -Name $filename -ItemType File }
    if (check-imported $modulename $global:modules_imported) {
        & (Join-Path -Path $dirname -ChildPath $filename) }
}


# TIPS: If you do not want to download modules by yourself, you can try to import the modules in the $current_script_directory/downloads/Modules