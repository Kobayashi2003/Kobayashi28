<#
.SYNOPSIS
    paste the files from the clipboard to the given path

.PARAMETER path
    The path to paste the files
.PARAMETER action
    The action to take on the files (move, copy, link)

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
    [String] $action = 'move'
)

try {
    $files = Get-Clipboard -Format FileDrop

    if ($files.Count -eq 0) {
        throw 'No files found in clipboard' }
    if (-not (Test-Path $path)) {
        throw 'Path does not exist' }

    foreach ($file in $files) {
        if ($action -eq 'move') {
            Move-Item -Path $file -Destination $path
        } elseif ($action -eq 'copy') {
            Copy-Item -Path $file -Destination $path
        } elseif ($action -eq 'link') {
            New-Item -ItemType SymbolicLink -Path $path -Name $file.BaseName -Value $file
        }
    }

    Write-Host "✅ Files pasted to $path"
    exit 0
} catch {
    Write-Host "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}