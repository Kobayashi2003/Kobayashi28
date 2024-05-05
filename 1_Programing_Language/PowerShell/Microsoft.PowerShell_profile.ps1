using namespace System.Management.Automation
using namespace System.Management.Automation.Language

$My_Script_Path  = $MyInvocation.MyCommand.Definition
$My_Script_Dir   = Split-Path $My_Script_Path
$My_History_Filename = "my-history.txt"
$My_History_Path = $My_Script_Dir + "\" + $My_History_Filename

$Start_Conda = $false
$Conda_Path = "" # the path of conda.exe
$Remote_Repository_Address = "" # the address of the remote repository of git
$Remote_Repository_Branch  = "" # the name of the branch of the remote repository of git


##### -- Function Start -- #####


#region conda initialize
# !! Contents within this block are managed by 'conda init' !!
function Conda-Init {
    if (-not (Test-Path $Conda_Path)) {
        return $false
    }
    try {
        (& $Conda_Path "shell.powershell" "hook") | Out-String | Invoke-Expression
        (& $Conda_Path config --set changeps1 False)
    } catch {
        return $false
    }
    return $true
}
#endregion

## -- { Init Function } -- ##

$default_title = "Windows PowerShell"
$default_color = "White"
$default_background_color = "Black"

$current_title = $Host.UI.RawUI.WindowTitle
$current_color = $Host.UI.RawUI.ForegroundColor
$current_background_color = $Host.UI.RawUI.BackgroundColor

$bufsize = $Host.UI.RawUI.BufferSize
$uisize  = $Host.UI.RawUI.WindowSize


function Format-Status {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$true)]
        [Alias('m')]
        [string] $Message,

        [Parameter(Mandatory=$true, ParameterSetName="Task")]
        [Alias('t')]
        [scriptblock] $Task,

        [Parameter(Mandatory=$true, ParameterSetName="Status")]
        [Alias('s')]
        [bool] $Status,

        [Alias('ff')]
        [System.ConsoleColor] $ForegroundColorFalse = "Red",

        [Alias('bf')]
        [System.ConsoleColor] $BackgroundColorFalse = $current_background_color,

        [Alias('ft')]
        [System.ConsoleColor] $ForegroundColorTrue = "Green",

        [Alias('bt')]
        [System.ConsoleColor] $BackgroundColorTrue = $current_background_color,

        [Alias('p')]
        [int] $Pading = 80,

        [Alias('mf')]
        [string] $MessageFalse = "ERROR",

        [Alias('mt')]
        [string] $MessageTrue = "OK",

        [switch] $ReturnStatus
    )

    Write-Host $message -NoNewline

    if ($PSCmdlet.ParameterSetName -eq "Task") {
        try {
            $Status = & $Task
        } catch {
            $Status = $false
        }
    }

    if ($Status) {
        $status_message = $MessageTrue
        $ForegroundColor = $ForegroundColorTrue
        $BackgroundColor = $BackgroundColorTrue
    } else {
        $status_message = $MessageFalse
        $ForegroundColor = $ForegroundColorFalse
        $BackgroundColor = $BackgroundColorFalse
    }

    $Pading = $Pading - $Message.Length
    if ($Pading + $Message.Length + $status_message.Length + 4 -gt $bufsize.Width) {
        $Pading = $bufsize.Width - $Message.Length - $status_message.Length - 5
    }
    if ($Pading -lt 0) {
        $Pading = 0
    }

    Write-Host "".PadRight($Pading), "[ " -NoNewline

    if ($ForegroundColor -and $BackgroundColor) {
        Write-Host $status_message -ForegroundColor:$ForegroundColor -BackgroundColor:$BackgroundColor -NoNewline
    } elseif ($ForegroundColor) {
        Write-Host $status_message -ForegroundColor:$ForegroundColor -NoNewline
    } elseif ($BackgroundColor) {
        Write-Host $status_message -BackgroundColor:$BackgroundColor -NoNewline
    } else {
        Write-Host $status_message -NoNewline
    }

    Write-Host " ]"

    if ($ReturnStatus) {
        return $Status
    }
}

