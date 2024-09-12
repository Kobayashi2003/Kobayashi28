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
    if ($global:PSVERSION -lt 6) {
        Set-Clipboard -Path $path
    } else {
        Add-Type -AssemblyName System.Windows.Forms
        $files = [System.Collections.Specialized.StringCollection]::new()
        $files.Add((Get-Item $path).FullName) >$null
        [System.Windows.Forms.Clipboard]::SetFileDropList($files)
    }
    Write-Host "✅ Files copied to clipboard"
    exit 0
} catch {
    Write-Host "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}