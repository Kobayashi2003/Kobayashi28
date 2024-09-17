function global:reload-apps {
    Get-ChildItem (Join-Path -Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "common\*ps1"   ) | ForEach-Object { & $_.FullName }
    & (Join-Path -Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "apps\init-apps.ps1") }

function global:show-apps { $global:APPS_ALIAS | Format-Table }

Get-ChildItem (Join-Path -Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "apps\init-*.ps1"   ) | ForEach-Object { if ($_.Name -ne $MyInvocation.MyCommand.Name) { & $_.FullName } }

$global:APPS_ALIAS.GetEnumerator() | ForEach-Object { if (Test-Path -Path $_.Value -ErrorAction SilentlyContinue) { Set-Alias -Name $_.Key -Value $_.Value -Scope Global } }