function Format-Color {
    # https://duffney.io/usingansiescapesequencespowershell/#text-styling
    [CmdletBinding()]
    param (
        [Parameter(ValueFromPipeline=$true, ParameterSetName='Formatter')]
        [Alias('m')]
        [string]
        $Message,

        [Parameter(ParameterSetName="Formatter")]
        [Alias("f")] # foreground color
        [ArgumentCompleter({ param (
            $commandName,
            $parameterName,
            $wordToComplete,
            $commandAst,
            $fakeBoundParameters )
            @(
                "Black"   , "DarkRed"    , "DarkGreen", "DarkYellow",
                "DarkBlue", "DarkMagenta", "DarkCyan" , "Gray",
                "DarkGray", "Red"        , "Green"    , "Yello",
                "Blue"    , "Magenta"    , "Cyan"     , "White"
            ) | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object { $_ } })]
        $ForegroundColor,

        [Parameter(ParameterSetName="Formatter")]
        [Alias("b")] # background color
        [ArgumentCompleter({ param (
            $commandName,
            $parameterName,
            $wordToComplete,
            $commandAst,
            $fakeBoundParameters )
            @(
                "Black"   , "DarkRed"    , "DarkGreen", "DarkYellow",
                "DarkBlue", "DarkMagenta", "DarkCyan" , "Gray",
                "DarkGray", "Red"        , "Green"    , "Yello",
                "Blue"    , "Magenta"    , "Cyan"     , "White"
            ) | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object { $_ } })]
        $BackgroundColor,

        [Parameter(ParameterSetName="ShowColorTable")]
        [switch]
        $ShowColorTable
    )

    begin {

        $colorMapping = @{
            "Black"   = 30; "DarkRed"    = 31; "DarkGreen" = 32; "DarkYellow" = 33
            "DarkBlue"= 34; "DarkMagenta"= 35; "DarkCyan"  = 36; "Gray"       = 37
            "DarkGray"= 90; "Red"        = 91; "Green"     = 92; "Yellow"      = 93
            "Blue"    = 94; "Magenta"    = 95; "Cyan"      = 96; "White"      = 97
        }

        function Get-ColorTable {
            $esc = $([char]27)
            Write-Host "`n$esc[1;4m256-Color Foreground & Background Charts$esc[0m"
            foreach ($fgbg in 38, 48) { # background/foreground switch
                foreach ($color in 0..255) {
                    # color range
                    # Display the colors
                    $field = "color".PadLeft(4) # pad the chart boxes with spaces
                    Write-Host -NoNewLine "$esc[$fgbg;5;${color}m$field $esc[0m"
                    # Display 8 colors per line
                    if ( ($color + 1) % 8 -eq 0 ) { Write-Host } # new line
                }
                Write-Host
            }
        }

        function ParseColor { param ($value)
            if ($null -eq $value) {
                throw "The color is empty"
            }
            elseif ($value -is [string]) {
                if ($colorMapping.ContainsKey($value)) {
                    Write-Output $colorMapping[$value]
                }
            }
            elseif ($value -is [int]) {
                if ($value -ge 0 -and $value -le 255) {
                    Write-Output $value
                } else {
                    throw "The color number should be between 0 and 255"
                }
            }
            elseif ($value -is [System.ConsoleColor]) {
                Write-Output $colorMapping[$value.ToString()]
            }
            else {
                throw "The color is not ligal"
            }
        }

        $colorMapping = @{
            "Black"   = 30; "DarkRed"    = 31; "DarkGreen" = 32; "DarkYellow" = 33
            "DarkBlue"= 34; "DarkMagenta"= 35; "DarkCyan"  = 36; "Gray"       = 37
            "DarkGray"= 90; "Red"        = 91; "Green"     = 92; "Yellow"      = 93
            "Blue"    = 94; "Magenta"    = 95; "Cyan"      = 96; "White"      = 97
        }

        $esc = $([char]27)
        $backgroundSwitch = 48
        $foregroundSwitch = 38

        $ansiParam = @()
        if ($null -ne $PSBoundParameters["ForegroundColor"]) {
            if ($ForegroundColor -is [string]) {
                $ansiParam += "5;$(ParseColor $ForegroundColor)".Trim()
            }
            else {
                $ansiParam += "$foregroundSwitch;5;$(ParseColor $ForegroundColor)".Trim()
            }
        }
        if ($null -ne $PSBoundParameters["BackgroundColor"]) {
            if ($BackgroundColor -is [string]) {
                $ansiParam += "5;$((ParseColor $BackgroundColor)+10)".Trim()
            }
            elseif ($BackgroundColor -is [int]) {
                $ansiParam += "$backgroundSwitch;5;$((ParseColor $BackgroundColor))".Trim()
            }
            elseif ($BackgroundColor -is [System.ConsoleColor]) {
                $ansiParam += "5;$((ParseColor $BackgroundColor)+10)".Trim()
            }
        }
    }

    process {
        $current = $_
        if ($PSCmdlet.ParameterSetName -eq "ShowColorTable") {
            Get-ColorTable
        } else {
            if ([string]::IsNullOrEmpty($current)) {
                $current = $Message
            }
            if ($ansiParam.Count -gt 0) {
                Write-Output "$esc[$($ansiParam -join ';')m$current$esc[0m"
            }
            else {
                Write-Output $current
            }
        }
    }

    end {}
}

