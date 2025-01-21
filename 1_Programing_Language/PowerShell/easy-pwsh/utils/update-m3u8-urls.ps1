<#
.SYNOPSIS
    Updates ts file paths in m3u8 playlist to full URLs
.DESCRIPTION
    This PowerShell script modifies an m3u8 playlist file by replacing local ts file paths with full URLs.
.PARAMETER InputFile
    Specifies the path to the input m3u8 file
.PARAMETER BaseURL
    Specifies the base URL where ts files are hosted
.EXAMPLE
    PS> ./update-m3u8-urls.ps1 -InputFile "video.m3u8" -BaseURL "https://raw.githubusercontent.com/user/repo/master/video"
.NOTES
    Author: KOBAYASHI
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,

    [Parameter(Mandatory=$true)]
    [string]$BaseURL
)

try {
    # Validate input file
    if (-not (Test-Path $InputFile)) {
        throw "Input file does not exist: $InputFile"
    }

    # Create backup of original file
    $backupFile = "$InputFile.backup"
    Copy-Item -Path $InputFile -Destination $backupFile -Force

    # Read m3u8 content
    $content = Get-Content -Path $InputFile

    # Process each line
    $newContent = $content | ForEach-Object {
        $line = $_
        # Check if line contains .ts extension
        if ($line -match '.*\.ts$') {
            # Extract ts filename
            $tsFile = Split-Path $line -Leaf
            # Replace with full URL
            $line = "$BaseURL/$tsFile"
        }
        $line
    }

    # Write modified content back to file
    $newContent | Set-Content -Path $InputFile -Force

    Write-Host "M3U8 file updated successfully!"
    Write-Host "Original file backed up to: $backupFile"
    Write-Host "Updated file: $InputFile"
    exit 0 # success
} catch {
    Write-Host "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])" -ForegroundColor Red
    exit 1
}