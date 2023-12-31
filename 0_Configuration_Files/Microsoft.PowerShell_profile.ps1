using namespace System.Management.Automation
using namespace System.Management.Automation.Language

$My_Script_Dir = 'C:\Users\KOBAYASHI\Documents\WindowsPowerShell\myScripts'
$My_Script_Path = 'C:\Users\KOBAYASHI\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1'

# TODO
#      7.try to write a function to manage the history message



##### -- Function Start -- #####



## -- {Function 1 -- Start Or Kill a Process} -- ##

# Start or Kill a Process
function _Start_and_Kill($app_path, $state="start") {
    # echo $app_path $state
    $app_name = ($app_path.Split("\")[-1]).Split(".")[-2]
    if ($state -eq "start") { # Start Process
        Write-Output "$app_name Run"
        # Start-Process
        Start-Process $app_path
    } elseif ($state.startswith("k")) { # Kill Process
        Write-Output "$app_name Kill"
        Stop-Process -ProcessName $app_name
    } elseif ($state.startswith("p")) { # show the paths
        Write-Output $app_path
    }
}



## -- {Function 2 -- Edit this Script} -- ##

# A function for editing this Sctipt
function _Edit_My_Script {
    powershell_ise $My_Script_Path
}



## -- {Function 3 -- Show all current Paths} -- ##

# A function for showing all current Paths
function _Show_Path() {
    # echo $My_Script_Path
    Write-Output "===================="
    (Get-Content -Path $My_Script_Path -Raw).Split(";")[-1] | Write-Output
    Write-Output "===================="
}



## -- {Function 4 -- Delete a Path} -- ##

# A funtion for deleting Paths
function _Delete_Path($app_name="") {
    # clc -Path C:\Users\KOBAYASHI\Desktop\test.ps1 -Include "function"
    if ($app_name -eq "") {
        Write-Output "You have to enter an app name"
        return
    }
    $pattern1 = "# $app_name"
    $content1 = Select-String -Path $My_Script_Path -Pattern $pattern1
    $line1 = $content1.ToString().Split(":")[-2] - 1

    $pattern2 = "# END $app_name"
    $content2 = Select-String -Path $My_Script_Path -Pattern $pattern2
    $line2 = $content2.ToString().Split(":")[-2] - 1

    $len = $line2 - $line1 + 1

    # echo $line1 $line2 $len

    $old_content = Get-Content -Path $My_Script_Path -ReadCount 0
    $new_content = @()
    for($i = 0; $i -lt $old_content.Length; $i += 1) {
        if ($i -gt $line1-1 -and $i -lt $line1+$len+1 ) {
            # echo $old_content[$i]
        } else {
            $new_content += $old_content[$i]
        }
    }
    # echo $new_content
    Set-Content -Path $My_Script_Path -Value $new_content
    Write-Output "Path Deleted"
}



## -- {Function 5 -- Add a Path} -- ##

# A function for adding new Paths
function _Add_Path($app_name="", $app_path="") {

    if ($app_name -eq "") {
        Write-Output "You have to enter an app name"
        return
    }
    if($app_path -eq "") {
        Write-Output "You have to enter the path of app"
        return
    }

    $content = Get-Content $My_Script_Path
    if ("# $app_name" -in $content) {
        Write-Output "This path already exists. Do you want to overwrite it? [Y/N]"
        $judge = Read-Host
        if ($judge -eq "Y") {
            _Delete_Path $app_name
        } else {
            return
        }
    }
    Add-Content $My_Script_Path "`n# $app_name`nfunction $app_name(`$state`=`"start`") {`n    `$app_path = `'$app_path`'`n    _Start_and_Kill `$app_path `$state`n}`n`# END $app_name"
    Write-Output "New Path Added"
}



## -- {Function 6 -- Show all the Paths} -- ##

# A function to make a new file and go to the file
function _Mkdir_And_CD($dirname) {
    mkdir $dirname
    Set-Location $dirname
}



## -- {Function 7 -- Forward the ports of WSL to Windows} -- ##

# A function to forward the ports of WSL to Windows
function _Forward_Port($port="") {

    # check if the permission is admin
    $admin = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    if ($admin.IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator") -eq $false) {
        Write-Output "You have to run this script as an administrator"
        return
    }
    Write-Output "This script is running as an administrator"

    # check if the port is ligal(it should be a number)
    if ($port -eq "") {
        Write-Output "You have to enter a port number"
        return
    }
    if ($port -notmatch "^[0-9]+$") {
        Write-Output "The port number should be a number"
        return
    }
    if ($port -lt 0 -or $port -gt 65535) {
        Write-Output "The port number is not ligal"
        return
    }

    # $ip_of_wsl = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -eq "vEthernet (WSL)" }).IPAddress # this is wrong
    $ip_of_wsl = (wsl.exe -- ifconfig eth0 | Select-String -Pattern "inet ").toString().Trim().Split(" ")[1]
    # $ip_of_windows = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -eq "Ethernet" -or $_.InterfaceAlias -eq "��̫��" }).IPAddress
    $ip_of_windows = "0.0.0.0"

    # bind the IP of WSL and Windows
    netsh Interface portproxy add v4tov4 listenport=$port listenaddress=$ip_of_windows connectport=$port connectaddress=$ip_of_wsl

    Write-Output "Port: $port Forwarded Successfully"
}



## -- {Function 8 -- Set a hook to the current path and Go to the hook} -- ##

# Staging the current path by setting a temporary variable
function _Set_HooK {
    $global:hook = Get-Location
    Write-Output "Hooks Set"
}

# Go to the path that is set by _Set_HooK
function _Go_HooK {
    if ($null -eq $global:hook) {
        Write-Output "You have to set a hook first"
        return
    }
    $tmp = Get-Location
    Set-Location $global:hook
    Write-Output "Hooks Go"
    $global:hook = $tmp
}



## -- {Function 9 -- Git} -- ##

# Git
function _Git {
    git add .
    # get current date
    $date = Get-Date -Format "yyMMdd"
    git commit -m $date
    git push origin master
}


function Get-Temperature {
    # the temperature of the motherboard
    $t = Get-WmiObject MSAcpi_ThermalZoneTemperature -Namespace "root/wmi"
    $returntemp = @()

    foreach ($temp in $t.CurrentTemperature) {
        $currentTempKelvin = $temp / 10
        $currentTempCelsius = $currentTempKelvin - 273.15

        $currnetTempFahrenheit = ($currentTempCelsius * 1.8) + 32

        $returntemp += ([math]::Round($currentTempCelsius, 2)).ToString() + " C : " + ([math]::Round($currnetTempFahrenheit, 2)).ToString() + " F" + " : " + ([math]::Round($currentTempKelvin, 2)).ToString() + " K"
    }

    return $returntemp
}

##### -- Function End -- #####






##### -- my scripts Start -- #####


# accept all the parameters then pass them to the script $My_Script_Dir\main.py
function _ImgAsst {
    python.exe $My_Script_Dir\ImgAsst\main.py $args
    # param(
    #     [parameter(Mandatory=$true, ValueFromPipeline=$true)]
    #     [string]
    #     $values
    # )
    # BEGIN {}
    # # pass the parameters to the script
    # PROCESS {
    #     # if values exists, then pass it to the script
    #     if ($values) {
    #         # change the values from list to a line
    #         python.exe $My_Script_Dir\ImgAsst\main.py $values
    #     }
    #     # if values does not exist, then pass the args to the script
    #     else {
    #         python.exe $My_Script_Dir\ImgAsst\main.py $args
    #     }
    # }
    # END {}
}
Set-Alias -Name img -Value _ImgAsst



function _FileExplorer {
    python.exe $My_Script_Dir\FileExplorer\main.py
}
Set-Alias -Name fe -Value _FileExplorer


##### -- my scripts End -- #####


## Atlas200Dk Function Start
function _Connect_Atlas200Dk {
    $ips = arp -a -N 192.168.137.1 | Select-String -Pattern "192.168.137.[0-9]+" | Select-Object -Skip 1 | ForEach-Object { $_.ToString().Trim().Split(" ")[0] }
    $ip = $ips[0]
    if ($null -eq $ip) {
        Write-Output "Atlas200Dk is not connected"
        return
    }
    ssh HwHiAiUser@$ip
}
## Atlas200Dk Function End


##### -- Alias Start -- #####

# Alias for _Set_HooK
Set-Alias -Name sh -Value _Set_HooK
# Alias for _Go_HooK
Set-Alias -Name gh -Value _Go_HooK
# Alias for _Mkdir_And_CD
Set-Alias -Name mkcd -Value _Mkdir_And_CD

##### -- Alias End -- #####



##### --- Module --- #####


### Module Get-ChildItemColor ###

If (-Not (Test-Path Variable:PSise)) {  # Only run this in the console and not in the ISE
    Import-Module Get-ChildItemColor # import the module

    # set the alias 'l' and 'ls' as the Get-ChildItemColor
    Set-Alias l Get-ChildItemColor -option AllScope
    Set-Alias ls Get-ChildItemColorFormatWide -option AllScope

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
        $GetChildItemColorTable.File.Add($Extension, "DarkGreen")
    }

    ForEach ($Extension in $GetChildItemColorExtensions['Image']) {
        $GetChildItemColorTable.File.Add($Extension, "DarkYello")
    }
}

