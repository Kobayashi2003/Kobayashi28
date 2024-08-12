<#
.SYNOPSIS
    copy the given files to the clipboard

.PARAMETER files

    The files to copy
.EXAMPLE
    copy 'C:\Windows\System32\notepad.exe'
#>


param (
    [Parameter(Mandatory = $true, ValueFromPipeline = $true)]
    [Alias("p")] [String[]] $path
)

try {
    Set-Clipboard -Path $path
    Write-Host "✅ Files copied to clipboard"
    exit 0
} catch {
    Write-Host "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}