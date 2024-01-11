$My_Script_Path = 'C:\Users\KOBAYASHI\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1'

# Start or Kill a Process
function _Start_and_Kill($app_path, $state="start") {
    # Write-Output $app_path $state
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

# A function for editing this Sctipt
function _Edit_My_Script {
    powershell_ise $My_Script_Path
}

# A function for showing all current Paths
function _Show_Path() {
    # Write-Output $My_Script_Path
    Write-Output "===================="
    (Get-Content -Path $My_Script_Path -Raw).Split(";")[-1] | Write-Output
    Write-Output "===================="
}

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

    # Write-Output $line1 $line2 $len

    $old_content = Get-Content -Path $My_Script_Path -ReadCount 0
    $new_content = @()
    for($i = 0; $i -lt $old_content.Length; $i += 1) {
        if ($i -gt $line1-1 -and $i -lt $line1+$len+1 ) {
            # Write-Output $old_content[$i]
        } else {
            $new_content += $old_content[$i]
        }
    }
    # Write-Output $new_content
    Set-Content -Path $My_Script_Path -Value $new_content
    Write-Output "Path Deleted"
}

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



# Moudle

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

# import the module
Import-Module PSReadline

$_history_path = "C:\Users\KOBAYASHI\Documents\WindowsPowerShell\_history.txt"

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

### Module PSReadLine End ###

### Module Anaconda ###

#region conda initialize
# !! Contents within this block are managed by 'conda init' !!
(& "D:\Program\Anaconda\Scripts\conda.exe" "shell.powershell" "hook") | Out-String | Invoke-Expression
#endregion

### Module Anaconda End ###

# Moudle End



;
### User's Paths ###

