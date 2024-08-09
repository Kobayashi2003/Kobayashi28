function reload-apps {
    Get-ChildItem (Join-Path -Path $global:current_script_directory -ChildPath "config\*ps1"   ) | ForEach-Object { . $_.FullName }
    Get-ChildItem (Join-Path -Path $global:current_script_directory -ChildPath "apps\*ps1"   ) | ForEach-Object { . $_.FullName } }

function show-apps { $global:apps | Format-Table }

$global:apps.GetEnumerator() | ForEach-Object { Set-Alias -Name $_.Key -Value $_.Value -Scope Global }