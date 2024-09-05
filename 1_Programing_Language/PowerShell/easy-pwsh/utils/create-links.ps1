<#
.SYNOPSIS
    Create symbolic links for the given files or directories

.PARAMETER items
    The items to create links for
.PARAMETER path
    The path to create the links in

.EXAMPLE
    create-links 'C:\Windows\System32\notepad.exe' 'C:\temp'
#>

#requires -RunAsAdministrator

param (
    [Parameter(Mandatory = $true, ValueFromPipeline = $true)]
    [String[]] $items,

    [Parameter(Mandatory = $true)]
    [String] $path
)

$items = Get-Item "$items"

foreach ($item in $items) {
    if (Test-Path $item -PathType Leaf) {
        $itemname = $item.BaseName
    } else {
        $itemname = Split-Path $item -Leaf
    }

    if (-not $itemname) {
        Write-Host "⚠️ Cannot create link for $item without a name"
        continue
    }
    if (Test-Path "$path\$itemname") {
        Write-Host "⚠️ Link already exists for $item"
        continue
    }

    New-Item -ItemType SymbolicLink -Path "$path" -Name "$itemname" -Target "$item"
}