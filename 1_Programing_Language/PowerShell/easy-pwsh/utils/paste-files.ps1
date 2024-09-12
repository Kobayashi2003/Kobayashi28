<#
.SYNOPSIS
    paste the items from the clipboard to the given path

.PARAMETER path
    The path to paste the items
.PARAMETER action
    The action to take on the items (move, copy, link)

.EXAMPLE
    paste c:\temp
#>


param (
    [Parameter(ValueFromPipeline = $true)]
    [Alias("p")]
    [String] $path = '.\',

    [Parameter(Mandatory = $false)]
    [Alias("a")]
    [ArgumentCompleter({ param (
        $commandName,
        $parameterName,
        $wordToComplete,
        $commandAst,
        $fakeBoundParameters )
    @('move', 'copy', 'link') | Where-Object { $_ -like "$wordToComplete*" }})]
    [String] $action = 'copy'
)

try {
    if ($global:PSVERSION -lt 6) {
        $items = Get-Clipboard -Format FileDrop
    } else {
        Add-Type -AssemblyName System.Windows.Forms
        $items = [System.Windows.Forms.Clipboard]::GetFileDropList()
    }

    if ($items.Count -eq 0) {
        throw 'No items found in clipboard' }
    if (-not (Test-Path $path)) {
        throw 'Path does not exist' }

    foreach ($item in $items) {

        if (Test-Path -Path (Join-Path $path (Split-Path $item -Leaf))) {
            Write-Host "`n⚠️ File already exists in $path" -nonewline
            continue
        }

        if ($action -eq 'move') {
            Move-Item -Path $item -Destination $path
        } elseif ($action -eq 'copy') {
            Copy-Item -Path $item -Destination $path
        } elseif ($action -eq 'link') {
            if (Test-Path $item -PathType Leaf) {
                $filename = $item.BaseName
                if (-not $filename) {
                    throw 'Cannot create link for file without a name'
                }
                sudo New-Item -ItemType SymbolicLink -Path "$path "-Name "$filename" -Target "$item"
            } else {
                $dirname = Split-Path $item -Leaf
                if (-not $dirname) {
                    throw 'Cannot create link for directory without a name'
                }
                sudo New-Item -ItemType SymbolicLink -Path "$path" -Name "$dirname" -Target "$item"
            }
        }
    }

    Write-Host "✅ Files pasted to $path"
    exit 0
} catch {
    Write-Host "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}