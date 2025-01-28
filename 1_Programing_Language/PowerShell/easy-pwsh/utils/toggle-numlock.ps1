<#
.SYNOPSIS
    Toggles the NumLock key state and displays its new status
.DESCRIPTION
    This PowerShell script simulates pressing the NumLock key, effectively toggling its state.
    It displays the new NumLock status after the toggle with color and symbols.
.EXAMPLE
    PS> ./Toggle-NumLock
#>

try {
    [KeyboardSimulator]::ToggleKey([KeyboardSimulator]::VK_NUMLOCK)

    $newState = [KeyboardSimulator]::IsKeyToggled([KeyboardSimulator]::VK_NUMLOCK)
    if ($newState) {
        Write-Host "🔢 NumLock is now " -NoNewline
        Write-Host "ON" -ForegroundColor Green
    } else {
        Write-Host "❌ NumLock is now " -NoNewline
        Write-Host "OFF" -ForegroundColor Red
    }

    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}