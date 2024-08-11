<#
    .SYNOPSIS
        Set the title of the console window
    .PARAMETER Title
        The title to set
    .EXAMPLE
        PS> Set-Title "My New Title"
#>

param ( [string] $Title )

try {
    $host.ui.RawUI.WindowTitle = $title
    Write-Host "Title set to $title"
    exit 0 # sucess
} catch {
    Write-Host "Failed to set title: $($_.Exception.Message)"
    exit 1
}