### Module Get-ChildItemColor End ###



### Module PSReadline ###


# -- binded keys -- #
# [Alt + w] : SaveInHistory (save the current command in the history but do not execute it)

# [F7]      : History (show the history)
# [Ctrl + b]: BuildCurrentDirectory (build the current directory)

# [Ctrl + R]: ReverseSearchHistory (search the history)
# [Ctrl + S]: ForwardSearchHistory (search the history)

# [Ctrl + q]: TabCompleteNext (Tab acts like in bash)
# [Ctrl + Q]: TabCompletePrevious (Tab acts like in bash)

# [Ctrl + C]: Copy (clipboard interaction)
# [Ctrl + v]: Paste (clipboard interaction)

# [Ctrl + d, Ctrl + c]: CaptureScreen (good for blog posts or email showing a transaction of what you did when asking for help or demonstrating a technique)

# [Alt + d]: ShellKillWord (delete the word before the cursor)
# [Alt + Backspace]: ShellBackwardKillWord (delete the word before the cursor)

# [Alt + b]: ShellBackwardWord (move the cursor to the start of the word before the cursor)
# [Alt + f]: ShellForwardWord (move the cursor to the end of the word after the cursor)
# [Alt + B]: SelectShellBackwardWord (select the word before the cursor)
# [Alt + F]: SelectShellForwardWord (select the word after the cursor)

