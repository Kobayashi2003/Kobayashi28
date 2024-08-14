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

    if (!(Get-Module -ListAvailable -Name $name)) {
        try {
            Write-Host "Module $name not found. Installing..." -ForegroundColor Yellow
            if ($version -eq "latest") {
                sudo Install-Module -Name $name
            } else {
                sudo Install-Module -Name $name -RequiredVersion $version
            }
            if (!(Get-Module -ListAvailable -Name $name)) {
                throw "Failed to install $name module"
            }
        } catch {
            Write-Host "Failed to install $name module: $_" -ForegroundColor Red
            return  $null
        }
    }

    $installed_versions = @(
        Get-Module -ListAvailable |
        Where-Object { $_.Name -eq $name } |
        Sort-Object -Property Version -Descending |
        foreach { $_.Version.ToString() })


    if ($version -eq "latest") {
        return $installed_versions[0]
    }

    $_version = $version

    if ($_version.contains('=')) {
        $_version = $_version.Replace('=', '')
        if ($installed_versions -contains $_version) {
            return $_version
        }
    }

    if ($_version.contains(">")) {
        $_version = $_version.Replace('>', '')
        foreach ($v in $installed_versions) {
            if ($v -gt $_version) {
                return $v
            }
        }
    }

    if ($_version.contains("<")) {
        $_version = $_version.Replace('<', '')
        foreach ($v in $installed_versions) {
            if ($v -lt $_version) {
                return $v
            }
        }
    }

    if (-not ($_version -match '^[0-9]+\.[0-9]+\.[0-9]+$')) {
        throw "Invalid version format:$_version"
    }

    Write-Host "Module $name version $_version not found, installing..." -ForegroundColor Yellow
    try {
        sudo Install-Module -Name $name -RequiredVersion $_version
    } catch {
        Write-Host "Failed to install $name module: $_" -ForegroundColor Red
        return $null
    }

    return $_version
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
        try { Import-Module -Name $_.Key -RequiredVersion $_.Value.Replace('=','').Replace('>','').Replace('<','') ;
            $global:modules_imported += $_.Key } catch {} }
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