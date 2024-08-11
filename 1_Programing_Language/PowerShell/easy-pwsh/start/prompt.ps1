function global:prompt {
    $host.ui.RawUI.WindowTitle = "PS " + $(Get-Location)
    Write-Host ("PS " + $(Get-Location) +">") -NoNewLine
    return " "
}