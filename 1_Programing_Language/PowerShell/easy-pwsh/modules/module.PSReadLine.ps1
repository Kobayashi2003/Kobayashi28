using namespace System.Management.Automation
using namespace System.Management.Automation.Language


Set-PSReadLineOption -BellStyle None
# Set-PSReadLineOption -EditMode Emacs
Set-PSReadLineOption -EditMode Windows

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

Set-PSReadLineOption -PromptText ' > ' # change the ' > ' character red
Set-PSReadLineOption -PromptText ' > ', ' X ' # replace the ' > ' character with a red ' X '

# set the file path to save the history

$history_save_path = (Split-Path $profile.CurrentUserAllHosts) + "\.ps_history"
# $history_save_path = (Join-Path $global:CURRENT_SCRIPT_DIRECTORY -ChildPath "config\.ps_history")

Set-PSReadLineOption -HistorySavePath $history_save_path
Set-PSReadLineOption -HistorySaveStyle SaveIncrementally
Set-PSReadLineOption -PredictionSource HistoryAndPlugin
Set-PSReadLineOption -MaximumHistoryCount 100000

# $history_save_path = (Get-PSReadLineOption).HistorySavePath

# set the filter for the history
Set-PSReadLineOption -AddToHistoryHandler {
    param([string]$line)

    $sensitive = "password|asplaintext|token|key|secret|galgame|eroi"
    return ($line -notmatch $sensitive)
}

# prediction configuration
Set-PSReadLineOption -PredictionSource History
# Set-PSReadLineOption -PredictionViewStyle ListView
Set-PSReadLineOption -PredictionViewStyle InlineView

# Shows navigable menu of all options when hitting Tab
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete

# Autocompletion for arrow keys
Set-PSReadLineOption -HistoryNoDuplicates
Set-PSReadLineOption -HistorySearchCursorMovesToEnd
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward

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
# TODO: Unfortunately, revertline may not work as expected when you use listview completion.

# Set-PSReadLineKeyHandler -Key Ctrl+b `
#                          -LongDescription "Open Visual Studio Code" `
#                          -ScriptBlock {
#     [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
#     [Microsoft.PowerShell.PSConsoleReadLine]::Insert('code -r')
#     [Microsoft.PowerShell.PSConsoleReadLine]::AcceptLine()
# }

