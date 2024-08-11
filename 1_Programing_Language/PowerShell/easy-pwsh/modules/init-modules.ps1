function global:check-module {
<#
.SYNOPSIS
    Check if module is installed

.PARAMETER name
    Name of the module

.EXAMPLE
    check-module -name Terminal-Icons
#>

    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [string] $name
    )

    if (!(Get-Module -ListAvailable -Name $name)) {
        try {
            Write-Host "Module $name not found. Installing..." -ForegroundColor Yellow
            sudo Install-Module -Name $name
            if (!(Get-Module -ListAvailable -Name $name)) {
                throw "Failed to install $name module"
            }
        } catch {
            Write-Host "Failed to install $name module: $_" -ForegroundColor Red
            return $false
        }
    }

    return $true
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
$global:modules | ForEach-Object { if ((check-module -Name $_)) { try { Import-Module -Name $_ ; $global:modules_imported += $_ } catch {} } }
$global:modules_imported | ForEach-Object {
    $private:modulename = $_
    $private:filename = "module.$modulename.ps1"
    $private:dirname = Join-Path -Path $global:current_script_directory -ChildPath "modules"
    if (-not (Test-Path (Join-Path -Path $dirname -ChildPath $filename))) {
        New-Item -Path $dirname -Name $filename -ItemType File }
    if (check-imported $modulename $global:modules_imported) {
        & (Join-Path -Path $dirname -ChildPath $filename) }
}
