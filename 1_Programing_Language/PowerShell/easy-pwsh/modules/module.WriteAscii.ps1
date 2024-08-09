if (!(Get-Module -ListAvailable -Name WriteAscii)) {
    Write-Host "WriteAscii module not found. Installing..." -ForegroundColor Yellow
    Install-Module WriteAscii
} else {
    # Write-Host "WriteAscii module found. Importing..." -ForegroundColor Green
}

Import-Module WriteAscii

# Write-Ascii -InputObject ">>> easy pwsh <<<" -ForegroundColor DarkCyan