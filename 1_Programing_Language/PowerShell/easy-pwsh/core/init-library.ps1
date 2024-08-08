$current_script_filename = $MyInvocation.MyCommand.Name
$current_script_directory = Split-Path $MyInvocation.MyCommand.Definition # core directory

Get-ChildItem (Join-Path -Path $current_script_directory -ChildPath "..\core\*ps1") | ForEach-Object { if ($_.Name -ne $current_script_filename) { . $_.FullName } }
Get-ChildItem (Join-Path -Path $current_script_directory -ChildPath "..\apps\*ps1") | ForEach-Object { . $_.FullName }
Get-ChildItem (Join-Path -Path $current_script_directory -ChildPath "..\utils\*ps1") | ForEach-Object { . $_.FullName }
Get-ChildItem (Join-Path -Path $current_script_directory -ChildPath "..\modules\*ps1") | ForEach-Object { . $_.FullName }
Get-ChildItem (Join-Path -Path $current_script_directory -ChildPath "..\start\*ps1") | ForEach-Object { . $_.FullName }

Remove-Variable -Name current_script_filename
Remove-Variable -Name current_script_directory
