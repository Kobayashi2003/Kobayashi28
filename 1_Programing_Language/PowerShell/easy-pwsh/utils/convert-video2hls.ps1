<#
.SYNOPSIS
    Converts a video file to HLS (HTTP Live Streaming) format
.DESCRIPTION
    This PowerShell script converts a video file to HLS format, creating an m3u8 playlist and video segments.
.PARAMETER InputFile
    Specifies the path to the input video file
.PARAMETER OutputDir
    Specifies the output directory for HLS files (optional, defaults to input file directory)
.PARAMETER SegmentDuration
    Specifies the duration of each segment in seconds (optional, defaults to 5 seconds)
.EXAMPLE
    PS> ./Convert-Video2HLS.ps1 -InputFile "C:\Videos\myvideo.mp4"
.NOTES
    Author: KOBAYASHI
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,

    [Parameter(Mandatory=$false)]
    [string]$OutputDir = "",

    [Parameter(Mandatory=$false)]
    [int]$SegmentDuration = 10
)

try {
    # Validate input file
    if (-not (Test-Path $InputFile)) {
        throw "Input file does not exist: $InputFile"
    }

    # Set up output directory
    $fileName = [System.IO.Path]::GetFileNameWithoutExtension($InputFile)
    if ($OutputDir -eq "") {
        $OutputDir = Join-Path ([System.IO.Path]::GetDirectoryName($InputFile)) $fileName
    }
    if (-not (Test-Path $OutputDir)) {
        New-Item -ItemType Directory -Path $OutputDir | Out-Null
    }

    # Define output files
    $tempFile = Join-Path $OutputDir "temp_converted.mp4"
    $playlistFile = Join-Path $OutputDir "$fileName.m3u8"
    $segmentPattern = Join-Path $OutputDir "$fileName%03d.ts"

    # Step 1: Convert to H.264 if needed
    Write-Host "Converting video to H.264 format..."
    ffmpeg -i $InputFile -c:v libx264 -strict -2 $tempFile

    # Step 2: Create m3u8 playlist and segments
    Write-Host "Creating HLS segments and playlist..."
    ffmpeg -i $tempFile -c copy -map 0 -f segment -segment_list $playlistFile -segment_time $SegmentDuration -segment_format mpegts $segmentPattern

    # Step 3: Clean up temporary files
    Remove-Item $tempFile

    Write-Host "Process completed successfully!"
    Write-Host "M3U8 playlist: $playlistFile"
    Write-Host "Segments directory: $OutputDir"
    exit 0 # success
} catch {
    Write-Host "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])" -ForegroundColor Red
    exit 1
}