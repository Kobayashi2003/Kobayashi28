function reload-apps {
    Get-ChildItem (Join-Path -Path $global:current_script_directory -ChildPath "common\*ps1"   ) | ForEach-Object { & $_.FullName }
    & (Join-Path -Path $global:current_script_directory -ChildPath "apps\init-apps.ps1") }

function show-apps { $global:apps | Format-Table }

Get-ChildItem (Join-Path -Path $global:current_script_directory -ChildPath "apps\*ps1"   ) | ForEach-Object { if ($_.Name -ne $MyInvocation.MyCommand.Name) { & $_.FullName } }

$global:apps.GetEnumerator() | ForEach-Object { Set-Alias -Name $_.Key -Value $_.Value -Scope Global }