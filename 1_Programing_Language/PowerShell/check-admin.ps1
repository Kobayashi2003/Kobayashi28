# first, check if the powershell script is running as admin
# if not, then relaunch the script as admin
$wid=[System.Security.Principal.WindowsIdentity]::GetCurrent()
$prp=new-object System.Security.Principal.WindowsPrincipal($wid)
if (-not $prp.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator))
{
    Start-Process powershell.exe "-File",('"{0}"' -f $MyInvocation.MyCommand.Path) -Verb RunAs
    exit
}

# then, check if the registry key exists
# if not, then create the registry key
$regkey = "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32"
if (-not (Test-Path "Registry::$regkey"))
{
    # reg add $regkey /f /ve
    Write-Output "Registry key does not exist, do you want to create it? (y/n)"
    $response = Read-Host
    if ($response -eq "y")
    {
        reg add $regkey /f /ve
    }
}
# if the registry key exists, then delete the registry key
else
{
    # reg delete $regkey /va /f
    Write-Output "Registry key exists, do you want to delete it? (y/n)"
    $response = Read-Host
    if ($response -eq "y")
    {
        reg delete $regkey /va /f
    }
}