function My-Check-Admin {
    $admin = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    if ($admin.IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator") -eq $false) {
        return $false
    }
    return $true
}

function My-Check-Module {
    param (
        [Parameter(Mandatory=$true)]
        [string]
        $module_name,

        [Parameter(Mandatory=$false)]
        [string]
        $module_version = $null
    )
    $module = Get-Module -ListAvailable | Where-Object { $_.Name -eq $module_name }
    if ($module.Count -gt 1) {
        $module = $module | Sort-Object -Property Version -Descending | Select-Object -First 1
    }

    if ($null -eq $module) {
        return $false
    }
    if ($null -ne $module_version -and $module_version -ne "") {
        if ($module.Version -lt $module_version) {
            return $false
        }
    }

    return $true
}

function My-Get-UI-Infor {
    $info = (Get-Host).UI.RawUI
    foreach ($prop in $info | Get-Member -MemberType Property) {
        $name = $prop.Name
        $value = $info.$name
        $name = '| RawUI.' + $name.PadRight(25) + ' |'
        if ($value -ne $null) {
            Format-Status -Message $name -Status $true -MessageTrue $value -ForegroundColorTrue "Cyan"
        } else {
            Format-Status -Message $name -Status $false -MessageFalse "null" -ForegroundColorFalse "Red"
        }
    }
}

