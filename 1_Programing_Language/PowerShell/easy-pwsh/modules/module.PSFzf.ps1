# Select Current Provider Path (default chord: `Ctrl+t`)
# Reverse Search Through PSReadline History (default chord: `Ctrl+r`)
Set-PsFzfOption -PSReadlineChordProvider 'Ctrl+t' -PSReadlineChordReverseHistory 'Ctrl+r'

# Set-Location Based on Selected Directory (default chord: `Alt+c`)
# example command - use $Location with a different command:
$commandOverride = [ScriptBlock]{ param($Location) Write-Host $Location }
# pass your override to PSFzf:
Set-PsFzfOption -AltCCommand $commandOverride

# Search Through Command Line Arguments in PSReadline History (default chord: `Alt+a`)
Set-PSReadLineKeyHandler -Key Alt+a -ScriptBlock { Invoke-FuzzyHistory }

Set-PsFzfOption -TabExpansion

Set-PSFzfOption -EnableFd
Set-PSFzfOption -EnableAliasFuzzyEdit           # fe
Set-PSFzfOption -EnableAliasFuzzyFasd           # ff
Set-PSFzfOption -EnableAliasFuzzyZLocation      # fz
Set-PSFzfOption -EnableAliasFuzzyGitStatus      # fgs
Set-PSFzfOption -EnableAliasFuzzyHistory        # fh
Set-PSFzfOption -EnableAliasFuzzyKillProcess    # fkill
Set-PSFzfOption -EnableAliasFuzzySetLocation    # fd
Set-PSFzfOption -EnableAliasFuzzyScoop          # fs
Set-PSFzfOption -EableAliasFuzzySetEverything   # cde