# [Backspace]: SmartBackspace (delete previous character or matching quotes/parens/braces)

# [Alt + (]: ParenthesizeSelection (put parens around the current selection or line)
# [Alt + ']: ToggleQuoteArgument (change the token under or before the cursor)
# [Alt + "]: ToggleQuoteArgument (change the token under or before the cursor and move the cursor to the end of the token)

# [F1]      : CommandHelp (open the help window of the current command)
# [Alt + %] : ExpandAlias (Replace all aliases with the full command)

# [Ctrl + v]: PasteAsHereString (paste the clipboard text as a here string)

# [Ctrl + J]: MarkDirectory (mark the current directory)
# [Ctrl + j]: JumpToMarkDirectory (jump to the marked directory)
# [Alt + j]: ShowMarkDirectories (show the marked directories)

# [Alt + a]: SlectCommandArgument (select the command argument)

# [F3]: ShowBinding (show the binding of the current key)

# import the module
Import-Module PSReadline

# The color option
Set-PSReadLineOption -Colors @{
#  Command            = 'Magenta'
#  Number             = 'DarkGray'
#  Member             = 'DarkGray'
#  Operator           = 'DarkGray'
#  Type               = 'DarkGray'
#  Variable           = 'DarkGreen'
#  Parameter          = 'DarkGreen'
#  ContinuationPrompt = 'DarkGreen'
#  Default            = 'DarkGray'
}

# set the file path to save the history
$_history_path = "C:\Users\KOBAYASHI\Documents\WindowsPowerShell\_history.txt"
Set-PSReadLineOption -HistorySavePath $_history_path

function _History {
    notepad $_history_path
}

# Set the source
Set-PSReadLineOption -PredictionSource History

# Shows navigable menu of all options when hitting Tab
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete

# Autocompletion for arrow keys
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward

# It will move the cursor to the end of the line when using the arrow keys to navigate through history
Set-PsReadLineOption -HistorySearchCursorMovesToEnd

# Alt + w to save the current command in the history but do not execute it
$parmeters = @{
    Key = 'Alt+w'
    BriefDescription = 'SaveInHistory'
    LongDescription = 'Save the current command in the history but do not execute it'
    ScriptBlock = {
        param($key, $arg)

        $line = $null
        $cursor = $null
        [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$cursor)

        # AddToHistory saves the line in the history, but does not execute it
        $line = $line.Trim()
        if ($line.Length -gt 0) {
            [Microsoft.PowerShell.PSConsoleReadLine]::AddToHistory($line)
        }

        # Revert is like pressing ESC
        [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
    }
}
Set-PSReadLineKeyHandler @parmeters

# Ctrl + R to search the history
Set-PSReadLineKeyHandler -Key Ctrl+R -Function ReverseSearchHistory
# Ctrl + S to search the history
Set-PSReadLineKeyHandler -Key Ctrl+S -Function ForwardSearchHistory


# This key handler shows the entire history or filtered history using Out-GridView
# The typed text is used as the substring pattern for filtering
# A selected command is inserted to the command line without invoking.
Set-PSReadLineKeyHandler -Key F7 `
                         -BriefDescription History `
                         -LongDescription "Show the history" `
                         -ScriptBlock {
    $pattern = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$pattern, [ref]$null)
    if ($pattern) {
        $pattern = [regex]::Escape($pattern)
    }

    $history = [System.Collections.ArrayList]@(
        $last = ''
        $lines = ''
        foreach ($line in [System.IO.File]::ReadLines((Get-PSReadLineOption).HistorySavePath)) {
            if ($line.EndsWith('`')) {
                $line = $line.Substring(0, $line.Length - 1)
                $lines = if ($lines) { "$lines`n$line" } else { $line }
                continue
            }

            if ($lines) {
                $line = "$lines`n$line"
                $lines = ''
            }

            if (($line -cne $last) -and (!$pattern -or ($line -match $pattern))) {
                $last = $line
                $line
            }
        }
    )
    $history.Reverse()

    $command = $history | Out-GridView -Title 'History' -PassThru
    if ($command) {
        [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
        [Microsoft.PowerShell.PSConsoleReadLine]::Insert("msbuild")
    }
}

