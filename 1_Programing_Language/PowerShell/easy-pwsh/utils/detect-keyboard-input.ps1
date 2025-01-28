<#
.SYNOPSIS
    Detects and echoes all keyboard input
.DESCRIPTION
    This PowerShell script continuously detects keyboard input and displays the pressed keys in real-time.
    It uses the GetAsyncKeyState method from the WinApi class to detect key presses.
.EXAMPLE
    PS> ./Detect-Keyboard-Input.ps1
    Starts detecting and displaying keyboard input. Press Ctrl+C to stop.
#>

function Get-KeyState($key) {
    return [WinApi]::GetAsyncKeyState($key) -band 0x8000
}

$keyMap = @{
    8 = "Backspace"; 9 = "Tab"; 13 = "Enter"; 16 = "Shift"; 17 = "Ctrl"; 18 = "Alt"; 19 = "Pause";
    20 = "Caps Lock"; 27 = "Esc"; 32 = "Space"; 33 = "Page Up"; 34 = "Page Down"; 35 = "End"; 36 = "Home";
    37 = "Left"; 38 = "Up"; 39 = "Right"; 40 = "Down"; 44 = "Print Screen"; 45 = "Insert"; 46 = "Delete";
    91 = "Windows"; 93 = "Context Menu";
    112 = "F1"; 113 = "F2"; 114 = "F3"; 115 = "F4"; 116 = "F5"; 117 = "F6";
    118 = "F7"; 119 = "F8"; 120 = "F9"; 121 = "F10"; 122 = "F11"; 123 = "F12"
}

Write-Host "Detecting keyboard input. Press Ctrl+C to stop." -ForegroundColor Yellow

try {
    while ($true) {
        for ($key = 8; $key -le 255; $key++) {
            if (Get-KeyState $key) {
                if ($keyMap.ContainsKey($key)) {
                    Write-Host $keyMap[$key] -NoNewline -ForegroundColor Cyan
                }
                elseif ($key -ge 65 -and $key -le 90) {
                    # Letters
                    Write-Host ([char]$key) -NoNewline -ForegroundColor Green
                }
                elseif ($key -ge 48 -and $key -le 57) {
                    # Numbers
                    Write-Host ([char]$key) -NoNewline -ForegroundColor Magenta
                }
                else {
                    # Other printable characters
                    $char = [char]$key
                    if ([char]::IsLetterOrDigit($char) -or [char]::IsPunctuation($char) -or [char]::IsSymbol($char)) {
                        Write-Host $char -NoNewline -ForegroundColor White
                    }
                }
                Write-Host " " -NoNewline
                Start-Sleep -Milliseconds 50  # Debounce
            }
        }
        Start-Sleep -Milliseconds 10  # Reduce CPU usage
    }
}
finally {
    Write-Host "`nKeyboard detection stopped." -ForegroundColor Yellow
}
