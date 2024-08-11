using namespace System.Management.Automation
using namespace System.Management.Automation.Language


If (-Not (Test-Path Variable:PSise)) {  # Only run this in the console and not in the ISE
    Import-Module Get-ChildItemColor # import the module

    # set the alias 'l' and 'ls' as the Get-ChildItemColor
    # Set-Alias l Get-ChildItemColor -option AllScope
    # Set-Alias ls Get-ChildItemColorFormatWide -option AllScope
    Set-Alias l Get-ChildItemColor -Scope Global -Force -option AllScope
    Set-Alias ls Get-ChildItemColorFormatWide -Scope Global -Force -option AllScope

    # ALL COLOR: Black, DarkBlue, DarkGreen, DarkCyan, DarkRed, DarkMagenta, DarkYellow, Gray, DarkGray, Blue, Green, Cyan, Red, Magenta, Yellow, White

    # Change color for directories to Blue
    $GetChildItemColorTable.File['Directory'] = "Blue"

    # Change color for executables to Magenta
    ForEach ($Exe in $GetChildItemColorExtensions['ExecutableList']) {
        $GetChildItemColorTable.File[$Exe] = "Magenta"
    }

    $GetChildItemColorExtensions['OfficeList'] = @(
        ".docx",
        ".pdf",
        ".pptx",
        ".xlsx"
    )

    $GetChildItemColorExtensions['Image'] = @(
        ".png",
        ".jpg"
    )

    ForEach ($Extension in $GetChildItemColorExtensions['OfficeList']) {
        if (-not $GetChildItemColorTable.File.ContainsKey($Extension)) {
            $GetChildItemColorTable.File.Add($Extension, "DarkGreen")
        }
    }

    ForEach ($Extension in $GetChildItemColorExtensions['Image']) {
        if (-not $GetChildItemColorTable.File.ContainsKey($Extension)) {
            $GetChildItemColorTable.File.Add($Extension, "DarkYello")
        }
    }
}

