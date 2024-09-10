<#
.SYNOPSIS
    Show the size of your monitor in pixels.
#>

$hdc    = [WinApi]::GetDC(0)
$width  = [WinApi]::GetDeviceCaps($hdc, 118)
$height = [WinApi]::GetDeviceCaps($hdc, 117)

Write-Host "Screen size: $width x $height"