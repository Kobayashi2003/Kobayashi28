<#
.SYNOPSIS
    Displays directory structure in a tree-like format
.DESCRIPTION
    This PowerShell script displays the directory structure in a tree-like format, similar to the Linux tree command.
.EXAMPLE
    PS> ./tree.ps1
    .
    ├── File1.txt
    ├── File2.txt
    ├── Folder1
    │   ├── SubFile1.txt
    │   └── SubFolder1
    │       └── DeepFile.txt
    └── Folder2
        └── SubFile2.txt
.EXAMPLE
    PS> ./tree.ps1 C:\SomeDirectory
    C:\SomeDirectory
    ├── File1.txt
    ├── File2.txt
    └── Folder1
        └── SubFile1.txt
.LINK
    https://github.com/YourGitHubUsername/PowerShell
.NOTES
    Author: Your Name | License: CC0
#>

try {
    function Show-TreeView {
        param (
            [string]$Path = ".",
            [int]$IndentLevel = 0
        )

        # $items = Get-ChildItem -Path $Path
        $items = Get-ChildItem -LiteralPath $Path

        foreach ($item in $items) {
            $indent = "│   " * $IndentLevel
            $lastItem = $item -eq $items[-1]

            if ($lastItem) {
                Write-Host "$indent└── $($item.Name)"
            } else {
                Write-Host "$indent├── $($item.Name)"
            }

            if ($item.PSIsContainer) {
                $newIndent = $IndentLevel + 1
                Show-TreeView -Path $item.FullName -IndentLevel $newIndent
            }
        }
    }

    $startPath = if ($args.Count -gt 0) { $args[0] } else { "." }
    Write-Host $startPath
    Show-TreeView -Path $startPath
    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}