function My-Check-Environment {
    $esc = $([char]27)
    Write-Host "$esc[1;3;4;$(93)mChecking Environment...$esc[0m"

    if ($My_Script_Path -ne $PROFILE) {
        $message = "The path of the script is not the same as the path of the profile"
        Format-Status -Message $message -Status $false -MessageFalse "Error" -ForegroundColorFalse "Red"
    } else {
        $message = "The path of the script is the same as the path of the profile"
        Format-Status -Message $message -Status $true -MessageTrue "OK" -ForegroundColorTrue "Green"
    }

    $message = "Checking Admin Permission..."
    Format-Status -Message $message -Task { My-Check-Admin } -MessageTrue "Admin" -MessageFalse "User"

    $modules2check = @(
        "Get-ChildItemColor",
        "PSReadline",
        "PSColor"
    )

    $modules_version = @{
        "PSReadline" = "2.2.6"
    }

    foreach ($module in $modules2check) {
        $message = "Checking Module $module..."
        if ($null -ne $modules_version[$module] -and $modules_version[$module] -ne "") {
            $status = Format-Status -Message $message -Task { My-Check-Module -module_name $module -module_version $modules_version[$module] } -MessageTrue "Installed" -MessageFalse "Not Installed" -ReturnStatus
        } else {
            $status = Format-Status -Message $message -Task { My-Check-Module -module_name $module } -MessageTrue "Installed" -MessageFalse "Not Installed" -ReturnStatus
        }
        if (-not $status) {
            if ($null -eq $modules_version[$module] -or $modules_version[$module] -eq "") {
                $message = "Installing Module $module..."
                Format-Status -Message $message -Task { Install-Module -Name $module -Scope CurrentUser -Force } -MessageTrue "Installed" -MessageFalse "Error"
            } else {
                $message = "Uninstalling old version of Module $module..."
                Format-Status -Message $message -Task { Uninstall-Module -Name $module -Force -AllVersions } -MessageTrue "Uninstalled" -MessageFalse "Error"
                $message = "Installing Module $module..."
                Format-Status -Message $message -Task { Install-Module -Name $module -Scope CurrentUser -Force -RequiredVersion $modules_version[$module] } -MessageTrue "Installed" -MessageFalse "Error"
            }
        }
    }

    # if .powershell_config is not exist, create it silently
    if (-not (Test-Path "$My_Script_Dir\.powershell_config")) {
        New-Item -Path $My_Script_Dir -Name ".powershell_config" -ItemType "file" -Force | Out-Null
        Add-Content -Path "$My_Script_Dir\.powershell_config" -Value "Start_Conda=false"
        Add-Content -Path "$My_Script_Dir\.powershell_config" -Value "Conda_Path="
        Add-Content -Path "$My_Script_Dir\.powershell_config" -Value "Remote_Repository_Address="
        Add-Content -Path "$My_Script_Dir\.powershell_config" -Value "Remote_Repository_Branch="
    }

    if (-not $global:Conda_Path -or -not (Test-Path $global:Conda_Path)) {
        # try to open .powershell_config in current directory to get the path of conda
        try {
            $conda_path = (Get-Content -Path "$My_Script_Dir\.powershell_config" -Raw).Split("`n") |
                 Where-Object { $_ -like "Conda_Path*" } |
                    ForEach-Object { $_.Split("=")[-1].Trim() }
        } catch {
            $conda_path = $null
        }
        if ($null -ne $conda_path -and $conda_path -ne "") {
            $global:Conda_Path = $conda_path
            $start_conda = (Get-Content -Path "$My_Script_Dir\.powershell_config" -Raw).Split("`n") |
                Where-Object { $_ -like "Start_Conda*" } |
                    ForEach-Object { $_.Split("=")[-1].Trim() }
            if ($null -ne $start_conda -and "true" -eq $start_conda.ToLower()) {
                $global:Start_Conda = $true
            }
        }
    }

    if (-not $global:Remote_Repository_Address -or -not $global:Remote_Repository_Branch) {
        # try to open .powershell_config in current directory to get the path of conda
        try {
            $remote_repository_address = (Get-Content -Path "$My_Script_Dir\.powershell_config" -Raw).Split("`n") |
                Where-Object { $_ -like "Remote_Repository_Address*" } |
                    ForEach-Object { $_.Split("=")[-1].Trim() }
        } catch {
            $remote_repository_address = $null
        }
        try {
            $remote_repository_branch = (Get-Content -Path "$My_Script_Dir\.powershell_config" -Raw).Split("`n") |
                Where-Object { $_ -like "Remote_Repository_Branch*" } |
                    ForEach-Object { $_.Split("=")[-1].Trim() }
        } catch {
            $remote_repository_branch = $null
        }
        if ($null -ne $remote_repository_address -and $remote_repository_address -ne "") {
            $global:Remote_Repository_Address = $remote_repository_address
        }
        if ($null -ne $remote_repository_branch -and $remote_repository_branch -ne "") {
            $global:Remote_Repository_Branch = $remote_repository_branch
        }
    }

    if (-not $global:Conda_Path -or -not (Test-Path $global:Conda_Path)) {
        $message = "The path of Conda is not set or the path is invalid"
        Format-Status -Message $message -Status $false -MessageFalse "Error" -ForegroundColorFalse "Red"
    } else {
        $message = "The path of Conda is set"
        Format-Status -Message $message -Status $true -MessageTrue "OK" -ForegroundColorTrue "Green"
        if ($global:Start_Conda) {
            $message = "Initializing Conda..."
            Format-Status -Message $message -Task { Conda-Init } -MessageTrue "Init" -MessageFalse "Error"
        }
    }

    My-Get-UI-Infor

    $name = '| ' + "PowerShell Version".PadRight(31) + ' |'
    $value = $PSVersionTable.PSVersion
    Format-Status -Message $name -Status $true -MessageTrue $value

    Write-Host "$esc[1;3;4;$(93)mWelcome to Windows PowerShell, $env:USERNAME!$esc[0m"
}
My-Check-Environment

