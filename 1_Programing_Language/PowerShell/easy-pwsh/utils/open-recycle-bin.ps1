<#
.SYNOPSIS
    Open the recycle bin in Windows.
#>

try {
    Start-Process "$env:windir\explorer.exe" -ArgumentList "shell:::{645FF040-5081-101B-9F08-00AA002F954E}"
    "✔️  Done."
    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}