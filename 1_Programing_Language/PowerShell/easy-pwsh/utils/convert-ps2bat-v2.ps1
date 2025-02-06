param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

function Convert-PowerShellToBatch {
    param ([string]$Path)

    try {
        $psContent = Get-Content -Path $Path -Raw
        $md5Hash = (Get-FileHash -InputStream ([System.IO.MemoryStream]::new([System.Text.Encoding]::UTF8.GetBytes($psContent))) -Algorithm MD5).Hash.ToLower()
        $encodedContent = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($psContent))
        $batPath = [System.IO.Path]::ChangeExtension($Path, ".bat")
        $batContent = @"
@echo off
powershell -NoProfile -Command "[IO.File]::WriteAllText('$md5Hash.ps1', [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('$encodedContent')))"
powershell -NoProfile -ExecutionPolicy Bypass -File $md5Hash.ps1
del $md5Hash.ps1
"@
        [System.IO.File]::WriteAllText($batPath, $batContent, [System.Text.Encoding]::ASCII)
        Write-Host "Converted $Path to $batPath"
    } catch {
        Write-Host "Error converting $Path : $($_.Exception.Message)" -ForegroundColor Red
    }
}

Get-ChildItem -Path $FilePath -Filter *.ps1 | ForEach-Object {
    Convert-PowerShellToBatch -Path $_.FullName
}