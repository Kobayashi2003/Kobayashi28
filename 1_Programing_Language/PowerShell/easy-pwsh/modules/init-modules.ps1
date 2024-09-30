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

    if ($version.contains('<')) {
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

    if ($version.contains('==')) {
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

    return $true
}


function global:init-modules {
<#
.SYNOPSIS
    Import, Check, Init and Show Moudles
#>

    $global:MODULES.GetEnumerator() | Where-Object { (-not $global:CHECK_MODULES) -or (check-module -Name $_.Key -Version $_.Value) } | ForEach-Object {
        if ($_.Value -eq "latest") {
            Import-Module -Name $_.Key
        } else {
            Import-Module -Name $_.Key -RequiredVersion $_.Value.Replace('=','').Replace('>','').Replace('<','')
        }

        $init_module_file = Join-Path -Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "modules\module.$($_.Key).ps1"

        if (-not (Test-Path $init_module_file)) {
            New-Item -Path $init_module_file -ItemType "File" -Force
        }
        if (Test-Path $init_module_file) {
            & $init_module_file
        }

        if ($global:SHOW_MODULES) {
            Write-Host "module" -ForegroundColor Green -NoNewline
            Write-Host " $($_.Key) " -ForegroundColor Yellow -NoNewline
            Write-Host "is imported" -ForegroundColor Green
        }
    }
}


function global:init-module { param (
    [Parameter(Mandatory = $true)]
    [string] $name,
    [Parameter(Mandatory = $false)]
    [string] $version = "latest"
)
    if ($version -eq "latest") {
        Import-Module -Name $name -Force
    } else {
        Import-Module -Name $name -RequiredVersion $version -Force
    }

    $init_module_file = Join-Path -Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "modules\module.$($name).ps1"

    if (Test-Path $init_module_file) {
        & $init_module_file
    } else {
        Write-Host "init-module: $init_module_file not found" -ForegroundColor Red
    }
}


if ($global:IMPORT_MODULES) { init-modules }


# TIPS: If you do not want to download modules by yourself, you can try to import the modules in the $global:CURRENT_SCRIPT_DIRECTORY/downloads/Modules