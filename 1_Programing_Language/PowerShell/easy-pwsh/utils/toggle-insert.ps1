<#
.SYNOPSIS
    Toggles the Insert key state and displays its new status
.DESCRIPTION
    This PowerShell script simulates pressing the Insert key, effectively toggling its state.
    It displays the new Insert key status after the toggle with color and symbols.
.EXAMPLE
    PS> ./Toggle-Insert
#>

try {
    [KeyboardSimulator]::ToggleKey([KeyboardSimulator]::VK_INSERT)

    $newState = [KeyboardSimulator]::IsKeyToggled([KeyboardSimulator]::VK_INSERT)
    if ($newState) {
        Write-Host "✏️ Insert mode is now " -NoNewline
        Write-Host "ON" -ForegroundColor Green
    } else {
        Write-Host "🚫 Insert mode is now " -NoNewline
        Write-Host "OFF" -ForegroundColor Red
    }

    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}