function Prompt {
    $lst_cmd_state = $?
    $esc = $([char]27)
    $time = "$esc[1;32m$esc[1;4m" + (Get-Date -Format "HH:mm:ss") + "$esc[0m" # green and italic
    if (-not $lst_cmd_state) {
        $time = "$esc[1;31m$esc[1;4m" + (Get-Date -Format "HH:mm:ss") + "$esc[0m" # red and italic
    } else {
        $time = "$esc[1;32m$esc[1;4m" + (Get-Date -Format "HH:mm:ss") + "$esc[0m" # green and italic
    }
    $path = ($PWD.Path).Replace($env:USERPROFILE, "~") # replace the user profile with ~
    $conda_env = $env:CONDA_DEFAULT_ENV
    if ($null -ne $conda_env -and $conda_env -ne "") {
        return "$esc[1;33m$esc[1;4m($conda_env)$esc[0m $time $path" + " > "
    }
    return "$time $path > "
}

function My-Set-Title {
    param (
        [Parameter(Mandatory=$true)]
        [string] $title
    )
    try {
        $host.ui.RawUI.WindowTitle = $title
    } catch {
        $host.ui.RawUI.WindowTitle = $default_title
        throw "The title is not ligal, the title is set to default"
    }
}

function My-Set-Color {
    param (
        [Parameter(Mandatory=$true)]
        [ArgumentCompleter({ param (
            $commandName,
            $parameterName,
            $wordToComplete,
            $commandAst,
            $fakeBoundParameters )
            @(
                "Black"   , "DarkBlue", "DarkGreen", "DarkCyan",
                "DarkRed" , "DarkMagenta", "DarkYellow", "Gray",
                "DarkGray", "Blue"    , "Green"    , "Cyan",
                "Red"     , "Magenta" , "Yellow"   , "White"
            ) | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object { $_ } })]
        [string] $color
    )
    try {
        $host.ui.RawUI.ForegroundColor = $color
    } catch {
        $host.ui.RawUI.ForegroundColor = $default_color
        throw "The color is not ligal, the color is set to default."
    }
}

function My-Set-BackgroundColor { param ( [string] $color )
    param (
        [Parameter(Mandatory=$true)]
        [ArgumentCompleter({ param (
            $commandName,
            $parameterName,
            $wordToComplete,
            $commandAst,
            $fakeBoundParameters )
            @(
                "Black"   , "DarkBlue", "DarkGreen", "DarkCyan",
                "DarkRed" , "DarkMagenta", "DarkYellow", "Gray",
                "DarkGray", "Blue"    , "Green"    , "Cyan",
                "Red"     , "Magenta" , "Yellow"   , "White"
            ) | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object { $_ } })]
        [string] $color
    )
    try {
        $host.ui.RawUI.BackgroundColor = $color
    } catch {
        $host.ui.RawUI.BackgroundColor = $default_background_color
        throw "The background color is not ligal, the background color is set to default."
    }
}


