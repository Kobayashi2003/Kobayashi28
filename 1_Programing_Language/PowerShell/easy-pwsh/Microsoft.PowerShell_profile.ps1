using namespace System.Management.Automation
using namespace System.Management.Automation.Language

$My_Script_Path  = $MyInvocation.MyCommand.Definition
$My_Script_Dir   = Split-Path $My_Script_Path
$My_History_Filename = "my-history.txt"
$My_History_Path = $My_Script_Dir + "\" + $My_History_Filename

$Remote_Repository_Address = "" # the address of the remote repository of git
$Remote_Repository_Branch  = "" # the name of the branch of the remote repository of git

##### -- Function Start -- #####


## -- { Init Function } -- ##


## -- {Function 9 -- Git} -- ##
function My-Git {
    if ($null -eq $Remote_Repository_Address -and "" -eq $Remote_Repository_Address) {
        Write-Output "You have to set the git remote repository address first"
        return
    } elseif ($null -eq $Remote_Repository_Branch -and "" -eq $Remote_Repository_Branch) {
        Write-Output "You have to set the git remote repository branch first"
        return
    } elseif (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Output "Git is not installed"
        return
    }

    git add .
    # get current date
    $date = Get-Date -Format "yyMMdd"
    git commit -m $date
    # git push origin main
    git push $Remote_Repository_Address $Remote_Repository_Branch
}


## -- {Function 12 -- Reload Script } -- ##
function Reload-Script {
    . $My_Script_Path
}

## -- Set the alias -- ##

Set-Alias    -Name mygit    -Value My-Git
Set-Alias    -Name grep     -Value findstr
Set-Alias    -Name reload   -Value Reload-Script

##### -- Function End -- #####

# load script library

$core_home = Join-Path -Path $My_Script_Dir -ChildPath "core"
Get-ChildItem (Join-Path -Path $core_home -ChildPath "*.ps1") | ForEach-Object { . $_.FullName }

$apps_home = Join-Path -Path $My_Script_Dir -ChildPath "apps"
Get-ChildItem (Join-Path -Path $apps_home -ChildPath "*.ps1") | ForEach-Object { . $_.FullName }

$utils_home = Join-Path -Path $My_Script_Dir -ChildPath "utils"
Get-ChildItem (Join-Path -Path $utils_home -ChildPath "*.ps1") | ForEach-Object { . $_.FullName }

##### --- Module --- #####

. $My_Script_Dir\module\module.PSReadLine.ps1
. $My_Script_Dir\module\module.Get-ChildItemColor.ps1
. $My_Script_Dir\module\module.PSFzf.ps1


