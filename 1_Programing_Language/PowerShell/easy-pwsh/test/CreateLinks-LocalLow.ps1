<#
.SYNOPSIS
Creates symbolic links from current directory to LocalLow folder with admin privileges

.DESCRIPTION
This script will:
1. Auto-elevate to admin privileges if needed
2. Show preview of items to link
3. Create symbolic links in LocalLow folder
4. Display results and wait for user confirmation
#>

param(
    [switch]$Elevated  # Internal flag to indicate elevated execution
)

function Invoke-AdminElevation {
    <#
    .DESCRIPTION
    Restarts the current script with admin privileges in a new Windows Terminal

    .PARAMETER ScriptPath
    Full path to the current script
    #>
    param(
        [Parameter(Mandatory)]
        [string]$ScriptPath
    )

    # Build restart command with preserved working directory
    $restartCommand = @"
        `$prevPath = (Get-Location).Path
        Set-Location "`$prevPath"
        & "$ScriptPath" -Elevated
"@

    # Encode command to avoid escaping issues
    $bytes = [System.Text.Encoding]::Unicode.GetBytes($restartCommand)
    $encodedCommand = [Convert]::ToBase64String($bytes)

    # Launch elevated process
    Start-Process wt -Verb RunAs -ArgumentList @(
        "pwsh.exe",
        "-NoExit",
        "-EncodedCommand",
        $encodedCommand
    )

    # Exit current non-admin instance
    exit
}

#region Main Execution
##############################################################################
# Main script logic
##############################################################################

# Elevate to admin if needed
if (-not $Elevated) {
    # Check current admin status
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($identity)

    if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        # Restart with admin rights using script's full path
        Invoke-AdminElevation -ScriptPath $MyInvocation.MyCommand.Path
    }
}

try {
    #region Path Configuration
    ##################################################
    # Get target directories
    ##################################################

    # LocalLow folder path
    $localPath = [Environment]::GetFolderPath([Environment+SpecialFolder]::LocalApplicationData)
    $locallowPath = Join-Path (Split-Path $localAppData -Parent) "LocalLow"
    if (-not $locallowPath) {
        throw "Failed to locate LocalLow folder"
    }

    # Source directory (script location or current directory)
    $scriptPath = if ($PSScriptRoot) {
        $PSScriptRoot
    } else {
        (Get-Location).Path
    }
    #endregion

    #region Preview Display
    ##################################################
    # Show linking preview
    ##################################################

    # Get items to link (exclude self)
    $items = Get-ChildItem -Path $scriptPath -Exclude $MyInvocation.MyCommand.Name

    # Display header
    Write-Host "`nSymbolic Link Creation Preview" -ForegroundColor Cyan
    Write-Host ("-" * 80)

    # Show items table
    $items | ForEach-Object {
        $linkName = if ($_.PSIsContainer) { $_.Name } else { $_.BaseName }
        [PSCustomObject]@{
            'Item Type' = if ($_.PSIsContainer) { 'Folder' } else { 'File' }
            'Link Name' = $linkName
            'Target'    = $_.FullName
        }
    } | Format-Table -AutoSize

    # Confirmation prompt
    Write-Host "`nCreate these links in LocalLow folder? (Y/N)" -ForegroundColor Yellow -NoNewline
    $confirmation = Read-Host
    if ($confirmation -notmatch '^[yY]') {
        Write-Host "Aborted by user" -ForegroundColor Red
        exit 0
    }
    #endregion

    #region Link Creation
    ##################################################
    # Create symbolic links
    ##################################################

    $results = foreach ($item in $items) {
        # Generate link name
        $itemName = if ($item.PSIsContainer) { $item.Name } else { $item.BaseName }
        $linkPath = Join-Path $locallowPath $itemName

        # Skip existing items
        if (Test-Path $linkPath) {
            Write-Host "[SKIPPED] $itemName (Already exists)" -ForegroundColor DarkGray
            continue
        }

        # Create symbolic link
        try {
            Write-Host "[CREATING] $itemName..." -ForegroundColor Green -NoNewline
            $null = New-Item `
                -ItemType SymbolicLink `
                -Path $linkPath `
                -Target $item.FullName `
                -ErrorAction Stop

            Write-Host "`r[CREATED ] $itemName" -ForegroundColor Green
            [PSCustomObject]@{
                Name   = $itemName
                Status = 'Created'
                Path   = $linkPath
            }
        }
        catch {
            Write-Host "`r[FAILED  ] $itemName ($($_.Exception.Message))" -ForegroundColor Red
            [PSCustomObject]@{
                Name   = $itemName
                Status = 'Error'
                Path   = $linkPath
                Error  = $_.Exception.Message
            }
        }
    }
    #endregion

    #region Results Display
    ##################################################
    # Show operation results
    ##################################################

    Write-Host "`nOperation Results:" -ForegroundColor Cyan
    Write-Host ("-" * 80)
    $results | Format-Table -AutoSize -Property Name, Status, Path

    # Wait for user confirmation
    Write-Host "`nPress Enter to exit..." -ForegroundColor Cyan -NoNewline
    $null = Read-Host
    exit 0
    #endregion
}
catch {
    Write-Host "`nFATAL ERROR: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}