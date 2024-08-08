$current_script_dir = Split-Path $MyInvocation.MyCommand.Definition

if (-not (Test-Path -Path $profile)) {
    New-Item -Path $profile -ItemType File
}

$startup_content = ". $(Join-Path -Path $current_script_dir -ChildPath 'core\init-library.ps1')"

if (-not (Select-String -Path $profile -Pattern $startup_content -SimpleMatch)) {
    Add-Content -Path $profile -Value $startup_content
}
