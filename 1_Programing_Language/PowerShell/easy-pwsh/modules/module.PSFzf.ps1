if (!(Get-Module -ListAvailable -Name PSFzf)) {
    Write-Host "PSFzf module not found. Installing..." -ForegroundColor Yellow
    Install-Module PSFzf
} else {
    Write-Host "PSFzf module found. Importing..." -ForegroundColor Green
}

if (!(Get-Command 'fzf' -ErrorAction SilentlyContinue)) {
    Write-Host "fzf is not installed." -ForegroundColor Red
    Write-Host "You can get fzf from https://github.com/junegunn/fzf" -ForegroundColor Yellow
}

Import-Module PSFzf

Set-PsFzfOption -PSReadlineChordProvider 'Ctrl+t' -PSReadlineChordReverseHistory 'Ctrl+r'
