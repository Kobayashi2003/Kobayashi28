function Set-Title {
    param ( [string] $Title )

    $default_title = 'Windows PowerShell'
    try {
        # if empty, set to windows powershell
        if ('' -eq $Title) {
            $title = $default_title
        } else {
            $host.ui.RawUI.WindowTitle = $title
        }
    } catch {
        $host.ui.RawUI.WindowTitle = $default_title
        Write-Host "Failed to set title: $($_.Exception.Message)"
    }
}