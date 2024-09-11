﻿$global:CURRENT_SCRIPT_DIRECTORY = Split-Path (Split-Path $MyInvocation.MyCommand.Definition)

Get-ChildItem (Join-Path -Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "common\*ps1" ) | ForEach-Object { & $_.FullName }
Get-ChildItem (Join-Path -Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "core\*ps1"   ) | ForEach-Object { if ($_.Name -ne $MyInvocation.MyCommand.Name) { & $_.FullName } }
Get-ChildItem (Join-Path -Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "start\*ps1"  ) | ForEach-Object { & $_.FullName }

& (Join-Path -Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "apps\init-apps.ps1")
& (Join-Path -Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "modules\init-modules.ps1")

$env:PATH = (Join-Path -Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "utils") + [IO.Path]::PathSeparator + $env:PATH
# [Environment]::SetEnvironmentVariable("PATH", (Join-Path -Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "utils") + [IO.Path]::PathSeparator + $env:PATH, "User")

. (Join-Path -Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "functions\init-functions.ps1")