Set-PSReadLineKeyHandler -Key Ctrl+b `
                         -LongDescription "Cursor" `
                         -ScriptBlock {
    [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
    [Microsoft.PowerShell.PSConsoleReadLine]::Insert('cursor -r')
    [Microsoft.PowerShell.PSConsoleReadLine]::AcceptLine()
}

Set-PSReadLineKeyHandler -Key Ctrl+H `
                         -LongDescription "Computer sleep" `
                         -ScriptBlock {
    [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
    [Microsoft.PowerShell.PSConsoleReadLine]::Insert('shutdown -h')
    [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition(0)
    [Microsoft.PowerShell.PSConsoleReadLine]::SelectLine()
    # [Microsoft.PowerShell.PSConsoleReadLine]::AcceptLine()
}

Set-PSReadLineKeyHandler -Key Ctrl+g -ScriptBlock {
    if (Get-Command git -ErrorAction SilentlyContinue) {
        [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
        [Microsoft.PowerShell.PSConsoleReadLine]::Insert('git pull')
        [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition(0)
        [Microsoft.PowerShell.PSConsoleReadLine]::SelectLine()
        # [Microsoft.PowerShell.PSConsoleReadLine]::AcceptLine()
    }
}

Set-PSReadLineKeyHandler -Key Ctrl+G -ScriptBlock {
    if (Get-Command git -ErrorAction SilentlyContinue) {
        [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
        $commitMessage = Get-Date -Format "yyyy-MM-dd-HH-mm-ss"
        $command = "git add . ; git commit -m '$commitMessage' ; git push"
        [Microsoft.PowerShell.PSConsoleReadLine]::Insert($command)
        $cursorPosition = $command.IndexOf($commitMessage)
        [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition($cursorPosition)
        [Microsoft.PowerShell.PSConsoleReadLine]::SelectForwardChar($null, $commitMessage.Length)
    }
}

# In Emacs mode - Tab acts like in bash, but the Windows style completion
# is still useful sometimes, so bind some keys so we can do both
Set-PSReadLineKeyHandler -Key Ctrl+q -Function TabCompleteNext
Set-PSReadLineKeyHandler -Key Ctrl+Q -Function TabCompletePrevious

# Clipboard interaction is bound by default in Windows mode, but not Emacs mode.
# Set-PSReadLineKeyHandler -Key Ctrl+C -Function Copy
Set-PSReadLineKeyHandler -Key Ctrl+v -Function Paste

Set-PSReadLineKeyHandler -Chord 'Ctrl+z' -Function Undo
Set-PSReadLineKeyHandler -Chord 'Ctrl+y' -Function Redo

Set-PSReadLineKeyHandler -Chord 'Ctrl+d' -Function DeleteChar
Set-PSReadLineKeyHandler -Chord 'Ctrl+w' -Function BackwardDeleteWord

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

<# TODO
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
            [Microsoft.PowerShell.PSConsoleReadLine]::Insert("$quote$quote")
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
#>

<# TODO
Set-PSReadLineKeyHandler -Key '(','{','[' `
                         -BriefDescription InsertPairedBraces `
                         -LongDescription "Insert matching braces" `
                         -ScriptBlock {
    param($key, $arg)

    $closeChar = switch ($key.KeyChar)
    {
        '(' { [char]')'; break }
        '{' { [char]'}'; break }
        '[' { [char]']'; break }
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
#>

<# TODO
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
#>

<#TODO
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
                '"' { $toMatch = '"'; break }
                "'" { $toMatch = "'"; break }
                ')' { $toMatch = '('; break }
                ']' { $toMatch = '['; break }
                '}' { $toMatch = '{'; break }
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
#>

#endregion Smart Insert/Delete

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

# Auto correct common typos
Set-PSReadLineOption -CommandValidationHandler {
    param([CommandAst]$CommandAst)

    $cmdMap = @{
        'git' = @{
            's'     = 'status'
            'a'     = 'add .'
            'p'     = 'push'
            'cl'    = 'clone'
            'cmt'   = 'commit'
            'undo'= '@whole:git reset --mixed HEAD~1'
            'master' = "@whole:git checkout master --"
            'quickpush' = "@whole:git add . ; git commit -m $(Get-Date -Format 'yyMMdd') ; git push"
            'prettylog'  = '@whole:git log --no-merges --color --stat --graph --date=format:"%Y-%m-%d %H:%M:%S" --pretty=format:"%Cred%h%Creset -%C(yellow)%d%Cblue %s %Cgreen(%cd) %C(bold blue)<%an>%Creset" --abbrev-commit'
            'shallowclone'= '@whole:git clone --depth 1 --filter=blob:none --no-checkout'
            'proxyon'  = '@whole:git config --global http.proxy http://127.0.0.1:7890 ; git config --global https.proxy http://127.0.0.1:7890'
            'proxyoff' = '@whole:git config --global --unset http.proxy ; git config --global --unset https.proxy'
        }
        'conda' = @{
            'a' = 'activate'
            'd' = 'deactivate'
            'i' = 'info'
            'l' = 'env list'
        }
        'pixi' = @{
            'shell' = 'shell --change-ps1 false'
        }
        'cd' = @{
            '...'  = '../..'
        }
    }

    if ($cmdMap.ContainsKey($CommandAst.GetCommandName()) -And
        $cmdMap[$CommandAst.GetCommandName()].ContainsKey($CommandAst.CommandElements[1].Extent.Text)) {

        $cmdBase = $CommandAst.CommandElements[0].Extent
        $cmdArg  = $CommandAst.CommandElements[1].Extent
        $newCont = $cmdMap[$CommandAst.GetCommandName()][$CommandAst.CommandElements[1].Extent.Text]

        if ($newCont -match '^@whole:') {
            [Microsoft.PowerShell.PSConsoleReadLine]::Replace(
                $cmdBase.StartOffset, $cmdArg.EndOffset - $cmdBase.StartOffset,
                $newCont.SubString($newCont.IndexOf(':') + 1))
        } else {
            [Microsoft.PowerShell.PSConsoleReadLine]::Replace(
                $cmdArg.StartOffset, $cmdArg.EndOffset - $cmdArg.StartOffset,
                $newCont)
        }
    }
}
# This checks the validation script when you hit enter
Set-PSReadLineKeyHandler -Chord Enter -Function ValidateAndAcceptLine

# Custom completion for common commands
$scriptblock = {
    param($wordToComplete, $commandAst, $cursorPosition)
    $customCompletions = @{
        'git' = @('status', 'add', 'commit', 'push', 'pull', 'clone', 'checkout', 'branch', 'merge', 'rebase', 'log', 'fetch', 'remote')
        'deno' = @('run', 'compile', 'bundle', 'test', 'lint', 'fmt', 'cache', 'info', 'doc', 'upgrade', 'repl', 'eval', 'task')
        'conda' = @('create', 'activate', 'deactivate', 'install', 'update', 'remove', 'list', 'search', 'info', 'config', 'clean', 'env')
        'docker' = @('run', 'build', 'pull', 'push', 'images', 'ps', 'stop', 'start', 'restart', 'exec', 'logs', 'volume', 'network')
        'yarn' = @('add', 'remove', 'install', 'upgrade', 'init', 'run', 'info', 'licenses', 'list', 'why', 'create', 'set', 'config')
        'powershell' = @('-Command', '-File', '-ExecutionPolicy', '-NoProfile', '-NonInteractive', '-WindowStyle', '-Version')
        'pip' = @('install', 'uninstall', 'freeze', 'list', 'show', 'check', 'download', 'config', 'search', 'wheel', 'hash', 'completion')
        'npm' = @('install', 'start', 'run', 'test', 'build', 'update', 'init', 'publish', 'list', 'search', 'audit', 'outdated')
        'winget' = @('install', 'show', 'list', 'search', 'upgrade', 'uninstall', 'source', 'hash', 'validate', 'settings', 'features', 'export', 'import')
        'choco' = @('install', 'upgrade', 'uninstall', 'list', 'search', 'info', 'outdated', 'pin', 'source', 'config', 'feature', 'apikey')
        'scoop' = @('install', 'uninstall', 'update', 'list', 'search', 'info', 'status', 'bucket', 'cleanup', 'config', 'cache', 'help', 'home', 'hold', 'prefix', 'reset', 'virustotal', 'which')
    }

    $command = $commandAst.CommandElements[0].Value
    if ($customCompletions.ContainsKey($command)) {
        $customCompletions[$command] | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object {
            [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
        }
    }
}
Register-ArgumentCompleter -Native -CommandName git, npm, deno, conda, docker, pip, yarn, powershell, winget, choco -ScriptBlock $scriptblock

$scriptblock = {
    param($wordToComplete, $commandAst, $cursorPosition)
    dotnet complete --position $cursorPosition $commandAst.ToString() |
        ForEach-Object {
            [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
        }
}
Register-ArgumentCompleter -Native -CommandName dotnet -ScriptBlock $scriptblock

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

# Set Ctrl+Backspace to delete the previous word
Set-PSReadLineKeyHandler -Key Ctrl+Backspace `
                         -BriefDescription DeletePreviousWord `
                         -LongDescription "Delete the previous word" `
                         -ScriptBlock {
    param($key, $arg)

    $selectionStart = $null
    $selectionLength = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetSelectionState([ref]$selectionStart, [ref]$selectionLength)

    $line = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$cursor)

    # If text is selected, delete the selection
    if ($selectionLength -gt 0) {
        [Microsoft.PowerShell.PSConsoleReadLine]::Delete($selectionStart, $selectionLength)
        return
    }

    # if the cursor is not at the end of any word,
    # find and delete whitespace until the cursor is at the end of a word
    $lastWordEnd = $cursor
    while ($lastWordEnd -gt 0 -and $line[$lastWordEnd - 1] -match '\s') {
        $lastWordEnd--
    }
    if ($lastWordEnd -ne $cursor) {
        [Microsoft.PowerShell.PSConsoleReadLine]::Delete($lastWordEnd, $cursor - $lastWordEnd)
        return
    }

    [Microsoft.PowerShell.PSConsoleReadLine]::BackwardKillWord($key, $arg)
}

# Set Ctrl+LeftArrow to move the cursor to the beginning of the previous word
Set-PSReadLineKeyHandler -Key Ctrl+LeftArrow `
                         -BriefDescription MoveToPreviousWord `
                         -LongDescription "Move the cursor to the beginning of the previous word" `
                         -ScriptBlock {
    param($key, $arg)

    $special_chars = @('/','\','(',')','{','}','[',']','<','>','"','''','`', ':', '.', ';')

    $line = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$cursor)

    $lastWordEnd = $cursor
    if ($line[$cursor - 1] -match '\s') {
        while ($lastWordEnd -gt 0 -and $line[$lastWordEnd - 1] -match '\s') {
            $lastWordEnd--
        }
    } elseif ($line[$cursor - 1] -in $special_chars) {
        $lastWordEnd--
    } else {
        while ($lastWordEnd -gt 0 -and $line[$lastWordEnd - 1] -notmatch '\s') {
            if ($line[$lastWordEnd - 1] -in $special_chars) {
                break
            }
            $lastWordEnd--
        }
    }

    [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition($lastWordEnd)
}

# Set Ctrl+RightArrow to move the cursor to the end of the next word
Set-PSReadLineKeyHandler -Key Ctrl+RightArrow `
                         -BriefDescription MoveToNextWord `
                         -LongDescription "Move the cursor to the end of the next word" `
                         -ScriptBlock {
    param($key, $arg)


    $special_chars = @('/','\','(',')','{','}','[',']','<','>','"','''','`', ':', '.', ';')

    $line = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$cursor)

    # if is the end of line, accept the next suggestion word
    if ($cursor -eq $line.Length) {
        [Microsoft.PowerShell.PSConsoleReadLine]::AcceptNextSuggestionWord($key, $arg)
        return
    }

    $nextWordStart = $cursor
    if ($line[$cursor] -match '\s') {
        while ($nextWordStart -lt $line.Length - 1 -and $line[$nextWordStart] -match '\s') {
            $nextWordStart++
        }
    } elseif ($line[$cursor] -in $special_chars) {
        $nextWordStart++
    } else {
        while ($nextWordStart -lt $line.Length - 1 -and $line[$nextWordStart] -notmatch '\s') {
            if ($line[$nextWordStart] -in $special_chars) {
                break
            }
            $nextWordStart++
        }
        if ($nextWordStart -eq $line.Length - 1) {
            $nextWordStart++
        }
    }

    [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition($nextWordStart)
}

# Set Ctrl+UpArrow to execute the previous command
Set-PSReadLineKeyHandler -Key Ctrl+UpArrow `
                         -BriefDescription ExecutePreviousCommand `
                         -LongDescription "Execute the previous command" `
                         -ScriptBlock {
    $history = Get-History
    if ($history.Count -gt 0) {
        $lastCommand = $history[-1].CommandLine
        [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
        [Microsoft.PowerShell.PSConsoleReadLine]::Insert($lastCommand)
        [Microsoft.PowerShell.PSConsoleReadLine]::AcceptLine()
    }
}

# Set Shift+UpArrow to execute the previous command under admin privileges
Set-PSReadLineKeyHandler -Key Shift+UpArrow `
                         -BriefDescription ExecutePreviousAdminCommand `
                         -LongDescription "Execute the previous command under admin privileges" `
                         -ScriptBlock {
    $history = Get-History
    if (($history.Count -gt 0) -and (Get-Command 'sudo' -ErrorAction SilentlyContinue)) {
        $lastCommand = $history[-1].CommandLine
        $command = 'sudo ' + $lastCommand
        [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
        [Microsoft.PowerShell.PSConsoleReadLine]::Insert($command)
        [Microsoft.PowerShell.PSConsoleReadLine]::AcceptLine()
    }
}

# set Ctrl+DownArrow to insert a copy of the last command at the cursor position
set-psreadlinekeyhandler -key Ctrl+DownArrow `
                         -briefdescription copylastcommand `
                         -longdescription "insert a copy of the last command at the cursor position" `
                         -scriptblock {
    $history = get-history
    if ($history.count -gt 0) {
        $lastcommand = $history[-1].commandline
        [microsoft.powershell.psconsolereadline]::insert($lastcommand)
    }
}

# Set Ctrl+Enter to add the current line to history, but don't execute it
Set-PSReadLineKeyHandler -Key Ctrl+Enter `
                         -BriefDescription AddLineToHistory `
                         -LongDescription "Add the current line to history" `
                         -ScriptBlock {
    param($key, $arg)

    $line = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$cursor)

    $line = $line.Trim()
    if ($line.Length -gt 0) {
        [Microsoft.PowerShell.PSConsoleReadLine]::AddToHistory($line)
    }

    [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
}

# Set Escape to clear the current line
Set-PSReadLineKeyHandler -Key Escape `
                         -BriefDescription ClearLine `
                         -LongDescription "Clear the current line" `
                         -ScriptBlock {
        param($key, $arg)
        if ([Microsoft.PowerShell.PSConsoleReadLine]::EditMode -eq 'Vi') {
            [Microsoft.PowerShell.PSConsoleReadLine]::ViCommandMode
            return
        }
        [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
}


function global:__Check-Path {
<#
.SYNOPSIS
    Checks if a path is valid
.PARAMETER Path
    Path to check
.OUTPUTS
    Boolean
#>
    param (
        [Parameter(Mandatory = $true)]
        [string[]] $path
    )

    try {
        # $path = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($path)
        $path = (Get-Item $path).FullName
        if (-not $path) {
            throw 'Invalid path'
        }
        foreach ($p in $path) {
            if (-not (Test-Path -LiteralPath $p)) {
                Write-Host ERROR2 $path -ForegroundColor Red
                throw 'Path does not exist'
            }
        }
        return $true
    } catch {
        return $false
    }
}

function global:__Get-Selection {
<#
.SYNOPSIS
    Gets the current selection
.OUTPUTS
    String
#>

    $line = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$cursor)

    $selectionStart = $null
    $selectionLength = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetSelectionState([ref]$selectionStart, [ref]$selectionLength)
    if ($selectionStart -ne -1 -and $selectionLength -ne -1) {
        return $line.SubString($selectionStart, $selectionLength)
    }
    return $null
}

function global:__Replace-Selection { param (
    [Parameter(Mandatory = $true)]
    [string[]] $Text
)
<#
.SYNOPSIS
    Replaces the current selection
.PARAMETER Text
    Text to replace with
.OUTPUTS
    [Boolean]
#>
    $selectionStart = $null
    $selectionLength = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetSelectionState([ref]$selectionStart, [ref]$selectionLength)

    if ($selectionStart -ne -1 -and $selectionLength -ne -1) {
        [Microsoft.PowerShell.PSConsoleReadLine]::Replace($selectionStart, $selectionLength, $Text)
        return $true
    }
    return $false
}

function global:__Get-Around-Cursor {
<#
.SYNOPSIS
    Gets the content around the cursor
.OUTPUTS
    String
#>

    $line = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$cursor)

    $ast = $null
    $tokens = $null
    $errors = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$ast, [ref]$tokens, [ref]$errors, [ref]$cursor)
    foreach ($token in $tokens) {
        if ($token.Extent.StartOffset -le $cursor -and $token.Extent.EndOffset -ge $cursor) {
            return $line.SubString($token.Extent.StartOffset, ($token.Extent.EndOffset - $token.Extent.StartOffset))
        }
    }

    return $null
}

function global:__Replace-Around-Cursor { param(
    [Parameter(Mandatory = $true)]
    [string[]] $Text
)
<#
.SYNOPSIS
    Replaces the content around the cursor
.PARAMETER Text
    Text to replace with
.OUTPUTS
    None
#>
    $ast = $null
    $tokens = $null
    $errors = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$ast, [ref]$tokens, [ref]$errors, [ref]$cursor)
    foreach ($token in $tokens) {
        if ($token.Extent.StartOffset -le $cursor -and $token.Extent.EndOffset -ge $cursor) {
            [Microsoft.PowerShell.PSConsoleReadLine]::Replace($token.Extent.StartOffset, $token.Extent.EndOffset - $token.Extent.StartOffset, $Text)
            return $true
        }
    }

    return $false
}


# This may slow down your console
$USE_GLOBAL_CLIPACTION = $false

function global:__Reset-ClipAction {
    if ($USE_GLOBAL_CLIPACTION) {
        [Environment]::SetEnvironmentVariable('CLIPACTION', $null, 'User')
    } else {
        $env:CLIPACTION = $null
    }
}
& __Reset-ClipAction

function global:__Reload-ClipAction {
    if ($USE_GLOBAL_CLIPACTION) {
        $env:CLIPACTION = [System.Environment]::GetEnvironmentVariable("CLIPACTION","User")
    }
}

function global:__Set-ClipAction { param (
    [Parameter(Mandatory = $true)]
    [ValidateSet('copy', 'cut', 'link')]
    [string] $action
)
    if ($USE_GLOBAL_CLIPACTION) {
        [Environment]::SetEnvironmentVariable('CLIPACTION', $action, 'User')
    } else {
        $env:CLIPACTION = $action
    }
}

function global:__Copy-Files {

    $path = __Get-Selection
    if (-not $path) {
        $path = __Get-Around-Cursor
    }
    if (-not $path) {
        return
    }
    if (-not (__Check-Path -Path $path)) {
        return
    }

    try {
        if ($global:PSVERSION -lt 6) {
            Set-Clipboard -Path $path
        } else {
            Add-Type -AssemblyName System.Windows.Forms

            $files = [System.Collections.Specialized.StringCollection]::new()
            $files.Add((Get-Item $path).FullName) >$null

            [System.Windows.Forms.Clipboard]::SetFileDropList($files)
        }
    } catch {
        Write-Error $_
    }
}

function global:__Paste-Files {
    param (
        [Parameter(Mandatory = $true)]
        [string[]] $paths,
        [Parameter(Mandatory = $false)]
        [ValidateSet('copy', 'cut', 'link')]
        [string] $action = 'copy'
    )
    if ($paths.Count -eq 0) {
        return
    }
    foreach ($path in $paths) {

        if (Test-Path -Path (Join-Path $pwd (Split-Path $path -Leaf))) {
            Write-Host "`n⚠️ File already exists in $path" -nonewline
            continue
        }

        try {
            if ($action -eq 'copy') {
                Copy-Item -Path $path -Destination $pwd
            } elseif ($action -eq 'cut') {
                Move-Item -Path $path -Destination $pwd
            } elseif ($action -eq 'link') {
                New-Item -Path $pwd -ItemType SymbolicLink -Value $path
            }
        } catch {
            Write-Error $_
        }
    }
}

Set-PSReadLineKeyHandler -Key Ctrl+C `
                         -BriefDescription CopyFile `
                         -LongDescription "Copy the file to the clipboard" `
                         -ScriptBlock {
    & __Copy-Files
    & __Set-ClipAction -action 'copy'
    & __Reload-ClipAction
}

Set-PSReadLineKeyHandler -Key Ctrl+X `
                         -BriefDescription CutFile `
                         -LongDescription "Cut the file to the clipboard" `
                         -ScriptBlock {
    & __Copy-Files
    & __Set-ClipAction -action 'cut'
    & __Reload-ClipAction
}

Set-PSReadLineKeyHandler -Key Ctrl+L `
                         -BriefDescription CreateFileLink `
                         -LongDescription "Create File Link" `
                         -ScriptBlock {
    & __Copy-Files
    & __Set-ClipAction -action 'link'
    & __Reload-ClipAction
}

Set-PSReadLineKeyHandler -Key Ctrl+V `
                         -BriefDescription PasteAsHereString `
                         -LongDescription "Paste the clipboard text as a here string" `
                         -ScriptBlock {

    param($key, $arg)

    if ($global:PSVERSION -lt 6) {
        $files = Get-Clipboard -Format FileDrop
    } else {
        Add-Type -AssemblyName System.Windows.Forms
        $files = [System.Windows.Forms.Clipboard]::GetFileDropList()
    }

    if ($files.Count -gt 0) {
        & __Reload-ClipAction
        if ($env:CLIPACTION) {
            & __Paste-Files -action $env:CLIPACTION -paths $files
            & __Reset-ClipAction
        } else {
            & __Paste-Files -paths $files
        }
        return
    }

    & __Reset-ClipAction

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

Set-PSReadLineKeyHandler -Key Ctrl+p `
                         -BriefDescription ShowAbsolutePath `
                         -LongDescription "Show the full path" `
                         -ScriptBlock {

    $path = & __Get-Selection
    if (-not $path) {
        $path = & __Get-Around-Cursor
    }
    if (-not $path) {
        return
    }
    if (-not (& __Check-Path -Path $path)) {
        return
    }

    $absolutePath = (Get-Item -Path $path).FullName

    if (& __Replace-Selection -Text $absolutePath) {
        return
    }

    & __Replace-Around-Cursor -Text $absolutePath | Out-Null
}

# ctrl + <space>
Set-PSReadLineKeyHandler -Key Ctrl+SpaceBar `
                         -ScriptBlock {

    if (-not (Get-Command 'quicklook' -ErrorAction SilentlyContinue)) {
        return
    }

    $path = & __Get-Selection
    if (-not $path) {
        $path = & __Get-Around-Cursor
    }
    if (-not $path) {
        $path = Get-Location
    }
    if (-not (& __Check-Path -Path $path)) {
        return
    }

    $absolutePath = (Get-Item -Path $path).FullName

    try {
        & quicklook $absolutePath
    } catch {
        Write-Error $_
    }
}

Set-PSReadLineKeyHandler -Key Ctrl+u `
                         -BriefDescription GoToBeginningOfLine `
                         -LongDescription "Move cursor to beginning of line" `
                         -ScriptBlock {

    [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition(0)
}

Set-PSReadLineKeyHandler -Key Ctrl+U `
                         -BriefDescription GoToEndOfLine `
                         -LongDescription "Move cursor to end of line" `
                         -ScriptBlock {
    $line = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$cursor)
    [Microsoft.PowerShell.PSConsoleReadLine]::SetCursorPosition($line.Length)
}

Set-PSReadLineKeyHandler -Key Alt+u `
                         -BriefDescription DelectToBeginningOfLine `
                         -LongDescription "Delete from cursor to beginning of line" `
                         -ScriptBlock {
    $line = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$cursor)
    [Microsoft.PowerShell.PSConsoleReadLine]::Delete(0, $cursor)
}

Set-PSReadLineKeyHandler -Key Alt+U `
                         -BriefDescription DelectToEndOfLine `
                         -LongDescription "Delete from cursor to end of line" `
                         -ScriptBlock {
    $line = $null
    $cursor = $null
    [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState([ref]$line, [ref]$cursor)
    [Microsoft.PowerShell.PSConsoleReadLine]::Delete($cursor, $line.Length - $cursor)
}