# This is an example of a marco that you might use to execute a command.
# This will add the command to the history.
Set-PSReadLineKeyHandler -Key Ctrl+b `
                         -BriefDescription BuildCurrentDirectory `
                         -LongDescription "Build the current directory." `
                         -ScriptBlock {
    [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
    [Microsoft.PowerShell.PSConsoleReadLine]::Insert("code -r")
    [Microsoft.PowerShell.PSConsoleReadLine]::AcceptLine()
}

# In Emacs mode - Tab acts like in bash, but the Windows style completion
# is still useful sometimes, so bind some keys so we can do both
Set-PSReadLineKeyHandler -Key Ctrl+q -Function TabCompleteNext
Set-PSReadLineKeyHandler -Key Ctrl+Q -Function TabCompletePrevious

# Clipboard interaction is bound by default in Windows mode, but not Emacs mode.
Set-PSReadLineKeyHandler -Key Ctrl+C -Function Copy
Set-PSReadLineKeyHandler -Key Ctrl+v -Function Paste

# CaptureScreen is good for blog posts or email showing a transaction
# of what you did when asking for help or demonstrating a technique.
Set-PSReadLineKeyHandler -Chord 'Ctrl+d,Ctrl+c' -Function CaptureScreen

# The built-in word movement uses character delimiters, but token based word
# movement is also very useful - these are the bindings you'd use if you
# prefer the token based movements bound to the normal emacs word movement
# key bindings.
Set-PSReadLineKeyHandler -Key Alt+d -Function ShellKillWord
Set-PSReadLineKeyHandler -Key Alt+Backspace -Function ShellBackwardKillWord
Set-PSReadLineKeyHandler -Key Alt+b -Function ShellBackwardWord
Set-PSReadLineKeyHandler -Key Alt+f -Function ShellForwardWord
Set-PSReadLineKeyHandler -Key Alt+B -Function SelectShellBackwardWord
Set-PSReadLineKeyHandler -Key Alt+F -Function SelectShellForwardWord


#region Smart Insert/Delete

# The next four key handlers are designed to make entering matched quotes
# parens, and braces a nicer experience.  I'd like to include functions
# in the module that do this, but this implementation still isn't as smart
# as ReSharper, so I'm just providing it as a sample.

Set-PSReadLineKeyHandler -Key '"',"'" `
                         -BriefDescription SmartInsertQuote `
                         -LongDescription "Insert paired quotes if not already on a quote" `
                         -ScriptBlock {
    param($key, $arg)

    $quote = $key.KeyChar

    $selectionStart = $null
    $selectionLength = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetSelectionState([ref]$selectionStart, [ref]$selectionLength)

    $line = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$cursor)

    # If text is selected, just quote it without any smarts
    if ($selectionStart -ne -1)
    {
        [Microsoft.PowerShell.PSConsoleReadLine]::Replace($selectionStart, $selectionLength, $quote + $line.SubString($selectionStart, $selectionLength) + $quote)
        [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition($selectionStart + $selectionLength + 2)
        return
    }

    $ast = $null
    $tokens = $null
    $parseErrors = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$ast, [ref]$tokens, [ref]$parseErrors, [ref]$null)

    function FindToken
    {
        param($tokens, $cursor)

        foreach ($token in $tokens)
        {
            if ($cursor -lt $token.Extent.StartOffset) { continue }
            if ($cursor -lt $token.Extent.EndOffset) {
                $result = $token
                $token = $token -as [StringExpandableToken]
                if ($token) {
                    $nested = FindToken $token.NestedTokens $cursor
                    if ($nested) { $result = $nested }
                }

                return $result
            }
        }
        return $null
    }

    $token = FindToken $tokens $cursor

    # If we're on or inside a **quoted** string token (so not generic), we need to be smarter
    if ($token -is [StringToken] -and $token.Kind -ne [TokenKind]::Generic) {
        # If we're at the start of the string, assume we're inserting a new string
        if ($token.Extent.StartOffset -eq $cursor) {
            [Microsoft.PowerShell.PSConsoleReadLine]::Insert("$quote$quote ")
            [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition($cursor + 1)
            return
        }

        # If we're at the end of the string, move over the closing quote if present.
        if ($token.Extent.EndOffset -eq ($cursor + 1) -and $line[$cursor] -eq $quote) {
            [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition($cursor + 1)
            return
        }
    }

    if ($null -eq $token -or
        $token.Kind -eq [TokenKind]::RParen -or $token.Kind -eq [TokenKind]::RCurly -or $token.Kind -eq [TokenKind]::RBracket) {
        if ($line[0..$cursor].Where{$_ -eq $quote}.Count % 2 -eq 1) {
            # Odd number of quotes before the cursor, insert a single quote
            [Microsoft.PowerShell.PSConsoleReadLine]::Insert($quote)
        }
        else {
            # Insert matching quotes, move cursor to be in between the quotes
            [Microsoft.PowerShell.PSConsoleReadLine]::Insert("$quote$quote")
            [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition($cursor + 1)
        }
        return
    }

    # If cursor is at the start of a token, enclose it in quotes.
    if ($token.Extent.StartOffset -eq $cursor) {
        if ($token.Kind -eq [TokenKind]::Generic -or $token.Kind -eq [TokenKind]::Identifier -or
            $token.Kind -eq [TokenKind]::Variable -or $token.TokenFlags.hasFlag([TokenFlags]::Keyword)) {
            $end = $token.Extent.EndOffset
            $len = $end - $cursor
            [Microsoft.PowerShell.PSConsoleReadLine]::Replace($cursor, $len, $quote + $line.SubString($cursor, $len) + $quote)
            [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition($end + 2)
            return
        }
    }

    # We failed to be smart, so just insert a single quote
    [Microsoft.PowerShell.PSConsoleReadLine]::Insert($quote)
}

Set-PSReadLineKeyHandler -Key '(','{','[' `
                         -BriefDescription InsertPairedBraces `
                         -LongDescription "Insert matching braces" `
                         -ScriptBlock {
    param($key, $arg)

    $closeChar = switch ($key.KeyChar)
    {
        <#case#> '(' { [char]')'; break }
        <#case#> '{' { [char]'}'; break }
        <#case#> '[' { [char]']'; break }
    }

    $selectionStart = $null
    $selectionLength = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetSelectionState([ref]$selectionStart, [ref]$selectionLength)

    $line = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$cursor)

    if ($selectionStart -ne -1)
    {
      # Text is selected, wrap it in brackets
      [Microsoft.PowerShell.PSConsoleReadLine]::Replace($selectionStart, $selectionLength, $key.KeyChar + $line.SubString($selectionStart, $selectionLength) + $closeChar)
      [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition($selectionStart + $selectionLength + 2)
    } else {
        # No text is selected, insert a pair, check if some text is behind the cursor, if so, insert a space
        # if not, insert a pair of braces and move the cursor in between
        if ($cursor -lt $line.Length -and $line[$cursor] -ne ' ') {
            [Microsoft.PowerShell.PSConsoleReadLine]::Insert("$($key.KeyChar)")
            [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition($cursor + 1)
        }
        else
        {
            [Microsoft.PowerShell.PSConsoleReadLine]::Insert("$($key.KeyChar)$closeChar")
            [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition($cursor + 1)
        }
    }
}

Set-PSReadLineKeyHandler -Key ')',']','}' `
                         -BriefDescription SmartCloseBraces `
                         -LongDescription "Insert closing brace or skip" `
                         -ScriptBlock {
    param($key, $arg)

    $line = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$cursor)

    if ($line[$cursor] -eq $key.KeyChar)
    {
        [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition($cursor + 1)
    }
    else
    {
        [Microsoft.PowerShell.PSConsoleReadLine]::Insert("$($key.KeyChar)")
    }
}

Set-PSReadLineKeyHandler -Key Backspace `
                         -BriefDescription SmartBackspace `
                         -LongDescription "Delete previous character or matching quotes/parens/braces" `
                         -ScriptBlock {
    param($key, $arg)

    $line = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$cursor)

    if ($cursor -gt 0)
    {
        $toMatch = $null
        if ($cursor -lt $line.Length)
        {
            switch ($line[$cursor])
            {
                <#case#> '"' { $toMatch = '"'; break }
                <#case#> "'" { $toMatch = "'"; break }
                <#case#> ')' { $toMatch = '('; break }
                <#case#> ']' { $toMatch = '['; break }
                <#case#> '}' { $toMatch = '{'; break }
            }
        }

        if ($toMatch -ne $null -and $line[$cursor-1] -eq $toMatch)
        {
            [Microsoft.PowerShell.PSConsoleReadLine]::Delete($cursor - 1, 2)
        }
        else
        {
            [Microsoft.PowerShell.PSConsoleReadLine]::BackwardDeleteChar($key, $arg)
        }
    }
}

#endregion Smart Insert/Delete


# Insert text from the clipboard as a here string
Set-PSReadLineKeyHandler -Key Ctrl+V `
                         -BriefDescription PasteAsHereString `
                         -LongDescription "Paste the clipboard text as a here string" `
                         -ScriptBlock {
    param($key, $arg)

    Add-Type -Assembly PresentationCore
    if ([System.Windows.Clipboard]::ContainsText())
    {
        # Get clipboard text - remove trailing spaces, convert \r\n to \n, and remove the final \n.
        $text = ([System.Windows.Clipboard]::GetText() -replace "\p{Zs}*`r?`n","`n").TrimEnd()
        [Microsoft.PowerShell.PSConsoleReadLine]::Insert("@'`n$text`n'@")
    }
    else
    {
        [Microsoft.PowerShell.PSConsoleReadLine]::Ding()
    }
}

# Sometimes you want to get a property of invoke a member on what you've entered so far
# but you need parens to do that.  This binding will help by putting parens around the current selection,
# or if nothing is selected, the whole line.
Set-PSReadLineKeyHandler -Key 'Alt+(' `
                         -BriefDescription ParenthesizeSelection `
                         -LongDescription "Put parens around the current selection or line" `
                         -ScriptBlock {
    param($key, $arg)

    $selectionStart = $null
    $selectionLength = $null

    [Microsoft.PowerShell.PSConsoleReadLine]::GetSelectionState([ref]$selectionStart, [ref]$selectionLength)

    $line = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$cursor)
    if ($selectionStart -ne -1) {
        [Microsoft.PowerShell.PSConsoleReadLine]::Replace($selectionStart, $selectionLength, "($($line.Substring($selectionStart, $selectionLength)))")
        [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition($cursor + 2)
    }
    else {
        [Microsoft.PowerShell.PSConsoleReadLine]::Replace(0, $line.Length, "($line)")
        [Microsoft.PowerShell.PSConsoleReadLine]::EndOfLine()
    }
}

# Each time you press Alt+', this key handler will change the token
# under or before the cursor.  It will cycle through single quotes, double quotes, or
# no quotes each time it is invoked.
# the cursor will be kept at the same position
Set-PSReadLineKeyHandler -Key "Alt+'" `
                         -BriefDescription ToggleQuoteArgument `
                         -LongDescription "Toggle quotes on the argument under the cursor" `
                         -ScriptBlock {
    param($key, $arg)

    $ast = $null
    $tokens = $null
    $errors = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$ast, [ref]$tokens, [ref]$errors, [ref]$cursor)

    $cursor_record = $cursor

    $tokenToChange = $null
    foreach ($token in $tokens) {
        $extent = $token.Extent

        if ($entent.StartOffset -le $cursor -and $extent.EndOffset -ge $cursor) {

            $tokenToChange = $token

            # If the cursor is at the end (it's really 1 past the end) of the previous token,
            # we only want to change the previous token if there is no token under the cursor
            if ($extent.EndOffset -eq $cursor -and $foreach.MoveNext()) {
                $nextToken = $foreach.Current
                if ($nextToken.Extent.StartOffset -eq $cursor) {
                    $tokenToChange = $nextToken
                }
            }
            break
        }
    }

    $cursor_move = $null
    if ($tokenToChange -ne $null) {
        $extent = $tokenToChange.Extent
        $tokenText = $extent.Text

        if ($tokenText -eq "") {
            # Add single quotes
            [Microsoft.PowerShell.PSConsoleReadLine]::Insert("''")
            [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition($_cursor + 1)
            return
        }

        if ($tokenText[0] -eq '"' -and $tokenText[-1] -eq '"') {
            # Switch to no quotes
            $replacement = $tokenText.Substring(1, $tokenText.Length - 2)
            $cursor_move = -1
        }
        elseif ($tokenText[0] -eq "'" -and $tokenText[-1] -eq "'") {
            # Switch to double quotes
            $replacement = '"' + $tokenText.Substring(1, $tokenText.Length - 2) + '"'
            $cursor_move = 0
        }
        else {
            # Add single quotes
            $replacement = "'" + $tokenText + "'"
            $cursor_move = 1
        }

        [Microsoft.PowerShell.PSConsoleReadLine]::Replace(
            $extent.StartOffset,
            $tokenText.Length,
            $replacement)
    }

    [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition($cursor_record + $cursor_move)
}

# the same as above, but the cursor will move to the end of token or the end of word
Set-PSReadLineKeyHandler -Key 'Alt+"' `
                         -BriefDescription ToggleQuoteArgument `
                         -LongDescription "Toggle quotes on the argument under the cursor" `
                         -ScriptBlock {
    param($key, $arg)

    $ast = $null
    $tokens = $null
    $errors = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$ast, [ref]$tokens, [ref]$errors, [ref]$cursor)

    $tokenToChange = $null
    foreach ($token in $tokens) {
        $extent = $token.Extent

        if ($entent.StartOffset -le $cursor -and $extent.EndOffset -ge $cursor) {

            $tokenToChange = $token

            # If the cursor is at the end (it's really 1 past the end) of the previous token,
            # we only want to change the previous token if there is no token under the cursor
            if ($extent.EndOffset -eq $cursor -and $foreach.MoveNext()) {
                $nextToken = $foreach.Current
                if ($nextToken.Extent.StartOffset -eq $cursor) {
                    $tokenToChange = $nextToken
                }
            }
            break
        }
    }

    if ($tokenToChange -ne $null) {
        $extent = $tokenToChange.Extent
        $tokenText = $extent.Text

        if ($tokenText -eq "") {
            # Add single quotes
            [Microsoft.PowerShell.PSConsoleReadLine]::Insert("''")
            [Microsoft.PowerShell.PSConsoleReadLine]::EndOfLine()
            return
        }

        if ($tokenText[0] -eq '"' -and $tokenText[-1] -eq '"') {
            # Switch to no quotes
            $replacement = $tokenText.Substring(1, $tokenText.Length - 2)
        }
        elseif ($tokenText[0] -eq "'" -and $tokenText[-1] -eq "'") {
            # Switch to double quotes
            $replacement = '"' + $tokenText.Substring(1, $tokenText.Length - 2) + '"'
        }
        else {
            # Add single quotes
            $replacement = "'" + $tokenText + "'"
        }

        [Microsoft.PowerShell.PSConsoleReadLine]::Replace(
            $extent.StartOffset,
            $tokenText.Length,
            $replacement)
    }
}

# This example will replace any aliases on the command line with the resolved commands.
Set-PSReadLineKeyHandler -Key "Alt+%" `
                         -BriefDescription ExpandAliases `
                         -LongDescription "Replace all aliases with the full command" `
                         -ScriptBlock {
    param($key, $arg)

    $ast = $null
    $tokens = $null
    $errors = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$ast, [ref]$tokens, [ref]$errors, [ref]$cursor)

    $startAdjustment = 0
    foreach ($token in $tokens)
    {
        if ($token.TokenFlags -band [TokenFlags]::CommandName)
        {
            $alias = $ExecutionContext.InvokeCommand.GetCommand($token.Extent.Text, 'Alias')
            if ($alias -ne $null)
            {
                $resolvedCommand = $alias.ResolvedCommandName
                if ($resolvedCommand -ne $null)
                {
                    $extent = $token.Extent
                    $length = $extent.EndOffset - $extent.StartOffset
                    [Microsoft.PowerShell.PSConsoleReadLine]::Replace(
                        $extent.StartOffset + $startAdjustment,
                        $length,
                        $resolvedCommand)

                    # Our copy of the tokens won't have been updated, so we need to
                    # adjust by the difference in length
                    $startAdjustment += ($resolvedCommand.Length - $length)
                }
            }
        }
    }
}

# F1 for help on the command line - naturally
Set-PSReadLineKeyHandler -Key F1 `
                         -BriefDescription CommandHelp `
                         -LongDescription "Open the help window for the current command" `
                         -ScriptBlock {
    param($key, $arg)

    $ast = $null
    $tokens = $null
    $errors = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$ast, [ref]$tokens, [ref]$errors, [ref]$cursor)

    $commandAst = $ast.FindAll( {
        $node = $args[0]
        $node -is [CommandAst] -and
        $node.Extent.StartOffset -le $cursor -and
        $node.Extent.EndOffset -ge $cursor
    }, $true) | Select-Object -Last 1

    if ($commandAst -ne $null) {
        $commandName = $commandAst.GetCommandName()
        if ($commandName -ne $null) {
            $command = $ExecutionContext.InvokeCommand.GetCommand($commandName, 'All')
            if ($command -is [AliasInfo]) {
                $command = $command.ResolvedCommandName
            }
            if ($commandName -ne $null) {
                Get-Help $commandName -ShowWindow
            }
        }
    }
}


# Ctrl+Shift+j then type a key to mark the current directory.
# Ctrl+j then the same key will change back to that directory without
# needing to type cd and won't change the command line.

$global:PSReadLineMarks = @{}

Set-PSReadLineKeyHandler -Key Ctrl+J `
                         -BriefDescription MarkDirectory `
                         -LongDescription "Mark the current directory" `
                         -ScriptBlock {
    param($key, $arg)

    $key = [Console]::ReadKey($true)
    $global:PSReadLineMarks[$key.KeyChar] = $pwd
}

Set-PSReadLineKeyHandler -Key Ctrl+j `
                         -BriefDescription JumpDirectory `
                         -LongDescription "Goto the marked directory" `
                         -ScriptBlock {
    param($key, $arg)

    $key = [Console]::ReadKey()
    $dir = $global:PSReadLineMarks[$key.KeyChar]
    if ($dir) {
        Set-Location $dir
        [Microsoft.PowerShell.PSConsoleReadLine]::InvokePrompt()
    }
}

Set-PSReadLineKeyHandler -Key Alt+j `
                         -BriefDescription ShowDirectoryMarks `
                         -LongDescription "Show the currently marked directories" `
                         -ScriptBlock {
    param($key, $arg)

    $global:PSReadLineMarks.GetEnumerator() | ForEach-Object {
        [PSCustomObject]@{Key = $_.Key; Dir = $_.Value} |
        Format-Table -AutoSize | Out-Host
    }

    [Microsoft.PowerShell.PSConsoleReadLine]::InvokePrompt()
}

# Auto correct 'git cmt' to 'git commit'
Set-PSReadLineOption -CommandValidationHandler {
    param([CommandAst]$CommandAst)

    switch ($CommandAst.GetCommandName()) {
        'git' {
            $gitCmd = $CommandAst.CommandElements[1].Extent
            switch ($gitCmd.Text) {
                'cmt' {
                    [Microsoft.PowerShell.PSConsoleReadLine]::Replace(
                        $gitCmd.StartOffset, $gitCmd.EndOffset - $gitCmd.StartOffset, 'commit')
                }
            }
        }
    }
}


# `ForwardChar` accepts the entrie suggestio text when the cursor is at the end of the line
# This custom binding makes `RightArrow` behave similarly - accepting the next word instead of the entire suggestion text.
Set-PSReadLineKeyHandler -Key RightArrow `
                         -BriefDescription ForwardCharAndAcceptNextSuggestionWord `
                         -LongDescription "Move cursor one character to the right in the current editing line and accept the next word in suggestion when it's at the end of current editing line" `
                         -ScriptBlock {
    param($key, $arg)

    $line = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$cursor)

    if ($cursor -lt $line.Length) {
        [Microsoft.PowerShell.PSConsoleReadLine]::ForwardChar($key, $arg)
    } else {
        [Microsoft.PowerShell.PSConsoleReadLine]::AcceptNextSuggestionWord($key, $arg)
    }
}


# Cycle through arguments on current line and select the text. This makes it easier to quickly change the argument if re-running a previously run command from the history
# or if using a psreadline predictor. You can also use a digit argument to specify which argument you want to select, i.e. Alt+1, Alt+a selects the first argument
# on the command line.
Set-PSReadLineKeyHandler -Key Alt+a `
                         -BriefDescription SelectCommandArguments `
                         -LongDescription "Set current selection to next command argument in the command line. Use of digit argument selects argument by position" `
                         -ScriptBlock {
    param($key, $arg)

    $ast = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$ast, [ref]$null, [ref]$null, [ref]$cursor)

    $asts = $ast.FindAll( {
        $args[0] -is [System.Management.Automation.Language.ExpressionAst] -and
        $args[0].Parent -is [System.Management.Automation.Language.CommandAst] -and
        $args[0].Extent.StartOffset -ne $args[0].Parent.Extent.StartOffset
      }, $true)

    if ($asts.Count -eq 0) {
        [Microsoft.PowerShell.PSConsoleReadLine]::Ding()
        return
    }

    $nextAst = $null

    if ($null -ne $arg) {
        $nextAst = $asts[$arg - 1]
    }
    else {
        foreach ($ast in $asts) {
            if ($ast.Extent.StartOffset -ge $cursor) {
                $nextAst = $ast
                break
            }
        }

        if ($null -eq $nextAst) {
            $nextAst = $asts[0]
        }
    }

    $startOffsetAdjustment = 0
    $endOffsetAdjustment = 0

    if ($nextAst -is [System.Management.Automation.Language.StringConstantExpressionAst] -and
        $nextAst.StringConstantType -ne [System.Management.Automation.Language.StringConstantType]::BareWord) {
            $startOffsetAdjustment = 1
            $endOffsetAdjustment = 2
    }

    [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition($nextAst.Extent.StartOffset + $startOffsetAdjustment)
    [Microsoft.PowerShell.PSConsoleReadLine]::SetMark($null, $null)
    [Microsoft.PowerShell.PSConsoleReadLine]::SelectForwardChar($null, ($nextAst.Extent.EndOffset - $nextAst.Extent.StartOffset) - $endOffsetAdjustment)
}


Set-PSReadLineKeyHandler -Key F3 `
                         -BriefDescription ShowKeyBindings `
                         -LongDescription "Show the current key bindings" `
                         -ScriptBlock {
    param($key, $arg)

    $keyBindings = [Microsoft.PowerShell.PSConsoleReadLine]::GetKeyHandlers()
    # show in by Out-GridView
    $command = $keyBindings | Out-GridView -Title 'Key Bindings' -PassThru
    if ($command) {
        [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
        [Microsoft.PowerShell.PSConsoleReadLine]::Insert($command -join "`n")
    }
}


### Module PSReadLine End ###



### Module Anaconda ###

#region conda initialize
# !! Contents within this block are managed by 'conda init' !!
function _Conda_Init {
    (& "D:\Program\anaconda3\Scripts\conda.exe" "shell.powershell" "hook") | Out-String | Invoke-Expression
}
#endregion

### Module Anaconda End ###

##### --- Module End --- #####



;
### User's Paths ###

# Clash for Windows
function Clash($state="start") {
    $app_path = 'D:\Item\Clash for Windows\Clash for Windows.exe'
    _Start_and_Kill $app_path $state > $null
}
# END Clash for Windows


# Free Download Manager
function FDM($state="start") {
    $app_path = 'D:\Item\Free Download Manager\fdm.exe'
    _Start_and_Kill $app_path $state
}
# END Free Download Manager


# Everything
function Everything($state="start") {
    $app_path = 'D:\Item\Everything\Everything.exe'
    _Start_and_Kill $app_path $state
}
# END Everything


# ShareMouse
function ShareMouse($state="start") {
    if ($state -eq "KEY") {
        Write-Output "SMOENT-DO-AAGEMY-1299-UN-KKPX-QTSX-X9JHRR1LXHX5ZXTB-FEEB32EF75C43CE5F220B324678701CB" | Set-Clipboard
        return
    }
    $app_path = 'C:\Program Files (x86)\ShareMouse\ShareMouse.exe'
    _Start_and_Kill $app_path $state
}
# END ShareMouse


function CodeServer { # the application in wsl
    wsl.exe -- /mnt/d/Program/code-server-3.10.2-linux-amd64/code-server /mnt/d/Program/Code
}


