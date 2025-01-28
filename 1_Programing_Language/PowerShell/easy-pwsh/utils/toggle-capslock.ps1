<#
.SYNOPSIS
    Toggles the CapsLock key state and displays its new status
.DESCRIPTION
    This PowerShell script simulates pressing the CapsLock key, effectively toggling its state.
    It displays the new CapsLock status after the toggle with color and symbols.
.EXAMPLE
    PS> ./Toggle-CapsLock
#>

try {
    [KeyboardSimulator]::ToggleKey([KeyboardSimulator]::VK_CAPITAL)

    $newState = [KeyboardSimulator]::IsKeyToggled([KeyboardSimulator]::VK_CAPITAL)
    if ($newState) {
        Write-Host "🔠 CapsLock is now " -NoNewline
        Write-Host "ON" -ForegroundColor Green
    } else {
        Write-Host "🔡 CapsLock is now " -NoNewline
        Write-Host "OFF" -ForegroundColor Red
    }

    exit 0 # success
} catch {
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
    exit 1
}