## -- {Function 1 -- Start Or Kill a Process} -- ##
function My-Start-or-Kill {
    param (
        [string]
        $app_path,
        [string]
        $state = "start"
    )

    $app_name = ($app_path.Split("\")[-1]).Split(".")[-2]
    if ($state -eq "start") { # Start Process
        Start-Process $app_path
        Format-Status -Message $app_name -Status $true -MessageTrue "Run" -ForegroundColorTrue "Green" -BackgroundColorTrue $current_background_color
    } elseif ($state.startswith("k")) { # Kill Process
        Stop-Process -ProcessName $app_name
        Format-Status -Message $app_name -Status $false -MessageFalse "Kill" -ForegroundColorFalse "Red" -BackgroundColorFalse $current_background_color
    } elseif ($state.startswith("p")) { # show the paths
        Write-Output $app_path
    }
}


## -- {Function 2 -- Edit this Script} -- ##
function My-Script {
    Get-Item -Path $My_Script_Path | Select-Object -Property * | Format-List -Property * | Write-Output
}


## -- {Function 3 -- Show all Applications Paths} -- ##
function My-Show-Applications {
    # echo $My_Script_Path
    # Write-Output "===================="
    # (Get-Content -Path $My_Script_Path -Raw).Split(";")[-1] | Write-Output
    # Write-Output "===================="
    (Get-Item Function:) | Where-Object { $_.Name -like "App-*" } | Write-Output
}


## -- {Function 4 -- Delete a Application Path} -- ##
function My-Delete-App {
    param (
        [parameter(Mandatory=$true)]
        [string]
        $app_name
    )
    if ($app_name -eq "") {
        throw "You have to enter an application name"
    }
    $app_name = "App-" + $app_name
    $pattern1 = "# $app_name"
    $content1 = Select-String -Path $My_Script_Path -Pattern $pattern1
    $pattern2 = "# END $app_name"
    $content2 = Select-String -Path $My_Script_Path -Pattern $pattern2

    if ($null -eq $content1 -or $null -eq $content2) {
        throw "The application is not found"
    }

    $line1 = $content1.ToString().Split(":")[-2] - 1
    $line2 = $content2.ToString().Split(":")[-2] - 1

    $len = $line2 - $line1 + 1

    $old_content = Get-Content -Path $My_Script_Path -ReadCount 0
    $new_content = @()
    for($i = 0; $i -lt $old_content.Length; $i += 1) {
        if ($i -gt $line1-1 -and $i -lt $line1+$len+1 ) {
            # echo $old_content[$i]
        } else {
            $new_content += $old_content[$i]
        }
    }
    Set-Content -Path $My_Script_Path -Value $new_content

    Format-Color -Message "Delete $app_name" -ForegroundColor "Green" -BackgroundColor $current_background_color
}


## -- {Function 5 -- Add a Application Path} -- ##
function My-Add-App {
    param (
        [parameter(Mandatory=$true)]
        [string] $app_name,
        [parameter(Mandatory=$true)]
        [string] $app_path
        )
    $app_name_tmp = $app_name
    $app_name = "App-" + $app_name
    $content = Get-Content $My_Script_Path
    if ("# $app_name" -in $content) {
        Write-Output "This path already exists. Do you want to overwrite it? (Y/[N])"
        $judge = Read-Host
        if ($judge -eq "Y") {
            My-Delete-App $app_name_tmp
        } else {
            Format-Status -Message "Add $app_name" -Status "False" -MessageFalse "Fail" -ForegroundColorFalse "Red" -BackgroundColorFalse $current_background_color
            return
        }
    }
    Add-Content $My_Script_Path "`n# $app_name`nfunction $app_name(`$state`=`"start`") {`n    `$app_path = `'$app_path`'`n    My-Start-or-Kill `$app_path `$state`n}`n`# END $app_name"
    Format-Status -Message "Add $app_name" -Status "True" -MessageTrue "Success" -ForegroundColorTrue "Green" -BackgroundColorTrue $current_background_color
}


## -- {Function 6 -- Make a new file and go to the file} -- ##
function My-Mkdir-and-CD {
    param (
        [parameter(Mandatory=$true)]
        [string] $dirname )
    mkdir $dirname
    Set-Location $dirname
}


## -- {Function 7 -- Forward the ports of WSL to Windows} -- ##
function My-Forward-Port { # (abaondoned)
    param ( [string] $port )

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
function My-Set-Hook {
    $global:hook = Get-Location
    Write-Output "Hooks Set"
}

# Go to the path that is set by My-Set-Hook
function My-Go-Hook {
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
function My-Git {
    if ($null -eq $Remote_Repository_Address -or "" -eq $Remote_Repository_Address) {
        Write-Output "You have to set the git remote repository address first"
        return
    } elseif ($null -eq $Remote_Repository_Branch -or "" -eq $Remote_Repository_Branch) {
        Write-Output "You have to set the git remote repository branch first"
        return
    }
    git add .
    # get current date
    $date = Get-Date -Format "yyMMdd"
    git commit -m $date
    # git push origin main
    git push $Remote_Repository_Address $Remote_Repository_Branch
}


## -- {Function 10 -- Get the CPU temperature} -- ##
function My-Get-CPU-Temperature { # get the temperature of the CPU
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


function Get-CmdletAlias ($cmdletname) {
    Get-Alias | Where-Object -FilterScript { $_.Definition -like "$cmdletname" } |
        Format-Table -Property Definition, Name -AutoSize

}


## -- Set the alias -- ##

Set-Alias    -Name shook    -Value My-Set-Hook
Set-Alias    -Name ghook    -Value My-Go-Hook
Set-Alias    -Name mkcd     -Value My-Mkdir-and-CD
Set-Alias    -Name addapp   -Value My-Add-App
Set-Alias    -Name delapp   -Value My-Delete-App
Set-Alias    -Name showapp  -Value My-Show-Applications
Set-Alias    -Name mygit    -Value My-Git
Set-Alias    -Name cputemp  -Value My-Get-CPU-Temperature
Set-Alias    -Name grep     -Value findstr
Set-Alisa    -Name shut     -Value shutdown

##### -- Function End -- #####




##### -- My Scripts Start -- #####

# accept all the parameters then pass them to the script $My_Script_Dir\main.py
function My-ImgAsst { # TODO
    param(
        [Parameter(Mandatory=$true, ValueFromPipeline=$true)]
        [Alias('v')]
        [string]
        $values
    )
    BEGIN {}
    # pass the parameters to the script
    PROCESS {
        python.exe $My_Script_Dir\ImgAsst\main.py $values
    }
    END {}
}

function My-FileExplorer { # TODO
    python.exe $My_Script_Dir\FileExplorer\main.py
}

## Atlas200Dk Function Start
function My-Connect-Atlas200Dk { # this function is used to connect to Atlas200Dk (only for Windows) (abaondoned)
    $ips = arp -a -N 192.168.137.1 | Select-String -Pattern "192.168.137.[0-9]+" | Select-Object -Skip 1 | ForEach-Object { $_.ToString().Trim().Split(" ")[0] }
    $ip = $ips[0]
    if ($null -eq $ip) {
        Write-Output "Atlas200Dk is not connected"
        return
    }
    ssh HwHiAiUser@$ip
}
## Atlas200Dk Function End

# set the alias
Set-Alias -Name img -Value My-ImgAsst
Set-Alias -Name fe  -Value My-FileExplorer

##### -- my scripts End -- #####




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

# [F1]      : CommandHelp (open the help window of the current command)
# [F3]      : ShowBinding (show the binding of the current key)
# [F7]      : History (show the history)

# [Backspace]: SmartBackspace (delete previous character or matching quotes/parens/braces)

# [Ctrl + b]: BuildCurrentDirectory (build the current directory)

# [Ctrl + R]: ReverseSearchHistory (search the history)
# [Ctrl + S]: ForwardSearchHistory (search the history)

# [Ctrl + q]: TabCompleteNext (Tab acts like in bash)
# [Ctrl + Q]: TabCompletePrevious (Tab acts like in bash)

# [Ctrl + C]: Copy (clipboard interaction)
# [Ctrl + v]: Paste (clipboard interaction)
# [Ctrl + V]: PasteAsHereString (paste the clipboard text as a here string)

# [Ctrl + J]: MarkDirectory (mark the current directory)
# [Ctrl + j]: JumpToMarkDirectory (jump to the marked directory)
# [Alt + j]: ShowMarkDirectories (show the marked directories)

# [Ctrl + Backspace]: ShellBackwardKillWord (delete the word before the cursor)
# [Ctrl + LeftArrow]: ShellBackwardWord (move the cursor to the start of the word before the cursor)
# [Ctrl + RightArrow]: ShellForwardWord (move the cursor to the end of the word after the cursor)

# [Ctrl + d, Ctrl + c]: CaptureScreen (good for blog posts or email showing a transaction of what you did when asking for help or demonstrating a technique)

# [Alt + a]: SlectCommandArgument (select the command argument)

# [Alt + w] : SaveInHistory (save the current command in the history but do not execute it)

# [Alt + d]: ShellKillWord (delete the word before the cursor)
# [Alt + b]: ShellBackwardWord (move the cursor to the start of the word before the cursor)
# [Alt + f]: ShellForwardWord (move the cursor to the end of the word after the cursor)
# [Alt + B]: SelectShellBackwardWord (select the word before the cursor)
# [Alt + F]: SelectShellForwardWord (select the word after the cursor)

# [Alt + (]: ParenthesizeSelection (put parens around the current selection or line)
# [Alt + ']: ToggleQuoteArgument (change the token under or before the cursor)
# [Alt + "]: ToggleQuoteArgument (change the token under or before the cursor and move the cursor to the end of the token)

# [Alt + %]: ExpandAlias (Replace all aliases with the full command)

# [Alt + Backspace]: ShellBackwardKillWord (delete the word before the cursor)



# import the module
Import-Module PSReadline

Set-PSReadLineOption -EditMode Emacs
Set-PSReadLineOption -BellStyle None

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
Set-PSReadLineOption -HistorySavePath $My_History_Path
Set-PSReadLineOption -HistorySaveStyle SaveIncrementally

$history_save_path = (Get-PSReadLineOption).HistorySavePath

# set the filter for the history
Set-PSReadLineOption -AddToHistoryHandler {
    param([string]$line)

    $sensitive = "password|asplaintext|token|key|secret|galgame|eroi"
    return ($line -notmatch $sensitive)
}

# prediction configuration
Set-PSReadLineOption -PredictionSource History
Set-PSReadLineOption -PredictionViewStyle ListView

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

# Auto correct common typos
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
        'conda' {
            $condaCmdBase = $CommandAst.CommandElements[0].Extent
            $condaCmdArg = $CommandAst.CommandElements[1].Extent
            switch ($condaCmdArg.Text) {
                'a' {
                    [Microsoft.PowerShell.PSConsoleReadLine]::Replace(
                        $condaCmdArg.StartOffset, $condaCmdArg.EndOffset - $condaCmdArg.StartOffset, 'activate')
                }
                'd' {
                    [Microsoft.PowerShell.PSConsoleReadLine]::Replace(
                        $condaCmdArg.StartOffset, $condaCmdArg.EndOffset - $condaCmdArg.StartOffset, 'deactivate')
                }
                'i' {
                    [Microsoft.PowerShell.PSConsoleReadLine]::Replace(
                        $condaCmdBase.StartOffset, $condaCmdArg.EndOffset - $condaCmdBase.StartOffset, 'Conda-Init')
                }
            }
        }
    }
}
# This checks the validation script when you hit enter
Set-PSReadLineKeyHandler -Chord Enter -Function ValidateAndAcceptLine


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

### Module PSReadLine End ###


##### --- Module End --- #####


# please let this ';' be the last ';' in this file
;
### User's Paths ###

# Clash for Windows (abaondoned)
function App-Clash($state="start") {
    $app_path = 'D:\Item\Clash for Windows\Clash for Windows.exe'
    My-Start-or-Kill $app_path $state > $null
}
# END Clash for Windows


# Free Download Manager (abandoned)
function App-FDM($state="start") {
    $app_path = 'D:\Item\Free Download Manager\fdm.exe'
    My-Start-or-Kill $app_path $state
}
# END Free Download Manager


# Everything
function App-Everything($state="start") {
    $app_path = 'D:\Item\Everything\Everything.exe'
    My-Start-or-Kill $app_path $state
}
# END Everything


# ShareMouse (abandoned)
function App-ShareMouse($state="start") {
    if ($state -eq "KEY") {
        Write-Output "SMOENT-DO-AAGEMY-1299-UN-KKPX-QTSX-X9JHRR1LXHX5ZXTB-FEEB32EF75C43CE5F220B324678701CB" | Set-Clipboard
        return
    }
    $app_path = 'C:\Program Files (x86)\ShareMouse\ShareMouse.exe'
    My-Start-or-Kill $app_path $state
}
# END ShareMouse


# CodeServer (abandoned)
function App-CodeServer { # the application in wsl
    wsl.exe -- /mnt/d/Program/code-server-3.10.2-linux-amd64/code-server /mnt/d/Program/Code
}
# End CodeServer