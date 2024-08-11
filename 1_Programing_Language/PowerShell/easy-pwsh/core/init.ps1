$global:current_script_directory = Split-Path (Split-Path $MyInvocation.MyCommand.Definition)

Get-ChildItem (Join-Path -Path $global:current_script_directory -ChildPath "common\*ps1" ) | ForEach-Object { & $_.FullName }
Get-ChildItem (Join-Path -Path $global:current_script_directory -ChildPath "core\*ps1"   ) | ForEach-Object { if ($_.Name -ne $MyInvocation.MyCommand.Name) { & $_.FullName } }
Get-ChildItem (Join-Path -Path $global:current_script_directory -ChildPath "start\*ps1"  ) | ForEach-Object { & $_.FullName }

. (Join-Path -Path $global:current_script_directory -ChildPath "modules\init-modules.ps1")
& (Join-Path -Path $global:current_script_directory -ChildPath "apps\init-apps.ps1")

$env:PATH = (Join-Path -Path $global:current_script_directory -ChildPath "utils") + [IO.Path]::PathSeparator + $env:PATH
