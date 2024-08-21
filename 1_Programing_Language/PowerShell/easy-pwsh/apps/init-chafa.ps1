﻿<#
.SYNOPSIS
    Chafa image viewer
.NOTES
    https://github.com/hpjansson/chafa
#>

if (-not (Get-Command 'chafa' -ErrorAction SilentlyContinue)) {
    return
}

function global:loop-images {
<#
.PARAMETER path
    Path to image
.PARAMETER interval
    Interval between images
.PARAMETER random
    Randomize image
.PARAMETER sortby
    Sort images
#>
    param (
        [Parameter(Mandatory = $true, ValueFromPipeline = $true, Position = 0)]
        [string[]] $path,

        [Parameter(Position = 1)]
        [float] $interval = 0,

        [Parameter(ParameterSetName = 'random')]
        [switch] $random,

        [Parameter(ParameterSetName = 'sort')]
        [ValidateSet('Name', 'LastWriteTime', 'Size')]
        [string] $sortby
    )

    $images = (Get-ChildItem -Path $path -File | Select-Object -ExpandProperty FullName)

    if ($images.Count -eq 0) {
        Write-Host 'Invalid path' -NoNewline -ForegroundColor DarkRed
        return
    }

    if ($sortby) {
        $images = $images | Sort-Object $sortby
    }

    if ($random) {
        $images = $images | Sort-Object { Get-Random }
    }

    $idx = 0
    $lst = -1
    $stop = $false
    while ($true) {

        if ($Host.UI.RawUI.KeyAvailable) {
            $key = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyUp')
            if ($key.VirtualKeyCode -eq 27) { # ESC
                break
            } elseif ($key.VirtualKeyCode -eq 32) { # SPACE
                $stop = !$stop
                if ($stop) {
                    Write-Host 'Stopped' -NoNewline -ForegroundColor DarkCyan
                } else {

                }
            } elseif ($key.VirtualKeyCode -eq 38) { # UP
                $idx = ($idx - 1 + $images.Count) % $images.Count
            } elseif ($key.VirtualKeyCode -eq 40) { # DOWN
                $idx = ($idx + 1) % $images.Count
            } elseif ($key.VirtualKeyCode -eq 81) { # Q
                break
            } elseif ($key.VirtualKeyCode -eq 82) { # R
                $lst = -1
            }
        }

        if ($lst -ne $idx) {
            $lst = $idx
            $image = $images[$idx]
            & chafa $image --clear --align 'center,center' --optimize 0
        }

        if ($interval -gt 0 -and -not $stop) {
            Start-Sleep -Seconds $interval
            $idx = ($idx + 1) % $images.Count
        } else {

        }
    }
}


function global:show-image {
<#
.PARAMETER path
    Path to image
#>
    param (
        [Parameter(Mandatory = $true, ValueFromPipeline = $true, Position = 0)]
        [string[]] $path
    )

    & chafa $path --clear --align 'center,center' --optimize 0
}